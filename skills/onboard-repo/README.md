# Onboard Repository (Orchestrator)

**Status**: validated

## What it does

Orchestrates repository onboarding by running codebase review, architecture assessment, README generation, and Agent entry setup in sequence, then aggregates all outputs into a single onboarding report. Does not perform analysis or write documentation itself; invokes review-codebase, review-architecture, generate-standard-readme, write-agents-entry, and optionally discover-skills.

## When to use

- New team member onboarding: rapidly understand a new or unfamiliar repository.
- Repository acquisition or handoff: assess structure, quality, and documentation gaps.
- Open-source preparation: ensure documentation and architecture quality before going public.
- For individual tasks (e.g. only generating a README or only reviewing architecture), use the corresponding atomic skill instead.

## Inputs

- Repository root path or directory to onboard.
- User preferences (improve existing docs, skip optional steps).

## Outputs

- Single aggregated onboarding report (diagnostic-report format: Repository Summary, Architecture Findings, Tech Debt, Documentation Status, Skill Recommendations, Action Items).
- Generated or improved README.md and AGENTS.md files.

## Scores (ASQM)

| Dimension        | Score |
| :--------------- | :---- |
| agent_native     | 5     |
| cognitive        | 5     |
| composability    | 5     |
| stance           | 5     |
| **asqm_quality** | 20    |

## Ecosystem

| Field                                 | Value                                                                  |
| :------------------------------------ | :--------------------------------------------------------------------- |
| overlaps_with (owner/repo:skill-name) | nesnilnehc/ai-cortex:review-codebase, nesnilnehc/ai-cortex:review-code |
| market_position                       | differentiated                                                         |

## Full definition

See [SKILL.md](./SKILL.md) for execution order, behavior, and output contract.
