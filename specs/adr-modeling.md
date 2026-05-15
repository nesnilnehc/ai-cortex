---
id: ADR_MODELING_SPEC_V1
name: ADR Modeling Schema
description: Spec defining the ADR document data contract — frontmatter field constraints, status 5-value enum, decay-related conditional fields, and required 4-section body structure.
version: 1.0.0
status: active
lifecycle: living
created_at: 2026-05-15
scope: |
  Defines the structural contract for Architecture Decision Records (ADRs): required frontmatter
  fields, status state machine, conditional fields for archived/superseded states, and the
  mandatory 4-section body structure. Applies to all ADRs under docs/adr/.
related:
  - ../rules/adr-management.md
  - ../docs/ARTIFACT_NORMS.md
---

# ADR 建模规范

> **数据契约**：定义 ADR 文档的结构与字段
>
> 配套：写作纪律见 [rules/adr-management.md](../rules/adr-management.md)

---

## ADR 回答的四个核心问题

每篇 ADR 必须清晰回答以下四个问题：

| 问题 | 描述 |
|---|---|
| **What** | 我们做了什么决定？（一句话陈述） |
| **Why** | 为什么这样决定？（上下文、驱动力、约束） |
| **Alternatives** | 考虑过哪些替代方案？为什么不选？（含被拒方案与理由） |
| **Consequences** | 会带来什么后果？（含正面、负面、未知风险） |

后续字段约束与正文结构均围绕回答这四个问题展开。

---

## 适用范围

适用于 `docs/adr/` 目录下的所有 Architecture Decision Record。

---

## 路径与命名约定

```
docs/adr/NNNN-{slug}.md
```

- **编号**：4 位顺序号，从 `0001` 起，单调递增，不复用
- **slug**：小写横线分隔的简短描述性名称（3-6 词）
- **目录**：固定在 `docs/adr/`，不嵌套子目录
- **新编号**：取当前最大编号 + 1；可在 `docs/adr/README.md` 索引中找到最新编号

---

## Frontmatter 契约

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

### 字段约束

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `artifact_type` | string | 必 | 固定 `adr` |
| `created_by` | string | 必 | 固定 `decision-record` |
| `lifecycle` | enum | 必 | 固定 `snapshot`（ADR 是时点决策） |
| `created_at` | date | 必 | 决策日期（`YYYY-MM-DD`） |
| `status` | enum | 必 | 5 值枚举（见下方状态机） |
| `description` | string | 必 | 一句话摘要，补充 H1 标题 |
| `superseded_by` | string | 条件 | `status: superseded` 时必填，值为替代 ADR 编号（`NNNN-{slug}`） |
| `archived_at` | date | 条件 | `status: archived` 时必填 |
| `archived_reason` | string | 条件 | `status: archived` 时必填 |
| `expires_at` | date | 可选 | 复核提醒日期；超过该日期未复核则触发衰减评估 |

### Status 状态机

| 状态值 | 含义 |
|---|---|
| `proposed` | 已提出，待决策 |
| `accepted` | 已采纳，当前有效 |
| `superseded` | 被另一篇 ADR 替代（需填 `superseded_by`） |
| `archived` | 已归档，不再活跃（需填 `archived_at` + `archived_reason`） |
| `rejected` | 已明确拒绝，保留作决策历史 |

**禁止使用的旧枚举值**：`draft` / `active` / `approved` / `已批准` / `live`

---

## 正文必填结构（4 节）

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

**校验**：

- 4 节缺一不可（`背景` / `决策` / `替代方案` / `后果`）
- `替代方案` 节至少含 1 个被拒方案（新建 ADR 时须说明为何不选其他路径）
- `后果` 节须含正面与负面（或中性）两类

---

## Frontmatter 示例

```yaml
---
artifact_type: adr
created_by: decision-record
lifecycle: snapshot
created_at: 2026-05-15
status: accepted
description: 采用 4 位顺序编号替代 3 位编号，与 MADR/adr-tools 行业惯例对齐
---
```

---

## 反模式

- ❌ `status:` 在 frontmatter 以外额外用 `**状态**：` 行重复（双写违规）
- ❌ 使用 `active` / `draft` / `approved` 等旧枚举值
- ❌ `superseded` 状态未填 `superseded_by`
- ❌ `archived` 状态未填 `archived_at` 与 `archived_reason`
- ❌ 缺少 `description` 字段
- ❌ 正文缺少 4 节中的任一节
- ❌ `替代方案` 节为空（必须解释为何不选其他路径）
- ❌ 文件名编号少于 4 位（`001-` 而非 `0001-`）
