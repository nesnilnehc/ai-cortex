# Review Testing

Reviews code for the **testing** concern: test existence, coverage adequacy, test quality and structure, test type and layering, edge-case and error-path coverage, and test maintainability.

## Purpose

Analyses a given code scope for testing health across six dimensions:

1. **Do tests exist** — do the critical modules have tests of their own?
2. **Coverage adequacy** — are the high-risk paths tested?
3. **Test quality and structure** — are the tests well structured, with meaningful assertions?
4. **Test type and layering** — a sound mix of unit, integration, and e2e?
5. **Edge cases and error paths** — boundary conditions, invalid input, failure modes?
6. **Test maintainability** — DRY, organised fixtures, not brittle?

## When to use

- As part of an orchestrated review run by [orchestrate-code-review](../orchestrate-code-review/SKILL.md) (the cognitive step).
- Standalone, when you want the testing dimension checked and nothing else (before a release, after a refactor).
- Gap analysis, to identify untested modules or low-quality tests.

## Inputs

- **Code scope**: files, a directory, or a diff, supplied by the caller or by a scope skill.

## Outputs

- A findings list in the standard format: location, category ("cognitive-testing"), severity, title, description, suggestion.

## Related skills

- [orchestrate-code-review](../orchestrate-code-review/SKILL.md) — the orchestrator that includes this skill in the cognitive phase.
- [automate-tests](../automate-tests/SKILL.md) — actually runs the tests; this skill reviews test code quality.
- [review-codebase](../review-codebase/SKILL.md) — the scope skill that treats testability as one of its dimensions.

## Installation

Installation is handled centrally by the AI Cortex canonical installer; see the repository root [README](../../README.md#-install-and-use).
