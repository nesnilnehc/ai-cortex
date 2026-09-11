---
name: review-technical-design
description: "Review an existing technical design against its modeling Spec, canonical quality Rule and applicable engineering Rule profiles before tasks or coding begin."
description_zh: 在任务拆分或编码前依据技术设计规范、权威质量规则及适用工程规则画像审查既有技术设计。
tags: [review, technical-design, pre-coding]
version: 1.0.0
license: MIT
recommended_scope: both
metadata:
  author: ai-cortex
triggers: [review technical design, technical design review, validate technical design]
input_schema:
  type: document-artifact
  description: Existing technical-design document path or content
  artifact_type: technical-design
output_schema:
  type: findings-list
  description: Zero or more technical-design-quality findings
---

# Skill: Review Technical Design

## Purpose

Evaluate an existing technical design against [technical-design-modeling](../../specs/technical-design-modeling.md), [technical-design-quality](../../rules/technical-design-quality.md) and the engineering Rule IDs it claims to satisfy. This is an atomic pre-coding gate.

## Core objective

Determine whether tasks can be derived without architectural ambiguity and whether applicable architecture, security, performance, observability, reliability and testing concerns have explicit tactics and verification.

## Scope boundaries

This Skill reviews the design artifact and cited local context. It does not author the design, inspect implementation, run code review or aggregate downstream Skills.

## Use cases

- After technical design is drafted and before task derivation
- After architecture, contract, data, operational or risk decisions change
- Before coding a cross-boundary or quality-sensitive change

## Behavior

1. Load [technical-design-quality](../../rules/technical-design-quality.md) in full and record its version, then load each engineering Rule set the design references.
2. Resolve applicability per [rule-modeling](../../specs/rule-modeling.md): whether the design triggers a quality attribute, a data change or an interface change, plus the project's profiles, parameters and valid waivers from `.ai-cortex/config.yaml` when present.
3. Evaluate each applicable item independently, gathering only the evidence that item declares. An unresolved project value makes its item evidence-limited unless the design already records that absence as a blocking open question.
4. For each triggered engineering concern, verify the design names Rule IDs, a system-specific tactic, its trade-off and a verification method; do not perform the future code review.
5. Emit one finding per failed obligation, with category `technical-design-quality`, an exact section location, and the failed Rule ID in the description, for example `technical-design-quality@<active-version>/TDES-007`.
6. Apply a waiver only when every waiver field is valid and its Rule ID and scope cover the exact finding. Report waived items separately.
7. Return Rule coverage using the exact `passed`, `waived`, `not_applicable` and `evidence_limited` fields from the findings-list Spec.

## Input and output

Input is one technical-design artifact plus its local parent and project configuration. Output follows [findings-list](../../specs/findings-list.md): every finding uses category `technical-design-quality` and cites the failed Rule ID, and the coverage footer is metadata rather than a finding.

## Restrictions

- Do not invent project topology, budgets, SLOs or security classifications.
- Do not restate engineering Rule text in the design; require references and design-specific decisions.
- Do not approve unresolved blocking decisions.

## Self-Check

- [ ] The modeling Spec, quality Rule and referenced engineering Rules were loaded.
- [ ] Applicable profiles and parameters were resolved.
- [ ] Conditional quality-attribute design was checked when triggered.
- [ ] Findings are precise, category-compliant and each cites one failed Rule ID.
- [ ] Every applicable Rule ID received a pass, a finding, a valid waiver or an explicit evidence limitation.
- [ ] The coverage footer distinguishes passed, waived, not applicable and evidence limited.
- [ ] No implementation review was performed.

## Examples

### Example 1: new public API

The design defines endpoints but no compatibility tactic or contract verification. Emit a finding against the quality-attribute design and cite the missing public-contract Rule references.

### Example 2: no database change

Accept an explicit “no database change” statement. Do not require a migration plan when its trigger is false.

## Change record

- Initial atomic reviewer combining the existing design contract with profiled engineering Rule references.

