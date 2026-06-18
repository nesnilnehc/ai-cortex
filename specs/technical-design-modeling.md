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

# 技术设计建模规范

> **数据契约**：定义技术设计文档的字段结构与正文骨架

---

## 1. 定位与适用范围

技术设计文档（technical design document）面向工程视角，回答"工程上怎么实现"——架构、服务拆分、组件与详细设计、数据库、接口契约、错误处理、技术选型。它是从上游设计到任务列表之间的桥梁，是任务列表的直接来源。

技术设计**始终存在**于派生任务之前（可因纯流程变更而从简，但不省略）。功能层可被跳过——纯技术工作（重构 / 基建 / 依赖升级）由授权它的 ADR 直接派生技术设计。

适用：

- **架构设计**：系统层、服务层、模块层架构与服务拆分
- **组件 / 详细设计**：类、方法、接口的签名级定义
- **数据与集成设计**：数据库设计、API 契约、跨服务集成
- **纯技术工作**：架构重构、依赖升级、基础设施改造（无功能层，`parent` 指向授权 ADR）

不适用：

- 代码层级的具体实现（应写在代码注释或 ADR）
- 单一函数 / 类的局部设计（直接写在 PR 描述）
- 业务流程 / 角色权限 / 业务对象状态（归功能设计文档）
- 探索性原型方案（应写为 `experiments/` 或 ADR 候选）

---

## 3. 命名约定

```
YYYY-MM-DD-<topic>-technical-design.md
```

- `<topic>`：所设计对象的简短描述（kebab-case）
- `YYYY-MM-DD`：设计落地日期（快照制品需时间戳记录方案版本时刻）
- 示例：`2026-05-22-order-refund-technical-design.md`
- 存放位置由项目治理决定（典型：`docs/designs/`）

---

## 4. Frontmatter 契约

```yaml
---
artifact_type: technical-design
lifecycle: snapshot
created_at: YYYY-MM-DD
parent: <path to upstream functional-design OR requirement>
status: draft | approved | superseded
# 条件字段
superseded_by: <path to new technical design>   # status: superseded 时必填
---
```

### 4.1 字段表

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `artifact_type` | string | 必 | 固定 `technical-design` |
| `lifecycle` | enum | 必 | 固定 `snapshot`（设计是时点决策） |
| `created_at` | date | 必 | 设计完成日期 |
| `parent` | path | 必 | **多态**：常态指向上游 `functional-design`；非功能需求可跳过功能层指向 `requirement`；纯技术工作（无对应需求）指向授权它的 `adr`。校验 `parent` 的 `artifact_type ∈ {functional-design, requirement, adr}` |
| `status` | enum | 必 | `draft` / `approved` / `superseded`（语义见 §4.2） |
| `superseded_by` | path | 条件 | `status: superseded` 时必填，指向继任技术设计路径 |

### 4.2 状态机语义

| 状态 | 含义 | 转入条件 |
|---|---|---|
| `draft` | 草稿，尚在评审 | 技术设计首次落地 |
| `approved` | 已批准，可派生任务 | 工程评审通过，可作为任务列表的 `parent` |
| `superseded` | 被新技术设计替代 | 新技术设计已落地并接管（需填 `superseded_by`） |

---

## 5. 正文结构契约

### 5.1 必填章节（9 节）

按 **What / How-结构 / How-行为 / Why / Verify** 五维 MECE 组织。每份技术设计文档必须包含以下 9 节：

