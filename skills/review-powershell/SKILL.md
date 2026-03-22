---
name: review-powershell
description: "Review PowerShell code for language and runtime conventions: advanced functions, parameter design, error handling, object pipeline behavior, compatibility, and testability. Language-only atomic skill; output is a findings list."
description_zh: 按 PowerShell 规范审查代码：高级函数、参数设计、错误处理、对象管道、兼容性与可测性。
tags: [code-review]
version: 1.0.0
license: MIT
recommended_scope: project
metadata:
  author: ai-cortex
triggers: [review powershell]
input_schema:
  type: code-scope
  description: Source files or directories to review
output_schema:
  type: findings-list
  description: Zero or more findings with location, category, severity, and suggestion
---

# 技能（Skill）：复习PowerShell

## 目的 (Purpose)

仅查看 **PowerShell** 中的代码的**语言和运行时约定**。不要定义范围（差异与代码库）或执行安全/架构分析；这些是通过范围和cognitive技能来处理的。以标准格式发出**结果列表**以进行聚合。重点关注高级功能设计、参数验证和绑定、错误处理语义、对象管道行为、模块/导出和命名约定、兼容性（Windows PowerShell 与 PowerShell 7+）和可测试性。

---

## 核心目标（Core Objective）

**首要目标**：生成 PowerShell 语言/运行时结果列表，涵盖给定代码范围的函数设计、参数契约、错误处理、管道行为、状态/范围、兼容性和可测试性。

**成功标准**（必须满足所有要求）：

1. ✅ **仅 PowerShell 范围**：仅审查 PowerShell 语言和运行时约定；未执行范围选择、安全性或架构分析
2. ✅ **涵盖所有七个 PowerShell 维度**：在相关的情况下评估高级函数/cmdlet 约定、参数设计/验证、错误处理语义、对象管道行为、状态/范围/严格性、兼容性/可移植性和可测试性
3. ✅ **结果格式兼容**：每个结果包括位置、类别（`language-powershell`）、严重性、标题、描述和可选建议
4. ✅ **文件：行引用**：所有发现都引用带有行号的特定文件位置
5. ✅ **排除非 PowerShell 代码**：除非明确在范围内，否则不会分析非 PowerShell 文件的 PowerShell 特定规则

**验收**测试：输出是否包含以 PowerShell 为中心的结果列表，其中文件：行引用涵盖所有相关语言/运行时维度，而无需执行安全性、体系结构或范围分析？

---

## 范围边界（范围边界）

**本技能负责**：

- `[CmdletBinding()]`、`Verb-Noun` 命名、批准的动词、`begin/process/end` 块
- 参数类型、“Mandatory”、“ValueFromPipeline”、参数集、验证属性
- 终止与非终止错误、“-ErrorAction Stop”、静默故障预防
- 对象管道行为（更喜欢对象而不是格式化文本，“Write-Host”与“Write-Verbose”）
- 状态、范围、严格性（全局/有状态副作用、偏好变量变化）
- Windows PowerShell 5.1 与 PowerShell 7+ 兼容性和可移植性
- 性能和可测试性（Pester友好的功能设计，DI接缝）

**本技能不负责**：

- 范围选择——范围由调用者提供
- 安全分析——使用“review-security”
- 架构分析——使用“review-architecture”
- 全面精心策划的审核——使用“审核代码”

**转交点**：当所有 PowerShell 发现结果发出后，将其移交给“review-code”进行聚合。对于安全问题（例如命令注入、凭证暴露），请记下它们并建议“审查安全性”。

---

## 使用场景（用例）

- **精心安排的审查**：当 [review-code](../review-code/SKILL.md) 运行 PowerShell 项目的范围 -> 语言 -> 框架 -> 库 -> cognitive时，用作语言步骤。
- **仅 PowerShell 审查**：当用户只想检查语言/运行时约定时。
- **PR 前脚本质量检查**：在合并之前验证参数约定、管道行为和错误语义。

**何时使用**：当正在审查的代码是 PowerShell（`.ps1`、`.psm1`、`.psd1`）并且任务包括语言/运行时质量时。范围由调用者或用户确定。

---

## 行为（行为）

### 该技能的范围

- **分析**：**给定代码范围**（调用者提供的文件或差异）中的 PowerShell 语言和运行时约定。不决定范围；接受代码范围作为输入。
- **不要**：执行范围选择、安全审查或架构审查；除非明确在范围内，否则不要检查非 PowerShell 文件中特定于 PowerShell 的规则。

### 查看清单（仅限 PowerShell 维度）

1. **高级函数和 cmdlet 约定**：在适当的情况下使用“[CmdletBinding()]”，使用经过批准的动词进行“动词-名词”命名，仅在需要时使用“begin/process/end”块。
2. **参数设计与验证**：参数类型、`Mandatory`、`ValueFromPipeline`、参数集、验证属性（`ValidateSet`、`ValidatePattern`、`ValidateScript`）是连贯的，不矛盾。
3. **错误处理语义**：区分终止错误和非终止错误；在需要时使用“-ErrorAction Stop”；避免静默失败和空的“catch”。
4. **对象管道行为**：内部流程优先选择对象而不是格式化文本；避免使用“Write-Host”进行数据输出；确保函数输出是可预测的并且是管道安全的。
5. **状态、范围和严格性**：避免意外的全局/有状态副作用、不受控制的偏好变量更改以及不明确的变量初始化；在适当的情况下使用严格模式。
6. **兼容性和可移植性**：考虑 Windows PowerShell 5.1 和 PowerShell 7+、特定于平台的命令/模块以及路径处理之间的差异。
7. **性能和可测试性**：避免昂贵的管道误用和重复的数组串联；用于 Pester 友好测试和依赖隔离的结构函数。

