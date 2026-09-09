---
name: orchestrate-roadmap-planning
description: Orchestrator skill — run one roadmap planning pass by sequencing atomic skills from strategic goals through capture, scoring, dependency mapping, and promotion, satisfying each skill's halt conditions up front.
description_zh: 编排技能——按固定顺序串联从战略目标到晋升的原子技能，跑完一轮 roadmap planning；核心价值是提前满足各原子技能的 halt 条件。
tags: [planning, orchestration]
version: 1.0.0
license: MIT
recommended_scope: project
metadata:
  author: ai-cortex
triggers: [roadmap planning, plan the roadmap, roadmap ceremony, orchestrate roadmap]
input_schema:
  type: free-form
  description: Optional scope hint and any unregistered raw input; auto-discovers governance docs from project norms
output_schema:
  type: chat
  description: Aggregated report — steps executed, steps skipped with reasons, roadmap changes, capacity usage, and next actions
---

# 编排技能：路线图规划（Orchestrate Roadmap Planning）

## 目的 (Purpose)

按固定顺序串联路线图相关的原子技能，跑完一轮 roadmap planning ceremony。本技能仅做编排，不执行任何领域分析。单步操作请直接调用对应原子技能（只想晋升用 `promote-roadmap-items`、只想体检用 `review-roadmap`）。

**存在价值是提前满足下游的 halt 条件。** 手工调用时最常见的浪费是：一路做到 `promote-roadmap-items` 才发现 roadmap 缺容量分配，halt，回头跑 `define-roadmap`，再重来一遍——这个回退在 promote 的示例 2 里被当成正常流程写着。本技能把这类前置条件在调用前就检查并补齐。

---

## 编排职责（Orchestrator Role）

按命名规范，编排技能**只做 4 件事**：

1. **检测上下文**：调用步骤 0 取得 findings，从中机械推导 mode 与各步执行条件
2. **串联调用**：按固定顺序执行原子技能
3. **halt-on-failure**：按档位决定失败语义（见下）
4. **聚合输出**：合并各步产出为单一报告

**严禁**：在本技能内评估路线图质量、计算容量、判定依赖、决定优先级，或为任一原子技能重复实现其逻辑。

---

## 执行顺序（固定）

每步标注档位——**必选**条件命中即执行且不可跳过，**默认**条件命中即执行但用户可显式跳过，**推荐**只提示不自动执行。

| 步 | 类型 | 原子技能 | 档位 | 执行条件 |
|---|---|---|---|---|
| 0 | 体检 | `review-roadmap` | 必选 | 总是执行。只读无副作用，其 findings 是后续所有条件判定的输入 |
| 1 | 上游 | `design-strategic-goals` | 必选 | `strategic-goals.md` 不存在 |
| 2 | 结构 | `define-roadmap` | 必选 | 无 roadmap.md / 缺总容量基线 / 缺容量分配 / 百分比之和 ≠ 100% |
| 3 | 进件 | `capture-work-items` | 默认 | 有未登记的原始输入 |
| 4 | 评分 | `prioritize-backlog` | 全部 unset 必选；部分 unset 默认 | 存在 `priority: unset` 条目 |
| 5 | 依赖 | `map-item-dependencies` | 默认 | 晋升候选 ≥ 2 |
| 6 | 晋升 | `promote-roadmap-items` | 必选 | 总是执行；无候选时也要输出容量使用报告 |
| 7 | 运维 | `update-roadmap` | 推荐 | 用户有明确的状态变更 / 挪期意图 |
| 8 | 归档 | `archive-milestone` | 推荐 | 存在已完成且成熟度达标的里程碑 |

无匹配的步骤跳过；最终报告标注哪些步骤跳过及原因。

**档位不可随意调整**。三档是各原子技能既有约束的机械映射，不是本技能的领域判断：

