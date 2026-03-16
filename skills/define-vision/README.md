# define-vision

Define the long-term future the project aims to create. Answers "What future are we trying to build?"

## What it does

Produces a vision statement (1–3 sentences) describing the desired future state, aligned with the mission. Does not define North Star metric, goals, or milestones. Output is persisted to `docs/project-overview/vision.md` (or project norms).

## When to use

- After mission — establish "what future we build" once "why we exist" is clear.
- Strategy or direction reset — realign on the long-term target.
- Second layer in strategy chain — run after `define-mission` when building mission → vision → north star → goals → milestones.

## Inputs

- Mission (statement or path); project/product context.
- Optional: existing vision draft, time horizon, audience.

## Outputs

- Vision statement document at `docs/project-overview/vision.md` (or per project norms).
- Optional: "Aligned with mission", "Time horizon".

## Installation

```bash
npx skills add nesnilnehc/ai-cortex --skill define-vision
```

## Related skills

- `define-mission` — upstream: why we exist.
- `define-north-star` — next: single metric for user value.
- `design-strategic-goals` — 3–5 strategic outcomes.
- `define-milestones` — phase checkpoints from goals.
- `bootstrap-docs` — doc structure; can create project-overview layout.

## Full definition

See [SKILL.md](./SKILL.md) for behavior, restrictions, and examples.
