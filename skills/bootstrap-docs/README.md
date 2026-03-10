# Bootstrap Project Documentation

**Status**: validated

## What it does

Bootstrap or adapt project documentation using the [project-documentation-template](https://github.com/nesnilnehc/project-documentation-template) structure. Two modes: **Initialize** (empty project—copy templates and fill placeholders) and **Adjust** (non-empty—use template as target, rename/move/merge in-place, apply after confirmation). Repeatable runs; no empty dirs unless requested; strict kebab-case naming.

## When to use

- Empty project: initialize full docs skeleton for small/medium/large projects
- Non-empty project: analyze existing docs, recommend alignment with template, apply changes after confirmation
- Shared workflows: generate ADR, update version across docs, validate placeholders and links

## Inputs

- Project metadata (name, description, tech stack)
- Scale (small | medium | large, optional; inferred from context if absent)
- Mode override (initialize | adjust, optional)

## Outputs

- **Initialize**: Filled docs under `docs/`, `VERSION` file, summary of created files
- **Adjust**: Recommendation list (markdown), then applied changes and summary after user confirmation

## Scores (ASQM)

| Dimension      | Score |
| :---           | :---  |
| agent_native   | 5     |
| cognitive      | 4     |
| composability  | 4     |
| stance         | 5     |
| **asqm_quality** | 18  |

## Ecosystem

| Field | Value |
| :--- | :--- |
| overlaps_with (owner/repo:skill-name) | nesnilnehc/ai-cortex:generate-standard-readme, nesnilnehc/ai-cortex:write-agents-entry |
| market_position | differentiated |

## Full definition

See [SKILL.md](./SKILL.md) for complete behavior, restrictions, and examples.
