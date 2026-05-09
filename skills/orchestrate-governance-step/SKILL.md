---
name: orchestrate-governance-step
description: Single-step governance executor — reads plan-next routing output, executes the highest-priority action, and emits a continuation signal for /loop-driven autopilot.
description_zh: 单步治理执行器——读取 plan-next 路由输出，执行最高优先级动作，发出继续信号以支持 /loop 全自动推进。
tags: [automation, workflow, meta-skill]
version: 2.0.0
license: MIT
recommended_scope: project
metadata:
  author: ai-cortex
triggers: [auto iterate, iterate governance, autopilot, governance loop, auto-advance]
input_schema:
  type: free-form
  description: Optional governance docs root; auto-discovers defaults same as plan-next.
  defaults:
    docs_root: auto
output_schema:
  type: diagnostic-report
  description: "IterationStepReport: action taken, skill invoked, outcome, continuation_signal (advance | done | blocked | stalled | error)."
---

# 技能：自动迭代（orchestrate-governance-step）

> **角色**：单步治理执行器——plan-next 的配对执行层
> **WHAT**：每次调用执行 1 条 plan-next 路由建议，发出 `continuation_signal` 供 `/loop` 驱动迭代推进
> **HOW**：内部调用 plan-next → 取最高优先级卡片 → 人工闸门判断 → 执行子技能 → 执行后验证 → 输出报告
> **区别**：不同于 `plan-next`（只读诊断，不执行）；不同于 `/loop`（只调度，不执行业务逻辑）；不同于 `orchestrate-repair-loop`（修复代码缺陷，不推进治理层）

---

## 目的

将 plan-next 的路由建议转化为一次可执行的治理动作，使全自动 autopilot（`/loop /orchestrate-governance-step`）成为可能。

plan-next 只能诊断和建议；用户需手动执行每条建议。orchestrate-governance-step 填补这一执行缺口，配合 `/loop` 实现三层正交自动化：

| 层 | 技能 | 职责 |
|---|---|---|
| 调度 | `/loop` | 每 N 分钟触发一次 |
| **驱动** | **orchestrate-governance-step** | 读路由 → 执行 1 步 → 报告 |
| 诊断 | `plan-next` | 盘点 + 识别缺口 + 路由建议（只读） |

---

## 核心目标

**首要目标**：每次调用执行恰好 1 条治理动作，并通过 IterationStepReport 明确告知执行结果和是否继续。

**成功标准**（须全部满足）：

1. ✅ **单步执行**：每次调用执行且仅执行 1 条路由动作
2. ✅ **卡死检测**：同一路由卡片指纹在 session 内连续 2 次出现且目标未推进，触发 `stalled` 信号
3. ✅ **执行后验证**：执行子技能后重跑 plan-next，确认目标卡片是否已消失
4. ✅ **人工闸门**：战略创意类技能（define-mission、design-strategic-goals 等）执行前必须暂停并告知用户
5. ✅ **明确继续信号**：每次调用必须在 IterationStepReport 中输出 `continuation_signal` 五值之一

**验收测试**：执行完成后，IterationStepReport 是否清晰说明了执行了什么、结果如何、以及下一步是继续还是需要人工介入？

---

## 范围边界

**本技能负责**：
- 内部调用 plan-next 获取路由
- 从"现在该做"选取最高优先级卡片（`紧急` > `重要` > `缓`）
- 卡死检测（session 内指纹对比）
- 人工闸门判断
- 执行 1 条子技能
- 执行后轻量验证
- 输出 IterationStepReport

**本技能不负责**：
- 治理诊断与路由生成 → `plan-next`
- 循环调度 → `/loop`（Claude Code 内置）
- 代码缺陷修复循环 → `orchestrate-repair-loop`
- 战略创意决策内容（使命、愿景、战略目标内容）→ 需要人工

**转交点**：
- `continuation_signal: done` → 治理就绪，告知用户，停止
- `continuation_signal: blocked | stalled | error` → 需人工介入，停止并说明原因

---

## 使用场景

- "继续推进治理，直到完成" → `/loop /orchestrate-governance-step`
- "执行下一条治理动作" → `/orchestrate-governance-step`
- "全自动 autopilot，每 30 分钟推进一次" → `/loop /orchestrate-governance-step 30m`
- "只查看下一步会执行什么（不执行）" → 使用 `/plan-next`

---

## 行为

### 步骤 0：前置检查

