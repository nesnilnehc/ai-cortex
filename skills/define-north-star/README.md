# define-north-star

Define the single most important metric representing the core value delivered to users (North Star Metric).

## What it does

Derives and documents one North Star Metric (NSM) using the chain: User → Core Value → Primary Action → Observable Behavior → Measurable Metric. Ensures the metric reflects user value, behavior, and ongoing engagement (not vanity). Output includes NSM, rationale, optional 3–5 supporting metrics, and anti–North-Star examples. Persisted to `docs/project-overview/north-star.md` (or project norms).

## When to use

- After vision — establish the one metric that captures "value delivered".
- Product prioritization — single metric to guide what to optimize for.
- Replacing vanity metrics — when focus is on revenue/total users/downloads and you want a user-value anchor.
- Third layer in strategy chain — run after mission and vision.

## Inputs

- Project/product description; target users; core value proposition (or mission/vision).
- Optional: current metrics, constraints, comparable product examples.

## Outputs

- North Star document at `docs/project-overview/north-star.md` (or project norms): NSM + rationale, optional supporting metrics, anti-examples.

## Installation

```bash
npx skills add nesnilnehc/ai-cortex --skill define-north-star
```

## Related skills

- `define-mission` — why we exist.
- `define-vision` — what future we build.
- `design-strategic-goals` — next: 3–5 outcomes that move the NSM.
- `define-milestones` — phase checkpoints from goals.
- `align-planning` — can use north-star doc as top anchor for alignment.

## Full definition

See [SKILL.md](./SKILL.md) for behavior, restrictions, derivation framework, and examples.