- 步骤 1、2 为必选，因为 `strategic-goals.md` 缺失、roadmap.md 缺失、容量分配缺失都是 `promote-roadmap-items` 明写的 halt 条件，不补则整条链走不到底
- 步骤 4 的双档位对应 promote 的两种行为：它对「全部 unset」halt，对「部分 unset」只是跳过那些条目
- 步骤 5 为默认而非必选，因为候选 < 2 时依赖分析无意义
- 步骤 8 为推荐，因为 `archive-milestone` 会移除目录，属破坏性操作，其自身 `apply` 默认即为 `false`（dry-run）

**步骤 5 必须在步骤 6 之前**，这是本编排存在的核心理由之一：promote 的 Now 层准入要读 `depends_on`，依赖没登记就晋升，会把被阻塞的条目拉进 Now 占着容量不产出。

---

## 行为 (Behavior)

### 步骤 1：检测上下文

执行 `review-roadmap` 取得 findings，按下表机械映射出 mode。多个特征同时命中时取表中靠前者，因为靠前的 mode 对应更上游的缺口。

| mode | findings 特征 | 影响 |
|---|---|---|
| `bootstrap` | roadmap.md 或 strategic-goals.md 缺失 | 步骤 1、2 必然执行 |
| `refresh` | 缺容量基线 / 缺容量分配 / 百分比之和 ≠ 100% / 战略目标与 roadmap 不一致 | 步骤 2 必然执行；步骤 6 需先处理超配 |
| `intake` | 存在未晋升的已评分条目，且有剩余容量 | 主路径 3→4→5→6 |
| `maintain` | 无容量缺口，但存在有风险 / 阻塞 / 逾期条目 | 步骤 7 由推荐升为默认提示 |
| `healthy` | 无上述任何 findings | 输出体检报告后正常结束，不执行任何写操作 |

`review-roadmap` 本身不输出 mode——它只出 findings，映射在本层完成。

### 步骤 2：串联调用

按上表顺序依次调用，每步收集其产出。调用前把该步的前置条件核对一遍，能补的先补，避免下游 halt 后回退。

**步骤 8 的 `milestone_slug`**：`archive-milestone` 的输入是 structured，必填 `milestone_slug`，本层必须提供。取值来源是扫描 `docs/process-management/milestones/` 下非 `_archive/` 的目录，与 roadmap.md 中已完成阶段比对。存在多个候选时逐一提示，不批量归档；无法确定时跳过该步并在报告中说明，**不猜测 slug**。

### 步骤 3：halt-on-failure

档位决定失败语义。这是相对 `orchestrate-code-review` 单一 halt 规则的一处有意偏离——那里各原子技能彼此独立，这里步骤之间存在数据依赖，一刀切会让本可继续的流程提前中断：

| 档位 | 失败时 |
|---|---|
| 必选 | 终止编排，输出已完成部分与失败说明 |
| 默认 | 记录后继续。若后续步骤依赖其产出（如步骤 5 之于步骤 6 的依赖护栏），该后续步骤降级为推荐，并在报告中声明护栏未生效 |
| 推荐 | 未执行不计为失败 |

**步骤 1 的特殊 halt**：若用户拒绝 `design-strategic-goals` 降级模式给出的候选目标，本层不逐层回退去补愿景 / 北极星——那是 `plan-next` 目标树遍历的职责。halt 并提示先跑 `plan-next` 建立战略层。

### 步骤 4：聚合输出

单一报告，含：

- 各步执行结果摘要
- 跳过的步骤及原因
- roadmap 变更清单（新增 / 晋升 / 降级 / 状态变更）
- 容量使用报告（取自步骤 6）
- 未解决的 findings（步骤 0 中本轮未被处理的）
- 下一步建议

---

## 输入与输出

**输入**：可选的范围提示与未登记的原始输入；治理文档路径按项目规范自动发现。

**输出**：单一聚合报告（见上）。

---

## 限制 (Restrictions)

### 硬边界

- 不在本技能内评估路线图质量、计算容量、判定依赖或决定优先级
- 不改变执行顺序，尤其不得把步骤 5 放到步骤 6 之后
- 不调整档位；档位由各原子技能的既有约束决定
- 不代替用户确认：各原子技能要求的逐项确认照常进行，编排层不批量代批
- 不反向调用 `plan-next` 或 `orchestrate-governance-step`，避免调用环
- 不重新实现 `plan-next` 的目标树遍历

