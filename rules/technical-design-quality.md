---
artifact_type: rule
name: technical-design-quality
version: 2.0.0
model: RULE_MODEL_V1
rule_prefix: TDES
scope: technical design documents conforming to specs/technical-design-modeling.md
recommended_scope: project
status: active
created_by: ai-cortex
lifecycle: living
created_at: 2026-05-29
---

# Rule: Technical Design Quality

## Scope

Applies to a technical design document before tasks are derived or code is written. It decides whether the design is complete, executable without a clarifying question, unambiguous, sound and traceable to what authorized it.

It does not review business workflow, role permissions or business object states, which belong to the functional design; it does not inspect implementation; and it does not run the post-coding engineering gate.

## Profiles and parameters

| Name | Kind | Provenance | Meaning |
|---|---|---|---|
| `quality-attribute` | profile | — | An upstream quality scenario exists, or the change crosses a module, contract, data, trust or process boundary, introduces fallible I/O, or affects a declared quality budget |
| `data-change` | profile | — | The design defines or changes persisted schema, stored data or migration behaviour |
| `interface-change` | profile | — | The design defines or changes an interface consumed outside its own module |

Provenance follows [rule-modeling](../specs/rule-modeling.md) §5.4: a project writes only the `declared` values. This Rule set needs no project parameter; its obligations are decided from the document and its upstream chain.

## Rules

### TDES-001 — All required sections are present

| Field | Value |
|---|---|
| Level | `baseline` |
| Requirement | The document **MUST** contain every section its modeling Spec requires. |
| Applies when | always |
| Default severity | `major` |
| Enforcement | `automated` |
| Evidence | Document headings against the required set in [technical-design-modeling](../specs/technical-design-modeling.md). |
| Pass condition | Every required section exists, and a section with nothing to say states that rather than being absent. |
| Not applicable when | never |
| Remediation | Add the missing section, or state explicitly that it involves no change. |

### TDES-002 — Frontmatter is complete and within its enums

| Field | Value |
|---|---|
| Level | `baseline` |
| Requirement | The document **MUST** declare every required frontmatter field with a value inside its enum. |
| Applies when | always |
| Default severity | `minor` |
| Enforcement | `automated` |
| Evidence | Document frontmatter against [technical-design-modeling](../specs/technical-design-modeling.md). |
| Pass condition | Every required field is present, and the artifact type, lifecycle and status are inside their enums. |
| Not applicable when | never |
| Remediation | Add the missing field or correct the out-of-enum value. |

### TDES-003 — At least two candidate approaches are recorded

| Field | Value |
|---|---|
| Level | `baseline` |
| Requirement | The design **MUST** record at least two candidate approaches to the problem it solves. |
| Applies when | always |
| Default severity | `major` |
| Enforcement | `automated` |
| Evidence | The technology selection and trade-off section. |
| Pass condition | Two or more distinct approaches are described, not one approach and its absence. |
| Not applicable when | never |
| Remediation | Record the approaches that were genuinely considered, including the one already ruled out. |

### TDES-004 — Each rejected approach states its concrete drawback

| Field | Value |
|---|---|
| Level | `baseline` |
| Requirement | Every rejected approach **MUST** state the specific drawback that ruled it out. |
| Applies when | The design records a rejected approach. |
| Default severity | `major` |
| Enforcement | `judgment` |
| Evidence | The trade-off section read against each rejected option. |
| Pass condition | Each rejection names a concrete cost or limitation, not a preference or an unexplained score. |
| Not applicable when | No approach was rejected because only one is technically available, and that is stated. |
| Remediation | Replace the preference with the specific cost that decided against the option. |

### TDES-005 — Technical failure paths carry recovery behaviour

| Field | Value |
|---|---|
| Level | `baseline` |
| Requirement | The design **MUST** describe at least two technical failure paths and the recovery behaviour for each. |
| Applies when | always |
| Default severity | `major` |
| Enforcement | `tool-assisted` |
| Evidence | The data-flow and error-handling section read against the dependencies the design introduces. |
| Pass condition | The main failure paths the design creates are named, and each has a stated recovery or terminal outcome. |
| Not applicable when | never |
| Remediation | Add the missing failure path and state what the system does when it occurs. |

### TDES-006 — A section with nothing to change says so

| Field | Value |
|---|---|
| Level | `baseline` |
| Requirement | A required section that the change does not affect **MUST** say so explicitly rather than being left empty. |
| Applies when | A required section is not affected by this change. |
| Default severity | `minor` |
| Enforcement | `automated` |
| Evidence | Required section bodies. |
| Pass condition | No required section is empty; each states its content or that it involves no change. |
| Not applicable when | Every required section carries content. |
| Remediation | Write "no change" so a reader cannot mistake an omission for an oversight. |

