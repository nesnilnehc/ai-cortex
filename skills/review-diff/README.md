# Review Diff

**Status**: Validated

## Purpose

Reviews the current changes only (git diff, staged and unstaged). Covers intent and impact, regression and correctness, breaking changes and compatibility, side effects and idempotency, observability. Emits a findings list in the standard format so review-code can aggregate it.

## When to use

- Pre-commit: a diff-only check before committing.
- Orchestrated review: the scope step when review-code runs the whole pipeline.
- Focused change review: when the user wants "what changed" analysed and nothing else.

## Inputs

- The git diff (staged plus unstaged).

## Outputs

- Findings list: location, category=scope, severity, title, description, optional suggestion.

## Ecosystem

| Field | Value |
| :------------------------------------ | :---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| overlaps_with (owner/repo:skill-name) | nesnilnehc/ai-cortex:review-codebase, nesnilnehc/ai-cortex:review-code, wshobson/agents:code-review-excellence, Trailofbits/skills:diff-review |
| market_position | commodity |

## Full definition

See [SKILL.md](./SKILL.md) for the checklist, the limits, and the output contract.
