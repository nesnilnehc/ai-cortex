# Review Roadmap

Evaluates an existing roadmap document against `rules/roadmap-quality.md` and produces a findings list. It evaluates only; it does not rewrite.

## Purpose

Reviews roadmap quality across five dimensions: completeness (the four parts of the core model, the capacity baseline and its allocation), executability (whether the denominator exists, the WIP limit, goal ownership), clarity (metric triplets, outcome phrasing and hypothesis phrasing), soundness (outcome-driven items, mapped dependencies, change frequency), and traceability (goal mapping, the explicit not-doing list). **The criteria are not embedded in the skill** — every one of them is cited from the rule, so when a criterion changes, that rule changes and the skill does not.

## When to use

- **Gate before promotion**: when the capacity and dependency criteria do not hold, promotion cannot compute a correct result
- **Taking over someone else's roadmap**: see quickly what this roadmap is missing
- **Periodic health check**: a roadmap is a living document and drifts over time
- **Entry point of the orchestration chain**: step 0 of `orchestrate-roadmap-planning`

## Inputs

- The existing roadmap document (a path or the content)
- [rules/roadmap-quality.md](../../rules/roadmap-quality.md) (halt when it is missing)
- Corroborating sources: `docs/project-overview/strategic-goals.md` and the backlog items the Now tier references

## Outputs

- A findings list (location / category / severity / title / description / suggestion)
- An explicit statement of any dimension that could not be evaluated, with the reason
- When there are zero findings, an explicit statement that every criterion passed

## Boundaries

It neither generates nor rewrites a roadmap — structural gaps hand off to `define-roadmap`, and status or timing gaps hand off to `update-roadmap`. **It emits no orchestration mode**: detecting the context is the orchestration layer's own job.

## Installation

Installation is handled centrally by the AI Cortex canonical installer; see the repository root [README](../../README.md#-install-and-use).

## Related skills

- `define-roadmap` — downstream handoff: it fixes the structural findings
- `update-roadmap` — downstream handoff: it fixes the status and timing findings
- `review-requirements` — same family: another atomic skill that evaluates an existing governance document, sharing the same IO contract
- `orchestrate-roadmap-planning` — the orchestrator: this skill is its step 0 and supplies the basis for its conditional decisions

## Full definition

See [SKILL.md](./SKILL.md).
