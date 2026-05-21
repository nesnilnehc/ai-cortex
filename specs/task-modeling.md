---
id: TASK_MODELING_SPEC_V2
name: Task Modeling Schema
description: Spec defining task list document fields, table format, task status state machine, dependency semantics, and traceability to design.
version: 2.0.0
status: active
lifecycle: living
created_at: 2026-05-09
scope: |
  Defines the structural contract for task list documents: required task fields, status enum,
  dependency semantics, and frontmatter. Applies to implementation task lists derived from
  approved design documents.
related:
  - ./spec-modeling.md
  - ./design-modeling.md
  - ../rules/task-quality.md
---

# 任务建模规范

> **数据契约**：定义任务列表文档（`tasks.md`）的字段结构与表格格式

---

## 1. 定位与适用范围

任务列表（task list）是从设计派生的实施工单清单——把"设计中的每个组件 / 接口 / 流程"映射为可独立完成的具体任务，便于派工与追踪。

适用：

- 由设计文档派生的实施任务列表（`tasks.md` 或同等文件）
- 任务粒度：单次专注会话可完成（通常 ≤ 1 天）

不适用：

- 自由格式的 TODO 清单
- Issue 跟踪系统中的工单（由系统 schema 决定字段）
- Sprint backlog（由 PM 工具决定字段）
- 长跨度的史诗或主题（应拆分为多份任务列表或单独建模）

---

## 3. 命名约定

```
tasks.md
```

- 默认名 `tasks.md`，与上游 design 文档同目录或邻近目录
- 单一 design 派生多份任务列表时，可用 `<scope>-tasks.md`（如 `migration-tasks.md`、`refactor-tasks.md`）

---

## 4. Frontmatter 契约

```yaml
---
artifact_type: tasks
lifecycle: living
created_at: YYYY-MM-DD
parent: <path to upstream design document>
status: draft | active | superseded
# 条件字段
superseded_by: <path to new tasks document>   # status: superseded 时必填
---
```

### 4.1 字段表

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `artifact_type` | string | 必 | 固定 `tasks` |
| `lifecycle` | enum | 必 | 固定 `living`（任务列表持续更新） |
| `created_at` | date | 必 | 任务列表生成日期 |
| `parent` | path | 必 | 上游 design 文档路径（可追溯性） |
| `status` | enum | 必 | `draft` / `active` / `superseded`（语义见 §4.2） |
| `superseded_by` | path | 条件 | `status: superseded` 时必填，指向继任任务列表路径 |

注：文件级 `status` 表达任务列表自身的生命周期；任务**行**的 `status` 字段有独立状态机，定义在 §5.3——两者粒度不同。

### 4.2 状态机语义

文件级 `status` 的 3 值枚举：

| 状态 | 含义 | 转入条件 |
|---|---|---|
| `draft` | 任务列表起草中 | 任务定义中，尚未派工 |
| `active` | 已派工，任务在执行 | 派工完成，列表进入实施期（任务行 status 全为 `Todo`） |
| `superseded` | 被新任务列表替代 | 因设计变更等原因重新拆解，旧列表整体作废（需填 `superseded_by`） |

**不引入 `completed` 状态**：任务列表是否全部完成可从任务行 `status` 推断（全为 `Done` / `Cancelled`），不必文件级单独标注。

---

## 5. 正文结构契约

### 5.1 任务行的必填字段

每条任务必须包含以下 6 个字段：

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `id` | string | 必 | 任务唯一标识。建议 `T<n>`（如 `T1`、`T2`）；项目有自身惯例时（如 `AUTH-T1`、`TASK-001`）可保留，但同一文件内格式必须一致 |
| `title` | string | 必 | 任务标题（≤ 80 字符，含动词，避免"实施 X"等模糊描述） |
| `depends_on` | list[string] | 必 | 依赖任务 ID 列表（无依赖填 `—`） |
| `acceptance` | string | 必 | 验收标准（可测试或可验证） |
| `owner_or_hint` | string | 必 | 受让人（人 / 角色）或 AI 执行 hint |
| `status` | enum | 必 | 见 §5.3 任务行状态机 |

### 5.2 推荐表格格式

```markdown
| Id | Task | Depends on | Acceptance | Owner / Hint | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| T1 | ... | — | ... | ... | Todo |
| T2 | ... | T1 | ... | ... | Todo |
```

### 5.3 任务行状态机

任务**行**的 `status` 字段状态枚举（与文件级 `status` 粒度不同）：

