---
name: review-sql
description: Review SQL and query code for injection risk, parameterization, indexing and performance, transactions, NULL and constraints, and dialect portability. Language-only atomic skill; output is a findings list.
description_zh: 审查 SQL 与查询代码：注入风险、参数化、索引与性能、事务、NULL 与约束、方言可移植性。
tags: [code-review]
version: 1.0.1
license: MIT
recommended_scope: project
metadata:
  author: ai-cortex
triggers: [review sql]
input_schema:
  type: code-scope
  description: Source files or directories to review
output_schema:
  type: findings-list
  description: Zero or more findings with location, category, severity, and suggestion
---

# 技能（Skill）：审查 SQL

## 目的 (Purpose)

仅查看 **SQL** 和查询相关代码的 **语言和查询约定**。涵盖注入和参数化、索引和执行计划问题、事务和隔离、NULL 和唯一约束、方言可移植性、大表和分页模式以及敏感列和权限。以标准格式发出**结果列表**以进行聚合。不定义范围或执行全面的安全/架构审查；注入在这里是一个特定于 SQL 的问题，但更广泛的安全性是针对 [review-security](../review-security/SKILL.md)。

---

## 核心目标（Core Objective）

**首要目标**：生成以 SQL 为中心的 findings 列表，涵盖注入/参数化、索引、事务、NULL/约束、方言可移植性、分页模式及敏感列访问，针对给定代码范围。

**成功标准**（必须满足所有要求）：

1. ✅ **仅限 SQL 范围**：仅审查 SQL 和查询约定；未执行范围选择、完全安全性或架构分析
2. ✅ **涵盖所有七个 SQL 维度**：注入/参数化、索引/执行计划、事务/隔离、NULL/唯一约束、方言/可移植性、大表/分页模式以及相关的敏感列/权限
3. ✅ **结果格式兼容**：每个结果包括位置、类别（`language-sql`）、严重性、标题、描述和可选建议
4. ✅ **已标记关键注入问题**：SQL 注入模式（字符串连接、用户输入插值）被标记为“严重”严重性
5. ✅ **位置精确引用**：所有结果都引用特定文件：行或查询标识符位置

**验收**测试：输出是否包含涵盖所有相关查询维度的 SQL 结果列表，其中注入风险标记为“关键”以及每个结果的具体位置引用？

---

## 范围边界（范围边界）

**本技能负责**：

- 通过字符串连接或插值进行 SQL 注入 — 参数化查询和准备好的语句
- WHERE/JOIN/ORDER BY 列的索引间隙
- 事务边界、隔离级别、死锁风险、长时间运行的事务
- 比较/聚合中的 NULL 处理、唯一约束、NOT NULL 正确性
- 数据库方言可移植性（LIMIT/OFFSET/FETCH、日期函数、供应商特定语法）
- 大表全扫描、分页策略（keyset vs OFFSET）
- SELECT 中的敏感列暴露、最低权限角色使用

**本技能不负责**：

- 范围选择——范围由调用者提供
- 更广泛的安全分析（超越 SQL 注入）——使用“review-security”
- 架构分析——使用“review-architecture”
- 全面精心策划的审核——使用“审核代码”

**转交点**：当所有 SQL 结果发出后，将其交给 `review-code` 进行聚合。对于更广泛的安全问题（身份验证、加密、配置），请重定向到“审查安全”。

---

## 使用场景（用例）

- **精心安排的审阅**：当 [review-code](../review-code/SKILL.md) 为包含 SQL（.sql 文件、嵌入式 SQL 或 ORM 生成的 SQL）的项目运行时用作语言步骤。
- **仅 SQL 审查**：当用户只想检查查询的正确性、性能和安全性时。
- **迁移或可移植性**：检查特定方言的构造和跨数据库的可移植性。

**何时使用**：当正在审查的代码包含 SQL（原始 .sql、嵌入代码或 ORM 生成）时。范围（差异与路径）由调用者或用户确定。

---

## 行为（行为）

### 该技能的范围

- **分析**：**给定范围**（文件、片段或差异）中的 SQL 和查询逻辑。接受 .sql 文件、应用程序代码中的嵌入式 SQL 或 ORM 生成的 SQL（如果可见）。
- **不要**：决定范围（差异与代码库）；不执行完整的应用程序安全或架构审查。关注 SQL/查询维度。

### 查看清单（仅限 SQL 维度）

1. **注入和参数化**：SQL中用户输入无需字符串串联或插值；使用参数化查询或准备好的语句；避免来自不可信输入的动态 SQL。
2. **索引和执行计划**：对未索引列进行过滤或联接的查询；在大表上选择*；缺少 WHERE/JOIN/ORDER BY 的索引。
3. **事务和隔离**：适当的事务边界；隔离级别和锁定；避免长时间运行的事务；僵局风险。
4. **NULL和唯一约束**：比较和聚合中NULL的处理；独特的约束和重复的处理；在适当的情况下 NOT NULL。
5. **方言和可移植性**：特定于数据库的语法（例如 LIMIT 与 OFFSET/FETCH、日期函数）和可移植性（如果需要多数据库支持）。
6. **大表和分页**：对大表进行全量扫描；分页（键集与 OFFSET）和可扩展性。
7. **敏感列和权限**：SELECT中的敏感数据； SQL 中的最低权限和角色使用（如果可见）。

