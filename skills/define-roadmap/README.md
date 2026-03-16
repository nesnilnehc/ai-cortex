# define-roadmap

Translate strategic goals and milestones into a time-bound roadmap of initiatives or themes.

## What it does

Produces a roadmap document that maps goals and milestones to initiatives or themes with optional timeframes. Does not define goals, milestones, or backlog. Output is persisted to `docs/process-management/roadmap.md` (or project norms).

## When to use

- After milestones — build a visible plan that connects strategy to release or sprint planning.
- Planning cycle — establish initiative/theme sequence for the next 1–2 periods.
- Before backlog — provide roadmap so backlog items can be grouped under initiatives.
- Strategy-to-execution bridge — run after goals and milestones in the full hierarchy.

## Inputs

- Strategic goals and milestones (documents or paths); project context.
- Optional: initiatives document; time horizon; existing roadmap.

## Outputs

- Roadmap document at `docs/process-management/roadmap.md` (or project norms): initiatives/themes with traceability to milestones and goals.

## Installation

```bash
npx skills add nesnilnehc/ai-cortex --skill define-roadmap
```

## Related skills

- `design-strategic-goals`, `define-milestones` — upstream: roadmap derives from these.
- `define-strategic-pillars` — optional input: pillars can guide roadmap themes.

## Full definition

See [SKILL.md](./SKILL.md) for behavior, restrictions, and examples.
