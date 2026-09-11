# Review Functional Design

**Status**: Experimental

## Purpose

Evaluates an existing functional design against [functional-design-modeling](../../specs/functional-design-modeling.md) and the canonical [functional design quality Rules](../../rules/functional-design-quality.md). It is the pre-coding business-behaviour gate: business modules, workflows, states, permissions, exceptions and acceptance criteria must be complete and traceable enough for a technical design to be derived. It does not author the design and makes no technical choice.

## When to use

- Pre-technical-design gate: the user-visible behaviour is drafted and must be checked before engineering design starts.
- Collaborative review: one party drafts the functional design, a second assesses it independently.
- Imported designs: business behaviour arrives from an external tool and needs a quality assessment before it enters this workflow.

## Inputs

- A functional-design document (a path, or the raw content).
- Optional references to the upstream requirement the design claims to cover.

## Outputs

- Findings list: location (a section heading or a workflow step), category=`functional-design-quality`, severity, title, description, optional suggestion.
- Zero findings → confirmation that technical design can be derived without a clarifying question.

## Ecosystem

| Field | Value |
| :------------------------------------ | :------------------------------------------------------------------------------ |
| overlaps_with (owner/repo:skill-name) | nesnilnehc/ai-cortex:review-requirements, nesnilnehc/ai-cortex:review-technical-design |
| market_position | differentiated |

## Full definition

See [SKILL.md](./SKILL.md) for execution and boundaries; the criteria live only in [functional-design-quality.md](../../rules/functional-design-quality.md).
