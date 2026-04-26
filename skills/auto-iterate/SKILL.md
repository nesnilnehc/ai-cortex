---
name: auto-iterate
description: Single-step governance executor — reads plan-next routing output, executes the highest-priority action, and emits a continuation signal for /loop-driven autopilot.
description_zh: 单步治理执行器——读取 plan-next 路由输出，执行最高优先级动作，发出继续信号以支持 /loop 全自动推进。
tags: [automation, workflow, meta-skill]
version: 1.0.0
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

# 技能：自动迭代（auto-iterate）

> **角色**：单步治理执行器——plan-next 的配对执行层
> **WHAT**：每次调用执行 1 条 plan-next 路由建议，发出 `continuation_signal` 供 `/loop` 驱动迭代推进
> **HOW**：内部调用 plan-next → 取最高优先级卡片 → 人工闸门判断 → 执行子技能 → 执行后验证 → 输出报告
> **区别**：不同于 `plan-next`（只读诊断，不执行）；不同于 `/loop`（只调度，不执行业务逻辑）；不同于 `automate-repair`（修复代码缺陷，不推进治理层）

---

## 目的

将 plan-next 的路由建议转化为一次可执行的治理动作，使全自动 autopilot（`/loop /auto-iterate`）成为可能。

plan-next 只能诊断和建议；用户需手动执行每条建议。auto-iterate 填补这一执行缺口，配合 `/loop` 实现三层正交自动化：

| 层 | 技能 | 职责 |
|---|---|---|
| 调度 | `/loop` | 每 N 分钟触发一次 |
| **驱动** | **auto-iterate** | 读路由 → 执行 1 步 → 报告 |
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
- 代码缺陷修复循环 → `automate-repair`
- 战略创意决策内容（使命、愿景、战略目标内容）→ 需要人工
- 工作项追踪与状态维护 → `align-work-item-manifest`

**转交点**：
- `continuation_signal: done` → 治理就绪，告知用户，停止
- `continuation_signal: blocked | stalled | error` → 需人工介入，停止并说明原因

---

## 使用场景

- "继续推进治理，直到完成" → `/loop /auto-iterate`
- "执行下一条治理动作" → `/auto-iterate`
- "全自动 autopilot，每 30 分钟推进一次" → `/loop /auto-iterate 30m`
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

从"现在该做"取最高优先级 1 条（`紧急` → `重要` → `缓`）。

若"现在该做"为空 → `continuation_signal: done`，输出报告，停止。

### 步骤 3：卡死检测

将本次指纹与 session 内**上次执行的指纹**对比：

- **相同** → `continuation_signal: stalled`，说明"上次执行后目标卡片未推进"，停止
- **不同（或首次调用）** → 继续

### 步骤 4：人工闸门

以下情形必须暂停，输出说明，设置 `continuation_signal: blocked`：

- 推荐技能属于创意/战略类：`define-mission`、`design-strategic-goals`、`define-vision`、`define-north-star`、`define-strategic-pillars`
- 路由卡片完成标志含"受阻时回 plan-next 重评"且当前已触发

### 步骤 5：执行

调用路由卡片中的"推荐技能"命令（格式：`/skill-name [聚焦点]`）。

执行失败且无恢复路径 → `continuation_signal: error`，输出报告，停止。

### 步骤 6：执行后验证

轻量重跑 `/plan-next`，检查目标卡片是否已从"现在该做"消失：

| 结果 | 行动 |
|---|---|
| 卡片消失，"现在该做"仍有条目 | `continuation_signal: advance` |
| 卡片消失，"现在该做"为空 | `continuation_signal: done` |
| 卡片仍存在 | 更新卡死计数器；若计数达 2 → `continuation_signal: stalled` |

### 步骤 7：输出 IterationStepReport

---

## 输入与输出

### 输入

| 参数 | 必选 | 默认 | 说明 |
|---|---|---|---|
| `docs_root` | 否 | auto | 治理文档根目录；auto 同 plan-next 默认路径 |
| `pre_run_output` | 否 | — | 预运行的 plan-next 输出；提供时跳过内部调用 |