读取治理文档路径（默认同 plan-next 的 `docs_root`，或调用方显式提供）。

### 步骤 1：调用 plan-next

内部调用 `/plan-next`，捕获路由输出。若调用方提供了 `pre_run_output`，直接使用，跳过此步。

记录**目标卡片指纹**（用于卡死检测）：

```
指纹 = 主题字段 + "||" + 治理上下文字段
```

### 步骤 2：解析路由

从"现在该做"取最高优先级 1 条（`紧急` → `重要` → `缓` → `待执行`）。

**三态判定**（不要把"等执行"误认为"已完成"）：

| plan-next 输出 | continuation_signal | 含义 |
|---|---|---|
| 有路由卡片（紧急/重要/缓） | 进入步骤 3 继续 | 治理有缺口，可执行子技能 |
| 仅含「待执行」卡片（任务已拆分等开发） | `blocked` | 治理就绪、等外部执行 |
| 完全为空（所有目标 status=done 且 L1 KPI 已达成） | `done` | 治理 + 验收双重达成 |

**关键约束**：
- 「现在该做」为空 ≠ done。必须先确认 plan-next 是否在 L1 验收 KPI 检查 + L5 待执行分支后判定
- 若 plan-next 输出未含 L1 验收 KPI 状态字段 → 视为 plan-next 调用不合规，输出 `error` + 提示升级 plan-next
- 战略目标 `status = approved` 但验收未达成 → plan-next 必然返回路由（建立 KPI 或待执行卡片），不应空

### 步骤 3：卡死检测

将本次指纹与 session 内**上次执行的指纹**对比：

- **相同** → `continuation_signal: stalled`，说明"上次执行后目标卡片未推进"，停止
- **不同（或首次调用）** → 继续

### 步骤 4：人工闸门

以下情形必须暂停，输出说明，设置 `continuation_signal: blocked`：

- 推荐技能属于创意/战略类：`define-mission`、`design-strategic-goals`、`define-vision`、`define-north-star`、`define-strategic-pillars`
- 路由卡片完成标志含"受阻时回 plan-next 重评"且当前已触发
- **路由卡片标签为 `待执行`**：治理就绪、需外部开发执行，无治理技能可调用
- **首条路由是建立 L1 验收 KPI 数据源**且推荐技能属设计/架构类：需人工确认监控方案，不自动执行

### 步骤 5：执行

调用路由卡片中的"推荐技能"命令（格式：`/skill-name [聚焦点]`）。

执行失败且无恢复路径 → `continuation_signal: error`，输出报告，停止。

### 步骤 6：执行后验证

**强制重跑** `/plan-next`（不可跳过），检查目标卡片是否已从"现在该做"消失。
`done` 信号的唯一合法来源是本步骤的验证结果——禁止以模型自行推断替代。

| 结果 | 行动 |
|---|---|
| 卡片消失，"现在该做"仍有条目 | `continuation_signal: advance` |
| 卡片消失，"现在该做"为空 | `continuation_signal: done` |
| 卡片仍存在 | 更新卡死计数器；若计数达 2 → `continuation_signal: stalled` |

### 步骤 7：输出 IterationStepReport

---

## 与 /loop 交互模式（重要）

`/loop` 有两种模式，对 `continuation_signal` 的消费方式完全不同：

| /loop 模式 | 触发方式 | 信号消费 | 推荐用法 |
|---|---|---|---|
| **Dynamic** | 无 interval（自调度 ScheduleWakeup） | 读 `continuation_signal`：done/blocked/stalled/error 会停止循环 | ✅ **推荐**：`/loop /orchestrate-governance-step`（不带 interval） |
| **Fixed-interval (cron)** | 有 interval（如 `5m`） | **不读** `continuation_signal`：cron 持续触发，信号被忽略 | ⚠️ 不推荐自动停止场景；用户须手动 CronDelete |

**强制行为**：
- 检测到 fixed-interval cron 模式（通过会话上下文中存在 CronCreate 记录的 prompt=`/orchestrate-governance-step`），首条 IterationStepReport 必须警示用户：「当前为 cron 模式，信号被忽略；如不希望持续触发请改用 dynamic /loop 或在收到 stalled/blocked/done 后 CronDelete」
- `stalled` 信号在第 2 次连续出现时，IterationStepReport 须明示「**强烈建议立即 CronDelete <job-id>**」并提供 job ID

**解决方案**：用户希望「治理就绪后自动停」时，应使用 `/loop /orchestrate-governance-step`（无 interval，dynamic 模式），不要用 `/loop 1m /orchestrate-governance-step`。

