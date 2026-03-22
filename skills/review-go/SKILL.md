---
name: review-go
description: "Review Go code for language and runtime conventions: concurrency, context usage, error handling, resource management, API stability, type semantics, and testability. Language-only atomic skill; output is a findings list."
description_zh: 按 Go 语言与运行时规范审查代码：并发、context、错误处理、资源管理、API 稳定性、类型语义、可测性。
tags: [code-review]
version: 1.0.0
license: MIT
recommended_scope: project
metadata:
  author: ai-cortex
triggers: [review go]
input_schema:
  type: code-scope
  description: Source files or directories to review
output_schema:
  type: findings-list
  description: Zero or more findings with location, category, severity, and suggestion
---

# 技能（Skill）：复习围棋

## 目的 (Purpose)

仅查看 **Go** 中的代码以了解 **语言和运行时约定**。不要定义范围（差异与代码库）或执行安全/架构分析；这些是通过范围和cognitive技能来处理的。以标准格式发出**结果列表**以进行聚合。重点关注并发和 goroutine 生命周期、上下文使用、错误处理、资源管理、API 稳定性、类型和零值语义以及可测试性。

---

## 核心目标（Core Objective）

**首要目标**：生成一个 Go 语言/运行时结果列表，涵盖给定代码范围的并发性、上下文使用、错误处理、资源管理、API 稳定性、类型语义和可测试性。

**成功标准**（必须满足所有要求）：

1. ✅ **Go-only 范围**：仅审查 Go 语言和运行时约定；未执行范围选择、安全性或架构分析
2. ✅ **涵盖所有七个 Go 维度**：在相关的情况下评估并发/goroutine 生命周期、上下文使用、错误处理、资源管理、API 稳定性、类型/零值语义和可测试性
3. ✅ **符合调查结果格式**：每个调查结果包括位置、类别（`语言-go`）、严重性、标题、描述和可选建议
4. ✅ **文件：行引用**：所有发现都引用带有行号的特定文件位置
5. ✅ **排除非 Go 代码**：除非明确在范围内，否则不会分析非 Go 文件的 Go 特定规则

**验收测试**：输出是否包含以 Go 为中心的结果列表，其中包含 file:line 引用，涵盖所有相关语言/运行时维度，而无需执行安全性、架构或范围分析？

---

## 范围边界（范围边界）

**本技能负责**：

- Goroutine 生命周期和泄漏预防（通道关闭、取消、WaitGroup）
- 通过请求路径的上下文传播
- 错误处理（用 `%w`、`errors.Is/As` 包装，避免因预期错误而出现恐慌）
- 资源管理（defer Close()、resp.Body.Close()、context cancel()）
- API稳定性和Go模块（导出类型、向后兼容性、go.mod）
- 类型和零值语义（nil 接口与类型化 nil、指针/值接收器、切片/映射初始化）
- 可测试性（小接口、全局注入、确定性测试接缝）

**本技能不负责**：

- 范围选择——范围由调用者提供
- 安全分析——使用“review-security”
- 架构分析——使用“review-architecture”
- SQL 特定分析 — 使用 `review-sql`
- 全面精心策划的审核——使用“审核代码”

**转交点**：当所有 Go 发现结果发布后，将其移交给 `review-code` 进行聚合。对于 SQL 或安全问题，请记下它们并建议适当的cognitive技能。

---

## 使用场景（用例）

- **精心安排的审查**：当 [review-code](../review-code/SKILL.md) 运行 Go 项目的范围 -> 语言 -> 框架 -> 库 -> cognitive时，用作语言步骤。
- **仅 Go 审查**：当用户只想检查语言/运行时约定时（例如，添加新的 Go 文件后）。
- **PR Go 前检查清单**：确保并发、上下文和错误处理模式正确。

**何时使用**：当正在审查的代码是Go并且任务包括语言/运行时质量时。范围（差异与路径）由调用者或用户确定。

---

## 行为（行为）

### 该技能的范围

- **分析**：**给定代码范围**（调用者提供的文件或 diff）中的 Go 语言和运行时约定。不决定范围；接受代码范围作为输入。
- **不要**：执行范围选择（差异与代码库）、安全审查或架构审查；不要检查非 Go 文件中特定于 Go 的规则，除非明确在范围内。

### 审查清单（仅限 Go 维度）

1. **并发和 goroutine 生命周期**：正确使用 goroutine、通道、同步原语、WaitGroup 使用、通道关闭、选择模式以及避免 goroutine 泄漏或数据竞争。
2. **上下文使用**：上下文通过请求路径传递，遵守取消和截止日期，避免请求处理程序中的 context.Background() ，并且不在长期存在的结构中存储上下文。
3. **错误处理**：检查并返回错误；用 `%w` 包裹；使用 `errors.Is/As`；避免因预期错误而恐慌；避免错误阴影。
4. **资源管理**：`defer Close()` 用于 io.Closer，`resp.Body.Close()` 用于 HTTP 响应，`Stop()` 用于计时器/Ticker，`cancel()` 用于上下文。
5. **API稳定性和模块**：导出API的稳定性、导出类型和接口的更改、向后兼容性以及Go版本/模块期望（go.mod、构建标签）。
6. **类型和零值语义**：Nil 接口与类型化 nil 陷阱、指针与值接收器、映射/切片初始化、切片的复制和别名以及零值正确性。
7. **可测试性和接口**：更喜欢小接口、注入而不是全局变量以及确定性测试的接缝。

