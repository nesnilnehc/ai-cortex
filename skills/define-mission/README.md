# define-mission

Define the fundamental purpose of a project or organization. Answers "Why does this project exist?"

## What it does

Elicits and documents a single mission statement (1–3 sentences) that states why the project exists. Does not define vision, North Star metric, goals, or milestones. Output is persisted to `docs/project-overview/mission.md` (or project norms).

## When to use

- New project or initiative — establish "why we exist" before vision or strategy.
- Strategy refresh — re-anchor when direction is unclear.
- Top of strategy chain — run first when building mission → vision → north star → goals → milestones.

## Inputs

- Project or product identifier; current understanding of purpose (from docs, README, or user).
- Optional: existing mission draft, audience, problem statement.

## Outputs

- Mission statement document at `docs/project-overview/mission.md` (or per project norms).
- Optional: "For whom", "Core problem addressed" (1–2 lines).

## Installation

```bash
npx skills add nesnilnehc/ai-cortex --skill define-mission
```

## Related skills

- `define-vision` — next layer: what future we build.
- `define-north-star` — single metric for user value.
- `design-strategic-goals` — 3–5 strategic outcomes.
- `define-milestones` — phase checkpoints from goals.
- `bootstrap-docs` — doc structure; can create project-overview layout.

## Full definition

See [SKILL.md](./SKILL.md) for behavior, restrictions, and examples.