| # | 章节 | 维度 | 用途 | 校验 |
|---|---|---|---|---|
| 1 | 目标（Goal） | What | 陈述本技术设计要实现的范围与成功状态 | ≤ 200 字符；与上游 functional-design（或 requirement）一致 |
| 2 | 架构与服务拆分（Architecture & Service Decomposition） | How-结构 | 系统 / 服务 / 模块层次、边界、服务拆分 | 含 ≥ 1 种结构化表达（图 / 表）；标注外部与内部依赖；多服务时画拆分边界 |
| 3 | 组件与详细设计（Components & Detailed Design） | How-结构 | 关键组件职责 + 类 / 方法 / 接口定义，指导开发实现 | ≥ 1 组件，每个含职责 + 依赖；关键类 / 方法 / 接口含签名级定义 |
| 4 | 数据库设计（Database Design） | How-结构 | 表结构 / 字段 / 索引 / 关系 / 初始化数据 + 迁移 | 实体含字段 / 类型 / 约束 / 关系；关键索引标注；含初始化数据与迁移方案；**无变更时写"无数据库变更"，不留空** |
| 5 | 接口契约（API Contracts） | How-结构 | 对外接口：路径 / 方法 / 请求参数 / 响应结构 / 错误码 / 鉴权方式 | 每接口含路径 + 方法 + 入参 + 出参 + 错误码 + 鉴权；事件含 topic + payload schema；**无变更时写"无接口变更"** |
| 6 | 数据流与错误处理（Data Flow & Error Handling） | How-行为 | 数据在组件 / 服务间的流动 + 技术失败路径与处理 | 关键路径数据流标注；≥ 2 条技术失败路径，每条含失败条件 + 检测方式 + 恢复策略 |
| 7 | 技术选型与权衡（Tech Choices & Trade-offs） | Why | 技术选型决策 + 替代方案 + 依赖与风险 | ≥ 2 种替代方案，每种含优点 / 缺点 / 是否选用 + 理由；显式列依赖与风险 |
| 8 | 测试策略（Test Strategy） | Verify | 声明验证方法（**不写测试代码**） | 含测试层次（单元 / 集成 / 端到端）；含验收方式（自动化 / 人工） |
| 9 | 验收标准（Acceptance Criteria） | Verify | 技术设计完成的可验证条件 | ≥ 3 条；每条可追溯至上游 functional-design 的某条 acceptance；功能层被跳过（`parent` 直指 requirement）时追溯至 requirement 的某条 acceptance |

### 5.2 可选章节

按场景需要添加。条件必备项满足触发条件时**升为必填**：

| 章节 | 类型 | 触发场景 |
|---|---|---|
| 数据迁移详案（Migration Plan） | 条件必备 | 涉及破坏性 schema 变更 / 数据回填 / 不可回滚操作——升为必填，含回滚策略（否则迁移内联于 §4） |
| 部署与运维（Deployment & Operations） | 可选 | 含部署变更、扩缩容策略、配置管理 |
| 横切关注点（Cross-cutting Concerns） | 可选 | 安全 / 性能 / 可观测性有专门设计 |
| 作业调度（Scheduling） | 可选 | 含定时任务 / 后台 job / 队列消费者 |
| 范围定义（Scope） | 可选 | 跨服务 / 跨团队集成边界易误读 |
| 关联文档（References） | 可选 | 引用 ADR / 外部规范 / 上游设计 |

### 5.3 格式细节

#### 5.3.1 验收标准的追溯目标随 `parent` 类型而定

- `parent` 为 `functional-design`（常态）：每条验收追溯至功能设计的某条 acceptance（`覆盖 FD §验收 N`）。
- `parent` 为 `requirement`（功能层被跳过）：每条验收追溯至 requirement 的某条 acceptance。

#### 5.3.2 "无变更"逃生阀

§4 数据库设计、§5 接口契约对纯流程类设计可能不涉及变更。此时必须显式写"无数据库变更" / "无接口变更"作为正向断言，**不得留空**——留空无法区分"遗漏"与"确实无变更"。

---

## 6. 反模式

- ❌ 缺 frontmatter 必填字段（artifact_type / lifecycle / created_at / parent / status）
- ❌ `parent` 的 artifact_type 不在 {functional-design, requirement}（链条断裂）
- ❌ 含代码或脚手架（设计不写实现，实现在代码层）
- ❌ 含业务流程 / 角色权限 / 业务对象状态（归功能设计）
- ❌ 组件节用大段散文描述而非结构化职责 + 签名级定义
- ❌ 数据模型只列实体名不含字段 / 类型 / 关系（无法据此实施）
- ❌ 接口契约只写"有一个 API"不列方法 / 入参 / 出参 / 错误码（无法据此对接）
- ❌ §4 / §5 不涉及变更时留空而非写"无变更"（遗漏与 N/A 不可区分）
- ❌ 单一方案不做权衡（缺 §7 替代方案）
- ❌ 权衡分析只列被选方案的优点（必须含被拒方案的缺点）
- ❌ 测试策略写测试代码而非验证方法
- ❌ 验收标准 < 3 条，或追溯目标与 `parent` 类型不符
- ❌ 无 `parent` frontmatter（孤立设计，无可追溯性）
- ❌ `superseded` 状态未填 `superseded_by`

---

## 7. 示例

### 7.1 紧凑骨架示例：订单退款审批技术设计

每节用 1-3 句展示骨架，实际技术设计每节应展开为完整内容。

