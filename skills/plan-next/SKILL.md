---
name: plan-next
description: Analyze project governance state from mission/vision/backlogs and produce next-action plan. Use existing governance docs as input; when inputs are missing, recommend completing them first.
description_zh: 以存量 mission/vision/backlogs 等为输入源分析项目状态并产出下一行动建议；输入缺失时优先建议完善输入源。
tags: [workflow, meta-skill, automation]
version: 2.0.0
license: MIT
recommended_scope: project
metadata:
  author: ai-cortex
triggers: [plan next, next step, checkpoint, run checkpoint, governance, iteration]
input_schema:
  type: free-form
  description: Governance docs as input sources — mission, vision, north-star, strategic-goals, milestones, roadmap, backlog; optional trigger context
  defaults:
    sources: project canonical paths per docs/ARTIFACT_NORMS.md or spec/artifact-contract.md
output_schema:
  type: document-artifact
  description: Cycle report with input-source inventory, executed/skipped steps, and Recommended Next Tasks
  artifact_type: cognitive-loop
  path_pattern: docs/calibration/cognitive-loop.md
  lifecycle: living
---

# 技能：计划下一步（Plan Next）

## 目的 (Purpose)

以存量治理文档（mission、vision、backlogs 等）为输入源，分析项目治理状态并产出下一行动建议。若输入源缺失，优先将完善输入源作为行动建议。

---

## 核心目标（Core Objective）

**首要目标**：以存量治理文档为输入，产出可执行的下一行动建议与周期报告。

**成功标准**（须全部满足）：

1. ✅ **输入源盘点**：列出 mission、vision、north-star、strategic-goals、milestones、roadmap、backlog 的存在性与质量
2. ✅ **缺失优先**：当输入源缺失时，将完善输入源作为首要推荐行动（含对应技能与负责人）
3. ✅ **统一顺序执行**：输入源就绪时按固定顺序运行 alignment/doc readiness；输出驱动的条件决定后续技能
4. ✅ **决策可解释**：每个执行或跳过的步骤均有理由
5. ✅ **周期报告交付**：生成并持久化单一汇总报告
6. ✅ **无范围 bleed**：编排器本身不执行原子分析，仅聚合与路由

**验收测试**：他人能否仅凭此报告继续下一迭代，无需追问使用哪项技能或顺序？

**Scope Boundaries**：

- **本技能负责**：输入源盘点、准备门、场景编排、跨技能排序与转交、聚合到单一治理视图、建议下一周期行动
- **本技能不负责**：需求分析（`analyze-requirements`）、设计（`design-solution`）、对齐分析（`align-planning`）、架构合规（`align-architecture`）、文档差距分析（`assess-docs`）、修复执行（`run-repair-loop`）

**Handoff Point**：周期报告发布后，将具体执行移交给所属原子技能。

---

## 范围边界 (Scope Boundaries)

**本技能负责**：

- 输入源盘点（mission、vision、north-star、strategic-goals、milestones、roadmap、backlog）
- 规划准备门（discover-docs-norms、bootstrap-docs、assess-docs）
- 场景编排与跨技能排序、转交控制
- 产出聚合到单一治理视图
- 建议下一周期行动（含完善输入源）

**本技能不负责**：

- 需求分析内容（`analyze-requirements`）
- 设计内容（`design-solution`）
- 对齐分析本身（`align-planning`）
- 架构合规分析本身（`align-architecture`）
- 文档差距分析本身（`assess-docs`）
- 直接代码修复执行（`run-repair-loop`）

---

## 使用场景（Use Cases）

- **任务完成后**：在下一优先级前验证对齐与文档充分性
- **里程碑收尾**：运行全面治理检查
- **发布候选**：运行设计/对齐/文档准备门
- **定期迭代**：检查项目状态并获取下一步行动
- **输入源缺失**：发现 mission/vision/backlog 等缺失时，产出补齐输入源的建议

---

## 行为（Behavior）

### 输入源与默认路径

**标准输入源**（按 docs/ARTIFACT_NORMS.md 或 spec/artifact-contract.md 解析）：

