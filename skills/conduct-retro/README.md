# 工程回顾

**状态**：已验证

## 用途

基于 Git 提交历史、工作模式与代码质量指标，产出周或迭代的工程回顾报告；支持按人贡献分解，含表扬与成长建议。与 `align-planning` 互补（后者关注规划对齐，本技能关注交付复盘）。

## 何时使用

- 周/迭代结束时的工程复盘
- 用户问「这周发了什么」「我们 ship 了多少」
- 团队协作时需按人反馈

## 输入

- 可选时间窗口：`7d`（默认）、`14d`、`30d`

## 输出

- `docs/calibration/YYYY-MM-DD-retro.md` 回顾报告
- 对话中的摘要（Tweetable 与核心指标）

## 评分 (ASQM)

| 维度 | 分数 |
| :--- | :--- |
| agent_native | 4 |
| cognitive | 4 |
| composability | 4 |
| stance | 5 |
| **asqm_quality** | 17 |

## 生态

| 领域 | 值 |
| :--- | :--- |
| overlaps_with | nesnilnehc/ai-cortex:align-planning, nesnilnehc/ai-cortex:assess-docs |
| market_position | differentiated |

## 完整定义

参见 [SKILL.md](./SKILL.md) 了解完整行为、限制与示例。
