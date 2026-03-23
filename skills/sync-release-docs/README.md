# 发版后同步文档

**状态**：已验证

## 用途

在代码发版或 PR 合并后，确保项目文档（README、ARCHITECTURE、CONTRIBUTING、CLAUDE.md、CHANGELOG、TODOS）与已交付变更一致，保持可发现性与跨文档一致性。

## 何时使用

- 用户要求发版后更新文档、同步文档或 post-ship docs
- PR 已创建或合并，需确保文档与变更一致
- CHANGELOG 措辞需润色为面向用户的语气

## 输入

- 可选：base branch 名称；否则从项目配置或 `gh` 推断
- 包含未合并文档变更的 feature branch

## 输出

- 更新的文档文件（若有）及单次 commit
- 结构化的 doc health summary

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
| overlaps_with | nesnilnehc/ai-cortex:discover-docs-norms, nesnilnehc/ai-cortex:assess-docs, nesnilnehc/ai-cortex:bootstrap-docs |
| market_position | differentiated |

## 完整定义

参见 [SKILL.md](./SKILL.md) 了解完整行为、限制与示例。
