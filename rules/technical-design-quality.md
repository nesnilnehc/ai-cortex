---
artifact_type: rule
name: technical-design-quality
version: 1.0.0
scope: 评审或自检技术设计文档时
recommended_scope: user
status: active
---

# Rule: Technical Design Quality

> A 5-dimension review checklist plus spec compliance. Every item is independently verifiable.
>
> Applies to technical design documents that declare conformance to [specs/technical-design-modeling.md](../specs/technical-design-modeling.md).

---

## 5-dimension review

### 1. Completeness — is the structure all there?

- [ ] All 9 required sections present (objective / architecture and service decomposition / components and detailed design / database design / interface contracts / data flow and error handling / technology selection and trade-offs / test strategy / acceptance criteria)
- [ ] Frontmatter complete (artifact_type / lifecycle / created_at / parent / status)
- [ ] At least 2 alternative approaches, with trade-offs
- [ ] At least 2 technical failure paths, with recovery strategies

### 2. Executability — can the next layer break this into tasks directly?

- [ ] Components carry signature-level class, method and interface definitions, and can be implemented independently
- [ ] The database design carries fields, types, constraints and relationships, enough to create the tables from
- [ ] Interface contracts carry path, method, request, response, error codes and authorization, enough to integrate against
- [ ] A task list can be derived without asking a clarifying question

### 3. Clarity — is it unambiguous?

- [ ] Terminology is consistent, with the English given alongside on first use
- [ ] At least one structured representation is present — a diagram or a table
- [ ] No implementation code and no scaffolding
- [ ] The test strategy states verification methods, not test code
- [ ] Where §4 or §5 involves no change, it says "no change" rather than being left blank

### 4. Soundness — does the design hold up?

- [ ] Each technology choice has a stated reason, not "it looks good"
- [ ] The trade-off analysis states the concrete drawbacks of each rejected option
- [ ] Error handling covers the main technical failure paths
- [ ] Dependencies and risks are listed explicitly

### 5. Traceability — can the impact of a change be located?

- [ ] The frontmatter `parent`'s artifact_type ∈ {functional-design, requirement}
- [ ] Each acceptance criterion traces to an acceptance item of the upstream functional-design — or, when the functional layer is skipped, of the requirement
- [ ] Key decisions can be turned into an ADR, or already link to one
- [ ] Cited external specifications have working links

---

## Conditionally required sections

- [ ] Where a breaking schema change, a data backfill or an irreversible operation is involved, a detailed data migration plan is present, including the rollback strategy

---

## Spec compliance (specs/technical-design-modeling.md)

- [ ] Frontmatter carries every required field
- [ ] `artifact_type: technical-design`
- [ ] `lifecycle: snapshot`
- [ ] `status` ∈ `draft` / `approved` / `superseded`
- [ ] All 9 required sections exist
- [ ] At least 2 alternative approaches
- [ ] At least 2 technical failure paths
- [ ] At least 3 acceptance criteria
- [ ] `parent` points at an upstream design in `approved` status
- [ ] `superseded_by` filled in when status is `superseded`

---

## Anti-patterns

- ❌ Contains code or scaffolding
- ❌ Contains business workflow, role permissions or business object states — those belong to the functional design
- ❌ A single approach with no trade-off analysis
- ❌ §4 or §5 left blank instead of stating "no change"
- ❌ A test strategy written as test code
- ❌ The `parent`'s artifact_type outside {functional-design, requirement}
- ❌ No `parent` frontmatter — an orphaned design

---

## Related assets

- **Diagram selection**: [diagram-selection](./diagram-selection.md) — choosing among structured representations — architecture, component and deployment diagrams and the like — picking a tool, and steering clear of rendering pitfalls all defer to those criteria