---

## 输入与输出

### 输入

| 参数 | 必选 | 默认 | 说明 |
|---|---|---|---|
| `docs_root` | 否 | auto | 治理文档根目录；auto 同 plan-next 默认路径 |
| `pre_run_output` | 否 | — | 预运行的 plan-next 输出；提供时跳过内部调用 |

### 输出：IterationStepReport

```
## 这次自动推进做了什么

- **做了什么**：[用文件名/功能名说明；禁用"路由卡片""治理层级"等词]
- **为什么要修**：[发现了什么具体问题；首次新建文件时省略]
- **改了什么**（有文件变更时）：
  - 修改前：...
  - 修改后：...
- **结果**：成功 ✅ | 需要你来决定 ⚠️ | 出错了 ❌
- **下一步**：继续自动推进 | 全部完成，无需继续 | 需要你决定：[说明] | 卡住了：[说明]
- _（内部）继续信号：advance | done | blocked | stalled | error_
```

### continuation_signal 语义

| 值 | 含义 | /loop 行为 |
|---|---|---|
| `advance` | 动作已完成，治理还有工作 | 继续触发下次 |
| `done` | 步骤 6 重跑 plan-next 后"现在该做"为空；**禁止基于模型自行推断输出此值** | 停止循环 |
| `blocked` | 需要人工决策或外部依赖 | 停止循环，等用户介入 |
| `stalled` | 同一路由卡片连续 2 次无进展 | 停止循环，报告卡死原因 |
| `error` | 子技能执行失败且无恢复路径 | 停止循环，报告错误 |

---

## 限制

### 硬边界（Hard Boundaries）

**Rule 1**：每次调用 MUST NOT 执行超过 1 条动作
- 验证：IterationStepReport 中 `调用技能` 字段只有 1 条
- 后果：REJECT（破坏三层模型的单步语义）

**Rule 2**：战略创意类技能 MUST 触发人工闸门，不得直接执行
- 验证：推荐技能为 define-mission 等时，报告显示 `blocked`
- 后果：REJECT（战略决策不应被自动化）

**Rule 3**：每次调用 MUST 输出合法的 `continuation_signal`
- 验证：IterationStepReport 含 `继续信号` 字段且值在五值枚举内
- 后果：REJECT（/loop 依赖此信号决定是否继续）

**Rule 4**：`done` 信号 MUST 来自步骤 6 plan-next 重跑结果，MUST NOT 来自模型自行推断
- 验证：IterationStepReport 备注中不出现"治理层全部就绪"、"当前可执行的…均已创建"等自我评估语言；`done` 仅在步骤 6 确认"现在该做"为空后输出
- 后果：REJECT（模型替代 plan-next 做了路由判断，破坏三层模型的职责边界）

**Rule 5**：`done` MUST 满足「plan-next 输出含 L1 验收 KPI 已达成」声明 AND「现在该做为空」AND「无待执行卡片」三者同时满足
- 验证：IterationStepReport 在输出 `done` 时引用了 plan-next 治理上下文中的 KPI 状态字段（如「引用可见率 85% ≥ 80%（达成）」）；只要 KPI 未达成或数据缺失或含「待执行」卡片，一律不得输出 `done`
- 后果：REJECT（误把"战略目标 status=approved"当成验收达成，导致 /loop 在不该停时停）

**Rule 6**：检测到「待执行」标签卡片 MUST 输出 `blocked`，MUST NOT 尝试执行或 done
- 验证：IterationStepReport 中 selected_skill 为空或为 N/A，next_step 含「治理就绪、待外部执行」字样
- 后果：REJECT

### 技能边界（Skill Boundaries）

**不做以下事项**（其他技能负责）：
- **治理诊断与路由** → `plan-next`
- **循环调度** → `/loop`
- **代码修复循环** → `orchestrate-repair-loop`
- **文档健康检测** → AgentFabric runtime + linter / CI 工具（按 `rules/doc-health-criteria.md`）

---

## 反模式

### ✅ 正确：单步执行 + 后验证 + 继续信号

```
1. plan-next → 2 条路由：capture-work-items（缓）、prioritize-backlog（缓）
2. 取最高优先级：capture-work-items
3. 人工闸门：非创意类 → 继续
4. 执行 /capture-work-items
5. 重跑 plan-next → capture-work-items 卡片消失
6. 报告 continuation_signal: advance
```

