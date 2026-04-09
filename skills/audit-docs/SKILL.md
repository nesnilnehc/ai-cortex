---
name: audit-docs
description: Audit documentation governance in read-only mode and produce a unified report with prioritized actions and explicit skill routing.
description_zh: 以只读方式审计文档治理并输出统一报告，给出优先级行动与明确技能路由。
tags: [documentation, governance, orchestration, workflow, ssot]
version: 2.0.0
license: MIT
recommended_scope: project
metadata:
  author: ai-cortex
triggers: [docs governance, documentation governance, governance check, doc audit]
input_schema:
  type: free-form
  description: Project path, mode (full | quick | code-review), optional code-diff base branch
  defaults:
    mode: full
    code_diff: null
output_schema:
  type: document-artifact
  description: Unified governance report with compliance summary, risk map, and prioritized action plan
  artifact_type: audit-docs
  path_pattern: docs/calibration/audit-docs.md
  lifecycle: living
---

# 技能：文档治理审计（Audit Docs）

## 目的 (Purpose)

用只读方式整合文档治理现状，输出统一审计报告与行动路线图，不执行结构改造或规范落盘。

---

## 核心目标（Core Objective）

**首要目标**：产出可直接执行的治理审计报告（问题、优先级、路由），而不是直接改仓库。

**成功标准**（必须全部满足）：

1. ✅ 已完成模式对应的只读评估编排
2. ✅ 已汇总核心 findings 与风险优先级
3. ✅ 已输出明确的下一步技能路由
4. ✅ 已生成单一统一报告 `docs/calibration/audit-docs.md`
5. ✅ 未执行整理、迁移、规范落盘等写入操作

**验收测试**：团队是否能仅凭报告决定“下一步调用哪些技能”，且无需担心被隐式改仓库？

---

## 范围边界（Scope Boundaries）

**本技能负责**：

- 按模式编排只读评估技能
- 聚合评分、风险和行动优先级
- 生成统一治理报告

**本技能不负责**：

- 建立或更新规范文件（`define-docs-norms`）
- 仓库整理或文件迁移（`tidy-repo`）
- 自动接受并应用任何修改

**交接点**：报告完成后，交由用户选择是否执行创建/整理类技能。

---

## 使用场景（Use Cases）

- 新项目治理基线检查
- 发布前治理审计
- PR 合并前文档门禁
- 周期性治理体检

---

## 行为（Behavior）

### 模式定义

- `quick`：仅 `assess-docs`（核心评估）
- `full`：`assess-docs` + `assess-docs-links` + `assess-docs-ssot`
- `code-review`：`assess-docs` + `assess-docs-code-alignment`

### 执行步骤

1. 预检查：git 仓库可访问、docs 路径可读
2. 规范检查：若缺失 `docs/ARTIFACT_NORMS.md`，仅记录风险并路由 `discover-docs-norms`/`define-docs-norms`
3. 按模式执行只读评估技能并收集输出
4. 汇总评分（结构、就绪、链接、SSOT、代码对齐）
5. 生成 `docs/calibration/audit-docs.md`

---

## 输入与输出 (Input & Output)

### 输入

- 项目路径（默认 CWD）
- 模式：`quick|full|code-review`
- 可选 `code-diff`（用于 `code-review`）

### 输出

- `docs/calibration/audit-docs.md`
- 引用的下游报告（按模式）：
  - `docs/calibration/doc-assessment.md`
  - `docs/calibration/doc-link-health.md`
  - `docs/calibration/ssot-integrity-audit.md`
  - `docs/calibration/code-doc-alignment.md`

---

## 限制（Restrictions）

### 硬边界（Hard Boundaries）

- 不执行 `tidy-repo --apply` 或等价改写操作
- 不执行 `define-docs-norms` 落盘
- 不自动接受规范推导结果

### 技能边界 (Skill Boundaries)

**不要做这些（其他技能负责）**：

- 规范发现：`discover-docs-norms`
- 规范落盘：`define-docs-norms`
- 仓库整理：`tidy-repo`

---

## 自检（Self-Check）

- [ ] 模式对应编排正确
- [ ] 已汇总下游报告结论
- [ ] 已输出优先级路线图
- [ ] 未触发任何结构/规范写入
- [ ] 审计报告已落盘

---

## 示例（Examples）

### 示例 1：full 审计

- 执行：`assess-docs` + `assess-docs-links` + `assess-docs-ssot`
- 输出：`audit-docs.md` + 路由建议

### 示例 2：code-review 审计

- 执行：`assess-docs` + `assess-docs-code-alignment`
- 输出：聚焦 PR 的文档门禁建议