| 输入源 | 典型路径 |
| :--- | :--- |
| mission | docs/project-overview/mission.md |
| vision | docs/project-overview/vision.md |
| north-star | docs/project-overview/north-star.md |
| strategic-goals | docs/project-overview/strategic-goals.md |
| milestones | docs/process-management/milestones.md |
| roadmap | docs/designs/*.md 或 docs/process-management/*roadmap* |
| backlog | docs/process-management/backlog.md、backlog/*.md |

### 阶段 0：输入源盘点

1. 遍历标准输入源，检查文件是否存在
2. 对存在的文件做简要质量判断（空、占位、有实质内容）
3. 输出**输入源清单**：存在/缺失、质量（present|placeholder|empty|missing）

**分支**：

| 状态 | 行动 |
| :--- | :--- |
| 任一核心输入源缺失 | 短路或轻量模式：产出周期报告，**首要推荐行动 = 完善缺失输入源**（指明技能：define-mission、define-vision、define-north-star、define-strategic-pillars、define-milestones、define-roadmap、align-backlog、capture-work-items 等） |
| 核心输入源就绪 | 进入阶段 0.5 与 1 |

### 阶段 0.5：规划准备门

在第一阶段前，确认项目是否有足够规划文档使 align-planning 有意义。若没有，运用准备技能或采用最小填充计划。

**诊断**：

1. 检查规范：`docs/ARTIFACT_NORMS.md` 或 `.ai-cortex/artifact-norms.yaml` 是否存在
2. 检查结构：`docs/` 是否有与规划相关的目录
3. 运行 `assess-docs` 获取就绪度与最小填充计划

**分支**：规范缺失 → discover-docs-norms；结构缺失 → bootstrap-docs；就绪度=缺失 → 短路，输出周期报告含最小填充计划与建议的后续任务。

### 阶段 1：统一序列 + 输出驱动分支

**仅在阶段 0/0.5 未短路时执行。**

固定顺序：`align-planning`（完整）→ `assess-docs`

输出驱动的后续（仅在输出表明需要时）：`run-repair-loop`、`design-solution`、`analyze-requirements`、`align-architecture`

用户覆盖优先。

### 阶段 2：执行与收集

对每个选定技能：记录选择理由、在进程中运行、捕获关键发现、记录跳过及原因、捕获阻碍与依赖。**单一制品规则**：仅生成一个周期报告，不单独产出原子技能报告。

### 阶段 3：综合治理报告

报告须含：触发与场景、执行/跳过顺序、按技能的汇总发现、战略/里程碑状态（若适用）、阻碍与置信度、**Recommended Next Tasks**（含完善输入源为首要建议时的具体任务与负责人）。

### 交互策略

- **默认**：从上下文推断触发器；使用项目规范的路径解析输入源
- **选项**：用户可指定范围覆盖或自定义序列
- **确认**：执行前范围覆盖或自定义序列时向用户确认

---

## 输入与输出 (Input & Output)

### 输入

- **存量治理文档**：mission、vision、north-star、strategic-goals、milestones、roadmap、backlog（按 docs/ARTIFACT_NORMS.md 或 spec/artifact-contract.md 解析）
- 可选：触发事件、目标范围、模式覆盖、紧急或发布窗口

### 输出

周期报告写入 `docs/calibration/cognitive-loop.md`（或项目规范路径），含：

- 输入源清单（存在/缺失、质量）
- 路由顺序与汇总发现
- 阻碍与置信度
- **Recommended Next Tasks**（优先级、可操作、负责人、范围、理由；输入源缺失时，完善输入源为首要任务）

---

## 限制（Restrictions）

### 硬边界（Hard Boundaries）

- 不得直接进行原子分析；仅聚合与路由
- 不得保留路由原子技能单独输出；单一制品
- 不得隐藏跳过的步骤；始终披露跳过原因
- 不得通过触发器路由；使用输出驱动分支
- 不得脱离收集的输出提出建议
- 必须给出明确的 Recommended Next Tasks（优先级、可操作性、负责人、理由）

### 技能边界 (Skill Boundaries)

**不要做这些（其他技能负责）**：

- 需求诊断 → `analyze-requirements`
- 设计与批准 → `design-solution`
- 漂移与校准 → `align-planning`
- 架构与代码合规 → `align-architecture`
- 文档差距评分 → `assess-docs`
- 自动修复循环 → `run-repair-loop`
- 规范建立 → `discover-docs-norms`
- 文档结构建立 → `bootstrap-docs`
- 定义使命/愿景等 → `define-mission`、`define-vision` 等

**When to Stop**：

- 周期报告完成 → 将操作移交给选定原子技能
- 缺少上下文阻止路由 → 请求最少触发澄清

---

## 自检（Self-Check）

### 核心成功标准（须全部满足）

- [ ] 输入源清单已产出（存在/缺失、质量）
- [ ] 输入源缺失时，完善输入源为首要推荐行动
- [ ] 阶段 0.5 已执行；短路或以正确理由进入阶段 1
- [ ] 不短路时执行统一顺序；产出驱动后续有理由
- [ ] 执行/跳过步骤清楚列出
- [ ] 汇总发现已捕获
- [ ] 周期报告已持久化
- [ ] 未直接进行原子分析

### 流程质量检查

- [ ] 输出驱动的后续分支
- [ ] 用户覆盖受尊重
- [ ] 交接含明确所有者和下一步
- [ ] 报告支持立即下一迭代

### 验收测试

他人能否仅凭此报告继续下一迭代？若否 → 完善顺序理由与行动清晰度。若是 → 输出完成。

---

## 示例（Examples）

### 示例 1：输入源缺失

- **阶段 0**：mission 存在，vision 存在，north-star 缺失，backlog 存在
- **行动**：短路或轻量模式；周期报告首要推荐 = 运行 `define-north-star` 补齐 north-star 文档
- **结果**：用户获得明确下一步，补齐后再运行完整循环

### 示例 2：输入源就绪，任务完成

- **阶段 0**：所有核心输入源存在且非空
- **阶段 0.5**：就绪度弱，进入阶段 1
- **阶段 1**：align-planning → assess-docs；输出驱动添加 run-repair-loop
- **结果**：对齐部分有效；文档填充计划；缺陷修复建议

### 示例 3：里程碑关闭，架构合规

- **阶段 0**：输入源完整
- **阶段 1**：align-planning → assess-docs；里程碑上下文添加 align-architecture
- **结果**：规划一致；发现架构合规缺口；指定修复缺陷
