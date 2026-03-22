---
name: review-requirements
description: "Review an existing requirements document for quality: problem clarity, testable needs, constraint inventory, scope boundedness, requirement IDs, and open questions. Evaluative atomic skill; output is a findings list."
description_zh: 审查既有需求文档质量：问题清晰度、可测试需求、约束清单、范围边界、需求 ID 与遗留问题。
tags: [code-review]
version: 1.0.1
license: MIT
recommended_scope: both
metadata:
  author: ai-cortex
triggers: [review requirements, requirements review, requirements quality, check requirements, validate requirements doc, requirements check]
input_schema:
  type: document-artifact
  description: Existing requirements document (path or content) to evaluate
  artifact_type: requirements
output_schema:
  type: findings-list
  description: Zero or more findings with location, category, severity, and suggestion covering all six requirements quality dimensions
---

# 技能（Skill）：复习要求

## 目的 (Purpose)

根据定义的质量标准评估**现有需求文档**。不生成或重写需求；这些是“分析需求”的职责。发出**发现列表**，以便作者可以在设计开始之前或审查之前改进文档。

---

## 核心目标（Core Objective）

**首要目标**：生成需求质量调查结果列表，识别所有六个质量维度的差距，使作者能够在移交给设计之前达到可审查的标准。

**成功标准**（必须满足所有要求）：

1. ✅ **审查所有六个维度**：评估问题清晰度、可测试性、约束清单、范围界限、需求 ID 和开放问题
2. ✅ **仅限文档范围内的发现**：仅审查所提供文档中的内容；没有外部假设或生成性添加
3. ✅ **符合调查结果格式**：每个调查结果包括位置、类别（`需求质量`）、严重性、标题、描述和可选建议
4. ✅ **位置精确引用**：所有发现都引用文档中的特定部分或需求 ID（不是模糊的描述）
5. ✅ **可操作的输出**：每个发现都提供了参考相关部分或 ID 的具体改进方向

**验收**测试：作者是否可以阅读调查结果列表，确切地知道要修复哪个部分或要求，并理解“已修复”是什么样子 - 而无需提出澄清问题？

---

## 范围边界（范围边界）

**本技能负责**：

- 评估问题陈述的清晰度（不含解决方案/技术参考）
- 验证每个需求都有可测试的验收标准
- 检查约束清单完整性（实际约束与假设分离）
- 评估范围界限（V1 边界、延期项目、存在未决问题）
- 验证需求 ID 格式和唯一性（R-01、R-02、...）
- 识别缺失或未指定的开放式问题

**本技能不负责**：

- 生成或重写需求 — 使用“analyze-需求”
- 根据需求进行设计 — 使用“设计解决方案”
- 审查代码、架构或实现——使用“review-*”代码技能
- 全面需求诱导或诊断状态进展 (RA0–RA5) — 使用“分析需求”

**转交点**：当结果发布后，交给作者使用“分析需求”来修复差距，或者确认文档是无发现的并继续“设计解决方案”。

---

## 使用场景（用例）

- **预设计门**：在移交“设计解决方案”之前验证需求文档。
- **协作评审**：团队成员撰写需求；另一方运行此技能来评估质量。
- **进口需求**：需求是在该工作流程之外编写的（例如 Confluence、Notion、Jira）；使用前需要进行质量评估。
- **“分析需求”后验证**：在“分析需求”之后运行，作为独立检查是否满足所有成功标准。

---

## 行为（行为）

### 交互（互动）政策

- **默认**：接受所提供的文档；不要要求作者提供缺失的内容——而是发布一个发现。
- **禁止重写**：说明遗漏或不正确的内容；切勿代​​表作者重写需求文本。
- **仅在输入不明确时确认**：如果输入不是需求文档（例如设计文档），请先澄清后再继续。

### 审查清单（六个质量维度）

对于每个维度，扫描整个文档并发布发现的所有违规行为的结果：

1. **问题清晰**
   - 是否存在问题陈述来描述谁遇到了什么问题以及为什么它很重要？
   - 问题陈述是否回避了解决方案或技术参考？
   - 问题陈述是否与需求/要求列表不同？

