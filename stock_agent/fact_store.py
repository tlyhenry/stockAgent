from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from stock_agent.models import Claim, Source


@dataclass
class FactStore:
    claims: list[Claim]

    def __init__(self) -> None:
        self.claims = []

    def add(self, claim: Claim) -> None:
        self.claims.append(claim)

    def list_by_source(self, source: Source) -> Iterable[Claim]:
        return [claim for claim in self.claims if claim.source == source]
