---
name: align-work-item-manifest
description: Detect drift between project work-item manifest files and the physical artifacts they register (requirements / designs / tasks / PRs). Advisory-only in v1.0.0 — reports drift, does not auto-write.
description_zh: 检测项目的工作项清单文件（work-item manifest）与其登记的物理制品之间的漂移。v1.0.0 advisory-only——只报告漂移，不自动修复。
tags: [workflow, documentation, governance, alignment]
version: 1.0.0
license: MIT
recommended_scope: project
metadata:
  author: ai-cortex
triggers: [align manifest, work item manifest, manifest drift, linking mode manifest]
input_schema:
  type: free-form
  description: Project path; optional manifest glob pattern (default from ARTIFACT_NORMS.md or docs/process-management/now/*.md); optional artifact_norms_path override
output_schema:
  type: document-artifact
  description: Work-item manifest alignment report with drift findings, fix suggestions, and G3 drift anchors for plan-next consumption
  artifact_type: work-item-manifest-alignment
  path_pattern: docs/calibration/work-item-manifest-alignment.md
  lifecycle: living
---

# 技能：对齐工作项清单（Align Work-Item Manifest）

> **用途**：当项目使用**中央清单文件**（如 `docs/process-management/now/<slug>.md`）登记相关制品时，检测清单文件与物理制品的漂移。

## 目的 (Purpose)

中央清单风格的项目为每个主题或 Now tier 条目维护一份清单文件（如 `docs/process-management/now/<slug>.md`）登记关联的 requirement / design / tasks / PR。清单容易漂移：文件新增未登记、文件删除未清除、清单列了但物理文件不存在。本技能**只读**检测这些漂移并输出对齐报告；维护由用户或下游工具完成。

v1.0.0 **advisory-only**：不自动写清单、不移动文件、不修改 frontmatter。

---

## 核心目标（Core Objective）

**首要目标**：准确检测清单-物理漂移并输出可操作的差异清单。

**成功标准**（必须全部满足）：

1. ✅ 已扫描项目中所有符合清单 glob（默认 `docs/process-management/now/*.md`，可由 ARTIFACT_NORMS.md 覆盖）的文件；若**无清单文件存在**，明示项目未采用中央清单风格，停止并返回诊断
2. ✅ 已对每份清单对比其声明的文件列表与物理文件的存在性
3. ✅ 已输出三类漂移：**悬挂引用**（清单有，文件无）/ **未登记**（文件有，清单无）/ **命名不符**（文件路径与清单声明不一致）
4. ✅ 未自动写任何清单或制品

**验收测试**：报告是否可被 `plan-next` 作为 G3 真相漂移直接消费？

---

## 范围边界（Scope Boundaries）

**本技能负责**：

- 清单扫描与物理文件存在性对比
- 漂移分类与报告产出
- 给出**建议性**修复步骤（不执行）

**本技能不负责**：

- **维护清单**（用户或未来 v2.x 的自动维护机制）
- 链接模式识别（由 `discover-docs-norms`）
- 链接模式选择（由 `define-docs-norms`）
- 下游文件的实际创建 / 删除 / 移动

**Handoff Point**：漂移报告输出后，由用户手动修正清单 / 文件，或由 `plan-next` 的 G3 路由进一步路由到 `align-planning` / `tidy-repo`。

---

## 使用场景（Use Cases）

- 中央清单风格的项目定期健康检查
- plan-next 报告 G3 漂移且检测到清单文件时的深入诊断
- 迭代收尾前清单盘点
- 从无清单迁移到中央清单风格后的初次对齐

---

## 行为（Behavior）

### 第 0 阶段：Norms Resolution

按 [specs/artifact-contract.md §8 Runtime Norms Resolution Protocol](../../specs/artifact-contract.md#8-runtime-norms-resolution-protocol) 的 §8.2 / §8.3 / §8.5 实现：

1. 读项目规范 → 确定本技能产出 `work-item-manifest-alignment` 的 `path_pattern`（默认 `docs/calibration/work-item-manifest-alignment.md`）
2. 从规范读取 manifest glob 模式（默认 `docs/process-management/now/*.md`；可由 ARTIFACT_NORMS.md 覆盖）
3. **前置检查**：若 manifest glob 未匹配到任何文件，**停止并输出诊断**说明项目未采用中央清单风格
4. 本技能为固定路径治理产出，不涉及路径之外的模式分支

### 第 1 阶段：清单扫描

1. 按 Step 0 得到的 manifest 位置模式 glob 所有清单文件
2. 对每份清单，解析其列出的子制品引用（requirement / design / tasks / PR）
3. 构建清单声明映射：`manifest → [declared_file_paths]`

### 第 2 阶段：物理对比

1. 对每个 `declared_file_path` 检查物理存在
2. 扫描清单覆盖目录（如 requirements / designs / tasks 目录）列出所有实际物理文件
3. 交叉对比：
   - **悬挂引用**：清单列但物理无
   - **未登记**：物理有但无清单列出
   - **命名不符**：清单声明 `docs/foo/bar.md`，实际文件在 `docs/foo/bar-v2.md`（模糊匹配同 slug）

### 第 2.5 阶段：漂移检测决策分支（Decision Branches）

| 分支 ID | 触发条件 | 判定结果 | 报告动作 |
|---|---|---|---|
| D1-no-manifest | manifest glob 无任何匹配 | 项目未采用中央清单风格 | 停止流程，返回诊断信息，不写报告文件 |
| D2-declared-missing | `declared_file_path` 不存在 | 悬挂引用 | 记入“悬挂引用”分组，建议删除清单条目或补建文件 |
| D3-physical-unregistered | 物理文件存在但未被任何清单声明 | 未登记 | 记入“未登记”分组，建议追加到清单或归档文件 |
| D4-slug-mismatch | 清单路径不存在，但存在同 slug 的候选文件 | 命名不符 | 记入“命名不符”分组，建议更新清单路径或重命名文件 |
| D5-consistent | 清单声明与物理文件一一对应 | 无漂移 | 不记录问题，仅累计“已对齐项”计数 |
| D6-parse-error | 清单内容无法解析出声明路径 | 数据质量异常（非三类漂移） | 记入诊断附录并标记需人工修复清单格式 |

> 判定优先级：`D1 > D6 > D2/D4 > D3 > D5`。当同一声明同时命中多个条件时，按优先级取首个分支，避免重复计数。

### 第 3 阶段：报告产出

写入 Stage 0 解析的路径（默认 `docs/calibration/work-item-manifest-alignment.md`）：

```markdown
# 工作项清单对齐报告

**日期**：<ISO>
**清单数量**：<N>
**漂移总数**：<M>（悬挂 <X> / 未登记 <Y> / 命名不符 <Z>）

## 悬挂引用（清单有，文件无）

| 清单 | 清单声明路径 | 建议 |
|---|---|---|
| ... | ... | 删除清单条目 or 创建缺失文件 |

## 未登记（文件有，清单无）

| 文件 | 疑似所属清单 | 建议 |
|---|---|---|
| ... | ... | 追加到清单 or 归档文件 |

## 命名不符（同 slug，路径异）

| 清单声明 | 物理文件 | 建议 |
|---|---|---|
| ... | ... | 更新清单路径 or 重命名文件 |
```

---

## 输入与输出 (Input & Output)

**输入**：
- 项目路径（默认 CWD）
- 可选 manifest glob pattern（覆盖规范）
- 可选 `artifact_norms_path`

**输出**：
- `docs/calibration/work-item-manifest-alignment.md`（默认）或规范声明的路径
- 机器可读漂移摘要（嵌在报告里作 YAML fence）供 `plan-next` 消费

---

## 限制（Restrictions）

### 硬边界（Hard Boundaries）

- **只读**：v1.0.0 不写任何清单文件、不创建 / 删除 / 移动任何制品
- 无物理 manifest 文件时必须停止并诊断说明
- 不自行识别链接模式（依赖 `discover-docs-norms` 的产出）
- 不越权触发下游技能（`tidy-repo` / `align-planning` 由用户或 `plan-next` 路由）

### 技能边界 (Skill Boundaries)

| 动作 | 归属 |
|---|---|
| 模式识别 | `discover-docs-norms` |
| 模式选择 | `define-docs-norms` |
| 清单维护（自动） | 未来 v2.x 或下游技能职责 |
| 文件归档 / 重命名 | `tidy-repo` |
| 规划漂移修正 | `align-planning` |

---

## 自检（Self-Check）

- [ ] 已按 Stage 0 Norms Resolution 读项目规范
- [ ] 已 glob manifest 文件；若无匹配，已停止并诊断（项目未用中央清单）
- [ ] 已扫描全部清单文件并对比物理
- [ ] 已分类三类漂移（悬挂 / 未登记 / 命名不符）
- [ ] 报告嵌入机器可读漂移摘要供 plan-next 消费
- [ ] 未自动修改任何清单 / 文件

---

## 示例（Examples）

### 示例 1：纯 manifest 项目健康检查

**场景**：项目使用中央清单风格；存在 3 份清单文件 `docs/process-management/now/user-auth.md` / `billing.md` / `onboarding.md`。

**扫描发现**：
- `now/user-auth.md` 列了 `docs/designs/user-auth.md`，但该文件已被重命名为 `docs/designs/2026-04-20-user-auth.md` → **命名不符**
- `now/billing.md` 清单完整，所有文件存在 → 无漂移
- `docs/designs/onboarding-v2.md` 存在但 `now/onboarding.md` 未列 → **未登记**

**输出**：报告 2 条漂移；建议 `now/user-auth.md` 更新路径、`now/onboarding.md` 追加 `onboarding-v2.md` 条目。

### 示例 2：项目未采用中央清单（边缘场景）

**场景**：项目仓库里无 `docs/process-management/now/*.md` 或等价清单文件。

**输出**：Stage 0 前置检查不通过，停止并输出：

```
未检测到任何 manifest 文件（glob: docs/process-management/now/*.md）。
本技能适用于采用中央清单文件登记制品的项目；当前项目未见此风格文件。
如需启用，可手动建清单文件（例：docs/process-management/now/user-auth.md），再重跑本技能。
```

不写报告文件；返回诊断信息。
