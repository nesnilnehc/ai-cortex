# 映射条目依赖（Map Item Dependencies）

识别 backlog 与 roadmap 条目之间的依赖，写入条目 `depends_on`，产出依赖图与阻塞清单。在晋升前运行，避免被阻塞的条目被拉进 Now。

## 用途

按五类（技术 / 团队 / 外部 / 知识 / 顺序）逐一排查条目间依赖，标注「需在何时前解决」与责任方，对高风险依赖给出削减建议，并输出可被 `promote-roadmap-items` 直接消费的阻塞清单。依赖是路线图上风险最高的一类因素——它不体现在优先级里，也不体现在容量里，但会让高优先级条目进入 Now 后原地卡住。

## 何时使用

- **晋升前**：候选条目 ≥ 2 时先跑，避免把被阻塞条目拉进 Now
- **排期评审**：需要看清哪些条目必须串行、哪些可以并行
- **卡住时复盘**：Now 层条目迟迟不动，排查是否有未登记的前置

## 输入

- backlog 条目（任意 priority 状态）
- `docs/process-management/roadmap.md`
- 可选：范围限定（默认取当前晋升候选）

## 输出

- 对话依赖图 + 需解决时点表 + 削减建议
- 阻塞清单（哪些条目当前不可进 Now）
- 各条目 frontmatter 的 `depends_on` 被更新

## 安装

统一由 AI Cortex 的 canonical 安装管理，见仓库根 [README](../../README.md#-安装与使用)。

## 相关技能

- `promote-roadmap-items` —— 下游：Now 层准入护栏消费本技能产出的 `depends_on`
- `prioritize-backlog` —— 上游：提供已评分的候选条目
- `update-roadmap` —— 消费方：挪期时读 `depends_on` 计算下游影响
- `orchestrate-roadmap-planning` —— 编排方：作为晋升前的第 5 步

## 完整定义

参见 [SKILL.md](./SKILL.md)。
