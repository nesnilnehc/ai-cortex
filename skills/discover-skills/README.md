# Discover Skills

**Status**: validated

## What it does

Identifies missing skills for a task and recommends concrete installation steps from AI Cortex or public catalogs. Discovers candidates and suggests what to install; does not install or inject skills automatically.

## When to use

- Initial bootstrap: Agent starts with this skill, then recommends what to install
- On-demand extension: when a task requires a skill not available
- Capability discovery: help users find relevant skills from local or public catalogs

## Inputs

- Current task description
- Optional: list of already installed skills, allowed sources (local vs public)

## Outputs

- Recommended skills with rationale
- Install commands for each (e.g. `npx skills add owner/repo --skill name`)

## Scores (ASQM)

| Dimension      | Score |
| :---           | :---  |
| agent_native   | 5     |
| cognitive      | 3     |
| composability  | 5     |
| stance         | 4     |
| **asqm_quality** | 17   |

## Ecosystem

| Field | Value |
| :--- | :--- |
| overlaps_with (owner/repo:skill-name) | nesnilnehc/ai-cortex:refine-skill-design |
| market_position | differentiated |

## Full definition

See [SKILL.md](./SKILL.md) for complete behavior, restrictions, and examples.
