# Review Python

**Status**: Validated

## Purpose

Reviews Python code for language and runtime conventions only: type hints, exceptions, async/await, context managers, dependencies, testability. Emits a findings list in the standard format. Does not select scope and does not perform security or architecture review.

## When to use

- Orchestrated review: the language step when review-code runs on a Python project.
- Python-only review: when the user wants language and runtime conventions checked and nothing else.
- Pre-PR Python checklist: confirm type hints, exception handling, and async patterns are right.

## Inputs

- A code scope containing Python code (files, a directory, or a diff), supplied by the user or by a scope skill.

## Outputs

- Findings list: location, category=language-python, severity, title, description, optional suggestion.

## Ecosystem

| Field | Value |
| :------------------------------------ | :------------------------------------------------------------------------------------------------------------------------ |
| overlaps_with (owner/repo:skill-name) | nesnilnehc/ai-cortex:review-codebase, nesnilnehc/ai-cortex:review-code, nesnilnehc/ai-cortex:review-diff |
| market_position | commodity |

## Full definition

See [SKILL.md](./SKILL.md) for the checklist and the output contract.
