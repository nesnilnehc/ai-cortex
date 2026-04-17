---
name: plan-next
description: Analyze governance state and produce next-action routing plan from existing docs; default is planning-only (no downstream execution).
description_zh: 基于现有治理文档分析状态并输出下一步路由计划；默认仅规划，不执行下游技能。
tags: [workflow, meta-skill, automation]
version: 4.0.0
license: MIT
recommended_scope: project
cognitive_mode: interpretive
metadata:
  author: ai-cortex
triggers: [plan next, next step, checkpoint, governance, iteration]
input_schema:
  type: free-form
  description: Governance docs sources, optional scope, optional execute flag
  defaults:
    execute: false
output_schema:
  type: chat
  description: Structured chat output with 3 fixed sections — sources inventory, readiness verdict, prioritized next tasks
---

# 技能：计划下一步（Plan Next）

## 目的 (Purpose)

盘点治理输入源并生成下一步行动路由，默认只输出计划，不执行下游技能。

---

## 核心目标（Core Objective）

**首要目标**：提供可执行的下一步计划与技能路由，而不是在规划阶段隐式实施改动。

**成功标准**（必须全部满足）：

1. ✅ 输出符合 Behavior 各阶段要求的三节结构（输入源清单、准备门结论、推荐路由任务）
2. ✅ 默认 `execute=false` 下未调用任何下游技能

**验收测试**：报告是否能被他人直接用于执行，而无需再追问"接下来该跑哪些技能"？

---

## 范围边界（Scope Boundaries）

**本技能负责**：详见 Behavior 各阶段（治理输入发现 / 准备门诊断 / 路由建议生成）。

**本技能不负责**：

- 默认模式下执行下游技能
- 矩阵中推荐技能的实际执行（`define-*` / `align-*` / `assess-*` / `tidy-repo` / ...）

**交接点**：路由建议产出后由用户按优先级执行下游技能；遇阻碍按 ESCALATED 退出回到本技能重新评估。

---

## 使用场景（Use Cases）

- 迭代收尾后的下一步规划
- 发布前治理路径确认
- 输入源缺失时的补齐路线设计

---

## 行为（Behavior）

整体在 `execute=false` 默认模式下只生成路由建议；`execute=true` 时按矩阵推荐顺序执行下游技能。

### 阶段 0：治理输入发现

按 **5 主题（MECE）** 扫描仓库治理资产：

| 主题 | 含义 | 扫描位置 |
|---|---|---|
| **Why** | 为什么 / 去向 | `docs/project-overview/{mission,vision,north-star,strategic-goals,strategic-pillars}.md` |
| **What/When** | 做什么、何时做 | `docs/process-management/{roadmap,backlog/}.md`、`docs/requirements-planning/` |
| **How** | 怎么做（设计决策） | `docs/architecture/adrs/`、`docs/designs/` |
| **Is** | 实际状态 | 仓库代码、构建出的 docs |
| **Rules** | 治理规矩 | `docs/ARTIFACT_NORMS.md`、`specs/`、`protocols/`、`rules/` |

对每项资产记录：路径、状态（present / placeholder / missing）、质量、最后更新时间。

### 阶段 0.5：准备门诊断

判断是否短路（不进入完整路由生成），判据复用阶段 1 矩阵：

| 条件 | 判据 | 短路动作 |
|---|---|---|
| **治理基础设施缺位** | `Rules × G1` 命中（`docs/ARTIFACT_NORMS.md` 缺失或 `specs/` 为空） | 仅输出 P0 路由 `discover-docs-norms → define-docs-norms`，其他建议暂缓 |
| **战略锚点全空** | `Why × G1` 全部资产缺失（mission / vision / NSM / goals / pillars 一个都没有） | 仅输出 P0 路由 `define-mission`（或用户指定的入口资产），其他建议暂缓 |
| **均通过** | Rules 与 Why 至少各有一项 present | 进入阶段 1 完整路由生成 |

**短路理由**：上层资产缺失时，下层路由建议会建立在不稳定的前提上；先补足上层再继续。

**短路输出仍走对话三节结构**，第 3 节只列 P0 一条路由 + 明确说明"其他建议暂缓，等上层补齐后重跑 plan-next"。

### 阶段 1：路由建议生成

按 **主题 × 缺口类型** 矩阵诊断。主题与缺口类型正交，路由由两者交叉决定。

