---
name: market-research
description: Define a market and examine customers, demand, segments, trends, and defensible size estimates with transparent evidence.
description_zh: 明确市场边界，分析客户、需求、细分、趋势及有方法支撑的规模区间。
tags: [research, market, demand, sizing]
version: 1.0.0
license: MIT
recommended_scope: project
metadata:
  author: ai-cortex
  ai_cortex_type: domain
  ai_cortex_user_invocable: "true"
triggers: [market research, market demand, market size, 市场调研, 市场规模]
input_schema:
  type: free-form
  description: Market or category, geography, target segment, period, and intended decision
output_schema:
  type: document-artifact
  description: Market narrative and JSON Research Report with definition, demand, trends, and supported sizing or a gap
---

# Skill: Market Research

## Purpose

Study a defined market without assuming that a popular category or vendor estimate is a real demand signal. Apply [deep-research](../deep-research/SKILL.md) and preserve its [Research Report](../../specs/research-evidence.md) as the evidence core.

## Procedure

1. Define geography, segment, buyer and user, included products, exclusions, period and currency before searching. Record definition changes across sources.
2. Decompose demand, customer jobs, adoption, budgets, size, growth, supply and shifts. Prefer authorized customer interviews and observed use for need; method-bearing datasets, filings and associations for size. Attribute vendor, consultant and media estimates.
3. Inspect methodology, sample, denominator, year and provenance family. Cross-check important numbers against independent sources where possible. Do not add incompatible figures.
4. If sizing is defensible, show formula, source inputs, assumptions, range, units and date; map each input to finding IDs. If it is not, state `unsupported` and list missing inputs instead of inventing TAM/SAM/SOM.
5. Separate demand evidence from awareness or sales assertions. Classify every material statement and preserve contradictory estimates in conflicts. Add `domain: "market"` and `domain_details` only if useful; never replace common source or finding fields.

## Self-check

The reader can reproduce the market boundary and any estimate. Vendor claims remain attributed; trend and demand evidence are dated. Missing customer signals and unsupported sizing appear as gaps.
