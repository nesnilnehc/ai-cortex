# Review Tasks

**Status**: Experimental

## Purpose

Evaluates an existing task list against [task-modeling](../../specs/task-modeling.md) and the canonical [task quality Rules](../../rules/task-quality.md). It checks that every task is independently executable, dependency-safe, bounded, traceable back to the design it came from, and explicit about which engineering checks apply to it. It does not schedule work, assign people or implement anything.

## When to use

- Pre-coding gate: tasks are broken out and about to be assigned.
- Design coverage check: confirm no component of the technical design is left without a task.
- Dependency safety: confirm the dependency graph is acyclic and no task depends on an identifier that does not exist.

## Inputs

- A task-list document (a path, or the raw content).
- Optional upstream technical design used to check coverage and traceability.

## Outputs

- Findings list: location (a task ID or a section heading), category=`task-quality`, severity, title, description, optional suggestion.
- Zero findings → confirmation that the list is ready for assignment.

## Ecosystem

| Field | Value |
| :------------------------------------ | :---------------------------------------------------------------------------------------- |
| overlaps_with (owner/repo:skill-name) | nesnilnehc/ai-cortex:review-technical-design, nesnilnehc/ai-cortex:map-item-dependencies |
| market_position | differentiated |

## Full definition

See [SKILL.md](./SKILL.md) for execution and boundaries; the criteria live only in [task-quality.md](../../rules/task-quality.md).
