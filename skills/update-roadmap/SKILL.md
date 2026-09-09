---
name: update-roadmap
description: Day-to-day roadmap maintenance — change item status, shift dates with downstream impact analysis, and produce a what-changed summary. Does not move items between Now/Next/Later tiers.
description_zh: 路线图日常运维——改条目状态、挪期并计算下游影响、产出本次变更摘要；不改变条目所在的 Now/Next/Later 层级。
tags: [workflow, planning, maintenance]
version: 1.0.0
license: MIT
recommended_scope: project
cognitive_mode: interpretive
metadata:
  author: ai-cortex
triggers: [update roadmap, change status, at risk, blocked, shift dates, roadmap maintenance]
input_schema:
  type: free-form
  description: Current roadmap plus the intended status change or date shift; optional blocker details
output_schema:
  type: chat
  description: Updated roadmap.md and item frontmatter, downstream impact list, and a what-changed summary
---

# 技能：更新路线图（Update Roadmap）

## 目的 (Purpose)

路线图落地后的日常维护入口：改状态、挪期、说清这次改了什么。

`define-roadmap` 管从零建，`promote-roadmap-items` 管跨层晋升降级，两者之间还有一大块日常动作——某项开始做了、某项被卡住了、某项要往后推两周——本技能负责这一块。

---

## 核心目标（Core Objective）

**首要目标**：把一次路线图变更完整落地，并让读者看得出改了什么、为什么改、影响到谁。

**成功标准**（必须全部满足）：

1. ✅ 状态变更落到 roadmap.md 与条目 frontmatter 两处，不留单边更新
2. ✅ 改为 `at risk` 或 `blocked` 时，必须记录阻塞原因与缓解方案，缺一不写入
3. ✅ 挪期必须计算下游影响：列出因本次挪期而受影响的条目
4. ✅ 挪期后越过硬期限的条目被显式标出
5. ✅ 输出「本次变更了什么」摘要，含变更项、原因、影响面
6. ✅ 条目所在的 Now / Next / Later 层级保持不变

**验收测试**：变更之后，一个没参与这次讨论的人能否只看摘要就说清「改了什么、为什么、谁受影响」？

**交接点**：若本次变更实质上要求跨层调整（如某项已不该留在 Now），停止并交接 `promote-roadmap-items`。

---

## 范围边界（Scope Boundaries）

**本技能负责**：

- 条目状态变更（未开始 / 进行中 / 有风险 / 阻塞 / 已完成）
- 日期与时点调整，及其下游影响分析
- 本次变更摘要

**本技能不负责**：

- 跨层晋升 / 降级（`promote-roadmap-items`）
- 路线图结构变更：新增里程碑、改容量分配、改关键举措（`define-roadmap`）
- 新建条目（`capture-work-items`）
- 重新评分（`prioritize-backlog`）
- 依赖识别（`map-item-dependencies`）

**与 `promote-roadmap-items` 的分界**：**改变层级的归 promote，不改变层级的归本技能。** 把一个 Now 项推迟两周是本技能；把它挪到 Next 是 promote。判断标准是层级变没变，不是日期变没变。

---

## 使用场景（Use Cases）

- **进度同步**：某项开始了 / 完成了，状态要跟上
- **风险上报**：某项被卡住，需要记录阻塞原因与缓解方案
- **时点调整**：依赖滑期或范围变化，需要往后推并看清波及范围
- **变更沟通前**：需要一份「本次改了什么」供同步给干系人

---

## 行为（Behavior）

### 交互政策

- **默认**：读取项目规范路径下的 roadmap.md 与相关条目文件
- **必须追问**：改为 `at risk` / `blocked` 时，阻塞原因与缓解方案两项缺一不可，缺则不写入
- **确认后写入**：变更清单与下游影响先呈现，用户确认后才落盘

### 执行过程

1. **读取当前状态**：加载 roadmap.md 与涉及条目的 frontmatter。
2. **识别变更类型**：状态变更 / 挪期 / 两者兼有。
   - 若用户实际要的是跨层移动 → **停止**，说明这属于 `promote-roadmap-items` 的职责并交接。
3. **状态变更处理**：
   - 目标状态取自：未开始 / 进行中 / 有风险 / 阻塞 / 已完成
   - 改为**有风险**或**阻塞**时，追问两件事：卡在什么上（阻塞原因）、打算怎么办（缓解方案）。两者齐了才写入
   - 改为**已完成**时，检查该条目的成功指标是否达成；未达成而标完成的，要求用户说明
4. **挪期处理**：
   - 追问挪期原因（范围变化 / 依赖滑期 / 资源变化 / 其他）
   - **计算下游影响**：读取各条目的 `depends_on`，找出以本条目为前置的条目，逐个列出受影响时点
   - **标出硬期限越界**：挪期后越过合规、承诺、外部约束等硬期限的条目单独标红
   - 依赖数据缺失时（未跑过 `map-item-dependencies`），明确声明「下游影响未计算，因缺依赖数据」，不假装已分析
5. **呈现变更清单**：变更项 + 原因 + 下游影响 + 越界项，请用户确认。
6. **双写落盘**：roadmap.md 与条目 frontmatter 同步更新，不留单边。
7. **输出变更摘要**：见下方模板。

### 变更摘要模板

