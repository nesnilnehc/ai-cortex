# Review Diff

**Status**: validated

## What it does

Reviews only the current change (git diff, staged and unstaged). Covers intent and impact, regression and correctness, breaking changes and compatibility, side effects and idempotency, observability. Emits a findings list in the standard format for aggregation by review-code.

## When to use

- Pre-commit: diff-only check before commit.
- Orchestrated review: used as the scope step when review-code runs the full pipeline.
- Focused change review: when the user wants only "what changed" analyzed.

## Inputs

- Git diff (staged + unstaged).

## Outputs

- Findings list: Location, Category=scope, Severity, Title, Description, optional Suggestion.

## Scores (ASQM)

| Dimension      | Score |
| :---           | :---  |
| agent_native   | 5     |
| cognitive      | 4     |
| composability  | 5     |
| stance         | 5     |
| **asqm_quality** | 19   |

## Ecosystem

| Field | Value |
| :--- | :--- |
| overlaps_with (owner/repo:skill-name) | nesnilnehc/ai-cortex:review-codebase, review-code; external differential-review skills |
| market_position | commodity |

## Full definition

See [SKILL.md](./SKILL.md) for checklist, restrictions, and output contract.
