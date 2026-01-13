from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Protocol

from stock_agent.models import Evidence, Source


class DataSource(Protocol):
    def search(self, query: str) -> Iterable[Evidence]:
        ...


@dataclass(frozen=True)
class InMemoryRecord:
    source: Source
    text: str


class InMemorySource:
    def __init__(self, records: Iterable[InMemoryRecord]) -> None:
        self._records = list(records)

    def search(self, query: str) -> Iterable[Evidence]:
        lowered = query.lower()
        for record in self._records:
            if lowered in record.text.lower():
                yield Evidence(source=record.source, excerpt=record.text, score=1.0)


class TextFileSource:
    def __init__(self, source: Source, path: Path) -> None:
        self._source = source
        self._path = path

    def search(self, query: str) -> Iterable[Evidence]:
        if not self._path.exists():
            return []
        content = self._path.read_text(encoding="utf-8")
        if query.lower() not in content.lower():
            return []
        return [Evidence(source=self._source, excerpt=content, score=0.5)]
