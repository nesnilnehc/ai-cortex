---
name: assess-docs-links
description: Assess documentation link graph health including broken links, orphan docs, cycles, and deep chains.
description_zh: 评估文档链接图健康度，包括坏链、孤立文档、循环引用和过深引用链。
tags: [documentation, workflow, governance]
version: 1.0.0
license: MIT
recommended_scope: both
metadata:
  author: ai-cortex
triggers: [check links, docs links, docs graph]
input_schema:
  type: free-form
  description: Docs root, optional include patterns, optional depth threshold
output_schema:
  type: document-artifact
  description: Documentation link graph health report
  artifact_type: doc-link-health
  path_pattern: docs/calibration/doc-link-health.md
  lifecycle: living
---

# 技能：文档链接健康评估（Assess Docs Links）

## 目的 (Purpose)

检查文档之间的链接关系，识别坏链、孤立文档、循环与深链风险。

---

## 核心目标（Core Objective）

**首要目标**：输出一份可修复的链接健康报告。

**成功标准**：

1. ✅ 已构建文档链接图
2. ✅ 已识别坏链与孤立文档
3. ✅ 已识别循环引用和深链
4. ✅ 已给出修复建议
5. ✅ 已写入 `docs/calibration/doc-link-health.md`

---

## 范围边界（Scope Boundaries）

**本技能负责**：文档图健康。
**本技能不负责**：规范合规、code alignment、SSOT 审计。

---

## 使用场景（Use Cases）

- 发布前链接巡检
- 文档迁移后回归检查

---

## 行为（Behavior）

1. 扫描 Markdown/Wiki 链接
2. 构建有向图
3. 检测问题（broken/orphan/cycle/depth）
4. 汇总风险等级与修复建议

---

## 输入与输出 (Input & Output)

### 输入

- docs 根路径
- 可选路径过滤
- 可选深度阈值（默认 4）

### 输出

- `docs/calibration/doc-link-health.md`

---

## 限制（Restrictions）

- 不修改文档文件
- 不检查外部 URL 可达性（仅标记）

---

## 自检（Self-Check）

- [ ] 图构建完成
- [ ] 问题分类完整
- [ ] 报告落盘完成

---

## 示例（Examples）

- 文档 A 指向不存在文件 -> broken link
