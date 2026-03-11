# Review TypeScript

**Status**: validated

## What it does

Reviews TypeScript and JavaScript code for language and runtime conventions only: type safety and type system usage, async patterns and Promise handling, error handling, module design (ESM/CJS), runtime correctness (null/undefined, equality, coercion), API and interface design, and performance and memory. Emits a findings list in the standard format. Does not perform scope selection or security/architecture review.

## When to use

- Orchestrated review: used as the language step when review-code runs for TypeScript/JavaScript projects.
- TypeScript-only review: when the user wants only TypeScript/JavaScript language conventions checked.
- Pre-PR language checklist: ensure type safety, async correctness, and module design are sound.

## Inputs

- Code scope (files, directories, or diff) containing TypeScript or JavaScript code (.ts, .tsx, .js, .jsx, .mts, .mjs, .cts, .cjs), provided by the user or scope skill.

## Outputs

- Findings list: Location, Category=language-typescript, Severity, Title, Description, optional Suggestion.

## Scores (ASQM)

| Dimension        | Score |
| :--------------- | :---- |
| agent_native     | 5     |
| cognitive        | 4     |
| composability    | 5     |
| stance           | 5     |
| **asqm_quality** | 19    |

## Ecosystem

| Field                                 | Value                                                                                                    |
| :------------------------------------ | :------------------------------------------------------------------------------------------------------- |
| overlaps_with (owner/repo:skill-name) | nesnilnehc/ai-cortex:review-codebase, nesnilnehc/ai-cortex:review-code, nesnilnehc/ai-cortex:review-diff |
| market_position                       | commodity                                                                                                |

## Full definition

See [SKILL.md](./SKILL.md) for checklist and output contract.
