# align-architecture

Verify architecture and design documents against code implementation; produce an Architecture Compliance Report when implementation diverges from ADR or design decisions.

## What it does

Compares documented architecture and design decisions (ADRs, design docs) against the codebase, detects compliance gaps (boundary violations, missing components, divergent patterns), and produces a prioritized report with impact and remediation suggestions.

## When to use

- Post-implementation check — validate that implementation matches ADR or design doc
- Milestone or release gate — ensure architecture decisions are reflected in code
- Drift investigation — diagnose when implementation has drifted from documented design

## Inputs

- Optional ADR or design doc paths
- Optional code scope (paths or modules)
- Optional project docs root

## Outputs

- Architecture Compliance Report written to `docs/calibration/architecture-compliance.md` (overwritten unless a snapshot is requested)
- Machine-readable compliance gaps block

## Installation

```bash
npx skills add nesnilnehc/ai-cortex --skill align-architecture
```

## Related skills

- `align-planning` — planning layer alignment (goals, requirements, roadmap, milestones)
- `review-architecture` — code-only structure review (boundaries, dependencies)
- `design-solution` — design creation or design alternatives

## Full definition

See [SKILL.md](./SKILL.md) for behavior, restrictions, and examples.
