# Update Roadmap

The day-to-day maintenance entry point once a roadmap is in place: change status, shift dates and compute the downstream impact, and produce a "what changed this time" summary. It does not change which tier an item sits in.

## Purpose

`define-roadmap` builds a roadmap from nothing and `promote-roadmap-items` handles promotion and demotion across tiers; between the two sits a large body of day-to-day movement — an item has started, an item is stuck, an item slips by two weeks — and this skill owns that part. Moving an item to "at risk" or "blocked" writes nothing unless both the blocking reason and the mitigation are given; a date shift must compute the downstream impact and flag the items that cross a hard deadline.

## When to use

- **Progress sync**: an item started or finished and the status has to catch up
- **Risk escalation**: an item is stuck, and the blocking reason and the mitigation need to be recorded
- **Date adjustment**: a dependency slipped or the scope changed, so the item moves later and the blast radius has to be visible
- **Before communicating a change**: a "what changed this time" write-up is needed to bring stakeholders up to date

## Inputs

- `docs/process-management/roadmap.md` and the frontmatter of the items involved
- The intended change (status change / date shift)
- Optional: the blocking details

## Outputs

- `roadmap.md` and the item frontmatter updated together (never one side alone)
- A downstream impact list plus the items that cross a hard deadline
- A summary of this change (what changed / why / blast radius)

## Boundary with promote-roadmap-items

**Anything that changes the tier belongs to promote; anything that does not belongs here.** Pushing a Now item back by two weeks is this skill; moving it into Next is promote. The test is whether the tier changed, not whether the date changed.

## Install

Handled centrally by the canonical AI Cortex install; see the repository root [README](../../README.md#-install-and-use).

## Related skills

- `promote-roadmap-items` — adjacent boundary: cross-tier adjustments hand off to it
- `map-item-dependencies` — upstream: supplies `depends_on` for the downstream impact calculation
- `review-roadmap` — signal source: the status problems a health check turns up are handled here
- `define-roadmap` — adjacent boundary: structural changes (milestones / capacity) belong to it

## Full definition

See [SKILL.md](./SKILL.md).
