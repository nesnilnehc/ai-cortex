---
name: curate-skills
description: Govern skill inventory through output-contract and acceptance-criteria checks, lifecycle assignment, and overlap detection. Core goal — produce verifiable status and normalized documentation for all skills in repository.
description_zh: 通过输出合约与验收准则检查、生命周期分配、重叠检测治理技能清单；产出全库技能的可验证 status 与规范化文档。
tags: [meta-skill, documentation]
version: 2.0.0
license: MIT
recommended_scope: project
metadata:
  author: ai-cortex
triggers: [curate, curate skills, skill audit]
aliases: [curate]
input_schema:
  type: free-form
  description: Skills directory to audit (defaults to skills/ in current repo)
output_schema:
  type: diagnostic-report
  description: skills/SKILL_INVENTORY.md with status distribution, output-contract coverage, missing acceptance_criteria, and per-skill agent.yaml updates
---

# 技能（Skill）：策划技能

## 目的（Purpose）

通过对每个技能执行可验证的两项检查（输出合约存在性 + 验收准则数量）来分配 status，并规范化 agent.yaml 与 README。代理优先；agent.yaml 是机器可消费的事实来源。

---

## 核心目标（Core Objective）

**首要目标**：为存储库中所有技能产出可验证的 status、规范化文档与仓库级清单。

**成功标准**（必须满足全部）：

1. ✅ 每个技能的 SKILL.md 已扫描并标注 `has_output_contract: true|false`
2. ✅ 每个技能的 agent.yaml 含 `acceptance_criteria` 字段（数组，允许为空）
3. ✅ status 按规则推导并写回 agent.yaml
4. ✅ 重叠以 `owner/repo:skill-name` 形式填入 `overlaps_with`
5. ✅ 仓库级 `skills/SKILL_INVENTORY.md` 写入或刷新，含状态分布、合约覆盖、缺失清单、最终建议

**验收测试**：AI agent 是否可仅通过 agent.yaml 文件就理解每个技能的 status 与关系，无需阅读 SKILL.md 或 README？

---

## 范围边界

**本技能负责**：

- 输出合约检测（grep `## Appendix: Output contract` 或 `## 附录：输出合约/合同/契约`）
- 验收准则字段维护
- status 分配（validated / experimental / archive_candidate）
- 重叠检测与 market_position 标注
- agent.yaml 与 README.md 规范化
- 仓库级 `skills/SKILL_INVENTORY.md` 生成

**本技能不负责**：

- 技能设计细化（→ refine-skill-design）
- SKILL.md 内容修改（→ refine-skill-design）
- 输出合约附录撰写（→ refine-skill-design 或人工）
- 注册表同步（INDEX.md / manifest.json 单独流程）
- 从零生成 README（→ generate-standard-readme）

**交接点**：当 SKILL_INVENTORY.md 写入并附带最终建议时，交给用户审查或 refine-skill-design 处理识别出的问题。

---

## 使用场景

- **添加或更改技能后**：重新检查并更新 status 与文档
- **审计**：审查生命周期分布与重叠
- **仓库摘要**：生成或刷新 SKILL_INVENTORY.md
- **自我评估**：对存储库进行管理，包括本元技能自身

---

## 行为

1. **扫描**：列出 `skills_directory` 下所有技能目录
2. **检测输出合约**：对每个技能的 SKILL.md 执行 grep，匹配以下任一即视为 `has_output_contract: true`：
   - `## Appendix: Output contract`
   - `## 附录：输出合约`
   - `## 附录：输出合同`
   - `## 附录：输出契约`
3. **读取/初始化 acceptance_criteria**：从 agent.yaml 读取；不存在则初始化为空数组
4. **推导 status**：
   - `validated` ← `has_output_contract == true AND len(acceptance_criteria) >= 1`
   - `experimental` ← 否则
   - `archive_candidate` ← 仅由维护者手动设置，本技能不主动转移
5. **重叠与定位**：分配 `overlaps_with`（`owner/repo:skill-name` 形式）和 `market_position`（differentiated / commodity / experimental）
6. **写回**：更新每技能的 agent.yaml（status、has_output_contract、acceptance_criteria、overlaps_with、market_position）；规范化 README.md
7. **汇总**：写入 `skills/SKILL_INVENTORY.md`，必须含最终建议节

### status 决定规则

```
validated         = has_output_contract AND len(acceptance_criteria) >= 1
experimental      = otherwise
archive_candidate = manual only
```

无评分系统。无 cognitive mode 推导。无门控阈值。两个布尔条件即决定 status。

### 生态位置（每项技能）

- **overlaps_with**：`owner/repo:skill-name` 列表，本仓库与其他仓库格式一致；无则空 `[]`
- **market_position**：
  - `differentiated`：明显差异化、最小重叠、库存中独特价值
  - `commodity`：通用能力，与多个技能重叠
  - `experimental`：早期、利基或定位不明确

