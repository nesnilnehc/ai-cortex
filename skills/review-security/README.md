# Review Security

**Status**: Validated

## Purpose

Reviews code for security only: injection (SQL, command, template), sensitive data and logging, authentication and authorisation, dependencies and CVEs, configuration and secrets, cryptography and hashing. Emits a findings list in the standard format. Does not define scope and does not perform language or architecture analysis.

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

See [SKILL.md](./SKILL.md) for the checklist and the output contract.
