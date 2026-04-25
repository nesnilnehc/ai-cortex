---
name: plan-next
description: Analyze governance state and produce next-action routing plan from existing docs; default is planning-only (no downstream execution).
description_zh: 基于现有治理文档分析状态并输出下一步路由计划；默认仅规划，不执行下游技能。
tags: [workflow, meta-skill, automation]
version: 8.0.0
license: MIT
recommended_scope: project
cognitive_mode: interpretive
metadata:
  author: ai-cortex
triggers: [plan next, next step, checkpoint, governance, iteration]
input_schema:
  type: free-form
  description: Governance docs sources, optional scope, optional execute flag, optional threshold overrides
  defaults:
    execute: false
    thresholds:
      commit_idle_days: 3
      drift_staleness_days: 14
      backlog_min_items: 5
      confidence_low_below: 0.6
      task_stuck_days: 7
    task_source: auto
    roadmap_tier_source: docs/process-management/roadmap.md
    artifact_norms_path: docs/ARTIFACT_NORMS.md
output_schema:
  type: chat
  description: Three-section user-facing report — "Now do" (actionable routes), "Also watch" (other findings, capped at 5), "Diagnosis" (project status, asset inventory, decision rules, link scheme identification). Internal codes (S1-S7, G1-G4, P0-P3) appear only in Diagnosis as traceability anchors.
---

# 技能：计划下一步（Plan Next）

> **角色**：治理入口路由器
> **WHAT**：盘点治理资产、识别缺口、产出下一步技能路由建议
> **HOW**：默认只规划不执行；单一维度问题可直接调用 `assess-docs` / `align-planning` 等专用技能，无需通过本技能
> **区别**：不同于 `assess-docs`（深度文档评估）或 `align-planning`（漂移校准），本技能仅做路由分发，不做深度分析

## 目的 (Purpose)

盘点治理输入源并生成下一步行动路由，默认只输出计划，不执行下游技能。

### Positioning（与兄弟技能的位置关系）

- plan-next 是**入口路由器**：它看全局、决定下一步跑哪个技能
- **不适用时可跳过**：已确定只查文档就绪度 → 直跑 `assess-docs`；已确定有漂移 → 直跑 `align-planning`；已知某个维度缺失 → 直跑 `define-*` / `design-*`
- 适用时机：迭代收尾 / 发布前治理路径确认 / 对下一步无头绪时
- **执行态边界**：
  - **做**：每次从零扫，读 task 当前状态 × 代码活动交叉**诊断**治理健康（Step 2.7）；输出"现在该做"路由建议（含具体下游缺口与对应技能）
  - **不做**：
    - 不记 task 历史（不知"什么时候从 todo 变 in-progress"），不答"本周晋升几条"类时序问题
    - 不维护项目 task 列表 / 不分配 / 不充当外部系统的 task 状态 API（项目管理工具的活）
    - 不自动推进执行（默认 `execute=false`）——只导航不开车，路由建议交用户决定要不要跑、按什么顺序跑
