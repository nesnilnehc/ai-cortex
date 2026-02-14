# Review SQL

**Status**: validated

## What it does

Reviews SQL and query code for language and query conventions only: injection and parameterization, indexing and execution plan, transactions and isolation, NULL and constraints, dialect portability, large-table and paging, sensitive columns and permissions. Emits a findings list in the standard format. Does not perform scope selection or full security/architecture review.

## When to use

- Orchestrated review: used as the language step when review-code runs for projects that include SQL.
- SQL-only review: when the user wants only query correctness, performance, and safety checked.
- Migration or portability: check dialect-specific constructs.

## Inputs

- Code scope (files, snippets, or diff) containing SQL (.sql files, embedded SQL, or ORM-generated SQL), provided by the user or scope skill.

## Outputs

- Findings list: Location, Category=language-sql, Severity, Title, Description, optional Suggestion.

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
| overlaps_with (owner/repo:skill-name) | nesnilnehc/ai-cortex:review-codebase, nesnilnehc/ai-cortex:review-code, nesnilnehc/ai-cortex:review-security, nesnilnehc/ai-cortex:review-diff |
| market_position | commodity |

## Full definition

See [SKILL.md](./SKILL.md) for checklist and output contract.