| 状态 | 含义 | 转入条件 |
|---|---|---|
| `Todo` | 初始态，等待开始 | 派工时统一写入 |
| `In Progress` | 正在执行 | 执行者认领并开始工作 |
| `Blocked` | 阻塞中 | 依赖未达 / 外部阻塞（**必须**在邻近列注明原因） |
| `Done` | 已完成且验收通过 | 验收标准全部满足 |
| `Cancelled` | 已取消 | 范围调整或需求废弃（**必须**注明理由） |

**初始状态规则**：派工 skill 写入时所有任务必须为 `Todo`；其他状态由下游 runtime 或人工维护。

### 5.4 依赖语义

- 依赖必须**无环**（DAG）
- 多依赖用逗号分隔（`T1, T2`）
- 跨文档依赖以路径前缀标注（如 `other-tasks.md#T3`）
- 阻塞性依赖（必须先完成）与软依赖（建议先完成）暂不区分；如需可在 `acceptance` 字段说明

### 5.5 可追溯性

每个任务**至少**映射到上游设计文档的一节或一条验收标准。映射方式：

- 在任务 `acceptance` 字段中显式引用（如 "实现设计 §3.2 描述的 X"）
- 或在 `owner_or_hint` 中标注源（如 "基于设计 §架构.组件 A"）

---

## 6. 反模式

- ❌ 任务无 `depends_on` 字段（即使无依赖也应填 `—`）
- ❌ 循环依赖（`T1 → T2 → T1`）
- ❌ 任务粒度模糊（"实施模块 X" 而非具体可完成单元）
- ❌ 无 `acceptance` 字段（无法判断"完成"）
- ❌ 派工时填写非 `Todo` 的状态
- ❌ 无 `parent` frontmatter（孤立任务列表，无可追溯性）
- ❌ 缺 `status` frontmatter 字段（无法识别列表生命周期阶段）
- ❌ 任务无可追溯到设计的引用
- ❌ 多依赖用分号 / 空格分隔而非逗号（破坏依赖图解析）
- ❌ `Blocked` 或 `Cancelled` 状态未注明理由
- ❌ 同一文件内任务 id 格式混用（如 `T1` 与 `TASK-002` 同存）

---

## 7. 示例

### 7.1 最小合规 tasks.md：数据导出功能实施

````markdown
---
artifact_type: tasks
lifecycle: living
created_at: 2026-05-15
parent: ../designs/data-export-design.md
status: active
---

# 任务：数据导出功能实施

| Id | Task | Depends on | Acceptance | Owner / Hint | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| T1 | 定义导出任务表 schema | — | migration 通过；含 status / progress / file_url 字段（设计 §数据模型） | backend | Todo |
| T2 | 实现 CSV 序列化器 | — | 单元测试覆盖空集 / 大字段 / 特殊字符（设计 §组件 Serializer） | backend | Todo |
| T3 | 实现导出任务队列消费者 | T1, T2 | 集成测试通过；含失败重试 3 次（设计 §数据流） | backend | Todo |
| T4 | 实现 POST /exports 触发接口 | T1 | OpenAPI 文档；幂等键测试（设计 §接口契约） | backend | Todo |
| T5 | 实现 GET /exports/:id 查询接口 | T1 | 返回 status + progress + 下载 URL（若 Done）（设计 §接口契约） | backend | Todo |
| T6 | 大文件分片上传到对象存储 | T3 | 10GB 测试文件可成功导出（设计 §错误处理 OOM 路径） | backend | Todo |
| T7 | 前端导出按钮 + 进度轮询 | T4, T5 | UI 显示进度条；完成后弹下载链接（设计 §UI） | frontend | Todo |
````

---

## 8. 与其他资产关系

- **配套 rule**：[rules/task-quality.md](../rules/task-quality.md)——任务列表质量评审清单（字段完整性 / 依赖图正确性 / 可执行性 / 可追溯性）
- **上游 spec**：[design-modeling.md](./design-modeling.md)——任务列表的 `parent` 应指向 `approved` 状态的设计文档
- **相关实践**：GTD（每条任务需有明确"下一步行动"，对应 `owner_or_hint` 字段）；DAG 依赖（禁止循环依赖）
- **递归基础**：本 spec 自身遵循 [spec-modeling.md](./spec-modeling.md) v2.0.0 的 8 节骨架；跳过 §2 心智模型（任务无显著 N 问框架，6 字段表本身即必答维度）
