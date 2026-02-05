# Review Vue

**Status**: validated

## What it does

Reviews Vue 3 code for framework conventions only: Composition API and script setup, reactivity (ref/reactive, computed/watch), component boundaries and props/emits, state (Pinia/store), routing and guards, performance, accessibility. Emits a findings list in the standard format. Does not perform scope selection or security/architecture review.

## When to use

- Orchestrated review: used as the framework step when review-code runs for Vue projects.
- Vue-only review: when the user wants only Vue/frontend framework conventions checked.
- Pre-PR Vue checklist: ensure Composition API usage, reactivity, and component contracts are correct.

## Inputs

- Code scope (files, directories, or diff) containing Vue 3 code (.vue, .ts with Vue APIs), provided by the user or scope skill.

## Outputs

- Findings list: Location, Category=framework-vue, Severity, Title, Description, optional Suggestion.

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
| overlaps_with (owner/repo:skill-name) | nesnilnehc/ai-cortex:review-codebase, review-code, review-diff |
| market_position | commodity |

## Full definition

See [SKILL.md](./SKILL.md) for checklist and output contract.
