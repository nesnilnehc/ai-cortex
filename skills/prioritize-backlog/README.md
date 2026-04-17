# 优先级评分（Prioritize Backlog）

用多框架（RICE + WSJF + MoSCoW + ICE）并行**强制重评**全部 backlog 条目（忽略原 priority），自动适配多文件目录或单文件 backlog，呈现框架分歧，由用户做出最终优先级决策。

## 用途

批量重评 backlog 条目（自动识别单 / 多文件形态，强制覆盖旧评估）：每条跑四个框架评分，Surface 框架间分歧，捕获用户决策并按所在形态写回。**不聚合单一分数** —— 保留分歧信号是核心设计（依据 ADR 20260417-unified-value-driven-prioritization-model 决策 3.2）。

## 何时使用

- `capture-work-items` 批量捕获后建议触发
- Planning ceremony 前对积压做一次干净的全量重评
- 战略刷新后任何节点直接重跑（无需额外开关）
- `plan-next` 输出的大缺口被 capture 后进入评分
- 单文件 backlog 项目（仅有 `backlog.md`）也能直接处理

## 输入

- 任意 priority 状态的 backlog 条目（多文件目录形式或单文件 backlog.md 均可）
- `docs/project-overview/strategic-goals.md`
- 可选：项目自定义的阈值覆盖

## 输出

- 对话批量评分表（四框架结果 + 分歧标记 + 决策建议 + 形态声明 + 覆盖统计）
- 每个 backlog 条目按所在形态被更新：`priority` + `priority_decision`（含 `previous` 旧值快照）

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
