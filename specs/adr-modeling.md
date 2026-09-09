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
## 背景

<上下文说明：驱动本决策的问题、约束、前置条件——回答 Why>

## 决策

<做了什么决定，一句话核心陈述 + 必要细节——回答 What>

## 替代方案

<考虑过哪些替代，每种方案为什么被拒——回答 Alternatives>

## 后果

<正面、负面、中性后果——回答 Consequences>
```

### 5.2 Content validation

- All 4 sections are required (`背景` / `决策` / `替代方案` / `后果`)
- The `替代方案` section carries at least 1 rejected option; a new ADR must explain why the other paths were not taken
- The `后果` section must cover both positive and negative, or neutral, consequences

---

## 6. Anti-patterns

- ❌ `status` repeated outside the frontmatter on a `**状态**：` line — writing it twice
- ❌ Using a legacy enum value such as `active` / `draft` / `approved` / `已批准` / `live`
- ❌ A `superseded` status with no `superseded_by`
- ❌ An `archived` status with no `archived_at` and `archived_reason`
- ❌ A missing `description` field
- ❌ The body missing any one of the 4 sections
- ❌ An empty `替代方案` section; it must explain why the other paths were not taken
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
description: 采用 PostgreSQL 作为主数据库，替代 MongoDB
---

# ADR 0017：采用 PostgreSQL 作为主数据库

## 背景

服务上线初期选用 MongoDB 以应对 schema 频繁演化。随着业务稳定，多数核心实体已形成稳定 schema，且开始出现跨实体事务、复杂报表、外键约束等需求——这些场景 MongoDB 表达成本高、运行时风险大。

## 决策

主数据库切换为 PostgreSQL 15，所有核心实体迁移到关系模型。MongoDB 仅保留用于日志聚合等真正非结构化的场景。

## 替代方案

- **保留 MongoDB**：被拒。跨实体事务、强一致性约束代价过高；团队 SQL 经验积累优于文档查询。
- **MySQL**：被拒。JSON 列支持、生成列、`RETURNING` 子句、CTE 等高级特性 PostgreSQL 更成熟。
- **双写 PostgreSQL + MongoDB**：被拒。双写一致性维护成本高，长期债务大于短期灵活性。

## 后果

- ✅ 事务一致性、外键约束、复杂查询表达直接，开发与运维成本下降
- ✅ 团队 SQL 技能复用，招聘门槛与之前相当
- ⚠️ 迁移期需要双写过渡，约 2 个迭代窗口
- ⚠️ 已有的 MongoDB 聚合查询要重写为 SQL，约 30 个查询需逐个验证
````

### 7.2 A superseded status example

```yaml
---
artifact_type: adr
created_by: decision-record
lifecycle: snapshot
created_at: 2025-08-12
status: superseded
description: 用 Elasticsearch 实现全文检索
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
