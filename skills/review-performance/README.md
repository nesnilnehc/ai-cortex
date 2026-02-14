# Review Performance

**Status**: validated

## What it does

Reviews a given code scope for performance concerns only (complexity, query efficiency, I/O and network cost, memory behavior, contention, caching, and regression risk). Emits a findings list in a standard format for aggregation.

## When to use

- You want only performance risks reviewed for a change set or codebase.
- You are running an orchestrated multi-skill review and need the performance dimension.
- You want regression risk surfaced before merge or release.

## Inputs

- Code scope (files/directories/diff) selected by the caller

## Outputs

- Findings list (Location, Category=`cognitive-performance`, Severity, Title, Description, Suggestion)

## Scores (ASQM)

| Dimension | Score |
| :--- | :--- |
| agent_native | 5 |
| cognitive | 4 |
| composability | 5 |
| stance | 5 |
| **asqm_quality** | 19 |

## Ecosystem

| Field | Value |
| :--- | :--- |
| overlaps_with (owner/repo:skill-name) | nesnilnehc/ai-cortex:review-codebase, nesnilnehc/ai-cortex:review-code, nesnilnehc/ai-cortex:review-diff |
| market_position | commodity |

## Full definition

See [SKILL.md](./SKILL.md) for complete behavior, restrictions, and examples.

