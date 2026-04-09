---
name: assess-docs-ssot
description: Assess SSOT integrity with intent-first methodology and produce conflict matrix with canonical source mapping.
description_zh: 采用意图优先方法评估 SSOT 完整性，输出冲突矩阵与 canonical source 映射。
tags: [documentation, workflow, governance, ssot]
version: 1.0.0
license: MIT
recommended_scope: project
metadata:
  author: ai-cortex
triggers: [ssot audit, docs ssot, intent conflict]
input_schema:
  type: free-form
  description: Docs scope, optional conflict threshold, optional focus layers
output_schema:
  type: document-artifact
  description: SSOT integrity audit report with intent registry and conflict matrix
  artifact_type: ssot-integrity-audit
  path_pattern: docs/calibration/ssot-integrity-audit.md
  lifecycle: living
---

# 技能：SSOT 完整性评估（Assess Docs SSOT）

## 目的 (Purpose)

发现文档之间的语义重叠与冲突，建立 canonical source 与修复动作，降低重复与不一致风险。

---

## 核心目标（Core Objective）

**首要目标**：输出可执行 SSOT 审计报告（Intent Registry + Conflict Matrix + Repair Plan）。

**成功标准**：

1. ✅ 已完成意图建模（path_layer/artifact_type/ownership/granularity/section_intents）
2. ✅ 已完成候选对筛选与冲突判定
3. ✅ 已产出带优先级的冲突矩阵
4. ✅ 每个 P0/P1/P2 冲突都有 canonical source 与 repair action
5. ✅ 已写入 `docs/calibration/ssot-integrity-audit.md`

---

## 范围边界（Scope Boundaries）

**本技能负责**：SSOT 语义冲突审计。
**本技能不负责**：核心合规评分、链接图检查、代码文档对齐。

---

## 使用场景（Use Cases）

- full 治理审计
- 多目录文档重构前冲突排查

---

## 行为（Behavior）

1. 意图建模（Intent Registry）
2. 候选对筛选（意图重叠 + 粒度相近）
3. 分层相似度分析（section/doc/entity）
4. 冲突分级（P0/P1/P2/Info）
5. 输出 canonical mapping 与修复清单

---

## 输入与输出 (Input & Output)

### 输入

- docs 范围
- 可选冲突阈值
- 可选重点层

### 输出

- `docs/calibration/ssot-integrity-audit.md`

---

## 限制（Restrictions）

- 仅输出审计报告，不自动合并文档
- 不自动删除或移动文件

---

## 自检（Self-Check）

- [ ] Intent Registry 完整
- [ ] Conflict Matrix 完整
- [ ] 每个冲突含 canonical source + repair action
- [ ] 报告已落盘

---

## 示例（Examples）

- 两份 roadmap 文档里里程碑日期冲突 -> P0
