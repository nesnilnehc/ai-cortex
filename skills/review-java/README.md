# Review Java

**Status**: Validated

## Purpose

Reviews Java code for language and runtime conventions only: concurrency and thread safety, exceptions and try-with-resources, API and version compatibility, collections and streams, NIO and shutdown, testability. Emits a findings list in the standard format. Does not select scope and does not perform security or architecture review.

## When to use

- Orchestrated review: the language step when review-code runs on a Java project.
- Java-only review: when the user wants language and runtime conventions checked and nothing else.
- Pre-PR Java checklist: confirm concurrency, resource management, and API compatibility are right.

## Inputs

- A code scope containing Java code (files, a directory, or a diff), supplied by the user or by a scope skill.

## Outputs

- Findings list: location, category=language-java, severity, title, description, optional suggestion.

## Ecosystem

| Field | Value |
| :------------------------------------ | :------------------------------------------------------------------------------------------------------------------------ |
| overlaps_with (owner/repo:skill-name) | nesnilnehc/ai-cortex:review-codebase, nesnilnehc/ai-cortex:review-code, nesnilnehc/ai-cortex:review-diff |
| market_position | commodity |

## Full definition

See [SKILL.md](./SKILL.md) for the checklist and the output contract.
