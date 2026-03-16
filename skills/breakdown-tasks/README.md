# breakdown-tasks

Turn a validated design document into an executable task list with dependencies, acceptance criteria, and assignee or AI execution hints.

## Overview

This skill consumes the output of `design-solution` (or `brainstorm-design`) and produces a tasks document (e.g. tasks.md) so that implementation can proceed in order with clear "done" criteria and ownership. It is the third step in the execution chain: **analyze-requirements → design-solution → breakdown-tasks**.

## Key features

- **Design as input**: Reads design.md or docs/design-decisions/*.md
- **Ordered tasks**: Each task has dependencies; list is acyclic
- **Acceptance criteria**: Per-task "done" definition
- **Owner or hint**: Assignee (person/role) or AI execution hint per task
- **Traceability**: Tasks map back to design sections

## When to use

- After design is approved and you need an implementation plan
- When you want every design decision to map to concrete tasks
- When you want AI-executable hints (e.g. which skill or file to touch) per task

## Related skills

- `design-solution`: Produces the design document this skill consumes
- `analyze-requirements`: Produces requirements that feed design; not direct input to breakdown-tasks
- `align-planning`: Re-aligns execution with goals/milestones; can consume task state

## Installation

```bash
npx skills add nesnilnehc/ai-cortex --skill breakdown-tasks
```

## License

MIT
