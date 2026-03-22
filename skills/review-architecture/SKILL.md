---
name: review-architecture
description: "Review code for architecture: module and layer boundaries, dependency direction, single responsibility, cyclic dependencies, interface stability, and coupling. Cognitive-only atomic skill; output is a findings list."
description_zh: 审查代码架构：模块与层次边界、依赖方向、单一职责、循环依赖、接口稳定性与耦合。
tags: [code-review]
version: 1.0.1
license: MIT
recommended_scope: project
metadata:
  author: ai-cortex
triggers: [review architecture, architecture review]
input_schema:
  type: code-scope
  description: Source files or directories to review
output_schema:
  type: findings-list
  description: Zero or more findings with location, category, severity, and suggestion
---

# 技能（Skill）：回顾架构

## 目的 (Purpose)

仅审查 **架构** 问题的代码。不要定义范围（差异与代码库）或执行语言/框架/安全分析；这些是单独的原子技能。以标准格式发出**结果列表**以进行聚合。重点关注模块和层边界、依赖方向、单一职责、循环依赖、接口稳定性以及耦合和扩展点。

---

## 核心目标（Core Objective）

**首要目标**：生成一个以架构为中心的发现列表，涵盖模块/层边界、依赖方向、单一责任、循环依赖、接口稳定性和给定代码范围的耦合。

**成功标准**（必须满足所有要求）：

1. ✅ **仅架构范围**：仅审核架构维度；未执行范围选择、语言/框架约定、安全性或性能分析
2. ✅ **涵盖所有六个架构维度**：在相关的情况下评估模块/层边界、依赖方向、单一责任、循环依赖、接口稳定性和耦合
3. ✅ **符合调查结果格式**：每个调查结果包括位置、类别（“cognitive架构”）、严重性、标题、描述和可选建议
4. ✅ **位置精确引用**：所有发现都引用特定的模块、包或文件（不是模糊的描述）
5. ✅ **可操作的输出**：每个发现都提供了具体的重构建议或改进方向

**验收**测试：输出是否包含架构发现列表，涵盖所有相关的结构维度以及特定的模块/文件引用和可操作的重构建议？

---

## 范围边界（范围边界）

**本技能负责**：

- 模块和层边界清晰（API、领域、数据层分离）
- 依赖方向分析（向内领域，稳定抽象）
- 每个模块/班级的单一责任评估
- 循环依赖检测和断点
- 接口稳定性和泄漏实现细节
- 耦合分析及扩展点设计

**本技能不负责**：

- 范围选择（决定要分析哪些文件/路径）——范围由调用者提供
- 语言/框架约定分析——使用“review-dotnet”、“review-java”、“review-go”等。
- 安全审查——使用“review-security”
- 绩效评估——使用“review-performance”
- 结合所有维度的当前状态代码库审查 - 使用“review-codebase”
- 全面精心策划的审核——使用“审核代码”

**转交点**：当所有架构发现发布后，移交给“审查代码”编排器进行聚合，或直接交付给用户以进行以架构为中心的会话。对于深度代码库审核，建议还运行“review-codebase”。

---

## 使用场景（用例）

- **精心安排的审查**：当[review-code](../review-code/SKILL.md)运行范围→语言→框架→库→cognitive时用作cognitive步骤。
- **以架构为中心的审查**：当用户只想检查边界、依赖关系和结构时。
- **重构或入门**：理解并批评当前的规划或文档结构。

**何时使用**：当任务包括架构或设计审查时。范围和代码范围由调用者或用户确定。

---

## 行为（行为）

### 该技能的范围

- **分析**：**给定代码范围**中的架构维度（调用者提供的文件或差异）。不决定范围；接受代码范围作为输入。对于大范围，考虑层或模块并进行总结。
- **不要**：执行范围选择、语言/框架约定或安全审查。仅关注架构和结构。

### 审查清单（仅限架构维度）

1. **模块和层边界**：模块/服务边界是否清晰？是否尊重各层（例如 API、域、数据）？高层模块是否避免依赖底层细节？
2. **依赖关系方向**：依赖关系是否指向预期的方向（例如向内指向域，或指向稳定的抽象）？模块级别没有反向或循环依赖方向。
3. **单一职责**：每个模块/类是否都有一个明确的职责？边界是否具有凝聚力？
4. **循环依赖**：模块、包或组件之间是否存在循环？建议断点（例如提取接口、移动共享代码）。
5. **接口稳定性**：公共API和接口是否稳定且最小？实施细节是否会跨界泄露？
6. **Coupling and extension points**: Is coupling to concrete types or frameworks minimized where extension is expected?扩展点（例如插件、策略）是否清晰？

