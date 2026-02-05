# Review Security

**Status**: validated

## What it does

Reviews code for security only: injection (SQL, command, template), sensitive data and logging, authentication and authorization, dependencies and CVEs, configuration and secrets, cryptography and hashing. Emits a findings list in the standard format. Does not define scope or perform language/architecture analysis.

## When to use

- Orchestrated review: used as a cognitive step when review-code runs the full pipeline.
- Security-focused review: when the user wants only security dimensions checked.
- Compliance or audit: repeatable security checklist output.

## Inputs

- Code scope (files, directories, or diff) provided by the user or scope skill.

## Outputs

- Findings list: Location, Category=cognitive-security, Severity, Title, Description, optional Suggestion.

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
| overlaps_with (owner/repo:skill-name) | nesnilnehc/ai-cortex:review-codebase, review-code, review-sql, review-diff |
| market_position | commodity |

## Full definition

See [SKILL.md](./SKILL.md) for checklist and output contract.
