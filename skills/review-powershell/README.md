# Review PowerShell

**Status**: Validated

## Purpose

Reviews PowerShell code for language and runtime conventions only: advanced function design, parameter validation and binding, error-handling semantics, object pipeline behaviour, compatibility, testability. Emits a findings list in the standard format. Does not select scope and does not perform security or architecture review.

## When to use

- Orchestrated review: the language step when orchestrate-code-review runs on a PowerShell project.
- PowerShell-only review: when the user wants language and runtime conventions checked and nothing else.
- Pre-PR script quality check: verify the parameter contract, pipeline behaviour, and error semantics.

## Inputs

- A code scope containing PowerShell code (files, a directory, or a diff), supplied by the user or by a scope skill.

## Outputs

- Findings list: location, category=language-powershell, severity, title, description, optional suggestion.

## Ecosystem

| Field | Value |
| :------------------------------------ | :------------------------------------------------------------------------------------------------------------------------ |
| overlaps_with (owner/repo:skill-name) | nesnilnehc/ai-cortex:review-codebase, nesnilnehc/ai-cortex:orchestrate-code-review, nesnilnehc/ai-cortex:review-diff |
| market_position | commodity |

## Full definition

See [SKILL.md](./SKILL.md) for the checklist and the output contract.
