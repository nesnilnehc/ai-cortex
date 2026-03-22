---
name: review-php
description: "Review PHP code for language and runtime conventions: strict types, error handling, resource management, PSR standards, namespaces, null safety, generators, and testability. Language-only atomic skill; output is a findings list."
description_zh: 按 PHP 语言与运行时规范审查代码：strict types、错误处理、资源管理、PSR、命名空间、null 安全、生成器、可测性。
tags: [code-review]
version: 1.0.0
license: MIT
recommended_scope: project
metadata:
  author: ai-cortex
triggers: [review php]
input_schema:
  type: code-scope
  description: Source files or directories to review
output_schema:
  type: findings-list
  description: Zero or more findings with location, category, severity, and suggestion
---

# 技能（Skill）：复习PHP

## 目的 (Purpose)

仅查看 **PHP** 中的代码以了解 **语言和运行时约定**。不要定义范围（差异与代码库）或执行安全/架构分析；这些是通过范围和cognitive技能来处理的。以标准格式发出**结果列表**以进行聚合。重点关注严格的类型和声明、错误处理、资源管理、PSR 标准（PSR-4、PSR-12）、命名空间、空安全、生成器和可迭代、PHP 版本兼容性和可测试性。

---

## 核心目标（Core Objective）

**首要目标**：生成 PHP 语言/运行时结果列表，涵盖严格类型、错误处理、资源管理、PSR 标准、命名空间、空安全、生成器、版本兼容性和给定代码范围的可测试性。

**成功标准**（必须满足所有要求）：

1. ✅ **仅限 PHP 范围**：仅审查 PHP 语言和运行时约定；未执行范围选择、安全性或架构分析
2. ✅ **涵盖所有九个 PHP 维度**：严格类型、错误处理、资源管理、PSR 标准、命名空间/自动加载、空安全、生成器/可迭代、PHP 版本兼容性和可测试性（如果相关）进行评估
3. ✅ **结果格式兼容**：每个结果包括位置、类别（`language-php`）、严重性、标题、描述和可选建议
4. ✅ **文件：行引用**：所有发现都引用带有行号的特定文件位置
5. ✅ **排除非 PHP 代码**：除非明确在范围内，否则不会分析非 PHP 文件的 PHP 特定规则

**验收测试**：输出是否包含以 PHP 为中心的结果列表，其中包含 file:line 引用，涵盖所有相关语言/运行时维度，而无需执行安全性、架构或范围分析？

---

## 范围边界（范围边界）

**本技能负责**：

- `declare(strict_types=1)`，类型化属性，参数，返回类型
- 异常处理（Throwable层次结构，try-catch-finally，无空catch）
- 资源管理（fopen/fclose、数据库连接、try-finally 模式）
- PSR-4自动加载和PSR-12编码风格
- 命名空间和自动加载的正确性
- 空合并（`??`）、空安全运算符（`?->`）、避免错误抑制
- 生成器和可迭代的正确性
- PHP 版本与composer.json 约束的兼容性
- 可测试性（DI、静态/单例避免、构造函数注入）

**本技能不负责**：

- 范围选择——范围由调用者提供
- 安全分析（注入、身份验证、CSRF）——使用“review-security”
- 架构分析——使用“review-architecture”
- SQL 特定分析 — 使用 `review-sql`
- 全面精心策划的审核——使用“审核代码”

**转交点**：当所有 PHP 发现结果发出后，将其交给 `review-code` 进行聚合。对于 PHP 代码中发现的 SQL 注入或安全漏洞，请记下它们并建议“review-security”。

---

## 使用场景（用例）

- **精心安排的审查**：当 [review-code](../review-code/SKILL.md) 运行 PHP 项目的范围 → 语言 → 框架 → 库 → cognitive时，用作语言步骤。
- **仅 PHP 审查**：当用户只想检查语言/运行时约定时（例如，添加新的 PHP 文件后）。
- **PR 前 PHP 检查表**：确保类型安全、资源清理和 PSR 合规性正确。

**何时使用**：当正在审查的代码是 PHP 并且任务包括语言/运行时质量时。范围由调用者或用户确定。

---

## 行为（行为）

### 该技能的范围

- **分析**：**给定代码范围**（调用者提供的文件或差异）中的 PHP 语言和运行时约定。不决定范围；接受代码范围作为输入。
- **不要**：执行范围选择、安全审查或架构审查；除非明确在范围内，否则不要检查非 PHP 文件中的 PHP 特定规则。

### 审查清单（仅限 PHP 维度）

1. **Strict types and declarations**: `declare(strict_types=1)` usage;类型属性和参数；返回类型声明；避免隐式类型强制陷阱。
2. **错误处理**：异常与错误； `Throwable` 层次结构；正确的尝试捕获和重新抛出；避免空捕获或过于宽泛的捕获；相关的“error_reporting”和错误到异常的转换。
3. **资源管理**：`fopen`/`fclose`、数据库连接、流；确保资源已关闭（try-finally 或短期作用域）；避免资源泄漏。
4. **PSR 标准**：PSR-4 自动加载和命名空间到路径映射； PSR-12 编码风格（缩进、大括号、可见性）；类和方法的命名。
5. **命名空间和自动加载**：正确的`use`语句；避免全局命名空间污染；作曲家自动加载对齐。
6. **空安全**：空合并（`??`）、空安全运算符（`?->`）；避免“@”错误抑制；数组的“isset”与“array_key_exists”。
7. **生成器和迭代**：正确的`yield`用法；正确的迭代器实现；大型数据集的内存高效迭代。
8. **PHP版本兼容性**：使用的功能与composer.json中的“php”约束；已弃用的 API 和迁移路径。
9. **可测试性**：依赖注入；静态和单例使用；构造函数注入；用于嘲笑的接缝。

