---
name: competitive-research
description: Compare a dated competitor set by capabilities, positioning, pricing, and evidence quality without treating undocumented features as absent.
version: 1.1.0
license: MIT
metadata:
  ai_cortex_type: domain
  ai_cortex_user_invocable: "true"
---

# Skill: Competitive Research

## Purpose

Compare products using consistent criteria and dated evidence. Apply [deep-research](../deep-research/SKILL.md) and preserve the [Research Report](../../specs/research-evidence.md) as the evidence core. This Skill can identify strategic implications, but it does not decide whether to build a product.

## Procedure

1. Fix competitors, category, geography, product edition or plan, comparison criteria and as-of date. Include substitutes where they address the same user job.
2. Inspect official current product docs, release notes and price pages, then independent implementation evidence or reviews. Attribute marketing claims. Record version, region and plan restrictions.
3. Build a matrix whose populated cells contain a classification, date and finding ID. Use `Unknown` when evidence is absent or inaccessible; do not label a feature absent solely because docs are silent. State if pricing is historical, quote-based or unverified.
4. Compare like with like. Explain gaps caused by edition or regional differences and preserve contradictory sources. Tie any positioning or differentiation inference to specific findings.
5. Emit a concise narrative and JSON report. Add `domain: "competitive"` and `domain_details` only if useful; keep the shared evidence fields intact.

## Self-check

Every non-Unknown matrix cell has an exact source locator and date. Contradictory capability claims remain visible. An empty source search never becomes a negative feature claim.

## Examples

### Comparable editions

**Input:** compare the current paid plans of two products in one region. **Output:** produce a dated capability and pricing matrix whose supported cells cite exact official plan pages and finding IDs.

### Undocumented feature

**Input:** one vendor has no public document about an export feature. **Output:** mark that cell Unknown, record the search gap, and avoid claiming the feature is absent. If a review claims it exists, retain the conflict and its date.
