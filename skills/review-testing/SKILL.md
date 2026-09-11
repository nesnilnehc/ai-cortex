---
name: review-testing
description: "Review changed behavior and tests against the canonical testing quality Rule set, including direct oracles, boundary paths, integration assembly, contracts, determinism, doubles and coverage evidence."
description_zh: 依据权威测试质量规则审查行为断言、边界路径、集成装配、契约、确定性、测试替身与覆盖证据。
tags: [code-review, cognitive, testing]
version: 2.0.0
license: MIT
recommended_scope: project
metadata:
  author: ai-cortex
triggers: [review testing, testing review]
input_schema:
  type: code-scope
  description: Production and test code scope selected by the caller
output_schema:
  type: findings-list
  description: Zero or more testing findings traceable to canonical Rule IDs
---

# Skill: Review Testing

## Purpose

Evaluate changed production behavior and its tests against [testing-quality](../../rules/testing-quality.md), while applying [standards-test-code](../../rules/standards-test-code.md) to test-file construction. Emit [findings-list](../../specs/findings-list.md) output with category `cognitive-testing`.

## Core objective

Determine whether the test system would detect missing, incorrect and boundary behavior in the supplied scope, not merely whether tests or line coverage exist.

Success requires traceability from changed behavior to discriminating assertions, execution-boundary evidence where applicable, independent contract oracles, one outcome per Rule item and a Rule ID in every finding.

## Scope boundaries

This Skill reviews test adequacy and design. It does not run tests as its primary capability, select scope, review production architecture/security/performance, write tests, or repair failures. Use `automate-tests` for execution and `orchestrate-repair-loop` for fixes.

## Use cases

- Test-quality review for a change or repository area
- The testing cognitive step in `orchestrate-code-review`
- Review of public-contract, integration-boundary or critical-path evidence

## Behavior

1. Load [testing-quality](../../rules/testing-quality.md), [standards-test-code](../../rules/standards-test-code.md) and record versions where present.
2. Resolve profiles, coverage policy and waivers from project configuration and the changed behavior.
3. Build a behavior-to-test map. Inspect assertions, boundary/error cases, production composition, contract fixtures, determinism controls and test doubles.
4. Use existing test reports when available, but do not infer adequate oracles from a green run or aggregate coverage alone.
5. Emit one finding per failed Rule item with category `cognitive-testing` and a fully qualified TST ID.
6. Return Rule coverage using the exact `passed`, `waived`, `not_applicable` and `evidence_limited` fields from the findings-list Spec.

## Input and output

Input is selected production and test code. Output follows [findings-list](../../specs/findings-list.md); descriptions cite `testing-quality@<version>/<TST-ID>`.

## Restrictions

- Do not restate the test checklist in this Skill.
- Do not count a test file or executed line as a valid behavioral oracle by itself.
- Do not run full test suites or create tests unless another invoked Skill authorizes it.
- Do not mark environment-blocked evidence as passed.
- Do not report the production defect itself. This Skill reports only that nothing would have caught it; the concern Skill that owns the defect reports the defect and carries its severity.

## Self-Check

- [ ] Canonical testing and test-code Rules were loaded.
- [ ] Changed behaviors were mapped to discriminating assertions.
- [ ] Every applicable TST item has a pass, finding, valid waiver or evidence limitation.
- [ ] Findings are precise and cite Rule IDs.
- [ ] Green tests and aggregate coverage were not overinterpreted.

## Examples

### Example 1: built but not wired

Unit tests instantiate a new handler directly, but production registration is absent. Emit a TST-003 finding at the integration boundary; architecture review may separately raise ARC-008.

### Example 2: line coverage without an oracle

A branch executes but no assertion distinguishes the required outcome. Emit a TST-001 finding; do not accept the coverage percentage as proof.

## Change record

- Externalized adequacy criteria to `testing-quality` while retaining `standards-test-code` for construction.
- Added profile, evidence limitation, waiver and Rule-traceability semantics.

Version `2.0.0` reflects the new canonical policy source and completeness semantics.
