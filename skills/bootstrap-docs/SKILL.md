---
name: bootstrap-docs
description: Bootstrap or adapt project docs using project-documentation-template. Core goal - produce structured lifecycle documentation aligned with enterprise template. Initialize (empty) or Adjust (non-empty); repeatable; strict kebab-case naming.
description_zh: 使用 project-documentation-template 初始化或适配项目文档；产出结构化生命周期文档；支持 Initialize / Adjust。
tags: [documentation, writing]
version: 1.1.2
license: MIT
recommended_scope: both
metadata:
  author: ai-cortex
triggers: [bootstrap docs, bootstrap documentation]
input_schema:
  type: free-form
  description: Project directory to bootstrap or adapt documentation for
output_schema:
  type: document-artifact
  description: Structured lifecycle documentation tree aligned with enterprise template
  artifact_type: adr
  path_pattern: docs/process-management/decisions/YYYYMMDD-{slug}.md
  lifecycle: living
compatibility: Requires access to https://raw.githubusercontent.com or a local clone of nesnilnehc/project-documentation-template.
---

# 技能(Skill)：Bootstrap项目文档

## 目的 (Purpose)

使用 [project-documentation-template](https://github.com/nesnilnehc/project-documentation-template) 结构引导或调整项目文档。两种模式：**初始化**（空项目——复制模板并填充占位符）和**调整**（非空——使用模板作为目标，建议重命名/移动/合并，确认后就地应用）。支持可重复运行；除非有要求，否则避免空目录和模板文件；强制执行严格的短横线命名。技能生成的产品（ADR、待办、设计决策、校准）的输出路径遵循 [spec/artifact-contract.md](../../spec/artifact-contract.md)； project-documentation-template 提供内容和参考。创建流程管理结构时，为每个合同创建 `docs/process-management/project-board/待办/` 和 `docs/process-management/decisions/`。

---

## 核心目标（Core Objective）

**治理目标**：通过适合模式的引导或调整，生成与企业模板一致的结构化生命周期文档。

**成功标准**（必须满足所有要求）：

1. ✅ **正确选择模式**：针对空项目进行初始化，针对非空项目进行调整（或应用用户覆盖）
2. ✅ **应用模板结构**：文档遵循所选规模的项目-文档-模板约定
3. ✅ **占位符已填充**：所有 `[...]` 占位符替换为项目特定内容（或明确标记以供以后使用）
4. ✅ **强制执行命名约定**：所有路径都使用严格的短横线大小写； ADR 文件遵循 `YYYYMMDD-slug-title.md` 格式
5. ✅ **获得用户确认**：在调整模式下，仅在用户批准推荐列表后才应用更改

**仓库测试**：开发人员是否可以在不查阅模板存储库的情况下导航文档结构并查找生命周期文档？

---

## 范围边界（范围边界）

**本技能负责**：

- 文档结构引导（初始化模式）
- 文档结构调整（调整模式）
- 占位符填充和验证
- 路径命名标准化（kebab-case）
- ADR 生成和索引

**本技能不负责**：

- 自述文件生成（使用“generate-standard-readme”）
- AGENTS.md 条目创建（使用 `generate-agent-entry`）
- 特定于技能的文档（使用“refine-skill-design”）
- 超出模板占位符的内容编写（用户提供域内容）

**转交点**：建立文档结构并填充占位符后，将其移交给内容创作或特定于项目的文档工作流。

---

## 使用场景（用例）

- **空项目**：通过复制模板子集并填充小型/中型/大型项目的占位符来初始化完整的文档框架。
- **非空项目**：使用模板作为目标参考；分析现有文档，提出重命名/移动/合并以调整结构和命名；用户确认后应用就地更改。除非有要求，否则不要创建空目录或模板文件。可以反复运行。
- **共享工作流程**：生成架构决策记录 (ADR)、跨文档更新版本信息、验证占位符和链接。
- **迭代运行**：重复运行技能以逐步组织和完善文档；每次运行都基于当前状态，无需完全重新初始化。

**何时使用**：当项目需要与企业模板一致的结构化生命周期文档时，或者当现有文档应与该结构一致时。

---

## 行为（行为）

### 模式选择

首先确定执行模式。用户优先；否则：

|模式|触发|行为 |
| :--- | :------ | :----- |
| **初始化** |没有“docs/”或“docs/”为空 |复制子集，填充占位符，创建“VERSION”，输出文档骨架 |
| **调整** | `docs/` 有 ≥1 个有效文档 |扫描、比较、输出推荐列表；用户确认后申请 |

**检测规则**：

- 没有 `docs/` 或 `docs/` 为空 → **初始化**
- `docs/` 存在并且有 ≥1 个有效的 `.md` 文件 → **调整**
- 用户明确指定 `--mode=initialize` 或 `--mode=adjust` → 使用该模式

### 初始化模式步骤

1. 确定项目规模：小型、中型或大型（根据用户或上下文）。
2. 按规模从模板中选择文档子集：
   - **小**：项目概述、开发指南、用户指南
   - **中**：+架构、设计、需求和规划
   - **大型**：+流程管理、操作指南、合规性、社区和贡献
3. 从“TEMPLATE_BASE_URL”获取模板（请参阅附录）或使用本地克隆。
4. **仅**选定的文档复制到项目“docs/”。当规模允许时，根据 [spec/artifact-contract.md](../../spec/artifact-contract.md) 创建合同对齐目录：`docs/design-decisions/`（中+）、`docs/calibration/`、`docs/process-management/project-board/待办/`、`docs/process-management/decisions/`（大）。可以选择从合同创建“docs/ARTIFACT_NORMS.md”（根据 [spec/artifact-norms-schema.md](../../spec/artifact-norms-schema.md)）供用户自定义。除非用户明确请求，否则不要创建其他空目录。
5. 使用项目元数据（名称、日期、技术堆栈）填充占位符，并提示缺少的关键数据。
6. 创建一个“VERSION”文件（例如“1.0.0”），除非用户明确请求不创建新文件。
7. 验证：没有未替换的占位符、链接有效、表格对齐。

### 调整模式步骤

1. 使用 [project-documentation-template](https://github.com/nesnilnehc/project-documentation-template) 作为结构、约定和文件/目录名称的**目标参考**。
2. 扫描“docs/”下的现有文档（结构、占位符、链接、版本）。
3. 与模板进行比较并找出差距：
   - 结构和路径不匹配（非标准目录/文件名）
   - 文档可与模板对齐（重命名、移动或合并）
   - 未填充的占位符、损坏的链接、版本不一致
4. 制作**推荐列表**并呈现给用户；申请前要求确认。
5. 确认后，将更改**就地**应用到现有文件。除非用户明确请求，否则不要创建空目录或添加模板文件。
6.该技能是**幂等的**：可以重复运行以迭代地组织和细化文档。

### 约定（来自 llms.txt）

- **占位符**：`[描述]`、`[选项1/选项2]`、`YYYY-MM-DD`、`[数字]`
- **表格**：保持列对齐； “*”标记必填字段
- **版本**：使用 SemVer；更新文档底部的版本历史记录以了解更改
- **参考文献**：内部`[README](../../README.md)`；外部`[示例](https://example.com)`
- **日期**：`YYYY-MM-DD`

### 文件和目录命名（严格）

- **目录**：仅限“kebab-case”（例如“项目概述”、“开发指南”、“流程管理”）
- **文件**：带有“.md”扩展名的“kebab-case”（例如“goals-and-vision.md”、“versioning-standards.md”）
- **ADR 文件**：每个 [spec/artifact-contract.md](../../spec/artifact-contract.md) `docs/process-management/decisions/YYYYMMDD-slug.md`
- 没有空格、下划线或 PascalCase；仅限小写字母、数字、连字符。

---

## 输入与输出 (Input & Output)

### 输入（输入）

- **项目元数据**：名称、描述、技术堆栈
- **规模**：小|中等|大（可选；如果不存在，则从上下文推断）
- **模式覆盖**（可选）：`初始化` | `调整`

### 输出（输出）

- **初始化**：在`docs/`、`VERSION`下填充文档，以及创建文件的简短摘要
- **调整**：建议列表（降价或结构化），然后 - 确认后 - 应用的更改和摘要

---

## 限制（限制）

### 硬边界（Hard Boundaries）

- 在最终确定文档之前替换所有占位符；除非明确推迟，否则不要在最终输出中留下“[description]”等。
- 不要添加或保留损坏的内部链接；验证相对路径。
- 对版本使用一致的日期 (`YYYY-MM-DD`) 和 SemVer。
- 在调整模式下，未经用户确认请勿应用更改。
- 未经用户批准，请勿从模板中删除结构元素（部分、表格）。
- 除非用户明确请求，否则不要创建空目录或添加模板文件。
- 创建或重命名路径时，使用严格的文件和目录命名（短横线命名，ADR 格式“YYYYMMDD-title.md”）。

### 技能边界 (Skill Boundaries)（避免重叠）

**不要做这些（其他技能可以处理它们）**：

- **README 生成**：创建或更新 README.md 文件 → 使用 `generate-standard-readme`
- **AGENTS.md 条目创建**：编写或更新 AGENTS.md 文件 → 使用 `generate-agent-entry`
- **技能文档**：创建或优化 SKILL.md 文件 → 使用 `refine-skill-design`
- **内容创作**：在模板占位符之外编写特定于域的内容 → 用户提供内容

**何时停止并交接**：

- 用户说“结构已准备好”或“占位符已填充”→ 文档结构完成，移交给内容创作
- 用户询问“我该如何编写内容？” → 结构完成，移交给领域专家或内容工作流程
- 用户问“你能生成自述文件吗？” → 移交给“生成标准自述文件”
- 用户问“你能创建 AGENTS.md 吗？” → 移交给 `generate-agent-entry`

---

## 自检（Self-Check）

### 核心成功标准（必须满足所有标准）

- [ ] **正确选择模式**：针对空项目进行初始化，针对非空项目进行调整（或应用用户覆盖）
- [ ] **应用模板结构**：文档遵循所选规模的项目-文档-模板约定
- [ ] **占位符已填充**：所有“[...]”占位符替换为项目特定内容（或明确标记以供以后使用）
- [ ] **强制命名约定**：所有路径都使用严格的短横线大小写； ADR 文件遵循 `YYYYMMDD-slug-title.md` 格式
- [ ] **获得用户确认**：在调整模式下，仅在用户批准推荐列表后才应用更改

### 流程质量检查

- [ ] **链接已验证**：内部链接是否解析以及外部链接是否指向有效资源？
- [ ] **版本一致性**：“VERSION”和受影响的文档之间的版本是否一致？
- [ ] **表格对齐**：是否保留 Markdown 表格对齐方式？
- [ ] **没有额外的目录/文件**：除非用户请求，否则是否避免了空目录和模板文件？

### 验收测试

**开发人员可以在不查阅模板存储库的情况下浏览文档结构并查找生命周期文档吗？**

如果否：文档结构不完整或不清楚。返回特定于模式的步骤。

如果是：文档结构完整。继续转交。

---

## 示例（示例）

### 示例 1：初始化（空项目，小规模）

**上下文**：新的存储库“my-service”，没有“docs/”目录。

**步骤**：Agent选择Initialize；规模=小。从模板复制项目概述、开发指南、用户指南。填写项目名称、日期、占位符描述。将“VERSION”创建为“1.0.0”。输出创建的文件的摘要。

**输出片段**：`docs/project-overview/goals-and-vision.md`、`docs/development-guide/...`、`docs/user-guide/...`、`VERSION`。所有占位符都填充了项目特定的内容。

### 示例 2：调整（非空项目）

**上下文**：回购协议有“docs/”和“project_overview/goals.md”（非标准路径）。一些占位符未填充。

**步骤**：代理选择“调整”。使用 [project-documentation-template](https://github.com/nesnilnehc/project-documentation-template) 作为目标。产生推荐列表：

- 重命名 `project_overview/` → `project-overview/`, `goals.md` → `goals-and-vision.md` (kebab-case, 匹配模板)
- `goals-and-vision.md` 中未填充的占位符：`[项目描述]`、`[目标日期]`
- 损坏的链接：`../architecture/tech-stack.md`（路径不存在）

代理展示该列表并询问：“应用这些更改？（是/否）”。用户确认。代理重命名目录/文件，修复占位符和链接。没有创建新的空目录或模板文件。

### 示例 3：通用工作流程 — 生成 ADR

**上下文**：任何项目；用户需要一个架构决策记录。

**步骤**：代理从模板中获取“docs/process-management/decisions/ADR-TEMPLATE.md”。确定下一个 ADR 编号（例如 ADR-001）。用用户输入填充上下文、选项、基本原理、结果。保存为“docs/process-management/decisions/YYYYMMDD-decision-title.md”（kebab-case slug）并更新决策索引（如果存在）。

---

## 附录：输出合同

### 初始化模式

|可交付成果 |必填|
| :--- | :--- |
|仅包含选定模板文件的“docs/”（无空目录）|是的 |
| `版本` 文件 |是（除非用户明确请求不添加新文件）|
|所有占位符均已替换（或标记为稍后使用）|是的 |
|文档底部的版本历史表 |每个模板|

###调整模式推荐列表格式

|部分|内容 |
| :--- | :--- |
|目标参考| [project-documentation-template](https://github.com/nesnilnehc/project-documentation-template) |
|路径/命名问题 |当前路径→推荐路径（kebab-case、模板对齐）|
|可对齐文档 |可以重命名/移动/合并现有文档以匹配模板 |
|未填充的占位符 |文件路径+占位符文本|
|损坏/过时的链接 |文件路径+链接|
|版本问题 |冲突或缺少版本参考 |

### 模板源

- **TEMPLATE_BASE_URL**（规范）：`https://raw.githubusercontent.com/nesnilnehc/project-documentation-template/main/`
- 关键文件：`llms.txt`、`AGENTS.md`、`README.md`、`docs/`
- 如果获取失败（网络不可用）：提示用户提供本地克隆路径或稍后重试；不要继续使用过时或丢失的模板。