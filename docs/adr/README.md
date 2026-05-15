# Architecture Decision Records

本仓库使用 ADR（Architecture Decision Record）记录影响系统结构与治理的关键决策。

## 为什么用 ADR

好的决策记录回答四个问题：**What**（决定了什么）/ **Why**（为什么）/ **Alternatives**（考虑过哪些替代）/ **Consequences**（带来什么后果）。这些问题的答案散落在 commit、PR、口头讨论中会迅速消失；集中在 ADR 里，半年后的团队成员仍能重建决策上下文，而不是在代码里看到一个"为什么这样设计"的谜题。

## 数据契约与写作纪律

- **数据契约**（frontmatter 字段、status 枚举、正文结构）→ [specs/adr-modeling.md](../../specs/adr-modeling.md)
- **写作纪律**（准入门槛、状态执行、衰减政策）→ [rules/adr-management.md](../../rules/adr-management.md)

## 如何新增 ADR

1. 复制 [`templates/adr-template.md`](./templates/adr-template.md)
2. 命名为 `NNNN-{slug}.md`，编号取下方索引最大编号 + 1（首篇新 ADR 从 `0010` 起）
3. 填写 frontmatter 与 4 节正文（背景 / 决策 / 替代方案 / 后果）
4. 在下方索引追加一行

## ADR 索引

| 编号 | 标题 | 状态 |
|---|---|---|
| [0001](./0001-io-contract-protocol.md) | 技能链 I/O 契约协议 | accepted |
| [0002](./0002-plan-next-v6-restructure.md) | plan-next v6 结构重构 | accepted |
| [0003](./0003-plan-next-v6.3-execution-state-and-linking.md) | plan-next v6.3 执行态与制品链接 | accepted |
| [0004](./0004-norms-driven-artifact-architecture.md) | 规范驱动制品架构 | accepted |
| [0005](./0005-retract-linking-mode-enum.md) | 回撤 linking_mode 枚举 | accepted |
| [0006](./0006-delete-linking-mode-and-unify-artifact-paths.md) | 删除 linking_mode 并统一制品路径 | accepted |
| [0007](./0007-remove-plan-next-execute-flag.md) | 移除 plan-next execute 参数 | accepted |
| [0008](./0008-replace-asqm-with-acceptance-criteria.md) | 用 Acceptance Criteria 替代 ASQM | accepted |
| [0009](./0009-replace-merge-worktree-with-deliver-and-integrate.md) | 用 deliver-feature + integrate-worktrees 替代 merge-worktree | accepted |
