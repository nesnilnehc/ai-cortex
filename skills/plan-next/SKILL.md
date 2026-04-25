---
name: plan-next
description: Analyze governance state and produce next-action routing plan from existing docs; default is planning-only (no downstream execution).
description_zh: 基于现有治理文档分析状态并输出下一步路由计划；默认仅规划，不执行下游技能。
tags: [workflow, meta-skill, automation]
version: 9.2.0
license: MIT
recommended_scope: project
cognitive_mode: interpretive
metadata:
  author: ai-cortex
triggers: [plan next, next step, checkpoint, governance, iteration]
input_schema:
  type: free-form
  description: Governance docs sources, optional scope, optional threshold overrides.
  defaults:
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
  description: Three-section user-facing report — "Now do" (actionable routes), "Also watch" (other findings, capped at 5), "Diagnosis" (project status, asset inventory, decision rules). Internal codes (S1-S7, G1-G4, P0-P3) appear only in Diagnosis as traceability anchors.
---

# 技能：计划下一步（Plan Next）

> **角色**：治理入口路由器
> **WHAT**：按三步法 **扫**（盘点治理资产）→ **诊**（识别项目所处的治理阶段 7 态 + 资产缺陷 4 类）→ **荐**（产出三节路由报告）
> **HOW**：read-only 诊断；单一维度问题（只查就绪度 / 漂移 / 已知缺失）直接调专用技能（`assess-docs` / `align-planning` / `define-*` 等）
> **区别**：不同于 `assess-docs`（深度文档评估）或 `align-planning`（漂移校准），本技能仅做路由分发，不做深度分析

---

## 目的与边界

盘点治理输入源并生成下一步行动路由——**read-only**，永不执行下游技能。**入口路由器**：看全局、决定下一步跑哪个技能。

**适用时机**：迭代收尾 / 发布前治理路径确认 / 输入源缺失补齐 / 对下一步无头绪时。**不适用时可跳过**：单一维度问题（只查就绪度、只查漂移、已知某项缺失）直接跑专用技能。

### 边界

| 维度 | 做 | 不做 |
|---|---|---|
| 路由 | 输出"现在该做"治理路由建议 | 不充当 task 状态 API；不维护 task 列表 / 不分配；不记 task 历史，不答"本周晋升几条"类时序问题 |
| 执行 | read-only——产路由建议交用户或外层 orchestrator | 不自动推进下游；不充当 workflow engine——自动化由外层 orchestrator + `loop` 组合驱动 |

**Handoff**：路由产出后由用户按优先级执行下游；遇阻按"上抛条件"退回 plan-next 重评。

---

## 核心目标

**Primary Goal**：提供可执行的下一步计划与技能路由，不在规划阶段隐式实施改动。

**Acceptance Test**：报告的"现在该做"节是否可被他人直接用于执行，无需再追问"接下来该跑哪些技能"？

