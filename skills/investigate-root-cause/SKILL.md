---
name: investigate-root-cause
description: Systematic debugging with root cause investigation. Four phases: investigate, analyze, hypothesize, implement. Iron Law: no fixes without root cause. Use when asked to "debug this", "fix this bug", "why is this broken", "investigate this error", or "root cause analysis".
description_zh: 系统性根因调试：investigate → analyze → hypothesize → implement。铁律：无根因不修复。适用于报错、异常行为、故障排查。
tags: [workflow, optimization]
version: 1.0.0
license: MIT
recommended_scope: both
metadata:
  author: ai-cortex
  evolution:
    sources:
      - name: "investigate"
        repo: "https://github.com/nesnilnehc/gstack"
        version: "1.0.0"
        license: "MIT"
        type: "fork"
        borrowed: "Four-phase workflow, Iron Law, pattern analysis table, hypothesis testing rules, 3-strike escalation"
    enhancements:
      - "Platform-agnostic: removed gstack freeze hooks and scope lock script"
      - "Handoff to automate-repair for test-run-fix loop"
triggers: [debug, fix bug, investigate error, root cause analysis]
input_schema:
  type: free-form
  description: Error messages, stack traces, reproduction steps, or affected file paths
output_schema:
  type: document-artifact
  description: Debug report with symptom, root cause, fix, evidence, regression test reference
---

# 技能 (Skill)：根因调试

## 目的 (Purpose)

通过系统性根因调查与假设验证，在未确认根因前不实施修复，避免症状修补导致的连锁问题。适用于报错、异常行为或「之前能跑、现在坏了」的故障排查。

---

## 核心目标（Core Objective）

**首要目标**：在确认根因后实施最小修复，并附回归测试与验证证据。

**成功标准**（必须满足所有要求）：

1. ✅ **铁律**：未确认根因前不实施任何修复（no fixes without root cause）
2. ✅ **Phase 1 完成**：症状收集、代码追溯、近期变更检查、可复现性确认；产出可验证的根因假设
3. ✅ **Phase 2 完成**：与已知模式对照（竞态、nil 传播、状态损坏等）；必要时 WebSearch 通用错误类型（脱敏后）
4. ✅ **Phase 3 完成**：通过临时日志或断言验证假设；若三次假设均失败则中止并升级
5. ✅ **Phase 4 完成**：最小化 diff、修复根因非症状、编写回归测试、全量测试通过
6. ✅ **Phase 5 完成**：原始场景可复现验证；输出结构化 Debug Report

**验收测试**：回归测试在无修复时失败、有修复时通过；原始问题场景已复现并验证修复。

---

## 范围边界（Scope Boundaries）

**本技能负责**：

- 根因调查（症状、代码路径、git 历史、复现）
- 模式匹配与假设验证
- 根因确认后的最小修复与回归测试
- 结构化 Debug Report 输出

**本技能不负责**：

- 测试执行与修复循环编排（使用 `automate-repair`）
- 代码审查（使用 `review-diff`、`review-code`）
- 架构级问题（多次修复仍失败时建议人工审查）

**转交点**：根因确认并修复后，若需迭代运行测试并修复，移交 `automate-repair`。若三次假设失败，输出 BLOCKED 状态并建议人工介入。

---

## 使用场景（Use Cases）

- 用户报告错误、异常行为或「为什么坏了」
- 测试失败需定位根因
- 间歇性问题需系统性排查
- 回归引入的 bug 需追溯

---

## 行为（Behavior）

### 铁律（Iron Law）

**NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST.**

修补症状会形成打地鼠式调试。每次非根因修复都会增加后续排查难度。先确认根因，再修复。

---

### Phase 1：根因调查

在形成假设前收集上下文。

1. **收集症状**：读取错误信息、堆栈、复现步骤。若信息不足，一次只问一个问题。
2. **阅读代码**：从症状沿调用链回溯；使用 Grep 查找引用，Read 理解逻辑。
3. **检查近期变更**：`git log --oneline -20 -- <affected-files>`。之前能跑吗？改了什么？回归意味着根因在 diff 中。
4. **复现**：能否确定性地触发？若不能，继续收集证据。

输出：**"Root cause hypothesis: ..."** — 可验证的、具体的断言：哪里错了、为什么。

---

### Phase 2：模式分析

检查是否匹配已知模式：

