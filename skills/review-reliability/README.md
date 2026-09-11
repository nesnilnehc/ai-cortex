# Review Reliability

**Status**: Experimental

## Purpose

Executes the canonical [reliability quality Rules](../../rules/reliability-quality.md) over a supplied scope. It asks whether dependency and partial failures terminate predictably, preserve correct durable state and stay recoverable: timeouts and cancellation on every remote attempt, retries that are selective, bounded and budgeted, repeated operations that stay correct, an explicit consistency outcome on partial failure, isolated dependency failure, retained poison and terminal work, and fault verification at the real boundary.

## When to use

- Orchestrated review: the reliability cognitive step when orchestrate-code-review runs the whole pipeline.
- Fallible I/O: a change touches a remote dependency, a queue, a durable workflow or background processing.
- Retry review: layered retries are suspected of multiplying load rather than containing failure.

## Inputs

- A code scope (files, a directory, or a diff) supplied by the user or by a scope skill, including configuration and tests.

## Outputs

- Findings list: location, category=`cognitive-reliability`, severity, title, description, optional suggestion; each finding cites the reliability Rule ID it failed.
- Rule coverage metadata separating passed, waived, not-applicable and evidence-limited IDs.

## Ecosystem

| Field | Value |
| :------------------------------------ | :---------------------------------------------------------------------------------------- |
| overlaps_with (owner/repo:skill-name) | nesnilnehc/ai-cortex:review-observability, nesnilnehc/ai-cortex:review-performance, nesnilnehc/ai-cortex:orchestrate-code-review |
| market_position | commodity |

## Full definition

See [SKILL.md](./SKILL.md) for execution and boundaries; the criteria live only in [reliability-quality.md](../../rules/reliability-quality.md).
