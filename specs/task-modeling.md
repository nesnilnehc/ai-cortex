---
id: TASK_MODELING_SPEC_V2
name: Task Modeling Schema
description: Spec defining task list document fields, table format, task status state machine, dependency semantics, and traceability to technical-design.
version: 2.1.0
status: active
lifecycle: living
created_at: 2026-05-09
scope: |
  Defines the structural contract for task list documents: required task fields, status enum,
  dependency semantics, and frontmatter. Applies to implementation task lists derived from
  approved technical-design documents.
related:
  - ./spec-modeling.md
  - ./technical-design-modeling.md
  - ../rules/task-quality.md
---

# Task Modeling Schema

> **Data contract**: defines the field structure and table format of a task list document (`tasks.md`)

---

## 1. Position and scope

A task list is the set of implementation work items derived from a technical design. It maps each component, interface and flow in that design onto a concrete task that can be completed independently, so work can be assigned and tracked.

In scope:

- An implementation task list derived from a technical design document (`tasks.md` or an equivalent file)
- Task granularity: completable in one focused session, typically ≤ 1 day

Out of scope:

- A free-form TODO list
- Work items in an issue tracker, whose fields the tracker's own schema decides
- A sprint backlog, whose fields the PM tool decides
- A long-running epic or theme, which is split into several task lists or modelled separately

---

## 3. Naming

```text
tasks.md
```

- The default name is `tasks.md`, in the same directory as the upstream technical-design document or one nearby
- Where one technical design yields several task lists, use `<scope>-tasks.md` such as `migration-tasks.md` or `refactor-tasks.md`

---

## 4. Frontmatter contract

```yaml
---
artifact_type: tasks
lifecycle: living
created_at: YYYY-MM-DD
parent: <path to upstream technical-design document>
status: draft | active | superseded
# conditional field
superseded_by: <path to new tasks document>   # required when status is superseded
---
```

### 4.1 Field table

| Field | Type | Required | Description |
|---|---|---|---|
| `artifact_type` | string | yes | Fixed as `tasks` |
| `lifecycle` | enum | yes | Fixed as `living` — a task list is updated continuously |
| `created_at` | date | yes | The date the task list was generated |
| `parent` | path | yes | Path to the upstream technical-design document, for traceability. It always points at the technical design, never at the functional design |
| `status` | enum | yes | `draft` / `active` / `superseded`; semantics in §4.2 |
| `superseded_by` | path | conditional | Required when `status: superseded`, pointing at the successor task list |

Note: the file-level `status` expresses the lifecycle of the task list itself. The `status` field on a task **row** has its own state machine, defined in §5.3 — the two operate at different granularities.

### 4.2 State machine semantics

The 3-value enum for the file-level `status`:

| Status | Meaning | Entry condition |
|---|---|---|
| `draft` | The task list is being drafted | Tasks are still being defined and none has been assigned |
| `active` | Assigned, tasks in progress | Assignment is complete and the list has entered implementation, with every task row at `Todo` |
| `superseded` | Replaced by a new task list | A design change or similar prompted a re-decomposition and the old list is void as a whole; `superseded_by` must be filled in |

**No `completed` status is introduced**: whether the whole list is finished can be inferred from the task row `status` — all `Done` or `Cancelled` — so it does not need marking separately at file level.

---

## 5. Body structure contract

### 5.1 Required fields on a task row

Every task must carry these 6 fields:

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | string | yes | Unique task identifier. `T<n>` is recommended (`T1`, `T2`); a project's own convention such as `AUTH-T1` or `TASK-001` may be kept, but the format must be consistent within one file |
| `title` | string | yes | Task title, ≤ 80 characters, containing a verb, avoiding vague phrasing such as "implement X" |
| `depends_on` | list[string] | yes | List of task IDs depended on; write `—` when there are none |
| `acceptance` | string | yes | Acceptance criterion, testable or otherwise verifiable |
| `owner_or_hint` | string | yes | An assignee, person or role, or an AI execution hint |
| `status` | enum | yes | See the task row state machine in §5.3 |

### 5.2 Recommended table format

```markdown
| Id | Task | Depends on | Acceptance | Owner / Hint | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| T1 | ... | — | ... | ... | Todo |
| T2 | ... | T1 | ... | ... | Todo |
```

### 5.3 Task row state machine

The status enum for the `status` field on a task **row**, at a different granularity from the file-level `status`:

