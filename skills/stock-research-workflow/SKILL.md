---
name: stock-research-workflow
description: "Define and execute a 10-step equity research workflow with fixed input/output schemas, covering thesis framing, filings, governance, business model, industry sizing, competition, news catalysts, research divergence, modeling, and valuation/reporting. Use when structuring or implementing a multi-skill analyst agent that needs consistent schemas and handoffs between steps."
---

# Stock research workflow

## Use this workflow

- Define or implement a 10-skill analyst agent with strict input/output schemas.
- Translate user requests into a structured research pipeline with reusable, composable steps.

## Workflow steps

1. **Thesis Framing**: Establish the research question, consensus view, and top assumptions.
2. **Filings Ingestion**: Extract three-statement summaries, footnotes, policies, and MD&A highlights.
3. **Governance & History**: Assess control stability, incentives, integrity/transparency, and key events.
4. **Business Model Decomposition**: Map operating flow and profit pools by product/region/channel.
5. **Industry Sizing & Nature**: Summarize industry characteristics and TAM/SAM/SOM with growth drivers.
6. **Competition & Porter 5 Forces**: Track share shifts, five-forces conclusions, and falsifiable moats.
7. **News & Catalyst Tracker**: Link events to financial impacts, list catalysts, and define triggers/time windows.
8. **Research Divergence Extractor**: Capture disagreement matrix and largest uncertainties to validate.
9. **Modeling & Quality Diagnostics**: Build review, forward model, and sensitivity drivers.
10. **Valuation & Report Writer**: Generate final report from model output, comps, and risks.

## Output requirements

- Ensure each step’s output matches its schema.
- Preserve strict handoffs so later steps can consume the outputs without re-parsing.
- When implementing in code, validate required fields and formats.

## Reference schemas

See the schema definitions in [references/schemas.md](references/schemas.md).
