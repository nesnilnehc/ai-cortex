# Review React

**Status**: Validated

## Purpose

Reviews React code for framework conventions only: component design (function components, composition, props), hook correctness (dependency arrays, rules of hooks, cleanup), state management (local, context, external stores, server state), render performance (memo, keys, virtualisation), side effects and data fetching, routing and code splitting, and accessibility. Emits a findings list in the standard format. Does not select scope and does not perform security or architecture review.

## When to use

- Orchestrated review: the framework step when orchestrate-code-review runs on a React project.
- React-only review: when the user wants React/front-end framework conventions checked and nothing else.
- Pre-PR React checklist: confirm hook usage, component design, and state-management patterns are right.

## Inputs

- A code scope containing React code (.tsx, .jsx, .ts, or .js that uses React APIs) (files, a directory, or a diff), supplied by the user or by a scope skill.

## Outputs

- Findings list: location, category=framework-react, severity, title, description, optional suggestion.

## Ecosystem

| Field | Value |
| :------------------------------------ | :------------------------------------------------------------------------------------------------------------------------ |
| overlaps_with (owner/repo:skill-name) | nesnilnehc/ai-cortex:review-codebase, nesnilnehc/ai-cortex:orchestrate-code-review, nesnilnehc/ai-cortex:review-diff |
| market_position | commodity |

## Full definition

See [SKILL.md](./SKILL.md) for the checklist and the output contract.
