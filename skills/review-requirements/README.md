# Review Requirements

**Status**: Validated

## Purpose

Reviews an existing requirements document for quality across six dimensions: clarity of the problem statement, testability of the requirements (acceptance criteria + R-NN IDs), completeness of the constraint inventory, scope boundedness (the V1 boundary), requirement ID format and uniqueness, and open questions with a plan to resolve them. Emits a findings list in the standard format so the author can close the gaps before handing off to design-solution.

## When to use

- Pre-design gate: validate the requirements document before invoking design-solution.
- Collaborative review: a team member writes the requirements; a second party assesses the quality independently.
- Imported requirements: requirements come from an external tool (Confluence, Notion, Jira) and need a quality assessment before they are used in this workflow.
-post-analyze-requirements validation: an independent check that every success criterion is met.

## Inputs

- A requirements document (a path, for example `docs/requirements-planning/<topic>.md`, or the raw content).
- Optional project background or the downstream skill (for example "this feeds design-solution").

## Outputs

- Findings list: location (a section heading or an R-NN ID), category=`requirements-quality`, severity, title, description, optional suggestion.
- Zero findings → confirmation that the document is ready for design-solution.

## Ecosystem

| Field | Value |
| :------------------------------------ | :-------------------------------------------------------- |
| overlaps_with (owner/repo:skill-name) | nesnilnehc/ai-cortex:analyze-requirements |
| market_position | differentiated |

## Full definition

See [SKILL.md](./SKILL.md) for the checklist, the limits, and the output contract.