详细成功标准见 [Self-Check](#自检-self-check)。

---

## 行为（Behavior）

**整体规则**：**stateless**——每次从零重扫，不依赖上次结果。三步法：**扫（Scan）→ 诊（Diagnose）→ 荐（Recommend）**。

### 步骤 0：Norms Resolution

按 [artifact-contract §8.2](../../specs/artifact-contract.md#82-发现顺序) 顺序读项目规范到 `cache`：依序检查 `artifact_norms_path`（输入）→ `.ai-cortex/artifact-norms.yaml` → `docs/ARTIFACT_NORMS.md`，YAML 畸形则 HALT 诊断；缺失则继续不报错。`cache` 用于步骤 2.5 / 2.7 的 `path_pattern` 解析。

### 步骤 1：扫（Scan）— 资产盘点

**扫什么**：3 抽象层 × 5 主题（联合 MECE）。

| 抽象层 | 主题 | 扫描位置 | 细化字段 |
|---|---|---|---|
| 意图层 | **Why** | `docs/project-overview/{mission,vision,north-star,strategic-goals,strategic-pillars}.md` | — |
| 意图层 | **What/When** | `docs/process-management/{roadmap,backlog/}.md`、`docs/requirements/`、`docs/tasks/` | roadmap → Now/Next/Later 分层；tasks/ → `status` + `priority` |
| 意图层 | **How** | `docs/architecture/adrs/`、`docs/designs/` | — |
| 实施层 | **Is** | 仓库代码、git 历史 | 最近 N 天 commit、未合并 PR、最近 merge/release |
| 元规则层 | **Rules** | `docs/ARTIFACT_NORMS.md`、`specs/`、`protocols/`、`rules/` | — |

抽象层互斥；细化字段是同主题的辅助维度，**不是独立扫描**，供 §2.5 / §2.7 消费。

**怎么扫**——对每项资产记录 2 字段：

| 字段 | 判据 |
|---|---|
| **路径** | 文件系统路径 |
| **状态** | `present`（存在且内容非空非占位）/ `placeholder`（仅含 `[TODO]`/`<待填>`/`TBD`）/ `missing`（不存在） |

按需查询字段（不预扫）：S6 状态判定时单独读 `align-planning` 报告的最近 commit 时间；其他特定判据按需 git log。

### 步骤 2：诊（Diagnose）— 状态 + 缺口

**3 子步骤总览**（依次执行，每步可短路或下延）：

| 子步 | 做什么 | 产出 |
|---|---|---|
| 2.0 前置闸门 | Rules 层是否就位？ | 否则 short-circuit，仅输出"先建规范"路由 |
| 2.1 状态识别 | 项目处于哪个治理阶段（7 态 S1-S7）？ | 状态标签 + **聚焦范围**（S5 下钻 2.7） |
| 2.3 缺口判定 | 聚焦范围内有哪些缺口（4 类 G1-G4）？ | 缺口列表 → 矩阵路由 |

**协作关系**：状态机决定**看哪儿**（聚焦），缺口矩阵决定**那儿缺什么**（4 类），2.4 决策规则合并优先级 → "现在该做" 列表。

**辅助子步骤**：2.2 状态识别 fallback；2.5 / 2.6 Now tier 下游扫描细化（仅当聚焦含 Now tier 时介入）；2.7 S5 子状态机。

#### 2.0 前置闸门：Rules 层缺位检查

若 `ARTIFACT_NORMS.md` 缺失或 `specs/` 为空，触发 **short-circuit**：跳过状态识别，"现在该做"只列一条 P0 路由（建立规范 + 重跑 plan-next），"其他可留意"省略。

#### 2.1 状态识别（7 态状态机）

**为什么 7 态**：项目治理生命周期的 7 个有意义阶段——S1-S3 治理建立期（上游：愿景 → 路线 → backlog 充实）+ S4-S6 执行动态（下游：停滞 → 执行 → 收尾漂移）+ S7 稳定。从实证项目演进路径上识别出的可区分阶段。

| 状态 | 用户呈现 | 判定信号 | 聚焦 |
|---|---|---|---|
| S1 | **起步期** | Why 层全缺失或仅占位 | Why 层资产缺失 |
| S2 | **战略已起草** | Why ≥ 2 项 present；roadmap 缺 | 路线图缺失 |
| S3 | **路线已成、Backlog 稀薄** | roadmap present；backlog < `backlog_min_items` | Backlog 内容不全 |
| S4 | **Backlog 丰富但停滞** | roadmap+backlog 齐；无 in-progress；近 `commit_idle_days` 天无 commit | Pull ceremony（`prioritize-backlog` → `promote-roadmap-items`）|
| S5 | **执行中** | 有 in-progress task / 未合并 PR / 近期 commit | 任务 × 代码交叉判（见 §2.7）|
| S6 | **执行收尾、可能漂移** | 近期 merge/release；上次 `align-planning` > `drift_staleness_days` 天 | 文档代码漂移（`align-planning`）|
| S7 | **健康稳定** | 无缺口、无 in-flight、无漂移风险 | Quiet mode |

#### 2.2 低 confidence fallback

多个候选状态势均力敌（2.4 tiebreak 仍无法择一）→ 退化为全矩阵输出，诊断依据明示"状态未定"并列各候选支撑信号。

#### 2.3 缺口判定（4 类缺口矩阵）

**为什么 4 类**：从 4 个互斥维度刻画制品缺陷——**存在性**（有/无）× **完整性**（全/缺）× **一致性**（对齐/漂移）× **位置性**（合规/错位）。任意制品缺陷归属唯一一类（MECE）。

| 内部码 | 用户呈现 | 判据 | 动作 |
|---|---|---|---|
| G1 | **资产缺失** | 应存在但缺失 | DEFINE（`define-*`） |
| G2 | **内容不全** | 存在但未达就绪标准（占位、字段缺、链接断） | ASSESS（`assess-*`） |
| G3 | **真相漂移** | 与另一真相源冲突 | ALIGN（`align-*`） |
| G4 | **位置错位** | 内容合规但位置 / 命名 / 规范不符 | ORGANIZE（`tidy-repo` / `define-docs-norms`） |

**缺口路由矩阵**：

| 主题 | G1 资产缺失 | G2 内容不全 | G3 真相漂移 | G4 位置错位 |
|---|---|---|---|---|
| **Why** | `define-mission` / `define-vision` / `define-north-star` / `design-strategic-goals` / `define-strategic-pillars` | `assess-docs` → re-DEFINE | — | `tidy-repo` |
| **What/When** | `define-roadmap` / `analyze-requirements` / `capture-work-items` / `breakdown-tasks`（Now tier + design 已 present + task 未拆时） | `assess-docs` | `align-planning` / `align-backlog` | `tidy-repo` |
| **How** | `design-solution` | `assess-docs` | `align-architecture` | `tidy-repo` |
| **Is** | — | `review-*` | `assess-docs-code-alignment` | `tidy-repo` |
| **Rules** | `discover-docs-norms` → `define-docs-norms` | `audit-docs` | `align-planning` | `tidy-repo` / `curate-skills` |

记号：`/` 任选其一；`→` 链式调用；`—` 无自动路由（需人工判断，**不强行推荐**）。

#### 2.4 诊断决策规则

报告分层由三规则共同决定：

1. **多状态 tiebreak**：
   - **跨维度**：治理完整度（S1-S3）优先于执行态（S4-S7）——上游未稳时下游建议无意义
   - **治理维度内**：取上游（S1 > S2 > S3）——先补愿景再补计划
   - **执行维度内**：取下游（S6 > S5 > S4 > S7）——越后期越紧迫
2. **聚焦决定"现在该做"**：状态机聚焦内 → "现在该做"；外 → "其他可留意"
3. **优先级排序**：聚焦内按 现在 > 下次 > 以后 > 可忽略（内部 P0 > P1 > P2 > P3）

#### 2.5 Now tier 下游扫描

```
2.5.1 从步骤 0 cache 读各 artifact_type 的 path_pattern
      （命中用项目值；未命中 fall back 到技能默认 = §2 canonical）
2.5.2 按 Now tier 每条目的 slug 在各 path_pattern 目录 glob
      → 匹配到 = 下游存在；未匹配 = G1 缺口
2.5.3 (增强) 扫下游 frontmatter `parent:` 字段构反向索引补充信任度
2.5.4 (增强) 检测 manifest 文件（如 `now/<slug>.md`）
      → 存在则对比清单 vs 物理；差异作 G3 漂移
```

三层检测**独立可组合**——直接看物理信号。**项目定制**：

- 聚合式目录 → 在 `ARTIFACT_NORMS.md` 覆盖 `path_pattern` 为 `work/{slug}/<type>.md`
- 显式父指针 → 调用下游技能时传 `upstream_ref`
- 中央清单 → 建清单文件
- 不声明 → slug 默认生效

诊断依据需注明扫描依赖的物理信号组合（例："slug + 检测到 2 个 manifest + 无 parent 字段"）。

#### 2.6 Now tier 作用域（深度优先）

下游就绪度（requirement / design / task）评估**仅针对 Now tier 条目**：

- Now tier 无对应下游 → G1 真缺口
- Next/Later 无下游 → 正常状态，**不报告**
- Roadmap 未分层 → 先路由 `promote-roadmap-items`，**不评估下游**

**深度优先**：每个 Now tier 条目一次只报最上游缺口（requirement 缺 → 先补，不同时提 design / task）。

#### 2.7 S5 执行健康判定（任务 × 代码 2×2 交叉）

**概念位置**：本节是 §2.1 中 S5 的子状态机（在 7 态内）。5 类输出中 3 类漂移（追踪/完成/归档）属 G3 真相漂移子类、2 类（健康/卡点）属工作流动作型。

| 任务状态 | 代码活动 | 判定 | 归类 |
|---|---|---|---|
| in-progress | 近 `commit_idle_days` 天有 commit/PR 更新 | **健康执行** | S5 静默 |
| in-progress | 超 `task_stuck_days` 天无 commit/PR | **执行卡点** | `investigate-root-cause` + 人工 |
| todo | 有相关 commit/分支 | **追踪漂移** | `align-planning`（更新任务状态） |
| done | 无 merge 证据 | **完成漂移** | `align-planning` / 人工验证 |
| done | 已 merge 但未移出 in-progress 清单 | **归档漂移** | `tidy-repo` / `align-planning` |

- **Tiebreak**：多个卡点按任务自身 `priority` 排序——但**不参与** plan-next 路由 P0-P3
- **降级**：`task_source` 无可扫源时回退到仅看代码活动，诊断依据注明"任务源未配置"
- **路径解析**：扫描走步骤 0 cache 解析的 `path_pattern`（让 colocation 项目能扫到 `work/<slug>/tasks.md`）

### 步骤 3：荐（Recommend）— 路由生成与分层

**来源**：消费步骤 2 的产出。步骤 3 不引入新逻辑，只做**字段填充与呈现**。

**4 条指导原则**（详细规则见各引用节）：

1. **分层按聚焦** —— §2.4 / §3.3
2. **优先级按治理紧迫性** —— §3.1
3. **一条路由对一个矩阵格** —— §3.2
4. **深度优先 + 术语隔离** —— §2.6 / Anti-Patterns 内部术语节

#### 3.1 优先级（治理紧迫性）

- **现在（P0）**：阻断其他治理进展的根基问题（通常已被 2.0 闸门或 S1 聚焦吃掉）
- **下次（P1）**：战略层就绪度问题 / 计划层缺失或漂移
- **以后（P2）**：设计层 / 实现层任何缺口
- **可忽略（P3）**：其余

#### 3.2 每条路由六字段

主题 / 缺口类型 / 推荐技能 / 依据（指向具体资产）/ 优先级 / 停止条件。

**主题写法**：前两节用自然语言描述资产（"路线图"、"战略目标"、"规范文件"），不用作者视角分类词（详见 Anti-Patterns 内部术语节）。

**停止条件**三选一：

| 用户呈现 | 触发 |
|---|---|
| **完成条件** | 资产从 missing/incomplete/inconsistent 变 present/aligned |
| **延后条件** | 用户明确延后到下个周期 |
| **上抛条件** | 下游执行受阻（战略冲突、依赖循环），回 plan-next 重评 |

#### 3.3 用户输出三节

```
# 下一步建议

## 现在该做（1-3 条，六字段齐全）
...

## 其他可留意（≤5 条；超出折叠为 "+N more, use --full"）
...

## 诊断依据（末尾）
- 项目情况：<一句自然语言摘要>
- 资产清单：<表>
- 判定规则：<状态识别 + tiebreak + 聚焦范围；可括注 S 编号作追溯>
```

**用户 flag**：`--full` 强制全量展示；低 confidence 自动触发。

---

## Anti-Patterns

**关于职责边界**：

- ❌ 调用任何下游技能（read-only 硬边界）
- ❌ 隐藏跳过原因（short-circuit / 矩阵 `—` 时必须明示）
- ❌ 混入下游执行细节（不写 ADR、不修代码、不整结构）

**关于路由本身**：

- ❌ 矩阵 `—` 单元格强行推荐技能（明示需人工判断）
- ❌ 模糊措辞（"可能 / 或许 / 可以考虑"）
- ❌ 省略停止条件
- ❌ 一条路由混多个缺口类型
- ❌ 按缺口数量给优先级

**关于状态机与执行健康**：

- ❌ 用状态机折叠"其他可留意"（状态机是聚焦工具，不是过滤器；外部缺口必须呈现，无发现写"无"）
- ❌ 状态不明强行归类（应 fallback 到 §2.2）
- ❌ 仅凭单信号判执行健康（必须 §2.7 的 2×2 交叉）
- ❌ 用任务 priority 决定 plan-next 路由 P0-P3（仅供卡点间 tiebreak）

**关于 Now tier 与扫描**：

- ❌ 对 Next/Later tier 报下游缺口
- ❌ 同时报同一条目的多层缺口（违反深度优先）
- ❌ 引入 mode 枚举或配置字段（直接看物理信号）
- ❌ 承担下行清单维护职责（只读，差异作 G3；维护是 `align-work-item-manifest` 的事）

**关于内部术语泄漏**：

- ❌ 前两节使用 S1-S7 / G1-G4 / P0-P3 / 主题分类词（Why / What/When / How / Is / Rules）；主题列用自然语言（"路线图"、"战略目标"、"规范文件"）
- ❌ 诊断依据用 S 编号作主语（应用自然语言，S 编号至多括注追溯如"（S2）"）
- ❌ 示例标题写"S2 → S3 过渡"（用自然语言场景描述）

---

## 自检（Self-Check）

**扫**：

- [ ] cache 已加载或明示"no norms found"
- [ ] 资产 2 字段齐
- [ ] roadmap tier 已读

**诊**：

- [ ] 状态识别完成；tiebreak / fallback 已处理
- [ ] 聚焦范围已明示；S5 命中时已下钻 §2.7
- [ ] Now tier 物理信号扫描；Next/Later 未误报

**荐**：

- [ ] 六字段齐；停止条件齐
- [ ] P0>P1>P2>P3 排序
- [ ] 矩阵 `—` 未强推
- [ ] 深度优先

**输出**：

- [ ] 内部术语未泄漏前两节
- [ ] read-only 已遵守
- [ ] "其他可留意"≤5 条；short-circuit 时已省略
- [ ] 诊断依据注明扫描信号组合

---

## 示例（Examples）

### 示例 1：战略半成品（happy path）

**场景**：项目有 mission / vision；无 NSM / strategic-goals；roadmap 存在但 backlog 多项与 strategy 不匹配。

**输出**：

---

# 下一步建议

## 现在该做

| # | 主题 | 缺口 | 推荐技能 | 依据 | 优先级 | 停止条件 |
|---|---|---|---|---|---|---|
| 1 | 北极星指标 | 资产缺失 | `define-north-star` | NSM 缺失，无单一关键指标 | 下次 | 完成条件：north-star.md 写入并通过 `assess-docs` |
| 2 | 战略目标 | 资产缺失 | `design-strategic-goals` | strategic-goals 缺失 | 下次 | 完成条件：strategic-goals.md 写入；上抛：与 NSM 冲突需重定义 |

## 其他可留意

| 主题 | 概述 | 建议 |
|---|---|---|
| Backlog | 多项与战略不匹配 | 等战略层补齐再 `align-backlog` |

## 诊断依据

- **项目情况**：战略已起草但战略层上游缺失，整体偏早期
- **判定规则**：Why 层 2 项 present / 3 项 missing 匹配"战略已起草"（S2）；What 层 backlog 漂移命中 S3 但按 tiebreak 取治理上游 S2。聚焦 = 战略层缺失。What 层漂移降级到"其他可留意"

---

### 示例 2：新项目起步（短路场景）

**场景**：新项目，`docs/ARTIFACT_NORMS.md` 不存在，`specs/` 为空，无 mission。

**输出**：

---

# 下一步建议

## 现在该做

| # | 主题 | 缺口 | 推荐技能 | 依据 | 优先级 | 停止条件 |
|---|---|---|---|---|---|---|
| 1 | 规范文件 | 资产缺失 | `discover-docs-norms` → `define-docs-norms` | ARTIFACT_NORMS 缺失，规范基础未建立 | **现在** | 完成条件：ARTIFACT_NORMS.md 落盘后重跑 plan-next |

## 其他可留意

（短路场景省略——治理规则未建立时下游创建无统一标准。补齐规范后重跑 plan-next 获完整路由。）

## 诊断依据

- **项目情况**：规范层缺位，触发短路输出
- **判定规则**：Rules 层缺位命中 2.0 前置闸门，跳过状态识别

---

### 示例 3：执行收尾、漂移可能（边缘场景）

**场景**：项目刚发布，最近 2 周多次 merge；上次 `align-planning` 18 天前 > 14 天阈值。

**输出**：

---

# 下一步建议

## 现在该做

| # | 主题 | 缺口 | 推荐技能 | 依据 | 优先级 | 停止条件 |
|---|---|---|---|---|---|---|
| 1 | 文档与代码对齐 | 真相漂移 | `align-planning` | 上次 align-planning 18 天前 > 14 天；近期 3 次 merge 可能引入漂移 | 现在 | 完成条件：planning-alignment.md 更新；上抛：发现 roadmap 与实现冲突 |

## 其他可留意

| 主题 | 概述 | 建议 |
|---|---|---|
| ADR-015 | 缺"后果"节 | 做相关设计时顺手补，不阻塞 |
| 旧文档命名 | 2 个文件命名不符规范 | 下次 `tidy-repo` 时一并处理 |

## 诊断依据

- **项目情况**：执行收尾阶段；漂移校准已过期
- **判定规则**：近 14 天有 merge/release + 上次 align-planning > 14 天 → 匹配 S6；聚焦 = 漂移校准。其他发现归"其他可留意"
