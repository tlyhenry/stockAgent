from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Iterable

from stock_agent.fact_store import FactStore
from stock_agent.llm import LLMClient
from stock_agent.models import Answer, Claim, Evidence, QueryScope, Source, unique_sources
from stock_agent.retriever import Retriever


@dataclass
class AnalystAgent:
    retriever: Retriever
    fact_store: FactStore
    llm: LLMClient | None = None

    def analyze(self, scope: QueryScope) -> Answer:
        evidence = self.retriever.search(scope.question)
        claims = self._extract_claims(evidence)
        for claim in claims:
            self.fact_store.add(claim)
        response = self._compose_response(scope, evidence)
        key_facts = [claim.text for claim in claims] or [
            "No verifiable facts were found for this query."
        ]
        sources = unique_sources(evidence)
        notes = [
            "This answer is based on stored evidence. Add more sources to improve coverage."
        ]
        return Answer(response=response, key_facts=key_facts, sources=sources, notes=notes)

    def _extract_claims(self, evidence: Iterable[Evidence]) -> list[Claim]:
        claims: list[Claim] = []
        for item in evidence:
            excerpt = item.excerpt.strip().replace("\n", " ")
            if not excerpt:
                continue
            summary = excerpt[:180].rstrip()
            claim_text = f"{summary}"
            claims.append(Claim(text=claim_text, source=item.source, confidence=item.score))
        return claims

    def _compose_response(self, scope: QueryScope, evidence: list[Evidence]) -> str:
        if self.llm:
            prompt = self._build_prompt(scope, evidence)
            return self.llm.generate(prompt)
        if not evidence:
            return "No supporting evidence was found in the current data sources."
        top = evidence[0]
        return (
            "Based on available sources, the most relevant historical evidence is: "
            f"{top.excerpt.strip()}"
        )

    def _build_prompt(self, scope: QueryScope, evidence: list[Evidence]) -> str:
        lines = [
            "You are an analyst answering historical questions about Airbnb.",
            f"Question: {scope.question}",
        ]
        if scope.timeframe:
            lines.append(f"Timeframe: {scope.timeframe}")
        if scope.categories:
            lines.append(f"Categories: {', '.join(scope.categories)}")
        lines.append("Evidence:")
        for item in evidence[:5]:
            date_str = item.source.published_date.isoformat() if item.source.published_date else "unknown"
            lines.append(f"- ({date_str}) {item.source.name}: {item.excerpt.strip()}")
        lines.append("Provide a concise answer with key facts and citations.")
        return "\n".join(lines)


def sample_agent() -> AnalystAgent:
    from stock_agent.data_sources import InMemoryRecord, InMemorySource

    sample_source = InMemorySource(
        records=[
            InMemoryRecord(
                source=Source(
                    name="Airbnb Newsroom",
                    url="https://news.airbnb.com/",
                    published_date=date(2022, 5, 1),
                ),
                text="Airbnb introduced Categories in 2022 to help guests discover unique stays.",
            )
        ]
    )
    retriever = Retriever([sample_source])
    return AnalystAgent(retriever=retriever, fact_store=FactStore())
