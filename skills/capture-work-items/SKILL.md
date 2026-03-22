---
name: capture-work-items
description: Capture requirements, bugs, or issues from free-form input into structured, persistent artifacts. Use when user wants to record a work item quickly without deep validation.
description_zh: 将自由形式输入快速捕获为结构化、可持久的需求、缺陷或问题制品；无需深度验证。
tags: [writing, documentation, workflow]
version: 1.0.1
license: MIT
recommended_scope: both
metadata:
  author: ai-cortex
triggers: [capture, quick capture, record bug]
input_schema:
  type: free-form
  description: Raw description of requirement, bug, or issue from user
output_schema:
  type: document-artifact
  description: Structured work item(s) written per path detection
  artifact_type: backlog-item
  path_pattern: docs/process-management/project-board/backlog/YYYY-MM-DD-{slug}.md (canonical) or docs/backlog/YYYY-MM-DD-{slug}.md (fallback)
  lifecycle: living
---

# 技能（Skill）：捕获工作项

## 目的 (Purpose)

从自由格式的输入中捕获需求、错误或问题，并将其转化为结构化、持久性的产品。提供快速结构化记录，无需“分析需求”执行的深度验证。将输出路径与项目文档结构（例如项目文档模板）保持一致，并包括治理状态跟踪。

---

## 核心目标（Core Objective）

**首要目标**：将用户提供的需求、错误或问题描述转换为具有所有必填字段的结构化工作项，并将其保留到项目约定路径中。

**成功标准**（必须满足所有要求）：

1. ✅ **已识别的类型**：分类为需求、错误或问题的工作项
2. ✅ **必填字段完成**：该类型的所有必填字段均已填写（无推断；缺失时询问用户）
3. ✅ **状态设置**：前面的初始`状态：已捕获`
4. ✅ **检测到的路径**：根据项目文档结构选择的输出路径（请参阅路径检测）
5. ✅ **工件持久化**：工作项写入所选路径
6. ✅ **用户确认**：用户明确确认或委托写入

**验收测试**：某人或下游系统是否可以阅读产品并理解完整的工作项目并在不提出澄清问题的情况下采取行动？

---

## 范围边界（范围边界）

**本技能负责**：

- 自由格式输入 → 结构化工作项
- 单次或批量捕获（批量：按项目或批次确认）
- 输出到项目约定路径下的本地 Markdown
- 状态生命周期：仅限初始“已捕获”（下游更新“分类”、“进行中”、“完成”、“阻止”、“取消”）

**本技能不负责**：

- 深入需求澄清或验证 → 使用“分析需求”
- 设计或建筑 → 使用“设计解决方案”
- 直接 API 调用 Zentao/GitHub 以创建问题（扩展点；v1 不需要）

**转交点**：当产品被持久化并且用户确认后，如果项目需要更深入的验证，则移交给“分析需求”，或者移交给流程管理/里程碑进行规划。

---

## 使用场景（用例）

- **快速待办条目**：用户说“记录此错误”或“添加此要求” - 结构并持续，无需全面分析。
- **会议/电子邮件捕获**：从会议记录或电子邮件中提取工作项目并保存为结构化产品。
- **分类输入**：捕获项目以供以后在里程碑或任务分解中进行分类和优先级排序。
- **积压证据**：填补评估文档中确定的积压差距（例如“积压：弱 - 没有明确的待办文档”）。

---

## 行为（行为）

### 交互（互动）政策

- **默认**：项目规范或规格/产品合同的路径；从输入中键入
- **选择选项**：一次一个缺失字段的问题；在适用时提供选择
- **确认**：与默认路径不同时的目标路径；用户在写入前确认

### 解决项目规范

在坚持之前，根据 [spec/artifact-norms-schema.md](../../spec/artifact-norms-schema.md) 解析产品规范：

1. 检查“.ai-cortex/artifact-norms.yaml”或“docs/ARTIFACT_NORMS.md”
2.如果找到，解析path_pattern为`待办-item`并使用项目规则
3. 如果未找到，则使用 [spec/artifact-contract.md](../../spec/artifact-contract.md) 中的默认值

### 路径检测

使用解析规范（或合同默认值）选择输出路径：

|状况 |输出路径|
| :--- | :--- |
| `docs/process-management/` 存在 | `docs/process-management/project-board/待办/YYYY-MM-DD-<slug>.md` |
|否则 | `docs/待办/YYYY-MM-DD-<slug>.md` |