```markdown
## 本次路线图变更

**变更时间**：<ISO date>

| 条目 | 变更 | 原因 |
| #42 支付优化 | 进行中 → 阻塞 | 等第三方沙箱环境开通 |
| #63 移动端工作流 | 时点 +2 周 | 设计交付延后 |

**阻塞项与缓解方案**
- #42：已提工单，预计 3 个工作日；同时准备本地替身以便并行开发

**下游影响**
- #51 高级报表：前置 #42 推迟，本条目实际可开工时点顺延 2 周

**硬期限越界**
- 无

**未变更的**：层级维持不变（本技能不做跨层调整）
```

---

## 输入与输出 (Input & Output)

**输入**：当前 roadmap.md、目标变更意图、可选的阻塞详情。

**输出**：roadmap.md 与条目 frontmatter 更新 + 下游影响清单 + 本次变更摘要。

---

## 限制（Restrictions）

### 硬边界（Hard Boundaries）

- **不改变层级**：不得把条目在 Now / Next / Later 之间移动，那是 `promote-roadmap-items` 的职责
- **不改结构**：不新增里程碑、不动容量分配、不改关键举措
- **阻塞必须有下文**：`at risk` / `blocked` 缺阻塞原因或缓解方案时不写入
- **不单边更新**：roadmap.md 与条目 frontmatter 必须同步
- **依赖数据缺失时不得假装已分析下游影响**，须显式声明未计算及原因

### 反模式（避免）

- ❌ **静默改状态**：改了却不说为什么，下次没人记得当初发生了什么
- ❌ **挪期不看下游**：单条目往后推看似无害，实际会顺延一串
- ❌ **用挪期代替降级**：某项反复挪期说明它不该在 Now，应走 `promote-roadmap-items` 降级而不是一推再推
- ❌ **标完成不看指标**：成功指标未达成就标完成，等于让指标形同虚设
- ❌ **一次改一堆不留摘要**：变更摘要是给干系人看的，批量改动更需要它

### 技能边界（避免重叠）

| 动作 | 归属 |
|---|---|
| 跨层晋升 / 降级 | `promote-roadmap-items` |
| 新增里程碑 / 改容量 | `define-roadmap` |
| 新建条目 | `capture-work-items` |
| 重新评分 | `prioritize-backlog` |
| 依赖识别 | `map-item-dependencies` |
| 路线图健康体检 | `review-roadmap` |

---

## 自检（Self-Check）

- [ ] 变更类型已识别；属跨层移动的已交接 `promote-roadmap-items`
- [ ] `at risk` / `blocked` 变更均记录了阻塞原因与缓解方案
- [ ] 标为已完成的条目，其成功指标已核对
- [ ] 挪期已计算下游影响；依赖数据缺失时已显式声明未计算
- [ ] 硬期限越界项已单独标出
- [ ] 变更清单经用户确认后才落盘
- [ ] roadmap.md 与条目 frontmatter 双写完成
- [ ] 已输出本次变更摘要
- [ ] 条目层级未被改动

---

## 示例（Examples）

### 示例 1：条目被卡住（主流场景）

**背景**：#42 支付优化在 Now 层，进行中，突然卡在第三方沙箱环境上。

**流程**：

1. 识别为状态变更：进行中 → 阻塞。
2. 追问两项：卡在什么上（第三方沙箱未开通）、打算怎么办（已提工单，预计 3 个工作日；同时准备本地替身并行开发）。
3. 读 `depends_on`，发现 #51 高级报表以 #42 为前置 → 下游影响：#51 可开工时点顺延。
4. 无硬期限越界。
5. 用户确认 → roadmap.md 与 #42 的 frontmatter 双写。
6. 输出变更摘要。

**结果**：阻塞被记录且带缓解方案；#51 的顺延提前暴露，而不是等到它该开工时才发现。

### 示例 2：反复挪期应改为降级（边缘场景）

**背景**：#63 移动端工作流这是第三次要求往后推。

**流程**：

1. 识别为挪期，追问原因 → 「设计一直排不上」。
2. 检查历史：本 cycle 内该条目已挪期两次。
3. **提示用户**：一个条目在 Now 层反复挪期，说明它当前不具备被拉进 Now 的条件——继续挪期只会让 Now 层看起来满着但不动。
4. 建议改走 `promote-roadmap-items` 把它降级到 Next，释出容量给能推动的条目。
5. 用户接受 → **本技能停止**，交接 promote。

**结果**：没有用第三次挪期掩盖问题；层级调整交回了它该去的技能。

### 示例 3：依赖数据缺失（边缘场景）

**背景**：用户要把 #38 数据管道升级推迟 3 周，但项目从未跑过 `map-item-dependencies`，条目里没有 `depends_on`。

**流程**：

1. 识别为挪期，原因是资源被抽调。
2. 尝试计算下游影响 → 所有条目的 `depends_on` 均为空且非 `—`，无法区分「无依赖」与「未排查」。
3. **不假装已分析**。变更摘要中明确写：「下游影响未计算——项目尚未登记依赖数据」。
4. 建议先跑 `map-item-dependencies` 再决定这次挪期的幅度，同时给出用户可自行判断的提示：数据管道类条目通常有下游。
5. 用户选择先挪期、稍后补依赖 → 按其决定落盘，摘要保留未计算声明。

**结果**：变更照做，但「这次没算下游」被写在明面上，而不是让读者误以为已经评估过。
