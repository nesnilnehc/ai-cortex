# Review Security

**Status**: Validated

## Purpose

Executes the canonical [security quality Rules](../../rules/security-quality.md) over supplied code, configuration and dependency scope. It resolves trust-boundary profiles, gathers evidence, and emits Rule-traceable findings.

## When to use

- Orchestrated review: the cognitive step when orchestrate-code-review runs the whole pipeline.
- Security-focused review: when the user wants the security dimension checked and nothing else.
- Compliance or audit: a repeatable security-checklist output.

## Inputs

- A code scope (files, a directory, or a diff) supplied by the user or by a scope skill.

## Outputs

- Findings list: location, category=cognitive-security, severity, title, description, optional suggestion.

## Ecosystem

| Field | Value |
| :------------------------------------ | :-------------------------------------------------------------------------------------------------------------------------------------------- |
| overlaps_with (owner/repo:skill-name) | nesnilnehc/ai-cortex:review-codebase, nesnilnehc/ai-cortex:orchestrate-code-review, nesnilnehc/ai-cortex:review-sql, nesnilnehc/ai-cortex:review-diff |
| market_position | commodity |

## Full definition

See [SKILL.md](./SKILL.md) for execution and boundaries; the criteria live only in [security-quality.md](../../rules/security-quality.md).
