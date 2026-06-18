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

# 功能设计建模规范

> **数据契约**：定义功能设计文档的字段结构与正文骨架

---

## 1. 定位与适用范围

功能设计文档（functional design document）面向业务 / 产品视角，回答"系统对用户呈现什么行为"——功能模块、业务流程、角色权限、业务对象状态、异常场景。它处在需求与技术设计之间：需求回答"做什么"，功能设计回答"对用户表现成什么样"，技术设计回答"工程上怎么实现"。

本规范以业务行为为中心：不含架构、数据库、API 等工程实现细节（那些归技术设计）；业务规则不在此重新声明，而是用 `覆盖 R<n>` 引用上游需求已声明的规则 id。

适用：

- **新功能**：用户可见的功能模块、业务流程
- **流程变更**：审批 / 订单 / 单据等业务流转的调整
- **权限变更**：角色模型、菜单 / 操作 / 数据权限的调整

不适用：

- 纯技术工作（架构重构、依赖升级、基础设施改造）——由授权 ADR 直接派生技术设计，跳过本层
- 工程实现方案（架构、数据库、接口）——归技术设计文档
- 界面像素级视觉稿——归 UI 设计资产

---

## 3. 命名约定

```
YYYY-MM-DD-<topic>-functional-design.md
```

- `<topic>`：所设计功能的简短描述（kebab-case）
- `YYYY-MM-DD`：设计落地日期（快照制品需时间戳记录方案版本时刻）
- 示例：`2026-05-20-order-refund-functional-design.md`
- 存放位置由项目治理决定（典型：`docs/designs/`）

---

## 4. Frontmatter 契约

```yaml
---
artifact_type: functional-design
lifecycle: snapshot
created_at: YYYY-MM-DD
parent: <path to upstream requirement document>
status: draft | approved | superseded
# 条件字段
superseded_by: <path to new functional design>   # status: superseded 时必填
---
```

### 4.1 字段表

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `artifact_type` | string | 必 | 固定 `functional-design` |
| `lifecycle` | enum | 必 | 固定 `snapshot`（设计是时点决策） |
| `created_at` | date | 必 | 设计完成日期 |
| `parent` | path | 必 | 上游 requirement 文档路径（须 `approved` 状态） |
| `status` | enum | 必 | `draft` / `approved` / `superseded`（语义见 §4.2） |
| `superseded_by` | path | 条件 | `status: superseded` 时必填，指向继任功能设计路径 |

### 4.2 状态机语义

| 状态 | 含义 | 转入条件 |
|---|---|---|
| `draft` | 草稿，尚在评审 | 功能设计首次落地 |
| `approved` | 已批准，可派生技术设计 | 业务 / 产品评审通过，可作为技术设计的 `parent` |
| `superseded` | 被新功能设计替代 | 新功能设计已落地并接管（需填 `superseded_by`） |

---

## 5. 正文结构契约

### 5.1 必填章节（6 节）

按 **What / How-结构 / How-行为 / Why / Verify** 五维 MECE 组织。每份功能设计文档必须包含以下 6 节：

| # | 章节 | 维度 | 用途 | 校验 |
|---|---|---|---|---|
| 1 | 目标（Goal） | What | 陈述本设计要实现的业务能力与成功状态 | ≤ 200 字符；不含技术实现；与上游 requirement 目标一致 |
| 2 | 功能模块与边界（Functional Modules & Boundaries） | How-结构 | 划分功能模块、各模块职责、明确范围内 / 外 | ≥ 1 模块；每模块含名称 + 职责 + 功能边界（做什么 / 不做什么）；模块职责不重叠 |
| 3 | 业务流程（Business Workflow） | How-行为 | 完整业务从开始到结束的端到端流转 | ≥ 1 条主流程，含起点 / 终点 / 关键步骤 / 参与角色；用流程图表达；分支显式标注 |
| 4 | 异常与边界场景（Exception & Edge Scenarios） | How-行为 | 业务异常分支与边界情况的预期行为 | ≥ 2 条；覆盖失败 / 撤回 / 超时 / 重复提交 / 并发中适用者；每条含触发条件 + 预期业务行为（非技术处理） |
| 5 | 验收标准（Acceptance Criteria） | Verify | 业务层面可验证的完成条件 | ≥ 3 条；每条可追溯至上游 requirement 的某条 acceptance；无模糊形容词 |
| 6 | 权衡与开放问题（Trade-offs & Open Questions） | Why | 业务方案的取舍与未决事项 | ≥ 1 组业务取舍含被拒方案的业务代价，或显式写"无重大业务取舍"；只记业务取舍，技术选型取舍归技术设计 |

