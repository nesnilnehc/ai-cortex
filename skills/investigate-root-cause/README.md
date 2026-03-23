# 根因调试

**状态**：已验证

## 用途

通过系统性根因调查与假设验证，在未确认根因前不实施修复，避免症状修补导致的连锁问题。铁律：无根因不修复。适用于报错、异常行为或「之前能跑、现在坏了」的故障排查。

## 何时使用

- 用户报告错误、异常行为或「为什么坏了」
- 测试失败需定位根因
- 间歇性问题需系统性排查
- 回归引入的 bug 需追溯

## 输入

- 错误信息、堆栈、复现步骤
- 可选：受影响文件或目录

## 输出

- 根因假设与验证过程
- 最小修复与回归测试
- 结构化 Debug Report（symptom, root cause, fix, evidence, status）

## 评分 (ASQM)

| 维度 | 分数 |
| :--- | :--- |
| agent_native | 4 |
| cognitive | 5 |
| composability | 4 |
| stance | 5 |
| **asqm_quality** | 18 |

## 生态

| 领域 | 值 |
| :--- | :--- |
| overlaps_with | nesnilnehc/ai-cortex:automate-repair, nesnilnehc/ai-cortex:review-diff, nesnilnehc/ai-cortex:review-code |
| market_position | differentiated |

## 完整定义

参见 [SKILL.md](./SKILL.md) 了解完整行为、限制与示例。
