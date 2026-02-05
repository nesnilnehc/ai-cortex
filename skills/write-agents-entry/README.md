# Write Agents Entry

**Status**: validated

## What it does

Writes or revises AGENTS.md at repo root per the embedded output contract. Establishes project identity, authoritative sources, and behavioral expectations. Executable expectations (must/shall/must not); reference table for spec and index links.

## When to use

- New project: add Agent entry for repo with no AGENTS.md
- Revise existing: audit and complete missing sections
- Adopt format: use output contract for other projects
- Compliance check: audit against contract, output revision suggestions

## Inputs

- One-line positioning
- Top-level assets and dirs
- Optional: AGENTS.md Raw URL, existing entry, primary language

## Outputs

- Full AGENTS.md (or diff/revised text)
- Or audit checklist and revision suggestions

## Scores (ASQM)

| Dimension      | Score |
| :---           | :---  |
| agent_native   | 5     |
| cognitive      | 4     |
| composability  | 4     |
| stance         | 5     |
| **asqm_quality** | 18   |

## Ecosystem

| Field | Value |
| :--- | :--- |
| overlaps_with (owner/repo:skill-name) | nesnilnehc/ai-cortex:generate-standard-readme, nesnilnehc/ai-cortex:refine-skill-design |
| market_position | differentiated |

## Full definition

See [SKILL.md](./SKILL.md) for complete behavior, output contract, restrictions, and examples.
