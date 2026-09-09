# define-roadmap

Derives a roadmap of milestone nodes from the strategic goals; each node is a stage checkpoint carrying success criteria and traceability back to a goal.

## Purpose

Produces a roadmap document in which every node is a milestone (name, scope, success criteria, goal mapping). Does not define goals or backlog items. The output is saved to `docs/process-management/roadmap.md` or `milestones.md` (per the project norm).

## When to use

- **After the strategic goals**: define the stages or major checkpoints that express how far each goal has progressed.
- **Planning cycle**: settle "what counts as done" for the next 1–2 stages.
- **Governance gate**: supply the milestone roadmap for `plan-next` to assess.
- **Before the backlog**: supply the roadmap so backlog items can be grouped by initiative or theme.

## Inputs

- The strategic goals (document or path); project context.
- Optional: vision/NSM; time horizon; stage preferences.

## Outputs

- A roadmap document (roadmap.md or milestones.md): ordered milestone nodes with scope, success criteria, and goal mapping.

## Install

Handled centrally by the canonical AI Cortex install; see the repository root [README](../../README.md#-install-and-use).

## Related skills

- `design-strategic-goals` — upstream: roadmap nodes (milestones) come from the strategic goals.
- `define-strategic-pillars` — optional input: the pillars can drive how roadmap themes are grouped.
- `plan-next` — downstream: reads milestone status during governance diagnosis.

## Full definition

See [SKILL.md](./SKILL.md) for behavior, limits, and examples.