如果子目录不存在，则创建它们。今天使用“YYYY-MM-DD”； `<slug>` 是标题中的 kebab-case。

### 第 0 阶段：分类 — 识别类型

**开始时宣布：**“我正在使用捕获工作项技能来记录此工作项。”

将输入分类为：

- **要求**：新需求、功能请求或增强
- **bug**：缺陷、不正确的行为、未能满足规范
- **问题**：任务、改进或问题（通用工作项）

### 第 1 阶段：提取 — 识别字段

从输入中提取可用字段。按类型划分的必填字段：

|类型 |必填字段 |
| :--- | :--- |
|要求|标题、问题/需求、验收标准 |
|错误|标题、描述、重现步骤、预期与实际、严重性 |
|问题 |标题、描述、类型（任务\|改进\|问题）|

### 第 2 阶段：提示 — 填写缺少的必填字段

对于任何缺少的必填字段，请询问用户**一次一个问题**。不要推断或猜测。

### 第 3 阶段：坚持 — 编写工件

1. 运行“解决项目规范”，然后运行“路径检测”（见上文）
2. 如果目标路径与默认路径不同，请与用户确认
3. 使用适当的模板使用 YAML front-matter 编写 Markdown（请参阅输出模板）
4. 在 front-matter 中设置 `status: capture`

### 第 4 阶段：确认

与用户确认产品已编写且完整。除非用户明确请求，否则不要提交版本控制。

---

## 输入与输出 (Input & Output)

### 输入（输入）

- 用户的需求、错误或问题的原始描述
- 可选：项目上下文（用于路径检测的现有“docs/”结构）

### 输出（输出）

带有 YAML front-matter 的结构化工作项 Markdown 文件。模板如下。

#### 需求模板


```markdown
---
artifact_type: backlog-item
created_by: capture-work-items
lifecycle: living
type: requirement
date: YYYY-MM-DD
status: captured
source: [user|meeting|email]
trace_id: optional
---

# [Title]

## Problem / Need
[Who has what problem; no solution language]

## Acceptance Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]

## Notes
[Optional]
```


#### 错误模板


```markdown
---
artifact_type: backlog-item
created_by: capture-work-items
lifecycle: living
type: bug
date: YYYY-MM-DD
status: captured
severity: [critical|major|minor]
---

# [Title]

## Description
[What goes wrong]

## Steps to Reproduce
1. ...
2. ...

## Expected vs Actual
- **Expected**: ...
- **Actual**: ...

## Environment
[Optional]
```


#### 问题模板


```markdown
---
artifact_type: backlog-item
created_by: capture-work-items
lifecycle: living
type: issue
subtype: [task|improvement|question]
date: YYYY-MM-DD
status: captured
---

# [Title]

## Description
[Content]
```


### 状态生命周期

该技能仅设置“状态：捕获”。下游流程（里程碑、升级迭代任务、运行检查点）可能会更新为：“分类”、“进行中”、“完成”、“阻止”、“取消”。

---

## 限制（限制）

### 硬边界（Hard Boundaries）

- **不跳过必填字段**：如果无法推断必填字段，请询问用户。不要留空。
- **No analyze-需求 flow**: Do not run diagnostic states (RA0–RA5).如果输入内容非常模糊，建议先捕获，然后转交给“分析需求”。
- **写入前确认路径**：避免覆盖现有文件；当目标路径不明确时确认。
- **路径遵循项目结构**：使用路径检测规则；不要硬编码单个路径。

### 技能边界 (Skill Boundaries)（避免重叠）

**不要做这些**（其他技能可以处理它们）：

- **深度需求验证**：诊断状态、问题阐明、范围边界 → 使用“分析需求”
- **设计和架构**：解决方案、替代方案、权衡 → 使用“设计解决方案”
- **任务分解**：史诗/任务分解、验收标准细化→使用流程管理或实施计划

**何时停止并交接**：

- 用户说“这需要更多分析” → 移交给“分析需求”
- 用户说“设计这个” → 移交给“设计解决方案”
- 工件保留并确认 → 移交完成

---

## 自检（Self-Check）

### 核心成功标准（必须满足所有标准）

- [ ] **识别的类型**：工作项是需求、错误或问题
- [ ] **必填字段已填写**：已填写所有必填字段（无推断）
- [ ] **状态集**：前面的内容中的“状态：已捕获”
- [ ] **检测到路径**：输出路径遵循路径检测规则
- [ ] **工件保留**：文件写入所选路径
- [ ] **用户确认**：用户确认或委托写入

