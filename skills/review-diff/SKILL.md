---
name: review-diff
description: Review only git diff for impact, regression, correctness, compatibility, and side effects. Scope-only atomic skill; output is a findings list for aggregation.
description_zh: 仅审查 git diff（含未跟踪文件）的影响、回归、正确性、兼容性与副作用；scope-only 原子技能，输出 findings 列表。
tags: [code-review, scope-only]
license: MIT
recommended_scope: project
metadata:
  author: ai-cortex
triggers: [review diff, diff review]
input_schema:
  type: code-scope
  description: Git diff (staged + unstaged, optional untracked) to review
output_schema:
  type: findings-list
  description: Scope-only findings for impact, regression, correctness, compatibility, and side effects
---

# 技能（Skill）：审查 Diff（Review Diff）

## 目的 (Purpose)

仅审查**当前变更**（git diff：暂存 + 未暂存 + 可选未跟踪文件）的 5 维：意图 / 影响、回归 / 正确性、breaking change / 兼容性、副作用 / 幂等性、可观测性。产出 scope-only findings list，作为 `orchestrate-code-review` 的 scope 步聚合输入。

不做架构 / 安全 / 语言 / 框架特定分析——这些归对应原子技能。

---

## 核心目标（Core Objective）

**首要目标**：仅针对 diff 范围（含未跟踪文件）产出 5 维 findings list。

**成功标准**（必须全部满足）：

1. ✅ **仅 diff 范围**：仅审查变更集，不展开仓库级 / 架构 / 安全 / 语言特定检查
2. ✅ **5 维全覆盖**：意图 / 影响、回归 / 正确性、breaking change / 兼容性、副作用 / 幂等性、可观测性
3. ✅ **格式合规**：每条 finding 含 location / category=`scope` / severity / title / description / suggestion
4. ✅ **位置精确**：所有 findings 引用具体 `file:line` 或 `@@` 块
5. ✅ **bug fix 验证**：bug 修复 diff 必须验证修复正确性，并标记任何遗留或部分问题

---

## 范围边界（Scope Boundaries）

**本技能负责**：

- 当前 git diff（暂存 + 未暂存）
- 变更集中的未跟踪文件（默认包含，视为完整文件 add）
- 5 维分析：意图 / 影响、回归 / 正确性、breaking / 兼容性、副作用 / 幂等性、可观测性

**本技能不负责**：

- 仓库级或快照级审查 → `review-codebase`
- 全维度编排审查 → `orchestrate-code-review`
- 架构 / 安全 / 性能 / 测试 cognitive 维度 → 对应 cognitive 原子技能
- 语言 / 框架特定约定 → 对应原子技能

**交接点**：findings 输出后作为 orchestrate-code-review 的 scope 步聚合输入；或交给 `orchestrate-repair-loop` 做修复迭代。

---

## 使用场景

- **pre-commit / pre-PR 门禁**：提交前快速看变更引入的问题
- **作为 orchestrate-code-review 的 scope 步**：与 `review-codebase` 二选一
- **聚焦审查**：用户明确"只看变更"

---

## 行为 (Behavior)

### 范围解析

- **分析对象**：变更集中的文件——diff（暂存 + 未暂存）+ 默认包含的未跟踪文件
- **未跟踪文件处理**：调用方传入路径与完整内容；视为完整文件 add，应用同 5 维清单；引用 file:line
- **不分析**：未变更或超出变更集的文件

### 5 维分析清单

对每个变更文件，按以下维度产出 findings：

1. **意图与影响**：发生了什么变更、为什么；对调用方 / 数据 / 配置 / 部署的影响
2. **回归与正确性**：是否引入新 bug 或漏掉边界情况；bug fix diff 修复是否完整
3. **breaking change 与兼容性**：是否破坏 API / 数据 / 配置契约；向后兼容；版本控制 / 弃用
4. **副作用与幂等性**：意外副作用、数据损坏、重复执行风险、幂等性问题
5. **可观测性**：变更是否新增 / 修复用于生产调试的日志、指标、错误信息

### 特殊情况

- **bug fix diff**：验证修复正确性，记录任何遗留或部分问题
- **仅格式 / 注释 diff**：输出一条次要 finding "仅格式 / 注释，无行为变更"；如注释与代码矛盾则发 finding 含建议

---

## 输入与输出

### 输入

- **git diff**：当前分支 vs HEAD 的暂存 + 未暂存变更
- **未跟踪文件**（默认包含）：路径 + 完整内容

### 输出

- **Findings list**：标准格式（`location` / `category=scope` / `severity` / `title` / `description` / `suggestion`）
- 每条 finding 必须含 file:line 或 @@ 块引用
- 每条 finding 必须含 actionable suggestion（修复方向 + 具体位置）

---

## 限制 (Restrictions)

### 硬边界

- 不审查 diff 之外的文件
- 不输出无 file:line 引用的 finding
- 不使用模糊语言（"可能有问题"无类型与方向 → 删除）
- 不做安全 / 架构 / 语言 / 框架检查（保持在 scope 维度内）

### 技能边界

**不做**（其他原子技能负责）：

- 仓库级 / 快照级审查 → `review-codebase`
- 全维度编排 → `orchestrate-code-review`
- 安全 → `review-security`
- 架构 → `review-architecture`
- 语言 / 框架 → 对应原子技能

---

## 自检

- [ ] 仅审查变更集（diff + 包含的未跟踪文件）
- [ ] 5 维全覆盖
- [ ] 每条 finding 格式合规（含 6 字段）
- [ ] 每条 finding 含 file:line 或 @@ 块引用
- [ ] 每条 finding 含 actionable suggestion
- [ ] bug fix diff 已验证修复正确性

---

## 示例

### 示例 1：API 变更

- **输入**：diff 新增 query 参数并修改 response 形状
- **预期**：findings 覆盖意图 / 影响（对调用方）、向后兼容性风险、breaking change 建议（如版本控制或弃用）；引用具体行或 @@ 块；不输出安全 / 架构 finding（移交对应原子技能）

### 示例 2：bug fix

- **输入**：diff 修复 null pointer 与错误码
- **预期**：findings 确认修复 + 验证类似 null pointer / 错误码问题是否仍存在；可观测性维度（日志 / 错误）；引用变更行；category=scope

### 示例 3：仅格式 / 注释

- **输入**：diff 仅含缩进 / 空格 / 注释变更
- **预期**：要么无 finding，要么一条 minor finding "仅格式 / 注释，无行为变更"；如注释与代码矛盾则发 finding 含建议

### 示例 4：变更集中的新（未跟踪）文件

- **输入**：diff + 未跟踪文件（路径 + 完整内容）
- **预期**：新文件作完整文件 add 审查；应用 5 维清单；location=路径与行引用；category=scope
