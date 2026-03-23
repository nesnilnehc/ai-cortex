---
name: design-solution
description: Produce a validated design document from requirements (architecture, components, data flow, trade-offs) with no implementation. Use when requirements are clear and you need a single source of truth for downstream task breakdown.
description_zh: 从需求产出验证过的设计文档（架构、组件、数据流、权衡）；不含实现；用于下游任务拆解。
tags: [writing, documentation]
version: 1.1.1
license: MIT
recommended_scope: both
metadata:
  author: ai-cortex
  evolution:
    sources:
      - name: "design-solution"
        repo: "https://github.com/nesnilnehc/ai-cortex"
        version: "1.0.0"
        license: "MIT"
        type: "reference"
        borrowed: "Phase-based validation, HARD-GATE, trade-off framework, design doc structure"
    enhancements:
      - "Explicit input: requirements document (from analyze-requirements)"
      - "Output contract: design as single source of truth for breakdown-tasks"
      - "Strict no-implementation boundary"
triggers: [design solution, design from requirements, design doc]
input_schema:
  type: document-artifact + optional free-form
  description: Validated requirements document (e.g. requirements.md or docs/requirements-planning/<topic>.md); optional project context
output_schema:
  type: document-artifact
  description: Design document per [spec/artifact-contract.md](../../spec/artifact-contract.md)
  artifact_type: design
  path_pattern: docs/design-decisions/YYYY-MM-DD-{topic}.md
  lifecycle: snapshot
---

# 技能（Skill）：设计解决方案

## 目的 (Purpose)

将已验证需求转化为单一的、免实施的设计文档。该设计描述了架构、组件、数据流和权衡，以便下游技能（例如“分解任务”）可以毫无歧义地导出可执行任务列表。

---

## 核心目标（Core Objective）

**首要目标**：根据需求制作一份已验证的设计文档，作为实施规划的唯一事实来源；没有生成任何代码或实现步骤。

**成功标准**（必须满足所有要求）：

1. ✅ **设计文档已批准并保留**：写入“docs/design-decisions/YYYY-MM-DD-<topic>.md”（或每个“docs/ARTIFACT_NORMS.md”的项目约定路径）、已提交且用户明确批准
2. ✅ **需求可追溯性**：设计明确引用或总结其满足的需求
3. ✅ **已记录的替代方案**：至少考虑 2-3 种方法并进行权衡（优点/缺点/最佳方案）
4. ✅ **错误处理和测试策略**：关键失败路径和验证方法（测试方法，而不是测试代码）已记录
5. ✅ **无实施**：零代码、脚手架或实施任务； 仅设计
6. ✅ **下游就绪**：读者可以将设计分解为具有依赖性和验收标准的任务，而无需提出澄清问题

**验收测试**：有人可以单独使用这个设计文档来生成完整的、有序的任务列表（例如通过“breakdown-tasks”）而不提出澄清问题吗？

---

## 范围边界（范围边界）

**本技能负责**：

- 需求文档→设计文档（架构、组件、数据流、接口）
- 权衡分析和替代方法
- 设计批准和持久性作为实施规划的单一事实来源

**本技能不负责**：

- 引出或验证需求（使用“分析需求”）
- 将设计转化为任务列表（使用“breakdown-tasks”）
- 编写代码或实现（任何实现技能）
- 没有需求文档的粗略想法设计（使用此技能以粗略想法作为输入）

**转交点**：当设计被批准并坚持时，将其移交给`breakdown-tasks`来生成tasks.md（或同等文件）。

---

## 使用场景（用例）

- **后期需求设计**：您有一份已验证的需求文档，需要在实施前进行详细的设计。
- **来自需求的架构**：需求明确；您需要组件边界、数据流和技术权衡。
- **单一事实来源**：您需要一份可供实施和任务分解依赖的设计文档。

---

## 行为（行为）

### 交互（互动）政策

- **默认**：需要需求产品（路径或内容）；如果存在，则使用设计路径的项目规范
- **选择选项**：澄清时一次一个问题；在有用的地方提供“[A][B][C]”作为设计选择
- **确认**：转交前必须用户同意设计；未获批准前不予实施

### 硬门：无实施


```text
DO NOT write code, scaffold projects, or produce implementation steps.
Output is design documentation only. Implementation is downstream (e.g. breakdown-tasks then execution).
```


