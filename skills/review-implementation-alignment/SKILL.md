---
name: review-implementation-alignment
description: "Compare an implemented change and its verification evidence with approved requirements, designs and tasks. Post-coding atomic functional-alignment review; outputs findings without repairing."
description_zh: 对比已实现变更及验证证据与已批准的需求、设计和任务；编码后原子对齐审查，只输出 findings。
tags: [review, implementation, alignment, post-coding]
version: 1.0.0
license: MIT
recommended_scope: project
metadata:
  author: ai-cortex
triggers: [review implementation alignment, implementation alignment, verify implementation against design]
input_schema:
  type: free-form
  description: Approved artifact paths, implementation diff/scope and available verification evidence
output_schema:
  type: findings-list
  description: Zero or more implementation-alignment findings
---

# Skill: Review Implementation Alignment

## Purpose

Evaluate an implemented change against [implementation-alignment-quality](../../rules/implementation-alignment-quality.md). This is an atomic post-coding functional-alignment review. It is not a meta-skill, code-quality orchestrator or repair loop.

## Core objective

Find omissions, scope drift, contract/data divergence, missing production wiring and unsupported completion claims that a file-by-file review or implementation-shaped test suite can miss.

## Scope boundaries

This Skill compares approved artifacts, code and evidence. Intrinsic engineering quality belongs to `orchestrate-code-review`; test execution belongs to `automate-tests`; fixes and repetition belong to `orchestrate-repair-loop`.

## Use cases

- After implementation and before declaring functional completion
- After repair when acceptance or design alignment may have changed
- For a change whose tests are green but an approved item may be absent or unwired

## Behavior

1. Load the alignment Rule and the authoritative artifact chain in order: requirement, functional design when present, technical design, tasks.
2. Reject superseded or draft artifacts as completion authority. Resolve the exact implementation diff/scope and available test/manual evidence.
3. Build a traceability matrix from each in-scope acceptance/design/task item to production location and verification evidence.
4. Follow contracts and fields across layers and confirm production composition reaches delivered behavior.
5. Apply ALN items independently and emit category `cognitive-alignment`, citing fully qualified Rule IDs.
6. Return Rule coverage using the exact `passed`, `waived`, `not_applicable` and `evidence_limited` fields from the findings-list Spec. Missing authoritative artifacts are evidence limitations, not invented requirements.

## Input and output

Input is the approved artifact paths, implementation scope and evidence. Output follows [findings-list](../../specs/findings-list.md).

## Restrictions

- Do not infer an unrecorded requirement or approve scope changes.
- Do not rewrite artifacts or code.
- Do not substitute green tests for acceptance traceability.
- Do not fold engineering-quality findings into this category.

## Self-Check

- [ ] Authoritative artifacts and statuses were resolved.
- [ ] Every in-scope acceptance item maps to code and independent evidence.
- [ ] Contracts, data fields, tactics, production wiring and task completion were checked where applicable.
- [ ] Every finding uses category `cognitive-alignment` and cites an ALN Rule ID.
- [ ] Engineering review and repair were not performed here.

## Examples

### Example 1: acceptance item omitted

The design requires timeout and caching; code implements only timeout and tests mirror the code. Emit ALN-001 and ALN-007 findings at the acceptance/test locations.

### Example 2: field disappears between layers

The repository maps a new field, but the API response omits it. Emit ALN-004 with the contract and mapping locations.

## Change record

- Initial post-coding alignment reviewer externalizing criteria to a canonical Rule.
