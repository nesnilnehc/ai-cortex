# orchestrate-governance-step

单步治理执行器——plan-next 的配对执行层。

## 一句话

读取 plan-next 路由输出，执行最高优先级动作，返回 `continuation_signal` 供 `/loop` 驱动迭代推进。

## 三层模型中的位置

```
/loop /orchestrate-governance-step 30m
  └─ orchestrate-governance-step        ← 驱动层（本技能）
       └─ /plan-next     ← 诊断层（只读）
```

## 使用方式

| 场景 | 命令 |
|---|---|
| 执行下一条治理动作 | `/orchestrate-governance-step` |
| 全自动 autopilot | `/loop /orchestrate-governance-step` |
| 每 30 分钟自动推进 | `/loop /orchestrate-governance-step 30m` |
| 只查看建议（不执行） | `/plan-next` |

## 输出：IterationStepReport

每次调用输出一份报告，包含：
- 执行动作与治理上下文
- 调用的子技能
- 执行结果
- `continuation_signal`：`advance` / `done` / `blocked` / `stalled` / `error`

## 停止条件

| 信号 | 原因 |
|---|---|
| `done` | 治理链全部就绪 |
| `blocked` | 战略创意类技能需要人工 |
| `stalled` | 同一路由卡片连续 2 次无进展 |
| `error` | 子技能执行失败 |

## 参考

- `skills/plan-next/SKILL.md` — 诊断层
- `docs/architecture/adrs/007-remove-plan-next-execute-flag.md` — 三层模型决策
