---
id: ADR_MODELING_SPEC_V2
name: ADR Modeling Schema
description: Spec defining the ADR document data contract — frontmatter field constraints, status 5-value enum, decay-related conditional fields, and required 4-section body structure.
version: 2.0.0
status: active
lifecycle: living
created_at: 2026-05-15
scope: |
  Defines the structural contract for Architecture Decision Records (ADRs): required frontmatter
  fields, status state machine, conditional fields for archived/superseded states, and the
  mandatory 4-section body structure.
related:
  - ./spec-modeling.md
  - ../rules/adr-management.md
---

# ADR Modeling Schema

> **Data contract**: defines the field structure and body skeleton of an Architecture Decision Record

---

## 1. Position and scope

An Architecture Decision Record is a point-in-time snapshot of an architectural decision — why it was made, what alternatives were considered at the time, and what it might lead to. Accumulated ADRs form an organisation's long-term decision record, letting whoever comes later trace and understand how the existing architecture came about.

In scope:

- Any architectural, technical or design decision whose why is worth keeping long-term
- Decisions that affect several people, span services, or shape long-term structure

Out of scope:

- A routine bug fix or small feature change, where a commit message suffices
- A purely normative constraint — write a rule, not "we decided to follow the convention"
- A local refinement of an existing ADR, which is appended to that ADR

The admission test and decay policy for ADRs are defined in [rules/adr-management.md](../rules/adr-management.md); this spec governs the data structure only.

---

## 2. Mental model

> The four core questions a sound ADR must answer clearly.

| Question | Description |
|---|---|
| **What** | What did we decide? A one-line statement |
| **Why** | Why this way? Context, driving forces, constraints |
| **Alternatives** | Which alternatives were considered, and why were they not chosen? Including each rejected option and its reason |
| **Consequences** | What will it lead to? Positive, negative and unknown risks |

The 4 sections of the body structure contract in §5 — context / decision / alternatives / consequences — map one to one onto these four questions.

---

## 3. Naming

```text
NNNN-{slug}.md
```

- **Number**: a 4-digit sequence starting at `0001`, monotonically increasing, and **never reused**
- **slug**: a short descriptive name in lowercase with hyphens, 3-6 words
- **Choosing a new number**: take the current maximum and add 1. Uniqueness relies on ADR documents living in one place, which project governance decides

---

## 4. Frontmatter contract

```yaml
---
artifact_type: adr
created_by: decision-record
lifecycle: snapshot
created_at: YYYY-MM-DD
status: proposed | accepted | superseded | archived | rejected
description: <a one-line summary of the ADR, complementing the H1 title>
# conditional fields, required according to status
superseded_by: NNNN-{slug}       # required when status is superseded
archived_at: YYYY-MM-DD           # required when status is archived
archived_reason: <one-line reason>  # required when status is archived
expires_at: YYYY-MM-DD            # optional; the quarterly review trigger
---
```

### 4.1 Field table

| Field | Type | Required | Description |
|---|---|---|---|
| `artifact_type` | string | yes | Fixed as `adr` |
| `created_by` | string | yes | Fixed as `decision-record` |
| `lifecycle` | enum | yes | Fixed as `snapshot` — an ADR is a point-in-time decision |
| `created_at` | date | yes | The decision date, `YYYY-MM-DD` |
| `status` | enum | yes | A 5-value enum; semantics in §4.2 |
| `description` | string | yes | A one-line summary complementing the H1 title |
| `superseded_by` | string | conditional | Required when `status: superseded`; the number of the replacing ADR, `NNNN-{slug}` |
| `archived_at` | date | conditional | Required when `status: archived` |
| `archived_reason` | string | conditional | Required when `status: archived` |
| `expires_at` | date | optional | The review reminder date; passing it without a review triggers a decay assessment |

### 4.2 State machine semantics

| Status | Meaning | Entry condition |
|---|---|---|
| `proposed` | Proposed, awaiting decision | The ADR has just landed and has not passed review |
| `accepted` | Adopted and currently in force | The decision was approved and implemented |
| `superseded` | Replaced by another ADR | A new ADR landed and took over the decision; `superseded_by` must be filled in |
| `archived` | Archived, no longer active | The decision no longer affects the current system; `archived_at` and `archived_reason` must be filled in |
| `rejected` | Explicitly rejected, kept as decision history | Review decided against it, and the record is kept as a rejected option |

**Legacy enum values, forbidden**: `draft` / `active` / `approved` / `已批准` / `live`

---

## 5. Body structure contract

### 5.1 The 4 required sections

