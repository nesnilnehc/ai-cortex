---
artifact_type: north-star
created_by: define-north-star
lifecycle: living
created_at: 2026-03-24
status: active
---

# North Star

## The North Star metric

**Monthly skill usage** — invocation or use events for the skills in this catalogue.

- **Definition**: the number of distinct invocation or use events referencing a skill in this catalogue — an agent or a user triggers a skill and it produces something deliverable, such as a review output or a design document — counted per calendar month.
- **Why it stands for user value**: the mission is focused on software delivery and project governance, and the vision is to help teams reach semi-automated delivery and governance on this catalogue. Value is delivered when a capability is used — a skill invoked in context, an output obtained — so usage shows that a team is folding these capabilities into its semi-automated delivery and governance chains. It is a behavioural metric, not a vanity one such as stars or clones.

## Derivation, from mission and vision

1. **Mission**: provide the agent skills used throughout software delivery and project governance, supporting both the delivery chain and the governance chain.
2. **Vision**: help teams reach semi-automated delivery and governance on this catalogue, invoking capabilities by situation and collaborating per the specs across both chains.
3. **Users**: teams working in the delivery and governance chains, who need semi-automated capabilities to raise both efficiency and predictability.
4. **Core value**: at every step of delivery and governance a team can invoke a capability suited to the situation, making the work semi-automated and collaboration predictable.
5. **Primary behaviour**: using a capability — triggering a skill in context and obtaining something deliverable.
6. **Observable behaviour**: a skill invocation or use event.
7. **Measurable metric**: monthly skill usage.

## Principles

1. It reflects user value; 2. it stands for user behaviour; 3. it measures sustained engagement; 4. it is product-driven; 5. it is simple and clear.

## Supporting metrics (optional)

The number of skills in the catalogue, the Spec compliance rate, intent coverage, channel presence. Install count can serve as a proxy observation while usage is out of reach, but it is not the North Star.

## Measurement and its limits

**Out of reach in the short and medium term**. Today's ecosystem — skills.sh, Cursor, Claude and the like — exposes no usage telemetry to a skill's author. If an API or data source appears later, measurement can start then; until it does, there is no direct way to observe this.

## Anti North Star

GitHub stars, clones and forks, total unique visitors — vanity or one-off, and none of them reflects use or value.
