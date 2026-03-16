# assess-docs

Assess documentation health in one pass: validate artifact norms compliance (paths, naming, front-matter) and evidence readiness by layer; report gaps and produce a minimum-fill plan.

## What it does

1. **Compliance**: Scans `docs/` against project artifact norms (or spec default); reports path, naming, and front-matter violations with actionable suggestions.
2. **Readiness**: Evaluates whether project docs (goals, requirements, architecture, milestones, roadmap, backlog) are sufficient for reliable AI-assisted planning. Scores each layer as strong, weak, or missing; prioritizes gaps by impact and effort; produces a minimal actionable fill plan.

## When to use

- Pre-commit or audit — ensure docs comply and are sufficient before milestone
- Alignment confidence is low — `align-planning` reports weak evidence
- New repo with partial docs — compliance check and minimum docs to add first
- After norms change — re-validate and re-assess
- Documentation debt triage — one report for both compliance and readiness

## Inputs

- Project docs scope (default: repository `docs/`)
- Optional layer path mapping
- Optional target readiness level (`medium` | `high`)

## Outputs

- Documentation Assessment Report written to `docs/calibration/doc-assessment.md` (overwritten unless a snapshot is requested)
- Single report containing: Compliance Findings (with Location, Severity, Suggestion per violation), Layer Readiness, Gap Priority List, Minimal Fill Plan

## Installation

```bash
npx skills add nesnilnehc/ai-cortex --skill assess-docs
```

## Related skills

- `discover-docs-norms` — establish or update artifact norms
- `bootstrap-docs` — structural docs bootstrap from scratch
- `align-planning` — post-task drift and evidence assessment
- `run-checkpoint` — orchestrate governance including assess-docs

## Full definition

See [SKILL.md](./SKILL.md) for behavior, restrictions, and examples.
