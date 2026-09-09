# Review Architecture

**Status**: Validated

## Purpose

Reviews code for architecture only: module and layer boundaries, dependency direction, single responsibility, cyclic dependencies, interface stability, coupling, and extension points. Emits a findings list in the standard format. Does not define scope and does not perform language or security analysis.

## When to use

- Orchestrated review: the cognitive step when review-code runs the whole pipeline.
- Architecture-focused review: when the user wants boundaries and structure checked and nothing else.
- Refactoring or onboarding: understand and critique the current structure.

## Inputs

- A code scope (files, a directory, or a diff) supplied by the user or by a scope skill.

## Outputs

- Findings list: location, category=cognitive-architecture, severity, title, description, optional suggestion.

## Ecosystem

| Field | Value |
| :------------------------------------ | :------------------------------------------------------------------------------------------------------------------------ |
| overlaps_with (owner/repo:skill-name) | nesnilnehc/ai-cortex:review-codebase, nesnilnehc/ai-cortex:review-code, nesnilnehc/ai-cortex:review-diff |
| market_position | commodity |

## Full definition

See [SKILL.md](./SKILL.md) for the checklist and the output contract.
