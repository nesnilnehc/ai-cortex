---
artifact_type: rule
name: task-quality
version: 2.0.0
model: RULE_MODEL_V1
rule_prefix: TASK
scope: task list documents conforming to specs/task-modeling.md
recommended_scope: project
status: active
created_by: ai-cortex
lifecycle: living
created_at: 2026-05-09
---

# Rule: Task Quality

## Scope

Applies to a task list document before its tasks are assigned or executed. It decides whether the list is executable, dependency-safe, traceable to its design and explicit about the engineering obligations its tasks carry.

It does not review the upstream design, schedule or staff the work, execute a task, or review the code a task later produces. Those belong to the design reviewers, to planning, and to the post-coding gates.

## Profiles and parameters

| Name | Kind | Provenance | Meaning |
|---|---|---|---|
| `handoff` | profile | — | The list is being handed to execution rather than still drafted |
| `engineering-governance` | profile | — | A task implements a quality-attribute tactic, crosses a declared boundary, adds fallible I/O, concurrency, background work or telemetry, or is subject to a quality budget or waiver |
| `tasks.session_budget` | parameter | declared | What the project counts as one focused working session |

Provenance follows [rule-modeling](../specs/rule-modeling.md) §5.4: a project writes only the `declared` values.

## Rules

### TASK-001 — Every task row carries its required fields

| Field | Value |
|---|---|
| Level | `baseline` |
| Requirement | Every task row **MUST** carry an id, title, dependency list, acceptance, owner or execution hint, and a status drawn from the modeled enum. |
| Applies when | The document contains one or more task rows. |
| Default severity | `major` |
| Enforcement | `automated` |
| Evidence | The task table and the field contract in [task-modeling](../specs/task-modeling.md). |
| Pass condition | No row omits a required field, and every status value is inside the enum. |
| Not applicable when | The document declares no task rows yet. |
| Remediation | Fill the missing field, or remove a row that is not yet a task. |

### TASK-002 — A handed-off list carries no started work

| Field | Value |
|---|---|
| Level | `profile:handoff` |
| Requirement | Every task **MUST** be at its initial status when the list is handed off for execution. |
| Applies when | The list is presented as ready for assignment or execution. |
| Default severity | `major` |
| Enforcement | `automated` |
| Evidence | The status column and the hand-off statement or review request. |
| Pass condition | No task carries a status beyond the initial one at hand-off. |
| Not applicable when | The list is an in-progress execution record rather than a hand-off. |
| Remediation | Reset the status, or state explicitly that this is a progress record and not a hand-off. |

### TASK-003 — The document declares its required frontmatter

| Field | Value |
|---|---|
| Level | `baseline` |
| Requirement | The document **MUST** declare the artifact type, lifecycle, creation date and parent required by its modeling Spec. |
| Applies when | always |
| Default severity | `minor` |
| Enforcement | `automated` |
| Evidence | Document frontmatter against [task-modeling](../specs/task-modeling.md). |
| Pass condition | Every required field is present and inside its enum. |
| Not applicable when | never |
| Remediation | Add the missing frontmatter field. |

### TASK-004 — The dependency graph is acyclic

| Field | Value |
|---|---|
| Level | `baseline` |
| Requirement | Task dependencies **MUST NOT** form a cycle. |
| Applies when | Two or more tasks declare dependencies. |
| Default severity | `major` |
| Enforcement | `automated` |
| Evidence | The dependency column resolved into a directed graph. |
| Pass condition | Every strongly connected component contains exactly one task. |
| Not applicable when | No task declares a dependency. |
| Remediation | Break the cycle by splitting a task or inverting one dependency. |

### TASK-005 — Every dependency reference resolves

| Field | Value |
|---|---|
| Level | `baseline` |
| Requirement | Every declared dependency **MUST** resolve to an existing task, and a dependency outside this document **MUST** carry its document path. |
| Applies when | A task declares at least one dependency. |
| Default severity | `major` |
| Enforcement | `automated` |
| Evidence | Dependency values, the local id set and any referenced task documents. |
| Pass condition | Every reference resolves to a real task, and no cross-document reference is written as a bare id. |
| Not applicable when | No task declares a dependency. |
| Remediation | Correct the id, or add the document path to the cross-document reference. |

### TASK-006 — An absent dependency is recorded explicitly

| Field | Value |
|---|---|
| Level | `baseline` |
| Requirement | A task with no dependency **MUST** record that explicitly rather than leaving the field blank. |
| Applies when | A task has no prerequisite. |
| Default severity | `minor` |
| Enforcement | `automated` |
| Evidence | The dependency column. |
| Pass condition | No dependency cell is empty; "none" is written with the modeled placeholder. |
| Not applicable when | Every task declares at least one dependency. |
| Remediation | Write the explicit placeholder so an unfilled cell cannot be mistaken for an omission. |

