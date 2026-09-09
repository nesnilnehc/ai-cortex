---
artifact_type: rule
name: task-quality
version: 1.0.0
scope: reviewing or self-checking a task list document
recommended_scope: user
status: active
---

# Rule: Task Quality

> Review checklist for a task list, plus spec compliance. Every item is independently verifiable.
>
> Applies to task list documents that declare conformance to [specs/task-modeling.md](../specs/task-modeling.md).

---

## Review checklist

### 1. Field completeness

- [ ] Every task carries the 6 required fields (id / title / depends_on / acceptance / owner_or_hint / status)
- [ ] Every task starts at status `Todo`
- [ ] Frontmatter is complete (artifact_type / lifecycle / created_at / parent)

### 2. Dependency graph correctness

- [ ] The dependency graph is acyclic (DAG)
- [ ] A task with no dependencies has `—` in `depends_on`, never a blank
- [ ] Cross-document dependencies carry a path prefix (for example `other-tasks.md#T3`)
- [ ] No task depends on an ID that does not exist

### 3. Executability

- [ ] Each task is concrete enough to finish in one focused session
- [ ] Each task has an assignee or an AI execution hint
- [ ] Task titles contain a verb; avoid the vague "implement X"
- [ ] Acceptance criteria are testable or otherwise verifiable

### 4. Traceability

- [ ] Frontmatter `parent` points at the upstream design
- [ ] Each task traces back to a section or an acceptance criterion of that design
- [ ] Every component in the design is covered by at least 1 task — no orphaned components

---

## Spec compliance (specs/task-modeling.md)

- [ ] Frontmatter `artifact_type: tasks`
- [ ] Frontmatter `lifecycle: living`
- [ ] Every task ID matches `T<n>` and is unique
- [ ] Every task status is within the enum
- [ ] All statuses are `Todo` at hand-off

---

## Anti-patterns

- ❌ Circular dependencies
- ❌ Vague tasks ("implement module X")
- ❌ No acceptance criteria
- ❌ A status other than Todo written at hand-off
- ❌ No `parent` frontmatter — an orphaned task list
- ❌ A task with no reference to the design
