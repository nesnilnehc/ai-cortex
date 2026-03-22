---
name: review-java
description: "Review Java code for language and runtime conventions: concurrency, exceptions, try-with-resources, API versioning, collections and Streams, NIO, and testability. Language-only atomic skill; output is a findings list."
description_zh: 按 Java 语言与运行时规范审查代码：并发、异常、try-with-resources、API 版本、集合与 Stream、NIO、可测性。
tags: [code-review]
version: 1.0.0
license: MIT
recommended_scope: project
metadata:
  author: ai-cortex
triggers: [review java]
input_schema:
  type: code-scope
  description: Source files or directories to review
output_schema:
  type: findings-list
  description: Zero or more findings with location, category, severity, and suggestion
---

# 技能（Skill）：复习Java

## 目的 (Purpose)

仅检查 **Java** 中的代码的 **语言和运行时约定**。不要定义范围（差异与代码库）或执行安全/架构分析；这些是通过范围和cognitive技能来处理的。以标准格式发出**结果列表**以进行聚合。重点关注并发和线程安全、异常和资源尝试、API 和版本兼容性、集合和流、NIO 和正确关闭、相关模块 (JPMS) 以及可测试性。

---

## 核心目标（Core Objective）

**首要目标**：生成 Java 语言/运行时结果列表，涵盖给定代码范围的并发性、异常、资源管理、API 兼容性、集合/流、NIO 和可测试性。

**成功标准**（必须满足所有要求）：

1. ✅ **仅限 Java 范围**：仅审查 Java 语言和运行时约定；未执行范围选择、安全性或架构分析
2. ✅ **涵盖所有六个 Java 维度**：在相关的情况下评估并发/线程安全、异常/资源、API/版本兼容性、集合/流、NIO/关闭和可测试性
3. ✅ **结果格式兼容**：每个结果包括位置、类别（`language-java`）、严重性、标题、描述和可选建议
4. ✅ **文件：行引用**：所有发现都引用带有行号的特定文件位置
5. ✅ **排除非 Java 代码**：除非明确在范围内，否则不会分析非 Java 文件的 Java 特定规则

**验收测试**：输出是否包含以 Java 为中心的结果列表，其中包含 file:line 引用，涵盖所有相关语言/运行时维度，而无需执行安全性、架构或范围分析？

---

## 范围边界（范围边界）

**本技能负责**：

- 并发和线程安全（同步、易失性、并发集合、执行器生命周期）
- 异常处理（try-with-resources、Throwable 层次结构、重新抛出模式）
- API 稳定性和版本兼容性（已弃用的 API、JPMS 边界）
- 集合和流 API（分配、装箱、副作用、不变性）
- NIO 和资源关闭（流、通道、选择器）
- 可测试性（DI、单例使用、最终/可重写设计）

**本技能不负责**：

- 范围选择——范围由调用者提供
- 安全分析——使用“review-security”
- 架构分析——使用“review-architecture”
- SQL 特定分析 — 使用 `review-sql`
- 全面精心策划的审核——使用“审核代码”

**转交点**：当所有 Java 发现结果发布后，将其交给“review-code”进行聚合。对于 Java 代码中发现的 SQL 或安全问题，请记下它们并建议适当的cognitive技能。

---

## 使用场景（用例）

- **精心安排的审查**：当 [review-code](../review-code/SKILL.md) 运行 Java 项目的范围 → 语言 → 框架 → 库 → cognitive时，用作语言步骤。
- **仅 Java 审查**：当用户只想检查语言/运行时约定时。
- **PR 前 Java 检查表**：确保并发、资源管理和 API 兼容性正确。

**何时使用**：当正在审查的代码是 Java 并且任务包括语言/运行时质量时。范围由调用者或用户确定。

---

## 行为（行为）

### 该技能的范围

- **分析**：**给定代码范围**（调用者提供的文件或 diff）中的 Java 语言和运行时约定。不决定范围；接受代码范围作为输入。
- **不要**：执行范围选择、安全审查或架构审查；除非明确在范围内，否则不要检查非 Java 文件中的 Java 规则。

### 审查清单（仅限 Java 维度）

1. **并发和线程安全**：正确使用synchronized、易失性、锁或并发API；可见性和发生之前；共享可变状态；执行器的使用和关闭。
2. **例外和资源**：Closeable/AutoCloseable 的 try-with-resources；异常处理和抑制；避免空捕获或过于宽泛的捕获。
3. **API及版本兼容性**：公共API稳定性；向后兼容性；使用已弃用的 API 和迁移路径； module boundaries (JPMS) if applicable.
4. **Collections 和 Streams**：Stream API 的适当使用；流中的副作用；分配和拳击；在适当的情况下使用不可变集合。
5. **NIO和关闭**：正确关闭流、通道和选择器；避免资源泄漏；使用尝试资源。
6. **可测试性**：依赖注入；静态和单例使用；可重写 vs 最终；测试双打和嘲笑。

