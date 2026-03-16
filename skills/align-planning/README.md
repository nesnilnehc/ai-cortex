# align-planning

Perform post-task traceback, drift detection, and top-down recalibration to keep planning (goals, requirements, milestones, roadmap) aligned with task execution.

## What it does

After a task is completed, runs a traceback from work to strategy, detects drift using a four-type planning model (goal, requirement, roadmap, priority), and produces prioritized recalibration recommendations. Supports Lightweight and Full modes with deterministic selection. Architecture vs code compliance is handled by `align-architecture`.

## When to use

- Post-task checkpoint — validate planning alignment after any completed ticket
- Milestone closure review — run full alignment before marking a milestone complete
- Release readiness — detect planning drift before a release cut
- Scope-shift diagnosis — investigate whether recent work still supports current goals

## Inputs

- Completed task description and outcome
- Optional mode override (`lightweight` | `full`)
- Optional document root and path mapping
- Optional context (release, milestone, epic markers)

## Outputs

- Planning Alignment Report written to `docs/calibration/planning-alignment.md` (overwritten unless a snapshot is requested)
- Machine-readable drifts and evidence readiness block

## Installation

```bash
npx skills add nesnilnehc/ai-cortex --skill align-planning
```

## Related skills

- `align-architecture` — verify ADR/design vs code compliance
- `assess-docs` — assess doc evidence before or after alignment
- `run-checkpoint` — checkpoint cycle including align-planning
- `analyze-requirements` — hand off when requirements need revalidation

## Full definition

See [SKILL.md](./SKILL.md) for behavior, restrictions, and examples.
