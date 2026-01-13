from __future__ import annotations

import argparse

from stock_agent.agent import AnalystAgent
from stock_agent.data_sources import InMemoryRecord, InMemorySource
from stock_agent.fact_store import FactStore
from stock_agent.llm import default_registry
from stock_agent.models import QueryScope, Source
from stock_agent.retriever import Retriever


def build_demo_agent() -> AnalystAgent:
    source = InMemorySource(
        records=[
            InMemoryRecord(
                source=Source(
                    name="Airbnb Investor Relations",
                    url="https://investors.airbnb.com/",
                ),
                text="Airbnb filed its Form S-1 in 2020 ahead of its public listing.",
            )
        ]
    )
    retriever = Retriever([source])
    fact_store = FactStore()
    return AnalystAgent(retriever=retriever, fact_store=fact_store)


def main() -> None:
    parser = argparse.ArgumentParser(description="Airbnb analyst agent")
    parser.add_argument("question", help="Question about Airbnb")
    parser.add_argument("--provider", default="mock", help="LLM provider name")
    parser.add_argument("--api-key", default="", help="API key for LLM provider")
    args = parser.parse_args()

    agent = build_demo_agent()
    if args.provider != "mock":
        registry = default_registry()
        agent.llm = registry.create(args.provider, api_key=args.api_key)

    scope = QueryScope(question=args.question)
    answer = agent.analyze(scope)
    print(answer.as_markdown())


if __name__ == "__main__":
    main()
