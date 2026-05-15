---
artifact_type: adr
created_by: decision-record
lifecycle: snapshot
created_at: 2026-04-28
status: accepted
description: 用 Acceptance Criteria 替代 ASQM 量化分数决定 Skill status
---

# ADR 0008：用 Acceptance Criteria 替代 ASQM 分数决定 Skill Status

## 背景

现行治理链用 ASQM（4 维度线性求和：agent_native + cognitive + composability + stance，0–20）决定 skill 的 status，阈值 17 + Gate A/B。实践中暴露三个问题：

1. **评分不客观**：composability、stance 等维度由 LLM 主观判断，两次运行结果可能不同；伪装成量化，实为有偏定性评估。
2. **分类无效**：当前 59/62 validated、3/62 experimental、0 archive_candidate，阈值 17 几乎不淘汰任何技能，辨识力接近零。
3. **量化错位**：ASQM 衡量 spec 文档质量，status 应反映生产可靠性——两者不等价。一个文档完善但行为飘忽的技能反而得分更高。

业界（Anthropic MCP、OpenAI function calling、LangChain tools、AWS Bedrock Agents）对 tool 的约束收敛在 input schema + description + acceptance tests 三件套。无一家使用打分系统决定 production 状态——schema 是机器强制的约束，质量由测试和使用验证，不由分数验证。

## 决策

**完全移除 ASQM 评分系统。** `scores`、`asqm_quality`、`validation_gates` 三个字段从 agent.yaml 中删除，不保留"informational only"的残留。

新 status 由两个可验证条件决定：

| 条件 | 说明 |
|------|------|
| `has_output_contract: true` | SKILL.md 含 `## Appendix: Output contract` 或 `## 附录：输出合约` 节 |
| `len(acceptance_criteria) >= 1` | agent.yaml 新增字段；每条是可观测的输入→输出断言 |

新 status 语义：

```
validated         = has_output_contract AND len(acceptance_criteria) >= 1
experimental      = otherwise
archive_candidate = 仅由维护者手动设置
```

agent.yaml 新增字段示例：

```yaml
has_output_contract: true
acceptance_criteria:
  - "给定包含 git diff 的仓库路径，产出 findings 列表，每条含 Location / Category / Severity / Title 字段"
```

## 替代方案与被拒原因

### 替代方案 A：保留 scores 作为 informational annotation

**被拒原因**：sunk-cost 思维。62 个文件已有分数 → 改动量大 → 下意识保留。但 ADR 006 删除 linking_mode 已经证明：保留一个不驱动任何决策的字段，只会让读者困惑"这个数字还算数吗"，比没有更糟。软删除留下认知负担。

### 替代方案 B：保留 ASQM 但调整阈值/维度

**被拒原因**：根本问题不在阈值，在量化对象错位（spec 质量 ≠ 生产可靠性）。调整阈值无法消除主观性，也无法消除"对文档完备性加分而非对行为可靠性加分"的结构偏差。

### 替代方案 C：仅依赖 has_output_contract，不引入 acceptance_criteria

**被拒原因**：output contract 描述格式，acceptance_criteria 描述行为断言。前者保证机器可消费，后者保证 skill 在给定输入下产出符合预期。两者互补，缺一则约束链不完整。

## 迁移路径

1. **curate-skills SKILL.md 改造**：删除打分逻辑、cognitive ceiling、validation_gates 规则；新增 has_output_contract + acceptance_criteria 检查
2. **62 个 skill agent.yaml 批量手术**：删除 scores / asqm_quality / validation_gates 字段，添加 has_output_contract + acceptance_criteria
3. **28 个缺中文输出合约的 skill**：渐进补写 SKILL.md `## 附录：输出合约` 节
4. **ASQM_AUDIT.md → SKILL_INVENTORY.md**：重命名 + 内容重写，删除所有分数列
5. 完成标志：全部 skill 有 has_output_contract + ≥1 条 acceptance_criteria

迁移期间无并存机制——Phase 3 一次性批量切换，避免新旧字段同时出现的认知负担。

## 后果

**正面**：
- status 有可验证依据，不依赖 LLM 主观打分
- curate-skills 职责收窄，降低维护成本
- acceptance_criteria 对调用方有实用价值（不只是 governance 层产物）
- 与业界 tool 约束模式（schema + description + acceptance tests）对齐

**负面 / 风险**：
- 切换瞬间 28 个 skill 从 validated 降为 experimental（缺中文输出合约），需后续补齐
- acceptance_criteria 质量仍依赖人工编写，未引入自动执行框架
- 失去"可比较的质量分数"——但 ADR 已论证此分数辨识力接近零，损失可忽略

## 不在此 ADR 范围内

- acceptance_criteria 自动执行（skill 行为测试框架）
- SKILL.md 规范格式修改（由 refine-skill-design 处理）
- 28 个缺合约 skill 的 acceptance_criteria 内容填写（由后续 curate-skills 运行处理）

## 相关决策

- ADR 005 / 006：linking_mode 软删除→硬删除的先例，本 ADR 沿用同一原则
