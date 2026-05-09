---
id: TASK_MODELING_SPEC_V1
name: Task Modeling Schema
description: Spec defining task document fields, table format, status enum, and traceability to design.
version: 1.0.0
status: active
lifecycle: living
created_at: 2026-05-09
scope: |
  Defines the structural contract for task list documents: required task fields, status enum,
  dependency semantics, and frontmatter. Applies to implementation task lists derived from
  approved design documents.
related:
  - ./design-modeling.md
  - ../rules/task-quality.md
---

# 任务建模规范

> **数据契约**：定义任务列表文档的结构与字段
>
> 配套：质量评审见 [rules/task-quality.md](../rules/task-quality.md)；上游设计见 [specs/design-modeling.md](./design-modeling.md)

---

## 适用范围

适用于由设计派生的实施任务列表（`tasks.md` 或同等文件）。不适用于：

- 自由格式的 TODO 清单
- Issue 跟踪系统中的工单（由系统 schema 决定字段）
- Sprint backlog（由 PM 工具决定字段）

---

## 必填字段（每个任务）

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `id` | string | 必 | 任务唯一标识，格式 `T<n>`（如 T1、T2） |
| `title` | string | 必 | 任务标题（≤ 80 字符，含动词） |
| `depends_on` | list[string] | 必 | 依赖任务 ID 列表（无依赖填 `—`） |
| `acceptance` | string | 必 | 验收标准（可测试或可验证） |
| `owner_or_hint` | string | 必 | 受让人（人 / 角色）或 AI 执行 hint |
| `status` | enum | 必 | 见下方状态枚举 |

---

## 状态枚举

| 状态 | 含义 | 谁可改 |
|---|---|---|
| `Todo` | 初始态，等待开始 | 派工 skill 写入 |
| `In Progress` | 正在执行 | runtime / 执行者 |
| `Blocked` | 阻塞中（含原因） | runtime / 执行者 |
| `Done` | 已完成且验收通过 | runtime / 执行者 |
| `Cancelled` | 已取消（含理由） | runtime / 执行者 |

**初始状态规则**：派工 skill 写入时所有任务必须为 `Todo`；其他状态由下游 runtime 或人工维护。

---

## 推荐表格格式

```markdown
| Id | Task | Depends on | Acceptance | Owner / Hint | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| T1 | ... | — | ... | ... | Todo |
| T2 | ... | T1 | ... | ... | Todo |
```

---

## 依赖语义

- 依赖必须**无环**（DAG）
- 多依赖用逗号分隔（`T1, T2`）
- 跨文档依赖以路径前缀标注（`other-tasks.md#T3`）
- 阻塞性依赖（必须先完成）与软依赖（建议先完成）暂不区分；如需可在 `acceptance` 字段说明

---

## 可追溯性

每个任务**至少**映射到设计文档的一节或一条验收标准。映射方式：

- 在任务 `acceptance` 字段中显式引用（如 "实现设计 §3.2 描述的 X"）
- 或在 `owner_or_hint` 中标注源（如 "基于设计 §架构.组件 A"）

---

## Frontmatter 契约

```yaml
---
artifact_type: tasks
lifecycle: living
created_at: YYYY-MM-DD
parent: <path to upstream design document>
---
```

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `artifact_type` | string | 必 | 固定 `tasks` |
| `lifecycle` | enum | 必 | `living`（任务列表持续更新） |
| `created_at` | date | 必 | 任务列表生成日期 |
| `parent` | path | 必 | 上游 design 文档路径 |

---

## 反模式

- ❌ 任务无 `depends_on` 字段（即使无依赖也应填 `—`）
- ❌ 循环依赖（T1 → T2 → T1）
- ❌ 任务粒度模糊（"实施模块 X" 而非具体可完成单元）
- ❌ 无 `acceptance` 字段（无法判断"完成"）
- ❌ 派工时填写非 `Todo` 的状态
- ❌ 无 `parent` frontmatter（孤立任务列表）
- ❌ 任务无可追溯到设计的引用

---

## 关联标准

- **GTD**：每条任务需有明确"下一步行动"（`owner_or_hint` 字段满足此要求）
- **DAG 依赖**：项目管理通用做法，禁止循环依赖