### 5.2 可选章节

按场景需要添加。条件必备项满足触发条件时**升为必填**：

| 章节 | 类型 | 触发场景 |
|---|---|---|
| 业务对象状态（Business Object States） | 条件必备 | 业务对象（订单 / 任务 / 审批 / 单据等）有 ≥ 3 状态且转换由业务规则驱动——升为必填，用状态图 / 状态表声明 |
| 角色与权限矩阵（Roles & Permission Matrix） | 条件必备 | 涉及 ≥ 2 个角色，或存在差异化的菜单 / 操作 / 数据权限——升为必填，用角色 × 权限矩阵声明 |
| 范围定义（Scope） | 可选 | 跨系统 / 跨团队，业务边界易误读 |
| UI 与交互流程（UI & Interaction Flow） | 可选 | 有面向用户的界面交互需描述 |
| 关联文档（References） | 可选 | 引用上游 requirement / 法规 / 业务流程规范 |

### 5.3 格式细节

#### 5.3.1 业务对象状态的声明形式（升为必填时）

- 用状态图或状态表声明，不写过程式步骤。
- 每个状态含名称 + 进入条件；每条转换含触发事件 + 源状态 + 目标状态。
- 覆盖终态（完成 / 取消 / 关闭）与异常态（超时 / 撤回）。

#### 5.3.2 权限矩阵的声明形式（升为必填时）

- 行 = 角色，列 = 菜单权限 / 操作权限 / 数据权限三类。
- 每个单元格明确"可 / 不可 / 条件可"；条件可须注明条件。

#### 5.3.3 业务规则的引用

业务规则归上游 requirement 声明。功能设计在业务流程与异常场景节用 `覆盖 R<n>` 回引规则 id，不在本文档重新声明，避免需求 / 功能设计 / 技术设计三处重复。

---

## 6. 反模式

- ❌ 缺 frontmatter 必填字段（artifact_type / lifecycle / created_at / parent / status）
- ❌ 含架构 / 数据库 / API 等技术实现细节（归技术设计）
- ❌ 功能模块用大段散文描述而非结构化职责 + 边界
- ❌ 业务流程缺起点 / 终点或不画流程图
- ❌ 异常与边界场景 < 2 条，或只列异常不写预期业务行为
- ❌ 业务对象有 ≥ 3 状态却不画状态图（满足升必填条件但缺状态节）
- ❌ 涉及多角色却无权限矩阵（满足升必填条件但缺权限节）
- ❌ 在本文档重新声明业务规则而非用 `覆盖 R<n>` 引用上游需求
- ❌ 验收标准 < 3 条，或无法追溯至上游 requirement
- ❌ 权衡分析混入技术选型取舍（应归技术设计）
- ❌ 无 `parent` frontmatter（孤立设计，无可追溯性）
- ❌ `superseded` 状态未填 `superseded_by`

---

## 7. 示例

### 7.1 紧凑骨架示例：订单退款审批功能设计

每节用 1-3 句展示骨架，实际功能设计每节应展开为完整内容。

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
```

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

## 8. 与其他资产关系

- **配套 rule**：[rules/functional-design-quality.md](../rules/functional-design-quality.md)——功能设计质量评审清单（5 维：完整性 / 可执行性 / 清晰性 / 合理性 / 可追溯性）
- **上游 spec**：[requirement-modeling.md](./requirement-modeling.md)——功能设计的 `parent` 必须指向 `approved` 状态的 requirement；业务规则在需求侧声明，本层引用其 id
- **下游 spec**：[technical-design-modeling.md](./technical-design-modeling.md)——`approved` 状态的功能设计才能派生技术设计；技术设计的 `parent` 指向功能设计
- **相关行业标准**：IEEE 1016（Software Design Description）、BPMN（业务流程建模）、UML 状态图、RBAC（角色权限模型）
- **递归基础**：本 spec 自身遵循 [spec-modeling.md](./spec-modeling.md) v2.0.0 的 8 节骨架；跳过 §2 心智模型（功能设计的必答维度已落在 §5.1 的 6 节 MECE 结构中）
