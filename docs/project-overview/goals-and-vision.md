# Goals and Vision

## Project Overview

**Project Name:** AI Cortex
**Project Code:** ai-cortex
**Project Type:** Capability Asset Library
**Target Users:** AI Agent developers, IDE users, teams adopting agent-first workflows

## Problem Statement

**Current Pain Points:**

- Skill definitions are scattered and inconsistent; no single spec for structure, metadata, or quality.
- Agents lack discoverable, machine-readable capability catalogs for task routing.
- Governance (ASQM, lifecycle, overlap detection) is manual and ad hoc.

**Opportunity Space:**

- LLM Agents need composable, spec-driven capability definitions.
- skills.sh, SkillsMP, and Claude Plugin adoption creates demand for standardized skill assets.

## Vision

**Vision Statement:**

Become the agent-first, governance-ready inventory of Skills where Specs turn capabilities into reusable, composable engineering assets.

**Success Criteria:**

- Canonical skill catalog discoverable via INDEX.md, manifest.json, scenario-map.
- ASQM scoring and lifecycle status enable quality-aware routing.
- Skills integrate with skills.sh, SkillsMP, Claude Plugin.

## Goals

### Business Goals

| Goal | Metric | Target | Timeline |
| :--- | :--- | :--- | :--- |
| Skill catalog growth | Skills count | 36+ skills | Ongoing |
| Spec adoption | Skills conforming to spec | 100% | Per release |
| Distribution | Channels | skills.sh, SkillsMP, Plugin | Maintained |

### User Goals

- **Agent developers:** Core need — discover and load skills by task semantics. Expected value — reduced prompt engineering, consistent contracts.
- **IDE users:** Core need — install rules and skills into Cursor/Trae. Expected value — AI behavior aligned with project standards.

### Technical Goals

- Contract-first: Structure, metadata, quality defined under spec/.
- Verifiable: Self-Check as minimum delivery guarantee.
- Composable: related_skills supports reuse and orchestration.
- Discoverable: INDEX.md, manifest.json, scenario-map as stable entry points.

## Value Proposition

**Value to Users:**

Skills are one-file, self-contained; Agents load SKILL.md for full definition. Scenario-map enables task-based discovery.

**Value to Ecosystem:**

Spec and ASQM provide shared quality bar; curate-skills maintains consistency across inventory.

**Competitive Advantage:**

- Single spec (skill.md) for structure; ASQM for quality and lifecycle.
- Scenario-to-skill mapping for governance workflows.

## Scope

### In Scope

- Skill definitions under skills/
- Spec (spec/skill.md)
- Registry (INDEX.md, manifest.json)
- Rules for AI behavior (rules/)
- AGENTS.md entry contract

### Out of Scope

- IDE/Agent/CI integration or install scripts
- Model invocation or runtime orchestration
- Vendor-specific adapters

## Key Assumptions

- Markdown-based skill definitions suffice for injection.
- ASQM dimensions (agent_native, cognitive, composability, stance) capture quality.
- Solo or small-team maintenance; governance scales with automation.

## Version History

| Version | Date | Changes | Author |
| :--- | :--- | :--- | :--- |
| 1.0 | 2026-03-06 | Initial goals-and-vision; formalize goal layer per documentation-readiness | ai-cortex |