### 输出：IterationStepReport

```
## auto-iterate 执行报告

- **执行动作**：[路由卡片主题]
- **治理上下文**：[战略目标「X」→ 路线图「Y」→ ... 当前：[层级]]
- **调用技能**：`/skill-name [聚焦点]`（未执行时注明原因）
- **执行结果**：成功 | 需要人工介入 | 被阻塞 | 被卡死 | 失败
- **继续信号**：advance | done | blocked | stalled | error
- **备注**：[若非 advance，说明原因及建议下一步]
```

### continuation_signal 语义

| 值 | 含义 | /loop 行为 |
|---|---|---|
| `advance` | 动作已完成，治理还有工作 | 继续触发下次 |
| `done` | "现在该做"为空，治理已就绪 | 停止循环 |
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

### 技能边界（Skill Boundaries）

**不做以下事项**（其他技能负责）：
- **治理诊断与路由** → `plan-next`
- **循环调度** → `/loop`
- **代码修复循环** → `automate-repair`
- **文档评估** → `assess-docs`
- **工作项状态维护** → `align-work-item-manifest`

---

## 反模式

### ✅ 正确：单步执行 + 后验证 + 继续信号

```
1. plan-next → 2 条路由：breakdown-tasks（缓）、analyze-requirements（缓）
2. 取最高优先级：breakdown-tasks
3. 人工闸门：非创意类 → 继续
4. 执行 /breakdown-tasks
5. 重跑 plan-next → breakdown-tasks 卡片消失
6. 报告 continuation_signal: advance
```

**为什么正确**：单步执行保持三层模型正交性；后验证确认真实推进；/loop 自然驱动下一步。

---

### ❌ 错误：一次执行两条路由

```
1. plan-next → 2 条路由
2. auto-iterate 执行 breakdown-tasks AND analyze-requirements
```

**问题分析**：违反单步语义；若第二条失败，难以确定回滚范围；破坏 /loop 的粒度控制。

---

### ❌ 错误：绕过人工闸门

```
1. plan-next 路由：/design-strategic-goals
2. auto-iterate 直接执行，不暂停
```

**问题分析**：战略目标内容需要人工判断；自动执行产出低质量战略文档，且用户无感知。

---

### ❌ 错误：跳过执行后验证直接报告 advance

```
1. 执行 /breakdown-tasks 完成
2. 直接报告 continuation_signal: advance
3. 实际上文件未成功写入
```

**问题分析**：缺少后验证导致虚假 advance；下次 plan-next 仍给出同一路由，触发 stalled。

---

## 示例

### 示例 1：快乐路径——任务拆解成功

**场景**：plan-next 路由设计 D1b 的任务拆解；首次调用；子技能成功。

**执行过程**：
1. 内部调用 plan-next → 主题："为设计 D1b 拆解可执行任务"，推荐技能：`/breakdown-tasks`，优先级：缓
2. 卡死检测：首次调用，无历史指纹 → 继续
3. 人工闸门：`breakdown-tasks` 非创意类 → 继续
4. 执行 `/breakdown-tasks 基于设计 D1b 拆解任务清单，参考 D1a 拆解粒度`
5. 执行后验证：重跑 plan-next → D1b 卡片消失，"现在该做"仍有 1 条 → advance

**IterationStepReport**：

```
## auto-iterate 执行报告

- **执行动作**：为设计 D1b 拆解可执行任务
- **治理上下文**：战略目标「目标 A」→ 路线图「N1」→ 需求「R1」→ 设计「D1b」当前：任务层
- **调用技能**：`/breakdown-tasks 基于设计 D1b 拆解任务清单，参考 D1a 拆解粒度`
- **执行结果**：成功
- **继续信号**：advance
- **备注**：任务层缺口已填补；治理链还有 1 条待处理路由，/loop 可继续触发
```

---

### 示例 2：人工闸门阻断——战略目标待定义

**场景**：plan-next 路由 `design-strategic-goals`（战略创意类）；auto-iterate 必须暂停。

