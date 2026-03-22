---
name: review-vue
description: Review Vue 3 code for Composition API, reactivity, components, state (Pinia), routing, and performance. Framework-only atomic skill; output is a findings list.
description_zh: 审查 Vue 3 代码：Composition API、响应式、组件、状态 (Pinia)、路由与性能；框架级原子技能。
tags: [code-review]
version: 1.0.0
license: MIT
recommended_scope: project
metadata:
  author: ai-cortex
triggers: [review vue]
input_schema:
  type: code-scope
  description: Source files or directories to review
output_schema:
  type: findings-list
  description: Zero or more findings with location, category, severity, and suggestion
---

# 技能（Skill）：复习Vue

## 目的 (Purpose)

仅查看 **Vue 3** 代码的 **框架约定**。不要定义范围（差异与代码库）或执行安全/架构分析；这些是通过范围和cognitive技能来处理的。以标准格式发出**结果列表**以进行聚合。重点关注组合 API 和 `<script setup>`、反应性（ref/reactive、compute/watch）、组件边界和 props/emits、状态（Pinia/store）、路由和防护、性能（例如 v-memo）以及相关的可访问性。

---

## 核心目标（Core Objective）

**首要目标**：生成 Vue 3 框架调查结果列表，涵盖组合 API 使用情况、反应性正确性、组件边界、状态管理、路由、性能和给定代码范围的可访问性。

**成功标准**（必须满足所有要求）：

1. ✅ **仅 Vue 3 框架范围**：仅审查 Vue 3 框架约定；未执行范围选择、安全性或架构分析
2. ✅ **涵盖所有七个 Vue 维度**：组合 API/脚本设置、反应性（参考/反应/计算/监视）、组件边界/道具/发射、状态 (Pinia)、路由/防护、渲染性能和可访问性（如果相关）
3. ✅ **结果格式兼容**：每个结果包括位置、类别（`framework-vue`）、严重性、标题、描述和可选建议
4. ✅ **组件/文件引用**：所有发现都引用特定文件：行或组件名称
5. ✅ **排除非 Vue 代码**：除非明确在范围内，否则不会分析非 Vue 文件的 Vue 特定规则

**验收**测试：输出是否包含以 Vue 3 为中心的结果列表，其中包含涵盖所有相关框架维度的组件/文件引用，而无需执行安全性、架构或范围分析？

---

## 范围边界（范围边界）

**本技能负责**：

- 组合 API 和 `<script setup>` 正确性（defineProps、defineEmits、defineExpose、生命周期挂钩）
- 反应性正确性（参考与反应性、计算与观察、道具突变、深度反应性）
- 组件边界设计（道具/发射合同、道具钻探、提供/注入）
- 状态管理（Pinia/Vuex：动作与直接突变，避免服务器状态重复）
- 路由（Vue Router、导航守卫、延迟加载、路由参数/查询处理）
- 性能（v-memo、v-for key 稳定性、不必要的重新渲染）
- 辅助功能（语义 HTML、ARIA、表单标签、焦点管理）

**本技能不负责**：

- 范围选择——范围由调用者提供
- 安全分析（XSS、注入风险）——使用“review-security”
- 架构分析——使用“review-architecture”
- 语言/运行时（JavaScript/TypeScript）约定——使用一般的 JS/TS 分析或注释作为单独的关注点
- 全面精心策划的审核——使用“审核代码”

**转交点**：当所有 Vue 发现结果发出后，将其移交给“review-code”进行聚合。对于 XSS 风险（v-html 滥用、未经净化的内容），请记下它们并建议“审查安全性”。

---

## 使用场景（用例）

- **精心安排的审查**：当 [review-code](../review-code/SKILL.md) 运行 Vue 项目的范围 → 语言 → 框架 → 库 → cognitive时，用作框架步骤。
- **仅 Vue 审查**：当用户只想检查 Vue/前端框架约定时。
- **PR Vue 前检查表**：确保 Composition API 使用、反应性和组件契约正确。

**何时使用**：当正在审查的代码是 Vue 3 并且任务包括框架质量时。范围由调用者或用户确定。

---

## 行为（行为）

### 该技能的范围

- **分析**：**给定代码范围**（调用者提供的文件或 diff）中的 Vue 3 框架约定。不决定范围；接受代码范围作为输入。
- **不要**：执行范围选择、安全审查或架构审查；不要审查非 Vue 文件的 Vue 规则，除非在范围内（例如混合存储库）。

### 审查清单（仅限 Vue 框架）

1. **Composition API 和脚本设置**：优先选择 `<script setup>` 和 Composition API；正确使用defineProps、defineEmits、defineExpose；生命周期挂钩（onMounted、onUnmounted 等）。
2. **反应性**：正确使用ref与reactive；计算与手表；避免改变道具；深度反应性和模板中的展开。
3. **组件边界**：明确 props/emits 合约；避免在适合储存或提供/注入的地方进行支柱钻探；每个组件单一责任。
4. **状态（Pinia/store）**：适当使用Pinia（或Vuex）商店；避免在多个地方重复服务器状态；行动与直接突变。
5. **路由和守卫**：Vue Router 的使用；导航守卫和延迟加载；路由参数和查询处理。
6. **性能**：列表渲染代价昂贵的v-memo；避免不必要的重新渲染；列表中的键用法。
7. **辅助功能**：语义 HTML 和 ARIA（如果相关）；表单标签和焦点管理。