**为什么正确**：单步执行保持三层模型正交性；后验证确认真实推进；/loop 自然驱动下一步。

---

### ❌ 错误：一次执行两条路由

```
1. plan-next → 2 条路由
2. orchestrate-governance-step 执行 capture-work-items AND prioritize-backlog
```

**问题分析**：违反单步语义；若第二条失败，难以确定回滚范围；破坏 /loop 的粒度控制。

---

### ❌ 错误：绕过人工闸门

```
1. plan-next 路由：/design-strategic-goals
2. orchestrate-governance-step 直接执行，不暂停
```

**问题分析**：战略目标内容需要人工判断；自动执行产出低质量战略文档，且用户无感知。

---

### ❌ 错误：跳过执行后验证直接报告 advance

```
1. 执行 /capture-work-items 完成
2. 直接报告 continuation_signal: advance
3. 实际上文件未成功写入
```

**问题分析**：缺少后验证导致虚假 advance；下次 plan-next 仍给出同一路由，触发 stalled。

---

### ❌ 错误：自行判断"治理完成"替代步骤 6 重跑 plan-next

```
1. 执行子技能成功
2. 模型推断"当前可执行的治理文档均已创建，其余依赖开发者执行层"
3. 直接输出 continuation_signal: done，未重跑 plan-next
```

**问题分析**：模型把"治理层 vs 开发者执行层"的判断权抢走了——这是 plan-next 的职责，不是 orchestrate-governance-step 的。blocked 节点（如 T48/T52 依赖 T47/T49）应由 plan-next 路由并触发 `blocked` 信号，而不是由模型自行宣布"治理完成"。`done` 只有一个合法来源：步骤 6 重跑 plan-next 后"现在该做"为空。

---

### ❌ 错误：把 `战略目标 status=approved` 当成验收已达成 → 输出 done

```
1. plan-next: G1 status=approved，验收 KPI「引用可见率」无监控数据
2. orchestrate-governance-step 取空"现在该做"（plan-next 实际应返回路由，但此例假定 plan-next 也漏判）
3. 输出 done，/loop 停止
4. 实际上 G1 远未达成；下次唤醒检查时陷入 stalled 死循环
```

**问题分析**：违反 Rule 5——必须先确认 plan-next 输出含 L1 验收 KPI 状态字段且 KPI 已达成；否则即使「现在该做」为空也不应 done。`approved` 只代表决策批准，验收未达成时应继续推进，输出应是 blocked（等执行 + 等 KPI 数据）。

---

### ❌ 错误：从中间层（M5/任务）状态推断 done

```
1. plan-next 报：M5 任务全部 pending、设计 ADR 完备、需求文件完备
2. 模型推断"治理层无缺口" → 输出 done
3. 未回到战略目标 G1 验收检查
```

**问题分析**：从中间层扫描会丢失"为什么这条任务重要"的因果链。orchestrate-governance-step 的判定起点必须是「L1 验收 KPI 是否达成」，不是「中间层文档是否完备」。这与 plan-next 的目标树遍历方向一致——根节点是战略目标的验收标准。

---

### ❌ 错误：cron 模式下持续输出 done 而不警示用户

```
1. /loop 1m /orchestrate-governance-step 注册 cron
2. 首次 plan-next 返回空 → 输出 done（错误）
3. cron 不读信号，继续每分钟触发，陷入 done 空转
4. 用户不知 cron 在空转
```

**问题分析**：违反「与 /loop 交互模式」节约束。cron 模式下信号被忽略，技能必须主动警示用户改用 dynamic /loop 或建议 CronDelete。

---

## 示例

### 示例 1：快乐路径——需求登记成功

**场景**：plan-next 路由 backlog 新条目登记；首次调用；子技能成功。

**执行过程**：
1. 内部调用 plan-next → 主题："登记 M5 阶段新增的 3 项 backlog 条目"，推荐技能：`/capture-work-items`，优先级：缓
2. 卡死检测：首次调用，无历史指纹 → 继续
3. 人工闸门：`capture-work-items` 非创意类 → 继续
4. 执行 `/capture-work-items 把 M5 新发现的 3 项需求登记到 backlog`
5. 执行后验证：重跑 plan-next → 该卡片消失，"现在该做"仍有 1 条 → advance

**IterationStepReport**：

