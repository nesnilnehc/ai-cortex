---
name: map-item-dependencies
description: Identify dependencies among backlog and roadmap items across five categories, record them in each item's depends_on field, and produce a dependency graph with need-by dates and reduction options. Runs before promotion so blocked items are not pulled into Now.
description_zh: 识别 backlog 与 roadmap 条目间的五类依赖，写入条目 depends_on 字段，产出依赖图、需解决时点与削减建议；在晋升前运行，避免被阻塞条目被拉进 Now。
tags: [workflow, planning, dependencies]
version: 1.0.0
license: MIT
recommended_scope: project
cognitive_mode: interpretive
metadata:
  author: ai-cortex
triggers: [map dependencies, dependency graph, item dependencies, blocked by, sequencing]
input_schema:
  type: free-form
  description: Backlog items (any priority state) and current roadmap; optional scope limited to promotion candidates
output_schema:
  type: chat
  description: Dependency graph + need-by table + reduction options; depends_on written back to each item's frontmatter
---

# 技能：映射条目依赖（Map Item Dependencies）

## 目的 (Purpose)

找出 backlog 与 roadmap 条目之间的依赖关系，登记到条目上，让晋升决策知道哪些条目现在拉不动。

依赖是路线图上风险最高的一类因素：它不体现在优先级里，也不体现在容量里，但会让一个高优先级条目在进入 Now 之后原地卡住。

---

## 核心目标（Core Objective）

**首要目标**：为给定范围内的条目识别依赖、写回 `depends_on`，并输出可据以排序的依赖图。

**成功标准**（必须全部满足）：

1. ✅ 每个条目的依赖按五类逐一排查（技术 / 团队 / 外部 / 知识 / 顺序），无依赖时显式记为 `—`
2. ✅ 依赖图无环；发现环时 halt 并指出环路径，不自行打破
3. ✅ 每条依赖标注「需在何时前解决」与责任方
4. ✅ `depends_on` 写回条目 frontmatter，跨文档依赖以路径前缀标注
5. ✅ 对高风险依赖给出削减建议
6. ✅ 输出可直接被 `promote-roadmap-items` 消费的阻塞清单（哪些条目当前不可进 Now）

**验收测试**：拿到输出后，能否直接回答「这条目现在能不能进 Now，不能的话卡在谁身上」？

**交接点**：依赖登记完成后交接 `promote-roadmap-items` 执行晋升。

---

## 范围边界（Scope Boundaries）

**本技能负责**：

- 识别条目间依赖并分类
- 写回 `depends_on` 字段
- 产出依赖图、需解决时点、削减建议
- 输出阻塞清单

**本技能不负责**：

- 晋升 / 降级决策（`promote-roadmap-items`）
- 条目评分（`prioritize-backlog`）
- 创建条目（`capture-work-items`）
- 解决依赖本身（那是执行层的事，本技能只登记与提示）
- 任务级依赖拆解（由 AgentFabric 等 runtime 承接）

---

## 使用场景（Use Cases）

- **晋升前**：候选条目 ≥ 2 时，先跑本技能，避免把被阻塞条目拉进 Now
- **排期评审**：需要看清哪些条目必须串行、哪些可以并行
- **卡住时复盘**：Now 层条目迟迟不动，排查是否有未登记的前置

---

## 行为（Behavior）

### 交互政策

- **默认**：范围取当前晋升候选；用户可指定为全量 backlog 或指定条目集
- **推断与确认**：依赖关系优先从条目正文、`strategic_goal_id`、既有 roadmap 顺序中推断；推断出的依赖须经用户确认后才写回，不自动落盘
- **halt**：发现依赖环时停止并报告，由用户决定如何拆环

### 依赖五类

| 类别 | 含义 | 典型信号 |
|---|---|---|
| 技术 | 本条目需要另一条目产出的技术能力 | 「需要新的数据管道」「依赖 API 重构」 |
| 团队 | 需要另一团队交付物（设计、平台、数据） | 「等设计稿」「需平台组开权限」 |
| 外部 | 等供应商、合作方、第三方集成 | 「等对方接口上线」 |
| 知识 | 需先有调研或验证结论才能开工 | 「方案未定」「需先做 POC」 |
| 顺序 | 必须先交付 A 才能开始 B（共用代码或用户流程） | 「先上注册再上邀请」 |

### 执行过程

1. **确定范围**：默认取晋升候选；用户可指定全量或子集。
2. **逐类排查**：对范围内每个条目，按上表五类逐一提问，不跳类。无依赖的类别明确记为无，不留空。
3. **构图与查环**：把依赖关系构成有向图，检测是否有环。**有环立即 halt**，输出环路径，请用户决定拆哪条边——本技能不自行打破环。
4. **标注需解决时点与责任方**：每条依赖记「谁负责解决」与「需在何时前解决」。无责任方的依赖视为高风险，单独标出。
5. **给削减建议**：对高风险依赖逐条问四个问题——
   - 能否做一个简化版绕过这个依赖？
   - 能否用接口契约或替身并行推进？
   - 能否调整顺序，把依赖提前解决？
   - 能否把这部分工作吸收进本团队，去掉跨团队协调？
6. **确认后写回**：呈现依赖清单，用户确认后写入各条目 frontmatter 的 `depends_on`。
7. **输出阻塞清单**：列出当前存在未决前置的条目，供 `promote-roadmap-items` 作为 Now 层准入依据。

### `depends_on` 字段

