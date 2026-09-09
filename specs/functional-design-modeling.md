---
id: FUNCTIONAL_DESIGN_MODELING_SPEC_V1
name: Functional Design Modeling Schema
description: Spec defining functional design document fields, formats, and validation rules. Business/product-facing layer. Covers frontmatter contract, 6 mandatory body sections (Goal/Modules/Workflow/Exceptions/Acceptance/Trade-offs), and conditionally-mandatory sections (State Diagram, Permission Matrix).
version: 1.0.1
status: active
lifecycle: living
created_at: 2026-05-29
scope: |
  Defines the structural contract for functional design documents: the business/product-facing
  design layer — functional modules, business workflows, roles & permissions, business-object
  states, and exception scenarios. Applies to feature work with user-visible behavior or
  business-process change.
related:
  - ./spec-modeling.md
  - ./requirement-modeling.md
  - ./technical-design-modeling.md
  - ../rules/functional-design-quality.md
---

# Functional Design Modeling Schema

> **Data contract**: defines the field structure and body skeleton of a functional design document

---

## 1. Position and scope

A functional design document takes the business and product viewpoint and answers what behaviour the system presents to users: functional modules, business workflow, role permissions, business object states and exception scenarios. It sits between the requirement and the technical design. The requirement answers what to build, the functional design answers how it appears to users, and the technical design answers how it is engineered.

This spec is centred on business behaviour. It carries no architecture, database or API implementation detail — those belong to the technical design — and business rules are not restated here. They are cited from the upstream requirement by rule id, as `Covers R<n>`.

In scope:

- **New capability**: user-visible functional modules and business workflow
- **Workflow change**: adjustments to how an approval, order or document flows
- **Permission change**: adjustments to the role model, or to menu, operation and data permissions

Out of scope:

- Purely technical work such as architectural refactoring, dependency upgrades or infrastructure changes, which derives a technical design directly from an authorising ADR and skips this layer
- The engineering solution — architecture, database, interfaces — which belongs to the technical design document
- Pixel-level visual mockups, which belong to the UI design assets

---

## 3. Naming

```text
YYYY-MM-DD-<topic>-functional-design.md
```

- `<topic>`: a short description of the capability being designed, in kebab-case
- `YYYY-MM-DD`: the date the design landed; a snapshot artifact needs a timestamp to record which moment the approach belongs to
- Example: `2026-05-20-order-refund-functional-design.md`
- Where it lives is decided by project governance; typically `docs/designs/`

---

## 4. Frontmatter contract

```yaml
---
artifact_type: functional-design
lifecycle: snapshot
created_at: YYYY-MM-DD
parent: <path to upstream requirement document>
status: draft | approved | superseded
# conditional field
superseded_by: <path to new functional design>   # required when status is superseded
---
```

### 4.1 Field table

| Field | Type | Required | Description |
|---|---|---|---|
| `artifact_type` | string | yes | Fixed as `functional-design` |
| `lifecycle` | enum | yes | Fixed as `snapshot` — a design is a point-in-time decision |
| `created_at` | date | yes | The date the design was completed |
| `parent` | path | yes | Path to the upstream requirement document, which must be in `approved` status |
| `status` | enum | yes | `draft` / `approved` / `superseded`; semantics in §4.2 |
| `superseded_by` | path | conditional | Required when `status: superseded`, pointing at the successor functional design |

### 4.2 State machine semantics

| Status | Meaning | Entry condition |
|---|---|---|
| `draft` | A draft still under review | The functional design has just landed |
| `approved` | Approved; a technical design may derive from it | Business and product review passed, so it can serve as a technical design's `parent` |
| `superseded` | Replaced by a new functional design | The new design has landed and taken over; `superseded_by` must be filled in |

---

## 5. Body structure contract

### 5.1 The 6 required sections

Organised MECE across five dimensions: **What / How-structure / How-behaviour / Why / Verify**. Every functional design document must contain these 6 sections:

