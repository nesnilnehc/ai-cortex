# Review Go

**Status**: validated

## What it does

Reviews Go code for language and runtime conventions only: concurrency and goroutine lifecycle, context usage, error handling, resource management, API stability, type and zero-value semantics, testability. Emits a findings list in the standard format. Does not perform scope selection or security/architecture review.

## When to use

- Orchestrated review: used as the language step when review-code runs for Go projects.
- Go-only review: when the user wants only language/runtime conventions checked.
- Pre-PR Go checklist: ensure concurrency, context, and error handling patterns are correct.

## Inputs

- Code scope (files, directories, or diff) containing Go code, provided by the user or scope skill.

## Outputs

- Findings list: Location, Category=language-go, Severity, Title, Description, optional Suggestion.

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
| overlaps_with (owner/repo:skill-name) | nesnilnehc/ai-cortex:review-codebase, nesnilnehc/ai-cortex:review-code, nesnilnehc/ai-cortex:review-diff |
| market_position | commodity |

## Full definition

See [SKILL.md](./SKILL.md) for checklist and output contract.
