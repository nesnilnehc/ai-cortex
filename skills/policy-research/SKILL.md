---
name: policy-research
description: Research a jurisdiction's policy or compliance question with official sources, effective dates, applicability, and product implications.
version: 1.1.0
license: MIT
metadata:
  ai_cortex_type: domain
  ai_cortex_user_invocable: "true"
---

# Skill: Policy Research

## Purpose

Answer a bounded policy question for a named jurisdiction and date. This Skill applies the method in [deep-research](../deep-research/SKILL.md) and emits the shared [Research Report](../../specs/research-evidence.md). It explains potential product implications; it does not issue a legal opinion or certify compliance.

## Procedure

1. Fix jurisdiction, regulated activity, actor, relevant period and as-of date. If jurisdiction is missing and material, ask or state a narrow assumption; never generalize one country's rule.
2. Decompose into instruments, scope of applicability, binding obligations, official guidance, enforcement or transition timing, and product implications.
3. Prioritize current official text and amendment history, then regulator guidance, then attributed interpretations. Inspect original wording and cite section or article locators. Record promulgation and effective dates separately.
4. Apply deep-research's source, classification, corroboration and conflict discipline. A binding text's wording can be a Fact; an interpretation or enforcement prediction is a Claim or Inference. Mark ambiguous applicability Unknown.
5. In the narrative, give an instrument table with issuer, force, effective date, affected actors, relevant clause and finding ID. Separate what the law says, what a source claims it means, and the product implication derived from cited findings.
6. Explain jurisdictional or temporal conflicts, unknowns, and what legal or regulatory review could resolve them. Preserve the report's evidence core; add `domain: "policy"` and `domain_details` only if useful.

## Self-check

Every obligation has an official locator, effective date and affected actor. Every product implication traces to source-backed findings. An unresolved interpretation stays unresolved, and no compliance verdict is asserted from incomplete evidence.

## Examples

### Effective-date check

**Input:** assess how a named regulation affects a product in one jurisdiction. **Output:** cite the official instrument and clause, distinguish promulgation from effective date, identify affected actors, and trace each possible product change to a finding.

### Jurisdiction omitted

**Input:** “Does this feature comply with privacy law?” with no jurisdiction or regulated actor. **Output:** ask for the boundary when it changes applicability; do not generalize one country's rule or issue a compliance verdict.
