# Review PHP

**Status**: validated

## What it does

Reviews PHP code for language and runtime conventions only: strict types and declarations, error handling, resource management, PSR standards (PSR-4, PSR-12), namespaces, null safety, generators and iterables, PHP version compatibility, testability. Emits a findings list in the standard format. Does not perform scope selection or security/architecture review.

## When to use

- Orchestrated review: used as the language step when review-code runs for PHP projects.
- PHP-only review: when the user wants only language/runtime conventions checked.
- Pre-PR PHP checklist: ensure type safety, resource cleanup, and PSR compliance are correct.

## Inputs

- Code scope (files, directories, or diff) containing PHP code, provided by the user or scope skill.

## Outputs

- Findings list: Location, Category=language-php, Severity, Title, Description, optional Suggestion.

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