### 语气和参考

- **专业和技术**：参考具体位置（文件：行）。发出包含位置、类别、严重性、标题、描述、建议的结果。

---

## 输入与输出 (Input & Output)

### 输入（输入）

- **代码范围**：用户或范围技能已选择的文件或目录（或差异）。该技能不决定范围；它仅检查所提供的 Java 代码的语言约定。

### 输出（输出）

- 以**附录：输出合同**中定义的格式发出零个或多个**结果**。
- 该技能的类别是**语言-java**。

---

## 限制（限制）

### 硬边界（Hard Boundaries）

- **不要**执行安全、架构或范围选择。遵守 Java 语言和运行时约定。
- **不要**在没有具体地点或可行建议的情况下给出结论。
- **不要**检查非 Java 代码的 Java 特定规则，除非明确在范围内。

### 技能边界 (Skill Boundaries)

**不要做这些**（其他技能可以处理它们）：

- 不要选择或定义代码范围 - 范围由调用者或“审查代码”确定
- 不要执行安全分析——使用“review-security”
- 不要执行架构分析——使用“review-architecture”
- 不要执行全面的 SQL 分析 — 使用 `review-sql`

**何时停止并交接**：

- 当所有 Java 发现结果发布后，将其交给“review-code”进行聚合
- 当用户需要全面审查（范围+语言+cognitive）时，重定向到“审查代码”
- 当发现 SQL 或安全问题时，记下它们并建议适当的cognitive技能

---

## 自检（Self-Check）

### 核心成功标准

- [ ] **仅限 Java 范围**：仅审查 Java 语言和运行时约定；未执行范围选择、安全性或架构分析
- [ ] **涵盖所有六个 Java 维度**：在相关的情况下评估并发/线程安全、异常/资源、API/版本兼容性、集合/流、NIO/关闭和可测试性
- [ ] **结果格式兼容**：每个结果包括位置、类别（`language-java`）、严重性、标题、描述和可选建议
- [ ] **文件：行引用**：所有结果都引用带有行号的特定文件位置
- [ ] **排除非 Java 代码**：除非明确在范围内，否则不会分析非 Java 文件的 Java 特定规则

### 流程质量检查

- [ ] 是否仅审查了 Java 语言/运行时维度（无范围/安全/架构）？
- [ ] 是否涵盖了相关的并发、异常、资源、集合/流、NIO 和可测试性？
- [ ] 每个发现是否都包含位置、类别=语言-java、严重性、标题、描述和可选建议？
- [ ] file:line 是否引用了问题？

### 验收测试

输出是否包含以 Java 为中心的结果列表，其中包含涵盖所有相关语言/运行时维度的 file:line 引用，而无需执行安全性、体系结构或范围分析？

---

## 示例（示例）

### 示例 1：资源和异常

- **Input**：打开InputStream并且不使用try-with-resources的Java方法。
- **预期**：发出资源管理结果；建议尝试使用资源。类别=语言-java。

### 示例 2：并发

- **输入**：从多个线程访问的共享可变列表，无需同步或并发收集。
- **预期**：发出线程安全的发现（例如使用 CopyOnWriteArrayList 或同步）；参考字段和用法。类别=语言-java。

### 边缘情况：混合 Java 和 SQL

- **输入**：具有 JDBC 或 JPA 和 Java 逻辑的文件。
- **预期**：仅查看 Java 约定（资源、异常、并发）。不要在此处发出 SQL 注入结果；这是用于 review-security 或 review-sql。

---

## 附录：输出合约

每项调查结果必须遵循标准调查结果格式：

|元素|要求|
| :--- | :--- |
| **位置** | `path/to/file.ext`（可选行或范围）。 |
| **类别** | `语言-java`。 |
| **严重性** | `关键` \| `主要` \| `次要` \| `建议`。 |
| **标题** |简短的一行摘要。 |
| **描述** | 1-3 句话。 |
| **建议** |具体修复或改进（可选）。 |

示例：


```markdown
- **Location**: `src/main/java/com/example/Loader.java:45`
- **Category**: language-java
- **Severity**: major
- **Title**: InputStream not closed in all paths
- **Description**: Leak possible if an exception is thrown before close.
- **Suggestion**: Use try-with-resources for the InputStream.
```