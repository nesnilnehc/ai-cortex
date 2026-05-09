# 编排：代码审查（orchestrate-code-review）

按固定顺序串联原子 review-* 技能（scope → language → framework → library → cognitive），聚合 findings 为统一报告。本技能仅做编排，不执行代码分析。

## 何时使用

- 完整代码审查：用户要求"审查代码"或"审查我的更改"并期望统一报告
- pre-PR / pre-commit：跑完整流水线一次拿到 baseline
- 与 `orchestrate-repair-loop` 配合：先跑本技能拿到 findings，再交给 `orchestrate-repair-loop` 迭代修复

## 何时不用

- 单维度审查 → 直接调用对应原子技能（`review-diff` / `review-security` / 等）

## 输入

- 用户意图（diff 还是 codebase；指定路径）
- 可选：语言 / 框架提示

## 输出

- 单一聚合报告（findings + risk_signals + 跳过步骤说明）

## 编排原则

仅做：检测上下文 / 串联子技能 / halt-on-failure / 聚合输出。所有 domain 检测逻辑位于原子 review-* 子技能内。

## 完整定义

见 [SKILL.md](./SKILL.md)。