### 语气和参考

- **专业和技术**：参考具体位置（文件：行或组件名称）。发出包含位置、类别、严重性、标题、描述、建议的结果。

---

## 输入与输出 (Input & Output)

### 输入（输入）

- **代码范围**：包含 Vue 3 代码（.vue、带有 Vue API 的 .ts）的文件或目录（或 diff）。由用户或范围技能提供。

### 输出（输出）

- 以**附录：输出合同**中定义的格式发出零个或多个**结果**。
- 此技能的类别是 **framework-vue**。

---

## 限制（限制）

### 硬边界（Hard Boundaries）

- **不要**执行范围选择、安全性或架构审查。遵守 Vue 3 框架约定。
- **不要**在没有具体地点或可行建议的情况下给出结论。
- **不要**审查非 Vue 代码的 Vue 特定规则，除非明确在范围内。

### 技能边界 (Skill Boundaries)

**不要做这些**（其他技能可以处理它们）：

- 不要选择或定义代码范围 - 范围由调用者或“审查代码”确定
- 不要执行安全分析（XSS、注入）——使用“review-security”
- 不要执行架构分析——使用“review-architecture”

**何时停止并交接**：

- 当所有 Vue 发现结果发出后，将其交给“review-code”进行聚合
- 当发现 XSS 风险时（例如不安全的 `v-html` 使用），记下它们并建议 `review-security`
- 当用户需要全面审查（范围+语言+cognitive）时，重定向到“审查代码”

---

## 自检（Self-Check）

### 核心成功标准

- [ ] **仅 Vue 3 框架范围**：仅审查 Vue 3 框架约定；未执行范围选择、安全性或架构分析
- [ ] **涵盖所有七个 Vue 维度**：组合 API/脚本设置、反应性（参考/反应/计算/监视）、组件边界/道具/发射、状态 (Pinia)、路由/防护、渲染性能和可访问性（如果相关）
- [ ] **符合调查结果格式**：每个调查结果包括位置、类别（`framework-vue`）、严重性、标题、描述和可选建议
- [ ] **组件/文件引用**：所有结果引用特定文件：行或组件名称
- [ ] **排除非 Vue 代码**：除非明确在范围内，否则不会分析非 Vue 文件的 Vue 特定规则

### 流程质量检查

- [ ] 是否仅审查了 Vue 框架维度（无范围/安全/架构）？
- [ ] 是否涵盖了相关的组合 API、反应性、组件、状态、路由和性能？
- [ ] 每个发现是否都包含位置、类别=framework-vue、严重性、标题、描述和可选建议？
- [ ] 问题是否与 file:line 或组件相关？

### 验收测试

输出是否包含以 Vue 3 为中心的结果列表，其中包含涵盖所有相关框架维度的组件/文件引用，而无需执行安全性、架构或范围分析？

---

## 示例（示例）

### 示例 1：改变 props

- **输入**：分配给脚本或模板中的道具的组件。
- **预期**：发出 prop 突变的发现（主要/次要）；建议本地状态或发送给父级。类别=framework-vue.

### 示例 2：v-for 中缺少键

- **输入**：v-for 不带 :key 或带有不稳定密钥（例如索引）。
- **预期**：发出列表身份和性能的结果；建议稳定的唯一密钥。类别=framework-vue.

### 边缘情况：Vue 2 选项 API

- **输入**：混合代码库中的旧版 Vue 2 Options API。
- **预期**：如果技能扩展到 Vue 2，则回顾 Vue 2 模式（数据、方法、生命周期）；否则请注意“首选 Vue 3 Composition API”（在迁移可行的情况下）。对于这个技能，重点关注Vue 3；仅当明确在范围内时才注意 Vue 2。

---

## 附录：输出合约

每项调查结果必须遵循标准调查结果格式：

|元素|要求 |
| :--- | :--- |
| **位置** | `path/to/file.vue` 或 `.ts` （可选行或范围）。 |
| **类别** | `框架-vue`。 |
| **严重性** | `关键` \| `主要` \| `次要` \| `建议`。 |
| **标题** |简短的一行摘要。 |
| **描述** | 1-3 句话。 |
| **建议** |具体修复或改进（可选）。 |

示例：


```markdown
- **Location**: `src/components/UserList.vue:18`
- **Category**: framework-vue
- **Severity**: major
- **Title**: v-for missing stable key
- **Description**: Using index as key can cause incorrect reuse and state bugs when list order changes.
- **Suggestion**: Use a unique stable id (e.g. user.id) as :key.
```