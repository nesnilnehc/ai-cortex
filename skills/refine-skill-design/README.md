# Refine Skill Design

**Status**: Validated

## Purpose

Reviews and refactors an existing skill. Applies a meta-audit model: intent, logic, constraints, examples. Brings the skill into spec compliance and improves its robustness and scenario coverage. For drafts and quality fixes; not for creating a new skill from scratch.

## When to use

- New skill onboarding: expert review after a draft is generated
- Quality fix: adjust the logic when the behaviour is inconsistent
- Consistency review: match the tags and naming in INDEX.md
- Upgrade: turn plain formatting into a full agent capability

## Inputs

- A SKILL Markdown document or draft

## Outputs

- A refined SKILL (written to a fixed temporary "SKILL.refined.md", or to a new "SKILL.refined.YYYYMMDD.md" per run; the original file is never overwritten)
- A diff summary (what changed and why)
- A version suggestion (SemVer)

## Ecosystem

| Field | Value |
| :------------------------------------ | :------------------------------------------------------------------------------------ |
| overlaps_with (owner/repo:skill-name) | — |
| market_position | differentiated |

## Full definition

See [SKILL.md](./SKILL.md) for the full behaviour, the limits, and the examples.
