# Promote Roadmap Items

Promotes scored requirements and defects into the roadmap's Now / Next / Later slots in priority order, with goal traceability and dependency readiness. Event-driven, not tied to a fixed cycle.

## Purpose

The skill behind a roadmap planning ceremony: it reads the prioritized backlog, the current roadmap, and the strategic goals, produces promotion and demotion candidates, and — once the user confirms each one — updates the roadmap and supported planning fields while preserving approval status.

## When to use

- **Items completed**: after the previous batch of Now-tier items is done
- **Strategy refresh**: after the strategic goals or priorities change
- **Filling a large gap**: a large governance gap reported by `plan-next` reaches promotion once it has been captured and prioritized
- **Planning on demand**: started by the user, not bound to a fixed cycle

## Inputs

- `docs/process-management/roadmap.md`
- Backlog items whose priority is already set
- `docs/project-overview/strategic-goals.md`

## Outputs

- A decision table in the conversation (promotions plus demotions)
- An updated `roadmap.md`
- Updated project-defined planning fields, where supported; source approval status stays unchanged

## Install

Handled centrally by the canonical AI Cortex install; see the repository root [README](../../README.md#-install-and-use).

## Related skills

- `prioritize-backlog` — upstream: supplies backlog items whose priority is already set
- `define-roadmap` — upstream structural dependency: defines the roadmap structure and promotion criteria
- `design-strategic-goals` — upstream dependency: supplies the strategic goals
- `capture-work-items` — downstream: records the requirements a newly promoted Now item still needs
- `plan-next` — signal source: a large gap reaches Now via capture-work-items → prioritize-backlog → this skill

## Full definition

See [SKILL.md](./SKILL.md).

Roadmap rows contain requirements and defects only. Task-only changes stay in source
task lists unless they change the parent outcome, status or key blocker.