**执行过程**：
1. 内部调用 plan-next → 推荐技能：`/design-strategic-goals`，优先级：重要
2. 卡死检测：首次调用 → 继续
3. 人工闸门：`design-strategic-goals` 属战略创意类 → **触发暂停**

**IterationStepReport**：

```
## auto-iterate 执行报告

- **执行动作**：补充战略目标文档
- **治理上下文**：战略目标「缺失」当前：战略目标层
- **调用技能**：（未执行——人工闸门触发）
- **执行结果**：需要人工介入
- **继续信号**：blocked
- **备注**：战略目标内容需要人工判断与确认。请手动运行 `/design-strategic-goals`，完成后重新运行 `/auto-iterate`。
```

---

### 示例 3（边界场景）：卡死检测——子技能未推进

**场景**：上次 `/analyze-requirements` 执行后需求文档未成功写入；本次 plan-next 路由出同一卡片。

**执行过程**：
1. 内部调用 plan-next → 指纹 = "分析路线图节点 N1 的需求||战略目标「目标 A」→ 路线图「N1」当前：需求层"
2. 卡死检测：与上次指纹相同 → **触发 stalled**

**IterationStepReport**：

```
## auto-iterate 执行报告

- **执行动作**：分析路线图节点 N1 的需求
- **治理上下文**：战略目标「目标 A」→ 路线图「N1」当前：需求层
- **调用技能**：（未执行——卡死检测触发）
- **执行结果**：被卡死
- **继续信号**：stalled
- **备注**：同一路由卡片连续 2 次出现，上次执行后目标未推进。可能原因：需求文件未写入、路径配置错误、或技能执行有误。建议：手动运行 `/analyze-requirements` 并检查输出文件是否存在，解决后重新运行 /auto-iterate。
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

- **识别标志**：IterationStepReport 缺少 `继续信号` 字段，或值不在五值枚举内
- **纠正步骤**：
  1. 检查执行结果，按以下逻辑补填：
     - 子技能成功 + 仍有路由 → `advance`
     - 子技能成功 + 无路由 → `done`
     - 人工闸门触发 → `blocked`
     - 指纹重复 → `stalled`
     - 子技能失败 → `error`
  2. 补充 `备注` 字段说明原因

---

### 问题 3：跳过执行后验证就报告 advance

- **识别标志**：报告显示 `advance` 但未重跑 plan-next 确认
- **纠正步骤**：
  1. 重跑 `/plan-next`，检查目标卡片是否已消失
  2. 若已消失 → 确认 `advance` 正确
  3. 若仍存在 → 更新卡死计数；若第 2 次出现 → 修正为 `stalled`

---

## 自检

### 必选节完整性

- [ ] 11 个必选节全部存在（目的 / 核心目标 / 范围边界 / 使用场景 / 行为 / 输入与输出 / 限制 / 反模式 / 示例 / AI 重构指令 / 自检）
- [ ] Semantic Role 定位块存在，说明了与 plan-next / loop / automate-repair 的区别

### 核心成功标准

- [ ] 每次调用执行且仅执行 1 条动作
- [ ] 卡死检测：session 内指纹重复 2 次触发 stalled
- [ ] 执行后验证：重跑 plan-next 确认目标卡片消失
- [ ] 人工闸门：战略创意类技能触发 blocked
- [ ] 每次输出合法的 continuation_signal（advance / done / blocked / stalled / error）

### 质量门检查

- [ ] Hard Boundaries 使用 MUST / MUST NOT 并附验证方式
- [ ] Anti-Patterns ≥ 2 个对比示例（实际 4 个）
- [ ] Examples ≥ 2 个，其中 ≥ 1 个边界场景（示例 3 覆盖卡死检测）
- [ ] AI 重构指令覆盖 ≥ 2 种错误模式（实际 3 种）

### 验收测试

执行完成后，IterationStepReport 是否清晰说明了执行了什么、结果如何、以及下一步是继续还是需要人工介入？若否 → 重写 IterationStepReport。
