# Review Performance

**Status**: Validated

## Purpose

Executes the canonical [performance quality Rules](../../rules/performance-quality.md) over a supplied code scope. It resolves budgets and load profiles, separates measured defects from evidence limitations, and emits Rule-traceable findings.

## When to use

- You want a changeset or codebase reviewed for performance risk and nothing else.
- You are running an orchestrated multi-skill review and need the performance dimension.
- You want regression risk surfaced before a merge or a release.

## Inputs

- A code scope chosen by the caller (files / directory / diff)

## Outputs

- Findings list (location, category=`cognitive-performance`, severity, title, description, suggestion)

## Ecosystem

| Field | Value |
| :--- | :--- |
| overlaps_with (owner/repo:skill-name) | nesnilnehc/ai-cortex:review-codebase, nesnilnehc/ai-cortex:orchestrate-code-review, nesnilnehc/ai-cortex:review-diff |
| market_position | commodity |

## Full definition

See [SKILL.md](./SKILL.md) for execution and boundaries; the criteria live only in [performance-quality.md](../../rules/performance-quality.md).
