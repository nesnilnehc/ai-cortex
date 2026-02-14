# Review Architecture

**Status**: validated

## What it does

Reviews code for architecture only: module and layer boundaries, dependency direction, single responsibility, cyclic dependencies, interface stability, coupling and extension points. Emits a findings list in the standard format. Does not define scope or perform language/security analysis.

## When to use

- Orchestrated review: used as a cognitive step when review-code runs the full pipeline.
- Architecture-focused review: when the user wants only boundaries and structure checked.
- Refactor or onboarding: understand and critique current structure.

## Inputs

- Code scope (files, directories, or diff) provided by the user or scope skill.

## Outputs

- Findings list: Location, Category=cognitive-architecture, Severity, Title, Description, optional Suggestion.

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