### 与既有编排层的正交边界

| 技能 | 覆盖面 | 行为 | 关系 |
|---|---|---|---|
| `plan-next` | 跨层，只读 | 目标树遍历出路由建议 | 本技能不得重新实现遍历；可只读取用其状态 |
| `orchestrate-governance-step` | 跨层，执行 1 条建议 | 通用单步执行器 | 可将本技能当作一条可执行动作调用 |
| `orchestrate-roadmap-planning` | 仅路线图纵切片 | 固定序列一次走完 | 不得反向调用上述两者 |

一句话区分：`plan-next` 回答「整个项目下一步该干什么」，本技能回答「路线图这条线，从战略到晋升一次走完」。

### 技能边界

**编排技能内不做**（由原子子技能承接）：路线图评估 → `review-roadmap`；结构定义 → `define-roadmap`；评分 → `prioritize-backlog`；依赖 → `map-item-dependencies`；晋升 → `promote-roadmap-items`；状态与时点 → `update-roadmap`；归档 → `archive-milestone`。

---

## 自检

- [ ] 仅做「检测上下文 / 串联调用 / halt-on-failure / 聚合输出」4 件事
- [ ] 未在本技能内实现任何领域判断逻辑
- [ ] mode 由步骤 0 的 findings 机械映射得出，未自行评估路线图
- [ ] 执行顺序固定，步骤 5 在步骤 6 之前
- [ ] 跳过步骤已在报告中注明原因
- [ ] 失败语义按档位处理；默认步骤失败时已声明下游护栏是否失效
- [ ] 步骤 8 的 `milestone_slug` 有明确来源，未猜测
- [ ] 报告含容量使用与未解决 findings

---

## 示例

### 示例 1：容量释出后拉新条目（主流场景）

- **上下文**：`review-roadmap` findings 显示结构完整、容量分配齐全，但有 3 条已评分条目未晋升且 Now 层有剩余容量 → mode = `intake`
- **调度**：步骤 0 → 跳过 1、2（治理文档齐全）→ 跳过 3（无未登记输入）→ 跳过 4（无 unset 条目）→ 步骤 5（候选 3 条 ≥ 2）→ 步骤 6 → 跳过 7、8
- **步骤 5 产出**：1 条候选存在未决前置，被标为不可进 Now
- **步骤 6**：另 2 条晋升 Now，被阻塞那条进 Next
- **聚合**：容量报告 + 变更清单 + 建议对新晋升的 Now 项跑 `capture-work-items`

### 示例 2：新项目冷启动（边缘场景）

- **上下文**：`docs/` 下除 README 外为空 → findings 显示 roadmap.md 与 strategic-goals.md 均缺失 → mode = `bootstrap`
- **调度**：步骤 0 → 步骤 1（`design-strategic-goals` 检测到愿景与北极星也缺失，自行转入降级模式，从仓库实证反推候选目标）→ 步骤 2 → 步骤 3 → 步骤 4 → 跳过 5（候选 < 2）→ 步骤 6
- **关键点**：编排层**不**因为愿景缺失就去调 `define-vision`。上游是否齐备、走正常还是降级模式，由 `design-strategic-goals` 自己判断
- **若用户拒绝降级候选**：halt，提示先跑 `plan-next` 建立战略层，输出已完成的步骤 0 体检报告

### 示例 3：依赖步骤失败后的降级（边缘场景）

- **上下文**：mode = `intake`，5 条晋升候选
- **步骤 5 失败**：`map-item-dependencies` 检测到依赖环并 halt
- **处理**：步骤 5 是**默认**档位，不终止整条编排；记录失败后继续
- **步骤 6 降级**：promote 的 Now 层依赖护栏因缺 `depends_on` 数据而无法生效，该步由必选降为推荐，执行前明确告知用户「本轮依赖护栏未生效，晋升到 Now 的条目未经依赖检查」
- **聚合报告**：显式列出「步骤 5 失败：存在依赖环 `#12 → #19 → #25 → #12`；步骤 6 的依赖护栏未生效」，并建议先拆环再重跑
