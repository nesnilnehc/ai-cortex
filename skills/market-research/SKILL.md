---
name: market-research
description: Define a market and examine customers, demand, segments, trends, and defensible size estimates with transparent evidence.
version: 1.1.0
license: MIT
metadata:
  ai_cortex_type: domain
  ai_cortex_user_invocable: "true"
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

## Examples

### Reproducible estimate

**Input:** estimate annual spending for a defined buyer segment in one country. **Output:** show the segment boundary, source-backed buyer count and spend assumptions, formula, dated range, and finding IDs for each input.

### Incompatible estimates

**Input:** two sources use different definitions of the market, and neither discloses a denominator. **Output:** keep the figures separate as attributed claims, mark sizing unsupported, and name the missing inputs needed for a defensible estimate.