```yaml
depends_on:
  - ref: <条目 ID 或 相对路径#锚点>
    kind: technical | team | external | knowledge | sequential
    need_by: <ISO date | 阶段名>
    owner: <责任方>
```

无依赖时写 `depends_on: —`，不留空——留空无法区分「没有依赖」与「还没排查」。

**字段语义来源**：沿用 [rules/task-quality.md](../../rules/task-quality.md) 对 `depends_on` 的既有约定（依赖图无环、无依赖填 `—`、跨文档依赖以路径前缀标注）。该 rule 原本约束的是 task，此处是把同一套语义借用到 backlog-item 上。

> **已知债务**：backlog-item 目前没有对应的 spec，结构只由 `capture-work-items` 的输出模板隐式定义。本技能是在一个无 spec 的制品上增加字段，属于语义借用。若 backlog-item 的字段继续增长，应补 `specs/backlog-item-modeling.md` 把结构收归 spec。此处仅记账，不代表已解决。

---

## 输入与输出 (Input & Output)

**输入**：backlog 条目（任意 priority 状态）+ 当前 roadmap；可选的范围限定。

**输出**：对话依赖图 + 需解决时点表 + 削减建议 + 阻塞清单；各条目 frontmatter 的 `depends_on` 被更新。

---

## 限制（Restrictions）

### 硬边界（Hard Boundaries）

- 发现依赖环时必须 halt，不得自行选边打破
- 推断出的依赖未经用户确认不得写回
- 不修改条目的 `priority` / `status` / 所在层级
- 不因为「看起来该有依赖」而编造依赖；无证据即记为无
- 无责任方的依赖必须显式标为高风险，不得静默略过

### 反模式（避免）

- ❌ **只查技术依赖**：团队与外部依赖才是最常拖垮排期的，不能只盯代码层
- ❌ **登记完就算完**：依赖登记的价值在于喂给晋升决策，不产出阻塞清单等于白做
- ❌ **把依赖当既定事实**：每条高风险依赖都要过一遍削减建议，先问能不能不依赖
- ❌ **留空代替「无依赖」**：留空会让下游无法区分「没有」与「没查」

### 技能边界（避免重叠）

| 动作 | 归属 |
|---|---|
| 晋升 / 降级 | `promote-roadmap-items` |
| 评分 | `prioritize-backlog` |
| 创建条目 | `capture-work-items` |
| 改状态 / 挪期 | `update-roadmap` |
| 任务级依赖 | AgentFabric runtime（不在 AI Cortex 范围） |

---

## 自检（Self-Check）

- [ ] 范围已与用户确认
- [ ] 每个条目按五类逐一排查，无依赖的类别已显式记为无
- [ ] 已做环检测；有环时已 halt 并输出环路径
- [ ] 每条依赖有 kind / need_by / owner；无 owner 的已标为高风险
- [ ] 高风险依赖已逐条过削减建议四问
- [ ] 依赖清单经用户确认后才写回 `depends_on`
- [ ] 已输出阻塞清单，可被 `promote-roadmap-items` 直接消费
- [ ] 未修改条目的 priority / status / 层级

---

## 示例（Examples）

### 示例 1：晋升前排查（主流场景）

**背景**：4 个晋升候选，准备进 Now。

**流程**：

1. 范围取这 4 条候选。
2. 逐类排查：
   - #42 支付优化 → 无依赖
   - #51 高级报表 → 技术依赖 #38 数据管道升级（在 backlog，未晋升）
   - #17 auth 重构 → 无依赖
   - #63 移动端工作流 → 团队依赖：等设计组交付稿，need_by 本阶段中点，owner 设计组
3. 构图无环。
4. 削减建议：#51 可否先做只读报表绕开管道升级 → 用户认为可行，记为备选方案。
5. 用户确认后写回 `depends_on`。
6. 阻塞清单：**#51 当前不可进 Now**（前置 #38 仍在 backlog）；#63 可进但需盯设计交付。

**结果**：晋升时 #51 改进 Next，避免了一个会在 Now 里卡住的条目。

### 示例 2：发现依赖环（边缘场景）

**背景**：三个条目互相引用——#12 说要等 #19 的接口，#19 说要等 #25 的鉴权模型，#25 又说要等 #12 的数据结构。

**流程**：

1. 构图时检测到环：`#12 → #19 → #25 → #12`。
2. **halt**，输出环路径与三条边各自的依据。
3. 说明本技能不自行拆环——拆哪条边是范围与设计决策，超出依赖登记的职责。
4. 提示两个常见拆法供用户判断：把某条边降级为「接口契约先行、实现后补」，或把三者合并为一个条目一次做完。
5. 用户决定把 `#25 → #12` 改为接口契约先行。
6. 重新构图无环，继续正常流程。

**结果**：环被用户显式拆掉并留下决策依据；技能没有替用户做范围决策。

### 示例 3：证据不足（边缘场景）

**背景**：条目正文只有一句「优化搜索」，看不出是否依赖别的条目。

**流程**：

1. 五类逐一排查，均无可依据的信号。
2. **不编造依赖**——不因为「搜索通常要依赖索引」就凭空加一条。
3. 记为 `depends_on: —`，并在报告中标注「该条目描述过简，依赖排查依据不足」。
4. 建议用户补充条目描述后重跑，或在晋升时人工确认。

**结果**：无依据处不臆造；同时把「查不动」这件事显式告诉用户，而不是静默记为无依赖。
