---
artifact_type: rule
name: requirement-quality
version: 2.1.0
created_by: ai-cortex
lifecycle: living
created_at: 2026-05-09
recommended_scope: user
status: active
---

# Rule: Requirement Quality

> A 5-dimension review checklist plus protocol compliance. Every item is independently verifiable.
>
> Applies to requirement documents that declare conformance to [specs/requirement-modeling.md](../specs/requirement-modeling.md).

---

## 5-dimension review

Authors self-check against this list before submitting for review. The checkpoints map one to one onto the 5 review dimensions: completeness, executability, clarity, soundness, traceability.

### 1. Completeness — is the information all there?

- [ ] All 8 required fields are filled in (ID, title, background, objective, acceptance, source, dependencies, risks)
- [ ] The background field carries a user story or a problem statement, and **not** a solution or technical detail
- [ ] More than 3 acceptance criteria, covering both functional scope and quality requirements
- [ ] The requirement's source is clear and traceable — not "someone mentioned it" or "passed on verbally"

### 2. Executability — can an implementer start immediately?

- [ ] The dependency list is clear, with the critical ones marked
- [ ] Every precondition states how it is verified, without ambiguity
- [ ] Every acceptance criterion is automatically verifiable or plainly testable
- [ ] A scope definition exists, or the "simple requirement" exemption applies, and the boundary is clear
- [ ] The open questions list is complete, and blocking questions have a resolution

### 3. Clarity — is it easy to read and unambiguous?

- [ ] The title is concise — ideally ≤ 15 words, and ≤ 80 characters
- [ ] The title states the subject of the requirement (a capability, a problem, a task), not the expected outcome; outcomes belong in the objective section
- [ ] The background contains no solution, implementation or architecture detail
- [ ] Acceptance criteria carry no vague words ("should", "reasonable", "appropriate", "fast")
- [ ] Every technical term is defined or linked on first use
- [ ] Terminology for risks, constraints and assumptions is used consistently, without mixing

### 4. Soundness — is it worth doing, and can it be done?

- [ ] Priority matches the effort — a P0 or P1 should not be a task that takes 1 day
- [ ] At least 1 critical risk, with an explicit mitigation
- [ ] The schedule matches the complexity, with no over-optimistic estimate
- [ ] No direct conflict with an existing requirement, or the conflict is stated explicitly
- [ ] Technical feasibility has been verified — a POC is done, or it is a known stack

### 5. Traceability — can evolution and impact be traced?

- [ ] The requirement ID follows the format PROJECT-REQ-nn and is not duplicated
- [ ] The source is explicit (feature request / business goal / incident) and traceable
- [ ] Dependencies are accurate, with no circular reference
- [ ] Related documents are complete — specs, ADRs, knowledge base links
- [ ] Business rules escalated to required carry a stable id, and rule-derived acceptance criteria cite it back (for example 「覆盖 R3」)
- [ ] Version history is clear; where the requirement has iterated, each change record states its reason

---

## Protocol compliance

Use this list to verify that a requirement document conforms to the protocol:

- [ ] **Frontmatter**: carries the metadata (ID, title, version where applicable)
- [ ] **8 required fields**: all present and complete
  - [ ] Requirement ID (PROJECT-REQ-nn format)
  - [ ] Title (< 80 characters, carrying the type)
  - [ ] Background and value (no solution, context clear)
  - [ ] Objective (a single line stating how the world changes once this ships; not a repeat of the background, and no solution)
  - [ ] Acceptance criteria (≥ 3, quantifiable, no vague words)
  - [ ] Dependencies and preconditions (write "no dependencies" explicitly when there are none)
  - [ ] Risks, constraints, assumptions (priority computed, mitigation attached)
  - [ ] Requirement source (type + link + decision background)
- [ ] **Conditionally required**: a scope definition is required when any of these hold:
  - [ ] Integration across multiple systems, or
  - [ ] Ambiguity across a boundary, or
  - [ ] Estimated effort > 5 days
- [ ] **Conditionally required**: a separate business rules section is required when any of these hold:
  - [ ] The rule set is itself the deliverable (pricing / eligibility / tax / risk scoring), or
  - [ ] One rule is cited by ≥ 2 acceptance criteria, or
  - [ ] The rules form a state machine or a decision table, or
  - [ ] The rules serve as the authoritative source (SSOT) for a downstream compliance audit
- [ ] **5-dimension review**: all pass
  - [ ] Completeness: the information is all there
  - [ ] Executability: an implementer can start immediately
  - [ ] Clarity: unambiguous, no piled-up jargon
  - [ ] Soundness: worth doing and technically feasible
  - [ ] Traceability: source and dependencies are clear
- [ ] **Optional fields**: where used, complete and valid
  - [ ] Scope definition (required when the conditions above hold)
  - [ ] Business rules (required when the conditions above hold; declarative or decision-table form)
  - [ ] Open questions (marked blocking or non-blocking)
  - [ ] Related documents (links working)
  - [ ] Priority and schedule (P0 / P1 / P2, timing realistic)
  - [ ] Definition of done (checklist complete)

---
