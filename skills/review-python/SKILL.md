---
name: review-python
description: "Review Python code for language and runtime conventions: type hints, exceptions, async/await, context managers, dependencies, and testability. Language-only atomic skill; output is a findings list."
description_zh: 按 Python 规范审查代码：类型提示、异常、async/await、上下文管理器、依赖与可测性。
tags: [code-review]
version: 1.0.0
license: MIT
recommended_scope: project
metadata:
  author: ai-cortex
triggers: [review python]
input_schema:
  type: code-scope
  description: Source files or directories to review
output_schema:
  type: findings-list
  description: Zero or more findings with location, category, severity, and suggestion
---

# 技能（Skill）：复习Python

## 目的 (Purpose)

仅查看 **Python** 中的代码的 **语言和运行时约定**。不要定义范围（差异与代码库）或执行安全/架构分析；这些是通过范围和cognitive技能来处理的。以标准格式发出**结果列表**以进行聚合。重点关注类型提示、异常处理、异步/等待模式、上下文管理器、依赖管理和可测试性。

---

## 核心目标（Core Objective）

**首要目标**：生成 Python 语言/运行时结果列表，涵盖类型提示、异常处理、异步/等待模式、上下文管理器、依赖项管理、命名约定和给定代码范围的可测试性。

**成功标准**（必须满足所有要求）：

1. ✅ **仅限 Python 范围**：仅审查 Python 语言和运行时约定；未执行范围选择、安全性或架构分析
2. ✅ **涵盖所有八个 Python 维度**：类型提示、异常处理、异步/等待、上下文管理器、依赖项管理、可变默认值、命名约定 (PEP8) 和可测试性（如果相关）进行评估
3. ✅ **结果格式兼容**：每个结果包括位置、类别（`language-python`）、严重性、标题、描述和可选建议
4. ✅ **文件：行引用**：所有发现都引用带有行号的特定文件位置
5. ✅ **排除非 Python 代码**：除非明确在范围内，否则不会分析非 Python 文件的 Python 特定规则

**验收测试**：输出是否包含以 Python 为中心的结果列表，其中包含 file:line 引用，涵盖所有相关语言/运行时维度，而无需执行安全性、架构或范围分析？

---

## 范围边界（范围边界）

**本技能负责**：

- 类型提示（`typing` 模块、`Optional`、`Union`、泛型）
- 异常处理（特定异常，“raise ... from”，没有裸露的“ except:”，“try/finally”）
- 异步/等待模式（异步函数、异步上下文中的阻塞调用、`asyncio.gather`）
- 上下文管理器（`with`语句、`__enter__`/`__exit__`、`@contextmanager`）
- 依赖管理（固定依赖、避免“导入 *”、虚拟环境）
- 可变的默认参数（避免`def foo(a=[]):`）
- PEP8 命名约定（snake_case、PascalCase、SCREAMING_SNAKE_CASE）
- 可测试性（全局状态避免、DI、模拟友好设计）

**本技能不负责**：

- 范围选择——范围由调用者提供
- 安全分析——使用“review-security”
- 架构分析——使用“review-architecture”
- SQL 特定分析 — 使用 `review-sql`
- 全面精心策划的审核——使用“审核代码”

**转交点**：当所有 Python 发现结果发布后，将其交给 `review-code` 进行聚合。对于安全问题（注入、身份验证），请记下它们并建议“审查安全性”。

---

## 使用场景（用例）

- **精心安排的审查**：当 [review-code](../review-code/SKILL.md) 运行 Python 项目的范围 -> 语言 -> 框架 -> 库 -> cognitive时，用作语言步骤。
- **仅限 Python 的审查**：当用户只想检查语言/运行时约定时（例如，添加新的 Python 文件后）。
- **PR 前的 Python 检查表**：确保类型提示、异常处理和异步模式正确。

**何时使用**：当正在审查的代码是Python并且任务包括语言/运行时质量时。范围（差异与路径）由调用者或用户确定。

---

## 行为（行为）

### 该技能的范围

- **分析**：**给定代码范围**（调用者提供的文件或 diff）中的 Python 语言和运行时约定。不决定范围；接受代码范围作为输入。
- **不要**：执行范围选择（差异与代码库）、安全审查或架构审查；除非明确在范围内，否则不要检查非 Python 文件中的 Python 特定规则。

### 审核清单（仅限 Python 维度）

1. **类型提示**：对于复杂类型使用 `typing` 模块，尽可能避免使用 `Any`，使用 `Optional[T]` 而不是 `T |对于 Python <3.10，无`，正确使用 `Union`、`List`、`Dict`、`Callable` 和泛型类型提示。
2. **异常处理**：捕获特定异常，避免裸露的` except:`，使用`raise ... from`进行异常链接，避免在没有日志记录的情况下吞噬异常，正确使用`try/finally`。
3. **异步/等待**：正确使用`async def`和`await`，避免异步函数中的阻塞调用，异步上下文中正确的异常处理，使用`asyncio.gather`，`asyncio.create_task`实现并发。
4. **上下文管理器**：使用`with`语句进行​​资源管理，实现`__enter__`/`__exit__`或使用`@contextmanager`，避免手动打开/关闭。
5. **依赖管理**：将依赖项固定在`需求.txt`或`pyproject.toml`中，避免`import *`，使用虚拟环境，正确使用`sys.path`操作。
6. **可变默认值**：避免可变默认参数（例如 `def foo(a=[]):`），使用 `None` 并在函数内部初始化。
7. **命名约定**：遵循 PEP8（函数/变量使用 snake_case，类使用 PascalCase，常量使用 SCREAMING_SNAKE_CASE）。
8. **可测试性**：避免全局状态，使用依赖注入，模拟外部服务，避免紧密耦合。

