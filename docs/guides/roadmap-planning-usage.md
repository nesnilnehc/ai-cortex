---
artifact_type: guide
created_by: ai-cortex
lifecycle: living
created_at: 2026-09-09
status: active
---

# 路线图规划链路使用指南

面向使用者：从战略目标到条目进入 Now，这条链上有九个技能，本文说明什么时候用哪个、以及第一次用会撞上什么。

各技能的权威定义在各自的 `SKILL.md`，执行顺序与档位的权威定义在 [orchestrate-roadmap-planning](../../skills/orchestrate-roadmap-planning/SKILL.md)。本文不复述这些，只讲怎么进门。

---

## 1. 绝大多数情况：一句话

```text
/orchestrate-roadmap-planning
```

它先做体检，判断当前卡在哪一环，再只执行需要执行的步骤，跳过的会在报告里说明原因。**不需要自己判断该调哪个技能**——这正是它存在的理由。

也可以不用斜杠命令，直接说「跑一轮路线图规划」。

---

## 2. 按状态找入口

明确知道自己要干什么时，直接点名单个技能更快。

| 你的处境 | 用哪个 |
| :--- | :--- |
| 想知道这份路线图有什么问题 | [`review-roadmap`](../../skills/review-roadmap/SKILL.md) |
| 战略目标还没有 | [`design-strategic-goals`](../../skills/design-strategic-goals/SKILL.md) |
| 要从战略目标建一份路线图 | [`define-roadmap`](../../skills/define-roadmap/SKILL.md) |
| 有个需求 / 缺陷要记下来 | [`capture-work-items`](../../skills/capture-work-items/SKILL.md) |
| 积压该重排优先级了 | [`prioritize-backlog`](../../skills/prioritize-backlog/SKILL.md) |
| 想搞清楚条目之间谁卡谁 | [`map-item-dependencies`](../../skills/map-item-dependencies/SKILL.md) |
| 要把条目拉进 Now | [`promote-roadmap-items`](../../skills/promote-roadmap-items/SKILL.md) |
| 某项卡住了 / 要挪期 | [`update-roadmap`](../../skills/update-roadmap/SKILL.md) |
| 里程碑做完了要归档 | [`archive-milestone`](../../skills/archive-milestone/SKILL.md) |

用白话描述也能匹配上——匹配规则见 [AGENTS.md](../../AGENTS.md) §4，各技能的 `triggers` 字段就是为此准备的。

---

## 3. 两个会挡住你的地方

这两个都是设计如此，不是故障。

### 3.1 晋升时说「缺容量分配」

`promote-roadmap-items` 的容量公式是「该目标的百分比 × 总容量基线」。这两个数都不在，它会停下来让你先跑 `define-roadmap`。

**为什么不自动填**：容量分配是资源承诺，技能不允许替你推断。`define-roadmap` 会问你两件事——

1. **总容量基线**：工程师人数 × 周期时长 − 已知开销（会议、oncall、假期），按有效工时 60–70% 折算。未规划工作的缓冲在这一步就让出去了，所以后面的百分比是相对于有效容量，不是日历容量。
2. **各战略目标的百分比**：之和必须为 100%，且工程健康类目标不得为 0%——这类工作没有战略代言，在价值竞争里永远排不进容量。

### 3.2 治理文档全空时不会从零盘问你

新项目跑 `design-strategic-goals`，如果愿景与北极星都还没有，它不会一条条问你要答案，而是从仓库实证反推候选目标：README 与 AGENTS.md 看意图，CHANGELOG 与 git log 看实际投入方向，代码结构看能力边界，backlog 看未满足的需要。

**但产出会被明确标记**：每条候选目标都附指向具体文件的推断依据，推不出依据的不写；未经你逐条确认不落盘；文档头部留「缺上游背书、属临时锚」的标记。补齐愿景与北极星后应当重跑。

理由很直接——实证反推出来的目标读着会很顺、很自洽，恰恰因此最容易是脑补在填空。挂上依据、要你确认，是为了让你能当场证伪。

---

## 4. 依赖为什么要在晋升之前排

`map-item-dependencies` 排在 `promote-roadmap-items` 前面，是整条链顺序上最关键的一处。

优先级高不代表现在拉得动。一个 P0 条目如果前置还躺在 backlog 里，晋升进 Now 之后就是占着容量不产出，而容量报告看起来是满的。所以 Now 层准入有两个条件：排名靠前，**且**无未决前置依赖。

条目没登记过依赖时，`promote-roadmap-items` 不会静默放行，会提示先跑依赖登记；你坚持继续的话，候选表里会标「依赖未排查」。

---

## 5. 判据在哪

路线图该长什么样、哪些算问题，判据统一在 [rules/roadmap-quality.md](../../rules/roadmap-quality.md)。生产侧（`define-roadmap`）、诊断侧（`plan-next`）、评审侧（`review-roadmap`）都引用同一份，改判据改那里，不改技能。

---

## 6. 与 plan-next 的区别

两个都能告诉你「下一步做什么」，但覆盖面不同：

- [`plan-next`](../../skills/plan-next/SKILL.md) 回答「整个项目下一步该干什么」，跨使命到任务全层，只读不执行。
- `orchestrate-roadmap-planning` 回答「路线图这条线，从战略到晋升一次走完」，只管这一条纵切片，会实际执行。

治理层面不确定该往哪走时先跑 `plan-next`；确定要推进路线图时用 `orchestrate-roadmap-planning`。
