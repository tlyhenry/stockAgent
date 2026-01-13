from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Iterable, Sequence


@dataclass(frozen=True)
class Source:
    name: str
    url: str
    published_date: date | None = None


@dataclass(frozen=True)
class Evidence:
    source: Source
    excerpt: str
    score: float


@dataclass(frozen=True)
class Claim:
    text: str
    source: Source
    confidence: float


@dataclass(frozen=True)
class QueryScope:
    question: str
    timeframe: str | None = None
    categories: Sequence[str] = field(default_factory=tuple)


@dataclass(frozen=True)
class Answer:
    response: str
    key_facts: Sequence[str]
    sources: Sequence[Source]
    notes: Sequence[str] = field(default_factory=tuple)

    def as_markdown(self) -> str:
        lines: list[str] = ["Answer", "", self.response, "", "Key facts"]
        lines.extend([f"- {fact}" for fact in self.key_facts])
        lines.append("")
        lines.append("Sources")
        for source in self.sources:
            line = f"- {source.name}: {source.url}"
            if source.published_date:
                line += f" ({source.published_date.isoformat()})"
            lines.append(line)
        if self.notes:
            lines.append("")
            lines.append("Notes")
            lines.extend([f"- {note}" for note in self.notes])
        return "\n".join(lines)


def unique_sources(evidence: Iterable[Evidence]) -> list[Source]:
    seen: set[str] = set()
    sources: list[Source] = []
    for item in evidence:
        key = f"{item.source.name}|{item.source.url}"
        if key in seen:
            continue
        seen.add(key)
        sources.append(item.source)
    return sources