```
## 这次自动推进做了什么

- **做了什么**：把 M5 新发现的 3 项需求登记到 backlog
- **为什么要修**：M5 巡检发现 3 项需求散落在讨论中，未结构化登记
- **改了什么**：
  - 修改前：backlog/ 目录下无对应条目
  - 修改后：新增 3 个 backlog 条目文件，含 frontmatter 与摘要
- **结果**：成功 ✅
- **下一步**：继续自动推进（还有 1 条待处理项）
- _（内部）继续信号：advance_
```

---

### 示例 2：人工闸门阻断——战略目标待定义

**场景**：plan-next 路由 `design-strategic-goals`（战略创意类）；orchestrate-governance-step 必须暂停。

**执行过程**：
1. 内部调用 plan-next → 推荐技能：`/design-strategic-goals`，优先级：重要
2. 卡死检测：首次调用 → 继续
3. 人工闸门：`design-strategic-goals` 属战略创意类 → **触发暂停**

**IterationStepReport**：

```
## 这次自动推进做了什么

- **做了什么**：识别到战略目标文档缺失，需要补充
- **为什么要修**：docs/strategic-goals.md 不存在，无法推进后续路线图规划
- **结果**：需要你来决定 ⚠️
- **下一步**：需要你决定：战略目标内容需要人工判断与确认，请手动运行 `/design-strategic-goals`，完成后重新运行 `/orchestrate-governance-step`
- _（内部）继续信号：blocked_
```

---

### 示例 3（边界场景）：卡死检测——子技能未推进

**场景**：上次 `/capture-work-items` 执行后需求文档未成功写入；本次 plan-next 路由出同一卡片。

**执行过程**：
1. 内部调用 plan-next → 指纹 = "分析路线图节点 N1 的需求||战略目标「目标 A」→ 路线图「N1」当前：需求层"
2. 卡死检测：与上次指纹相同 → **触发 stalled**

**IterationStepReport**：

```
## 这次自动推进做了什么

- **做了什么**：尝试分析路线图 N1 的需求，但检测到连续 2 次未推进
- **为什么要修**：requirements/N1-requirements.md 在上次 `/capture-work-items` 后未成功写入
- **结果**：出错了 ❌
- **下一步**：卡住了：同一任务连续 2 次无进展，可能原因：需求文件未写入、路径配置错误、或技能执行有误。建议手动运行 `/capture-work-items` 并检查输出文件是否存在，解决后重新运行 /orchestrate-governance-step
- _（内部）继续信号：stalled_
```

---

## AI 重构指令

### 问题 1：执行了多条路由

- **识别标志**：IterationStepReport 出现多个 `调用技能` 条目
- **纠正步骤**：
  1. 识别被执行的多条路由
  2. 仅保留优先级最高 1 条（`紧急` > `重要` > `缓`）
  3. 重新输出 IterationStepReport，只报告 1 条动作

---

### 问题 2：遗漏 continuation_signal

- **识别标志**：IterationStepReport 缺少内部继续信号字段，或值不在五值枚举内
- **纠正步骤**：
  1. 检查执行结果，按以下逻辑补填：
     - 子技能成功 + 仍有路由 → `advance`
     - 子技能成功 + 无路由 → `done`
     - 人工闸门触发 → `blocked`
     - 指纹重复 → `stalled`
     - 子技能失败 → `error`
  2. 在 `下一步` 字段说明原因

---

### 问题 3：跳过执行后验证就报告 advance

- **识别标志**：报告显示 `advance` 但未重跑 plan-next 确认
- **纠正步骤**：
  1. 重跑 `/plan-next`，检查目标卡片是否已消失
  2. 若已消失 → 确认 `advance` 正确
  3. 若仍存在 → 更新卡死计数；若第 2 次出现 → 修正为 `stalled`

---

### 问题 4：自行判断完成状态跳过步骤 6

- **识别标志**：`下一步` 字段出现"治理层全部就绪"、"当前可执行的…均已创建"、"属于开发者执行层"等自我评估语言，且无步骤 6 plan-next 重跑记录
- **纠正步骤**：
  1. 重跑 `/plan-next`
  2. 若"现在该做"为空 → `done` 正确，报告无需修改
  3. 若"现在该做"仅含 blocked 条目 → 修正为内部继续信号 `blocked`，`下一步` 说明阻塞原因
  4. 若"现在该做"仍有可执行条目 → 修正为内部继续信号 `advance`，继续下一步

---

## Appendix: Output contract

### YAML schema（formal）