````markdown
---
artifact_type: technical-design
lifecycle: snapshot
created_at: 2026-05-22
parent: ../designs/2026-05-20-order-refund-functional-design.md
status: approved
---

# 技术设计：订单退款审批

## 目标

实现退款单的发起 / 审批 / 执行流程，集成支付侧退款 API，支撑功能设计的单级审批与超时升级。

## 架构与服务拆分

```
[客服端/主管端] → [Order Service] → [Refund Module] → [Payment Gateway (外部)]
                                          ↓
                                    [Notification Service]
```

外部依赖：Payment Gateway（退款 API）。内部依赖：Order Service、Notification Service。本期不拆独立 Refund Service，作为 Order Service 模块。

## 组件与详细设计

- **RefundService**：`initiate(orderId, amount, reason)` / `approve(refundId, approverId)` / `reject(refundId, reason)`。职责：状态流转、并发控制。
- **RefundExecutor**：`execute(refundId)` 调用 Payment Gateway，失败重试。职责：幂等退款。

## 数据库设计

```
refund_order
  id: UUID PK
  order_id: UUID FK -> order.id (index)
  amount: decimal NOT NULL
  status: enum NOT NULL (待审/处理中/已完成/失败/已驳回)
  approver_id: UUID NULL
  created_at: timestamp NOT NULL
```

约束：(order_id) 部分唯一索引 WHERE status IN ('待审','处理中')——保证同订单无并发进行中退款。迁移：新增表，无数据回填。

## 接口契约

- `POST /refunds` — body `{order_id, amount, reason}` → 201 `{refund_id, status}` / 409 `DUPLICATE_ACTIVE_REFUND` / 422 `AMOUNT_EXCEEDS_REFUNDABLE`；鉴权：客服角色
- `POST /refunds/{id}/approve` → 200 `{status}` / 403 `NOT_APPROVER`；鉴权：主管角色
- 事件：`REFUND_APPROVED` / `REFUND_FAILED`（payload schema 见 nats-messaging spec）

## 数据流与错误处理

退款执行：approve → 写 status=处理中 → RefundExecutor 调用 Payment Gateway → 成功写 已完成 + 发 REFUND_APPROVED / 失败写 失败 + 发 REFUND_FAILED。

- **支付网关超时**：标记失败，保留可重试；不阻塞订单其他操作
- **并发审批**：approve 用乐观锁（status 版本），第二次审批返回 409

## 技术选型与权衡

- **方案 A：唯一部分索引防并发退款**（选用）。优点：DB 层强保证。缺点：依赖 PostgreSQL 部分索引。
- **方案 B：应用层分布式锁**（拒）。优点：DB 无关。缺点：锁失效边界复杂，弱于 DB 约束。
- 依赖与风险：Payment Gateway 退款 API 限流 10 QPS，高峰需排队。

## 测试策略

- 单元：状态流转、金额校验、幂等执行
- 集成：完整发起 / 审批 / 退款链路（mock Payment Gateway）
- 验证方式：CI 自动跑单元 + 集成

## 验收标准

- [ ] 同订单并发退款被 DB 约束拒绝（覆盖 FD §验收 2）
- [ ] 退款失败可重试且不影响订单状态（覆盖 FD §验收 1）
- [ ] 审批鉴权：仅主管角色可 approve（覆盖 FD §权限矩阵）
````

---

## 8. 与其他资产关系

- **配套 rule**：[rules/technical-design-quality.md](../rules/technical-design-quality.md)——技术设计质量评审清单（5 维：完整性 / 可执行性 / 清晰性 / 合理性 / 可追溯性）
- **上游 spec**：[functional-design-modeling.md](./functional-design-modeling.md)（常态）——技术设计的 `parent` 指向 `approved` 功能设计；[requirement-modeling.md](./requirement-modeling.md)——非功能需求跳过功能层时直接指向 `approved` requirement；纯技术工作（无对应需求）的 `parent` 指向授权它的 ADR
- **下游 spec**：[task-modeling.md](./task-modeling.md)——任务列表的 `parent` 指向 `approved` 状态的技术设计
- **相关行业标准**：IEEE 1016（Software Design Description）、C4 Model、arc42 模板、Google Design Doc 实践
- **递归基础**：本 spec 自身遵循 [spec-modeling.md](./spec-modeling.md) v2.0.0 的 8 节骨架；跳过 §2 心智模型（技术设计的必答维度已落在 §5.1 的 9 节 MECE 结构中）
