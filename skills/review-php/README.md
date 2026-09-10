# Review PHP

**Status**: Validated

## Purpose

Reviews PHP code for language and runtime conventions only: strict types and declarations, error handling, resource management, PSR standards (PSR-4, PSR-12), namespaces, null safety, generators and iterables, PHP version compatibility, testability. Emits a findings list in the standard format. Does not select scope and does not perform security or architecture review.

## When to use

- Orchestrated review: the language step when orchestrate-code-review runs on a PHP project.
- PHP-only review: when the user wants language and runtime conventions checked and nothing else.
- Pre-PR PHP checklist: confirm type safety, resource cleanup, and PSR compliance are right.

## Inputs

- A code scope containing PHP code (files, a directory, or a diff), supplied by the user or by a scope skill.

## Outputs

- Findings list: location, category=language-php, severity, title, description, optional suggestion.

## Ecosystem

| Field | Value |
| :------------------------------------ | :------------------------------------------------------------------------------------------------------------------------ |
| overlaps_with (owner/repo:skill-name) | nesnilnehc/ai-cortex:review-codebase, nesnilnehc/ai-cortex:orchestrate-code-review, nesnilnehc/ai-cortex:review-diff |
| market_position | commodity |

## Full definition

See [SKILL.md](./SKILL.md) for the checklist and the output contract.
