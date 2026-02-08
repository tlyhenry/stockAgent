# Stock agent

## Airbnb analyst agent concept

This repository defines an AI agent that works as an analyst to investigate Airbnb and answer historical, fact-based questions. The agent is designed to ground answers in reliable sources and keep a clear audit trail so users can see where facts came from.

### Goals

- Answer questions about Airbnb with **verifiable facts from the past**, including financial performance, product milestones, policy changes, and market context.
- Provide **clear citations** for every material claim.
- Distinguish **facts vs. analysis** (e.g., “facts” and “interpretation” sections).

### Core capabilities

1. **Question intake & scoping**
   - Clarify the timeframe (e.g., “2015–2020” vs. “last quarter”).
   - Identify the category: financials, operations, regulatory issues, product, or competitive landscape.
   - Ask follow-up questions if the scope is ambiguous.

2. **Evidence collection**
   - Retrieve primary sources: Airbnb filings (10-K, 10-Q, S-1), earnings calls, shareholder letters, and official press releases.
   - Use secondary sources (reputable news, analyst reports) to contextualize, but never replace primary sources for key facts.
   - Maintain a **source log** with timestamps and URLs for reproducibility.

3. **Fact synthesis**
   - Summarize relevant facts in a “Key facts” list.
   - Provide a short analytical summary only after facts are established.
   - Flag uncertainty explicitly (e.g., “This is inferred because…”).

4. **Response formatting**
   - **Answer** (1–2 paragraph concise response).
   - **Key facts** (bulleted, cited).
   - **Sources** (bullet list with links).
   - **Notes/assumptions** (if needed).

### Example questions

- “What were Airbnb’s revenue and net income trends between 2019 and 2023?”
- “When did Airbnb introduce its ‘Categories’ feature, and what was the stated goal?”
- “What were Airbnb’s major regulatory challenges in 2016–2018?”

### Data sources (suggested)

- SEC filings (10-K, 10-Q, S-1) for financial history.
- Investor relations page and shareholder letters.
- Official Airbnb newsroom posts.
- Reputable business news outlets for context.

### Guardrails

- Do not speculate about future performance; keep answers historical.
- Always cite sources for factual statements.
- If sources disagree, surface the discrepancy rather than picking one silently.

### Implementation outline

- **Retriever**: Search over a curated corpus (SEC filings, press releases, newsroom posts).
- **Fact store**: Structured memory (e.g., JSON/DB) with `{claim, source, date, url, confidence}`.
- **Answer composer**: Template-driven response that separates facts from analysis.
- **Evaluation**: Periodic checks for factual accuracy and citation coverage.

## Research skill schema

The 10-step workflow is defined as a reusable skill package under `skills/stock-research-workflow/`.
See the schema and step definitions in that skill’s `SKILL.md` and `references/schemas.md` to wire
an agent with strict input/output handoffs.

## Reference implementation

The `stock_agent` package is a reference implementation with interchangeable components:

- **Data sources**: in-memory records and text files (extend with SEC/press release loaders).
- **Retriever**: collects evidence from all sources.
- **Fact store**: stores extracted claims with confidence values.
- **LLM registry**: placeholders for OpenAI, Anthropic, and Gemini.
- **Agent**: orchestrates retrieval, fact extraction, and answer composition.
- **CLI**: a simple command-line interface for asking questions.

### Example usage

```bash
python -m stock_agent.cli "When did Airbnb file its S-1?"
```

If you want this agent implemented for production, the next step is to decide the tooling (e.g., LangChain, LlamaIndex, or a custom RAG pipeline) and provide access to the preferred sources.
If you want this agent implemented, the next step is to decide the tooling (e.g., LangChain, LlamaIndex, or a custom RAG pipeline) and provide access to the preferred sources.
