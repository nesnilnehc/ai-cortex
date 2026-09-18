# Review Error Surfacing

**Status**: Validated

## Purpose

Executes the canonical [error surfacing quality Rules](../../rules/error-surfacing-quality.md) over a supplied code scope: where a defect is decided, and whether the failure that results can be acted on. Emits Rule-traceable findings without selecting scope or performing another concern's analysis.

## When to use

- Orchestrated review: the error-surfacing cognitive step when orchestrate-code-review runs the whole pipeline.
- A change that adds an input boundary, a guard, or a failure path a person or a program will meet.
- A command-line tool, compiler or interface whose failures a person reads, or an API whose failures a program branches on.

## Boundary

The confusable neighbour is observability. This Skill reads the message handed back to whoever asked; `review-observability` reads the event written for whoever operates. Retry and partial-failure behaviour belongs to `review-reliability`, and disclosure to `review-security`.

See [SKILL.md](./SKILL.md) for execution and boundaries; the criteria live only in [error-surfacing-quality.md](../../rules/error-surfacing-quality.md).
