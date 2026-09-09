# Review Go

**Status**: Validated

## Purpose

Reviews Go code for language and runtime conventions only: concurrency and goroutine lifetime, context usage, error handling, resource management, API stability, type and zero-value semantics, testability. Emits a findings list in the standard format. Does not select scope and does not perform security or architecture review.

## When to use

- Orchestrated review: the language step when review-code runs on a Go project.
- Go-only review: when the user wants language and runtime conventions checked and nothing else.
- Pre-PR Go checklist: confirm the concurrency, context, and error-handling patterns are right.

## Inputs

- A code scope containing Go code (files, a directory, or a diff), supplied by the user or by a scope skill.

## Outputs

- Findings list: location, category=language, severity, title, description, optional suggestion.

## Ecosystem

| Field | Value |
| :------------------------------------ | :------------------------------------------------------------------------------------------------------------------------ |
| overlaps_with (owner/repo:skill-name) | nesnilnehc/ai-cortex:review-codebase, nesnilnehc/ai-cortex:review-code, nesnilnehc/ai-cortex:review-diff |
| market_position | commodity |

## Full definition

See [SKILL.md](./SKILL.md) for the checklist and the output contract.