**4 类缺口（MECE，互斥且穷尽）**：

| 类型 | 判据 | 动作 |
|---|---|---|
| **G1 Absent** | 应存在但缺失 | **DEFINE** （`define-*`） |
| **G2 Incomplete** | 存在但未达就绪标准（占位、字段缺失、链接断） | **ASSESS** （`assess-*`） |
| **G3 Inconsistent** | 与另一真相源冲突（drift） | **ALIGN** （`align-*`） |
| **G4 Disorganized** | 内容合规但位置 / 命名 / 规范不符 | **ORGANIZE** （`tidy-repo` / `define-docs-norms`） |

**路由矩阵**：

| 主题 | G1 Absent | G2 Incomplete | G3 Inconsistent | G4 Disorganized |
|---|---|---|---|---|
| **Why** | `define-mission` / `define-vision` / `define-north-star` / `design-strategic-goals` / `define-strategic-pillars` | `assess-docs` → re-DEFINE | — | `tidy-repo` |
| **What/When** | `define-roadmap` / `analyze-requirements` / `capture-work-items` | `assess-docs` | `align-planning` / `align-backlog` | `tidy-repo` |
| **How** | `design-solution` | `assess-docs` | `align-architecture` | `tidy-repo` |
| **Is** | — | `review-*` 家族 | `assess-docs-code-alignment` | `tidy-repo` |
| **Rules** | `discover-docs-norms` → `define-docs-norms` | `audit-docs` | `align-planning` | `tidy-repo` / `curate-skills` |

**矩阵记号**：

- `/` 表示并列（任选其一）
- `→` 表示链式调用（先后顺序）
- `—` 表示无自动路由（需人工判断或不在本技能职责，如 Why × G3 是策略漂移需重新定义；Is × G1 是项目尚未存在）

**优先级规则**（默认）：

- **P0**：`Rules × G1`（治理基础设施缺位）OR `Why × G1` 全空（无战略锚点）
- **P1**：`Why × G2` / `What × G1` / `What × G3`（计划层缺失或漂移）
- **P2**：`How × any` / `Is × any`（设计与实现层）
- 其余 **P3**

**每条路由输出字段**：主题、缺口类型、推荐技能、依据（指向具体资产）、优先级、停止条件。

**停止条件写法**（每条路由必含三种退出之一）：

| 退出 | 触发 |
|---|---|
| **DONE** | 对应资产状态从 missing/incomplete/inconsistent 变为 present/aligned |
| **DEFERRED** | 使用者明确延后到下个周期 |
| **ESCALATED** | 下游技能执行受阻（如战略冲突、依赖循环），回到 plan-next 重新评估 |

---

## 输入与输出 (Input & Output)

**输入**：见 frontmatter `input_schema` —— 治理文档上下文 + `execute` 开关（默认 false）。

**输出**：对话直出三节（输入源清单 / 准备门结论 / 推荐路由任务）。每节字段详见 Behavior 阶段 0、0.5、1。

---

## 限制（Restrictions）

### 硬边界（Hard Boundaries）

- 不在 `execute=false` 时调用任何下游技能
- 不隐藏跳过原因（短路或矩阵 `—` 时必须明示）
- 不混入下游技能的执行细节（不写 ADR、不修代码、不整结构）

### 技能边界 (Skill Boundaries)

**plan-next 只推荐路由，不执行**。各动作的实际执行者：

| 动作 | 实际执行技能 |
|---|---|
| **DEFINE** | `define-mission` / `define-vision` / `define-north-star` / `design-strategic-goals` / `define-strategic-pillars` / `define-roadmap` / `define-docs-norms` / `design-solution` / `analyze-requirements` / `capture-work-items` |
| **ASSESS** | `assess-docs` / `audit-docs` / `review-*` 家族 |
| **ALIGN** | `align-planning` / `align-backlog` / `align-architecture` / `assess-docs-code-alignment` |
| **ORGANIZE** | `tidy-repo` / `discover-docs-norms` / `curate-skills` |

### Anti-Patterns

