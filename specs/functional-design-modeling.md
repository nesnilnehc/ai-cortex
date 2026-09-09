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

This spec is centred on business behaviour. It carries no architecture, database or API implementation detail — those belong to the technical design — and business rules are not restated here. They are cited from the upstream requirement by rule id, as `覆盖 R<n>`.

In scope:

- **New capability**: user-visible functional modules and business workflow
- **Workflow change**: adjustments to how an approval, order or document flows
- **Permission change**: adjustments to the role model, or to menu, operation and data permissions

不In scope:

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

Business rules are declared in the upstream requirement. In its workflow and exception sections, a functional design cites the rule id back as `覆盖 R<n>` rather than restating it, so the same rule is not maintained across requirement, functional design and technical design.

---

## 6. Anti-patterns

- ❌ A missing required frontmatter field (artifact_type / lifecycle / created_at / parent / status)
- ❌ Architecture, database or API implementation detail, which belongs to the technical design
- ❌ Functional modules described in long prose instead of structured responsibility plus boundary
- ❌ A workflow missing its start or end, or with no flowchart
- ❌ Fewer than 2 exception or edge scenarios, or listing the exception without the expected business behaviour
- ❌ A business object with ≥ 3 states and no state diagram — the trigger is met but the section is missing
- ❌ Several roles involved and no permission matrix — the trigger is met but the section is missing
- ❌ Restating a business rule here instead of citing the upstream requirement as `覆盖 R<n>`
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

# 功能设计：订单退款审批

## 目标

让客服发起的退款请求经主管审批后自动退款，杜绝未审批直接退款，缩短退款时效。

## 功能模块与边界

- **退款发起**：客服按订单发起退款，填写金额与原因。做：校验金额 ≤ 可退余额。不做：实际打款（归技术设计的支付集成）。
- **审批处理**：主管审批 / 驳回。做：审批意见留痕。不做：多级审批（本期单级）。
- **退款执行**：审批通过后触发退款并通知客户。

## 业务流程

```

客服发起退款 → 系统校验金额 → 主管待审
  → 通过：触发退款 → 退款成功 → 通知客户（覆盖 R1 单级审批规则）
  → 驳回：退回客服，附驳回原因

```markdown

## 异常与边界场景

- **重复提交**：同一订单已有"待审 / 处理中"退款时再次发起 → 拒绝并提示已有进行中退款
- **审批超时**：待审超 48 小时 → 自动升级通知上级主管，不自动通过
- **退款失败**：支付侧退款失败 → 退款单转"失败"，保留可重试，不影响订单其他状态

## 业务对象状态

退款单状态机：`待审` →(通过) `处理中` →(退款成功) `已完成` / `处理中` →(退款失败) `失败` →(重试) `处理中` / `待审` →(驳回) `已驳回` / `待审` →(超时48h) `待审`(升级通知，状态不变)

## 角色与权限矩阵

| 角色 | 发起退款 | 审批退款 | 查看全部退款单 |
|---|---|---|---|
| 客服 | 可 | 不可 | 仅本人发起 |
| 主管 | 不可 | 可 | 可 |

## 验收标准

- [ ] 退款必须经主管审批通过才触发打款（对应 SHOP-REQ-22 §验收 1）
- [ ] 同一订单不允许并发的进行中退款（对应 §验收 3）
- [ ] 待审超 48 小时自动升级通知（对应 §验收 4）

## 权衡与开放问题

- **单级审批 vs 多级审批**（选单级）。多级更严但拖慢退款时效，与"缩短退款时效"目标冲突，本期单级。
- 开放问题：大额退款是否需财务二次确认——待业务方在 D+7 前确认（非阻塞）。
````

---

## 8. Relationship to other assets

- **Paired rule**: [rules/functional-design-quality.md](../rules/functional-design-quality.md) — the functional design quality review checklist across 5 dimensions: completeness, executability, clarity, soundness, traceability
- **Upstream spec**: [requirement-modeling.md](./requirement-modeling.md) — a functional design's `parent` must point at a requirement in `approved` status; business rules are declared on the requirement side and cited here by id
- **Downstream spec**: [technical-design-modeling.md](./technical-design-modeling.md) — only a functional design in `approved` status can derive a technical design, whose `parent` points back at it
- **Related industry standards**: IEEE 1016 (Software Design Description), BPMN, UML state diagrams, and RBAC
- **Recursive basis**: this spec itself follows the 8-section skeleton of [spec-modeling.md](./spec-modeling.md) v2.0.0, skipping §2 mental model — the dimensions a functional design must answer are already carried by the 6-section MECE structure in §5.1
