---
name: align-backlog
description: Align the product or work backlog with the current strategy, goals, and roadmap. Analyze backlog items, identify misaligned or orphan work, and propose concrete changes (adds, cuts, reprioritization) so backlog clearly supports strategic outcomes.
description_zh: 将产品/工作待办与当前战略、目标、路线图对齐；分析待办项，识别脱节或孤儿工作，提出变更建议。
tags: [workflow, documentation]
version: 1.0.0
license: MIT
recommended_scope: both
aliases: [align-backlog-to-strategy]
metadata:
  author: ai-cortex
triggers: [align backlog, backlog alignment, backlog to strategy, align backlog to strategy]
input_schema:
  type: free-form
  description: Optional backlog location (path or convention), optional strategy docs root, optional scope (full backlog vs subset)
  defaults:
    scope: full
output_schema:
  type: document-artifact
  description: Backlog Alignment Report written to docs/calibration/backlog-alignment.md (default)
  artifact_type: backlog-alignment
  path_pattern: docs/calibration/backlog-alignment.md
  lifecycle: living
---

# 技能（Skill）：对齐待办事项列表

## 目的 (Purpose)

将产品或工作待办与当前战略、目标和路线图保持一致。根据战略来源分析现有的待办项目，识别错位或孤立的工作，并生成一份积压工作协调报告，其中包含具体的变更建议（添加、削减、合并、重新确定优先级），以便待办明确支持战略成果。

---

## 核心目标（Core Objective）

**首要目标**：生成一份可操作的待办事项调整报告，将待办事项映射到战略/目标/路线图，对调整状态进行分类，并建议具体的待办变更。

**成功标准**（必须满足所有要求）：

1. ✅ **找到待办事项和策略来源**：识别并解析待办事项和策略层文档（目标、路线图、里程碑）
2. ✅ **生成映射**：每个待办项目（或代表性样本）都映射到至少一个战略锚点（目标、里程碑、路线图主题）或标记为孤立/未映射
3. ✅ **未对齐分类**：项目按基本原理进行分类（对齐、部分、未对齐、孤儿）；根据调查结果说明影响和根本原因
4. ✅ **列出的更改建议**：提供具体建议（添加、删除、合并、重新确定优先级），并提供优先级和策略可追溯性
5. ✅ **报告持久化**：Backlog Alignment Report写入约定路径
6. ✅ **避免不安全写入**：如果待办位置不确定或建议的编辑具有破坏性，则在应用更改之前请求用户确认

**验收测试：产品或交付负责人能否阅读报告并立即了解哪些待办项目支持策略，哪些不支持策略，以及添加、删除或重新订购哪些内容？

---

## 范围边界（范围边界）

**本技能负责**：

- 积压库存和策略层发现
- 将待办项目映射到目标、里程碑和路线图
- 对对齐进行分类（对齐、部分、未对齐、孤儿）
- 提出具体的待办变更（添加、削减、合并、重新确定优先级）
- 保留待办事项调整报告

**本技能不负责**：

- 任务后追溯和规划漂移（使用“align-planning”）
- 架构与代码合规性（使用“align-architecture”）
- 定义或重写策略（使用`define-mission`、`设计-strategic-goals`、`define-routetu`等）
- 从头开始创建新的待办项目（使用“capture-work-items”或“analyze-需求”）
- 运行完整的策略检查点或治理周期（使用“run-checkpoint”）

**转交点**：报告生成后，根据需要转交给适当的技能 - 例如用于执行回溯的“align-planning”，或用于应用更改的产品/待办工具。

---

## 使用场景（用例）

- **待办事项健康检查**：定期确保待办事项跟踪当前策略
- **策略刷新后**：当目标、路线图或里程碑发生变化时重新调整待办处
- **冲刺或发布准备**：使用策略作为事实来源来确定待办事项的优先级和修剪
- **孤儿清理**：识别并建议删除或重新利用不再支持策略的工作

---

## 编排指导

|场景|推荐用途 |
| ---| ---|
|策略文档已更新 | `align-待办` 将待办重新映射到新目标/路线图 |
|待办事项让人感觉超载或偏离策略 |首先`align-待办`；如果还需要执行回溯，那么`align-planning`
|里程碑或释放门|为相关待办切片运行 `align-待办`；需要时通过“run-checkpoint”聚合治理状态 |

---

## 行为（行为）

### 代理即时合同


```text
You are responsible for backlog alignment with strategy.

Analyze the product or work backlog against the current strategy, goals, and roadmap.
Map items to strategic anchors, classify alignment, and produce a Backlog Alignment Report
with concrete change proposals (adds, cuts, reprioritization).
```


### 交互（互动）政策

- **默认**：来自项目规范或公共路径的待办事项（待办目录中的“docs/待办/”、“*.md”或项目约定）；来自“docs/project-overview/”、“docs/process-management/”的策略文档；范围 = 完整待办事项
- **选择选项**：非默认时显式待办路径和策略文档根；范围 = 当待办很大时的子集（例如通过史诗或标签）
- **确认**：在对待办文件提出编辑建议之前；在大剪切/合并建议之前

### 第 0 阶段：解决待办事项和战略来源

1. 解析待办位置（项目规范，`docs/ARTIFACT_NORMS.md`，或默认：`docs/待办/`，repo 待办约定）
2. 解决策略来源：目标、路线图、里程碑（例如`docs/project-overview/`、`docs/process-management/`）
3. 如果没有策略文档，则报告受阻，并建议先定义策略（`设计-策略-目标`、`定义-路线图`等）
4. 如果没有找到待办事项，报告被阻止并建议待办事项位置或“capture-work-items”来播种一个

### 第 1 阶段：将待办事项映射到战略

