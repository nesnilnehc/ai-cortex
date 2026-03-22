---
name: review-react
description: Review React code for component design, hooks correctness, state management, rendering performance, and accessibility. Framework-only atomic skill; output is a findings list.
description_zh: 审查 React 代码：组件设计、hooks 正确性、状态管理、渲染性能与可访问性；框架级原子技能。
tags: [code-review]
version: 1.0.0
license: MIT
recommended_scope: project
metadata:
  author: ai-cortex
triggers: [review react]
input_schema:
  type: code-scope
  description: Source files or directories to review
output_schema:
  type: findings-list
  description: Zero or more findings with location, category, severity, and suggestion
---

# 技能（Skill）：复习React

## 目的 (Purpose)

仅查看 **React** 代码的 **框架约定**。不要定义范围（差异与代码库）或执行安全/架构分析；这些是通过范围和cognitive技能来处理的。以标准格式发出**结果列表**以进行聚合。重点关注功能组件设计、钩子正确性、状态管理（本地和外部）、渲染性能、副作用和数据获取、路由和代码分割以及可访问性。

---

## 核心目标（Core Objective）

**首要目标**：生成一个 React 框架结果列表，涵盖组件设计、钩子正确性、状态管理、渲染性能、副作用、路由/代码分割以及给定代码范围的可访问性。

**成功标准**（必须满足所有要求）：

1. ✅ **React框架专用范围**：仅审查React框架约定；未执行范围选择、安全性或架构分析
2. ✅ **涵盖所有七个 React 维度**：组件设计、钩子正确性、状态管理、渲染性能、副作用/数据获取、路由/代码分割和可访问性（如果相关）进行评估
3. ✅ **结果格式兼容**：每个结果包括位置、类别（`framework-react`）、严重性、标题、描述和可选建议
4. ✅ **组件/文件引用**：所有发现都引用特定文件：行或组件名称
5. ✅ **排除非 React 代码**：除非明确在范围内，否则不会分析非 React 文件的 React 特定规则

**验收测试**：输出是否包含以 React 为中心的结果列表，其中包含涵盖所有相关框架维度的组件/文件引用，而无需执行安全性、架构或范围分析？

---

## 范围边界（范围边界）

**本技能负责**：

- 功能组件设计（单一职责、组合模式、道具类型/默认、子模式）
- 钩子正确性（依赖数组、陈旧闭包、自定义钩子提取、钩子规则、useEffect 中的清理）
- 状态管理（本地与全局状态、上下文使用、reducer 模式、Zustand/Redux 等外部存储、使用 TanStack Query/SWR 的服务器状态）
- 渲染性能（memo/useMemo/useCallback 使用、列表中的关键稳定性、避免不必要的重新渲染、大型列表的虚拟化）
- 副作用和数据获取（useEffect 模式、竞争条件、中止控制器、加载/错误状态、数据获取库）
- 路由和代码分割（React.lazy、Suspense 边界、基于路由的分割、错误边界）
- 辅助功能（ARIA 属性、语义 HTML、键盘导航、焦点管理、屏幕阅读器支持）

**本技能不负责**：

- 范围选择——范围由调用者提供
- 安全分析（XSS、注入风险）——使用“review-security”
- 架构分析——使用“review-architecture”
- 语言/运行时（JavaScript/TypeScript）约定 - 使用“review-typescript”或一般 JS/TS 分析
- 全面精心策划的审核——使用“审核代码”

**转交点**：当所有 React 发现结果发出后，将其移交给 `review-code` 进行聚合。对于 XSS 风险（危险的 SetInnerHTML 滥用、未经净化的内容），请记下它们并建议“审查安全性”。

---

## 使用场景（用例）

- **精心安排的审查**：当 [review-code](../review-code/SKILL.md) 运行 React 项目的范围 → 语言 → 框架 → 库 → cognitive时，用作框架步骤。
- **仅 React 审查**：当用户只想检查 React/前端框架约定时。
- **PR 前 React 检查表**：确保钩子使用、组件设计和状态管理模式正确。

**何时使用**：当正在审查的代码是React并且任务包括框架质量时。范围由调用者或用户确定。

---

## 行为（行为）

### 该技能的范围

- **分析**：**给定代码范围**（调用者提供的文件或 diff）中的 React 框架约定。不决定范围；接受代码范围作为输入。
- **不要**：执行范围选择、安全审查或架构审查；不要检查非 React 文件中的 React 规则，除非在范围内（例如混合存储库）。

### 审查清单（仅限 React 框架）

1. **组件设计**：优先选择功能组件；每个组件单一职责；深度嵌套的组合；具有合理默认值的显式 prop 类型（TypeScript 接口或 PropTypes）；适当地使用孩子并渲染道具。
2. **Hooks正确性**：正确使用useEffect/useMemo/useCallback中的依赖数组；避免陈旧的关闭；将可重用逻辑提取到自定义挂钩中；遵循钩子规则（仅限顶层，仅限 React 函数）； useEffect 中用于订阅和计时器的清理函数。
3. **状态管理**：适当选择本地状态（useState）与全局状态；使用 Context 来处理横切关注点，但不要过度使用；更喜欢 useReducer 来进行复杂的状态转换；正确集成外部存储（Zustand、Redux Toolkit）；将服务器状态（TanStack 查询、SWR）与客户端状态分开。
4. **渲染性能**：在明显有益的地方应用 React.memo、useMemo、useCallback；列表中的稳定键（动态列表没有索引作为键）；当导致重新渲染时，避免在 JSX 中内联创建对象/函数；对大型列表使用虚拟化（react-window、react-virtuoso）。
5. **副作用和数据获取**：正确的useEffect模式（单一目的效果，适当的清理）；使用中止控制器或标志处理竞争条件；明确表示加载/错误/成功状态；与原始 useEffect + fetch 相比，更喜欢数据获取库（TanStack Query、SWR）。
6. **路由和代码分割**：使用React.lazy和Suspense进行基于路由的代码分割；定义延迟加载路由的错误边界；保持路由定义是声明性的；当延迟加载合适时，避免急切地加载完整模块。
7. **辅助功能**：使用语义HTML元素；正确应用 ARIA 属性（角色、标签、活动区域）；确保键盘导航和焦点管理；支持屏幕阅读器；测试交互组件的可访问性合规性。