### TASK-007 — A task is bounded to one working session

| Field | Value |
|---|---|
| Level | `baseline` |
| Requirement | Each task **MUST** be small enough to be completed and verified within one focused working session. |
| Applies when | The document contains one or more task rows. |
| Default severity | `minor` |
| Enforcement | `judgment` |
| Evidence | Task scope, the number of distinct deliverables it names, and `tasks.session_budget` where the project declares one. |
| Pass condition | No task bundles deliverables that would have to be verified and handed over separately. |
| Not applicable when | The row is an explicitly labelled epic that decomposes into listed child tasks. |
| Remediation | Split the task along its deliverable boundaries. |

### TASK-008 — Every task names an owner or an execution hint

| Field | Value |
|---|---|
| Level | `baseline` |
| Requirement | Every task **MUST** name a human owner or an explicit execution hint. |
| Applies when | The document contains one or more task rows. |
| Default severity | `minor` |
| Enforcement | `automated` |
| Evidence | The owner or hint column. |
| Pass condition | No task leaves both empty. |
| Not applicable when | never |
| Remediation | Assign an owner, or state how the task is to be executed. |

### TASK-009 — A task title states its concrete action

| Field | Value |
|---|---|
| Level | `baseline` |
| Requirement | A task title **MUST** name the action to be performed and its object, not a module name alone. |
| Applies when | The document contains one or more task rows. |
| Default severity | `minor` |
| Enforcement | `judgment` |
| Evidence | Task titles read against the design elements they claim to deliver. |
| Pass condition | Each title tells a reader what will be different afterwards without opening the design. |
| Not applicable when | never |
| Remediation | Rewrite the title with a verb and the specific object it acts on. |

### TASK-010 — Task acceptance is verifiable

| Field | Value |
|---|---|
| Level | `baseline` |
| Requirement | Every task's acceptance **MUST** be decidable by a test, a command, an inspection or a named artifact. |
| Applies when | The document contains one or more task rows. |
| Default severity | `major` |
| Enforcement | `judgment` |
| Evidence | The acceptance column and the verification means it names. |
| Pass condition | Each acceptance statement can be decided without asking its author what was meant. |
| Not applicable when | never |
| Remediation | Replace a vague acceptance statement with the observable outcome that decides it. |

### TASK-011 — The list declares its upstream design

| Field | Value |
|---|---|
| Level | `baseline` |
| Requirement | The document **MUST** name the upstream design it derives from. |
| Applies when | always |
| Default severity | `major` |
| Enforcement | `automated` |
| Evidence | The parent field and the referenced document. |
| Pass condition | The parent resolves to an existing upstream artifact. |
| Not applicable when | never |
| Remediation | Add the parent reference, or create the missing upstream artifact before deriving tasks. |

### TASK-012 — Every task traces to a design element

| Field | Value |
|---|---|
| Level | `baseline` |
| Requirement | Every task **MUST** trace to a section or an acceptance item of the upstream design. |
| Applies when | An upstream design exists. |
| Default severity | `major` |
| Enforcement | `tool-assisted` |
| Evidence | Task-to-design mapping and the upstream document's headings and acceptance items. |
| Pass condition | No task exists that the upstream design does not call for. |
| Not applicable when | The list is authorized directly by an approved decision record that names the work. |
| Remediation | Add the design reference, or return the untraced work upstream for approval. |

### TASK-013 — Every design component has a task

| Field | Value |
|---|---|
| Level | `baseline` |
| Requirement | Every component and acceptance item in the upstream design's scope **MUST** be covered by at least one task. |
| Applies when | An upstream design exists and is in scope for this list. |
| Default severity | `major` |
| Enforcement | `judgment` |
| Evidence | Design components and acceptance items mapped against the task set. |
| Pass condition | No in-scope design element is left without a task, or its deferral is stated in the list. |
| Not applicable when | The list deliberately covers one phase and names the phases it excludes. |
| Remediation | Add the missing task, or record the deferral and its reason in the list. |

### TASK-014 — A quality-sensitive task carries its governance annotation

| Field | Value |
|---|---|
| Level | `profile:engineering-governance` |
| Requirement | A task meeting an engineering-governance trigger **MUST** carry the complete annotation its modeling Spec defines. |
| Applies when | A task implements a quality-attribute tactic, crosses a declared boundary, adds fallible I/O, concurrency, background work or telemetry, or is subject to a quality budget or waiver. |
| Default severity | `major` |
| Enforcement | `tool-assisted` |
| Evidence | Task descriptions, the annotation table and the trigger conditions in [task-modeling](../specs/task-modeling.md). |
| Pass condition | Every triggered task carries all annotation fields, and no triggered task is missing from the table. |
| Not applicable when | No task in the list meets a trigger. |
| Remediation | Add the annotation, or show that the task meets no trigger. |