| Status | Meaning | Entry condition |
|---|---|---|
| `Todo` | Initial state, waiting to start | Written uniformly at assignment |
| `In Progress` | Being worked on | An executor picked it up and started |
| `Blocked` | Blocked | A dependency is unmet, or something external blocks it. The reason **must** be noted in an adjacent column |
| `Done` | Complete and accepted | Every acceptance criterion is satisfied |
| `Cancelled` | Cancelled | Scope changed or the requirement was dropped. The reason **must** be noted |

**Initial state rule**: when the assigning skill writes the list, every task must be `Todo`. Other states are maintained by the downstream runtime or by a person.

### 5.4 Dependency semantics

- Dependencies must be **acyclic** (a DAG)
- Separate several dependencies with commas (`T1, T2`)
- Mark a cross-document dependency with a path prefix, such as `other-tasks.md#T3`
- Blocking dependencies (must finish first) and soft ones (recommended to finish first) are not distinguished for now; note the distinction in the `acceptance` field where it matters

### 5.5 Traceability

Every task maps to **at least** one section or one acceptance criterion of the upstream technical design document. Either:

- Reference it explicitly in the task's `acceptance` field, such as "implements X as described in technical design §3.2"
- Or note the source in `owner_or_hint`, such as "based on technical design §architecture.component A"

---

## 6. Anti-patterns

- ❌ A task with no `depends_on` field; even with no dependencies it takes `—`
- ❌ A circular dependency (`T1 → T2 → T1`)
- ❌ Vague granularity — "implement module X" instead of a concrete completable unit
- ❌ No `acceptance` field, leaving no way to judge completion
- ❌ A status other than `Todo` written at assignment
- ❌ No `parent` frontmatter — an orphaned task list with no traceability
- ❌ A missing `status` frontmatter field, leaving the list's lifecycle stage unidentifiable
- ❌ A task with no reference tracing back to the design
- ❌ Several dependencies separated by semicolons or spaces rather than commas, which breaks dependency graph parsing
- ❌ A `Blocked` or `Cancelled` status with no reason noted
- ❌ Mixed task id formats within one file, such as `T1` alongside `TASK-002`

---

## 7. Example

### 7.1 A minimally compliant tasks.md: implementing data export

````markdown
---
artifact_type: tasks
lifecycle: living
created_at: 2026-05-15
parent: ../designs/2026-05-12-data-export-technical-design.md
status: active
---

# 任务：数据导出功能实施

| Id | Task | Depends on | Acceptance | Owner / Hint | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| T1 | 定义导出任务表 schema | — | migration 通过；含 status / progress / file_url 字段（技术设计 §数据模型） | backend | Todo |
| T2 | 实现 CSV 序列化器 | — | 单元测试覆盖空集 / 大字段 / 特殊字符（技术设计 §组件 Serializer） | backend | Todo |
| T3 | 实现导出任务队列消费者 | T1, T2 | 集成测试通过；含失败重试 3 次（技术设计 §数据流） | backend | Todo |
| T4 | 实现 POST /exports 触发接口 | T1 | OpenAPI 文档；幂等键测试（技术设计 §接口契约） | backend | Todo |
| T5 | 实现 GET /exports/:id 查询接口 | T1 | 返回 status + progress + 下载 URL（若 Done）（技术设计 §接口契约） | backend | Todo |
| T6 | 大文件分片上传到对象存储 | T3 | 10GB 测试文件可成功导出（技术设计 §错误处理 OOM 路径） | backend | Todo |
| T7 | 前端导出按钮 + 进度轮询 | T4, T5 | UI 显示进度条；完成后弹下载链接（功能设计 §UI 交互流程） | frontend | Todo |
````

---

## 8. Relationship to other assets

- **Paired rule**: [rules/task-quality.md](../rules/task-quality.md) — the task list quality review checklist covering field completeness, dependency graph correctness, executability and traceability
- **Upstream spec**: [technical-design-modeling.md](./technical-design-modeling.md) — a task list's `parent` points at a technical design document in `approved` status
- **Related practice**: GTD, where every task needs an explicit next action, which maps to the `owner_or_hint` field; and DAG dependencies, which forbid cycles
- **Recursive basis**: this spec itself follows the 8-section skeleton of [spec-modeling.md](./spec-modeling.md) v2.0.0, skipping §2 mental model — a task has no significant N-question framework, and the 6-field table is itself the set of dimensions that must be answered