### 语气和参考

- **专业和技术**：参考具体位置（文件：行）。发出包含位置、类别、严重性、标题、描述、建议的结果。

---

## 输入与输出 (Input & Output)

### 输入（输入）

- **代码范围**：用户或范围技能已选择的文件或目录（或差异）。该技能不决定范围；它仅检查所提供的 Go 代码的语言约定。

### 输出（输出）

- 以**附录：输出合同**中定义的格式发出零个或多个**结果**。
- 该技能的类别是**语言**。

---

## 限制（限制）

### 硬边界（Hard Boundaries）

- **不要**执行安全、架构或范围选择。遵守 Go 语言和运行时约定。
- **不要**在没有具体地点或可行建议的情况下给出结论。
- **不要**检查非 Go 代码的 Go 特定规则，除非用户明确包含它（例如嵌入的代码片段）。

### 技能边界 (Skill Boundaries)

**不要做这些**（其他技能可以处理它们）：

- 不要选择或定义代码范围 - 范围由调用者或“审查代码”确定
- 不要执行安全分析——使用“review-security”
- 不要执行架构分析——使用“review-architecture”
- 不要执行全面的 SQL 分析 — 使用 `review-sql`

**何时停止并交接**：

- 当所有 Go 发现结果发布后，将其交给“review-code”进行聚合
- 当用户需要全面审查（范围+语言+cognitive）时，重定向到“审查代码”
- 当发现 SQL 或安全问题时，记下它们并建议适当的cognitive技能

---

## 自检（Self-Check）

### 核心成功标准

- [ ] **Go-only 范围**：仅审查 Go 语言和运行时约定；未执行范围选择、安全性或架构分析
- [ ] **涵盖所有七个 Go 维度**：在相关的情况下评估并发/goroutine 生命周期、上下文使用、错误处理、资源管理、API 稳定性、类型/零值语义和可测试性
- [ ] **符合调查结果格式**：每个调查结果包括位置、类别（`语言-go`）、严重性、标题、描述和可选建议
- [ ] **文件：行引用**：所有结果都引用带有行号的特定文件位置
- [ ] **排除非 Go 代码**：除非明确在范围内，否则不会分析非 Go 文件的 Go 特定规则

### 流程质量检查

- [ ] 是否仅审查了 Go 语言/运行时维度（无范围/安全/架构）？
- [ ] 是否涵盖了相关的并发性、上下文使用、错误处理、资源管理、API 稳定性、类型语义和可测试性？
- [ ] 每个发现是否都包含位置、类别=语言、严重性、标题、描述和可选建议？
- [ ] file:line 是否引用了问题？

### 验收测试

输出是否包含以 Go 为中心的结果列表，其中包含涵盖所有相关语言/运行时维度的 file:line 引用，而无需执行安全性、架构或范围分析？

---

## 示例（示例）

### 示例 1：Goroutine 泄漏

- **输入**：Goroutine 在请求处理程序中启动，该处理程序等待从未关闭或取消的通道。
- **预期**：发出 goroutine 泄漏和丢失取消的结果；参考处理程序和通道用法。类别=语言-go。

### 示例 2：错误处理

- **输入**：函数返回 `fmt.Errorf("failed: %v", err)` 并且调用者将错误与 `==` 进行比较。
- **预期**：发出一个结果，用 `%w` 包装并使用 `errors.Is/As`；参考错误构造和比较。类别=语言-go。

### 示例 3：Nil 接口陷阱

- **输入**：函数返回`(*MyStruct)(nil)`作为`error`接口；调用者检查“if err != nil”。
- **预期**：发出分配给接口的类型化 nil 不是 nil 的结果；建议返回一个显式的“nil”。类别=语言-go。

### 边缘情况：Go 和 SQL 混合

- **输入**：带有用于数据库查询的嵌入式 SQL 字符串的 Go 文件。
- **预期**：仅查看 Go 约定（上下文使用、错误处理、资源清理）。不要发出 SQL 注入结果；这是用于 review-security 或 review-sql。

---

## 附录：输出合约

每项调查结果必须遵循标准调查结果格式：

|元素|要求 |
| :--- | :--- |
| **位置** | `path/to/file.ext`（可选行或范围）。 |
| **类别** | “语言去”。 |
| **严重性** | `关键` \| `主要` \| `次要` \| `建议`。 |
| **标题** |简短的一行摘要。 |
| **描述** | 1-3句话。 |
| **建议** |具体修复或改进（可选）。 |

示例：


```markdown
- **Location**: `internal/worker/pool.go:87`
- **Category**: language-go
- **Severity**: major
- **Title**: Goroutine leak due to missing cancellation
- **Description**: The goroutine blocks on a channel that is never closed or canceled, so it will leak per request.
- **Suggestion**: Pass a context and exit on cancellation, or close the channel when the work is done.
```