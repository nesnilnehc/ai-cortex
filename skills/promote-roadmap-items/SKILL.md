---
name: promote-roadmap-items
description: Promote prioritized backlog items into the roadmap's Now/Next/Later tiers based on strategic_goal capacity allocation and priority scores. Event-driven (not calendar-driven).
description_zh: 把已评分的 backlog 条目按 strategic_goal 容量分配晋升进 roadmap 的 Now/Next/Later 槽位；事件驱动，不绑定固定周期。
tags: [workflow, automation, meta-skill]
version: 1.0.0
license: MIT
recommended_scope: project
cognitive_mode: interpretive
metadata:
  author: ai-cortex
triggers: [promote roadmap, roadmap planning, pull items, release planning]
input_schema:
  type: free-form
  description: Priority-scored backlog items, current roadmap, strategic_goal capacity allocation
output_schema:
  type: chat
  description: Promotion/demotion decisions for Now/Next/Later tiers + capacity usage report + updated roadmap.md
---

# 技能：晋升 Roadmap 条目（Promote Roadmap Items）

## 目的 (Purpose)

把已评分的 backlog 条目按战略目标容量分配晋升进 roadmap 的 Now / Next / Later 槽位。是 **roadmap planning ceremony** 的支撑技能，事件驱动。

---

## 核心目标（Core Objective）

**首要目标**：基于当前战略目标容量分配和 backlog 优先级，决定哪些条目晋升 / 降级 / 保持，更新 roadmap.md。

**成功标准**（必须全部满足）：

1. ✅ 读取 priority 已定的 backlog 条目（跳过 unset）
2. ✅ 计算当前 roadmap 各层（Now/Next/Later）容量使用与剩余
3. ✅ 按 strategic_goal 容量分配（来自 roadmap.md 或战略设置）呈现晋升候选
4. ✅ 用户确认每条晋升 / 降级决策
5. ✅ 更新 roadmap.md 和被晋升条目的 status 字段
6. ✅ 输出容量使用报告（各目标已用 / 总量 / 剩余）

**验收测试**：晋升后，读者能否从 roadmap.md 直接看到 Now 层每项来自哪个 strategic_goal、priority 为多少？

---

## 范围边界（Scope Boundaries）

**本技能负责**：

- Backlog → Roadmap 晋升 / 降级决策
- 按 strategic_goal 容量护栏控制
- 更新 roadmap.md 和被晋升条目状态

**本技能不负责**：

- 创建新 backlog 条目（`capture-work-items`）
- 为 backlog 条目评分（`prioritize-backlog`）
- 定义 roadmap 基础结构 / 里程碑（`define-roadmap`）
- 拆任务（`breakdown-tasks`）
- 需求分析（`analyze-requirements`）

**交接点**：晋升后的 Now 层条目按需进入 `analyze-requirements` → `breakdown-tasks` → 执行。

---

## 使用场景（Use Cases）

- **容量释出**：上一批 Now 层条目完成，释出容量，需要拉新条目进入
- **战略刷新**：战略目标调整后，重新评估 Now 层条目是否仍合适
- **大缺口补入**：`plan-next` 输出的大缺口被 capture + prioritize 后进入晋升决策
- **按需 planning**：用户主动启动 roadmap planning，不绑定固定 cycle

---

## 行为（Behavior）

### 阶段 0：读取输入

1. 读取 `docs/process-management/roadmap.md`（当前 Now / Next / Later 状态）
2. 读取 backlog 目录，筛选 `priority` 已定（非 unset）的条目
3. 读取 `docs/project-overview/strategic-goals.md`（战略目标列表）
4. 读取 roadmap.md 中声明的战略目标容量分配（见阶段 1）

**halt 条件**：
- roadmap.md 不存在 → 建议先 `define-roadmap`
- strategic-goals.md 不存在 → 建议先 `design-strategic-goals`
- 所有 backlog 条目均 `priority: unset` → 建议先 `prioritize-backlog`
- roadmap.md 中无容量分配 → halt，提示运行 `define-roadmap` 敲定容量

### 阶段 1：计算当前容量状态

对每个 strategic_goal：

| 字段 | 含义 |
|---|---|
| 分配容量 | roadmap.md 中该目标的百分比 × cycle 总容量 |
| 已用容量 | 当前 Now 层归属该目标的条目工作量之和 |
| 剩余容量 | 分配 - 已用 |

输出容量表：

```
## 当前容量使用

| Strategic Goal | 分配 | 已用 | 剩余 | 占比 |
| 目标 1（用户价值） | 6 人周 | 4 人周 | 2 人周 | 67% |
| 目标 2（市场扩张） | 2 人周 | 1 人周 | 1 人周 | 50% |
| 目标 3（工程健康） | 2 人周 | 0 人周 | 2 人周 | 0% |
```

### 阶段 2：生成晋升候选

对每个 strategic_goal：

1. 筛选该目标的 backlog 条目
2. 按 `priority` 排序（P0 > P1 > P2 > P3）
3. 按剩余容量从高优先级往下拉，直到填满该目标容量或无更多条目

输出晋升候选表：

```
## 晋升候选（Now 层）

| Goal | Item | Priority | Effort | 动作 |
| 目标 1 | #42 支付优化 | P0 | 2w | 晋升 Later → Now |
| 目标 3 | #17 技术债：auth 重构 | P1 | 2w | 晋升 Backlog → Now |
```

### 阶段 3：降级 / 拖延决策

对当前 Now 层条目检查：

- 若 priority 已降级（如战略变动后重评结果） → 建议降级到 Next 或 Later
- 若 strategic_goal 容量超配 → 建议最低 priority 条目降级