### 语气和参考

- **专业和技术**：参考具体位置（文件：行或组件名称）。发出包含位置、类别、严重性、标题、描述、建议的结果。

---

## 输入与输出 (Input & Output)

### 输入（输入）

- **代码范围**：包含 React 代码的文件或目录（或 diff）（带有 React API 的 .tsx、.jsx、.ts、.js）。由用户或范围技能提供。

### 输出（输出）

- 以**附录：输出合同**中定义的格式发出零个或多个**结果**。
- 此技能的类别是 **framework-react**。

---

## 限制（限制）

### 硬边界（Hard Boundaries）

- **不要**执行范围选择、安全性或架构审查。遵守 React 框架约定。
- **不要**在没有具体地点或可行建议的情况下给出结论。
- **不要**审查非 React 代码的 React 特定规则，除非明确在范围内。

### 技能边界 (Skill Boundaries)

**不要做这些**（其他技能可以处理它们）：

- 不要选择或定义代码范围 - 范围由调用者或“审查代码”确定
- 不要执行安全分析（XSS、注入）——使用“review-security”
- 不要执行架构分析——使用“review-architecture”

**何时停止并交接**：

- 当所有 React 发现结果发出后，将其交给“review-code”进行聚合
- 当发现 XSS 风险时（例如不安全的 `dangerouslySetInnerHTML` 使用），请注意并建议 `review-security`
- 当用户需要全面审查（范围+语言+cognitive）时，重定向到“审查代码”

---

## 自检（Self-Check）

### 核心成功标准

- [ ] **仅限 React 框架范围**：仅审查 React 框架约定；未执行范围选择、安全性或架构分析
- [ ] **涵盖所有七个 React 维度**：组件设计、钩子正确性、状态管理、渲染性能、副作用/数据获取、路由/代码分割和可访问性（如果相关）进行评估
- [ ] **符合调查结果格式**：每个调查结果包括位置、类别（`framework-react`）、严重性、标题、描述和可选建议
- [ ] **组件/文件引用**：所有结果引用特定文件：行或组件名称
- [ ] **排除非 React 代码**：除非明确在范围内，否则不会分析非 React 文件的 React 特定规则

### 流程质量检查

- [ ] 是否仅审查了 React 框架维度（无范围/安全/架构）？
- [ ] 是否涵盖了相关的组件设计、挂钩、状态、性能、副作用、路由和可访问性？
- [ ] 每个发现是否都包含位置、类别=framework-react、严重性、标题、描述和可选建议？
- [ ] 问题是否与 file:line 或组件相关？

### 验收测试

输出是否包含以 React 为中心的结果列表，其中包含涵盖所有相关框架维度的组件/文件引用，而无需执行安全性、架构或范围分析？

---

## 示例（示例）

### 示例 1：useEffect 中缺少清理

- **Input**：在 useEffect 中建立 WebSocket 连接的组件，不带清理功能。
- **预期**：发出缺少清理的结果（主要）；建议返回一个关闭连接的清理函数。类别=框架-反应。

### 示例 2：索引作为动态列表中的键

- **输入**：使用数组索引作为键呈现可排序/可过滤列表的组件。
- **预期**：发出关键不稳定和潜在状态错误的发现；建议使用稳定的唯一标识符作为密钥。类别=框架-反应。

### 边缘情况：现代代码库中的类组件

- **输入**：代码库中的旧类组件，否则使用功能组件和挂钩。
- **预期**：在可行的情况下提出迁移到带有钩子的功能组件的建议；检查类组件的生命周期正确性（componentDidMount、componentWillUnmount 清理）。请注意，对于稳定、经过充分测试的组件，建议进行迁移，但并不总是需要迁移。

---

## 附录：输出合约

每项调查结果必须遵循标准调查结果格式：

|元素|要求 |
| :--- | :--- |
| **位置** | `path/to/Component.tsx` 或 `.jsx` （可选行或范围）。 |
| **类别** | `框架反应`。 |
| **严重性** | `关键` \| `主要` \| `次要` \| `建议`。 |
| **标题** |简短的一行摘要。 |
| **描述** | 1-3 句话。 |
| **建议** |具体修复或改进（可选）。 |

示例：


```markdown
- **Location**: `src/components/UserList.tsx:42`
- **Category**: framework-react
- **Severity**: major
- **Title**: useEffect missing cleanup for subscription
- **Description**: The WebSocket subscription in useEffect is never closed, causing memory leaks when the component unmounts.
- **Suggestion**: Return a cleanup function from useEffect that calls `socket.close()`.
```