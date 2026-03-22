---
name: review-typescript
description: Review TypeScript/JavaScript code for type safety, async patterns, error handling, and module design. Atomic skill; output is a findings list.
description_zh: 审查 TypeScript/JavaScript 代码：类型安全、异步模式、错误处理与模块设计；原子技能。
tags: [code-review]
version: 1.0.0
license: MIT
recommended_scope: project
metadata:
  author: ai-cortex
triggers: [review typescript, review ts]
input_schema:
  type: code-scope
  description: Source files or directories to review
output_schema:
  type: findings-list
  description: Zero or more findings with location, category, severity, and suggestion
---

# 技能（Skill）：复习TypeScript

## 目的 (Purpose)

仅查看 **TypeScript 和 JavaScript** 代码的 **语言和运行时约定**。不要定义范围（差异与代码库）或执行安全/架构分析；这些是通过范围和cognitive技能来处理的。以标准格式发出**结果列表**以进行聚合。重点关注类型安全和类型系统使用、异步模式和 Promise 处理、错误处理、模块设计、运行时正确性、API 和接口设计以及性能和内存注意事项。

---

## 核心目标（Core Objective）

**首要目标**：生成 TypeScript/JavaScript 语言调查结果列表，涵盖给定代码范围的类型安全、异步模式、错误处理、模块设计、运行时正确性、API/界面设计和性能/内存。

**成功标准**（必须满足所有要求）：

1. ✅ **仅限 TypeScript/JavaScript 语言范围**：仅审查 TypeScript 和 JavaScript 语言以及运行时约定；未执行范围选择、安全性或架构分析
2. ✅ **涵盖所有七种语言维度**：类型安全、异步模式、错误处理、模块设计、运行时正确性、API/接口设计和性能/内存（如果相关）进行评估
3. ✅ **结果格式兼容**：每个结果包括位置、类别（`语言打字稿`）、严重性、标题、描述和可选建议
4. ✅ **文件/行引用**：所有发现都引用特定文件：行或符号名称
5. ✅ **排除非 TS/JS 代码**：除非明确在范围内，否则不会分析非 TypeScript/JavaScript 文件的 TS/JS 特定规则

**验收**测试：输出是否包含以 TypeScript/JavaScript 为中心的结果列表，其中包含涵盖所有相关语言维度的文件/行引用，而无需执行安全性、架构或范围分析？

---

## 范围边界（范围边界）

**本技能负责**：

- 类型安全和类型系统使用（严格模式、正确类型、“任何”避免、受歧视联合、类型保护、泛型）
- 异步模式（异步/等待、承诺处理、错误传播、竞争条件、未处理的拒绝）
- 错误处理（try/catch 模式、自定义错误类型、错误边界、详尽的错误处理）
- 模块设计（ESM vs CJS、桶式导出、循环依赖、tree-shaking、副作用）
- 运行时正确性（空/未定义处理、相等性检查、强制陷阱、原型污染）
- API和接口设计（函数签名、重载、品牌类型、只读正确性）
- 性能和内存（闭包泄漏、事件侦听器清理、WeakRef/WeakMap 使用、包大小影响）

**本技能不负责**：

- 范围选择——范围由调用者提供
- 安全分析（注入、秘密、XSS）——使用“review-security”
- 架构分析——使用“review-architecture”
- 框架约定（Vue、React、Angular）——使用特定于框架的技能（例如“review-vue”）
- 全面精心策划的审核——使用“审核代码”

**转交点**：当所有 TypeScript/JavaScript 结果发出后，将其移交给“review-code”进行聚合。对于代码中的注入风险或秘密，请记下它们并建议“审查安全性”。

---

## 使用场景（用例）

- **精心安排的审查**：当 [review-code](../review-code/SKILL.md) 运行 TypeScript/JavaScript 项目的范围 → 语言 → 框架 → 库 → cognitive时，用作语言步骤。
- **仅 TypeScript 审查**：当用户只想检查 TypeScript/JavaScript 语言约定时。
- **PR 前语言检查表**：在合并之前确保类型安全、异步正确性和模块设计健全。

**何时使用**：当审查的代码是 TypeScript 或 JavaScript 并且任务包括语言质量时。范围由调用者或用户确定。

---

## 行为（行为）

### 该技能的范围

- **分析**：**给定代码范围**（调用者提供的文件或差异）中的 TypeScript 和 JavaScript 语言和运行时约定。不决定范围；接受代码范围作为输入。
- **不要**：执行范围选择、安全审查或架构审查；除非在范围内，否则不要检查非 TS/JS 文件的 TS/JS 规则。

### 审核清单（仅限 TypeScript/JavaScript 语言）

1. **类型安全和类型系统使用**：强制执行“严格”模式；与“any”相比，更喜欢显式类型；使用受歧视的联合进行状态建模；应用类型保护和缩小；利用泛型进行重用，而不牺牲类型信息；在可能缩小范围的情况下避免类型断言（`as`）。
2. **异步模式**：确保正确的 async/await 使用和 Promise 链；验证通过异步边界的错误传播；检测竞争条件和未处理的 Promise 拒绝；检查悬空的 Promise（缺少 `await`）；验证并发模式（“Promise.all”、“Promise.allSettled”）。
3. **错误处理**：验证try/catch的位置和特异性；与原始字符串/错误相比，更喜欢自定义错误类型；确保详尽的错误处理（switch/if-else 涵盖所有情况）；检查错误是否带有足够的上下文；验证finally 块中的清理。
4. **模块设计**：更喜欢ESM（`import`/`export`）而不是CJS（`require`/`module.exports`）；审计桶出口的影响；检测循环依赖；检查模块范围内的意外副作用；验证一致的模块分辨率。
5. **运行时正确性**：检查空/未定义处理（可选链接、空合并）；强制严格相等（`===`/`!==`）；检测强制陷阱（隐式类型转换）；检查原型污染风险；验证迭代器/生成器的正确性。
6. **API和界面设计**：检查函数签名的清晰度和一致性；验证重载的顺序正确且不含糊；检查品牌/不透明类型以确保域安全；在意外突变的情况下强制执行“只读”；验证索引签名和映射类型。
7. **性能和内存**：检测基于闭包的内存泄漏；验证事件监听器和订阅清理；检查 WeakRef/WeakMap 的缓存模式使用情况；评估进口捆绑规模的影响；识别热路径效率低下的情况（例如循环中不必要的分配）。

