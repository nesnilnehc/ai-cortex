# 策划技能

**状态**：已验证

## 用途

对所有技能执行两项可验证检查：SKILL.md 是否含输出合约附录、agent.yaml 是否含 acceptance_criteria。基于结果分配 status，规范化 agent.yaml 与 README，产出仓库级 SKILL_INVENTORY.md。

## 何时使用

- 添加或更改技能后：重新检查并更新 status
- 审计：审查 status 分布与重叠
- 仓库摘要：生成或刷新 `skills/SKILL_INVENTORY.md`
- 自我评估：对仓库进行管理（包括本元技能）

## 输入

- `skills_directory`：包含技能子目录的根路径（例如 `skills/`）

## 输出

- 每项技能：更新 agent.yaml（status、has_output_contract、acceptance_criteria、overlaps_with、market_position）；规范化 README.md
- 仓库级：`skills/SKILL_INVENTORY.md` 或结构化聊天摘要
- 重叠与 market_position 报告

## status 规则

```
validated         = has_output_contract AND len(acceptance_criteria) >= 1
experimental      = 否则
archive_candidate = 仅维护者手动设置
```

无评分系统（ASQM 已由 [ADR 008](../../docs/architecture/adrs/008-replace-asqm-with-acceptance-criteria.md) 完整移除）。

## 生态

| 领域 | 值 |
| :--- | :--- |
| overlaps_with | nesnilnehc/ai-cortex:refine-skill-design, nesnilnehc/ai-cortex:generate-standard-readme |
| market_position | differentiated |

## 完整定义

参见 [SKILL.md](./SKILL.md) 了解完整行为、限制与示例。
