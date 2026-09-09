# Orchestrate Roadmap Planning

Chains the atomic skills from strategic goals through promotion in a fixed 9 steps, running one full roadmap planning ceremony. Orchestration only, no domain analysis.

## Purpose

**It exists to satisfy the downstream halt conditions up front.** The most common waste in manual invocation: you get all the way to `promote-roadmap-items` before finding that the roadmap has no capacity allocation, halt, go back and run `define-roadmap`, and start the whole thing over. This skill checks and fills preconditions like that before the call.

Every step carries one of three grades — **required** (runs as soon as its condition matches, cannot be skipped), **default** (can be skipped explicitly), **recommended** (prompts only, never runs on its own). The grade is a mechanical mapping of each atomic skill's existing constraints, not a judgement made by the orchestration layer.

## When to use

- **Full planning**: you need one complete pass from strategy to promotion, not a single-point operation
- **Unsure where it is stuck**: when it is unclear which skill to run now, the health-check step decides
- **Cold start on a new project**: governance documents are missing wholesale and need filling in order

For a single-step operation, call the matching atomic skill directly — `promote-roadmap-items` if you only want promotion, `review-roadmap` if you only want the health check.

## Inputs

- An optional scope hint and any unrecorded raw input
- Governance document paths are discovered automatically, per the project norm

## Outputs

One aggregated report: the result of each step, which steps were skipped and why, the roadmap change list, the capacity usage report, unresolved findings, and next-step suggestions.

## Boundary with the existing orchestration layers

| Skill | Coverage | Relationship |
| :--- | :--- | :--- |
| `plan-next` | Cross-layer, read-only | This skill does not reimplement its goal-tree walk |
| `orchestrate-governance-step` | Cross-layer, executes 1 suggestion | It can call this skill as one executable action |
| This skill | The roadmap vertical slice only | Must not call back into either of the two above |

In one line: `plan-next` answers "what the whole project does next", and this skill answers "the roadmap track, walked from strategy to promotion in one go".

## Install

Handled centrally by the canonical AI Cortex install; see the repository root [README](../../README.md#-install-and-use).

## Related skills

The atomic skills it orchestrates: `review-roadmap`, `design-strategic-goals`, `define-roadmap`, `capture-work-items`, `prioritize-backlog`, `map-item-dependencies`, `promote-roadmap-items`, `update-roadmap`, `archive-milestone`.

## Full definition

See [SKILL.md](./SKILL.md).