### 语气和参考

- **专业和技术**：参考具体位置（文件：行或符号名称）。发出包含位置、类别、严重性、标题、描述、建议的结果。

---

## 输入与输出 (Input & Output)

### 输入（输入）

- **代码范围**：包含 TypeScript 或 JavaScript 代码（.ts、.tsx、.js、.jsx、.mts、.mjs、.cts、.cjs）的文件或目录（或 diff）。由用户或范围技能提供。

### 输出（输出）

- 以**附录：输出合同**中定义的格式发出零个或多个**结果**。
- 此技能的类别是**语言打字稿**。

---

## 限制（限制）

### 硬边界（Hard Boundaries）

- **不要**执行范围选择、安全性或架构审查。遵守 TypeScript/JavaScript 语言和运行时约定。
- **不要**在没有具体地点或可行建议的情况下给出结论。
- **不要**审查非 TS/JS 代码的 TS/JS 特定规则，除非明确在范围内。

### 技能边界 (Skill Boundaries)

**不要做这些**（其他技能可以处理它们）：

- 不要选择或定义代码范围 - 范围由调用者或“审查代码”确定
- 不要执行安全分析（注入、秘密）——使用“review-security”
- 不要执行架构分析——使用“review-architecture”
- 不要查看特定于框架的约定（Vue、React、Angular）——使用相应的框架技能

**何时停止并交接**：

- 当所有 TypeScript/JavaScript 结果发出后，将其移交给“review-code”进行聚合
- 当发现注入风险或秘密时，记下它们并建议“审查安全性”
- 当用户需要全面审查（范围+语言+cognitive）时，重定向到“审查代码”

---

## 自检（Self-Check）

### 核心成功标准

- [ ] **仅限 TypeScript/JavaScript 语言范围**：仅审查 TypeScript 和 JavaScript 语言以及运行时约定；未执行范围选择、安全性或架构分析
- [ ] **涵盖所有七种语言维度**：类型安全、异步模式、错误处理、模块设计、运行时正确性、API/界面设计和性能/内存（如果相关）进行评估
- [ ] **符合调查结果格式**：每个调查结果包括位置、类别（`语言打字稿`）、严重性、标题、描述和可选建议
- [ ] **文件/行引用**：所有结果引用特定文件：行或符号名称
- [ ] **排除非 TS/JS 代码**：除非明确在范围内，否则不会分析非 TypeScript/JavaScript 文件的 TS/JS 特定规则

### 流程质量检查

- [ ] 是否仅审查了 TypeScript/JavaScript 语言维度（无范围/安全/架构）？
- [ ] 是否涵盖了相关的类型安全、异步模式、错误处理、模块设计、运行时正确性、API 设计和性能？
- [ ] 每个发现是否都包含位置、类别=语言打字稿、严重性、标题、描述和可选建议？
- [ ] 问题是否通过文件：行或符号名称引用？

### 验收测试

输出是否包含以 TypeScript/JavaScript 为中心的结果列表，其中包含涵盖所有相关语言维度的文件/行引用，而无需执行安全性、架构或范围分析？

---

## 示例（示例）

### 示例 1：不安全地使用 `any`

- **输入**：函数参数类型为“any”且没有运行时验证的模块。
- **预期**：针对不安全的“any”使用发出一个发现（主要）；建议用适当的类型、泛型或类型缩小的“未知”来替换。类别 = 语言打字稿。

### 示例 2：异步调用时缺少 `await`

- **输入**：异步函数调用另一个异步函数而不使用“await”，丢弃 Promise。
- **预期**：针对悬空 Promise 发出一个发现（关键/主要）；建议添加 `await` 或显式处理返回的 Promise。类别 = 语言打字稿。

### 边缘情况：在同一项目中混合使用 ESM 和 CJS

- **输入**：使用“import”/“export”使用某些文件进行项目，使用“require”/“module.exports”使用其他文件。
- **预期**：发出模块系统使用不一致的结果；建议迁移到单模块系统（最好是 ESM）或记录混合使用的原因。类别 = 语言打字稿。

---

## 附录：输出合约

每项调查结果必须遵循标准调查结果格式：

|元素|要求|
| :--- | :--- |
| **位置** | `path/to/file.ts` 或 `.js` （可选行或范围）。 |
| **类别** | `语言打字稿`。 |
| **严重性** | `关键` \| `主要` \| `次要` \| `建议`。 |
| **标题** |简短的一行摘要。 |
| **描述** | 1-3 句话。 |
| **建议** |具体修复或改进（可选）。 |

示例：


```markdown
- **Location**: `src/services/userService.ts:42`
- **Category**: language-typescript
- **Severity**: major
- **Title**: Unsafe `any` type in function parameter
- **Description**: Parameter `data` is typed as `any`, bypassing all type checking and allowing silent runtime errors.
- **Suggestion**: Replace `any` with `unknown` and add type narrowing, or define a specific interface for the expected shape.
```