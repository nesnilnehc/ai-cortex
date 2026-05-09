---
name: orchestrate-code-review
description: Orchestrator skill — sequence atomic review-* skills (scope → language → framework → library → cognitive) and aggregate findings into a unified report.
description_zh: 编排技能——按 scope → language → framework → library → cognitive 顺序串联原子 review-* 技能，聚合 findings 为统一报告。
tags: [code-review, orchestration]
license: MIT
recommended_scope: project
metadata:
  author: ai-cortex
triggers: [review code, code review, pr review, orchestrate code review]
input_schema:
  type: code-scope
  description: Diff or codebase path(s) to review, plus optional language/framework hint
  defaults:
    scope: diff
    untracked: include
output_schema:
  type: findings-list
  description: Aggregated, deduplicated findings with risk signals from all executed atomic skills
---

# 编排技能：代码审查（Orchestrate Code Review）

## 目的 (Purpose)

按固定顺序串联原子 review-* 技能并聚合 findings。本技能仅做编排，不执行代码分析。单维度审查请直接调用对应原子技能（如仅查 diff 用 `review-diff`、仅查安全用 `review-security`）。

---

## 编排职责（Orchestrator Role）

按命名规范，编排技能**只做 4 件事**：

1. **检测上下文**：根据用户意图与项目状态确定 scope（diff / codebase）、语言、框架
2. **串联调用**：按固定顺序 scope → language → framework → library → cognitive 执行原子 review-* 技能
3. **halt-on-failure**：任一原子技能失败时停止后续，汇报已收集 findings
4. **聚合输出**：合并 findings、去重（位置 + 标题相同保留最高严重度）、机械派生 risk_signals

**严禁**：在本技能内执行代码分析、内嵌 lint 规则、为单一原子 skill 重复实现其逻辑。

---

## 执行顺序（固定）

| 步骤 | 类型 | 候选原子技能 | 选择规则 |
|---|---|---|---|
| 1 | scope | `review-diff` 或 `review-codebase` | 二选一，按用户意图（diff = 当前变更；codebase = 给定路径） |
| 2 | language | `review-typescript` / `review-python` / `review-go` / `review-java` / `review-php` / `review-powershell` / `review-dotnet` / `review-sql` | 0 或 1 个，按范围内主语言推断 |
| 3 | framework | `review-react` / `review-vue` | 0 或 1 个，按范围内框架推断 |
| 4 | library | `review-orm-usage` | 0 或 1 个，按范围内 ORM 使用情况推断 |
| 5 | cognitive | `review-security` → `review-performance` → `review-architecture` → `review-testing` | 全部按顺序执行 |

无匹配的步骤跳过；最终报告标注哪些步骤跳过及原因。

---

## 行为 (Behavior)

### 步骤 1：检测上下文

- 范围（scope）确认：用户未明示时让其在 `diff` / `codebase` 间二选一
- diff 模式默认包含未跟踪文件
- codebase 模式默认仓库根，可指定路径
- 语言 / 框架推断：从范围内文件后缀与依赖文件（package.json、pyproject.toml 等）推断；不确定时从候选列表让用户选

### 步骤 2：串联调用

按上表顺序依次调用原子技能，每步收集 findings（标准格式：location / category / severity / title / description / suggestion）。

### 步骤 3：halt-on-failure

任一原子技能失败 → 停止后续，输出已收集 findings + 失败说明。

### 步骤 4：聚合输出

- **去重规则**：相同 `location + title` 跨步骤合并，保留最高 severity，在 description 标注其他命中步骤
- **风险信号**：基于聚合后 findings + 变更上下文做**机械规则映射**（按 severity 分布、文件涉及面、关键词匹配），不做主观判断；无明确信号时输出空列表 `[]`

---

## 输入与输出

### 输入

- 用户意图（要查 diff / codebase / 指定路径）
- 可选：语言 / 框架提示

### 输出

单一聚合报告：

- 各原子技能 findings（按 category 或 location 分组）
- 跳过步骤说明
- `risk_signals` 列表（每条含 signal_name + 可选 confidence ∈ [0, 1]）
- 顶部摘要（按 severity 计数、按 category 计数）

---

## 限制 (Restrictions)

### 硬边界

- 不在本技能内执行代码分析、lint、规则匹配（违反 orchestrator 4-things 原则）
- 不改变执行顺序（scope → language → framework → library → cognitive）
- 不发明 findings；只聚合原子技能产出
- 不要求每个原子技能输出 risk_signals；风险标签只在聚合阶段产出
- 不修改代码 / 不实施修复（交给开发或 `orchestrate-repair-loop`）

### 技能边界

**编排技能内不做**（应由原子子技能或下游技能承接）：

- 直接代码分析 → 各原子 review-* 技能
- 单维度审查 → 直接调用对应原子技能
- 修复实施 → `orchestrate-repair-loop` 或开发流程
- 测试编写 → 测试相关技能

---

## 自检

- [ ] 仅做"检测上下文 / 串联调用 / halt-on-failure / 聚合输出" 4 件事
- [ ] 未在本技能内实现 domain 检测逻辑
- [ ] scope 已与用户确认
- [ ] 执行顺序固定（scope → language → framework → library → cognitive）
- [ ] 跳过步骤已在报告中注明
- [ ] findings 去重规则已应用（同 location + title 保留最高 severity）
- [ ] risk_signals 基于聚合 findings 机械派生，无主观判断

---

## 示例

### 示例 1：.NET 项目 diff 审查

- 输入：用户说"查我的更改"，项目是 C#
- 调度：`review-diff` → `review-dotnet` → `review-security` → `review-performance` → `review-architecture` → `review-testing`
- 跳过：framework / library 步（无匹配）
- 聚合：单一报告 + risk_signals

### 示例 2：Vue 前端 codebase 审查

- 输入：`src/frontend`，项目使用 Vue 3 + ORM
- 调度：`review-codebase` → `review-typescript` → `review-vue` → `review-orm-usage` → `review-security` → `review-performance` → `review-architecture` → `review-testing`
- 聚合：单一报告

### 示例 3：边界场景——无语言匹配

- 输入：Rust 项目（无对应原子技能）
- 调度：`review-codebase` → 跳过 language / framework / library → cognitive 全部执行
- 聚合：报告标注语言 / 框架步跳过及原因
