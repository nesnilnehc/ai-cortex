---
name: breakdown-tasks
description: Break a design document into an executable task list with dependencies, acceptance criteria, and assignee or AI execution hints. Use when design is approved and you need an implementation plan.
tags: [writing, documentation, workflow]
version: 1.1.0
license: MIT
recommended_scope: both
metadata:
  author: ai-cortex
triggers: [breakdown tasks, task breakdown, implementation plan, tasks from design]
input_schema:
  type: document-artifact + optional free-form
  description: Design document (e.g. design.md or docs/design-decisions/YYYY-MM-DD-<topic>.md); optional scope or priority hints
output_schema:
  type: document-artifact
  description: Task list document with ordered tasks, dependencies, acceptance criteria, and assignee/execution hints
  path_pattern: docs/process-management/tasks/YYYY-MM-DD-{topic}.md (or project-convention tasks.md)
  lifecycle: living
---

# Skill: Breakdown Tasks

## Purpose

Turn a validated design document into an ordered, trackable task list. Each task has dependencies, acceptance criteria, and an assignee (or AI execution hint) so that implementation can proceed without ambiguity.

---

## Core Objective

**Primary Goal**: Produce a tasks document (e.g. tasks.md) from a design document so that every implementable unit is one task with clear dependencies, acceptance criteria, and ownership.

**Success Criteria** (ALL must be met):

1. ✅ **Tasks document exists**: Written to agreed path (e.g. `docs/process-management/tasks/YYYY-MM-DD-<topic>.md` or project `tasks.md`) and committed
2. ✅ **Design traceability**: Each task maps to at least one part of the design (section or acceptance criterion)
3. ✅ **Dependencies explicit**: Task order or dependency list is clear (no circular dependencies)
4. ✅ **Acceptance criteria per task**: Each task has concrete "done" criteria
5. ✅ **Assignee or execution hint**: Each task has owner (person/role) or AI execution hint (e.g. which skill or step to run)
6. ✅ **User confirmed**: User explicitly approved or adjusted the task list

**Acceptance Test**: Can an executor (human or Agent) pick the next task, implement it, and verify completion using only this document and the design?

---

## Scope Boundaries

**This skill handles**:

- Design document → Ordered task list (tasks.md or equivalent)
- Dependencies between tasks; acceptance criteria per task; assignee or AI execution hints
- Persisting the task list as a living artifact for implementation tracking

**This skill does NOT handle**:

- Creating or validating the design (use `design-solution` or `brainstorm-design`)
- Validating requirements (use `analyze-requirements`)
- Executing tasks (implementation skills, run-repair-loop, etc.)
- Scheduling or capacity planning (use project/milestone tools)

**Handoff point**: When the task list is approved and persisted, hand off to implementation (e.g. run tasks in order, or feed into backlog/board).

---

## Use Cases

- **Post-design planning**: Design is approved; you need a clear implementation plan before coding.
- **Traceability**: You want every design decision to map to one or more concrete tasks.
- **AI-assisted execution**: You want each task to include hints (e.g. "use skill X" or "edit file Y") so an Agent can execute the plan.

---

## Behavior

### Interaction Policy

- **Defaults**: Require a design document (path or content); use project norms for output path if present
- **Choice options**: When design is ambiguous, ask one clarifying question at a time
- **Confirm**: User must approve or adjust the task list before handoff

### Phase 1: Ingest Design

1. **Load design**: Read the design document (e.g. design.md or docs/design-decisions/*.md).
2. **Extract structure**: Identify sections that imply work (architecture, components, data flow, error handling, testing, etc.).
3. **Confirm scope**: If user specified a subset (e.g. "only backend"), restrict tasks to that subset.

### Phase 2: Derive Tasks

1. **One task per implementable unit**: Each task should be completable in a single focus session; avoid vague "implement X" where X is large.
2. **Order by dependency**: List tasks so that dependencies come first; document dependency explicitly (e.g. "Depends on: T1, T2").
3. **Acceptance criteria**: For each task, state what "done" looks like (testable or verifiable).
4. **Assignee or hint**: For each task, set assignee (person/role) or an AI execution hint (e.g. "Run design-solution for module Y", "Edit src/foo.ts per design §3").

### Phase 3: Persist and Hand Off

1. **Resolve path**: Prefer project norms (e.g. docs/ARTIFACT_NORMS.md); else `docs/process-management/tasks/YYYY-MM-DD-<topic>.md` or project-convention `tasks.md`.
2. **Write tasks document**: Use a consistent format (see below); include front-matter if project uses it (`created_by: breakdown-tasks`, `lifecycle: living`, design source path).
3. **User approval**: Present summary and ask for approval or edits.
4. **Handoff**: Suggest starting implementation from the first unblocked task.

---

## Input & Output

| Role | Content |
| :--- | :--- |
| **Input** | Design document (path or content); optional scope/priority from user |
| **Output** | Tasks document at `docs/process-management/tasks/YYYY-MM-DD-<topic>.md` or project `tasks.md`; each task has id, title, dependencies, acceptance criteria, assignee/hint |

---

## Recommended Task List Format

```markdown
# Implementation tasks: [Topic]

**Source design:** [path or title]
**Created:** YYYY-MM-DD

| Id | Task | Depends on | Acceptance criteria | Owner / Hint |
|----|------|------------|----------------------|--------------|
| T1 | ...  | —          | ...                  | ...         |
| T2 | ...  | T1         | ...                  | ...         |
```

Optional: Add a short "Summary" and "Design traceability" (task → design section) at the top.

---

## Restrictions

### Hard Boundaries

- **Design first**: Do not run when design is missing or unapproved; hand off to `design-solution` or `brainstorm-design`.
- **No implementation**: Do not write code or run implementation skills; only produce the task list.
- **No circular dependencies**: Task order must be acyclic.

### Skill Boundaries (Avoid Overlap)

**Do NOT do these (other skills handle them)**:

- Requirements analysis or validation → `analyze-requirements`
- Design exploration or approval → `design-solution`
- Execution of tasks or repair loops → implementation skills or `run-repair-loop`

---

## Self-Check

- [ ] Tasks document exists and is committed
- [ ] Every task has dependencies (or "—"), acceptance criteria, and owner/hint
- [ ] Design sections are traceable to at least one task
- [ ] No circular dependencies
- [ ] User approved or explicitly accepted the task list

---

## Examples

### Example 1: Standard design-to-tasks flow

**Invocation**: "We have design in docs/design-decisions/2026-03-16-core-v1.md. Break it down into tasks."

**Agent**: Uses breakdown-tasks; reads design; derives ordered tasks with deps and acceptance criteria; writes docs/process-management/tasks/2026-03-16-core-v1.md; gets user approval; suggests starting with first task.

### Example 2: Edge case — oversized design

**Invocation**: "Our design doc for the platform is huge (multiple subsystems). We only want tasks for 'auth + user onboarding' right now."

**Agent**:

- Asks the user to confirm the intended scope subset (e.g. sections 3 and 4 of the design).
- Limits task derivation to that subset and clearly notes the scoped source sections in the tasks document.
- Ensures dependencies outside scope are either stubbed as external prerequisites or captured as explicit blockers.
- Produces a tasks file whose first column links each task back to the specific design sections used, so future runs can extend coverage without duplication.