### 语气和参考

- **专业和技术**：参考特定位置（文件、模块或包）。发出包含位置、类别、严重性、标题、描述、建议的结果。

---

## 输入与输出 (Input & Output)

### 输入（输入）

- **代码范围**：用户或范围技能已选择的文件或目录（或差异）。该技能不决定范围；它仅审查所提供的架构代码。

### 输出（输出）

- 以**附录：输出合同**中定义的格式发出零个或多个**结果**。
- 此技能的类别是**cognitive架构**。

---

## 限制（限制）

### 硬边界（Hard Boundaries）

- **不要**执行范围选择、语言、框架或安全审查。保持在架构维度内。
- **不要**在没有具体地点或可行建议的情况下给出结论。
- **不要**采用特定的架构风格（例如干净/六边形），除非项目声明它；根据一般边界和依赖原则进行评估。

### 技能边界 (Skill Boundaries)

**不要做这些**（其他技能可以处理它们）：

- 不要选择或定义代码范围 - 范围由调用者或“审查代码”确定
- 不要执行语言/框架约定分析 - 使用 `review-dotnet`、`review-java`、`review-go` 等。
- 不要执行安全或性能审查——使用“review-security”或“review-performance”
- 除非明确说明，否则不要假设特定的架构模式（干净、六边形等）

**何时停止并交接**：

- When all architecture findings are emitted, hand off to `review-code` for aggregation in an orchestrated review
- 当用户需要全面审查（范围+语言+cognitive）时，重定向到“审查代码”
- 当需要架构之外的全面代码库状态审查时，重定向到“审查代码库”

---

## 自检（Self-Check）

### 核心成功标准

- [ ] **仅限架构范围**：仅审查架构维度；未执行范围选择、语言/框架约定、安全性或性能分析
- [ ] **涵盖所有六个架构维度**：在相关的情况下评估模块/层边界、依赖方向、单一责任、循环依赖、接口稳定性和耦合
- [ ] **符合调查结果格式**：每个调查结果包括位置、类别（“cognitive架构”）、严重性、标题、描述和可选建议
- [ ] **位置精确引用**：所有发现都引用特定的模块、包或文件（不是模糊的描述）
- [ ] **可操作的输出**：每个发现都提供了具体的重构建议或改进方向

### 流程质量检查

- [ ] 是否仅审查了架构维度（没有范围/语言/安全性）？
- [ ] 是否涵盖了相关的边界、依赖方向、责任、周期、接口和耦合？
- [ ] 每个发现是否都包含位置、类别=cognitive架构、严重性、标题、描述和可选建议？
- [ ] 模块/包/文件引用是否足够精确以进行操作？

### 验收测试

输出是否包含一个架构发现列表，涵盖所有相关的结构维度以及特定的模块/文件引用和可操作的重构建议？

---

## 示例（示例）

### 示例 1：反向依赖

- **输入**：域层直接从基础设施（例如数据库驱动程序）导入。
- **预期**：发出依赖方向的发现；建议领域中的接口和基础设施中的实现。类别=cognitive架构。

### 示例 2：在包之间循环

- **输入**：包A导入B，B导入C，C导入A。
- **预期**：发出识别循环的结果并建议断点（例如，将共享接口或类型提取到中性包）。类别=cognitive架构。

### 边缘情况：小或单文件范围

- **输入**：单个文件或非常小的模块。
- **预期**：审查内部结构（职责、与外部类型的耦合）；如果范围对于模块级问题来说太小，请说明并仅发出适用的结果（例如单一责任、接口清晰度）。

---

## 附录：输出合约

每项调查结果必须遵循标准调查结果格式：

|元素|要求 |
| :--- | :--- |
| **位置** | `path/to/file.ext` 或模块/包名称（可选行或范围）。 |
| **类别** | “cognitive架构”。 |
| **严重性** | `关键` \| `主要` \| `次要` \| `建议`。 |
| **标题** |简短的一行摘要。 |
| **描述** | 1-3 句话。 |
| **建议** |具体修复或改进（可选）。 |

示例：


```markdown
- **Location**: `pkg/domain/order.go`
- **Category**: cognitive-architecture
- **Severity**: major
- **Title**: Domain imports infrastructure directly
- **Description**: Order service imports DB driver; domain should not depend on infrastructure.
- **Suggestion**: Define repository interface in domain; implement in infrastructure and inject.
```