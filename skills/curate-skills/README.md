# 策划技能

**状态**：已验证

## 用途

对所有技能进行评估、评分（ASQM **严格**）、标记和标准化。根据技能写入“agent.yaml”和标准化“README.md”。严格评分：有据可依；仅当技能在 SKILL.md 中有明确的输出契约时，agent_native = 5。重叠和 market_position 描述了生态系统位置（仅限元数据）。

## 何时使用

- 添加或更改技能后：重新评分并更新状态
- 审计：审查生命周期（已验证/实验/存档_候选）和重叠
- 仓库摘要：生成或刷新 ASQM_AUDIT.md
- 自我评估：运行管理，包括此元技能

## 输入

- `skills_directory`：包含技能子目录的根路径（例如`skills/`）

## 输出

- 每项技能：更新`agent.yaml`（分数、状态、重叠、市场位置）、标准化`README.md`
- 回购级别：`ASQM_AUDIT.md` 或结构化聊天摘要
- 重叠和市场位置报告

## 评分 (ASQM)

| 维度 | 分数 |
| ：-------------- | :---- |
|agent_native | 5 |
|cognitive| 4 |
|composability | 5 |
|stance| 5 |
| **asqm_quality** | 19 |

生命周期：质量 ≥ 17 AND Gate A 和 Gate B → 已验证；质量 ≥ 10 → 实验性的。

## 生态

|领域 |价值|
| :------------------------------------ | :------------------------------------------------------------------------------------------ |
|overlaps_with（所有者/存储库：技能名称）| nesnilnehc/ai-cortex:refine-skill-design, nesnilnehc/ai-cortex:generate-standard-readme |
|市场地位 |差异化|

## 完整定义

请参阅 [SKILL.md](./SKILL.md) 了解完整的行为、限制和示例。