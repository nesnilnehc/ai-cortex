---
name: define-docs-norms
description: Create or update docs/ARTIFACT_NORMS.md from an approved proposal and establish project docs norms as canonical rules.
description_zh: 基于已确认提案创建或更新 docs/ARTIFACT_NORMS.md，建立项目文档规范的单一权威来源。
tags: [documentation, workflow]
version: 1.0.0
license: MIT
recommended_scope: project
metadata:
  author: ai-cortex
triggers: [define docs norms, create docs norms, apply norms]
input_schema:
  type: free-form
  description: Approved norms proposal, optional existing ARTIFACT_NORMS.md, optional merge strategy
output_schema:
  type: document-artifact
  description: Canonical docs norms file
  artifact_type: governance
  path_pattern: docs/ARTIFACT_NORMS.md
  lifecycle: living
---

# 技能：定义文档规范（Define Docs Norms）

## 目的 (Purpose)

将已审阅的规范提案固化为 `docs/ARTIFACT_NORMS.md`，并作为项目文档治理的 canonical 规则。

---

## 核心目标（Core Objective）

**首要目标**：安全、可审计地创建或更新项目规范文件。

**成功标准**（必须全部满足）：

1. ✅ 输入提案已明确并可落盘
2. ✅ 规范文件结构符合项目 schema 与约定
3. ✅ 变更说明清晰（新增、修改、删除规则）
4. ✅ 写入目标仅限 `docs/ARTIFACT_NORMS.md`
5. ✅ 输出后可被 `assess-docs` 等技能直接消费

**验收测试**：规范文件是否可直接作为路径/命名/front-matter 校验依据，并被其他技能稳定解析？

---

## 范围边界（Scope Boundaries）

**本技能负责**：

- 创建或更新 `docs/ARTIFACT_NORMS.md`
- 合并已有规范与新提案（可配置策略）
- 输出变更摘要与迁移提示

**本技能不负责**：

- 规范发现与推导（使用 `discover-docs-norms`）
- 仓库整理与文件迁移（使用 `tidy-repo`）
- 合规审计与就绪评分（使用 `assess-docs`）

**交接点**：规范写入后，交给 `assess-docs` 做合规评估，交给 `tidy-repo` 做结构整改。

---

## 使用场景（Use Cases）

- 新项目首次建立 `ARTIFACT_NORMS`
- 旧项目将提案升级为正式规则
- 规范迭代更新（路径、命名、字段政策）

---

## 行为（Behavior）

### 阶段 1：输入确认

1. 读取提案（通常来自 `docs/calibration/docs-norms-proposal.md`）
2. 检查是否存在旧版 `docs/ARTIFACT_NORMS.md`
3. 确认落盘策略：`create | merge | replace`

### 阶段 2：规范组装

1. 组装路径映射、命名策略、front-matter 标准
2. 写入低置信度规则的人工确认注记（如有）
3. 校验格式一致性与可解析性

### 阶段 3：落盘与摘要

1. 写入 `docs/ARTIFACT_NORMS.md`
2. 输出本次变更摘要（新增/修改/删除）
3. 输出后续建议：`assess-docs` 与 `tidy-repo`

---

## 输入与输出 (Input & Output)

### 输入

- 已审阅规范提案
- 可选已有 `docs/ARTIFACT_NORMS.md`
- 可选合并策略（`create|merge|replace`）

### 输出

- `docs/ARTIFACT_NORMS.md`
- 变更摘要

---

## 限制（Restrictions）

### 硬边界（Hard Boundaries）

- 仅允许写入规范文件，不执行仓库结构改造
- 输入提案不明确时停止并要求确认
- 不得把未确认冲突规则标记为已定稿

### 技能边界 (Skill Boundaries)

**不要做这些（其他技能负责）**：

- 发现与推导：`discover-docs-norms`
- 合规评分：`assess-docs`
- 文件整理：`tidy-repo`

---

## 自检（Self-Check）

- [ ] 已接收可落盘的规则输入
- [ ] 已正确写入 `docs/ARTIFACT_NORMS.md`
- [ ] 已输出规则变更摘要
- [ ] 未执行非规范文件写入

---

## 示例（Examples）

### 示例 1：从提案新建规范

- 输入：`docs/calibration/docs-norms-proposal.md`
- 行为：`create`
- 输出：`docs/ARTIFACT_NORMS.md`

### 示例 2：对旧规范增量更新

- 输入：旧规范 + 新提案
- 行为：`merge`
- 输出：更新后的规范文件 + 变更摘要
