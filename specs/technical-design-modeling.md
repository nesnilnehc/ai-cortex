---
id: TECHNICAL_DESIGN_MODELING_SPEC_V1
name: Technical Design Modeling Schema
description: Spec defining technical design document fields, formats, and validation rules. Engineering-facing layer. Covers frontmatter contract, 9 mandatory body sections (Goal/Architecture/Components/Database/APIs/DataFlow&Errors/TechChoices/TestStrategy/Acceptance), and conditionally-mandatory sections.
version: 2.0.0
status: active
lifecycle: living
created_at: 2026-05-29
scope: |
  Defines the structural contract for technical design documents: the engineering-facing design
  layer — architecture, service decomposition, components, database design, API contracts, error
  handling, tech selection. Always present before tasks are derived. Applies to any work that
  produces an implementation.
related:
  - ./spec-modeling.md
  - ./functional-design-modeling.md
  - ./requirement-modeling.md
  - ./task-modeling.md
  - ../rules/technical-design-quality.md
---

# Technical Design Modeling Schema

> **Data contract**: defines the field structure and body skeleton of a technical design document

---

## 1. Position and scope

A technical design document takes the engineering viewpoint and answers how something is built: architecture, service decomposition, components and detailed design, database, interface contracts, error handling and technology selection. It bridges the upstream design and the task list, and is the direct source of that list.

A technical design **always exists** before tasks are derived. A purely procedural change may make it brief, but never absent. The functional layer, by contrast, can be skipped: purely technical work such as refactoring, infrastructure or a dependency upgrade derives its technical design directly from the ADR that authorised it.

In scope:

- **Architecture**: system, service and module architecture, and service decomposition
- **Component and detailed design**: signature-level definitions of classes, methods and interfaces
- **Data and integration design**: database design, API contracts, cross-service integration
- **Purely technical work**: architectural refactoring, dependency upgrades, infrastructure changes — there is no functional layer, and `parent` points at the authorising ADR

Out of scope:

- Implementation at code level, which belongs in code comments or an ADR
- The local design of a single function or class, which goes straight into the PR description
- Business workflow, role permissions and business object states, which belong to the functional design document
- Exploratory prototypes, which belong in `experiments/` or as an ADR candidate

---

## 3. Naming

```text
YYYY-MM-DD-<topic>-technical-design.md
```

- `<topic>`: a short description of what is being designed, in kebab-case
- `YYYY-MM-DD`: the date the design landed; a snapshot artifact needs a timestamp to record which moment the approach belongs to
- Example: `2026-05-22-order-refund-technical-design.md`
- Where it lives is decided by project governance; typically `docs/designs/`

---

## 4. Frontmatter contract

```yaml
---
artifact_type: technical-design
lifecycle: snapshot
created_at: YYYY-MM-DD
parent: <path to upstream functional-design OR requirement>
status: draft | approved | superseded
# conditional field
superseded_by: <path to new technical design>   # required when status is superseded
---
```

### 4.1 Field table

| Field | Type | Required | Description |
|---|---|---|---|
| `artifact_type` | string | yes | Fixed as `technical-design` |
| `lifecycle` | enum | yes | Fixed as `snapshot` — a design is a point-in-time decision |
| `created_at` | date | yes | The date the design was completed |
| `parent` | path | yes | **Polymorphic**: normally points at the upstream `functional-design`; a non-functional requirement may skip the functional layer and point at the `requirement`; purely technical work with no corresponding requirement points at the `adr` that authorised it. Validate that the `parent` has `artifact_type ∈ {functional-design, requirement, adr}` |
| `status` | enum | yes | `draft` / `approved` / `superseded`; semantics in §4.2 |
| `superseded_by` | path | conditional | Required when `status: superseded`, pointing at the successor technical design |

### 4.2 State machine semantics

| Status | Meaning | Entry condition |
|---|---|---|
| `draft` | A draft still under review | The technical design has just landed |
| `approved` | Approved; tasks may derive from it | Engineering review passed, so it can serve as a task list's `parent` |
| `superseded` | Replaced by a new technical design | The new design has landed and taken over; `superseded_by` must be filled in |

---

## 5. Body structure contract

### 5.1 The 9 required sections

Organised MECE across five dimensions: **What / How-structure / How-behaviour / Why / Verify**. Every technical design document must contain these 9 sections:

