# Review Python

**Status**: validated

## What it does

Reviews Python code for language and runtime conventions only: type hints, exceptions, async/await, context managers, dependencies, testability. Emits a findings list in the standard format. Does not perform scope selection or security/architecture review.

## When to use

- Orchestrated review: used as the language step when review-code runs for Python projects.
- Python-only review: when the user wants only language/runtime conventions checked.
- Pre-PR Python checklist: ensure type hints, exception handling, and async patterns are correct.

## Inputs

- Code scope (files, directories, or diff) containing Python code, provided by the user or scope skill.

## Outputs

- Findings list: Location, Category=language-python, Severity, Title, Description, optional Suggestion.

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