2. **需求的可测试性**
   - 每项要求（必须有、应该有、可以有）是否都有明确的验收标准？
   - 验收标准是否具体（给定/何时/然后或可测量的指标）而不是基于形容词的（“快速”、“简单”、“直观”）？
   - 每个要求都可以由第三方独立验证吗？

3. **限制库存**
   - 是否有明确的约束库存部分（或同等内容）？
   - 真正的限制（预算、时间、技能、依赖性）是否与未验证的假设分开？
   - 所有约束和假设都可以追溯到来源或验证计划吗？

4. **范围界限**
   - 是否明确规定了 V1 边界（范围内与范围外）？
   - 推迟的项目是否列出了重新考虑的触发器？
   - 是否描述了行走骨架或最小可行版本？

5. **需求 ID**
   - 每个需求是否都有一个格式为“R-NN”的唯一 ID（例如 R-01、R-02）？
   - ID 是否连续且没有间隙或重复？
   - 文档中的所有交叉引用是否都使用 ID 而不是自由文本描述？

6. **开放式问题**
   - 是否有开放问题部分（或同等内容）？
   - 每个悬而未决的问题是否都有解决计划或负责人？
   - 需求文本中是否存在应作为开放问题明确表示的隐含未知数？

### 严重性指导

|严重程度 |何时使用 |
| :--- | :--- |
| `关键` |缺少问题陈述；对于任何必须具备的要求没有接受标准；没有范围定义 |
| `主要` |存在验收标准但无法测试（仅限形容词）；约束库存缺失；无 V1 边界 |
| `轻微` |部分需求缺少ID；一些验收标准不完整；假设未分离|
| `建议` |开放性问题可以更明确； ID 不连续；细微的措辞改进 |

---

## 输入与输出 (Input & Output)

### 输入（输入）

- **需求文档**：文件路径（例如`docs/requirements-planning/<topic>.md`）或内联粘贴的原始内容。
- **可选上下文**：项目名称、目标受众或下游技能（例如“这将提供设计解决方案”）。

### 输出（输出）

- 以**附录：输出合同**中定义的格式发出零个或多个**结果**。
- 该技能的所有发现的类别是**需求质量**。
- 如果没有发现：发出简短的“要求文档满足所有六个质量维度。准备‘设计解决方案’。”确认。

---

## 限制（限制）

### 硬边界（Hard Boundaries）

- **不要重写**：不要生成新的需求文本、验收标准或问题陈述。发出带有建议的发现；将创作留给用户或“分析需求”。
- **不要添加范围**：不要发明缺失的需求或扩展文档的范围。
- **仅文档**：仅基于所提供文档的调查结果。不要添加基于外部知识的调查结果，即需求“应该”包含六个维度之外的内容。

### 技能边界 (Skill Boundaries)

**不要做这些**（其他技能可以处理它们）：

- 不要引出、澄清或重写需求——使用“分析需求”
- 不要根据需求进行设计——使用“设计解决方案”
- 不要审查代码、架构或实现质量——使用“审查代码”、“审查架构”等。
- 不要运行完整的 RA0–RA5 诊断状态进程 — 使用“analyze-需求”

**何时停止并交接**：

- 当所有发现都发布后，交给作者来修复差距（可以选择使用“分析需求”）
- 当文档的发现为零时，确认其已准备好并建议“设计解决方案”作为下一步
- 当输入的内容不是需求文档时，澄清并重定向到适当的技能

---

## 自检（Self-Check）

### 核心成功标准

- [ ] **审查所有六个维度**：评估问题清晰度、可测试性、约束清单、范围界限、需求 ID 和开放问题
- [ ] **仅限文件范围内的发现**：无外部假设；仅基于所提供文档的调查结果
- [ ] **符合调查结果格式**：每个调查结果包括位置、类别（`需求质量`）、严重性、标题、描述和可选建议
- [ ] **位置精确引用**：所有发现都引用特定的章节标题或要求 ID
- [ ] **可操作的输出**：每个发现都说明了问题所在以及改进之处

### 流程质量检查

