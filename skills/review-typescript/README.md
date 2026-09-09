# Review TypeScript

**Status**: Validated

## Purpose

Reviews TypeScript and JavaScript code for language and runtime conventions only: type safety and type-system usage, async patterns and promise handling, error handling, module design (ESM/CJS), runtime correctness (null/undefined, equality, coercion), API and interface design, and performance and memory. Emits a findings list in the standard format. Does not select scope and does not perform security or architecture review.

## When to use

- Orchestrated review: the language step when review-code runs on a TypeScript/JavaScript project.
- TypeScript-only review: when the user wants TypeScript/JavaScript language conventions checked and nothing else.
- Pre-PR language checklist: confirm type safety, async correctness, and module design are sound.

## Inputs

- A code scope containing TypeScript or JavaScript code (.ts, .tsx, .js, .jsx, .mts, .mjs, .cts, .cjs) (files, a directory, or a diff), supplied by the user or by a scope skill.

## Outputs

- Findings list: location, category=language-typescript, severity, title, description, optional suggestion.

## Ecosystem

| Field | Value |
| :------------------------------------ | :------------------------------------------------------------------------------------------------------------------------ |
| overlaps_with (owner/repo:skill-name) | nesnilnehc/ai-cortex:review-codebase, nesnilnehc/ai-cortex:review-code, nesnilnehc/ai-cortex:review-diff |
| market_position | commodity |

## Full definition

See [SKILL.md](./SKILL.md) for the checklist and the output contract.