| 模式 | 特征 | 关注点 |
|------|------|--------|
| 竞态条件 | 间歇性、依赖时序 | 并发访问共享状态 |
| nil/null 传播 | NoMethodError、TypeError | 可选值缺少守卫 |
| 状态损坏 | 数据不一致、部分更新 | 事务、回调、钩子 |
| 集成失败 | 超时、意外响应 | 外部 API、服务边界 |
| 配置漂移 | 本地能跑、staging/prod 失败 | 环境变量、特性开关、DB 状态 |
| 陈旧缓存 | 显示旧数据、清缓存后恢复 | Redis、CDN、浏览器缓存 |

同时检查：`TODOS.md` 中相关已知问题；`git log` 同区域历史修复 — 同一文件反复出 bug 多为架构问题。

**外部模式搜索**：若不匹配上述模式，WebSearch `"{framework} {generic error type}"` — **先脱敏**：去掉主机名、IP、路径、SQL、客户数据。仅搜索错误类别。WebSearch 不可用时跳过。

---

### Phase 3：假设验证

在编写任何修复前，验证假设。

1. **确认假设**：在疑似根因处添加临时日志、断言或调试输出。复现。证据是否匹配？
2. **若假设错误**：返回 Phase 1 收集更多证据。可先 WebSearch 通用错误类型（脱敏）。勿猜测。
3. **三次失败规则**：若三次假设均失败，**中止**。AskUserQuestion：
   ```
   3 次假设验证均未匹配。可能是架构问题而非简单 bug。
   A) 继续调查 — 我有新假设：[描述]
   B) 升级人工审查 — 需熟悉系统的人
   C) 增加日志等待 — 在相关区域加日志，下次发生时捕获
   ```

**红旗**：提出「先临时修一下」、在未追溯数据流前提议修复、每次修复都暴露出新问题 — 放慢节奏，考虑是否在错误层级。

---

### Phase 4：实施

根因确认后：

1. **修复根因，非症状**。最小改动消除实际问题。
2. **最小 diff**：最少文件、最少行数。勿顺便重构相邻代码。
3. **编写回归测试**：无修复时失败、有修复时通过。
4. **运行全量测试**。粘贴输出。不允许回归。
5. **若修复涉及 >5 个文件**：AskUserQuestion 提示影响面，确认是否拆分或重新评估。

---

### Phase 5：验证与报告

**新鲜验证**：复现原始 bug 场景，确认已修复。不可省略。

输出结构化 Debug Report：

```
DEBUG REPORT
════════════════════════════════════════
Symptom:         [用户观察到的现象]
Root cause:      [实际根因]
Fix:             [变更内容，含 file:line]
Evidence:        [测试输出、复现结果]
Regression test: [新测试的 file:line]
Related:         [TODOS 项、同区域历史 bug、架构备注]
Status:          DONE | DONE_WITH_CONCERNS | BLOCKED
════════════════════════════════════════
```

---

## 输入与输出 (Input & Output)

### 输入

- 错误信息、堆栈、复现步骤
- 可选：受影响文件或目录

### 产出

- 根因假设与验证过程
- 最小修复与回归测试
- 结构化 Debug Report

---

## 限制（Restrictions）

### 硬边界

- 未确认根因前不实施修复
- 无法复现并验证的修复不交付
- 不说「这应该能修好」；必须运行测试证明
- 三次假设失败后中止并升级

### 技能边界 (Skill Boundaries)

**不要做这些（其他技能可以处理它们）**：

- **测试-修复循环**：使用 `automate-repair`
- **代码审查**：使用 `review-diff`、`review-code`

---

## 自检（Self-Check）

### 成功标准

- [ ] 根因假设已明确且可验证
- [ ] Phase 1–3 已完成；假设已通过验证
- [ ] 修复针对根因、diff 最小
- [ ] 回归测试已编写并通过
- [ ] 原始场景已复现并验证修复
- [ ] Debug Report 已输出

### 验收测试

回归测试在无修复时失败、有修复时通过？

---

## 示例（Examples）

### 示例 1：nil 传播

**症状**：`NoMethodError: undefined method 'x' for nil`。  
**Phase 1**：追溯调用链，发现某处返回 nil 未守卫。  
**Phase 2**：匹配 nil 传播模式。  
**Phase 3**：在疑似处加断言，复现后确认。  
**Phase 4**：加 nil 检查；编写测试覆盖该路径。  
**Phase 5**：原始场景验证；输出 Report。

### 示例 2：三次假设失败

**Phase 3**：三次假设均被验证否决。输出 BLOCKED，建议人工审查或增加日志等待下次捕获。
