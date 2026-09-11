# Review Architecture

**Status**: Validated

## Purpose

Executes the canonical [architecture quality Rules](../../rules/architecture-quality.md) over a supplied code scope. It resolves project profiles and topology, gathers evidence, and emits Rule-traceable findings without selecting scope or performing another concern's analysis.

## When to use

- Orchestrated review: the cognitive step when orchestrate-code-review runs the whole pipeline.
- Architecture-focused review: when the user wants boundaries and structure checked and nothing else.
- Refactoring or onboarding: understand and critique the current structure.

## Inputs

- A code scope (files, a directory, or a diff) supplied by the user or by a scope skill.

## Outputs

- Findings list: location, category=cognitive-architecture, severity, title, description, optional suggestion.

## Ecosystem

| Field | Value |
| :------------------------------------ | :------------------------------------------------------------------------------------------------------------------------ |
| overlaps_with (owner/repo:skill-name) | nesnilnehc/ai-cortex:review-codebase, nesnilnehc/ai-cortex:orchestrate-code-review, nesnilnehc/ai-cortex:review-diff |
| market_position | commodity |

## Full definition

See [SKILL.md](./SKILL.md) for execution and boundaries; the criteria live only in [architecture-quality.md](../../rules/architecture-quality.md).
