---
name: assess-docs-code-alignment
description: Assess alignment gaps between code changes and required documentation updates.
description_zh: 评估代码变更与应更新文档之间的对齐缺口。
tags: [documentation, workflow, governance]
version: 1.0.0
license: MIT
recommended_scope: both
metadata:
  author: ai-cortex
triggers: [code docs alignment, docs alignment, code review docs]
input_schema:
  type: free-form
  description: Base branch or diff range, docs root, optional mapping rules
output_schema:
  type: document-artifact
  description: Code-to-doc alignment report
  artifact_type: code-doc-alignment
  path_pattern: docs/calibration/code-doc-alignment.md
  lifecycle: living
---

# 技能：代码文档对齐评估（Assess Docs Code Alignment）

## 目的 (Purpose)

检测代码改动是否有相应文档更新，输出可执行的补文档清单。

---

## 核心目标（Core Objective）

**首要目标**：从代码 diff 推断需要更新的文档，并报告未覆盖缺口。

**成功标准**：

1. ✅ 已解析代码 diff 范围
2. ✅ 已映射代码区域到文档区域
3. ✅ 已输出 missing/partial/covered 对齐结果
4. ✅ 已产出可执行补齐建议
5. ✅ 已写入 `docs/calibration/code-doc-alignment.md`

---

## 范围边界（Scope Boundaries）

**本技能负责**：代码变更与文档变更对齐分析。
**本技能不负责**：文档规范评估（`assess-docs`）、链接图（`assess-docs-links`）、SSOT（`assess-docs-ssot`）。

---

## 使用场景（Use Cases）

- PR 合并前文档门禁
- 发版前代码变更回查

---

## 行为（Behavior）

1. 获取 diff：`git diff <base>...HEAD --name-status --diff-filter=MAD`
2. 归类代码变更区域
3. 依据映射规则推断“应更新文档”
4. 对比当前分支文档改动
5. 输出 findings 与建议

---

## 输入与输出 (Input & Output)

### 输入

- `base` 或 diff 范围
- docs 根路径（可选）
- 区域映射规则（可选）

### 输出

- `docs/calibration/code-doc-alignment.md`

---

## 限制（Restrictions）

- 不修改代码与文档文件
- 仅输出评估和建议

---

## 自检（Self-Check）

- [ ] 已解析 diff
- [ ] 已产出缺口列表与建议
- [ ] 已写入单一对齐报告

---

## 示例（Examples）

- `src/api/auth.py` 修改但 `docs/architecture/api.md` 未更新 -> high
