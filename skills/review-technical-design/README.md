# Review Technical Design

**Status**: Experimental

## Purpose

Evaluates an existing technical design against [technical-design-modeling](../../specs/technical-design-modeling.md), the canonical [technical design quality Rules](../../rules/technical-design-quality.md) and the engineering Rule IDs the design claims to satisfy. It answers one question: can tasks be derived from this without architectural ambiguity, and do the applicable architecture, security, performance, observability, reliability and testing concerns have explicit tactics and verification?

## When to use

- Pre-task gate: the technical design is drafted and tasks are about to be broken out.
- Profile check: the project activates engineering Rule profiles and the design must show a tactic and a verification for each.
- Collaborative review: an independent assessment before the design is approved.

## Inputs

- A technical-design document (a path, or the raw content).
- Optional project configuration supplying active profiles, topology and quality targets.

## Outputs

- Findings list: location (a section heading), category=`technical-design-quality`, severity, title, description, optional suggestion.
- Zero findings → confirmation that a task list can be derived without a clarifying question.

## Ecosystem

| Field | Value |
| :------------------------------------ | :------------------------------------------------------------------------------- |
| overlaps_with (owner/repo:skill-name) | nesnilnehc/ai-cortex:review-functional-design, nesnilnehc/ai-cortex:review-tasks |
| market_position | differentiated |

## Full definition

See [SKILL.md](./SKILL.md) for execution and boundaries; the criteria live only in [technical-design-quality.md](../../rules/technical-design-quality.md).