### 第 1 阶段：摄取要求

1. **负载需求**：阅读需求文档（例如需求.md或docs/requirements-planning/*.md）。
2. **确认范围**：与用户简要确认此需求文档是本设计的范围（或同意子集）。
3. **识别约束**：从需求中提取约束、验收标准和范围外的项目。

### 第 2 阶段：探索替代方案和权衡

1. **提出 2-3 种方法**：满足需求的架构/组件/数据流选项。
2. **记录权衡**：对于每个选项：优点、缺点、“最适合”。
3. **推荐**：说明推荐的方法和理由；请用户选择或调整。

### 第 3 阶段：生成设计文档

1. **结构**：目标、架构、组件、数据流、错误处理策略（关键故障路径）、测试策略（验证方法，而不是测试代码）、考虑的权衡、验收标准（可追溯到需求）。
2. **Scale to Complexity**：简单范围的缩写；需要时提供更多细节，以便任务分解明确。
3. **解析路径**：先检查`docs/ARTIFACT_NORMS.md`（项目覆盖）；默认后备是每个 [spec/artifact-contract.md](../../spec/artifact-contract.md) 的 `docs/design-decisions/YYYY-MM-DD-<topic>.md`。
4. **编写并保存**：保存带有前置内容的设计（`artifact_type: 设计`、`created_by: 设计解决方案`、`lifecycle: snapshot`、`created_at`）。

### 第 4 阶段：批准和移交

1. **用户批准**：在宣布完成之前获得明确批准。
2. **Handoff**：建议使用此设计的“breakdown-tasks”作为输入来生成tasks.md。

---

## 输入与输出 (Input & Output)

|角色 |内容 |
| :--- | :--- |
| **输入** |需求文档（路径或内容）；可选的项目背景、现有设计或 ADR |
| **输出** |设计文档位于“docs/design-decisions/YYYY-MM-DD-<topic>.md”（或每个“docs/ARTIFACT_NORMS.md”的项目路径）；实施和任务分解的单一事实来源|

---

## 限制（限制）

### 硬边界（Hard Boundaries）

- **无实施**：不生成代码、文件布局或分步实施说明。
- **需求第一**：当需求模糊或缺失时，不要运行此技能；首先移交给“分析需求”。
- **仅设计**：不生成任务列表；为此，请移交给“分解任务”。

### 技能边界 (Skill Boundaries)（避免重叠）

**不要做这些（其他技能可以处理它们）**：

- 需求获取或验证→“分析需求”
- 任务分解或计划 → `分解任务`
- 代码实施或重构→实施技巧

---

## 自检（Self-Check）

- [ ] 设计文档已批准并保留：写入“docs/design-decisions/YYYY-MM-DD-<topic>.md”（或每个“docs/ARTIFACT_NORMS.md”的项目路径）、已提交、用户明确批准
- [ ] 要求被引用或总结；溯源清晰
- [ ] 记录了至少 2-3 个具有权衡的替代方案
- [ ] 错误处理和测试策略：关键故障路径和验证方法已记录
- [ ] 输出中没有代码或实现步骤
- [ ] 读者可以根据此设计生成任务列表，无需进一步说明

---

## 示例（示例）

### 示例1：已验证需求的标准设计

**调用**：“我们在 docs/requirements-planning/core-v1.md 中有需求。为其制作一个设计文档。”

**代理**：使用设计解决方案；读取需求；提出 2-3 个架构选项并进行权衡；将设计写入 docs/design-decisions/YYYY-MM-DD-core-v1.md；获得用户认可；建议在该设计上运行分解任务来获取tasks.md。

### 示例 2：边缘情况 — 范围非常小

**调用**：“对小型 CLI 工具的要求已在 docs/requirements-planning/one-off-migration.md 中捕获。我们还需要完整的设计文档吗？”

**代理人**：

- 确认需求已验证，但范围较小。
- 生成简洁的设计文档，该文档仍然涵盖架构、数据流和约束，但保持各部分简短且重点突出。
- 明确说明为什么轻量级设计就足够了，并将文档标记为以后回归或重复运行的单一事实来源。
- 获得用户批准，然后在共享或重复实施的情况下推荐“分解任务”。