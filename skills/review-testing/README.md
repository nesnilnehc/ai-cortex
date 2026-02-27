# review-testing

Review code for **testing** concerns: test existence, coverage adequacy, test quality and structure, test types and layering, edge-case and error-path coverage, and test maintainability.

## What it does

Analyzes the given code scope for testing health across six dimensions:

1. **Test existence** — Do key modules have corresponding tests?
2. **Coverage adequacy** — Are high-risk paths tested?
3. **Test quality and structure** — Are tests well-structured with meaningful assertions?
4. **Test types and layering** — Appropriate mix of unit, integration, and e2e?
5. **Edge cases and error paths** — Boundary conditions, invalid inputs, failure modes?
6. **Test maintainability** — DRY, organized fixtures, not brittle?

## When to use

- As part of an orchestrated review via [review-code](../review-code/SKILL.md) (cognitive step).
- Standalone when you want only testing dimensions checked (e.g. before release, after refactor).
- Gap analysis to identify untested modules or low-quality tests.

## Inputs

- **Code scope**: Files, directories, or diff provided by the caller or scope skill.

## Outputs

- Findings list in standard format: Location, Category (`cognitive-testing`), Severity, Title, Description, Suggestion.

## Related skills

- [review-code](../review-code/SKILL.md) — Orchestrator that includes this skill in the cognitive stage.
- [run-automated-tests](../run-automated-tests/SKILL.md) — Actually executes tests; this skill reviews test code quality.
- [review-codebase](../review-codebase/SKILL.md) — Scope skill that mentions testability as one dimension.

## Install

```bash
npx skills add nesnilnehc/ai-cortex --skill review-testing
```