```yaml
type: object
required:
  - report_title
  - action_taken
  - result
  - next_step
  - continuation_signal
properties:
  report_title:
    type: string
    const: "这次自动推进做了什么"
  action_taken:
    type: string
    minLength: 1
    description: 用文件名或功能名描述本次唯一执行动作
  why_fix:
    type: string
    minLength: 1
    description: 可选；首次创建文件可省略
  changes:
    type: object
    required: [before, after]
    properties:
      before:
        type: string
      after:
        type: string
  result:
    type: string
    enum: ["成功 ✅", "需要你来决定 ⚠️", "出错了 ❌"]
  next_step:
    type: string
    minLength: 1
  continuation_signal:
    type: string
    enum: [advance, done, blocked, stalled, error]
  execution_trace:
    type: object
    required: [selected_skill, post_check_plan_next_rerun]
    properties:
      selected_skill:
        type: string
        pattern: "^/[a-z0-9-]+"
      post_check_plan_next_rerun:
        type: boolean
        const: true
additionalProperties: false
```

### JSON schema（formal）

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "IterationStepReport",
  "type": "object",
  "required": [
    "report_title",
    "action_taken",
    "result",
    "next_step",
    "continuation_signal",
    "execution_trace"
  ],
  "properties": {
    "report_title": {
      "type": "string",
      "const": "这次自动推进做了什么"
    },
    "action_taken": {
      "type": "string",
      "minLength": 1
    },
    "why_fix": {
      "type": "string",
      "minLength": 1
    },
    "changes": {
      "type": "object",
      "required": ["before", "after"],
      "properties": {
        "before": { "type": "string" },
        "after": { "type": "string" }
      },
      "additionalProperties": false
    },
    "result": {
      "type": "string",
      "enum": ["成功 ✅", "需要你来决定 ⚠️", "出错了 ❌"]
    },
    "next_step": {
      "type": "string",
      "minLength": 1
    },
    "continuation_signal": {
      "type": "string",
      "enum": ["advance", "done", "blocked", "stalled", "error"]
    },
    "execution_trace": {
      "type": "object",
      "required": ["selected_skill", "post_check_plan_next_rerun"],
      "properties": {
        "selected_skill": {
          "type": "string",
          "pattern": "^/[a-z0-9-]+"
        },
        "post_check_plan_next_rerun": {
          "type": "boolean",
          "const": true
        }
      },
      "additionalProperties": false
    }
  },
  "additionalProperties": false
}
```

---

## 自检

### 必选节完整性

- [ ] 11 个必选节全部存在（目的 / 核心目标 / 范围边界 / 使用场景 / 行为 / 输入与输出 / 限制 / 反模式 / 示例 / AI 重构指令 / 自检）
- [ ] Semantic Role 定位块存在，说明了与 plan-next / loop / orchestrate-repair-loop 的区别

### 核心成功标准

- [ ] 每次调用执行且仅执行 1 条动作
- [ ] 卡死检测：session 内指纹重复 2 次触发 stalled
- [ ] 执行后验证：重跑 plan-next 确认目标卡片消失
- [ ] 步骤 6 是否真正执行了重跑 plan-next？（不接受"自行推断治理完成"替代；备注中不出现自我评估语言）
- [ ] 人工闸门：战略创意类技能触发 blocked；「待执行」标签卡片触发 blocked
- [ ] 每次输出合法的 continuation_signal（advance / done / blocked / stalled / error）
- [ ] **plan-next 输出的"治理上下文"含 L1 验收 KPI 当前状态**？若否，视为 plan-next 不合规，输出 error 并提示升级
- [ ] **`done` 信号同时满足三条件**：plan-next 输出"现在该做"为空 + KPI 已达成 + 无「待执行」卡片
- [ ] **cron 模式（fixed-interval）下首次报告含 dynamic /loop 改用建议**
- [ ] **`stalled` 第 2 次连续出现时含「立即 CronDelete <job-id>」提示**

### 质量门检查

- [ ] Hard Boundaries 使用 MUST / MUST NOT 并附验证方式
- [ ] Anti-Patterns ≥ 2 个对比示例（实际 4 个）
- [ ] Examples ≥ 2 个，其中 ≥ 1 个边界场景（示例 3 覆盖卡死检测）
- [ ] AI 重构指令覆盖 ≥ 2 种错误模式（实际 3 种）

### 验收测试

执行完成后，IterationStepReport 是否清晰说明了执行了什么、结果如何、以及下一步是继续还是需要人工介入？若否 → 重写 IterationStepReport。