| # | Section | Dimension | Purpose | Validation |
|---|---|---|---|---|
| 1 | Goal | What | States the business capability this design delivers and what success looks like | At most 200 characters; no implementation detail; agrees with the upstream requirement's objective |
| 2 | Functional modules and boundaries | How-structure | Divides the capability into modules, states each one's responsibility, and marks what is in and out of scope | At least 1 module; each carries a name, a responsibility and a boundary — what it does and does not do; responsibilities do not overlap |
| 3 | Business workflow | How-behaviour | The end-to-end flow of the business from start to finish | At least 1 main flow carrying its start, its end, key steps and the roles involved; expressed as a flowchart, with branches marked explicitly |
| 4 | Exception and edge scenarios | How-behaviour | Expected behaviour on business exception branches and at the edges | At least 2, covering whichever of failure, withdrawal, timeout, duplicate submission and concurrency apply; each carries its trigger and the expected business behaviour, not the technical handling |
| 5 | Acceptance criteria | Verify | Completion conditions verifiable at the business level | At least 3, each traceable to an acceptance item of the upstream requirement, with no vague adjectives |
| 6 | Trade-offs and open questions | Why | The business trade-offs made and what remains undecided | At least 1 business trade-off stating the business cost of the rejected option, or an explicit statement that there were none. Business trade-offs only; technology-selection trade-offs belong to the technical design |

### 5.2 Optional sections

Added as the situation requires. A conditionally required section **becomes required** once its trigger is met:

| Section | Kind | Trigger |
|---|---|---|
| Business object states | Conditionally required | A business object — an order, task, approval or document — has ≥ 3 states and its transitions are driven by business rules. It then becomes required, declared as a state diagram or state table |
| Roles and permission matrix | Conditionally required | ≥ 2 roles are involved, or menu, operation or data permissions differ by role. It then becomes required, declared as a role-by-permission matrix |
| Scope | Optional | It spans systems or teams and the business boundary is easily misread |
| UI and interaction flow | Optional | There is user-facing interface interaction to describe |
| References | Optional | It cites an upstream requirement, a regulation or a business process standard |

### 5.3 Format detail

#### 5.3.1 How business object states are declared, once required

- Declare them as a state diagram or a state table, not as procedural steps.
- Each state carries a name and its entry condition; each transition carries its triggering event, source state and target state.
- Cover the terminal states (completed, cancelled, closed) and the exception states (timeout, withdrawal).

#### 5.3.2 How the permission matrix is declared, once required

- Rows are roles; columns are the three permission kinds — menu, operation and data.
- Each cell states allowed, not allowed, or conditionally allowed; a conditional cell must state its condition.

#### 5.3.3 Citing business rules

Business rules are declared in the upstream requirement. In its workflow and exception sections, a functional design cites the rule id back as `Covers R<n>` rather than restating it, so the same rule is not maintained across requirement, functional design and technical design.

---

## 6. Anti-patterns

- ❌ A missing required frontmatter field (artifact_type / lifecycle / created_at / parent / status)
- ❌ Architecture, database or API implementation detail, which belongs to the technical design
- ❌ Functional modules described in long prose instead of structured responsibility plus boundary
- ❌ A workflow missing its start or end, or with no flowchart
- ❌ Fewer than 2 exception or edge scenarios, or listing the exception without the expected business behaviour
- ❌ A business object with ≥ 3 states and no state diagram — the trigger is met but the section is missing
- ❌ Several roles involved and no permission matrix — the trigger is met but the section is missing
- ❌ Restating a business rule here instead of citing the upstream requirement as `Covers R<n>`
- ❌ Fewer than 3 acceptance criteria, or criteria that cannot be traced to the upstream requirement
- ❌ Trade-off analysis mixed with technology-selection trade-offs, which belong to the technical design
- ❌ No `parent` frontmatter — an orphaned design with no traceability
- ❌ A `superseded` status with no `superseded_by`