### 语气和参考

- **专业和技术**：参考具体位置（文件：行）。发出包含位置、类别、严重性、标题、描述、建议的结果。

---

## 输入与输出 (Input & Output)

### 输入（输入）

- **代码范围**：用户或范围技能已选择的文件或目录（或差异）。该技能不决定范围；它仅检查所提供的 Python 代码的语言约定。

### 输出（输出）

- 以**附录：输出合同**中定义的格式发出零个或多个**结果**。
- 此技能的类别是**语言-python**。

---

## 限制（限制）

### 硬边界（Hard Boundaries）

- **不要**执行安全、架构或范围选择。遵守 Python 语言和运行时约定。
- **不要**在没有具体地点或可行建议的情况下给出结论。
- **不要**检查非 Python 代码的 Python 特定规则，除非用户明确包含它（例如嵌入的代码片段）。

### 技能边界 (Skill Boundaries)

**不要做这些**（其他技能可以处理它们）：

- 不要选择或定义代码范围 - 范围由调用者或“审查代码”确定
- 不要执行安全分析——使用“review-security”
- 不要执行架构分析——使用“review-architecture”
- 不要执行全面的 SQL 分析 — 使用 `review-sql`

**何时停止并交接**：

- 当所有 Python 发现结果发布后，将其交给“review-code”进行聚合
- 当用户需要全面审查（范围+语言+cognitive）时，重定向到“审查代码”
- 当发现安全问题时（例如 SQL 注入、命令注入），记下它们并建议 `review-security`

---

## 自检（Self-Check）

### 核心成功标准

- [ ] **仅限 Python 范围**：仅审查 Python 语言和运行时约定；未执行范围选择、安全性或架构分析
- [ ] **涵盖所有八个 Python 维度**：类型提示、异常处理、异步/等待、上下文管理器、依赖项管理、可变默认值、命名约定 (PEP8) 和可测试性（如果相关）进行评估
- [ ] **结果格式兼容**：每个结果包括位置、类别（`language-python`）、严重性、标题、描述和可选建议
- [ ] **文件：行引用**：所有结果都引用带有行号的特定文件位置
- [ ] **排除非 Python 代码**：除非明确在范围内，否则不会分析非 Python 文件的 Python 特定规则

### 流程质量检查

- [ ] 是否仅审查了 Python 语言/运行时维度（无范围/安全/架构）？
- [ ] 是否涵盖了相关的类型提示、异常处理、异步模式、上下文管理器和可测试性？
- [ ] 每个发现是否都包含位置、类别=语言-python、严重性、标题、描述和可选建议？
- [ ] file:line 是否引用了问题？

### 验收测试

输出是否包含以 Python 为中心的结果列表，其中包含涵盖所有相关语言/运行时维度的 file:line 引用，而无需执行安全性、体系结构或范围分析？

---

## 示例（示例）

### 示例 1：可变默认参数

- **输入**：`def foo(items=[]):`
- **预期**：发出可变默认参数的结果；建议使用“None”并在内部初始化。类别 = 语言-python。

### 示例 2：除了

- **输入**：`除了：通过`
- **Expected**: Emit a finding to catch specific exceptions;引用裸露的 except 子句。类别 = 语言-python。

### 示例 3：异步阻塞调用

- **输入**：异步函数内的`async def fetch(): requests.get(url)`。
- **预期**：发出使用“aiohttp”或“httpx”的发现；引用阻塞调用。类别 = 语言-python。

### 边缘情况：Python 和 SQL 混合

- **输入**：带有用于数据库查询的嵌入式 SQL 字符串的 Python 文件。
- **预期**：仅查看 Python 约定（类型提示、异常处理）。不要发出 SQL 注入结果；这是用于 review-security 或 review-sql。

---

## 附录：输出合约

每项调查结果必须遵循标准调查结果格式：

|元素|要求 |
| :--- | :--- |
| **位置** | `path/to/file.ext`（可选行或范围）。 |
| **类别** | `语言-python`。 |
| **严重性** | `关键` \| `主要` \| `次要` \| `建议`。 |
| **标题** |简短的一行摘要。 |
| **描述** | 1-3句话。 |
| **建议** |具体修复或改进（可选）。 |

示例：


```markdown
- **Location**: `utils/helpers.py:42`
- **Category**: language-python
- **Severity**: major
- **Title**: Mutable default argument
- **Description**: Using a list as default argument leads to shared state across calls.
- **Suggestion**: Use `def foo(items=None):` and initialize with `if items is None: items = []`.
```