# Review React

**Status**: validated

## What it does

Reviews React code for framework conventions only: component design (functional, composition, props), hooks correctness (dependency arrays, rules of hooks, cleanup), state management (local, context, external stores, server state), rendering performance (memo, keys, virtualization), side effects and data fetching, routing and code splitting, and accessibility. Emits a findings list in the standard format. Does not perform scope selection or security/architecture review.

## When to use

- Orchestrated review: used as the framework step when review-code runs for React projects.
- React-only review: when the user wants only React/frontend framework conventions checked.
- Pre-PR React checklist: ensure hooks usage, component design, and state management patterns are correct.

## Inputs

- Code scope (files, directories, or diff) containing React code (.tsx, .jsx, .ts, .js with React APIs), provided by the user or scope skill.

## Outputs

- Findings list: Location, Category=framework-react, Severity, Title, Description, optional Suggestion.

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
| overlaps_with (owner/repo:skill-name) | nesnilnehc/ai-cortex:review-codebase, nesnilnehc/ai-cortex:review-code, nesnilnehc/ai-cortex:review-diff |
| market_position | commodity |

## Full definition

See [SKILL.md](./SKILL.md) for checklist and output contract.
