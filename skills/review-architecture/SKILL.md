---
name: review-architecture
description: "Review code against the canonical architecture quality Rule set, including boundaries, dependency direction, cohesion, cycles, contract stability, coupling, composition and change surface. Cognitive-only atomic skill; output is a findings list."
description_zh: 依据权威架构质量规则审查边界、依赖方向、内聚性、循环、契约稳定性、耦合、装配与变更面。
tags: [code-review, cognitive, architecture]
version: 2.0.1
license: MIT
recommended_scope: project
metadata:
  author: ai-cortex
triggers: [review architecture, architecture review]
input_schema:
  type: code-scope
  description: Source files, directories or a diff selected by the caller
output_schema:
  type: findings-list
  description: Zero or more architecture findings traceable to canonical Rule IDs
---

# Skill: Review Architecture

## Purpose

Evaluate the supplied code scope against [architecture-quality](../../rules/architecture-quality.md). This Skill owns execution and evidence gathering; the Rule owns every architecture criterion. Emit a [findings list](../../specs/findings-list.md), never a score or a rewrite.

## Core objective

Produce location-precise, actionable architecture findings for every applicable failed Rule item, while reporting which items were not applicable or could not be evaluated because project parameters were absent.

Success requires:

1. The active Rule version and every applicable item ID are named.
2. Project topology, protected contracts, profiles and valid waivers are resolved before judgment.
3. Automated evidence is preferred where the Rule declares it, without overstating tool coverage.
4. Every finding cites one failed Rule ID and uses category `cognitive-architecture`.
5. Zero findings is reported only after all applicable items have a pass, valid waiver or explicit evidence limitation.

## Scope boundaries

This Skill reviews architecture only. It does not select diff versus codebase scope, review language conventions, security, performance, reliability, observability or test quality, modify code, or approve a waiver. Use the corresponding atomic Skill or `orchestrate-code-review` for those concerns.

## Use cases

- Architecture-focused review of a change, module or repository
- The architecture cognitive step inside `orchestrate-code-review`
- Verification of declared module topology or a protected-contract change
- Review of composition, wiring and change-surface risk after implementation

## Behavior

1. Load [architecture-quality](../../rules/architecture-quality.md) in full and record its version.
2. Read the nearest project `AGENTS.md`, architecture documentation and `.ai-cortex/config.yaml` when present. Resolve active profiles, parameters and waivers according to [rule-modeling](../../specs/rule-modeling.md).
3. Build only the evidence required by applicable items:
   - Prefer repository-native dependency or contract checks.
   - Otherwise use build metadata, import graphs, exported signatures, production call sites and the supplied diff.
   - For judgment items, compare concrete responsibility and dependency evidence; do not use an unexplained quality score.
4. Evaluate each applicable item independently. A missing project parameter makes only its `project:*` item not evaluable; it does not suppress baseline items.
5. Emit one finding per failed obligation. Include the active Rule version in the description, for example `architecture-quality@<active-version>/ARC-003`.
6. Apply a waiver only when every waiver field is valid and its Rule ID and scope cover the exact finding. Report waived items separately; do not erase their existence.
7. Return Rule coverage using the exact `passed`, `waived`, `not_applicable` and `evidence_limited` fields from the findings-list Spec.

## Input and output

Input is an already selected code scope: files, directories or a diff. Optional project context may include the change size and upstream technical design.

Output is zero or more findings in [findings-list](../../specs/findings-list.md) format. Every finding uses category `cognitive-architecture`; the description cites the failed Rule ID. The coverage footer is metadata, not a finding.

## Restrictions

- Do not restate or locally extend the architecture checklist; propose a Rule change when a criterion is missing.
- Do not assume a named architecture style or invent module topology.
- Do not treat a missing dependency tool as proof that dependency items pass.
- Do not approve, broaden or create a waiver during review.
- Do not perform repairs; hand blocking findings to `orchestrate-repair-loop` when repair is requested.
- Do not report a missing test as an architecture finding. This Skill owns whether composition and contracts are correct in production code; `review-testing` owns whether anything would have caught it.

## Self-Check

- [ ] The canonical architecture Rule was loaded and its version recorded.
- [ ] Active profiles, parameters and waivers were resolved from project evidence.
- [ ] Every applicable Rule ID received a pass, finding, valid waiver or explicit evidence limitation.
- [ ] Each finding has a precise location, category `cognitive-architecture`, valid severity and cited Rule ID.
- [ ] No architecture criterion was invented or duplicated in this Skill.
- [ ] The coverage footer distinguishes pass, waiver, N/A and evidence limitation.

## Examples

### Example 1: declared dependency violation

Input: the project declares that `domain` has no outward module dependencies, but `domain/order.ts` imports a database adapter.

Expected: emit a `major` `cognitive-architecture` finding at the import, citing ARC-002. Also evaluate ARC-003 and the other applicable baseline items; do not assume they fail.

### Example 2: valid legacy-cycle waiver

Input: a cycle matches ARC-003, and a non-expired waiver covers the exact legacy directory with an approved freeze control.

Expected: list ARC-003 under waived IDs, verify no new node or edge joined the frozen cycle, and emit a finding if the compensating control was violated.

### Example 3: no project topology

Input: a small library has no `.ai-cortex/config.yaml`.

Expected: mark ARC-002 and ARC-009 not evaluable or not applicable as their parameters require, then evaluate baseline cohesion, cycles, boundary leakage, coupling and speculative extension normally.

## Change record

- Externalized architecture criteria to `rules/architecture-quality.md`.
- Added profile, parameter, waiver and coverage semantics.
- Preserved the `code-scope -> findings-list` contract and category.

Version `2.0.0` is intentional: the source of truth and completeness semantics changed, even though the I/O artifact types remain compatible.

Version `2.0.1` removes a stale example pin so the Skill always reports the active Rule version it loaded.