### TDES-007 — A triggered quality-attribute design is present

| Field | Value |
|---|---|
| Level | `profile:quality-attribute` |
| Requirement | A design meeting a quality-attribute trigger **MUST** contain the quality attribute design section. |
| Applies when | An upstream quality scenario exists, or the change crosses a module, contract, data, trust or process boundary, introduces fallible I/O, or affects a declared quality budget. |
| Default severity | `major` |
| Enforcement | `tool-assisted` |
| Evidence | The upstream requirement's quality scenarios and the boundaries this design crosses. |
| Pass condition | The section exists and covers every triggered concern. |
| Not applicable when | No trigger is met and the design states which boundaries it does not cross. |
| Remediation | Add the section, or show that no trigger applies. |

### TDES-008 — Each triggered concern maps to a tactic, trade-off, verification and owner

| Field | Value |
|---|---|
| Level | `profile:quality-attribute` |
| Requirement | Each triggered quality concern **MUST** map its source and cited Rule ids to a system-specific tactic, its trade-off, a verification method and an owner. |
| Applies when | The quality attribute design section is required. |
| Default severity | `major` |
| Enforcement | `judgment` |
| Evidence | The quality attribute design rows read against the concerns the change triggers. |
| Pass condition | No triggered concern is answered by a generic instruction such as following best practice; each names what this system will do and how that will be checked. |
| Not applicable when | The quality attribute design section is not required. |
| Remediation | Replace the generic answer with the tactic this system adopts, its cost and the check that decides it. |

### TDES-009 — Every cited engineering Rule reference resolves

| Field | Value |
|---|---|
| Level | `profile:quality-attribute` |
| Requirement | Every engineering Rule id cited by the design **MUST** resolve to an active canonical Rule item. |
| Applies when | The design cites one or more engineering Rule ids. |
| Default severity | `major` |
| Enforcement | `automated` |
| Evidence | Cited ids resolved against the active canonical Rule sets. |
| Pass condition | Every cited id resolves to an active item of the version the design names. |
| Not applicable when | The design cites no engineering Rule. |
| Remediation | Correct the id, or cite the item that actually governs the concern. |

### TDES-010 — Profiles and required parameters are resolved or explicitly blocked

| Field | Value |
|---|---|
| Level | `profile:quality-attribute` |
| Requirement | The design **MUST** resolve the project profiles and parameters its triggered concerns need, or record their absence as a blocking open question. |
| Applies when | A triggered concern depends on a project profile or parameter. |
| Default severity | `major` |
| Enforcement | `tool-assisted` |
| Evidence | Project configuration, the design's open questions and the parameters the cited items need. |
| Pass condition | Each needed value is resolved, or its absence is listed as blocking; no needed value is silently skipped. |
| Not applicable when | No triggered concern depends on a project profile or parameter. |
| Remediation | Resolve the value, or record the missing decision as a blocking open question with an owner. |

### TDES-011 — Components carry signature-level definitions

| Field | Value |
|---|---|
| Level | `baseline` |
| Requirement | Each component **MUST** be defined to the level of its types, operations and interfaces, so it can be implemented independently. |
| Applies when | The design introduces or changes a component. |
| Default severity | `major` |
| Enforcement | `judgment` |
| Evidence | The components section read against what an implementer would need to start. |
| Pass condition | An implementer could build each component without inventing its interface. |
| Not applicable when | The change introduces no component. |
| Remediation | Add the operation and interface definitions the component is missing. |

### TDES-012 — A data design is complete enough to build from

| Field | Value |
|---|---|
| Level | `profile:data-change` |
| Requirement | The data design **MUST** carry fields, types, constraints and relationships sufficient to create the schema from it. |
| Applies when | The design changes persisted schema or stored data. |
| Default severity | `major` |
| Enforcement | `judgment` |
| Evidence | The database design section. |
| Pass condition | The schema could be created from the document without a further question. |
| Not applicable when | The change alters no persisted data. |
| Remediation | Add the missing field, type, constraint or relationship. |

### TDES-013 — An interface contract is complete enough to integrate against

| Field | Value |
|---|---|
| Level | `profile:interface-change` |
| Requirement | Each interface contract **MUST** carry its address, operation, request, response, error outcomes and authorization behaviour. |
| Applies when | The design defines or changes an interface consumed outside its own module. |
| Default severity | `major` |
| Enforcement | `judgment` |
| Evidence | The interface contracts section. |
| Pass condition | A consumer could integrate from the document without a further question. |
| Not applicable when | The change defines no externally consumed interface. |
| Remediation | Add the missing request, response, error or authorization detail. |

