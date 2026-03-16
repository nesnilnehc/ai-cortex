# Align Backlog

**Status**: validated

## What it does

Aligns the product or work backlog with current strategy, goals, and roadmap. Inventories backlog items, maps each to a strategic anchor (goal, milestone, or roadmap theme), classifies alignment status (aligned / partial / misaligned / orphan), and produces a Backlog Alignment Report with concrete change proposals: cuts, merges, reprioritization, and suggested additions.

## When to use

- After a strategy or roadmap refresh — re-map backlog to updated goals.
- Sprint or release prep — trim and prioritize using strategy as source of truth.
- Backlog health check — identify orphan or misaligned items before they accumulate.
- Orphan cleanup — propose removal or repurposing of work no longer tied to strategy.

## Inputs

- Optional backlog path or project convention.
- Optional strategy docs root (goals, roadmap, milestones in `docs/project-overview/`, `docs/process-management/`).
- Optional scope: full backlog or subset (by epic, label, or time window).

## Outputs

- Backlog Alignment Report (`docs/calibration/backlog-alignment.md`; living artifact).
- Machine-readable alignment summary and change proposals block (YAML) embedded in the report.

## Scores (ASQM)

| Dimension        | Score |
| :--------------- | :---- |
| agent_native     | 4     |
| cognitive        | 4     |
| composability    | 4     |
| stance           | 5     |
| **asqm_quality** | 17    |

## Ecosystem

| Field                                 | Value                                                                                                          |
| :------------------------------------ | :------------------------------------------------------------------------------------------------------------- |
| overlaps_with (owner/repo:skill-name) | nesnilnehc/ai-cortex:align-planning, nesnilnehc/ai-cortex:plan-next, nesnilnehc/ai-cortex:capture-work-items |
| market_position                       | differentiated                                                                                                 |

## Full definition

See [SKILL.md](./SKILL.md) for checklist, restrictions, and output contract.
