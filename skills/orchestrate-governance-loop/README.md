# orchestrate-governance-loop

Orchestrate project governance cycles by routing between requirements analysis, design, execution alignment, and documentation readiness checks.

## What it does

Runs repeatable governance loops by orchestrating atomic skills: `analyze-requirements`, `brainstorm-design`, `align-execution`, `assess-documentation-readiness`, and optionally `run-repair-loop`. Classifies triggers (task-complete, milestone-closed, release-candidate, scope-change, periodic-review) and selects the right skill sequence. Aggregates outputs into a single cycle report.

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

- Governance Loop Report written to `docs/calibration/YYYY-MM-DD-cognitive-loop.md` (single artifact; routed skills do not produce separate files)
- Routed sequence, aggregated findings, blockers, Recommended Next Tasks (prioritized, actionable, with owner, scope, rationale)

## Installation

```bash
npx skills add nesnilnehc/ai-cortex --skill orchestrate-governance-loop
```

## Related skills

- `align-execution` — post-task traceback and drift detection
- `assess-documentation-readiness` — docs evidence assessment
- `onboard-repo` — repo onboarding orchestration (different control-plane use case)

## Full definition

See [SKILL.md](./SKILL.md) for behavior, restrictions, and examples.
