---
name: review-security
description: "Review code and configuration against the canonical security quality Rule set. Resolves trust-boundary profiles, gathers tool-assisted evidence and emits findings traceable to stable Rule IDs."
description_zh: 依据权威安全质量规则审查代码与配置，解析信任边界配置并输出可追溯 findings。
tags: [code-review, cognitive, security]
version: 2.0.0
license: MIT
recommended_scope: project
metadata:
  author: ai-cortex
triggers: [review security, security review]
input_schema:
  type: code-scope
  description: Source files, configuration, manifests or a diff selected by the caller
output_schema:
  type: findings-list
  description: Zero or more security findings traceable to canonical Rule IDs
---

# Skill: Review Security

## Purpose

Evaluate the supplied scope against [security-quality](../../rules/security-quality.md). The Rule owns the security criteria; this Skill resolves applicability, gathers evidence and emits [findings-list](../../specs/findings-list.md) output with category `cognitive-security`.

## Core objective

Produce complete, location-precise security findings for all applicable failed Rule items without treating tool output as proof beyond its coverage.

Success requires the active Rule version, resolved profiles and waivers, one decision per applicable item, a Rule ID in every finding and a coverage footer separating pass, waiver, N/A and evidence limitations.

## Scope boundaries

This Skill covers security only. Scope selection, language/framework conventions, architecture, reliability, performance, observability, test quality and fixes belong to other Skills. It may inspect manifests and configuration needed by applicable security items, but it must not broaden into a general dependency or operations audit.

## Use cases

- Security-focused review of code, configuration or dependency changes
- The security cognitive step in `orchestrate-code-review`
- Review of a public entry point, authenticated flow, sensitive-data path or supply-chain change

## Behavior

1. Load [security-quality](../../rules/security-quality.md) and record its version.
2. Resolve active profiles and parameters from project contracts, data classification, entry points, manifests and `.ai-cortex/config.yaml`. Validate any waiver against [rule-modeling](../../specs/rule-modeling.md).
3. Gather the evidence named by each applicable item. Prefer repository-native secret, dependency and static-analysis results, then inspect source-to-sink flows, access-control placement, defaults, cryptographic calls and telemetry.
4. Follow data and authorization across the complete reachable path. Do not clear a Rule merely because one layer validates it when a later layer bypasses that control.
5. Emit one finding per failed obligation, cite the fully qualified Rule ID in its description and use the Rule's default severity unless concrete impact justifies a documented adjustment.
6. Return Rule coverage using the exact `passed`, `waived`, `not_applicable` and `evidence_limited` fields from the findings-list Spec.

## Input and output

Input is an already selected code/configuration scope. Output follows [findings-list](../../specs/findings-list.md); every finding uses category `cognitive-security` and cites `security-quality@<version>/<SEC-ID>`.

## Restrictions

- Do not invent security criteria or restate the Rule checklist.
- Do not claim a vulnerability scan ran when no tool result exists.
- Do not expose secret values in findings; identify the location and credential type only.
- Do not approve waivers or lower a severity to make a gate pass.
- Do not repair unless the caller invokes a repair capability.
- Do not restate an observability obligation about where a failure is recorded. This Skill owns whether security telemetry is actionable and non-disclosing; `review-observability` owns whether a terminal failure is recorded once at its owning boundary.

## Self-Check

- [ ] The canonical security Rule and version were loaded.
- [ ] Trust-boundary profiles, parameters and waivers were resolved from evidence.
- [ ] Every applicable SEC item has a pass, finding, valid waiver or evidence limitation.
- [ ] Findings are precise, actionable, secret-safe and traceable to Rule IDs.
- [ ] Tool coverage was not overstated and no criteria were duplicated.

## Examples

### Example 1: user input reaches a shell

Trace request input to a string-built process command. Emit a `critical` finding citing SEC-001 at the sink and suggest the parameterized process API plus domain validation.

### Example 2: dependency scan unavailable

For a lockfile change, inspect provenance and pinning but mark the vulnerability-assessment evidence for SEC-006 as limited; do not report it as passed.

## Change record

- Externalized all security criteria to `security-quality`.
- Added profile, waiver, evidence-limitation and Rule-traceability behavior.
- Preserved the `code-scope -> findings-list` contract and category.

Version `2.0.0` reflects the new canonical policy source and completeness semantics.
