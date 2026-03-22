---
name: review-orm-usage
description: Review ORM usage patterns for N+1 queries, connection management, migration safety, transaction handling, and query efficiency. Library-level atomic skill; output is a findings list.
description_zh: 审查 ORM 使用：N+1 查询、连接管理、迁移安全、事务与查询效率；库级原子技能。
tags: [code-review, optimization]
version: 1.0.0
license: MIT
recommended_scope: project
metadata:
  author: ai-cortex
triggers: [review orm, orm review]
input_schema:
  type: code-scope
  description: Source files or directories to review
output_schema:
  type: findings-list
  description: Zero or more findings with location, category, severity, and suggestion
---

# 技能（Skill）：回顾ORM用法

## 目的 (Purpose)

仅在**库级别**查看**ORM 使用模式**。不要定义范围（差异与代码库）或执行安全/架构分析；这些是通过范围和cognitive技能来处理的。以标准格式发出**结果列表**以进行聚合。专注于跨 ORM 库（Prisma、Entity Framework、SQLAlchemy、Sequelize、TypeORM、Hibernate、Django ORM、ActiveRecord 等）的 N+1 查询检测、连接管理、迁移安全、事务处理、查询效率和模型设计。

---

## 核心目标（Core Objective）

**首要目标**：生成一个 ORM 使用结果列表，涵盖给定代码范围的 N+1 查询、连接管理、迁移安全、事务处理、查询效率和模型设计。

**成功标准**（必须满足所有要求）：

1. ✅ **ORM库专用范围**：仅审查ORM使用模式；未执行范围选择、安全性或架构分析
2. ✅ **涵盖所有六个 ORM 维度**：N+1、连接、迁移、事务、查询效率和模型设计（如果相关）进行评估
3. ✅ **结果格式兼容**：每个结果包括位置、类别（`library-orm`）、严重性、标题、描述和可选建议
4. ✅ **文件/模型引用**：所有发现都引用特定文件：行或模型/实体名称
5. ✅ **ORM 不可知**：研究结果适用于整个 ORM 库；特定库仅在上下文中引用

**验收**测试：输出是否包含以 ORM 为中心的结果列表，其中包含涵盖所有相关库维度的文件/模型引用，而无需执行安全性、架构或范围分析？

---

## 范围边界（范围边界）

**本技能负责**：

- N+1 查询检测（急切加载与延迟加载、包含/连接模式、批量加载、数据加载模式）
- 连接管理（池配置、连接泄漏、超时处理、连接重用）
- 迁移安全（向后兼容的迁移、零停机部署、数据与模式迁移、回滚策略）
- 事务处理（事务范围、隔离级别、嵌套事务、死锁预防）
- 查询效率（不必要的 SELECT *、查询模式暗示的缺失索引、原始查询回退、查询复杂性）
- 模型设计（适当的关系、级联行为、软删除模式、审计列、索引声明）

**本技能不负责**：

- 范围选择——范围由调用者提供
- 安全分析（SQL注入、敏感数据暴露）——使用“review-security”
- 架构分析（模块边界、耦合）——使用“review-architecture”
- 原始 SQL 质量（语法、可移植性、参数化）——使用 `review-sql`
- 一般性能分析（算法复杂度、I/O 成本）——使用 `review-performance`
- 全面精心策划的审核——使用“审核代码”

**转交点**：当所有 ORM 结果发出后，将其交给“review-code”进行聚合。对于 SQL 注入风险（未经净化的原始查询），请记下它们并建议“审查安全性”。对于复杂的原始 SQL 质量，请注意并建议“review-sql”。

---

## 使用场景（用例）

- **精心安排的审查**：当 [review-code](../review-code/SKILL.md) 为使用 ORM 的项目运行范围 → 语言 → 框架 → 库 → cognitive时，用作库步骤。
- **仅 ORM 审查**：当用户只想在其数据层检查 ORM 使用模式时。
- **PR ORM 前检查表**：在合并之前确保 N+1 查询、事务处理和迁移安全正确。
- **迁移审查**：重点检查迁移文件的向后兼容性和回滚安全性。

**何时使用**：当正在审查的代码使用 ORM 库并且任务包括库级质量时。范围由调用者或用户确定。

---

## 行为（行为）

### 该技能的范围

- **分析**：**给定代码范围**（调用者提供的文件或 diff）中的 ORM 使用模式。不决定范围；接受代码范围作为输入。
- **不要**：执行范围选择、安全审查或架构审查；除非在范围内，否则不要检查非 ORM 文件中的 ORM 规则。

### 审查清单（仅限 ORM 库）

1. **N+1查询检测**：识别触发N+1查询的延迟加载模式；检查急切加载（包含/连接）、批量加载或数据加载模式；标记每次迭代发出单独查询的循环。
2. **连接管理**：验证池配置（最小/最大、空闲超时）；检测潜在的连接泄漏（未返回的连接、丢失处置/关闭）；检查超时和重试设置；确认请求范围上下文中的连接重用。
3. **迁移安全**：评估向后兼容性（仅添加性更改与破坏性更改）；检查零停机部署准备情况（大型表上没有表锁，没有默认值则没有 NOT NULL）；验证数据迁移与模式迁移分开；确认回滚策略存在。
4. **交易处理**：评估交易范围（太宽或太窄）；检查隔离级别的正确性；检测嵌套事务滥用（保存点与平面）；标记潜在的死锁模式（不一致的锁顺序、长期持有的锁）。
5. **查询效率**：标记不必要的`SELECT *`或过度获取的列；识别暗示缺少索引的查询模式（未索引的 WHERE/ORDER BY 列）；评估原始查询回退的适当性；评估查询复杂性（深度连接、循环中的子查询）。
6. **模型设计**：验证正确的关系声明（一对多、多对多、多态）；检查级联行为（意外级联删除）；审查软删除的实施；确认预期的审核列（createdAt、updatedAt）；检查频繁查询字段的索引声明。

