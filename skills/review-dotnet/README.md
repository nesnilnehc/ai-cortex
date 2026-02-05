# Review .NET

**Status**: validated

## What it does

Reviews .NET (C#, F#) code for language and runtime conventions only: async/await and ConfigureAwait, nullable reference types, API and versioning, IDisposable and resources, collections and LINQ, testability. Emits a findings list in the standard format. Does not perform scope selection or security/architecture review.

## When to use

- Orchestrated review: used as the language step when review-code runs for .NET projects.
- .NET-only review: when the user wants only language/runtime conventions checked.
- Pre-PR .NET checklist: ensure async, nullable, and resource patterns are correct.

## Inputs

- Code scope (files, directories, or diff) containing .NET code, provided by the user or scope skill.

## Outputs

- Findings list: Location, Category=language-dotnet, Severity, Title, Description, optional Suggestion.

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
