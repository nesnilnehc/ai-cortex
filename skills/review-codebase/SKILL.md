---
name: review-codebase
description: "Review given file/dir/repo for current-state code organization: module boundaries, design patterns, cross-module dependencies, tech debt, and interface stability. Scope-only atomic skill; output is a findings list."
description_zh: 对给定路径（文件 / 目录 / 仓库）做 scope-only 原子审查，覆盖模块边界、模式一致性、跨模块依赖、技术债与接口稳定性。
tags: [code-review, scope-only]
license: MIT
recommended_scope: project
metadata:
  author: ai-cortex
triggers: [review codebase, codebase review]
input_schema:
  type: code-scope
  description: Files, directories, or repository path to review for current-state structure
output_schema:
  type: findings-list
  description: Findings on module boundaries, patterns, dependencies, tech debt, and interface stability
---

# 技能（Skill）：审查代码库（Review Codebase）

## 目的 (Purpose)

对**给定路径**（单文件 / 目录 / 仓库）的**当前状态**做 scope-only 原子审查。与 `review-diff`（仅审查 git 变更）成对作为 orchestrate-code-review 的 scope 步候选——本技能看快照，review-diff 看变更。

**不做**：安全 / 性能 / 架构等 cognitive 维度（由 cognitive 步的原子技能 `review-security` / `review-performance` / `review-architecture` 承接），也不做语言或框架特定分析（由 language / framework 步承接）。

---

## 核心目标（Core Objective）

**首要目标**：产出 scope-only findings list，识别给定路径的结构性问题（边界、模式、依赖、技术债、接口）。

**成功标准**（必须全部满足）：

1. ✅ **范围已确认**：分析前确认用户的路径或目录
2. ✅ **5 维已覆盖**：模块边界、模式一致性、跨模块依赖、技术债、接口稳定性均输出 findings
3. ✅ **位置精确**：每个 finding 含 `file:line` 引用
4. ✅ **格式合规**：findings 含 location / category（`scope`）/ severity / title / description / suggestion
5. ✅ **大范围处理**：对仓库级范围按层（模块 / 目录）输出，或与用户确认优先子集
6. ✅ **不越界**：不输出安全 / 性能 / 架构 / 语言 / 框架 cognitive findings（标记并提示对应原子技能）

---

## 范围边界（Scope Boundaries）

**本技能负责**：

- 给定路径当前状态的结构性审查
- 5 维 findings：模块边界、模式一致性、跨模块依赖与耦合、技术债与可维护性、接口稳定性

**本技能不负责**：

- 仅 git 变更审查（用 `review-diff`）
- 全维度编排审查（用 `orchestrate-code-review`）
- 语言 / 框架特定约定（用 `review-<lang>` / `review-<framework>`）
- 安全 / 性能 / 架构 cognitive 维度（用 `review-security` / `review-performance` / `review-architecture`）

**交接点**：findings 输出后，作为 orchestrate-code-review 的 scope 步聚合输入；或交给用户决定后续（重构 / 进一步深审）。

---

## 使用场景

- **新模块审查**：给定 `src/auth/` 看当前结构与依赖
- **遗留路径审计**：给定路径看技术债与边界问题
- **采样审查**：同事指定的文件或目录，无需 diff
- **作为 orchestrate-code-review 的 scope 步**：与 `review-diff` 二选一

---

## 行为 (Behavior)

### 范围解析

- **输入定义范围**：单文件 / 目录 / 仓库根 / 多路径，由用户指定
- **不依赖 diff**：分析当前文件内容；用户提供 diff 仅作上下文参考，不是必需

### 默认值与运行前确认

| 项目 | 默认 | 用户偏离方式 |
|---|---|---|
| **路径** | 仓库根 | 选择：[仓库根] / [当前文件目录] / [列出顶级目录选择] |
| **大范围处理** | 按层（模块 / 目录）输出 | 选择优先子集（从顶级目录列表选） |

运行前必须确认两件事：(1) 审查路径；(2) 大范围时按层 vs 优先子集。

### 5 维分析

对范围内代码（按用户选定的层 / 子集），输出以下维度的 findings：

1. **模块边界**：模块 / 服务边界是否清晰、职责是否单一、依赖方向是否合理
2. **模式一致性**：模式使用是否得当、与仓库既有风格是否一致
3. **跨模块依赖与耦合**：依赖关系、循环依赖、耦合度
4. **技术债与可维护性**：重复、复杂度、可测试性、文档与注释当前状态
5. **接口稳定性**：模块对外接口的清晰度与稳定性

每条 finding 必须含 `file:line` 引用。

### 越界 finding 标记

如果在分析中发现属于安全 / 性能 / 架构 / 语言 / 框架的具体问题：**标记并提示对应原子技能**，但不展开分析。例：

> 检测到潜在 SQL 注入风险（user input 未转义直接拼接），建议运行 `review-security`

---

## 输入与输出

### 输入

- **路径**：一个或多个 file / dir 路径
- **可选**：focus 提示（如"重点看模块边界"）

### 输出

- **Findings list**：标准格式（location / category=scope / severity / title / description / suggestion），按文件或模块分组
- **大范围摘要**：按层组织时输出每层的 findings 数量与严重度分布

---

## 限制 (Restrictions)

### 硬边界

- 不假设"仅审查 diff"——本技能默认审查给定范围的完整当前状态
- 不输出 cognitive 维度的 findings（安全 / 性能 / 架构）
- 不输出语言 / 框架特定的 findings
- 不输出无 `file:line` 引用的 finding
- 不使用模糊语言（"可能有问题"无类型与方向 → 删除）

### 技能边界

**不做**（其他原子技能负责）：

- git 变更审查 → `review-diff`
- 全维度编排 → `orchestrate-code-review`
- 语言约定 → `review-<lang>`
- 框架约定 → `review-<framework>`
- 安全 / 性能 / 架构 → `review-security` / `review-performance` / `review-architecture`

---

## 自检

- [ ] 范围已与用户确认
- [ ] 大范围已按层输出或确认优先子集
- [ ] 5 维全部覆盖（模块边界 / 模式 / 依赖 / 技术债 / 接口）
- [ ] 每条 finding 含 file:line 引用
- [ ] 未输出 cognitive / 语言 / 框架维度的 finding（仅标记并提示对应原子技能）
- [ ] 输出格式合规（location / category / severity / title / description / suggestion）

---

## 示例

### 示例 1：单目录

- 输入：`src/auth/`
- 输出：5 维 findings，按文件分组，每条带 `auth.go:42` 类引用；遇到加密弱算法仅标记并提示 `review-security`

### 示例 2：单文件

- 输入：`pkg/validator/validator.go`
- 输出：模块职责 / 接口清晰度 / 测试覆盖 / 与上游模块依赖等 findings

### 示例 3：整仓（大范围）

- 输入：仓库根
- 行为：先按层（顶级目录）输出 findings 摘要表，再让用户选优先子集深入
- 输出：层级摘要 + 优先子集的详细 findings