### 语气和参考

- **专业和技术**：参考具体位置（文件：行或型号/实体名称）。发出包含位置、类别、严重性、标题、描述、建议的结果。

---

## 输入与输出 (Input & Output)

### 输入（输入）

- **代码范围**：包含 ORM 代码（模型、迁移、存储库、查询）的文件或目录（或 diff）。由用户或范围技能提供。

### 输出（输出）

- 以**附录：输出合同**中定义的格式发出零个或多个**结果**。
- 此技能的类别是 **library-orm**。

---

## 限制（限制）

### 硬边界（Hard Boundaries）

- **不要**执行范围选择、安全性或架构审查。保持 ORM 库的使用模式。
- **不要**在没有具体地点或可行建议的情况下给出结论。
- **不要**审查非 ORM 代码的 ORM 特定规则，除非明确在范围内。
- **不要**重复属于“review-sql”的原始 SQL 分析；仅标记 ORM 生成的查询问题。

### 技能边界 (Skill Boundaries)

**不要做这些**（其他技能可以处理它们）：

- 不要选择或定义代码范围 - 范围由调用者或“审查代码”确定
- 不执行安全分析（SQL 注入、数据暴露）——使用“review-security”
- 不要执行架构分析（模块边界、耦合）——使用“review-architecture”
- 不要执行原始 SQL 语法或可移植性审查 - 使用 `review-sql`
- 不要执行一般算法性能分析 - 使用“review-performance”

**何时停止并交接**：

- 当所有 ORM 结果发出后，将其交给“review-code”进行聚合
- 当发现 SQL 注入风险时（例如原始查询中未经消毒的插值），请记下它们并建议“审查安全性”
- 当发现原始 SQL 质量问题（语法、可移植性）时，记下它们并建议“review-sql”
- 当用户需要全面审查（范围+语言+cognitive）时，重定向到“审查代码”

---

## 自检（Self-Check）

### 核心成功标准

- [ ] **仅 ORM 库范围**：仅审查 ORM 使用模式；未执行范围选择、安全性或架构分析
- [ ] **涵盖所有六个 ORM 维度**：N+1、连接、迁移、事务、查询效率和模型设计（如果相关）进行评估
- [ ] **结果格式兼容**：每个结果包括位置、类别（`library-orm`）、严重性、标题、描述和可选建议
- [ ] **文件/模型引用**：所有结果引用特定文件：行或模型/实体名称
- [ ] **ORM 无关**：研究结果适用于整个 ORM 库；特定库仅在上下文中引用

### 流程质量检查

- [ ] 是否仅审查了 ORM 库维度（无范围/安全/架构）？
- [ ] 是否涵盖了相关的 N+1、连接、迁移、事务、查询效率和模型设计？
- [ ] 发布的每个发现是否包含位置、类别=library-orm、严重性、标题、描述和可选建议？
- [ ] 问题是否通过文件：行或模型/实体名称引用？

### 验收测试

输出是否包含以 ORM 为中心的结果列表，其中包含涵盖所有相关库维度的文件/模型引用，而无需执行安全性、体系结构或范围分析？

---

## 示例（示例）

### 示例 1：循环中的 N+1 次查询

- **输入**：获取订单列表的控制器或服务，然后迭代访问“order.customer”，而无需急切加载。
- **预期**：发出 N+1 查询模式的结果（主要）；建议通过 include/join 进行急切加载（例如 Prisma `include`、EF `Include`、SQLAlchemy `joinedload`、Hibernate `@EntityGraph`）。类别=库-orm。

### 示例 2：不回滚的破坏性迁移

- **输入**：删除列或重命名表的迁移，无需相应的向下/回滚迁移，也无需数据保存步骤。
- **预期**：在没有回滚策略的情况下发出破坏性迁移的发现（关键）；建议附加迁移模式（添加新列→回填→切换读取→删除旧列）。类别=库-orm。

### 边缘情况：ORM 上下文中的原始查询回退

- **输入**：使用原始 SQL（`prisma.$queryRaw`、`DbContext.Database.ExecuteSqlRaw`、`session.execute(text(...))`）进行查询的存储库方法，可以使用 ORM 查询构建器来表达。
- **预期**：发出一个发现（建议），指出原始查询绕过 ORM 类型安全和迁移跟踪；如果查询是可表达的，建议使用 ORM 查询构建器。如果原始查询是合理的（性能、不支持的功能），请接受它，但标记缺少参数化（如果存在），并建议针对注入风险进行“审查安全”。类别=库-orm。

---

## 附录：输出合约

每项调查结果必须遵循标准调查结果格式：

|元素|要求|
| :--- | :--- |
| **位置** | `path/to/file.ext` 或模型/实体名称（可选行或范围）。 |
| **类别** | `图书馆-orm`。 |
| **严重性** | `关键` \| `主要` \| `次要` \| `建议`。 |
| **标题** |简短的一行摘要。 |
| **描述** | 1-3 句话。 |
| **建议** |具体修复或改进（可选）。 |

示例：


```markdown
- **Location**: `src/services/OrderService.ts:42`
- **Category**: library-orm
- **Severity**: major
- **Title**: N+1 query on Order.customer relation
- **Description**: Each order triggers a separate query to fetch the customer. With 100 orders this produces 101 queries instead of 2.
- **Suggestion**: Use eager loading (e.g. Prisma `include: { customer: true }`, EF `.Include(o => o.Customer)`) or batch the customer lookup.
```