- ❌ **不要在矩阵 `—` 单元格强行推荐技能** —— 应明示需人工判断
- ❌ **不要用模糊措辞**（"可能 / 或许 / 可以考虑"）写路由 —— 每条路由必须确定推荐 + 明确停止条件
- ❌ **不要省略停止条件** —— 缺停止条件会导致重跑 plan-next 反复推荐同一条
- ❌ **不要把多个 G 类型混在一条路由** —— 一条路由对应矩阵的一个单元格
- ❌ **不要按缺口数量给优先级**（如"5 个 G1 比 1 个 G3 重要"）—— 优先级由治理层级决定，见阶段 1 优先级规则
- ❌ **不要在 `execute=false` 时返回执行结果** —— 仅返回路由建议

---

## 自检（Self-Check）

- [ ] 阶段 0 覆盖全部 5 主题（Why / What/When / How / Is / Rules），每项资产有状态（present / placeholder / missing）
- [ ] 阶段 0.5 短路条件已显式判定；未短路时给出"为何继续"
- [ ] 每条路由含六字段：主题、缺口类型（G1-G4）、推荐技能、依据、优先级、停止条件
- [ ] 每条停止条件是 DONE / DEFERRED / ESCALATED 三者之一
- [ ] 矩阵 `—` 单元格未被强行推荐技能（应明示需人工判断）
- [ ] 默认模式（`execute=false`）下未调用任何下游技能
- [ ] 输出三节顺序与语义对应 frontmatter `output_schema.description`（sources inventory ↔ 输入源清单 / readiness verdict ↔ 准备门结论 / prioritized next tasks ↔ 推荐路由任务）

---

## 示例（Examples）

### 示例 1：完整路由（happy path）

**场景**：项目有 mission / vision，无 NSM / strategic-goals，roadmap 存在但 backlog 大量项与 strategy 不匹配。

**对话输出**：

#### 1. 输入源清单

| 主题 | 资产 | 路径 | 状态 | 质量 |
|---|---|---|---|---|
| Why | mission | `docs/project-overview/mission.md` | present | high |
| Why | vision | `docs/project-overview/vision.md` | present | medium |
| Why | north-star | — | missing | — |
| Why | strategic-goals | — | missing | — |
| What/When | roadmap | `docs/process-management/roadmap.md` | present | high |
| What/When | backlog | `docs/process-management/backlog/` | present | medium（与 strategy 偏离） |
| Rules | ARTIFACT_NORMS | `docs/ARTIFACT_NORMS.md` | present | high |

#### 2. 准备门结论

**通过** —— Rules 与 Why 至少各有一项 present，进入完整路由。

#### 3. 推荐路由任务

| # | 主题 | 缺口 | 推荐技能 | 依据 | 优先级 | 停止条件 |
|---|---|---|---|---|---|---|
| 1 | Why | G1 | `define-north-star` | NSM 缺失，无单一关键指标 | P1 | DONE: north-star.md 写入并通过 `assess-docs` |
| 2 | Why | G1 | `design-strategic-goals` | strategic-goals 缺失 | P1 | DONE: strategic-goals.md 写入；ESCALATED: 与 NSM 冲突需重定义 |
| 3 | What/When | G3 | `align-backlog` | backlog 多项与 strategy 不匹配 | P1 | DONE: 所有 backlog 项有 strategy 映射；DEFERRED: 用户延后 |

---

### 示例 2：短路 —— 治理基础设施缺位（边缘场景）

**场景**：新项目，`docs/ARTIFACT_NORMS.md` 不存在，`specs/` 为空，无 mission。

**对话输出**：

#### 1. 输入源清单

| 主题 | 资产 | 状态 |
|---|---|---|
| Rules | ARTIFACT_NORMS | missing |
| Rules | specs/ | empty |
| Why | mission / vision / NSM / goals / pillars | 全部 missing |
| What/When / How / Is | （未扫描，短路触发） | — |

#### 2. 准备门结论

**短路** —— `Rules × G1` 命中。`Why × G1` 全空亦命中，但 Rules 优先级更高（P0 中靠前）。

#### 3. 推荐路由任务

| # | 主题 | 缺口 | 推荐技能 | 依据 | 优先级 | 停止条件 |
|---|---|---|---|---|---|---|
| 1 | Rules | G1 | `discover-docs-norms` → `define-docs-norms` | ARTIFACT_NORMS 缺失，规范基础未建立 | **P0** | DONE: ARTIFACT_NORMS.md 落盘并验收，之后重跑 plan-next |

> **其他建议暂缓** —— 治理规则未建立时，下游资产创建无统一标准。补齐 Rules 后重新运行 plan-next 获取完整路由（包括 Why × G1 的战略锚点补齐）。
