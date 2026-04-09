---
name: plan-next
description: Analyze governance state and produce next-action routing plan from existing docs; default is planning-only (no downstream execution).
description_zh: 基于现有治理文档分析状态并输出下一步路由计划；默认仅规划，不执行下游技能。
tags: [workflow, meta-skill, automation]
version: 3.0.0
license: MIT
recommended_scope: project
metadata:
  author: ai-cortex
triggers: [plan next, next step, checkpoint, governance, iteration]
input_schema:
  type: free-form
  description: Governance docs sources, optional scope, optional execute flag
  defaults:
    execute: false
output_schema:
  type: document-artifact
  description: Cycle routing report with discovered sources, readiness gate result, and recommended next tasks
  artifact_type: cognitive-loop
  path_pattern: docs/calibration/cognitive-loop.md
  lifecycle: living
---

# 技能：计划下一步（Plan Next）

## 目的 (Purpose)

盘点治理输入源并生成下一步行动路由，默认只输出计划，不执行下游技能。

---

## 核心目标（Core Objective）

**首要目标**：提供可执行的下一步计划与技能路由，而不是在规划阶段隐式实施改动。

**成功标准**（必须全部满足）：

1. ✅ 已完成治理输入源发现与质量盘点
2. ✅ 已完成准备门判断并给出短路条件
3. ✅ 已输出优先级明确的 Recommended Next Tasks
4. ✅ 默认 `execute=false` 下未执行下游技能
5. ✅ 周期报告写入 `docs/calibration/cognitive-loop.md`

**验收测试**：报告是否能被他人直接用于执行，而无需再追问“接下来该跑哪些技能”？

---

## 范围边界（Scope Boundaries）

**本技能负责**：

- 输入源发现与盘点
- 准备门诊断
- 路由与优先级建议
- 周期报告聚合

**本技能不负责**：

- 默认模式下执行下游技能
- 规范创建、结构整理、修复执行

**交接点**：报告完成后，交由用户按建议顺序执行下游技能。

---

## 使用场景（Use Cases）

- 迭代收尾后的下一步规划
- 发布前治理路径确认
- 输入源缺失时的补齐路线设计

---

## 行为（Behavior）

### 阶段 0：治理输入发现

1. 扫描仓库并识别 mission/vision/north-star/strategic-goals/roadmap/backlog
2. 对每项给出路径、发现方式、置信度、质量
3. 标记缺失与占位文档

### 阶段 0.5：准备门诊断

1. 检查 `docs/ARTIFACT_NORMS.md` 是否存在
2. 检查 docs 结构是否可支持规划
3. 建议核心评估技能：`assess-docs`

### 阶段 1：路由建议生成

1. 按缺口类型生成技能路由：
   - 规范缺失：`discover-docs-norms` -> `define-docs-norms`
   - 结构问题：`tidy-repo`
   - 就绪不足：`assess-docs`
   - 规划漂移：`align-planning`
2. 输出优先级、负责人建议和停止条件

### 执行开关

- 默认：`execute=false`，仅输出计划，不运行下游技能
- 显式：`execute=true` 时才允许按路由执行

---

## 输入与输出 (Input & Output)

### 输入

- 治理文档上下文
- 可选 scope/mode 覆盖
- 可选执行开关 `execute=true|false`（默认 false）

### 输出

- `docs/calibration/cognitive-loop.md`
- 输入源清单 + 准备门结论 + 推荐路由任务

---

## 限制（Restrictions）

### 硬边界（Hard Boundaries）

- 默认模式不得执行下游技能
- 不直接生成原子技能报告
- 不隐藏跳过原因

### 技能边界 (Skill Boundaries)

**不要做这些（其他技能负责）**：

- 规范落盘：`define-docs-norms`
- 结构整理：`tidy-repo`
- 核心评估：`assess-docs`
- 漂移分析：`align-planning`

---

## 自检（Self-Check）

- [ ] 输入源清单完整
- [ ] 准备门判断明确
- [ ] 路由建议可执行且有优先级
- [ ] 默认模式未执行下游技能
- [ ] 周期报告已落盘

---

## 示例（Examples）

### 示例 1：默认规划模式

- 输入：`execute=false`
- 输出：仅路由计划，不执行任何下游技能

### 示例 2：显式执行模式

- 输入：`execute=true`
- 输出：按路由执行并在报告中记录执行结果