| # | Section | Dimension | Purpose | Validation |
|---|---|---|---|---|
| 1 | Goal | What | States the scope this technical design delivers and what success looks like | At most 200 characters; agrees with the upstream functional-design, or requirement |
| 2 | Architecture and service decomposition | How-structure | The system, service and module layers, their boundaries, and how services are split | At least 1 structured representation, a diagram or a table; external and internal dependencies marked; the split boundary drawn where several services are involved |
| 3 | Components and detailed design | How-structure | The responsibilities of the key components, plus class, method and interface definitions to implement from | At least 1 component, each carrying its responsibility and dependencies; key classes, methods and interfaces given at signature level |
| 4 | Database design | How-structure | Table structure, fields, indexes, relationships, seed data and migration | Entities carry fields, types, constraints and relationships; key indexes marked; seed data and the migration plan included; **where nothing changes, state "no database change" rather than leaving it blank** |
| 5 | Interface contracts | How-structure | The outward interfaces: path, method, request parameters, response shape, error codes and authorization | Each interface carries path, method, request, response, error codes and authorization; each event carries its topic and payload schema; **where nothing changes, state "no interface change"** |
| 6 | Data flow and error handling | How-behaviour | How data moves between components and services, plus the technical failure paths and their handling | The data flow on the key paths marked; at least 2 technical failure paths, each carrying its failure condition, how it is detected, and the recovery strategy |
| 7 | Technology choices and trade-offs | Why | The technology decisions, the alternatives, and the dependencies and risks | At least 2 alternatives, each carrying advantages, drawbacks, whether it was chosen, and why; dependencies and risks listed explicitly |
| 8 | Test strategy | Verify | States the verification methods — **not test code** | Covers the test layers (unit, integration, end-to-end) and how acceptance happens (automated or manual) |
| 9 | Acceptance criteria | Verify | The verifiable conditions for the technical design being complete | At least 3, each traceable to an acceptance item of the upstream functional-design — or of the requirement where the functional layer was skipped and `parent` points straight at it |

### 5.2 Optional sections

Added as the situation requires. A conditionally required section **becomes required** once its trigger is met:

| Section | Kind | Trigger |
|---|---|---|
| Migration plan | Conditionally required | A breaking schema change, a data backfill or an irreversible operation is involved. It then becomes required, including the rollback strategy; otherwise the migration is inlined in §4 |
| Deployment and operations | Optional | There are deployment changes, scaling policy or configuration management to cover |
| Cross-cutting concerns | Optional | Security, performance or observability has a design of its own |
| Scheduling | Optional | There are scheduled tasks, background jobs or queue consumers |
| Scope | Optional | The integration boundary across services or teams is easily misread |
| References | Optional | It cites an ADR, an external specification or an upstream design |

### 5.3 Format detail

#### 5.3.1 What acceptance criteria trace to depends on the `parent` type

- Where `parent` is a `functional-design`, the normal case: each criterion traces to an acceptance item of that functional design, cited as `Covers FD §Acceptance N`.
- Where `parent` is a `requirement`, the functional layer having been skipped: each criterion traces to an acceptance item of the requirement.

#### 5.3.2 The "no change" escape hatch

For a purely procedural design, §4 database design and §5 interface contracts may involve no change at all. In that case the document must state "no database change" or "no interface change" explicitly, as a positive assertion, and **must not be left blank** — a blank leaves no way to tell an omission from a genuine absence of change.

---

## 6. Anti-patterns

- ❌ A missing required frontmatter field (artifact_type / lifecycle / created_at / parent / status)
- ❌ The `parent`'s artifact_type outside {functional-design, requirement}, breaking the chain
- ❌ Code or scaffolding; a design does not carry the implementation, which lives in the code
- ❌ Business workflow, role permissions or business object states, which belong to the functional design
- ❌ A components section written as long prose instead of structured responsibilities plus signature-level definitions
- ❌ A data model listing entity names without fields, types or relationships, which cannot be implemented from
- ❌ An interface contract that says there is an API without listing method, request, response and error codes, which cannot be integrated against
- ❌ §4 or §5 left blank rather than stating no change, leaving an omission indistinguishable from N/A
- ❌ A single approach with no trade-off analysis, missing the alternatives in §7
- ❌ A trade-off analysis listing only the chosen option's advantages; it must carry the rejected options' drawbacks
- ❌ A test strategy written as test code rather than as verification methods
- ❌ Fewer than 3 acceptance criteria, or criteria tracing to the wrong target for the `parent` type
- ❌ No `parent` frontmatter — an orphaned design with no traceability
- ❌ A `superseded` status with no `superseded_by`

---

## 7. Examples

### 7.1 A compact skeleton: order refund approval

Each section shows the skeleton in 1-3 sentences; a real technical design expands each into full content.

