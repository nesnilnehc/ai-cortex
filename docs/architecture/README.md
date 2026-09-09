---
artifact_type: architecture
created_by: ai-cortex
lifecycle: living
created_at: 2026-03-24
status: active
---

# Architecture

AI Cortex is an asset library for agents, organised into four governance layers: Spec / Protocol / Skill / Rule.

## Canonical sources

- [terminology.md](terminology.md) — the industry definitions of the 4 asset types, what each owns exclusively, and how to tell them apart
- [asset-naming.md](asset-naming.md) — the naming convention for the 4 asset types
- [skills/INDEX.md](../../skills/INDEX.md) — the skill catalogue
- [agentskills.io](https://agentskills.io) — the standard Skill format, the external authority

## ADR

Past architecture decisions are under [adrs/](../adr/).

## When to add an ADR

Add an ADR (`adrs/NNN-{slug}.md`) in these situations:

- A significant design decision whose rationale has to be stated explicitly
- An approved architectural choice worth keeping on record (the field contracts for design documents are in [specs/functional-design-modeling.md](../../specs/functional-design-modeling.md) and [specs/technical-design-modeling.md](../../specs/technical-design-modeling.md))
- A dependency across skills or across phases that has to be documented