- **链接约定无需声明**：AI Cortex canonical 约定（按 [artifact-contract §2](../../specs/artifact-contract.md#2-制品类型)，requirements/designs/tasks 统一为 `docs/<type>/{slug}.md`）已硬编码在所有产出技能 `path_pattern` 里；项目若想用聚合目录 / 父指针 / 清单等非默认约定，通过 `ARTIFACT_NORMS.md` 的 `path_pattern` 覆盖 + 可选 `upstream_ref` 输入 + 物理 manifest 文件表达即可

---

## 核心目标（Core Objective）

**Primary Goal**：提供可执行的下一步计划与技能路由，而不是在规划阶段隐式实施改动。

**Success Criteria**（必须全部满足）：

1. ✅ 输出符合三步法（扫 / 诊 / 荐）的三节用户报告（现在该做 / 其他可留意 / 诊断依据）
2. ✅ 默认 `execute=false` 下未调用任何下游技能
3. ✅ 用户报告里仅使用自然语言术语；内部编号（S1-S7、G1-G4、P0-P3）只出现在"诊断依据"末尾的追溯位置
4. ✅ "现在该做"由状态机聚焦范围决定，按 P0>P1>P2>P3 排序；聚焦外发现归入"其他可留意"
5. ✅ 下游资产（requirement / design / task）就绪度评估**仅针对 roadmap Now tier 条目**；Next/Later tier 的下游缺失不报告
6. ✅ 执行健康判定使用**任务状态 × 代码活动**双信号交叉，不单凭任一信号
7. ✅ Now tier 下游扫描按物理信号工作（resolved `path_pattern` + 可选 `parent:` frontmatter + 可选 manifest 文件）

**Acceptance Test**：报告的"现在该做"节是否能被他人直接用于执行，而无需再追问"接下来该跑哪些技能"？

---

## 范围边界（Scope Boundaries）

**本技能负责**：资产扫描 / 状态诊断 / 缺口识别 / 路由建议产出。

**本技能不负责**：

- 默认模式下执行下游技能
- 文档深度评估（交给 `assess-docs`）
- 漂移校准（交给 `align-planning`）
- 矩阵中推荐技能的实际执行（`define-*` / `align-*` / `assess-*` / `tidy-repo` / ...）
- **流水线状态追踪**：不记忆历史转换（哪项 task 从 todo→in-progress→done），只扫当下状态
- **task 执行引擎角色**：不推进 task 执行，仅识别"执行卡点 / 追踪漂移 / 完成漂移 / 归档漂移"四类发现
- **维护下行清单**：若项目有清单文件，plan-next 只读不写，不承担"文件变更时同步清单"的职责（那是 `align-work-item-manifest` 的职责）
- **定义或识别链接模式**：v8.0 起此概念不存在——没有 mode 字段、没有枚举、没有识别/选择流程。项目自定义约定通过 `path_pattern` 覆盖机制表达

**Handoff Point**：路由建议产出后由用户按优先级执行下游技能；遇阻碍按"上抛条件"退出回到本技能重新评估。

---

## 使用场景（Use Cases）

- 迭代收尾后的下一步规划
- 发布前治理路径确认
- 输入源缺失时的补齐路线设计
- 不确定下一步该跑哪个技能时的分发入口

---

## 行为（Behavior）

整体在 `execute=false` 默认模式下只生成路由建议；`execute=true` 时按路由推荐顺序执行下游技能。

诊断分三步：**扫（Scan）→ 诊（Diagnose）→ 荐（Recommend）**。

### 步骤 0：Norms Resolution（v8.0 简化）

**本技能产出自身**：plan-next 输出是对话直出（非文档制品），不适用 artifact-contract §8 的 path_pattern 解析。

**本技能消费规范**：按 [specs/artifact-contract.md §8.2](../../specs/artifact-contract.md#82-发现顺序) 顺序读取项目规范以获取下游技能路径覆盖。算法：

```
Step 0.1: Load Runtime Norms
  cache = {}
  for source in [artifact_norms_path, '.ai-cortex/artifact-norms.yaml',
                 'docs/ARTIFACT_NORMS.md']:
    if file exists and is readable:
      try parse YAML/Markdown frontmatter
      if parse error: HALT with diagnostic citing line
      else: merge into cache (first-win per field)
    else: skip silently (缺失 fall-through)
  if cache is empty: record "no norms found" flag（但不是错误——默认 slug 约定即可工作）
  return cache
```

`cache` 的主要用途：步骤 2.5 读 `artifact_types[<type>].path_pattern` 决定下游扫描目录；步骤 2.7 S5 扫描按覆盖值扫任务路径（让 colocation 项目能扫到 `work/<slug>/tasks.md`）。

### 步骤 1：扫（Scan）— 资产盘点

按 **5 主题（MECE）** 扫描仓库治理资产：

| 主题 | 含义 | 扫描位置 |
|---|---|---|
| **Why** | 为什么 / 去向 | `docs/project-overview/{mission,vision,north-star,strategic-goals,strategic-pillars}.md` |
| **What/When** | 做什么、何时做 | `docs/process-management/{roadmap,backlog/}.md`、`docs/requirements-planning/`、`tasks/` |
| **How** | 怎么做（设计决策） | `docs/architecture/adrs/`、`docs/designs/` |
| **Is** | 实际状态 | 仓库代码、构建出的 docs、近期 commit / PR 活动 |
| **Rules** | 治理规矩 | `docs/ARTIFACT_NORMS.md`、`specs/`、`protocols/`、`rules/` |

对每项资产记录：路径、状态（present / placeholder / missing）、质量、最后更新时间。

**补充扫描（为后续诊断提供上下文，不进入主题分类）**：

- **Roadmap tier 结构**：读 `roadmap_tier_source`（默认 `docs/process-management/roadmap.md`），提取 Now / Next / Later 分层及各 tier 的条目 slug 列表。未分层时记录"tier 未声明"。
- **Task 源**：按 `task_source` 读当前任务列表（`status` + `priority` 字段）。`auto` 模式依序探测 `tasks/*.md` → `docs/process-management/backlog/*.md` → `TODO.md`，取首个非空源。
- **代码活动**：最近 N 天 commit 数、未合并 PR 列表、最近 merge / release 时间。

这些补充数据用于步骤 2.1 的 S5 交叉判健康、步骤 2.5 的链接模式读取、步骤 2.6 的 Now tier 作用域计算、步骤 2.7 的任务×代码交叉判。

### 步骤 2：诊（Diagnose）— 状态识别 + 缺口判定

#### 2.0 前置闸门：Rules 层缺位检查

**先于状态识别**：若扫描发现 Rules 层缺位（`ARTIFACT_NORMS.md` 缺失或 `specs/` 为空），直接触发 Short-circuit 输出模式，不进入状态识别。

Short-circuit 模式下，"现在该做"只列 P0 一条路由（规范建立），"其他可留意"节省略，附明示"先补齐规范后重跑 plan-next"。

理由：Rules 层是后续所有资产创建的基准，缺位时状态识别没有稳定前提。

#### 2.1 状态识别（7 态状态机）

状态机是**解释器**，消费步骤 1 的扫描结果，产出状态标签用于步骤 3 的聚焦。

**两种聚焦形态**（状态机先区分）：
- **缺口型**（S1/S2/S3/S6）：聚焦落在矩阵单元格（主题 × 缺口类型）
- **工作流动作型**（S4/S5/S7）：聚焦是工作流动作（ceremony / 静默 / idle），不对应具体矩阵格

| 内部状态 | 用户呈现（自然语言） | 判定信号 | 聚焦范围 |
|---|---|---|---|
| S1 | **起步期** | Why 层所有资产缺失或仅占位 | Why 层资产缺失 |
| S2 | **战略已起草** | Why ≥ 2 项 present；roadmap 缺 | 路线图缺失 |
| S3 | **路线已成、Backlog 稀薄** | roadmap present；backlog 条目 < `backlog_min_items` | Backlog 内容不全 |
| S4 | **Backlog 丰富但停滞** | roadmap + backlog 齐全；无 in-progress；近 `commit_idle_days` 天无 commit | Pull ceremony（`prioritize-backlog` → `promote-roadmap-items`） |
| S5 | **执行中** | 有 in-progress task / 未合并 PR / 近 `commit_idle_days` 天有 commit；**任务状态 × 代码活动交叉判健康（见 2.7）** | 健康：静默，仅规范缺位打断。卡点：执行漂移路由 |
| S6 | **执行收尾、可能漂移** | 近期 merge / release；上次 `align-planning` > `drift_staleness_days` 天 | 文档与代码漂移（触发 `align-planning`） |
| S7 | **健康稳定** | 矩阵无缺口 + 无 in-flight + （漂移近期查过 **OR** 从未 merge/release 无漂移风险） | Quiet mode（明示无治理行动需要） |

> 缺口矩阵 MECE 覆盖所有**缺口型**发现；ceremony / 静默 / idle 是**非缺口型**输出模式，由状态机独立产出，不在矩阵内。

#### 2.2 低 confidence fallback

**完全定性触发**：多个候选状态势均力敌、无主次之分时，退化为全矩阵输出（"其他可留意"展开至所有发现），"诊断依据"明示"状态未定 fallback"并列出各候选状态的支撑信号。

**"势均力敌"的判断**：若 2.4 tiebreak 规则（跨维度优先 + 同维度方向）仍无法择一，即判定为势均力敌。

#### 2.3 缺口判定（4 类缺口矩阵）

**4 类缺口（MECE，互斥且穷尽）**：

| 内部代码 | 用户呈现 | 判据 | 动作 |
|---|---|---|---|
| G1 | **资产缺失** | 应存在但缺失 | **DEFINE** （`define-*`） |
| G2 | **内容不全** | 存在但未达就绪标准（占位、字段缺失、链接断） | **ASSESS** （`assess-*`） |
| G3 | **真相漂移** | 与另一真相源冲突（drift） | **ALIGN** （`align-*`） |
| G4 | **位置错位** | 内容合规但位置 / 命名 / 规范不符 | **ORGANIZE** （`tidy-repo` / `define-docs-norms`） |

**缺口路由矩阵**：

| 主题 | 资产缺失（G1） | 内容不全（G2） | 真相漂移（G3） | 位置错位（G4） |
|---|---|---|---|---|
| **Why（愿景与战略）** | `define-mission` / `define-vision` / `define-north-star` / `design-strategic-goals` / `define-strategic-pillars` | `assess-docs` → re-DEFINE | — | `tidy-repo` |
| **What/When（计划与待办）** | `define-roadmap` / `analyze-requirements` / `capture-work-items` / `breakdown-tasks`（Now tier + design 已 present + task 未拆时） | `assess-docs` | `align-planning` / `align-backlog` | `tidy-repo` |
| **How（设计决策）** | `design-solution` | `assess-docs` | `align-architecture` | `tidy-repo` |
| **Is（实际实现）** | — | `review-*` 家族 | `assess-docs-code-alignment` | `tidy-repo` |
| **Rules（治理规范）** | `discover-docs-norms` → `define-docs-norms` | `audit-docs` | `align-planning` | `tidy-repo` / `curate-skills` |

**矩阵记号**：`/` 并列任选其一；`→` 链式调用；`—` 无自动路由（需人工判断）。

#### 2.4 诊断决策规则（合并 tiebreak 与主从）

用户报告的分层由这三条规则共同决定：

1. **多状态 tiebreak**：多个候选状态同时命中时按下列方向择一——
   - **跨维度**：治理完整度维度（S1-S3）优先于执行态维度（S4-S7）。上游未稳时下游建议无意义。
   - **治理维度内部**：**取上游**（S1 > S2 > S3）。先补愿景再补计划，顺序不可颠倒。
   - **执行态维度内部**：**取下游**（S6 > S5 > S4 > S7）。越靠后越接近治理问题浮现，越紧迫。例：项目在执行中（S5）但漂移已过期（S6），取 S6 → 优先校准漂移，而非继续静默。
2. **聚焦决定"现在该做"**：状态机的聚焦范围决定哪些发现进"现在该做"；聚焦范围外的发现进"其他可留意"。
3. **优先级排序**：聚焦范围内按 **现在 > 下次 > 以后 > 可忽略** 排序（内部对应 P0 > P1 > P2 > P3）。

#### 2.5 Now tier 下游扫描策略

**扫描算法**（按物理信号工作）：

```
Step 2.5.1: 从步骤 0 的 cache 读各 artifact_type 的 resolved path_pattern
  - 命中：使用项目规范覆盖值
  - 未命中：fall back 到技能默认（AI Cortex canonical = docs/<type>/*.md 按 §2）

Step 2.5.2: 按 Now tier 每个条目的 slug 在各 resolved path_pattern 对应目录 glob
  - 匹配到文件 → 下游制品存在
  - 未匹配 → G1 缺口

Step 2.5.3: （可选增强）扫描下游 frontmatter 检测 parent: 字段反向索引
  - 若存在显式 parent 关系，补充信任度（"slug 匹配 + parent 确认"）

Step 2.5.4: （可选增强）检测 manifest 物理文件（如 docs/process-management/now/<slug>.md）
  - 存在 → 以清单为补充真相源，对比清单声明 vs 物理文件，差异作为 G3 漂移
  - 不存在 → 跳过，不强制
```

**无需 mode 配置**：上述三层检测（slug glob / parent 反向索引 / manifest 文件存在）**独立运作、可组合**。项目无需在 `ARTIFACT_NORMS.md` 声明任何"链接模式"——plan-next 直接看物理信号。

**项目定制途径**：

- 想要**聚合式目录**（v7.0 所谓 colocation）→ 在 `ARTIFACT_NORMS.md` 把各 artifact_type 的 `path_pattern` 覆盖为 `work/{slug}/<type>.md`。Step 0 cache 会读到覆盖值，Step 2.5.2 自然扫新路径。
- 想要**显式父指针**（v7.0 所谓 parent-pointer）→ 调用下游技能时传 `upstream_ref`，技能自动 emit `parent:`。Step 2.5.3 会检测。
- 想要**中央清单**（v7.0 所谓 manifest）→ 建清单文件。Step 2.5.4 会检测。
- 不声明任何 → 默认 slug 约定生效，Step 2.5.2 单层扫描。

**诊断依据注明**：最终报告里说明扫描依赖的信号组合（例："按 cache 覆盖的 path_pattern 扫 slug + 未检测到 manifest + 3/5 下游文件含 parent: 字段"）。

#### 2.6 Now tier 作用域

下游资产（requirement / design / task）就绪度评估**仅针对 roadmap Now tier 条目**：

- **Now tier 条目存在无对应下游** = G1 真缺口，进矩阵路由
- **Next / Later tier 的无下游** = 正常状态，**不报告**
- **Roadmap 未分层**（未声明 Now/Next/Later）= 先路由 `promote-roadmap-items` 做分层，**不评估下游就绪**

**深度优先拆解**：每个 Now tier 条目一次只提示**最上游的一步缺口**（requirement 缺 → 先补 requirement，不同时提 design / task），避免"现在该做"列出互相依赖的多条任务。

#### 2.7 S5 执行健康判定（任务 × 代码双信号交叉）

S5 命中时，进一步用任务状态 × 代码活动的 2×2 交叉判具体健康子态：

| 任务状态 | 代码活动 | 判定 | 归类 |
|---|---|---|---|
| in-progress | 近 `commit_idle_days` 天有 commit / PR 更新 | **健康执行** | S5 静默 |
| in-progress | 超 `task_stuck_days` 天无相关 commit / PR | **执行卡点** | `investigate-root-cause` + 人工介入 |
| todo | 有相关 commit / 分支 | **追踪漂移** | `align-planning`（更新任务状态） |
| done | 无 merge 证据 | **完成漂移** | `align-planning` / 人工验证 |
| done | merge 已合但未从 in-progress 清单移除 | **归档漂移** | `tidy-repo` / `align-planning` |

**Tiebreak**：多个执行卡点并存时按任务自身 `priority` 字段排序。注意：任务 priority **仅用于卡点之间 tiebreak**，**不参与** plan-next 路由优先级（P0-P3），后者由治理层级决定。

**降级**：若 `task_source` 未发现任何可扫描的任务源，S5 回退到仅用代码活动判断（原 v6.2 行为），并在诊断依据注明"任务源未配置，执行健康仅按代码活动判"。

**v7.0 路径解析**：扫描 task 源路径时用步骤 0 的 cache 解析——若 cache 含 `tasks` / `backlog-item` artifact_type 的 `path_pattern`，按 cache 值扫描；若无，fall through 到 `task_source` frontmatter 默认（`tasks/*.md` → `docs/process-management/backlog/*.md`）。colocation 模式下项目的 tasks 实际在 `work/<slug>/tasks.md`，v7.0 算法能正确扫到。

### 步骤 3：荐（Recommend）— 路由生成与分层

分层与排序由步骤 2.4 决策规则决定，步骤 3 负责字段填充与呈现。

#### 3.1 优先级（内部分级）

优先级体现"治理紧迫性"——越上游、越基础的缺口越优先：

- **现在（P0）**：阻断其他治理进展的根基问题（通常已由 2.0 前置闸门或 S1 聚焦吃掉，此处仅作语义锚点）
- **下次（P1）**：战略层就绪度问题 / 计划层的缺失或漂移
- **以后（P2）**：设计层 / 实现层的任何缺口
- **可忽略（P3）**：其余

#### 3.2 每条路由六字段

主题、缺口类型、推荐技能、依据（指向具体资产）、优先级（用户呈现为"现在/下次/以后/可忽略"）、停止条件。

**主题列的写法**：前两节（现在该做 / 其他可留意）中，主题用自然语言描述对应资产（如"路线图"、"战略目标"、"规范文件"），而非作者视角的分类词（Why/What/How/Is/Rules）。作者视角分类只在"诊断依据"的判定规则中作追溯出现。

**停止条件**三选一：

| 用户呈现 | 触发 |
|---|---|
| **完成条件** | 对应资产状态从 missing/incomplete/inconsistent 变为 present/aligned |
| **延后条件** | 使用者明确延后到下个周期 |
| **上抛条件** | 下游技能执行受阻（如战略冲突、依赖循环），回到 plan-next 重新评估 |

#### 3.3 用户输出三节

```
# 下一步建议

## 现在该做（1-3 条，六字段齐全）
...

## 其他可留意（≤5 条简短列表；超出折叠为 "+N more, use --full"）
...

## 诊断依据（末尾）
- 项目情况：<一句自然语言摘要>
- 资产清单：<表>
- 判定规则：<状态识别信号 + tiebreak + 聚焦范围说明；允许在句中以括注形式标注 S 编号作追溯，如"匹配'战略已起草'状态（S2）">
```

**用户 flag**：
- `--full` 强制全量展示（"其他可留意"不折叠）
- 低 confidence 自动触发 `--full`

---

## 输入与输出 (Input & Output)

**输入**：见 frontmatter `input_schema` —— 治理文档上下文 + `execute` 开关（默认 false）+ `thresholds` 阈值覆盖（默认见 frontmatter）。

**输出**：对话直出，三节用户报告（现在该做 / 其他可留意 / 诊断依据），顺序固定。内部术语使用规则见 Anti-Patterns 第 10 条。

---

## 限制（Restrictions）

### 硬边界（Hard Boundaries）

- 不在 `execute=false` 时调用任何下游技能
- 不隐藏跳过原因（short-circuit 或矩阵 `—` 时必须明示）
- 不混入下游技能的执行细节（不写 ADR、不修代码、不整结构）
- **plan-next 是 stateless 的**：每次调用从零开始重扫，不依赖上次结果
- 内部术语（S1-S7、G1-G4、P0-P3、Primary/Secondary、主题分类词）使用规则见 Anti-Patterns 第 10 条（集中规则，避免重复表述）

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
- ❌ **不要把多个缺口类型混在一条路由** —— 一条路由对应矩阵的一个单元格
- ❌ **不要按缺口数量给优先级**（如"5 个 G1 比 1 个 G3 重要"）—— 优先级由治理层级决定，见步骤 3.1
- ❌ **不要在 `execute=false` 时返回执行结果** —— 仅返回路由建议
- ❌ **不要用状态机折叠"其他可留意"** —— 状态机是**聚焦工具**，不是**过滤器**；聚焦外的缺口必须在"其他可留意"呈现（无发现时写"无"即可，不列 20 个"无"格）
- ❌ **不要在状态不明时强行归类** —— 低 confidence 时 fallback 到全矩阵输出，不伪装确定性
- ❌ **不要对 Next / Later tier 条目报下游缺口** —— 下游就绪度评估仅针对 Now tier；Next/Later 的无下游是正常状态
- ❌ **不要同时提示同一条目的多层缺口** —— 深度优先；每个 Now tier 条目一次只报最上游的一步
- ❌ **不要仅凭任务状态或仅凭 commit 活动单独判执行健康** —— 必须 2×2 交叉（见 2.7）；单信号会把"任务维护不规范"误判为"执行健康"
- ❌ **不要用任务 priority 字段决定 plan-next 路由优先级** —— 任务 priority 仅在执行卡点之间 tiebreak；治理优先级（P0-P3）由治理层级决定，不可僭越
- ❌ **不要承担下行清单的维护职责** —— plan-next 只读清单，把清单与物理文件差异作为 G3 漂移报出；维护由 `align-work-item-manifest` 承担
- ❌ **不要引入 mode 枚举或配置字段** —— 扫描直接按物理信号（resolved path_pattern + parent: frontmatter + manifest 文件存在）
- ❌ **不要让内部术语泄漏到用户视角**（统一规则）：
   - **前两节（现在该做 / 其他可留意）**：禁用内部编号（S1-S7、G1-G4、P0-P3）和主题分类词（Why / What/When / How / Is / Rules）；主题列用自然语言描述资产（"路线图"、"战略目标"、"规范文件"）
   - **诊断依据**：主要表达用自然语言（"战略已起草"而非"S2"）；S 编号至多以括注形式作追溯，如"（S2）"，不作为句子主语
   - **示例标题**：不要写"S2 → S3 过渡"之类，改为自然语言场景描述

---

## 自检（Self-Check）

**扫**：
- [ ] 5 主题全覆盖（Why / What/When / How / Is / Rules），每项资产有状态（present / placeholder / missing）
- [ ] 已读 roadmap tier 结构（Now / Next / Later）；未分层时已识别为"需先 promote"
- [ ] **步骤 0 Norms Resolution 已执行**：cache 已构建或明示"no norms found"；未静默使用默认（v7.0 断言式）
- [ ] Step 2.5 按物理信号扫描（resolved path_pattern + 可选 parent: + 可选 manifest）

**诊**：
- [ ] 项目状态已识别，多状态匹配时已应用 tiebreak（跨维度 / 治理维度上游 / 执行维度下游）；低 confidence 时已 fallback 全矩阵
- [ ] 聚焦范围已明示（矩阵单元格型 or 工作流动作型）
- [ ] S5 命中时已做任务 × 代码 2×2 交叉，产出健康 / 卡点 / 追踪漂移 / 完成漂移 / 归档漂移之一
- [ ] 下游就绪度评估仅对 Now tier 条目；Next/Later 未被误报为缺口

**荐**：
- [ ] "现在该做"每条路由六字段齐（主题、缺口类型、推荐技能、依据、优先级、停止条件）
- [ ] 聚焦范围内按 P0>P1>P2>P3 排序；聚焦外进"其他可留意"
- [ ] 矩阵 `—` 单元格未被强行推荐技能；停止条件是完成/延后/上抛之一
- [ ] 每个 Now tier 条目一次只报最上游缺口（深度优先，不同时报多层）

**输出与边界**：
- [ ] 用户报告前两节仅使用自然语言；内部编号只出现在"诊断依据"
- [ ] 默认模式（`execute=false`）下未调用任何下游技能
- [ ] "其他可留意"超过 5 条时已折叠为 "+N more"；short-circuit 时已省略
- [ ] 诊断依据里已注明下游扫描依赖的物理信号组合（例："按 cache 覆盖的 path_pattern 扫 slug + 检测到 2 个 manifest + 无 parent 字段"）

---

## 示例（Examples）

### 示例 1：战略半成品（happy path）

**场景**：项目有 mission / vision，无 NSM / strategic-goals，roadmap 存在但 backlog 大量项与 strategy 不匹配。

**对话输出**：

---

# 下一步建议

## 现在该做

| # | 主题 | 缺口 | 推荐技能 | 依据 | 优先级 | 停止条件 |
|---|---|---|---|---|---|---|
| 1 | 北极星指标 | 资产缺失 | `define-north-star` | NSM 缺失，无单一关键指标 | 下次 | 完成条件：north-star.md 写入并通过 `assess-docs` |
| 2 | 战略目标 | 资产缺失 | `design-strategic-goals` | strategic-goals 缺失（须含工程健康目标） | 下次 | 完成条件：strategic-goals.md 写入；上抛条件：与 NSM 冲突需重定义 |

## 其他可留意

| 主题 | 一句话概述 | 建议 |
|---|---|---|
| Backlog | 多项与战略不匹配 | 等战略层补齐再 `align-backlog`，避免基于未来要重定义的战略做对齐 |

## 诊断依据

- **项目情况**：战略已起草但战略层上游（北极星 / 战略目标）缺失，整体偏早期
- **资产清单**：

| 资产 | 路径 | 状态 | 质量 |
|---|---|---|---|
| mission | `docs/project-overview/mission.md` | present | high |
| vision | `docs/project-overview/vision.md` | present | medium |
| north-star | — | missing | — |
| strategic-goals | — | missing | — |
| roadmap | `docs/process-management/roadmap.md` | present | high |
| backlog | `docs/process-management/backlog/` | present | medium（与战略偏离） |
| ARTIFACT_NORMS | `docs/ARTIFACT_NORMS.md` | present | high |

- **判定规则**：Why 层 2 项 present / 3 项 missing，匹配"战略已起草"状态（S2）；What 层已有 roadmap 亦部分命中"路线已成、Backlog 稀薄"状态（S3）；按 tiebreak 取治理完整度维度上游（S2）。聚焦范围 = 战略层资产缺失。What 层漂移（backlog 与战略偏离）被聚焦规则降级为"其他可留意"，避免在上游未稳前做对齐。

---

### 示例 2：新项目起步（短路场景）

**场景**：新项目，`docs/ARTIFACT_NORMS.md` 不存在，`specs/` 为空，无 mission。

**对话输出**：

---

# 下一步建议

## 现在该做

| # | 主题 | 缺口 | 推荐技能 | 依据 | 优先级 | 停止条件 |
|---|---|---|---|---|---|---|
| 1 | 规范文件 | 资产缺失 | `discover-docs-norms` → `define-docs-norms` | ARTIFACT_NORMS 缺失，规范基础未建立 | **现在** | 完成条件：ARTIFACT_NORMS.md 落盘并验收后，重跑 plan-next |

## 其他可留意

（短路场景省略 —— 治理规则未建立时，下游资产创建无统一标准，扫描其他内容价值有限。补齐规范后重跑 plan-next 获得完整路由。）

## 诊断依据

- **项目情况**：新项目起步期，规范层与战略层都未建立，触发短路输出模式
- **资产清单**：

| 资产 | 状态 |
|---|---|
| ARTIFACT_NORMS | missing |
| specs/ | empty |
| mission / vision / NSM / goals / pillars | 全部 missing |
| 其他（计划 / 设计 / 实现） | 未扫描，短路触发 |

- **判定规则**：规范层缺位命中前置闸门，优先级最高，短路输出仅列一条路由。

---

### 示例 3：执行收尾、漂移可能（边缘场景）

**场景**：项目刚完成一次发布，最近 2 周多次 merge；上次 `align-planning` 报告是 18 天前，超过默认漂移过期阈值 14 天。

**对话输出**：

---

# 下一步建议

## 现在该做

| # | 主题 | 缺口 | 推荐技能 | 依据 | 优先级 | 停止条件 |
|---|---|---|---|---|---|---|
| 1 | 文档与代码对齐 | 真相漂移 | `align-planning` | 上次 align-planning 18 天前 > 14 天阈值；近期 3 次 merge 可能引入漂移 | 现在 | 完成条件：planning-alignment.md 更新并通过；上抛条件：发现 roadmap 与实际实现冲突需重定义 |

## 其他可留意

| 主题 | 一句话概述 | 建议 |
|---|---|---|
| ADR-015 | 缺"后果"节 | 做相关设计工作时顺手补；不阻塞 |
| 旧文档命名 | 2 个文件命名不符规范 | 下次 `tidy-repo` 时一并处理 |

## 诊断依据

- **项目情况**：执行收尾阶段，刚完成发布；漂移校准已过期，应优先触发对齐
- **资产清单**：（省略，全部 present，质量均中高）
- **判定规则**：近 14 天内有 merge/release + 上次 `align-planning` > 14 天，匹配"执行收尾、可能漂移"状态（S6）；聚焦 = 文档与代码漂移对齐（工作流动作型）。其他发现（设计文档不全、旧文档命名）不在聚焦内，归入"其他可留意"。