1. 列出待办事项（如果待办非常大，则为抽样集）
2. 对于每个项目，确定可追溯性：它支持哪个目标、里程碑或路线图主题（或标记孤立）
3. 记录映射和证据（例如标签、描述、链接）

### 第 2 阶段：分类对齐

对于每个项目（或按主题聚合）：

- **对齐**：明确支持当前目标/路线图/里程碑；优先级一致
- **部分**：支持战略，但优先级或范围可能需要调整
- **错位**：不再适合当前策略或与更高优先级的工作重复/冲突
- **孤儿**：没有可追踪的战略链接；削减或重新利用的候选人

包括每个发现的影响范围和根本原因。

### 第 3 阶段：提出变更建议

1. **剪切**：要删除或存档的项目（孤立的、被取代的或超出范围的）
2. **合并**：要合并或删除重复的项目
3. **重新确定优先级**：订单发生变化，因此最高战略价值显而易见
4. **添加**：待办中策略暗示尚未工作的差距（可选；仅作为建议列出）

每个提案必须引用策略（目标/路线图/里程碑）和项目 ID 或标题。

### 第 4 阶段：坚持报告

将报告写至：

- 项目规范或默认路径：`docs/calibration/待办-alignment.md`
- 或者用户指定的路径

报告必须包含用于对齐状态和更改建议的机器可读块（YAML 或 JSON）。

---

## 输入与输出 (Input & Output)

### 输入（输入）

- 可选的待办路径或惯例
- Optional strategy docs root
- 可选范围（史诗/标签/时间窗口的完整与子集）

### 输出（输出）

#### 待办事项调整报告模板


```markdown
# Backlog Alignment Report

**Date:** YYYY-MM-DD
**Backlog source:**
**Strategy sources:**
**Status:** aligned | partial | misaligned | blocked
**Confidence:** high | medium | low

## Summary
- Total items reviewed:
- Aligned:
- Partial:
- Misaligned:
- Orphan:

## Mapping (sample or full)
| Item | Strategic anchor | Status |
| --- | --- | --- |
| ... | ... | ... |

## Misalignment and Orphans
- Item / theme:
  Impact:
  Root cause:
  Recommendation: cut | merge | reprioritize | add

## Change Proposals
1. [Cut] ...
2. [Reprioritize] ...
3. [Merge] ...
4. [Add] ...

## Recommended Next Actions
1.
2.

## Machine-Readable Block

    alignment:
      summary: { aligned: N, partial: N, misaligned: N, orphan: N }
      items: []
    proposals:
      cut: []
      merge: []
      reprioritize: []
      add: []
```


---

## 限制（限制）

### 硬边界（Hard Boundaries）

- 当文档缺失时不要发明策略；报告被阻止并建议策略定义技能
- 未经用户明确批准，请勿默默编辑待办产品
- 不要执行规划层回溯（即“align-planning”）或架构合规性（即“align-architecture”）

### 技能边界 (Skill Boundaries)（避免重叠）

**不要做这些（其他技能可以处理它们）**：

- 任务后规划对齐和偏差检测 → `align-planning`
- 架构与代码合规性 → `align-architecture`
- 定义使命、目标、路线图→`定义-使命`、`设计-战略目标`、`定义-路线图`
- 从自由形式创建新工作项→“捕获工作项”、“分析需求”
- 里程碑或发布门处的全面治理检查点→“运行检查点”

**何时停止并交接**：

- 策略文档缺失或陈旧→建议“设计-策略-目标”、“定义-路线图”等。
- 用户需要在任务后执行回溯 → 移交给 `align-planning`
- 用户需要设计与代码检查→交给“align-architecture”

---

## 自检（Self-Check）

### 核心成功标准（必须满足所有标准）

- [ ] 确定和解析待办事项和策略来源
- [ ] 待办事项映射到战略锚点（或标记为孤儿）
- [ ] 对齐分类（对齐、部分、未对齐、孤儿）及其基本原理
- [ ] 列出可追溯的变更提案（剪切、合并、重新确定优先级、添加）
- [ ] 报告坚持约定的路径
- [ ] 在编辑或范围不确定的情况下要求用户确认

### 流程质量检查

- [ ] 使用时记录的默认路径和范围
- [ ] 每个提案引用策略来源和项目
- [ ] 报告中包含机器可读块
- [ ] 在适用时建议移交其他技能

### 验收测试

**产品或交付主管是否可以在没有额外说明的情况下对前 3-5 个变更提案采取行动？**

如果否：完善映射和提案理由。

如果是：报告完成；继续转交或待办更新。

---

## 示例（示例）

### 示例 1：策略刷新后的积压工作

**背景**：更新了战略目标和路线图； 待办有 50 多个项目。

**行为**：

1. 从 `docs/project-overview/`, `docs/process-management/` 加载目标和路线图
2. 从`docs/待办/`（或项目约定）加载待办
3. 将每个项目映射到目标/路线图主题或标记孤立项
4.分类：30个对齐，10个部分，5个未对齐，5个孤立
5. 建议：削减 5 个孤立主题，重新调整 10 个部分主题的优先级，合并 2 个重复主题
6. 保存报告到 `docs/calibration/待办-alignment.md`

### 示例 2：无策略文档

**背景**：项目没有目标或路线图文档。

**输出**：

- 状态：被阻止
- 消息：未找到策略文档。首先定义目标和路线图（例如`设计-策略-目标`，`定义-路线图`），然后重新运行align-待办。
- 置信度：不适用

### 示例 3：大量待办事项，子集范围

**上下文**：待办事项有 200 项；用户只想对齐“第二季度主题”。

**行为**：

1.解决待办及策略来源
2. 按Q2主题（标签或路径）过滤待办
3. 子集的映射和分类；报告指出“完整待办事项的子集”
4. 仅针对子集提出更改；建议稍后运行完整的待办事项