# assess-documentation-readiness

Assess documentation evidence readiness across project layers, report gaps, and produce a minimum-fill plan to improve alignment reliability.

## What it does

Evaluates whether project docs (goals, requirements, architecture, milestones, roadmap, backlog) are sufficient for reliable AI-assisted planning. Scores each layer as strong, weak, or missing; prioritizes gaps by impact and effort; produces a minimal actionable fill plan.

## When to use

- Alignment confidence is low — `align-execution` reports weak evidence
- New repo with partial docs — team needs to know the minimum docs to add first
- Pre-release governance — verify documentation sufficiency before milestone closure
- Documentation debt triage — prioritize docs work without boiling the ocean

## Inputs

- Project docs scope
- Optional layer path mapping
- Optional target readiness level (`medium` | `high`)

## Outputs

- Documentation Readiness Report written to `docs/calibration/YYYY-MM-DD-doc-readiness.md`
- Minimal fill plan with layer readiness and gap priority list

## Installation

```bash
npx skills add nesnilnehc/ai-cortex --skill assess-documentation-readiness
```

## Related skills

- `bootstrap-project-documentation` — structural docs bootstrap from scratch
- `align-execution` — post-task drift and evidence assessment
- `orchestrate-governance-loop` — orchestrate governance including assess-documentation-readiness

## Full definition

See [SKILL.md](./SKILL.md) for behavior, restrictions, and examples.
