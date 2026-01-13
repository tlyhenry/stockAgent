from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict


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

    def generate(self, prompt: str) -> str:
        raise NotImplementedError("OpenAI integration not configured yet.")


@dataclass(frozen=True)
class AnthropicClient(LLMClient):
    api_key: str

    def generate(self, prompt: str) -> str:
        raise NotImplementedError("Anthropic integration not configured yet.")


@dataclass(frozen=True)
class GeminiClient(LLMClient):
    api_key: str

    def generate(self, prompt: str) -> str:
        raise NotImplementedError("Gemini integration not configured yet.")


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
