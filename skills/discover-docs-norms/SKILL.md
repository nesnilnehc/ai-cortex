---
name: discover-docs-norms
description: Discover and propose project-specific artifact norms (paths, naming, lifecycle) from existing docs structure without writing norms files.
description_zh: 扫描并推导项目文档规范提案（路径、命名、生命周期），仅输出提案，不写入规范文件。
tags: [documentation, workflow]
version: 2.0.0
license: MIT
recommended_scope: project
metadata:
  author: ai-cortex
triggers: [discover norms, document norms]
input_schema:
  type: free-form
  description: Project path, optional docs root, optional confidence threshold
output_schema:
  type: document-artifact
  description: Norms discovery proposal report (no repository write)
  artifact_type: docs-norms-proposal
  path_pattern: docs/calibration/docs-norms-proposal.md
  lifecycle: living
---

# 技能：发现文档规范（Discover Docs Norms）

## 目的 (Purpose)

发现并提案项目级文档规范（路径、命名、front-matter、生命周期），为后续创建或更新规范文件提供输入依据。

---

## 核心目标（Core Objective）

**首要目标**：产出可审阅的规范提案，不执行规范落盘。

**成功标准**（必须全部满足）：

1. ✅ 已扫描目标 docs 范围并提取现有约定
2. ✅ 已输出规范提案（含路径映射、命名规则、front-matter 规则、置信度）
3. ✅ 已明确冲突项与低置信度项
4. ✅ 已给出下一步交接建议（`define-docs-norms`）
5. ✅ 未写入或覆盖 `docs/ARTIFACT_NORMS.md`

**验收测试**：是否可在不改动仓库结构的前提下，仅凭提案让团队评审并决定是否落盘？

---

## 范围边界（Scope Boundaries）

**本技能负责**：

- 扫描 docs 结构并推断文档治理约定
- 形成提案并标注置信度与冲突
- 输出建议的 canonical 规则与迁移提示

**本技能不负责**：

- 创建或更新 `docs/ARTIFACT_NORMS.md`（使用 `define-docs-norms`）
- 批量整理文件结构（使用 `tidy-repo`）
- 合规性评估和健康评分（使用 `assess-docs`）

**交接点**：提案确认后，交给 `define-docs-norms` 落盘规范。

---

## 使用场景（Use Cases）

- 项目首次治理前，需要先识别现有文档约定
- 规范争议时，需要生成可讨论的候选方案
- 多团队协作时，先统一候选规范再决定是否写入

---

## 行为（Behavior）

### 阶段 1：扫描与采样

1. 扫描 `docs/`（若不存在则扫描仓库内 Markdown）
2. 读取 front-matter、路径、文件名、标题
3. 提取 artifact_type、命名模式、日期模式、目录分布

### 阶段 2：规则推导

1. 生成 artifact_type -> path_pattern 候选映射
2. 推导命名规则（kebab/snake/camel、日期前缀策略）
3. 推导 front-matter 最小字段集合
4. 识别冲突分布（同类多路径、多命名风格）

### 阶段 3：置信度与风险评估

1. 对每项规则打分（0-100）
2. 标记低置信度（< 70）规则
3. 给出冲突裁决建议（保留哪个路径、迁移哪些文件）

### 阶段 4：输出提案（只读）

1. 生成 `docs/calibration/docs-norms-proposal.md`
2. 输出提案结构：规则表、冲突表、迁移建议、决策问题清单
3. 明确下一步：如需生效，执行 `define-docs-norms`

---

## 输入与输出 (Input & Output)

### 输入

- 项目路径（默认当前仓库）
- 可选 docs 根路径
- 可选置信度阈值

### 输出

- `docs/calibration/docs-norms-proposal.md`（规范提案）
- 不创建/更新 `docs/ARTIFACT_NORMS.md`

---

## 限制（Restrictions）

### 硬边界（Hard Boundaries）

- 未经用户显式要求，本技能不得写入 `docs/ARTIFACT_NORMS.md`
- 本技能不得执行仓库整理或文件移动
- 本技能不得将提案伪装成已生效规范

### 技能边界 (Skill Boundaries)

**不要做这些（其他技能负责）**：

- 规范落盘与变更：`define-docs-norms`
- 结构整理：`tidy-repo`
- 合规与就绪评估：`assess-docs`

---

## 自检（Self-Check）

- [ ] 已扫描目标 docs 范围并提取规则候选
- [ ] 已输出路径/命名/front-matter 提案
- [ ] 已标注低置信度与冲突项
- [ ] 已给出交接建议 `define-docs-norms`
- [ ] 未写入 `docs/ARTIFACT_NORMS.md`

---

## 示例（Examples）

### 示例 1：仅发现提案

- 输入：现有项目 `docs/` 结构
- 输出：`docs/calibration/docs-norms-proposal.md`
- 后续：评审通过后调用 `define-docs-norms`

### 示例 2：存在多套冲突目录

- 输入：同时存在 `docs/design/` 与 `docs/design-decisions/`
- 输出：冲突裁决建议 + 迁移清单
- 后续：由 `define-docs-norms` 固化 canonical 规则
