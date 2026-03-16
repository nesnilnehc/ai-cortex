# define-milestones

Break strategic goals into concrete phase checkpoints (milestones) that represent major progress stages.

## What it does

Produces a milestones document derived from strategic goals: each milestone has name, scope, success criterion, optional timeframe, and explicit mapping to at least one strategic goal. Does not define goals, requirements, or backlog. Output is persisted to `docs/process-management/milestones.md` (or project norms).

## When to use

- After strategic goals — define phases or checkpoints that indicate progress toward each goal.
- Release or planning cycle — establish "what done looks like" for the next 1–2 phases.
- Fifth layer in strategy chain — run after mission, vision, north star, and strategic goals.
- Governance — provide milestones for `run-checkpoint` or `align-planning`.

## Inputs

- Strategic goals (document or path); project context.
- Optional: vision/NSM; existing roadmap or phases; time constraints.

## Outputs

- Milestones document at `docs/process-management/milestones.md` (or project norms): list of milestones with goal mapping.

## Installation

```bash
npx skills add nesnilnehc/ai-cortex --skill define-milestones
```

## Related skills

- `design-strategic-goals` — upstream: milestones break down these goals.
- `define-vision` / `define-north-star` — context for alignment.
- `align-planning` — can use milestones for traceback.
- `run-checkpoint` — governance cycle can reference milestones.
- `capture-work-items` — backlog items can reference milestones.

## Full definition

See [SKILL.md](./SKILL.md) for behavior, restrictions, and examples.
