# Map Item Dependencies

Identifies the dependencies among backlog and roadmap items, writes them into each item's `depends_on`, and produces a dependency graph and a blocked list. Runs before promotion, so blocked items do not get pulled into Now.

## Purpose

Walks the dependencies between items in five categories (technical / team / external / knowledge / sequencing), records "needed by when" and who owns it, gives reduction options for the high-risk ones, and emits a blocked list that `promote-roadmap-items` can consume directly. Dependencies are the highest-risk factor on a roadmap — they appear neither in the priority nor in the capacity, yet they leave a high-priority item stuck in place once it enters Now.

## When to use

- **Before promotion**: run it first once there are ≥ 2 candidate items, so no blocked item gets pulled into Now
- **Schedule review**: you need to see which items must run in series and which can run in parallel
- **Post-mortem on a stall**: a Now-tier item has not moved in a long while, so check for an unrecorded prerequisite

## Inputs

- Backlog items (in any priority state)
- `docs/process-management/roadmap.md`
- Optional: a scope restriction (defaults to the current promotion candidates)

## Outputs

- An in-conversation dependency graph + a need-by table + reduction options
- A blocked list (which items cannot enter Now as things stand)
- The `depends_on` field in each item's frontmatter is updated

## Install

Handled centrally by the canonical AI Cortex install; see the repository root [README](../../README.md#-install-and-use).

## Related skills

- `promote-roadmap-items` — downstream: the Now-tier admission guardrail consumes the `depends_on` this skill produces
- `prioritize-backlog` — upstream: supplies the scored candidate items
- `update-roadmap` — consumer: reads `depends_on` when shifting dates, to work out the downstream impact
- `orchestrate-roadmap-planning` — orchestrator: this is step 5, the one before promotion

## Full definition

See [SKILL.md](./SKILL.md).
