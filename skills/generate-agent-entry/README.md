# Generate Agent Entry

**Status**: Validated

## Purpose

Writes or revises AGENTS.md at the repository root against the embedded output contract. Establishes the project identity, the authoritative sources, and the behavioral expectations. Actionable expectations (must / should / must not); a reference table of spec and index links.

## When to use

- New project: add an agent entry to a repository that has no AGENTS.md
- Revising what exists: audit it and complete the missing sections
- Adopting the format: apply the output contract to other projects
- Compliance check: audit against the contract and emit suggested revisions

## Inputs

- The one-line positioning
- Top-level assets and directories
- Optional: the raw AGENTS.md URL, an existing entry, the primary language

## Outputs

- A complete AGENTS.md (or diff/revision text)
- Or an audit checklist plus suggested revisions

## Ecosystem

| Field | Value |
| :------------------------------------ | :------------------------------------------------------------------------------------------ |
| overlaps_with (owner/repo: skill name) | nesnilnehc/ai-cortex:generate-standard-readme, nesnilnehc/ai-cortex:refine-skill-design |
| Market position | Differentiated |

## Full definition

See [SKILL.md](./SKILL.md) for the full behavior, the output contract, limits, and examples.
