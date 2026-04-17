# 晋升 Roadmap 条目（Promote Roadmap Items）

把已评分的 backlog 条目按战略目标容量分配晋升到 roadmap 的 Now / Next / Later 槽位。事件驱动，不绑固定周期。

## 用途

Roadmap planning ceremony 的支撑技能：读取 priority 已定的 backlog + 当前 roadmap + 战略目标容量分配，生成晋升 / 降级候选，用户逐项确认后更新 roadmap 和条目 status（依据 ADR 20260417-work-lifecycle-and-skill-responsibilities 决策 3.7.2）。

## 何时使用

- **容量释出**：上一批 Now 层条目完成后
- **战略刷新**：战略目标或容量分配调整后
- **大缺口补入**：`plan-next` 输出的治理大缺口被 capture + prioritize 后进入晋升
- **按需 planning**：用户主动启动，不绑定固定 cycle

## 输入

- `docs/process-management/roadmap.md`（含战略目标容量分配）
- priority 已定的 backlog 条目
- `docs/project-overview/strategic-goals.md`

## 输出

- 对话决策表（晋升 + 降级）
- `roadmap.md` 更新
- 条目 frontmatter 更新（`status`、`promoted_at` / `demoted_at`、`strategic_goal_id` 等）

## 安装

```bash
npx skills add nesnilnehc/ai-cortex --skill promote-roadmap-items
```

## 相关技能

- `prioritize-backlog` —— 上游：提供 priority 已定的 backlog 条目
- `define-roadmap` —— 上游结构依赖：定义 roadmap 和容量分配
- `design-strategic-goals` —— 上游依赖：提供战略目标
- `analyze-requirements` —— 下游：处理新晋升的 Now 项
- `plan-next` —— 信号源：大缺口通过 capture-work-items → prioritize-backlog → 本技能进入 Now

## 完整定义

参见 [SKILL.md](./SKILL.md)。
