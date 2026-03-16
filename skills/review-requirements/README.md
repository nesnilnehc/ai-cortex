# Review Requirements

**Status**: validated

## What it does

Reviews an existing requirements document for quality across six dimensions: problem statement clarity, testability of needs (acceptance criteria + R-NN IDs), constraint inventory completeness, scope boundedness (V1 boundary), requirement ID format and uniqueness, and open questions with resolution plans. Emits a findings list in the standard format so the author can fix gaps before handing off to `design-solution`.

## When to use

- Pre-design gate: verify a requirements document before `design-solution` is invoked.
- Collaborative review: a team member authored requirements; a second party assesses quality independently.
- Imported requirements: requirements came from an external tool (Confluence, Notion, Jira) and need quality assessment before use in this workflow.
- Post-`analyze-requirements` validation: independent check that all success criteria were met.

## Inputs

- Requirements document (path, e.g. `docs/requirements-planning/<topic>.md`, or raw content).
- Optional project context or downstream skill (e.g. "this feeds design-solution").

## Outputs

- Findings list: Location (section heading or R-NN ID), Category=`requirements-quality`, Severity, Title, Description, optional Suggestion.
- Zero findings → confirmation that document is ready for `design-solution`.

## Scores (ASQM)

| Dimension        | Score |
| :--------------- | :---- |
| agent_native     | 5     |
| cognitive        | 4     |
| composability    | 5     |
| stance           | 5     |
| **asqm_quality** | 19    |

## Ecosystem

| Field                                 | Value                                        |
| :------------------------------------ | :------------------------------------------- |
| overlaps_with (owner/repo:skill-name) | nesnilnehc/ai-cortex:analyze-requirements   |
| market_position                       | differentiated                               |

## Full definition

See [SKILL.md](./SKILL.md) for checklist, restrictions, and output contract.
