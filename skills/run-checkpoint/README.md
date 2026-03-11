# run-checkpoint

Analyze project state and produce next-action plan by running alignment, doc readiness, and output-driven follow-ups.

## What it does

**Phase 0.5 (Planning Readiness Gate)**: When project docs are missing, runs `discover-document-norms`, `bootstrap-docs`, or `assess-doc-readiness` to prepare; short-circuits with Minimal Fill Plan when readiness is too low.

**Phase 1**: Runs unified sequence `align-planning` (full) -> `assess-doc-readiness`, then output-driven follow-ups (`align-architecture`, `run-repair-loop`, `brainstorm-design`, `analyze-requirements`) when findings indicate need. Aggregates outputs into a single cycle report with Recommended Next Tasks.

## When to use

- Task completed — verify alignment and docs sufficiency before next priority
- Milestone closed — run full governance check
- Release candidate — run design, alignment, and docs readiness gate
- Periodic iteration — checkpoint project state and get next actions

## Inputs

- Trigger event and context
- Optional target scope and mode overrides
- Optional urgency or release window

## Outputs

- Cycle report written to `docs/calibration/cognitive-loop.md` (single artifact; overwritten unless a snapshot is requested)
- Routed sequence, aggregated findings, blockers, Recommended Next Tasks (prioritized, actionable, with owner, scope, rationale)

## Installation

```bash
npx skills add nesnilnehc/ai-cortex --skill run-checkpoint
```

## Related skills

- `align-planning` — post-task traceback and planning drift detection
- `align-architecture` — architecture vs code compliance verification
- `assess-doc-readiness` — doc evidence assessment
- `discover-document-norms` — establish artifact paths (Phase 0.5)
- `bootstrap-docs` — create docs structure (Phase 0.5)
- `onboard-repo` — repo onboarding orchestration (different control-plane use case)

## Full definition

See [SKILL.md](./SKILL.md) for behavior, restrictions, and examples.