**交互**：在批量覆盖技能文件或写入 SKILL_INVENTORY.md 之前，与用户确认；除非用户明确请求完整运行（如"curate all skills"）。

---

## 输入与输出

### 输入

- `skills_directory`：包含技能子目录的根路径（例如 `skills/`）

### 输出

- 每项技能：更新 agent.yaml（status、has_output_contract、acceptance_criteria、overlaps_with、market_position）；规范化 README.md
- 仓库级：`skills/SKILL_INVENTORY.md` 或结构化聊天摘要
- 重叠与定位报告

---

## 限制（Restrictions）

### 硬边界

- 不修改 specs/skill.md 或 manifest.json
- 不覆盖 SKILL.md（设计细化由 refine-skill-design 负责）
- 不撰写输出合约附录内容（仅检测存在性）
- 不主动设置 `archive_candidate`（仅维护者手动）
- 不输出任何评分字段（`scores`、`asqm_quality`、`validation_gates` 已由 ADR 008 移除，写入即为违规）

### 技能边界（避免重叠）

- 技能设计细化 → `refine-skill-design`
- 技能规格变更 → `refine-skill-design`
- 输出合约撰写 → `refine-skill-design` 或人工
- 注册表同步 → 独立流程
- 单独 README 生成 → `generate-standard-readme`

**何时停止并交接**：

- 用户问"如何改进这个技能的设计？" → `refine-skill-design`
- SKILL_INVENTORY.md 显示某技能缺输出合约 → 在最终建议节推荐 `refine-skill-design`
- 用户问"能更新 INDEX.md 吗？" → 解释注册表同步独立，提供手动步骤

---

## 自检（Self-Check）

### 核心成功标准

- [ ] 所有技能扫描 SKILL.md 并标注 has_output_contract
- [ ] 所有技能 agent.yaml 含 acceptance_criteria 字段
- [ ] status 按规则推导写回
- [ ] overlaps_with 以 `owner/repo:skill-name` 形式填入
- [ ] SKILL_INVENTORY.md 含状态分布、覆盖统计、缺失清单、最终建议

### 流程质量检查

- [ ] 扫描覆盖所有技能目录？
- [ ] has_output_contract 检测匹配中英文两种附录标题？
- [ ] acceptance_criteria 为空时 status 是否正确降为 experimental？
- [ ] 未输出任何 `scores` / `asqm_quality` / `validation_gates` 字段？
- [ ] 批量覆盖前是否与用户确认（除非明确请求完整运行）？

### 验收测试

**AI agent 是否可仅通过 agent.yaml 文件就理解每个技能的 status 与关系，无需阅读 SKILL.md 或 README？**

- 否：检测或文档不完整，返回相应步骤
- 是：管理已完成，交接或等待用户评论

---

## 示例

### 示例 1：完整管理运行

- **输入**：`skills_directory: skills/`；用户："curate all skills in this repo"
- **预期**：扫描所有子目录；对每技能 grep SKILL.md 检测输出合约；读取或初始化 acceptance_criteria；按规则推导 status；写回 agent.yaml；规范化 README；写入 `skills/SKILL_INVENTORY.md` 含最终建议

### 示例 2：单技能重新检查

- **输入**：用户："重新检查 refine-skill-design"
- **预期**：仅扫描该技能 SKILL.md；更新该 agent.yaml 的 has_output_contract 与 status；不写 SKILL_INVENTORY.md（除非要求）

### 边缘情况：新技能仅有 SKILL.md

- **输入**：新目录仅含 SKILL.md，无 agent.yaml、无 README
- **预期**：grep SKILL.md 检测输出合约；初始化 agent.yaml 含 has_output_contract、acceptance_criteria（空数组）、overlaps_with、market_position；status 推导为 experimental（acceptance_criteria 为空）；从 SKILL.md 生成最小规范化 README；汇总报告该技能为新增

---

## 附录：输出合约（per skill agent.yaml）

本技能写入或更新每个技能的 agent.yaml 时，使用此结构：

```yaml
name: [kebab-case skill name]
status: validated | experimental | archive_candidate

primary_use: [one-line purpose]

inputs:
  - [list of input names]

outputs:
  - [list of output artifacts]

has_output_contract: true | false   # SKILL.md 是否含输出合约附录

acceptance_criteria:                  # 可观测的输入→输出断言；空数组合法但 status 降为 experimental
  - [criterion 1]
  - [criterion 2]

overlaps_with:                        # Git-repo form: owner/repo:skill-name
  - [owner/repo:skill-name]

market_position: differentiated | commodity | experimental
```

**status 推导规则**：

- `validated` ← `has_output_contract AND len(acceptance_criteria) >= 1`
- `experimental` ← 否则
- `archive_candidate` ← 仅维护者手动设置

**禁止字段**（由 ADR 008 移除）：`scores`、`asqm_quality`、`validation_gates`、`cognitive_mode`。