```markdown
## Context

<the problem, constraints and preconditions that drove this decision — answering Why>

## Decision

<what was decided: the core statement in one sentence, plus the detail it needs — answering What>

## Alternatives

<which alternatives were considered, and why each was rejected — answering Alternatives>

## Consequences

<the positive, negative and neutral consequences — answering Consequences>
```

### 5.2 Content validation

- All 4 sections are required (`Context` / `Decision` / `Alternatives` / `Consequences`)
- The `Alternatives` section carries at least 1 rejected option; a new ADR must explain why the other paths were not taken
- The `Consequences` section must cover both positive and negative, or neutral, consequences

---

## 6. Anti-patterns

- ❌ `status` repeated outside the frontmatter on a `**状态**：` line — writing it twice
- ❌ Using a legacy enum value such as `active` / `draft` / `approved` / `已批准` / `live`
- ❌ A `superseded` status with no `superseded_by`
- ❌ An `archived` status with no `archived_at` and `archived_reason`
- ❌ A missing `description` field
- ❌ The body missing any one of the 4 sections
- ❌ An empty `Alternatives` section; it must explain why the other paths were not taken
- ❌ A filename number shorter than 4 digits — `001-` rather than `0001-`
- ❌ Reusing a filename number; a retired number is never reassigned

---

## 7. Examples

### 7.1 A fully compliant ADR

````markdown
---
artifact_type: adr
created_by: decision-record
lifecycle: snapshot
created_at: 2026-04-12
status: accepted
description: Adopt PostgreSQL as the primary database, replacing MongoDB
---

# ADR 0017: adopt PostgreSQL as the primary database

## Context

MongoDB was chosen when the service first shipped, because the schema was still changing constantly. As the business settled, most core entities reached a stable schema, and needs began to appear for cross-entity transactions, complex reporting, foreign key constraints and the like — all of which MongoDB expresses at high cost and with real runtime risk.

## Decision

Switch the primary database to PostgreSQL 15 and move every core entity onto the relational model. MongoDB is kept only for genuinely unstructured work such as log aggregation.

## Alternatives

- **Keep MongoDB**: rejected. Cross-entity transactions and strong consistency constraints cost too much, and the team's accumulated SQL experience outweighs its document-query experience.
- **MySQL**: rejected. PostgreSQL is more mature on the advanced features that matter here — JSON columns, generated columns, the `RETURNING` clause, CTEs.
- **Dual-write to PostgreSQL and MongoDB**: rejected. Keeping a dual write consistent costs too much to maintain; the long-term debt outweighs the short-term flexibility.

## Consequences

- ✅ Transactional consistency, foreign key constraints and complex queries all express directly, lowering both development and operations cost
- ✅ The team's SQL skills carry over, and the hiring bar is no higher than before
- ⚠️ The migration needs a dual-write transition, about 2 iteration windows
- ⚠️ The existing MongoDB aggregation queries have to be rewritten as SQL, about 30 of them, each verified individually
````

### 7.2 A superseded status example

```yaml
---
artifact_type: adr
created_by: decision-record
lifecycle: snapshot
created_at: 2025-08-12
status: superseded
description: Implement full-text search with Elasticsearch
superseded_by: 0058-adopt-typesense-for-search
---
```

---

## 8. Relationship to other assets

- **Paired rule**: [rules/adr-management.md](../rules/adr-management.md) — ADR discipline: the admission test, status enforcement, the decay policy, and the boundary with decisions

### 8.1 Decay thresholds

| Trigger | Action |
|---|---|
| `accepted`, and `created_at` was ≥ 12 months ago, and no document has referenced it in the last 12 months, and the decision no longer affects the system | Move to `archived` and fill in `archived_at` and `archived_reason` |
| `archived`, and `archived_at` was ≥ 6 months ago, and no file references it | `git rm` may be used to delete it physically |
| `rejected` / `superseded` / referenced by another ADR's `superseded_by` field | **Never deleted physically** — decision history and the chain of supersession are organisational memory |

### 8.2 Boundary with the rule

This spec governs the data structure only — fields, state machine, required-field relationships. The writing discipline itself, how to judge admission, how to perform a status transition, how to carry out a `git rm` decay, is carried by [rules/adr-management.md](../rules/adr-management.md). The two apply in parallel.

### 8.3 Recursive basis

This spec itself follows the 8-section skeleton of [spec-modeling.md](./spec-modeling.md) v2.0.0. Every conditionally required section (§2 / §3 / §4 / §4.2) is triggered, making the ADR a full template for the skeleton.
