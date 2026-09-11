# Review Observability

**Status**: Experimental

## Purpose

Executes the canonical [observability quality Rules](../../rules/observability-quality.md) over a supplied scope of source, configuration and telemetry definitions. It asks whether changed production behaviour can be measured, correlated and diagnosed safely: structured outcome events, correlation across execution boundaries, user-facing indicators, meaningful spans, bounded-cardinality and leak-free telemetry, actionable error signals, and background work that exposes its progress and its terminal backlog.

## When to use

- Orchestrated review: the observability cognitive step when orchestrate-code-review runs the whole pipeline.
- Deployable services: before a change that operators will have to diagnose in production.
- Background and batch work: when a job can finish a capped batch and leave a backlog nobody can see.

## Inputs

- A code scope (files, a directory, or a diff) supplied by the user or by a scope skill, including telemetry and configuration.

## Outputs

- Findings list: location, category=`cognitive-observability`, severity, title, description, optional suggestion; each finding cites the observability Rule ID it failed.
- Rule coverage metadata separating passed, waived, not-applicable and evidence-limited IDs.

## Ecosystem

| Field | Value |
| :------------------------------------ | :------------------------------------------------------------------------------------- |
| overlaps_with (owner/repo:skill-name) | nesnilnehc/ai-cortex:review-reliability, nesnilnehc/ai-cortex:orchestrate-code-review |
| market_position | commodity |

## Full definition

See [SKILL.md](./SKILL.md) for execution and boundaries; the criteria live only in [observability-quality.md](../../rules/observability-quality.md).