### TDES-014 — A task list can be derived without a clarifying question

| Field | Value |
|---|---|
| Level | `baseline` |
| Requirement | The design **MUST** be decided enough that the next layer can derive tasks without asking what was meant. |
| Applies when | always |
| Default severity | `major` |
| Enforcement | `judgment` |
| Evidence | The whole document read as the input to task derivation. |
| Pass condition | No section leaves a choice open that a task would have to make on its own. |
| Not applicable when | never |
| Remediation | Decide the open choice, or record it as a blocking open question with an owner. |

### TDES-015 — Terminology is consistent and introduced on first use

| Field | Value |
|---|---|
| Level | `baseline` |
| Requirement | Each technical term **MUST** be used consistently and introduced or linked where it first appears. |
| Applies when | always |
| Default severity | `minor` |
| Enforcement | `judgment` |
| Evidence | Term usage across sections and against the upstream artifacts. |
| Pass condition | One concept is named one way throughout, and no undefined term carries load. |
| Not applicable when | never |
| Remediation | Unify the naming, and define or link the term at first use. |

### TDES-016 — At least one structured representation is present

| Field | Value |
|---|---|
| Level | `baseline` |
| Requirement | The design **MUST** carry at least one diagram or table that shows structure rather than prose alone. |
| Applies when | always |
| Default severity | `minor` |
| Enforcement | `automated` |
| Evidence | Diagram blocks and tables in the document. |
| Pass condition | At least one structured representation is present and is referenced by the text. |
| Not applicable when | never |
| Remediation | Add the representation the content calls for; see [diagram-selection](./diagram-selection.md). |

### TDES-017 — The document carries no implementation code

| Field | Value |
|---|---|
| Level | `baseline` |
| Requirement | The design **MUST NOT** contain implementation code or scaffolding in place of a definition. |
| Applies when | always |
| Default severity | `minor` |
| Enforcement | `tool-assisted` |
| Evidence | Code blocks in the document and what each is doing there. |
| Pass condition | Code blocks carry contracts, schemas or configuration; none is an implementation body. |
| Not applicable when | never |
| Remediation | Replace the implementation with the signature or contract it was standing in for. |

### TDES-018 — The test strategy states verification methods

| Field | Value |
|---|---|
| Level | `baseline` |
| Requirement | The test strategy **MUST** state how the design will be verified, not carry test code. |
| Applies when | always |
| Default severity | `minor` |
| Enforcement | `judgment` |
| Evidence | The test strategy section. |
| Pass condition | Each verification names a method and what it would decide, with no test implementation. |
| Not applicable when | never |
| Remediation | Replace the test code with the method and the outcome it decides. |

### TDES-019 — The document carries no business-layer content

| Field | Value |
|---|---|
| Level | `baseline` |
| Requirement | The design **MUST NOT** define business workflow, role permissions or business object states, which the functional layer owns. |
| Applies when | always |
| Default severity | `minor` |
| Enforcement | `judgment` |
| Evidence | Section content compared with the functional design's ownership. |
| Pass condition | Business behaviour is cited from the functional layer rather than redefined here. |
| Not applicable when | never |
| Remediation | Move the business content upstream and cite it instead. |

### TDES-020 — Each technology choice states its reason

| Field | Value |
|---|---|
| Level | `baseline` |
| Requirement | Every technology choice **MUST** state the reason it was selected for this system. |
| Applies when | The design selects a technology, library or platform. |
| Default severity | `major` |
| Enforcement | `judgment` |
| Evidence | The technology selection section read against the constraints the design states. |
| Pass condition | Each choice names the property of this system that made it the right one. |
| Not applicable when | The change selects nothing new and says so. |
| Remediation | State the deciding property, or reconsider the choice. |

### TDES-021 — Dependencies and risks are listed explicitly

| Field | Value |
|---|---|
| Level | `baseline` |
| Requirement | The design **MUST** list the dependencies it takes on and the risks it carries. |
| Applies when | always |
| Default severity | `minor` |
| Enforcement | `automated` |
| Evidence | The dependency and risk statements in the document. |
| Pass condition | Both are present and specific; "none" is stated explicitly where true. |
| Not applicable when | never |
| Remediation | List the dependency or risk, or state explicitly that there is none. |

### TDES-022 — The parent resolves to an approved upstream of an allowed type

| Field | Value |
|---|---|
| Level | `baseline` |
| Requirement | The parent **MUST** point at a functional design, requirement or decision record that has reached its approved state. |
| Applies when | always |
| Default severity | `major` |
| Enforcement | `automated` |
| Evidence | The parent field, the referenced document's artifact type and its status. |
| Pass condition | The parent resolves, its type is allowed, and its status is approved or accepted. |
| Not applicable when | never |
| Remediation | Point at the correct upstream, or get that upstream approved before designing against it. |

