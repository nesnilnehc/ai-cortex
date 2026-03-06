# project-cognitive-loop

Orchestrate project governance cycles by routing between requirements analysis, design, execution alignment, and documentation readiness checks.

## What it does

Runs repeatable governance loops by orchestrating atomic skills: `analyze-requirements`, `brainstorm-design`, `execution-alignment`, `documentation-readiness`, and optionally `run-repair-loop`. Classifies triggers (task-complete, milestone-closed, release-candidate, scope-change, periodic-review) and selects the right skill sequence. Aggregates outputs into a single cycle report.

## When to use

- Task completed — verify alignment and docs sufficiency before next priority
- Milestone closed — run full governance check
- Release candidate — run design, alignment, and docs readiness gate
- Quarterly planning refresh — revisit requirements and architecture drift

## Inputs

- Trigger event and context
- Optional target scope and mode overrides
- Optional urgency or release window

## Outputs

- Project Cognitive Loop Report written to `docs/calibration/YYYY-MM-DD-cognitive-loop.md`
- Routed sequence, aggregated findings, blockers, next-cycle actions

## Installation

```bash
npx skills add nesnilnehc/ai-cortex --skill project-cognitive-loop
```

## Related skills

- `execution-alignment` — post-task traceback and drift detection
- `documentation-readiness` — docs evidence assessment
- `onboard-repo` — repo onboarding orchestration (different control-plane use case)

## Full definition

See [SKILL.md](./SKILL.md) for behavior, restrictions, and examples.
