# Review Testing

Executes the canonical [testing quality Rules](../../rules/testing-quality.md) over changed production behavior and its tests. It evaluates whether assertions detect missing or wrong behavior, resolves project profiles and emits Rule-traceable findings with category `cognitive-testing`.

## When to use

- As the testing cognitive step in [orchestrate-code-review](../orchestrate-code-review/SKILL.md).
- Standalone before release or after a behavior-changing refactor.
- To distinguish a green test run from adequate behavioral evidence.

## Boundaries

- Test execution belongs to [automate-tests](../automate-tests/SKILL.md).
- Functional intent alignment belongs to [review-implementation-alignment](../review-implementation-alignment/SKILL.md).
- Repair belongs to [orchestrate-repair-loop](../orchestrate-repair-loop/SKILL.md).

See [SKILL.md](./SKILL.md) for execution and boundaries; the criteria live only in [testing-quality.md](../../rules/testing-quality.md) and [standards-test-code.md](../../rules/standards-test-code.md).
