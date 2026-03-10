# orchestrate-governance-loop

Orchestrate project governance cycles by routing between requirements analysis, design, execution alignment, and documentation readiness checks.

## What it does

Runs repeatable governance loops with a unified sequence: `align-execution` (full) -> `assess-documentation-readiness`, then output-driven follow-ups (`align-architecture`, `run-repair-loop`, `brainstorm-design`, `analyze-requirements`) when findings indicate need. Trigger is metadata only (does not drive routing). Aggregates outputs into a single cycle report.

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

- `align-execution` — post-task traceback and planning drift detection
- `align-architecture` — architecture vs code compliance verification
- `assess-documentation-readiness` — docs evidence assessment
- `onboard-repo` — repo onboarding orchestration (different control-plane use case)

## Full definition

See [SKILL.md](./SKILL.md) for behavior, restrictions, and examples.