- [ ] 是否对每项要求（必须有、应该有、可能有）进行了验收标准扫描？
- [ ] 是否检查了问题陈述的解决方案/技术语言？
- [ ] 是否明确检查了实际约束和假设是否分离？
- [ ] 是否检查了所有需求 ID 的唯一性和格式 (R-NN)？
- [ ] 是否检查了未决问题的解决计划？

### 验收测试

**作者是否可以阅读调查结果列表，确切地知道要修复哪个部分或需求 ID，并了解“已修复”是什么样子 - 而无需提出澄清问题？**

如果否：调查结果不完整或不精确。添加位置参考和具体建议。

如果是：调查结果已准备就绪。移交给作者进行改进或确认文档已准备好用于“设计解决方案”。

---

## 示例（示例）

### 示例 1：缺少“必须有需求”的接受标准

**输入**：要求文档，其中包含 5 个必须具备的项目；其中 3 个没有验收标准。

**预期结果**：


```markdown
- **Location**: `## Need Hierarchy / Must Have / R-02`
- **Category**: requirements-quality
- **Severity**: major
- **Title**: Must Have requirement lacks acceptance criteria
- **Description**: R-02 ("Users can export data") has no acceptance criteria. Without a testable criterion, this requirement cannot be verified or designed against.
- **Suggestion**: Add acceptance criteria in the form "Given [context], when [action], then [outcome]". Example: "Given a user has at least one dataset, when they click Export, then a CSV file is downloaded within 3 seconds."
```


### 示例 2：问题陈述引用解决方案

**输入**：问题陈述为“我们需要一个带有 PostgreSQL 数据库的 React 应用程序，因为用户无法跟踪库存。”

**预期结果**：


```markdown
- **Location**: `## Problem Statement`
- **Category**: requirements-quality
- **Severity**: major
- **Title**: Problem statement contains solution references
- **Description**: "React app" and "PostgreSQL database" are technology choices, not problem descriptions. The problem statement should describe the pain without referencing solutions.
- **Suggestion**: Rewrite as: "Small business owners lose inventory data due to manual tracking limitations. They need a reliable way to track and query inventory across devices."
```


### 示例 3：无范围定义

**输入**：需求文档有 10 个需求，但没有范围内/范围外部分，也没有 V1 边界。

**预期结果**：


```markdown
- **Location**: (document-level — no scope section present)
- **Category**: requirements-quality
- **Severity**: critical
- **Title**: No scope definition or V1 boundary
- **Description**: The document lists requirements but does not define what is in scope for V1, what is deferred, or what a minimal useful version looks like. Without scope boundaries, design and implementation have no stopping condition.
- **Suggestion**: Add a "## Scope Definition" section with explicit In scope (V1), Out of scope, and Walking skeleton entries.
```


### 边缘情况：文档完整且调查结果为零

**输入**：完全已满足需求文档，包括问题陈述、所有需求的可测试验收标准、约束库存、V1 范围、唯一验证 R-NN ID 以及带有解决计划的开放问题。

**预期输出**：

> 要求文档满足所有六个质量维度。所有必须有的需求都有可测试的验收标准；问题陈述没有解决方案；约束和假设是分开的； V1范围明确；所有需求都带有R-NN ID；开放性问题有解决计划。准备“设计解决方案”。

---

## 附录：输出合约

每项调查结果必须遵循标准调查结果格式：

|元素|要求|
| :--- | :--- |
| **位置** |章节标题（例如“## 问题陈述”）或需求 ID（例如“R-03”）或“（文档级别）”（如果不存在特定锚点）。 |
| **类别** | “需求-质量”。 |
| **严重性** | `关键` \| `主要` \| `次要` \| `建议`。 |
| **标题** |简短的一行摘要。 |
| **描述** |用 1-3 句话解释问题。 |
| **建议** |具体改进方向（可选但强烈推荐）。 |

示例：


```markdown
- **Location**: `## Constraint Inventory`
- **Category**: requirements-quality
- **Severity**: minor
- **Title**: Assumptions not separated from real constraints
- **Description**: The constraint list mixes validated facts (e.g. "team has 3 engineers") with unvalidated assumptions (e.g. "users will have mobile devices"). Without separation, risk is hidden.
- **Suggestion**: Split into two sub-sections: "Real Constraints (Validated)" and "Assumptions (Unvalidated — need validation plan)".
```