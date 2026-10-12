---
artifact_type: rule
name: functional-design-quality
version: 2.0.0
scope: reviewing or self-checking a functional design document
recommended_scope: user
status: active
---

# Rule: Functional Design Quality

> A 5-dimension review checklist plus spec compliance. Every item is independently verifiable.
>
> Applies to functional design documents that declare conformance to [specs/functional-design-modeling.md](../specs/functional-design-modeling.md).

---

## 5-dimension review

### 1. Completeness — is the structure all there?

- [ ] All 6 required sections present (objective / functional modules and boundaries / business workflow / exception and edge scenarios / acceptance criteria / trade-offs and open questions)
- [ ] Frontmatter complete (artifact_type / lifecycle / created_at / parent / status)
- [ ] The business workflow states its start, its end, its key steps and the roles involved, and is expressed as a flowchart
- [ ] At least 2 exception or edge scenarios, covering whichever of failure / withdrawal / timeout / duplicate submission / concurrency apply

### 2. Executability — can the next layer derive a technical design directly?

- [ ] Each functional module has a clear responsibility and an explicit boundary — what it does and what it does not
- [ ] Workflow branches are explicit, with no ambiguous fork
- [ ] Acceptance criteria are verifiable
- [ ] A technical design can be derived without asking a clarifying question

### 3. Clarity — is it unambiguous?

- [ ] Terminology is consistent, with the English given alongside on first use
- [ ] At least one structured representation is present (flowchart / state diagram / permission matrix)
- [ ] No technical implementation detail — architecture, database, API
- [ ] Business rules are cited from the upstream requirement as `Covers R<n>`, not restated here

### 4. Soundness — does the design hold up?

- [ ] Every workflow closes — each path reaches a terminal state
- [ ] The trade-off analysis states the business cost of each rejected option, not its technical cost
- [ ] Expected behaviour in an exception scenario is business behaviour, not technical handling
- [ ] Scope agrees with the upstream requirement

### 5. Traceability — can the impact of a change be located?

- [ ] Frontmatter `parent` points at an upstream requirement in `approved` status
- [ ] Each acceptance criterion traces to an acceptance item of that requirement
- [ ] Each business rule id cited (`Covers R<n>`) exists in the upstream requirement
- [ ] Cited external specifications have working links

---

## Conditionally required sections

- [ ] When a business object has ≥ 3 states and transitions are driven by business rules, a separate business object state section is present (state diagram or state table, covering terminal and exception states)
- [ ] When ≥ 2 roles are involved, or menu, operation or data permissions differ by role, a separate role and permission matrix is present (rows = roles, columns = the three permission kinds)
- [ ] UI applicability is assessed against [functional-design-modeling §5.2–§5.3.4](../specs/functional-design-modeling.md#534-ui-and-interaction-decisions-once-required); a triggered change has a UI and interaction flow section, and a skipped change has a reason in its existing handoff
- [ ] A triggered UI section carries user tasks, key states and interactions, selection rationale, reuse constraints, independent UI asset links or a reason none is needed, and acceptance handoff
- [ ] Existing stack, components and design tokens are preferred; reuse is justified and does not require external references
- [ ] External reference sources and their effect on selection are traceable; consequential technical or licensing claims are verified against original documentation. Visual inspiration needs no technical research record; unavailable sources have an explicit limitation and fallback, with no fabricated evidence or authorization, quality or license claims
- [ ] UI acceptance names observable outcomes, responsive and keyboard/accessibility checks, verification methods and responsible roles; code review is not presented as visual acceptance

---

## Spec compliance (specs/functional-design-modeling.md)

- [ ] Frontmatter carries every required field
- [ ] `artifact_type: functional-design`
- [ ] `lifecycle: snapshot`
- [ ] `status` ∈ `draft` / `approved` / `superseded`
- [ ] All 6 required sections exist
- [ ] At least 2 exception or edge scenarios
- [ ] At least 3 acceptance criteria
- [ ] `superseded_by` filled in when status is `superseded`

---

## Anti-patterns

- ❌ Contains technical implementation detail — architecture, database, API
- ❌ Restates a business rule here instead of citing the upstream requirement
- ❌ Meets the condition that makes a section required, yet lacks the state diagram or permission matrix
- ❌ A new interface or significant experience change lacks UI decisions, or a backend/copy/pattern-preserving repair is forced through external research
- ❌ Trade-off analysis mixed with technology-selection trade-offs
- ❌ No `parent` frontmatter — an orphaned design

---

## Related assets

- **Diagram selection**: [diagram-selection](./diagram-selection.md) — choosing between a workflow and a state diagram, picking a tool, and steering clear of rendering pitfalls all defer to those criteria
- **UI decision workflow**: [UI design decisions](../docs/guides/ui-design-decisions.md) — reference selection, source limitations and implementation/acceptance handoff