### 流程质量检查

- [ ] **一次一个问题**：没有让用户因多个缺失字段的问题而不知所措
- [ ] **需求中没有解决方案语言**：问题/需求描述了问题，而不是实现
- [ ] **路径创建**：如果需要，创建`待办/`子目录
- [ ] **文件名约定**：使用 YYYY-MM-DD-{slug}.md

### 验收测试

**某人或下游系统是否可以阅读产品并理解完整的工作项目并在不提出澄清问题的情况下采取行动？**

如果否：必填字段不完整。返回提示阶段。

如果是：捕获完成。根据需要进行交接。

---

## 示例（示例）

### 示例 1：错误捕获

**用户**：“当我在密码字段中使用特殊字符时，登录页面显示 500。”

**代理宣布**：“我正在使用捕获工作项技能来记录此工作项。”

**分类**：分类为错误。

**摘录**：存在标题和描述；重现步骤、预期与实际、严重性缺失。

**提示**（一次一个）：

特工：“重现这个的具体步骤是什么？”

用户：“1. 转到 /login 2. 输入任意用户名 3. 输入带有 @ 或 # 的密码 4. 单击“登录””

特工：“你的预期与实际发生的情况有何不同？”

用户：“预期：正常登录或验证错误。实际：500 内部服务器错误。”

特工：“您会分配什么严重程度：严重、严重还是轻微？”

用户：“少校。”

**持久**：检测到路径 - `docs/process-management/` 存在。写入“docs/process-management/project-board/待办/2026-03-06-login-500-special-chars.md”。

**确认**：“已写入。您想要调整任何内容还是移交分类？”

### 示例 2：需求捕获 — 模糊输入

**用户**：“我们需要更好的错误消息。”

**代理宣布**：“我正在使用捕获工作项技能来记录此工作项。”

**分类**：分类为要求（可能是问题；代理选择要求作为默认的“需要”）。

**摘录**：标题可推导（“更好的错误消息”）；缺少问题/需求和验收标准。

**提示**：

代理：“谁遇到了这个问题？当前的错误消息到底出了什么问题？”

用户：“我们的 API 用户得到的是通用的‘出了问题’，但没有任何可操作的信息。”

特工：“‘完成’会是什么样子——至少有一个具体的验收标准？”

用户：“错误响应应包括代码（例如 ERR_001）和一条简短的人类可读消息，解释出现的问题。”

**持续**：检测到路径 - `docs/process-management/` 不存在。写入“docs/待办/2026-03-06-better-error-messages.md”。

**移交建议**：“这可能受益于分析需求的更深入验证。仅继续捕获，还是移交进行全面分析？”

用户：“暂时只捕获。”

**确认**：“已书面。准备好后交给分诊。”

### 示例 3：问题捕获 — 边缘情况（一条消息中包含多个项目）

**用户**：“两件事：1）更新自述文件安装部分。2）添加 CONTRIBUTING.md。”

**特工宣布**：“我正在使用捕获工作项技能。我看到两个单独的工作项。我将一次捕获它们一个。”

**第 1 项** — 类型：问题（任务）。标题：“更新自述文件安装部分”。描述：来自上下文。保留为“2026-03-06-update-readme-install.md”。

**第 2 项** — 类型：问题（任务）。标题：“添加 CONTRIBUTING.md”。描述：来自上下文。保留为“2026-03-06-add-contributing.md”。

**确认**：“两个项目均已捕获。如果需要，请检查并调整。”

---

## 附录：输出合约

该技能会生成**文档-制品**（待办项目）。每个输出文件必须符合：

|元素|要求|
| :--- | :--- |
| **路径** |每路径检测： `docs/process-management/project-board/待办/YYYY-MM-DD-<slug>.md` 或 `docs/待办/YYYY-MM-DD-<slug>.md` |
| **产品类型** | `待办项目` |
| **创建者** | `捕获工作项` |
| **生命周期** | `生活` |
| **类型** | `要求` \| `错误` \| `问题` |
| **状态** | ‘捕获’ |
| **必填部分** |每个类型：要求（标题、问题/需求、验收标准）； bug（标题、描述、重现步骤、预期与实际、严重性）；问题（标题、描述、子类型）|