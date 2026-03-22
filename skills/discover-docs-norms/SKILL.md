---
name: discover-docs-norms
description: Help users establish project-specific artifact norms (paths, naming, lifecycle) through dialogue and scanning. Core goal - produce docs/ARTIFACT_NORMS.md and optional .ai-cortex/artifact-norms.yaml.
description_zh: 通过对话与扫描，帮助建立项目级文档制品规范（路径、命名、生命周期）；产出 docs/ARTIFACT_NORMS.md。
tags: [documentation, workflow]
version: 1.0.1
license: MIT
recommended_scope: project
metadata:
  author: ai-cortex
triggers: [discover norms, document norms]
input_schema:
  type: free-form
  description: Project path, optional starting point (AI Cortex default, project-documentation-template, blank)
output_schema:
  type: document-artifact
  description: docs/ARTIFACT_NORMS.md and optionally .ai-cortex/artifact-norms.yaml
---

# 技能（Skill）：发现文档规范

## 目的 (Purpose)

帮助用户为文档治理定义特定于项目的产品规范（路径、命名、生命周期）。项目可能有自己的文档结构；该技能发现并形式化它，以便其他技能（捕获工作项、设计解决方案、评估文档）可以遵循项目规范。

---

## 核心目标（Core Objective）

**首要目标**：生成`docs/ARTIFACT_NORMS.md`（以及可选的`.ai-cortex/artifact-norms.yaml`），声明待办、设计、ADR 和校准产品的项目产品路径、命名和生命周期。

**成功标准**（必须满足所有要求）：

1. ✅ **扫描项目结构**：检查现有的 `docs/` 结构和约定
2. ✅ **确认用户偏好**：通过对话确认待办、设计、adr、文档准备的路径（或从起始模板接受）
3. ✅ **写入 ARTIFACT_NORMS.md**：人类可读的规范文件位于 `docs/ARTIFACT_NORMS.md`
4. ✅ **创建可选的 YAML**：如果用户请求，使用机器可读模式编写的 `.ai-cortex/artifact-norms.yaml`
5. ✅ **用户确认**：用户在最终写入之前明确批准了规范

**验收**测试：其他技能（例如 capture-work-items）能否读取输出并正确解析该项目的路径？

---

## 范围边界（范围边界）

**本技能负责**：

- 扫描项目`docs/`结构
- 确认产品路径和命名的对话
- 根据 [spec/artifact-norms-schema.md](../../spec/artifact-norms-schema.md) 生成 `docs/ARTIFACT_NORMS.md` 和可选的 `.ai-cortex/artifact-norms.yaml`
- 从 AI Cortex 默认、项目文档模板或空白开始

**本技能不负责**：

- 引导完整的项目文档（使用“bootstrap-docs”）
- 评估文档准备情况（使用“assess-docs”）
- 根据规范验证现有文档（使用“评估文档”；合规性是其报告的一部分）

**转交点**：编写并确认规范后，将其移交给其他文档制作技能或“评估文档”以进行合规性和准备情况检查。

---

## 使用场景（用例）

- **新项目**：尚无产品规范；用户希望在使用捕获工作项或设计解决方案之前建立它们。
- **现有项目**：项目具有自定义的“docs/”结构；将其正式化，以便技能协调一致。
- **迁移**：采用 AI Cortex 默认值或项目文档模板；创建规范文件以保持一致性。

---

## 行为（行为）

### 交互（互动）政策

- **默认**：项目路径 = 工作空间根目录；如果没有规范则从AI Cortex默认开始
- **选择选项**：起点`[ai-cortex][template][blank]`；每个产品类型的路径映射
- **确认**：在写入ARTIFACT_NORMS.md之前；所有路径映射

### 第 1 阶段：扫描

1.检查项目根目录和`docs/`（如果存在）
2. 识别现有路径：待办、设计、adr、校准等。
3. 记下示例文件中的任何约定（命名、前面的内容）

### 第 2 阶段：选择起点

询问用户或从上下文推断：

