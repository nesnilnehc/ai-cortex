# Review Performance

**Status**: Validated

## Purpose

Reviews the given code scope for performance only (complexity, query efficiency, I/O and network cost, memory behaviour, contention, caching, and regression risk). Emits a findings list in the standard format for aggregation.

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
| overlaps_with (owner/repo:skill-name) | nesnilnehc/ai-cortex:review-codebase, nesnilnehc/ai-cortex:review-code, nesnilnehc/ai-cortex:review-diff |
| market_position | commodity |

## Full definition

See [SKILL.md](./SKILL.md) for the full behaviour, the limits, and the examples.