### 语气和参考

- **专业和技术**：参考具体位置（文件：行）。发出包含位置、类别、严重性、标题、描述、建议的结果。

---

## 输入与输出 (Input & Output)

### 输入（输入）

- **代码范围**：用户或范围技能已选择的文件或目录（或差异）。该技能不决定范围； it reviews the provided PowerShell code for language conventions only.

### 输出（输出）

- 以**附录：输出合同**中定义的格式发出零个或多个**结果**。
- 此技能的类别是 **language-powershell**。

---

## 限制（限制）

### 硬边界（Hard Boundaries）

- **不要**执行安全、架构或范围选择。遵守 PowerShell 语言和运行时约定。
- **不要**在没有具体地点或可行建议的情况下给出结论。
- **不要**检查非 PowerShell 代码的 PowerShell 特定规则，除非明确在范围内。

### 技能边界 (Skill Boundaries)

**不要做这些**（其他技能可以处理它们）：

- 不要选择或定义代码范围 - 范围由调用者或“审查代码”确定
- 不要执行安全分析（凭证处理、注入风险）——使用“review-security”
- 不要执行架构分析——使用“review-architecture”

**何时停止并交接**：

- 当所有 PowerShell 发现结果发出后，将其移交给“review-code”进行聚合
- 当用户需要全面审查（范围+语言+cognitive）时，重定向到“审查代码”
- 当发现安全问题（凭证暴露、命令注入）时，记下它们并建议“审查安全性”

---

## 自检（Self-Check）

### 核心成功标准

- [ ] **仅限 PowerShell 范围**：仅审查 PowerShell 语言和运行时约定；未执行范围选择、安全性或架构分析
- [ ] **涵盖所有七个 PowerShell 维度**：高级函数/cmdlet 约定、参数设计/验证、错误处理语义、对象管道行为、状态/范围/严格性、兼容性/可移植性和可测试性（如果相关）
- [ ] **结果格式兼容**：每个结果包括位置、类别（`language-powershell`）、严重性、标题、描述和可选建议
- [ ] **文件：行引用**：所有结果都引用带有行号的特定文件位置
- [ ] **排除非 PowerShell 代码**：除非明确在范围内，否则不会分析非 PowerShell 文件的 PowerShell 特定规则

### 流程质量检查

- [ ] 是否仅审查了 PowerShell 语言/运行时维度（无范围/安全/架构）？
- [ ] 是否涵盖了相关的函数/参数约定、错误处理、管道行为、兼容性和可测试性？
- [ ] 发布的每个发现是否包含位置、类别=语言-powershell、严重性、标题、描述和可选建议？
- [ ] file:line 是否引用了问题？

### 验收测试

输出是否包含以 PowerShell 为中心的结果列表，其中包含涵盖所有相关语言/运行时维度的 file:line 引用，而无需执行安全性、体系结构或范围分析？

---

## 示例（示例）

### 示例 1：管道合同不匹配

- **输入**：函数声明管道输入，但未声明“ValueFromPipeline”，并且仅处理“end”中的完整数组。
- **预期**：发出管道合同不匹配的结果并建议参数属性+“流程”用法。类别=语言-powershell。

### 示例 2：错误处理

- **输入**：脚本将有风险的命令包装在“try/catch”中，但不设置“-ErrorAction Stop”，因此非终止错误绕过“catch”。
- **预期**：发出无效错误处理的结果；建议明确的终止行为。类别=语言-powershell。

### 边缘情况：数据输出被主机写入污染

- **输入**：函数返回对象，但也在处理循环中使用“Write-Host”。
- **预期**：发出混合演示/数据输出的结果，这会损害自动化和composability；建议使用“Write-Verbose”/“Write-Information”进行诊断并为管道使用者提供干净的对象输出。

---

## 附录：输出合约

每项调查结果必须遵循标准调查结果格式：

|元素|要求|
| :--- | :--- |
| **位置** | `path/to/file.ext`（可选行或范围）。 |
| **类别** | `语言-powershell`。 |
| **严重性** | `关键` \| `主要` \| `次要` \| `建议`。 |
| **标题** |简短的一行摘要。 |
| **描述** | 1-3句话。 |
| **建议** |具体修复或改进（可选）。 |

示例：


```markdown
- **Location**: `scripts/Build.ps1:34`
- **Category**: language-powershell
- **Severity**: major
- **Title**: Function output mixes objects and host-formatted text
- **Description**: The function emits `Write-Host` output in the data path, which makes automation output unstable.
- **Suggestion**: Return structured objects only and move diagnostics to `Write-Verbose` or `Write-Information`.
```