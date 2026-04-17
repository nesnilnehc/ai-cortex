---
name: plan-next
description: Analyze governance state and produce next-action routing plan from existing docs; default is planning-only (no downstream execution).
description_zh: 基于现有治理文档分析状态并输出下一步路由计划；默认仅规划，不执行下游技能。
tags: [workflow, meta-skill, automation]
version: 5.0.0
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
  description: Structured chat output with project state label, 3 fixed sections (sources inventory, readiness verdict, prioritized next tasks), and two-tier routing (Primary state-focused + Secondary full-matrix compressed)
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
3. ✅ 标识当前**项目状态**（S1-S7）及其判定依据（ADR 2 决策 3.5）
4. ✅ 推荐路由任务采用 **Primary（激活层） + Secondary（全矩阵压缩摘要）两层输出**（ADR 2 决策 3.6），矩阵 MECE 覆盖在 Secondary 完整保留

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

### 阶段 0.6：项目状态识别（7 态状态机）

**定位**：状态机是矩阵的**解释器**（上下游关系），不是替代者。消费阶段 0 的资产状态扫描，产出状态标签用于阶段 1 的 Primary 层聚焦。

基于阶段 0 结果 + git log + 文件 mtime 识别项目当前状态：

| 状态 | 判定信号 | 激活层（Primary 聚焦） |
|---|---|---|
| **S1 Greenfield** | Why 层所有资产缺失或仅占位 | Why × G1 |
| **S2 Strategy drafted** | Why ≥ 2 项 present；roadmap 缺 | What × G1 |
| **S3 Plan drafted, 稀薄 backlog** | roadmap present；backlog 条目 < 阈值（默认 5） | What × G2 |
| **S4 Backlog rich, idle** | roadmap + backlog 齐全；无 in-progress；近 N 天（默认 3）无 commit | Pull ceremony（`prioritize-backlog` → `promote-roadmap-items`） |
| **S5 Execution in-flight** | 有 in-progress task / 未合并 PR / 近 N 天有 commit | 静默，仅 Rules×G1 打断 |
| **S6 Post-execution, 可能漂移** | 近期 merge / release；上次 `align-planning` > N 天（默认 14） | Is × G3（触发 `align-planning`） |
| **S7 Healthy / Idle** | 矩阵无缺口 + 无 in-flight + 漂移近期查过 | Quiet mode（明示无治理行动需要） |

**信号来源**：
- 资产存在 / 状态：阶段 0 扫描结果
- in-flight：扫描 `backlog/*.md` 的 `status` 字段 + `git status` 未提交 + 近期 commit
- 漂移新鲜度：`docs/calibration/planning-alignment.md` 的 `created_at`
- 占位 vs 真实：frontmatter `status: placeholder` 或启发式字数判断

**低 confidence fallback**：多个状态都有部分匹配且无法择一时，降级到全矩阵输出（Secondary 层全展开），明示"状态未定 fallback"并列出各候选状态的支撑信号。

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

### 阶段 1.5：两层输出合成（Primary + Secondary）

**定位**：两层输出是**表现层**，在矩阵诊断（数据）和状态机（解释）之上，决定显示权重。

**输出结构**：

```
项目状态：S<N>（<判定摘要>）
判定依据：<关键信号>

=== Primary：激活层路由 ===

根据状态机激活层，详细列出相关路由（6 字段齐全）：
| # | 主题 | 缺口 | 技能 | 依据 | 优先级 | 停止条件 |
| 1 | ... | ... | ... | ... | P0/P1 | DONE/DEFERRED/ESCALATED |

=== Secondary：全矩阵其他发现（压缩） ===

其他矩阵格子检测到的缺口，1 行 / 项简要呈现：
| 格子 | 一句话概述 | 建议 |
| Rules × G4 | ARTIFACT_NORMS 老 schema | 做文档工作时顺手；不阻塞 |
| How × G2 | ADR-015 缺"后果"节 | 单独补；非紧急 |
```

**两层分工**：

| 层 | 内容 | 显示权重 |
|---|---|---|
| Primary | 当前状态激活层的缺口，完整 6 字段 | 高（详细、P0/P1 优先） |
| Secondary | 矩阵其他格子的缺口，1 行摘要 | 低（紧凑、便于扫视） |

**为什么保留 Secondary**：
- 矩阵 MECE 完整性不丢失（用户能看到系统性视角）
- 状态机误判时兜底（被"去优先化"的格子用户仍可见）
- Secondary 建议字段提示"立即 / 推迟 / 不阻塞"，帮用户做跨层判断

**用户 flag 覆盖**：
- `--force-full-matrix` 强制全量输出（Primary 扩展到所有格子）
- 低 confidence 自动触发此 flag

---

## 输入与输出 (Input & Output)

**输入**：见 frontmatter `input_schema` —— 治理文档上下文 + `execute` 开关（默认 false）。

**输出**：对话直出，固定结构：

1. **项目状态**（S1-S7）+ 判定依据（见 Behavior 阶段 0.6）
2. **输入源清单**（Behavior 阶段 0）
3. **准备门结论**（Behavior 阶段 0.5，含短路判定）
4. **推荐路由任务**（Behavior 阶段 1 + 1.5）：
   - Primary 层：状态激活的路由，6 字段齐全
   - Secondary 层：矩阵其他发现，1 行摘要

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
- ❌ **不要用状态机折叠 Secondary 层** —— 状态机是**显示权重**工具，不是**过滤器**；矩阵其他格子的缺口必须在 Secondary 层呈现
- ❌ **不要在状态不明时强行归类** —— 低 confidence 时 fallback 到全矩阵输出，不伪装确定性

