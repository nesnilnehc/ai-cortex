---
name: policy-research
description: Research a jurisdiction's policy or compliance question with official sources, effective dates, applicability, and product implications.
description_zh: 核对特定法域的政策、法规及其生效和适用边界，形成可追溯的产品影响分析。
tags: [research, policy, regulation, compliance]
version: 1.0.0
license: MIT
recommended_scope: project
metadata:
  author: ai-cortex
  ai_cortex_type: domain
  ai_cortex_user_invocable: "true"
triggers: [policy research, regulation research, compliance impact, 政策研究, 法规调研]
input_schema:
  type: free-form
  description: Policy question, jurisdiction, regulated actors, period or as-of date, and product context when relevant
output_schema:
  type: document-artifact
  description: Policy-focused narrative and JSON Research Report with applicability and product implications
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