---

## 7. Examples

### 7.1 A compact skeleton: order refund approval

Each section shows the skeleton in 1-3 sentences; a real functional design expands each into full content.

````markdown
---
artifact_type: functional-design
lifecycle: snapshot
created_at: 2026-05-20
parent: ../requirements/SHOP-REQ-22.md
status: approved
---

# Functional design: order refund approval

## Goal

A refund raised by a support agent is paid out automatically once a supervisor approves it, so no refund is ever paid without approval and the turnaround time shortens.

## Functional modules and boundaries

- **Raising a refund**: a support agent raises a refund against an order, entering the amount and the reason. Does: validate that the amount <= the refundable balance. Does not: make the actual payment, which belongs to the payment integration in the technical design.
- **Approval handling**: a supervisor approves or rejects. Does: keep a record of the approval comment. Does not: multi-level approval, which stays single-level this round.
- **Refund execution**: once approved, trigger the refund and notify the customer.

## Business workflow

```

Agent raises refund -> system validates amount -> awaiting supervisor
  -> approved: trigger refund -> refund succeeds -> notify customer (Covers R1, the single-level approval rule)
  -> rejected: return to the agent with the rejection reason

```markdown

## Exception and edge scenarios

- **Duplicate submission**: raising a refund on an order that already has one "awaiting approval" or "in progress" -> reject, and state that a refund is already under way
- **Approval timeout**: awaiting approval for more than 48 hours -> escalate to the supervisor's manager by notification; never auto-approve
- **Refund failure**: the payment side fails the refund -> the refund moves to "failed", stays retryable, and leaves the rest of the order's state untouched

## Business object states

The refund state machine: `awaiting approval` ->(approved) `in progress` ->(refund succeeded) `completed` / `in progress` ->(refund failed) `failed` ->(retry) `in progress` / `awaiting approval` ->(rejected) `rejected` / `awaiting approval` ->(48h timeout) `awaiting approval` (escalation notice; the state does not change)

## Roles and permission matrix

| Role | Raise a refund | Approve a refund | See every refund |
|---|---|---|---|
| Support agent | Yes | No | Own submissions only |
| Supervisor | No | Yes | Yes |

## Acceptance criteria

- [ ] A refund must be approved by a supervisor before any payout is triggered (SHOP-REQ-22 §Acceptance 1)
- [ ] Concurrent in-progress refunds on one order are not allowed (§Acceptance 3)
- [ ] Awaiting approval for more than 48 hours escalates automatically (§Acceptance 4)

## Trade-offs and open questions

- **Single-level vs multi-level approval** (single-level chosen). Multi-level is stricter but slows the refund down, which conflicts with the objective of shortening turnaround; single-level this round.
- Open question: does a large refund need a second confirmation from finance — awaiting the business owner's answer by D+7 (non-blocking).
````

---

## 8. Relationship to other assets

- **Paired rule**: [rules/functional-design-quality.md](../rules/functional-design-quality.md) — the functional design quality review checklist across 5 dimensions: completeness, executability, clarity, soundness, traceability
- **Upstream spec**: [requirement-modeling.md](./requirement-modeling.md) — a functional design's `parent` must point at a requirement in `approved` status; business rules are declared on the requirement side and cited here by id
- **Downstream spec**: [technical-design-modeling.md](./technical-design-modeling.md) — only a functional design in `approved` status can derive a technical design, whose `parent` points back at it
- **Related industry standards**: IEEE 1016 (Software Design Description), BPMN (business process modelling), UML state diagrams, RBAC (the role-permission model)
- **Recursive basis**: this spec itself follows the 8-section skeleton of [spec-modeling.md](./spec-modeling.md) v2.0.0, skipping §2 mental model — the dimensions a functional design must answer are already carried by the 6-section MECE structure in §5.1