- **AI Cortex 默认**：使用 [spec/artifact-contract.md](../../spec/artifact-contract.md) 作为基线
- **项目文档模板**：将模板结构映射到产品类型
- **空白**：从最小表开始，用户填写路径

### 第 3 阶段：确认路径

对于每种产品类型（待办项目、设计、adr、文档准备）：

- 从起点或现有结构提出路径模式和命名
- 要求用户确认或定制
- 待办项目的文档路径检测规则（如果适用）

### 第 4 阶段：写入并确认

1. 根据 [spec/artifact-norms-schema.md](../../spec/artifact-norms-schema.md) 生成 `docs/ARTIFACT_NORMS.md`
2. （可选）生成 `.ai-cortex/artifact-norms.yaml`
3. 现状总结；写入前请求用户确认
4、确认后写入文件

---

## 输入与输出 (Input & Output)

### 输入（输入）

- 项目路径（默认：当前工作空间根目录）
- 可选：起点（ai-cortex | 模板 | 空白）

### 输出（输出）

- `docs/ARTIFACT_NORMS.md`：人类可读的产品规范表
- `.ai-cortex/artifact-norms.yaml`（可选）：机器可读模式

---

## 限制（限制）

### 硬边界（Hard Boundaries）

- **未经确认不得覆盖**：未经用户明确批准，请勿写入或覆盖规范文件。
- **架构合规性**：输出必须遵循 [spec/artifact-norms-schema.md](../../spec/artifact-norms-schema.md)。

### 技能边界 (Skill Boundaries)（避免重叠）

**不要做这些（其他技能可以处理它们）**：

- **完整文档 bootstrap**：引导完整项目文档 → 使用 `bootstrap-docs`
- **准备情况评估**：评估文档就绪 → 使用 `assess-docs`
- **合规性验证**：验证制品规范合规 → 使用 `assess-docs`（在其报告中包含合规性）

**何时停止并交接**：

- 用户问「能帮我建立完整文档结构吗？」→ 移交给 `bootstrap-docs`
- 用户问「文档准备好发布了吗？」→ 移交给 `assess-docs`
- 规范已写入且用户确认 → 交接完成

---

## 自检（Self-Check）

### 核心成功标准（必须满足所有标准）

- [ ] **已扫描项目结构**：检查现有 `docs/` 目录
- [ ] **用户偏好确认**：通过对话确认的路径
- [ ] **ARTIFACT_NORMS.md 已写入**：文件存在于 `docs/ARTIFACT_NORMS.md`
- [ ] **用户确认**：用户在写入前已批准

### 验收测试

**其他技能可以读取输出并正确解析该项目的路径吗？**

如果否：规范不完整或不一致。返回第 3 阶段。
如果是：切换完成。

---

## 示例（示例）

### 示例 1：新项目，AI Cortex 默认值

**上下文**：空项目，没有文档/。

**步骤**：从 AI Cortex 默认开始。建议路径：`docs/待办/`、`docs/design-decisions/`、`docs/process-management/decisions/`、`docs/calibration/`。用户确认。编写“docs/ARTIFACT_NORMS.md”并根据需要创建“docs/”子目录。

### 示例 2：现有自定义结构

**上下文**：项目有“docs/work-items/”、“docs/decisions/”，没有正式规范。

**步骤**：扫描结构。建议映射：待办项 → `docs/work-items/`，adr → `docs/decisions/`。用户确认。使用自定义路径编写规范文件。

---

## 附录：输出合约

该技能为项目规范生成**文档产品**输出。输出必须符合：

|元素|要求 |
| :--- | :--- |
| **主要输出** | `docs/ARTIFACT_NORMS.md` — 人类可读的产品规范表（产品类型、路径模式、命名、生命周期）|
| **可选输出** | `.ai-cortex/artifact-norms.yaml` — 每个 [spec/artifact-norms-schema.md](../../spec/artifact-norms-schema.md) 的机器可读模式 |
| **路径映射** |每个 artifact_type 映射到一个 path_pattern；用户在写入前必须确认|