from __future__ import annotations

from typing import Iterable

from stock_agent.data_sources import DataSource
from stock_agent.models import Evidence


class Retriever:
    def __init__(self, sources: Iterable[DataSource]) -> None:
        self._sources = list(sources)

    def search(self, query: str) -> list[Evidence]:
        evidence: list[Evidence] = []
        for source in self._sources:
            evidence.extend(source.search(query))
        return sorted(evidence, key=lambda item: item.score, reverse=True)
