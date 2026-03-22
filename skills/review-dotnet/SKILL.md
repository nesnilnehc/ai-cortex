---
name: review-dotnet
description: "Review .NET (C#/F#) code for language and runtime conventions: async/await, nullable, API versioning, IDisposable, LINQ, and testability. Language-only atomic skill; output is a findings list."
description_zh: 按 .NET (C#/F#) 语言与运行时规范审查代码：async/await、nullable、API 版本、IDisposable、LINQ、可测性。
tags: [code-review]
version: 1.0.0
license: MIT
recommended_scope: project
metadata:
  author: ai-cortex
triggers: [review dotnet, review csharp]
input_schema:
  type: code-scope
  description: Source files or directories to review
output_schema:
  type: findings-list
  description: Zero or more findings with location, category, severity, and suggestion
---

# 技能（Skill）：回顾.NET

## 目的 (Purpose)

仅查看 **.NET** 生态系统（C#、F#）中的代码的**语言和运行时约定**。不要定义范围（差异与代码库）或执行安全/架构分析；这些是通过范围和cognitive技能来处理的。以标准格式发出**结果列表**以进行聚合。重点关注 async/await 和 ConfigureAwait、可空引用类型和 NRE 避免、API 和版本控制、资源和 IDisposable、集合和 LINQ 以及可测试性。

---

## 核心目标（Core Objective）

**首要目标**：生成 .NET 语言/运行时结果列表，涵盖异步/等待、可空类型、API 稳定性、资源管理、LINQ 使用以及给定代码范围的可测试性。

**成功标准**（必须满足所有要求）：

1. ✅ **仅限 .NET 范围**：仅审查 .NET (C#/F#) 语言和运行时约定；未执行范围选择、安全性或架构分析
2. ✅ **涵盖所有六个 .NET 维度**：异步/等待、可空引用类型、API/版本控制、资源/IDisposable、集合/LINQ 和可测试性（如果相关）
3. ✅ **结果格式兼容**：每个结果包括位置、类别（`language-dotnet`）、严重性、标题、描述和可选建议
4. ✅ **文件：行引用**：所有发现都引用带有行号的特定文件位置
5. ✅ **排除非 .NET 代码**：除非明确在范围内，否则不会分析非 .NET 文件的 .NET 特定规则

**验收**测试：输出是否包含以 .NET 为中心的结果列表，其中文件：行引用涵盖所有相关语言/运行时维度，而无需执行安全性、体系结构或范围分析？

---

## 范围边界（范围边界）

**本技能负责**：

- async/await 正确性和ConfigureAwait 用法（库与应用程序代码）
- 可空引用类型和 NRE 避免
- 公共API稳定性和版本控制策略
- IDisposable、IAsyncDisposable 和 using 语句模式
- 集合和 LINQ 效率（多重枚举、分配、跨度/内存）
- 可测试性（DI、密封/可重写、静态使用）

**本技能不负责**：

- 范围选择——范围由调用者提供
- 安全分析（注入、身份验证、加密）——使用“review-security”
- 架构分析——使用“review-architecture”
- 性能深入研究——使用“review-performance”
- 全面精心策划的审核——使用“审核代码”
- 代码库状态审查 — 使用 `review-codebase`

**转交点**：当所有 .NET 发现结果发布后，将其移交给“review-code”进行聚合。对于 .NET 代码中发现的安全或体系结构问题，请记下它们并建议运行适当的cognitive技能。

---

## 使用场景（用例）

- **精心安排的审查**：当 [review-code](../review-code/SKILL.md) 运行 .NET 项目的范围 → 语言 → 框架 → 库 → cognitive时，用作语言步骤。
- **仅.NET 审查**：当用户只想检查语言/运行时约定时（例如，添加新的 C# 文件后）。
- **PR .NET 预检查清单**：确保异步、可空和资源模式正确。

**何时使用**：当正在审查的代码是.NET (C#/F#) 并且任务包括语言/运行时质量时。范围（差异与路径）由调用者或用户确定。

---

## 行为（行为）

### 该技能的范围

- **分析**：**给定代码范围**（调用者提供的文件或 diff）中的 .NET 语言和运行时约定。不决定范围；接受代码范围作为输入。
- **不要**：执行范围选择（差异与代码库）、安全审查或架构审查；除非要求忽略语言，否则不要查看非 .NET 文件。

### 审核清单（仅限 .NET 维度）

1. **async/await和ConfigureAwait**：async的正确使用；在适当的情况下配置Await(false)（库代码）；取消令牌传播；避免 async void 除了事件处理程序。
2. **可空引用类型和NRE**：可空注释；在合理的情况下进行空值检查和空值宽容；避免不必要的 null-forgiving。
3. **API和版本控制**：公共API表面稳定性；重大变更；库的版本控制或弃用策略。
4. **资源和IDisposable**：正确使用IDisposable、using语句、IAsyncDisposable；没有泄漏的手柄或流。
5. **集合和LINQ**：适当使用LINQ；分配和枚举；避免多重枚举；相关的跨度/内存。
6. **可测试性**：依赖注入和可测试性；静态使用；在影响测试的地方密封/可重写。

### 语气和参考

- **专业和技术**：参考具体位置（文件：行）。发出包含位置、类别、严重性、标题、描述、建议的结果。

---

## 输入与输出 (Input & Output)

### 输入（输入）

- **代码范围**：用户或范围技能已选择的文件或目录（或差异）。该技能不决定范围；它仅检查所提供的 .NET 代码的语言约定。

### 输出（输出）

- 以**附录：输出合同**中定义的格式发出零个或多个**结果**。
- 此技能的类别是 **语言-dotnet**。

---

## 限制（限制）

### 硬边界（Hard Boundaries）

- **不要**执行安全、架构或范围选择。遵守 .NET 语言和运行时约定。
- **不要**在没有具体地点或可行建议的情况下给出结论。
- **不要**检查非 .NET 代码的 .NET 特定规则，除非用户明确包含它（例如嵌入脚本）。

### 技能边界 (Skill Boundaries)

**不要做这些**（其他技能可以处理它们）：

- 不要选择或定义代码范围 - 范围由调用者或“审查代码”确定
- 不要执行安全分析——使用“review-security”
- 不要执行架构分析——使用“review-architecture”
- 不要审查 .NET 约定的非 .NET 代码

**何时停止并交接**：

- 当所有 .NET 发现结果发布后，将其交给“review-code”进行聚合
- 当用户需要全面审查（范围+语言+cognitive）时，重定向到“审查代码”
- 当.NET代码中发现安全问题时，记下它们并建议“审查安全性”

---

## 自检（Self-Check）

### 核心成功标准

- [ ] **仅限 .NET 范围**：仅审查 .NET (C#/F#) 语言和运行时约定；未执行范围选择、安全性或架构分析
- [ ] **涵盖所有六个 .NET 维度**：异步/等待、可空引用类型、API/版本控制、资源/IDisposable、集合/LINQ 和可测试性（如果相关）
- [ ] **符合调查结果格式**：每个调查结果包括位置、类别（`language-dotnet`）、严重性、标题、描述和可选建议
- [ ] **文件：行引用**：所有结果都引用带有行号的特定文件位置
- [ ] **排除非 .NET 代码**：除非明确在范围内，否则不会分析非 .NET 文件的 .NET 特定规则

### 流程质量检查

- [ ] 是否仅审查了 .NET 语言/运行时维度（无范围/安全/架构）？
- [ ] 是否涵盖了相关的异步、可空、IDisposable、LINQ 和可测试性？
- [ ] 每个发现是否都包含位置、类别=语言-dotnet、严重性、标题、描述和可选建议？
- [ ] file:line 是否引用了问题？

### 验收测试

输出是否包含以 .NET 为中心的结果列表，其中包含文件：行引用，涵盖所有相关语言/运行时维度，而无需执行安全性、体系结构或范围分析？

---

## 示例（示例）

### 示例 1：异步方法

- **输入**：异步的 C# 方法，无需传递 CancellationToken 即可调用其他异步方法。
- **预期**：发出 CancellationToken 传播的发现（例如次要/建议）；参考方法和参数列表。类别 = 语言-dotnet.

### 示例 2：可空和处置

- **Input**：持有 IDisposable 且不实现 IDisposable 或使用 using 的 C# 类。
- **预期**：发出资源处置的结果，如果字段可以为空，则可能可以为空。类别 = 语言-dotnet.

### 边缘情况：混合 C# 和 SQL

- **输入**：包含 C# 和嵌入式 SQL 字符串的文件。
- **预期**：仅查看 .NET 约定的 C# 部分（例如异步、可空、处置）。不要发出 SQL 注入结果；这是用于 review-security 或 review-sql。

---

## 附录：输出合约

每项调查结果必须遵循标准调查结果格式：

|元素|要求|
| :--- | :--- |
| **位置** | `path/to/file.ext`（可选行或范围）。 |
| **类别** | `语言-dotnet`。 |
| **严重性** | `关键` \| `主要` \| `次要` \| `建议`。 |
| **标题** |简短的一行摘要。 |
| **描述** | 1-3 句话。 |
| **建议** |具体修复或改进（可选）。 |

示例：


```markdown
- **Location**: `src/Services/DataLoader.cs:22`
- **Category**: language-dotnet
- **Severity**: minor
- **Title**: Async method does not accept or forward CancellationToken
- **Description**: Long-running or cancellable operations should support cancellation.
- **Suggestion**: Add CancellationToken parameter and pass it to underlying async calls.
```