````markdown
---
artifact_type: technical-design
lifecycle: snapshot
created_at: 2026-05-22
parent: ../designs/2026-05-20-order-refund-functional-design.md
status: approved
---

# Technical design: order refund approval

## Goal

Implement the raise / approve / execute flow for a refund order, integrate the payment side's refund API, and support the single-level approval and timeout escalation set by the functional design.

## Architecture and service decomposition

```

[agent / supervisor client] -> [Order Service] -> [Refund Module] -> [Payment Gateway (external)]
                                          |
                                          v
                                    [Notification Service]

```markdown

External dependency: the Payment Gateway (its refund API). Internal dependencies: Order Service, Notification Service. No separate Refund Service is split out this round; it lives as a module of Order Service.

## Components and detailed design

- **RefundService**: `initiate(orderId, amount, reason)` / `approve(refundId, approverId)` / `reject(refundId, reason)`. Responsible for state transitions and concurrency control.
- **RefundExecutor**: `execute(refundId)` calls the Payment Gateway and retries on failure. Responsible for idempotent refunds.

## Database design

```

refund_order
  id: UUID PK
  order_id: UUID FK -> order.id (index)
  amount: decimal NOT NULL
  status: enum NOT NULL (awaiting_approval/in_progress/completed/failed/rejected)
  approver_id: UUID NULL
  created_at: timestamp NOT NULL

```markdown

Constraint: a partial unique index on (order_id) WHERE status IN ('awaiting_approval','in_progress'), guaranteeing that one order never has two refunds in flight. Migration: a new table, with no data backfill.

## Interface contracts

- `POST /refunds` — body `{order_id, amount, reason}` -> 201 `{refund_id, status}` / 409 `DUPLICATE_ACTIVE_REFUND` / 422 `AMOUNT_EXCEEDS_REFUNDABLE`; authorization: the support agent role
- `POST /refunds/{id}/approve` -> 200 `{status}` / 403 `NOT_APPROVER`; authorization: the supervisor role
- Events: `REFUND_APPROVED` / `REFUND_FAILED` (payload schema in the nats-messaging spec)

## Data flow and error handling

Refund execution: approve -> write status=in_progress -> RefundExecutor calls the Payment Gateway -> on success write completed and emit REFUND_APPROVED / on failure write failed and emit REFUND_FAILED.

- **Payment gateway timeout**: mark it failed and keep it retryable; do not block other operations on the order
- **Concurrent approval**: approve uses optimistic locking on the status version, and a second approval returns 409

## Technology choices and trade-offs

- **Option A: a partial unique index preventing concurrent refunds** (chosen). Upside: a strong guarantee at the database layer. Downside: it depends on PostgreSQL partial indexes.
- **Option B: an application-level distributed lock** (rejected). Upside: database-independent. Downside: the lock-expiry boundaries are complex, and it is weaker than a database constraint.
- Dependencies and risks: the Payment Gateway refund API is rate limited to 10 QPS, so peaks have to queue.

## Test strategy

- Unit: state transitions, amount validation, idempotent execution
- Integration: the full raise / approve / refund path with a mocked Payment Gateway
- How it is verified: CI runs unit plus integration automatically

## Acceptance criteria

- [ ] A concurrent refund on the same order is rejected by the database constraint (Covers FD §Acceptance 2)
- [ ] A failed refund is retryable and leaves the order state untouched (Covers FD §Acceptance 1)
- [ ] Approval authorization: only the supervisor role may approve (Covers FD §permission matrix)
````

---

## 8. Relationship to other assets

- **Paired rule**: [rules/technical-design-quality.md](../rules/technical-design-quality.md) — the technical design quality review checklist across 5 dimensions: completeness, executability, clarity, soundness, traceability
- **Upstream specs**: [functional-design-modeling.md](./functional-design-modeling.md) in the normal case, where the technical design's `parent` points at an `approved` functional design; [requirement-modeling.md](./requirement-modeling.md) where a non-functional requirement skips the functional layer and points straight at an `approved` requirement; and for purely technical work with no corresponding requirement, the `parent` points at the ADR that authorised it
- **Downstream spec**: [task-modeling.md](./task-modeling.md) — a task list's `parent` points at a technical design in `approved` status
- **Related industry standards**: IEEE 1016 (Software Design Description), the C4 model, the arc42 template, and Google's design doc practice
- **Recursive basis**: this spec itself follows the 8-section skeleton of [spec-modeling.md](./spec-modeling.md) v2.0.0, skipping §2 mental model — the dimensions a technical design must answer are already carried by the 9-section MECE structure in §5.1