### TDES-023 — Each acceptance criterion traces upstream

| Field | Value |
|---|---|
| Level | `baseline` |
| Requirement | Every acceptance criterion **MUST** trace to an upstream acceptance item, or for technical work authorized by a decision record, to one of its obligations or consequences. |
| Applies when | The design states acceptance criteria. |
| Default severity | `major` |
| Enforcement | `tool-assisted` |
| Evidence | Acceptance criteria mapped to the upstream artifact's items. |
| Pass condition | No criterion exists that the upstream chain does not call for. |
| Not applicable when | never |
| Remediation | Add the upstream reference, or return the untraced criterion upstream for approval. |

### TDES-024 — At least three acceptance criteria are stated

| Field | Value |
|---|---|
| Level | `baseline` |
| Requirement | The design **MUST** state at least three acceptance criteria. |
| Applies when | always |
| Default severity | `minor` |
| Enforcement | `automated` |
| Evidence | The acceptance criteria section. |
| Pass condition | Three or more distinct criteria are present. |
| Not applicable when | never |
| Remediation | Add the criteria that would decide whether this design was delivered. |

### TDES-025 — Cited external specifications resolve

| Field | Value |
|---|---|
| Level | `baseline` |
| Requirement | Every cited external specification or document **MUST** resolve. |
| Applies when | The design cites an external specification or document. |
| Default severity | `minor` |
| Enforcement | `automated` |
| Evidence | Link resolution over the document's references. |
| Pass condition | Every citation resolves to an existing target. |
| Not applicable when | The design cites nothing external. |
| Remediation | Correct the reference, or remove the citation it cannot support. |

### TDES-026 — A structural decision links to its decision record

| Field | Value |
|---|---|
| Level | `baseline` |
| Requirement | A decision with long-term structural consequence **MUST** link to its decision record, or record that one is to be written. |
| Applies when | The design makes a decision that constrains future structure beyond this change. |
| Default severity | `minor` |
| Enforcement | `judgment` |
| Evidence | The decisions the design makes and the decision records it links. |
| Pass condition | Each structural decision is either recorded or explicitly queued to be recorded. |
| Not applicable when | The design makes no decision beyond this change's own scope. |
| Remediation | Link the existing record, or note that one is owed and by whom. |

### TDES-027 — A breaking data change carries a migration and rollback plan

| Field | Value |
|---|---|
| Level | `profile:data-change` |
| Requirement | A breaking schema change, a data backfill or an irreversible operation **MUST** carry a detailed migration plan including its rollback strategy. |
| Applies when | The change breaks a schema, backfills data or performs an irreversible operation. |
| Default severity | `major` |
| Enforcement | `tool-assisted` |
| Evidence | The migration plan, its ordering, and the stated rollback behaviour. |
| Pass condition | The plan states the order of operations and what happens if it must be reversed partway. |
| Not applicable when | The change is additive and reversible. |
| Remediation | Add the migration ordering and the rollback strategy, or make the change reversible. |

## Severity and gate policy

A defect that would send the next layer the wrong way is `major`: a missing required section, a single approach with no alternative, an unexplained rejection, unhandled failure paths, an absent or generic quality-attribute design, an unresolvable Rule citation, an unresolved parameter that is not recorded as blocking, an underspecified component, data design or interface, a design that cannot be turned into tasks, an unjustified technology choice, an unapproved or wrong-type parent, an untraced acceptance criterion, and a breaking data change with no rollback.

Escalate to `critical` when the design authorizes an irreversible data operation with no stated rollback, since the damage cannot be undone downstream.

Presentation and bookkeeping defects are `minor`: frontmatter gaps, an empty section that should say "no change", inconsistent terminology, a missing diagram, implementation code standing in for a contract, a test strategy written as code, business content that belongs upstream, unlisted dependencies, fewer than three acceptance criteria, a dead citation and an unrecorded structural decision.

## Waivers

A waiver may defer a completeness or traceability obligation when the upstream artifact records the deferral and names who owes the decision. It **MUST NOT** be used to skip the quality-attribute design when a trigger is met, nor to approve a design whose parent is unapproved — in both cases the obligation exists because the work is not yet authorized to proceed.

## References

- [Technical Design Modeling Schema](../specs/technical-design-modeling.md)
- [Rule Modeling Schema](../specs/rule-modeling.md)
- [Findings List Schema](../specs/findings-list.md)
- [Task Quality](./task-quality.md)
- [Diagram Selection](./diagram-selection.md)
- [Rule Governance](./workflow-rule-governance.md)