输出降级建议。

### 阶段 4：用户确认每项决策

呈现合并清单（晋升 + 降级），用户逐项确认：

```
## 待确认清单

[ ] #42 晋升 Later → Now？
[ ] #17 晋升 Backlog → Now？
[ ] #8 降级 Now → Next？（超配 + priority 低）
[ ] ...
```

### 阶段 5：持久化

对每项被确认的决策：

1. 更新条目 frontmatter 的 `status`（`captured` → `active` 进入 Now；`active` → `deferred` 降级）
2. 更新 roadmap.md，增加 / 移除对应条目引用
3. 写入 `promoted_at` / `demoted_at` 时间戳到条目 frontmatter

### 阶段 6：输出最终报告

- 晋升数 / 降级数 / 保持数
- 更新后容量使用
- 下一步建议（如 `analyze-requirements` 处理新晋升的 Now 项）

---

## 输入与输出 (Input & Output)

**输入**：roadmap.md + backlog（priority 已定）+ strategic-goals.md + 容量分配。

**输出**：对话决策表 + roadmap.md 更新 + 条目 frontmatter 更新（status + promoted_at / demoted_at）。

---

## 限制（Restrictions）

### 硬边界（Hard Boundaries）

- 不对 `priority: unset` 条目晋升（先走 `prioritize-backlog`）
- 不超出 strategic_goal 容量分配（超配时必须先降级再晋升）
- 不自动晋升 P3 条目到 Now（P3 默认进 Later）
- 不自动修改 roadmap 的 strategic_goal 容量分配（那是 `define-roadmap` 的职责）

### 技能边界

**不做（其他技能负责）**：

| 动作 | 归属 |
|---|---|
| 创建 backlog | `capture-work-items` |
| 评分 backlog | `prioritize-backlog` |
| 定义 roadmap 结构和容量 | `define-roadmap` |
| 拆分 Now 项为任务 | `breakdown-tasks` |
| 需求详细分析 | `analyze-requirements` |

---

## Anti-Patterns

- ❌ **不要绑定固定 cycle**（"每周一跑"）—— 本技能是**事件驱动**（容量释出 / 战略变动 / 按需）
- ❌ **不要忽略容量护栏** —— 不能因某目标有高 priority 条目就超配抢其他目标的容量
- ❌ **不要一次晋升太多** —— Now 层堆积超过 WIP 限制会破坏 pull-based 流
- ❌ **不要对 priority unset 条目操作** —— 强制先评分
- ❌ **不要修改 roadmap 结构**（如新增里程碑）—— 那是 `define-roadmap` 的事

---

## 自检（Self-Check）

- [ ] 读取 roadmap.md、backlog、strategic-goals.md 成功
- [ ] 容量分配存在；不存在时已 halt 并建议 `define-roadmap`
- [ ] 只处理 `priority` 已定的 backlog 条目
- [ ] 每个 strategic_goal 的容量使用已计算
- [ ] 晋升候选按 priority 排序 + 容量约束生成
- [ ] 降级建议考虑 priority 和容量超配
- [ ] 用户逐项确认，未自动批准
- [ ] roadmap.md 更新 + 条目 frontmatter 更新
- [ ] 输出最终容量使用报告

---

## 示例（Examples）

### 示例 1：容量释出触发晋升（主流场景）

**背景**：cycle 里 3 个 Now 项完成，释出 4 人周容量。strategic goals：目标 1（60%）、目标 2（20%）、目标 3 工程健康（20%）。

**流程**：

1. 计算容量 —— 目标 3 空余 2 周，目标 1 空余 2 周
2. 生成候选：
   - 目标 1：#42 支付优化（P0, 2w）→ 晋升 Later → Now
   - 目标 3：#17 auth 重构（P1, 2w）→ 晋升 Backlog → Now
3. 用户逐项确认（全部 yes）
4. 更新 roadmap.md + 条目 status 为 active
5. 容量报告：目标 1 6/6、目标 2 1/2、目标 3 2/2

**结果**：2 个条目晋升 Now；交接建议运行 `analyze-requirements` 处理新 Now 项。

### 示例 2：战略刷新导致大规模重评（边缘场景）

**背景**：季度战略刷新后，新战略目标 4 加入，目标 3 容量从 20% 调到 10%。

**流程**：

1. halt 并检测 —— roadmap.md 的容量分配未反映新战略
2. 提示："战略目标或容量有变，本技能无法处理结构变更。请先运行 `define-roadmap` 重新敲定容量分配。"
3. 用户运行 `define-roadmap` 后重来
4. 重入 promote-roadmap-items：发现目标 3 超配（Now 中 2w，新容量 1w），建议降级 #17 到 Next
5. 用户确认 → 更新

**结果**：roadmap 与战略重新一致；#17 降级但未丢失。

---

## 附录：输出契约

### 被晋升条目的 frontmatter 更新

```yaml
status: active               # 从 captured 或 deferred 进入
priority: P<N>               # 由 prioritize-backlog 写入
strategic_goal_id: goal-N
promoted_at: <ISO date>
promoted_to: now             # now | next | later
```

### 被降级条目的 frontmatter 更新

```yaml
status: deferred             # 从 active 降级
demoted_at: <ISO date>
demoted_from: now
demoted_to: next             # next | later | backlog
demotion_reason: capacity_overflow | strategy_change | priority_drop
```

### roadmap.md 更新

在 Now / Next / Later 对应章节中增删条目引用，格式由 `define-roadmap` 规定，本技能只增删不改结构。