### TASK-015 — Affected scope is named exactly

| Field | Value |
|---|---|
| Level | `profile:engineering-governance` |
| Requirement | An annotated task **MUST** name the exact modules, contracts, data stores or operational paths it affects. |
| Applies when | A task carries an engineering-governance annotation. |
| Default severity | `major` |
| Enforcement | `judgment` |
| Evidence | The affected-scope field read against the project's declared modules and contracts. |
| Pass condition | A reader can locate every named element; no entry is a category such as "backend" or "various". |
| Not applicable when | No annotated task exists. |
| Remediation | Replace the category with the specific elements the task touches. |

### TASK-016 — Cited engineering Rule references resolve

| Field | Value |
|---|---|
| Level | `profile:engineering-governance` |
| Requirement | Every engineering Rule reference on a task **MUST** resolve to an active canonical Rule item, and the task **MUST NOT** restate that Rule's text. |
| Applies when | A task cites one or more engineering Rule ids. |
| Default severity | `major` |
| Enforcement | `automated` |
| Evidence | The cited ids resolved against the active canonical Rule sets. |
| Pass condition | Every id resolves to an active item, and no Rule prose is copied into the task. |
| Not applicable when | No task cites an engineering Rule. |
| Remediation | Correct the id, or cite the item that actually governs the work. |

### TASK-017 — Verification can decide the cited Rule items

| Field | Value |
|---|---|
| Level | `profile:engineering-governance` |
| Requirement | An annotated task's verification **MUST** name a test, tool command, review or evidence artifact capable of deciding every Rule item it cites. |
| Applies when | A task carries an engineering-governance annotation. |
| Default severity | `major` |
| Enforcement | `judgment` |
| Evidence | The verification field read against each cited item's own pass condition. |
| Pass condition | Each cited item has a named means of verification that could actually decide it. |
| Not applicable when | No annotated task exists. |
| Remediation | Name a concrete verification, or drop the citation the task cannot verify. |

### TASK-018 — A cited waiver is valid

| Field | Value |
|---|---|
| Level | `profile:engineering-governance` |
| Requirement | A waiver cited by a task **MUST** resolve to a valid, approved, unexpired waiver covering that exact Rule item and scope. |
| Applies when | A task cites a waiver. |
| Default severity | `major` |
| Enforcement | `automated` |
| Evidence | The cited waiver object against the validity contract in [rule-modeling](../specs/rule-modeling.md). |
| Pass condition | The waiver resolves, is unexpired and approved, and its scope covers the task's work. |
| Not applicable when | No task cites a waiver. |
| Remediation | Obtain a valid waiver, or plan the work to satisfy the Rule item. |

### TASK-019 — Task identifiers match the format and are unique

| Field | Value |
|---|---|
| Level | `baseline` |
| Requirement | Every task id **MUST** match the format its modeling Spec defines and **MUST** be unique inside the document. |
| Applies when | The document contains one or more task rows. |
| Default severity | `minor` |
| Enforcement | `automated` |
| Evidence | The id column against the format in [task-modeling](../specs/task-modeling.md). |
| Pass condition | Every id matches the format and appears exactly once. |
| Not applicable when | never |
| Remediation | Renumber the duplicate or malformed id, then update every reference to it. |

## Severity and gate policy

A defect that would send execution the wrong way is `major`: a dependency cycle, an unresolvable dependency, an undecidable acceptance, an untraced or uncovered design element, a missing or unverifiable governance annotation, an unresolvable Rule citation and an invalid waiver.

Escalate to `critical` when an invalid waiver or an unresolvable citation suppresses a `critical` engineering Rule item, since a document defect then silently removes a release-blocking obligation.

Presentation and bookkeeping defects are `minor`: frontmatter gaps, identifier format, an unassigned owner, a vague title, an oversized task and a blank dependency cell. They raise the cost of using the list rather than sending the work wrong.

## Waivers

A waiver may defer a traceability or coverage obligation when the upstream artifact records the deferral. It **MUST NOT** be used to hand off a list whose dependency graph does not resolve, nor to suppress an engineering-governance annotation whose trigger is met — that trigger exists precisely because the work carries risk.

## References

- [Task Modeling Schema](../specs/task-modeling.md)
- [Rule Modeling Schema](../specs/rule-modeling.md)
- [Findings List Schema](../specs/findings-list.md)
- [Technical Design Quality](./technical-design-quality.md)
- [Rule Governance](./workflow-rule-governance.md)
