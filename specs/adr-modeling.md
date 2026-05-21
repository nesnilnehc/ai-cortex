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

# ADR 建模规范

> **数据契约**：定义 Architecture Decision Record（ADR）文档的字段结构与正文骨架

---

## 1. 定位与适用范围

ADR（Architecture Decision Record）是记录架构决策的时点快照——为什么做这个决定、当时考虑过什么替代、可能带来什么后果。一个组织通过堆积 ADR 形成长期决策记录，让后来者能追溯并理解既有架构的成因。

适用：

- 所有需要长期保留 why 的架构 / 技术 / 设计决策
- 影响多人、跨服务、影响长期结构的决策

不适用：

- 日常 bug fix 或小功能改动（用 commit message 即可）
- 单纯的规范性约束（应写 rule，而非"我们决定遵守规范"）
- 已有 ADR 的局部细化（追加到原 ADR 即可）

ADR 准入门槛与衰减政策由 [rules/adr-management.md](../rules/adr-management.md) 定义；本 spec 只规范数据结构。

---

## 2. 心智模型（Mental Model）

> 一份合格 ADR 必须能清晰回答的四个核心问题。

| 问题 | 描述 |
|---|---|
| **What** | 我们做了什么决定？（一句话陈述） |
| **Why** | 为什么这样决定？（上下文、驱动力、约束） |
| **Alternatives** | 考虑过哪些替代方案？为什么不选？（含被拒方案与理由） |
| **Consequences** | 会带来什么后果？（含正面、负面、未知风险） |

§5 正文结构契约的 4 节（背景 / 决策 / 替代方案 / 后果）一一对应这四个问题。

---

## 3. 命名约定

```
NNNN-{slug}.md
```

- **编号**：4 位顺序号，从 `0001` 起，单调递增，**不复用**
- **slug**：小写横线分隔的简短描述性名称（3-6 词）
- **新编号取法**：取当前最大编号 + 1（编号唯一性依赖 ADR 文档统一存放位置，由项目治理决定）

---

## 4. Frontmatter 契约

```yaml
---
artifact_type: adr
created_by: decision-record
lifecycle: snapshot
created_at: YYYY-MM-DD
status: proposed | accepted | superseded | archived | rejected
description: <一句话 ADR 摘要，与 H1 标题互补>
# 条件字段（按 status 必填）
superseded_by: NNNN-{slug}       # status: superseded 时必填
archived_at: YYYY-MM-DD           # status: archived 时必填
archived_reason: <原因一句话>    # status: archived 时必填
expires_at: YYYY-MM-DD            # 可选；季度复核触发器
---
```

### 4.1 字段表

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `artifact_type` | string | 必 | 固定 `adr` |
| `created_by` | string | 必 | 固定 `decision-record` |
| `lifecycle` | enum | 必 | 固定 `snapshot`（ADR 是时点决策） |
| `created_at` | date | 必 | 决策日期（`YYYY-MM-DD`） |
| `status` | enum | 必 | 5 值枚举（语义见 §4.2） |
| `description` | string | 必 | 一句话摘要，补充 H1 标题 |
| `superseded_by` | string | 条件 | `status: superseded` 时必填，值为替代 ADR 编号（`NNNN-{slug}`） |
| `archived_at` | date | 条件 | `status: archived` 时必填 |
| `archived_reason` | string | 条件 | `status: archived` 时必填 |
| `expires_at` | date | 可选 | 复核提醒日期；超过该日期未复核则触发衰减评估 |

### 4.2 状态机语义

| 状态值 | 含义 | 转入条件 |
|---|---|---|
| `proposed` | 已提出，待决策 | ADR 首次落地，尚未通过评审 |
| `accepted` | 已采纳，当前有效 | 决策已批准并实施 |
| `superseded` | 被另一篇 ADR 替代 | 新 ADR 落地并接管该决策（需填 `superseded_by`） |
| `archived` | 已归档，不再活跃 | 决策不再影响当前系统（需填 `archived_at` + `archived_reason`） |
| `rejected` | 已明确拒绝，保留作决策历史 | 评审决定不采纳，保留作为"被拒方案"的记录 |

**禁止使用的旧枚举值**：`draft` / `active` / `approved` / `已批准` / `live`

---

## 5. 正文结构契约

### 5.1 4 节必填结构

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

### 5.2 内容校验

- 4 节缺一不可（`背景` / `决策` / `替代方案` / `后果`）
- `替代方案` 节至少含 1 个被拒方案（新建 ADR 时须说明为何不选其他路径）
- `后果` 节须含正面与负面（或中性）两类

---

## 6. 反模式

- ❌ `status` 在 frontmatter 以外额外用 `**状态**：` 行重复（双写违规）
- ❌ 使用 `active` / `draft` / `approved` / `已批准` / `live` 等旧枚举值
- ❌ `superseded` 状态未填 `superseded_by`
- ❌ `archived` 状态未填 `archived_at` 与 `archived_reason`
- ❌ 缺少 `description` 字段
- ❌ 正文缺少 4 节中的任一节
- ❌ `替代方案` 节为空（必须解释为何不选其他路径）
- ❌ 文件名编号少于 4 位（`001-` 而非 `0001-`）
- ❌ 文件名编号复用（已弃用编号不可重新分配）

---

## 7. 示例

### 7.1 完整合规 ADR

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

### 7.2 superseded 状态示例

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

## 8. 与其他资产关系

- **配套 rule**：[rules/adr-management.md](../rules/adr-management.md)——ADR 写作纪律（准入门槛、状态执行、衰减政策、与 decisions 边界）

### 8.1 衰减阈值

| 触发条件 | 动作 |
|---|---|
| `accepted` 且距 `created_at` ≥ 12 个月 且 近 12 个月无文档引用 且 决策已不影响系统 | 转 `archived`，填 `archived_at` + `archived_reason` |
| `archived` 且距 `archived_at` ≥ 6 个月 且 无任何文件引用 | 可执行 `git rm` 物理删除 |
| `rejected` / `superseded` / 被其他 ADR 的 `superseded_by` 字段引用 | **永不物理删除**（决策历史与替代脉络是组织记忆） |

### 8.2 与 rule 的边界

本 spec 只规范数据结构（字段、状态机、必填关系）；具体的写作纪律（如何判断 ADR 准入、如何执行状态转换、如何执行 `git rm` 衰减）由 [rules/adr-management.md](../rules/adr-management.md) 承担。两者并行生效。

### 8.3 递归基础

本 spec 自身遵循 [spec-modeling.md](./spec-modeling.md) v2.0.0 的 8 节骨架；所有条件必备章节（§2 / §3 / §4 / §4.2）均触发——ADR 是完整骨架样板。