### 语气和参考

- **专业和技术**：参考特定位置（文件：行或查询标识符）。发出包含位置、类别、严重性、标题、描述、建议的结果。

---

## 输入与输出 (Input & Output)

### 输入（输入）

- **代码范围**：包含 SQL 的文件或片段（例如 .sql 文件、带有嵌入式 SQL 的代码或 ORM 生成的 SQL（如果可用））。由用户或范围技能提供。

### 输出（输出）

- 以**附录：输出合同**中定义的格式发出零个或多个**结果**。
- 此技能的类别是**语言-sql**。

---

## 限制（限制）

### 硬边界（Hard Boundaries）

- **不要**执行范围选择或全面的安全/架构审查。遵守 SQL 和查询约定。
- **不要**在没有具体地点或可行建议的情况下给出结论。
- **不要**假设特定的数据库供应商，除非另有说明；相关时请注意方言。

### 技能边界 (Skill Boundaries)

**不要做这些**（其他技能可以处理它们）：

- 不要选择或定义代码范围 - 范围由调用者或“审查代码”确定
- 不要执行 SQL 注入之外的广泛安全分析 - 使用“review-security”
- 不要执行架构分析——使用“review-architecture”
- 不要审查非 SQL 代码的 SQL 约定（应用程序代码中的 SQL 注入应由“审查安全”标记）

**何时停止并交接**：

- 当所有 SQL 结果发出后，将其交给“review-code”进行聚合
- 当用户需要更广泛的安全分析（身份验证、加密、配置）时，重定向到“审查安全”
- 当用户需要全面审查（范围+语言+cognitive）时，重定向到“审查代码”

---

## 自检（Self-Check）

### 核心成功标准

- [ ] **仅 SQL 范围**：仅审查 SQL 和查询约定；未执行范围选择、完全安全性或架构分析
- [ ] **涵盖所有七个 SQL 维度**：注入/参数化、索引/执行计划、事务/隔离、NULL/唯一约束、方言/可移植性、大表/分页模式以及相关的敏感列/权限
- [ ] **结果格式兼容**：每个结果包括位置、类别（`语言-sql`）、严重性、标题、描述和可选建议
- [ ] **已标记关键注入问题**：SQL 注入模式（字符串连接、用户输入插值）被标记为“严重”严重性
- [ ] **位置精确引用**：所有结果都引用特定文件：行或查询标识符位置

### 流程质量检查

- [ ] 是否仅审查了 SQL/查询维度（没有超出查询设计的范围/架构）？
- [ ] 是否涵盖相关的参数化、索引、事务、NULL/约束和可移植性？
- [ ] 每个发现是否都包含位置、类别=语言-sql、严重性、标题、描述和可选建议？
- [ ] 问题是否通过 file:line 或查询标识符引用？

### 验收测试

输出是否包含涵盖所有相关查询维度的 SQL 结果列表，其中注入风险标记为“关键”以及每个结果的具体位置引用？

---

## 示例（示例）

### 示例 1：查询中的字符串连接

- **输入**：使用字符串连接（包括用户输入）构建的查询。
- **预期**：发出 SQL 注入的关键发现；建议参数化查询或准备好的语句。类别=语言-sql。

### 示例 2：没有分页的大表

- **输入**：SELECT * FROM large_table ORDER BY id，没有 LIMIT 或分页。
- **预期**：发出性能和可扩展性的结果；建议分页（例如键集或 OFFSET/FETCH），并在不需要时避免使用 SELECT *。类别=语言-sql。

### 边缘情况：ORM 生成的 SQL

- **输入**：仅使用 ORM 的应用程序代码；生成的 SQL 不可见。
- **预期**：检查代码中的任何原始 SQL 或查询构建器；如果没有可见的 SQL，请说明并跳过或报告“范围内没有要审查的 SQL”。不要发明 SQL。

---

## 附录：输出合约

每项调查结果必须遵循标准调查结果格式：

|元素|要求 |
| :--- | :--- |
| **位置** | `path/to/file.ext`（可选行或范围）或查询标识符。 |
| **类别** | `语言-sql`。 |
| **严重性** | `关键` \| `主要` \| `次要` \| `建议`。 |
| **标题** |简短的一行摘要。 |
| **描述** | 1-3 句话。 |
| **建议** |具体修复或改进（可选）。 |

示例：


```markdown
- **Location**: `scripts/orders.sql:12`
- **Category**: language-sql
- **Severity**: critical
- **Title**: Query built with string concatenation; injection risk
- **Description**: User-controlled input is concatenated into the WHERE clause.
- **Suggestion**: Use parameterized query or prepared statement with placeholders.
```