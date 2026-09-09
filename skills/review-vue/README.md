# Review Vue

**Status**: Validated

## Purpose

Reviews Vue 3 code for framework conventions only: Composition API and script setup, reactivity (ref/reactive, computed/watch), component boundaries and props/emits, state (Pinia/stores), routing and guards, performance, accessibility. Emits a findings list in the standard format. Does not select scope and does not perform security or architecture review.

## When to use

- Orchestrated review: the framework step when review-code runs on a Vue project.
- Vue-only review: when the user wants Vue/front-end framework conventions checked and nothing else.
- Pre-PR Vue checklist: confirm Composition API usage, reactivity, and component contracts are right.

## Inputs

- A code scope containing Vue 3 code (.vue, or .ts that uses Vue APIs) (files, a directory, or a diff), supplied by the user or by a scope skill.

## Outputs

- Findings list: location, category=framework-vue, severity, title, description, optional suggestion.

## Ecosystem

| Field | Value |
| :------------------------------------ | :------------------------------------------------------------------------------------------------------------------------ |
| overlaps_with (owner/repo:skill-name) | nesnilnehc/ai-cortex:review-codebase, nesnilnehc/ai-cortex:review-code, nesnilnehc/ai-cortex:review-diff |
| market_position | commodity |

## Full definition

See [SKILL.md](./SKILL.md) for the checklist and the output contract.
