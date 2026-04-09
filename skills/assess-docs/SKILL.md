---
name: assess-docs
description: Assess documentation core health in one pass — artifact norms compliance, layer readiness scoring, and minimum fill plan.
description_zh: 一次性评估文档核心健康：规范合规、分层就绪度评分与最小补齐计划。
tags: [documentation, workflow, governance]
version: 4.0.0
license: MIT
recommended_scope: both
metadata:
  author: ai-cortex
triggers: [doc readiness, documentation readiness, doc gap, validate docs]
input_schema:
  type: free-form
  description: Project docs scope, optional layer mapping, optional target readiness level
output_schema:
  type: document-artifact
  description: Documentation Assessment Report (compliance findings + layer readiness + minimum fill plan)
  artifact_type: doc-assessment
  path_pattern: docs/calibration/doc-assessment.md
  lifecycle: living
---

# 技能：文档评估（Assess Docs）

## 目的 (Purpose)

在单次运行中评估文档核心治理状态：是否符合规范、证据是否足够支撑规划、缺口应如何最小化补齐。

---

## 核心目标（Core Objective）

**首要目标**：输出一份可执行的文档评估报告，明确合规问题、层级就绪度和最小补齐行动。

**成功标准**（必须全部满足）：

1. ✅ 已解析项目规范（`docs/ARTIFACT_NORMS.md` 或默认契约）
2. ✅ 已完成路径/命名/front-matter 合规检查并给出 findings
3. ✅ 已完成层级就绪度评分（strong/weak/missing）
4. ✅ 已产出缺口优先级与最小补齐计划
5. ✅ 已写入单一报告 `docs/calibration/doc-assessment.md`

**验收测试**：团队是否能仅凭报告明确“先修什么、后补什么、由谁处理”？

---

## 范围边界（Scope Boundaries）

**本技能负责**：

- 规范合规检查（路径、命名、front-matter）
- 文档层级证据盘点与就绪度评分
- 缺口排序与最小补齐计划

**本技能不负责**：

- 规范创建/更新（使用 `define-docs-norms`）
- 代码-文档对齐分析（使用 `assess-docs-code-alignment`）
- 链接图健康分析（使用 `assess-docs-links`）
- SSOT 意图冲突审计（使用 `assess-docs-ssot`）
- 仓库结构改造（使用 `tidy-repo`）

**交接点**：核心评估报告完成后，按问题类型交给对应拆分技能做专项评估。

---

## 使用场景（Use Cases）

- 里程碑前文档就绪检查
- 规划前快速判断证据完整性
- 文档债务清单和优先级梳理

---

## 行为（Behavior）

### 阶段 0：规范与范围解析

1. 解析 docs 根路径
2. 读取 `docs/ARTIFACT_NORMS.md`；不存在则回退 `specs/artifact-contract.md`
3. 建立目标层映射（mission/vision/requirements/architecture/roadmap/backlog 等）

### 阶段 1：合规性验证

1. 扫描 docs 内 Markdown
2. 校验路径、命名、front-matter
3. 形成 findings（location/category/severity/title/description/recommendation）

### 阶段 2：层级证据盘点

1. 按层统计文档覆盖
2. 判断证据新鲜度与可用性
3. 标记每层状态（strong/weak/missing）

### 阶段 3：就绪度评分

1. 计算层级评分与总体 readiness（high/medium/low）
2. 标记关键阻断层

### 阶段 4：最小补齐计划

1. 按影响与工作量排序缺口
2. 形成最小行动集（先后顺序、责任建议、目标路径）

### 阶段 5：报告落盘

1. 写入 `docs/calibration/doc-assessment.md`
2. 输出“核心问题 + 建议下一步技能路由”

---

## 输入与输出 (Input & Output)

### 输入

- docs 范围（默认仓库 `docs/`）
- 可选层映射
- 可选目标就绪等级（`medium|high`）

### 输出

- `docs/calibration/doc-assessment.md`
- findings + readiness + minimum fill plan

---

## 限制（Restrictions）

### 硬边界（Hard Boundaries）

- 不执行仓库结构写操作
- 不创建或更新 `docs/ARTIFACT_NORMS.md`
- 不执行 code diff、links graph、SSOT 深度审计

### 技能边界 (Skill Boundaries)

**不要做这些（其他技能负责）**：

- 规范落盘：`define-docs-norms`
- 代码对齐：`assess-docs-code-alignment`
- 链接图：`assess-docs-links`
- SSOT 审计：`assess-docs-ssot`

---

## 自检（Self-Check）

- [ ] 已解析规范来源（项目规范或默认契约）
- [ ] 已输出完整合规 findings
- [ ] 已完成层级 readiness 评分
- [ ] 已产出最小补齐计划
- [ ] 仅生成核心评估报告，无专项扩展报告

---

## 示例（Examples）

### 示例 1：标准核心评估

- 输入：现有 docs
- 输出：`doc-assessment.md`（含合规+readiness+补齐计划）

### 示例 2：低就绪度项目

- 输入：仅有部分 roadmap/backlog 文档
- 输出：readiness=low，首要行动为补齐关键层文档
