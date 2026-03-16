# define-strategic-pillars

Derive 3–5 strategic pillars (high-level themes) from vision and North Star to structure goals and roadmap.

## What it does

Produces a strategic pillars document with 3–5 themes aligned with vision and North Star. Goals and roadmap can be grouped under pillars. Does not define mission, vision, North Star, goals, milestones, or roadmap. Output is persisted to `docs/project-overview/strategic-pillars.md` (or project norms).

## When to use

- After vision and North Star — establish pillars that structure how goals and roadmap are organized.
- Strategy structure — provide stable themes so goals and initiatives can be grouped.
- Fourth layer in strategy chain — Mission → Vision → North Star → Pillars → Goals → Milestones → Roadmap.

## Inputs

- Vision; North Star (or paths); project context.
- Optional: mission; existing goals or pillars.

## Outputs

- Strategic pillars document at `docs/project-overview/strategic-pillars.md`: 3–5 pillars with name, description, alignment to vision/NSM.

## Installation

```bash
npx skills add nesnilnehc/ai-cortex --skill define-strategic-pillars
```

## Related skills

- `define-vision`, `define-north-star` — upstream: pillars derive from these.
- `design-strategic-goals` — downstream: goals can map to pillars.
- `define-roadmap` — downstream: roadmap themes can align to pillars.

## Full definition

See [SKILL.md](./SKILL.md) for behavior, restrictions, and examples.
