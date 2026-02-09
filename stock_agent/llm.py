from __future__ import annotations

from dataclasses import dataclass
import json
import os
from typing import Callable, Dict, Optional
from urllib import error, request


class LLMClient:
    def generate(self, prompt: str) -> str:
        raise NotImplementedError


@dataclass(frozen=True)
class MockLLMClient(LLMClient):
    name: str = "mock"

    def generate(self, prompt: str) -> str:
        return f"[mock-response]\n{prompt}"


@dataclass(frozen=True)
class OpenAIClient(LLMClient):
    api_key: str
    model: str = "gpt-4o-mini"
    base_url: str = "https://api.openai.com/v1/chat/completions"

    def generate(self, prompt: str) -> str:
        payload = {
            "model": os.getenv("OPENAI_MODEL", self.model),
            "messages": [{"role": "user", "content": prompt}],
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        response = _post_json(os.getenv("OPENAI_BASE_URL", self.base_url), payload, headers)
        try:
            return response["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise RuntimeError(f"Unexpected OpenAI response shape: {response}") from exc


@dataclass(frozen=True)
class AnthropicClient(LLMClient):
    api_key: str
    model: str = "claude-3-5-sonnet-20240620"
    base_url: str = "https://api.anthropic.com/v1/messages"

    def generate(self, prompt: str) -> str:
        payload = {
            "model": os.getenv("ANTHROPIC_MODEL", self.model),
            "max_tokens": 1024,
            "messages": [{"role": "user", "content": prompt}],
        }
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        }
        response = _post_json(os.getenv("ANTHROPIC_BASE_URL", self.base_url), payload, headers)
        try:
            return response["content"][0]["text"]
        except (KeyError, IndexError, TypeError) as exc:
            raise RuntimeError(f"Unexpected Anthropic response shape: {response}") from exc


@dataclass(frozen=True)
class GeminiClient(LLMClient):
    api_key: str
    model: str = "gemini-1.5-flash"
    base_url: str = "https://generativelanguage.googleapis.com/v1beta/models"

    def generate(self, prompt: str) -> str:
        model = os.getenv("GEMINI_MODEL", self.model)
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
        }
        url = os.getenv("GEMINI_BASE_URL", self.base_url)
        response = _post_json(f"{url}/{model}:generateContent?key={self.api_key}", payload)
        try:
            return response["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError, TypeError) as exc:
            raise RuntimeError(f"Unexpected Gemini response shape: {response}") from exc


class LLMRegistry:
    def __init__(self) -> None:
        self._factories: Dict[str, Callable[..., LLMClient]] = {}

    def register(self, name: str, factory: Callable[..., LLMClient]) -> None:
        self._factories[name] = factory

    def create(self, name: str, **kwargs: str) -> LLMClient:
        if name not in self._factories:
            raise ValueError(f"Unknown LLM provider: {name}")
        return self._factories[name](**kwargs)


def default_registry() -> LLMRegistry:
    registry = LLMRegistry()
    registry.register("mock", lambda **_: MockLLMClient())
    registry.register("openai", lambda api_key: OpenAIClient(api_key=api_key))
    registry.register("anthropic", lambda api_key: AnthropicClient(api_key=api_key))
    registry.register("gemini", lambda api_key: GeminiClient(api_key=api_key))
    return registry


def _post_json(
    url: str,
    payload: Dict[str, object],
    headers: Optional[Dict[str, str]] = None,
) -> Dict[str, object]:
    data = json.dumps(payload).encode("utf-8")
    req_headers = {"Content-Type": "application/json"}
    if headers:
        req_headers.update(headers)
    req = request.Request(url, data=data, headers=req_headers, method="POST")
    try:
        with request.urlopen(req, timeout=60) as response:
            response_data = response.read().decode("utf-8")
    except error.HTTPError as exc:
        error_body = exc.read().decode("utf-8") if exc.fp else ""
        raise RuntimeError(f"LLM request failed ({exc.code}): {error_body}") from exc
    except error.URLError as exc:
        raise RuntimeError(f"LLM request failed: {exc.reason}") from exc
    try:
        return json.loads(response_data)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"LLM returned invalid JSON: {response_data}") from exc