---

## 自检（Self-Check）

- [ ] 阶段 0 覆盖全部 5 主题（Why / What/When / How / Is / Rules），每项资产有状态（present / placeholder / missing）
- [ ] 阶段 0.5 短路条件已显式判定；未短路时给出"为何继续"
- [ ] 阶段 0.6 项目状态（S1-S7）已识别，附判定依据；低 confidence 时 fallback 全矩阵
- [ ] 每条路由含六字段：主题、缺口类型（G1-G4）、推荐技能、依据、优先级、停止条件
- [ ] 每条停止条件是 DONE / DEFERRED / ESCALATED 三者之一
- [ ] 矩阵 `—` 单元格未被强行推荐技能（应明示需人工判断）
- [ ] 默认模式（`execute=false`）下未调用任何下游技能
- [ ] 输出含 Primary + Secondary 两层；Secondary 保留了所有矩阵发现的缺口，未因状态机而折叠
- [ ] 输出三节顺序与语义对应 frontmatter `output_schema.description`（sources inventory ↔ 输入源清单 / readiness verdict ↔ 准备门结论 / prioritized next tasks ↔ 推荐路由任务）

---

## 示例（Examples）

### 示例 1：完整路由（S2 → S3 过渡，happy path）

**场景**：项目有 mission / vision，无 NSM / strategic-goals，roadmap 存在但 backlog 大量项与 strategy 不匹配。

**对话输出**：

#### 项目状态：**S2 Strategy drafted**（部分完成，向 S3 过渡）

**判定依据**：
- Why 层 2 项 present（mission、vision），3 项 missing（north-star、strategic-goals、strategic-pillars）
- roadmap present 但其上游 strategic-goals 缺失，roadmap 有效性受影响
- 状态机倾向 S2；What 层已有 roadmap 所以也带 S3 特征
- 最终采 S2（上游优先），激活层：**Why × G1**

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

##### Primary：激活层路由（Why × G1）

| # | 主题 | 缺口 | 推荐技能 | 依据 | 优先级 | 停止条件 |
|---|---|---|---|---|---|---|
| 1 | Why | G1 | `define-north-star` | NSM 缺失，无单一关键指标 | P1 | DONE: north-star.md 写入并通过 `assess-docs` |
| 2 | Why | G1 | `design-strategic-goals` | strategic-goals 缺失（并须含工程健康目标） | P1 | DONE: strategic-goals.md 写入；ESCALATED: 与 NSM 冲突需重定义 |

##### Secondary：全矩阵其他发现（压缩）

| 格子 | 一句话概述 | 建议 |
|---|---|---|
| What × G3 | backlog 多项与 strategy 不匹配 | 等 Why 层补齐再 `align-backlog`，避免基于未来要重定义的 strategy 做对齐 |

> **Secondary 为什么不升 Primary**：Why × G1 是上游缺失；下游 align-backlog 在上游未稳前做会返工。状态机正确聚焦上游。

---

### 示例 2：短路 —— 治理基础设施缺位（S1 Greenfield，边缘场景）

**场景**：新项目，`docs/ARTIFACT_NORMS.md` 不存在，`specs/` 为空，无 mission。

**对话输出**：

#### 项目状态：**S1 Greenfield**

**判定依据**：Why 层全部 missing + Rules 层 missing → 匹配 Greenfield。进入 0.5 短路。

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

##### Primary：短路路由

| # | 主题 | 缺口 | 推荐技能 | 依据 | 优先级 | 停止条件 |
|---|---|---|---|---|---|---|
| 1 | Rules | G1 | `discover-docs-norms` → `define-docs-norms` | ARTIFACT_NORMS 缺失，规范基础未建立 | **P0** | DONE: ARTIFACT_NORMS.md 落盘并验收，之后重跑 plan-next |

##### Secondary：（短路时省略）

> 短路场景下 Secondary 层省略 —— 治理规则未建立时，下游资产创建无统一标准，扫描其他格子价值有限。补齐 Rules 后重跑 plan-next 获得完整路由（含 Why × G1）。

---

### 示例 3：健康状态（S7 Quiet mode，边缘场景）

**场景**：成熟项目，治理链齐全，近期已跑 align-planning 无漂移，无 in-flight 工作。

**对话输出**：

#### 项目状态：**S7 Healthy / Idle**

**判定依据**：
- 全部 5 主题资产 present，无 missing / placeholder
- `docs/calibration/planning-alignment.md` 最近 created_at = 3 天前 < 14 天阈值
- git log 近 3 天无 commit，无 in-progress task / 未合并 PR
- 矩阵全扫描无 G1-G4 缺口

#### 1. 输入源清单

（所有资产 present，质量均 high，全量列表略）

#### 2. 准备门结论

**通过**。Rules 与 Why 齐全，状态机识别为 S7。

#### 3. 推荐路由任务

##### Primary：无治理行动需要

> **Quiet mode**：治理状态健康，本轮无需任何治理技能。**建议按项目 roadmap 执行产品工作**。
>
> 下次建议检查：14 天后，或 align-planning 报告过期前（距今 11 天后到期）。

##### Secondary：全矩阵扫描（无发现）

| 格子 | 发现 |
|---|---|
| Why × G1-G4 | 无 |
| What × G1-G4 | 无 |
| How × G1-G4 | 无 |
| Is × G1-G4 | 无（上次 `assess-docs-code-alignment` 3 天前，通过） |
| Rules × G1-G4 | 无 |

> **Quiet mode 意图**：避免 plan-next 在健康状态下产出嗓音；把注意力还给产品工作。