### 语气和参考

- **专业和技术**：参考具体位置（文件：行）。发出包含位置、类别、严重性、标题、描述、建议的结果。

---

## 输入与输出 (Input & Output)

### 输入（输入）

- **代码范围**：用户或范围技能已选择的文件或目录（或差异）。该技能不决定范围；它仅检查所提供的 PHP 代码的语言约定。

### 输出（输出）

- 以**附录：输出合同**中定义的格式发出零个或多个**结果**。
- 该技能的类别是**语言-php**。

---

## 限制（限制）

### 硬边界（Hard Boundaries）

- **不要**执行安全、架构或范围选择。遵守 PHP 语言和运行时约定。
- **不要**在没有具体地点或可行建议的情况下给出结论。
- **不要**检查非 PHP 代码的 PHP 特定规则，除非明确在范围内。

### 技能边界 (Skill Boundaries)

**不要做这些**（其他技能可以处理它们）：

- 不要选择或定义代码范围 - 范围由调用者或“审查代码”确定
- 不要执行安全分析（SQL 注入、XSS、CSRF）——使用“review-security”
- 不要执行架构分析——使用“review-architecture”
- 不要执行全面的 SQL 分析 — 使用 `review-sql`

**何时停止并交接**：

- 当所有 PHP 发现结果发布后，将其交给“review-code”进行聚合
- 当用户需要全面审查（范围+语言+cognitive）时，重定向到“审查代码”
- 当发现 SQL 注入或安全问题时，记下它们并建议“审查安全性”

---

## 自检（Self-Check）

### 核心成功标准

- [ ] **仅限 PHP 范围**：仅审查 PHP 语言和运行时约定；未执行范围选择、安全性或架构分析
- [ ] **涵盖所有九个 PHP 维度**：严格类型、错误处理、资源管理、PSR 标准、命名空间/自动加载、空安全、生成器/可迭代、PHP 版本兼容性和可测试性（如果相关）进行评估
- [ ] **结果格式兼容**：每个结果包括位置、类别（`language-php`）、严重性、标题、描述和可选建议
- [ ] **文件：行引用**：所有结果都引用带有行号的特定文件位置
- [ ] **排除非 PHP 代码**：除非明确在范围内，否则不会分析非 PHP 文件的 PHP 特定规则

### 流程质量检查

- [ ] 是否仅审查了 PHP 语言/运行时维度（无范围/安全/架构）？
- [ ] 是否涵盖了相关的严格类型、错误处理、资源、PSR、命名空间、空安全、生成器、版本兼容性和可测试性？
- [ ] 每个发现是否都包含位置、类别=语言-php、严重性、标题、描述和可选建议？
- [ ] file:line 是否引用了问题？

### 验收测试

输出是否包含以 PHP 为中心的结果列表，其中包含文件：行引用，涵盖所有相关语言/运行时维度，而无需执行安全性、体系结构或范围分析？

---

## 示例（示例）

### 示例 1：资源泄漏

- **输入**：使用“fopen()”打开文件的 PHP 函数，并且不会在所有代码路径中关闭该文件。
- **预期**：发出资源管理结果；建议 try-finally 或确保所有路径中的“fclose()”。类别 = 语言-php.

### 示例 2：缺少严格类型

- **输入**：没有 `declare(strict_types=1)` 且缺少参数/返回类型的新 PHP 文件。
- **预期**：发出类型安全的结果；建议在可行的情况下添加严格的类型和类型化参数。类别 = 语言-php.

### 边缘情况：混合 PHP 和 SQL

- **输入**：带有用于数据库查询的嵌入式 SQL 字符串的 PHP 文件。
- **预期**：仅查看 PHP 约定（资源处理、错误处理、类型）。不要在此处发出 SQL 注入结果；这是用于 review-security 或 review-sql。

---

## 附录：输出合约

每项调查结果必须遵循标准调查结果格式：

|元素|要求|
| :--- | :--- |
| **位置** | `path/to/file.ext`（可选行或范围）。 |
| **类别** | `语言-php`。 |
| **严重性** | `关键` \| `主要` \| `次要` \| `建议`。 |
| **标题** |简短的一行摘要。 |
| **描述** | 1-3 句话。 |
| **建议** |具体修复或改进（可选）。 |

示例：


```markdown
- **Location**: `src/Service/FileLoader.php:34`
- **Category**: language-php
- **Severity**: major
- **Title**: File handle not closed in exception path
- **Description**: The resource from fopen() may leak if an exception is thrown before fclose().
- **Suggestion**: Use try-finally to ensure fclose() is called, or use SplFileObject which manages the handle.
```