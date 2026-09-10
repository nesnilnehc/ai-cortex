# Review SQL

**Status**: Validated

## Purpose

Reviews SQL and query code for language and query conventions only: injection and parameterisation, indexes and execution plans, transactions and isolation, NULL and constraints, dialect portability, large tables and pagination, sensitive columns and privileges. Emits a findings list in the standard format. Does not select scope and does not perform a full security or architecture review.

## When to use

- Orchestrated review: the language step when orchestrate-code-review runs on a project that contains SQL.
- SQL-only review: when the user wants query correctness, performance, and safety checked and nothing else.
- Migration or portability: check for dialect-specific constructs.

## Inputs

- A code scope containing SQL (.sql files, embedded SQL, or ORM-generated SQL) (files, snippets, or a diff), supplied by the user or by a scope skill.

## Outputs

- Findings list: location, category=language-sql, severity, title, description, optional suggestion.

## Ecosystem

| Field | Value |
| :------------------------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| overlaps_with (owner/repo:skill-name) | nesnilnehc/ai-cortex:review-codebase, nesnilnehc/ai-cortex:orchestrate-code-review, nesnilnehc/ai-cortex:review-security, nesnilnehc/ai-cortex:review-diff |
| market_position | commodity |

## Full definition

See [SKILL.md](./SKILL.md) for the checklist and the output contract.
