# 优先级评分（Prioritize Backlog）

用多框架（RICE + WSJF + MoSCoW + ICE）并行评估 backlog 条目，呈现框架分歧，由用户做出最终优先级决策。

## 用途

批量处理 `priority: unset` 的 backlog 条目：每条跑四个框架评分，Surface 框架间分歧，捕获用户决策并写回 backlog frontmatter。**不聚合单一分数** —— 保留分歧信号是核心设计（依据 ADR 20260417-unified-value-driven-prioritization-model 决策 3.2）。

## 何时使用

- `capture-work-items` 批量捕获后建议触发
- Planning ceremony 前批量处理未评分积压
- 战略刷新后，重新评估 backlog（显式 `re-score=true`）
- `plan-next` 输出的大缺口被 capture 后进入评分

## 输入

- 一批 `priority: unset` 的 backlog 条目
- `docs/project-overview/strategic-goals.md`
- 可选：项目自定义的阈值覆盖

## 输出

- 对话批量评分表（四框架结果 + 分歧标记 + 决策建议）
- 每个 backlog 文件 frontmatter 更新：`priority` + `priority_decision`

## 安装

```bash
npx skills add nesnilnehc/ai-cortex --skill prioritize-backlog
```

## 相关技能

- `capture-work-items` —— 上游：产生 `priority: unset` 条目
- `promote-roadmap-items` —— 下游：基于评分结果批量晋升
- `design-strategic-goals` —— 上游依赖：提供 strategic-goals 供 MoSCoW 判断

## 完整定义

参见 [SKILL.md](./SKILL.md)。
