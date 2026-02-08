# Stock research workflow schemas

## Thesis Framing

**Input**
- ticker
- horizon
- focus_areas

**Output**
- research_question
- consensus_summary
- key_assumptions (top 5)

## Filings Ingestion

**Input**
- filings (three years of quarterly/interim/annual filings)

**Output**
- financial_statements_summary (three-statement summary)
- footnotes_highlights
- accounting_policies_and_one_offs
- management_discussion_excerpt

## Governance & History

**Input**
- sources (prospectus, annual reports, announcements, management bios, ownership structure)

**Output**
- control_stability
- incentives
- integrity_transparency_score
- key_events_timeline

## Business Model Decomposition

**Input**
- disclosures (company disclosures)
- industry_materials

**Output**
- operating_flow (R&D/procurement/production/sales flow)
- profit_pool_layers (product/region/channel)

## Industry Sizing & Nature

**Input**
- industry_data
- penetration_rates
- benchmarks (domestic/global comparisons)

**Output**
- industry_characteristics (cycle/asset intensity/concentration/tech iteration)
- tam_sam_som
- growth_drivers

## Competition & Porter 5 Forces

**Input**
- competitor_data
- channel_signals (upstream/downstream signals)

**Output**
- share_shifts
- porter_five_forces
- falsifiable_advantage_tests (how to prove the advantage wrong)

## News & Catalyst Tracker

**Input**
- news_and_filings (last 6–12 months)

**Output**
- event_impact_paths
- catalyst_list
- triggers_and_time_windows

## Research Divergence Extractor

**Input**
- research_reports (sell-side/buy-side)

**Output**
- divergence_matrix (assumptions/evidence/valuation method)
- largest_uncertainties

## Modeling & Quality Diagnostics

**Input**
- historical_financials
- assumptions

**Output**
- three_year_review
- forward_model (3–5 year model)
- sensitivities (volume/price/gross margin/opex/capex/working capital)

## Valuation & Report Writer

**Input**
- model_output
- comparable_companies
- risk_list
- report_format

**Output**
- report (full report with conclusion, rationale, industry/company, model, valuation, risks)
