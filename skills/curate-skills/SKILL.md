---
name: curate-skills
description: Govern skill inventory through ASQM scoring, lifecycle management, and overlap detection. Core goal - produce validated quality scores and normalized documentation for all skills in repository.
description_zh: 通过 ASQM 评分、生命周期管理与重叠检测治理技能清单；产出全库技能的质量评分与规范化文档。
tags: [meta-skill, documentation]
version: 1.0.1
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
  description: ASQM_AUDIT.md with scores, lifecycle status, overlap analysis, and per-skill agent.yaml updates
---

# 技能（Skill）：策划技能

## 目的 (Purpose)

通过评估、评分、标记和标准化存储库中的每项技能（包括本技能）来管理技能库存。生成单一事实来源：机器可读的分数和每项技能的状态、标准化的面向人的自述文件、重叠检测和存储库级别摘要。代理优先； README 适用于人类，agent.yaml 适用于代理。

---

## 核心目标（Core Objective）

**首要目标**：为存储库中的所有技能生成已验证的 ASQM 分数、生命周期状态和标准化文档。

**成功标准**（必须满足所有要求）：

1. ✅ **所有技能评分**：每个技能目录都有严格计算的 ASQM 评分（agent_native、cognitive、composability、stance）并写入 agent.yaml
2. ✅ **分配生命周期状态**：每个技能都具有基于质量≥17+双门的已验证/实验/存档_候选状态（agent_native≥4，stance≥3）
3. ✅ **检测到重叠**：使用 Git-repo 表单（所有者/存储库：技能名称）在 agent.yaml 中为每个技能填充重叠字段
4. ✅ **文档标准化**：每个技能都按照标准结构更新了agent.yaml和README.md
5. ✅ **生成的审计产品**：ASQM_AUDIT.md 在回购级别编写，包含生命周期、分数、重叠、生态系统、调查结果和最终建议部分

**验收**测试：AI 代理是否可以使用 agent.yaml 文件来了解技能质量、状态和关系，而无需阅读 SKILL.md 或 README？

---

## 范围边界（范围边界）

**本技能负责**：

- 所有技能的 ASQM 评分（严格、基于证据）
- 生命周期状态分配（已验证/实验/archive_candidate）
- 重叠检测和市场定位
-每个技能的agent.yaml和README.md规范化
- 回购级审计产品（ASQM_AUDIT.md）生成

**本技能不负责**：

- 技能设计细化（使用“refine-skill-design”）
- 技能规格更改（使用“refine-skill-design”）
- 注册表同步（INDEX.md、manifest.json 更新根据规范是单独的）
- 从头开始生成个人技能自述文件（使用“generate-standard-readme”）

**转交点**：当 ASQM_AUDIT.md 与最终建议一起编写时，交给用户进行审查或“完善技能设计”以解决已识别的问题。

---

## 使用场景（用例）

- **添加或更改技能后**：重新评分并更新状态和文档，以便库存保持一致。
- **审核**：审查生命周期（已验证/实验/存档_候选）和重叠的所有技能。
- **Repo 摘要**：生成或刷新 ASQM_AUDIT.md 或整个技能目录的结构化聊天摘要。
- **自我评估**：对存储库进行管理，包括此元技能，因此治理本身就是一项技能。

## 行为（行为）

1. **扫描**：列出给定“skills_directory”下的所有技能目录（例如“skills/”）。
2. **阅读**：对于每项技能，阅读“agent.yaml”（如果存在）；否则请阅读 README 或 SKILL.md。首选 agent.yaml（如果存在）。
3. **分数**：对于每项技能，严格指定四个 ASQM 分数 0-5：“agent_native”、“cognitive”、“composability”、“stance”。应用**严格评分**（基于证据，无通货膨胀；见下文）。计算 **质量**（线性）：“asqm_quality = agent_native + cognitive + composability + stance”（0-20）。将分数和 asqm_quality 写入“agent.yaml”。
4. **生命周期**：应用双门规则。 **Gate A**（代理准备就绪）：agent_native ≥ 4。 **Gate B**（设计完整性）：stance ≥ 3。 **已验证**：质量 ≥ **17** AND Gate A AND Gate B。 **实验**：质量 ≥ 10。 **archive_candidate**：否则。
5. **重叠和位置**：对于每个技能，分配 `overlaps_with` （以 **Git-repo 形式** `owner/repo:skill-name` 表示的重叠技能列表，此存储库和其他存储库的格式相同；例如 `nesnilnehc/ai-cortex:generate-standard-readme`、`softaworks/agent-toolkit:commit-work`）和 `market_position`（`差异化` | `商品`） |“实验性”）。
6. **编写**：根据技能编写或更新 `agent.yaml` （分数、状态、overlaps_with、market_position）并将 `README.md` 标准化为标准部分（它的作用、何时使用、输入/输出等）。
7. **摘要**：在存储库级别编写“ASQM_AUDIT.md”或在聊天中打印结构化摘要。 **ASQM_AUDIT.md 必须包含最终建议部分**（例如“建议”）：可操作的后续步骤（例如分数调整、技能更改）或明确的“不建议更改”结论，因此每次审核都会以明确的指导结束。所需部分：按状态划分的生命周期、评分公式、维度清单、重叠、生态系统、调查结果、**建议**（最终）和简短的汇总表。

### 概念分裂

- ** 分数 (ASQM)** 衡量内在质量：为智能体设计的技能、推理卸载能力、composability和stance。
- **重叠和市场位置**描述生态系统位置：该技能如何与库存中的其他技能相关。

### 评分模型：ASQM（线性质量+双门）

- **质量**（线性）：`asqm_quality = agent_native + cognitive + composability + stance`；每个维度 0-5，总共 0-20。
- **Gate A**（代理准备就绪）：agent_native ≥ 4。
- **Gate B**（设计完整性）：stance≥ 3。
- **生命周期**：已验证 ↔ 质量 ≥ **17** AND Gate A AND Gate B；实验↔质量≥10； archive_candidate ↔ 否则。 （酒吧设置已验证 = 显然已准备好生产：17/20 + 两个门。）
- **维度**：agent_native — 代理消耗（合同、机器可读元数据）。cognitive——推理从用户转移到代理。composability——易于与其他技能或管道相结合。stance——设计stance（规范一致性、原则）。

### 严格评分（必填）

- **基于证据**：每个分数必须由技能的 SKILL.md 证明合理（例如存在附录：输出合同、交接点、范围边界、限制、自检）。
- **无通货膨胀**：仅当技能具有**显式的、机器可解析的输出合约**时，agent_native = 5（例如附录：输出合约或 SKILL.md 中的等效表/规范）。如果输出仅以散文形式描述，则 agent_native ≤ 4。
- **一致性**：对所有技能应用相同的标准；不要无缘无故地为了某一项技能而放松。

### 生态位置（每项技能）

- **overlaps_with**：**Git-repo 形式** `owner/repo:skill-name` 中的重叠技能列表。对此存储库和其他存储库使用相同的格式（没有单独的内部/外部）。示例：`nesnilnehc/ai-cortex:refine-skill-design`、`softaworks/agent-toolkit:commit-work`。如果没有，则清空“[]”。
- **市场位置**：
  - “差异化”：明显的差异化、最小的重叠、库存中独特的价值。
  - `商品`：通用能力，与许多技能重叠，标准模式。
  -“实验性”：生态系统中的早期、利基或定位不明确。

**交互**：在覆盖许多技能文件或编写 ASQM_AUDIT.md 之前，请与用户确认，除非他们明确请求完整运行（例如“策划所有技能”或“运行策划技能”）。

## 输入与输出 (Input & Output)

### 输入（输入）

- `skills_directory`：包含技能子目录的根路径（例如`skills/`）。

### 输出（输出）

- 每个技能：更新`agent.yaml`（分数、状态、重叠、市场位置）；标准化“README.md”。
- 回购级别：`ASQM_AUDIT.md` 或聊天中的结构化摘要。
- 重叠和市场位置报告：每个技能的重叠位置（所有者/存储库：技能名称）、市场位置。

## 限制（限制）

### 硬边界（Hard Boundaries）

- 不要在该技能中更改spec/skill.md或manifest.json； 元数据同步（INDEX、清单）是每个规范的单独步骤。
- 不要用该技能覆盖SKILL.md； curate-skills 更新每个技能的 agent.yaml 和 README。 SKILL.md 仍然是每个规范的规范定义。
- **INDEX.md** 是规范的功能列表（注册表、标签、版本、用途）；不要覆盖它。 **ASQM_AUDIT.md** 是仓库级别的管理产品：质量、生命周期、重叠、生态系统、发现和 **最终建议**（可操作的后续步骤或“无更改”）；在完整的管理运行中编写或更新它并提交它。
- 规范化时尊重技能/INDEX.md 中的现有标签；仅当与标签系统明确一致时才添加或建议标签。
- **严格评分**：严格应用ASQM维度；不要夸大分数。仅当技能在 SKILL.md 中有明确的输出契约（附录或同等内容）时，agent_native = 5。

### 技能边界 (Skill Boundaries)（避免重叠）

**不要做这些（其他技能可以处理它们）**：

- **技能设计细化**：审核和重构单个 SKILL.md 结构、内容或质量 → 使用 `refine-skill-design`
- **技能规格变更**：修改技能行为、限制或核心设计→使用`refine-skill-design`
- **注册表同步**：更新技能/INDEX.md或manifest.json以反映技能更改→每个spec/skill.md单独的进程
- **单独的 README 生成**：从头开始为新技能创建 README.md → 使用“generate-standard-readme”（curate-skills 规范现有的 README）
- **技能实现**：编写或修改技能代码/逻辑→超出范围

**何时停止并交接**：

- User asks "how do I improve this skill's 设计?" → 交给“精炼技能设计”
- 用户问“你能解决 SKILL.md 中的问题吗？” → 交给“精炼技能设计”
- ASQM_AUDIT.md 显示需要设计改进的技能 → 在最终建议部分推荐 `refine-skill-design`
- 用户问“你能更新 INDEX.md 吗？” → 解释注册表同步是根据规范分开的，提供手动步骤

## 自检（Self-Check）

### 核心成功标准（必须满足所有标准）

- [ ] **所有技能评分**：每个技能目录都有严格计算的 ASQM 评分（agent_native、cognitive、composability、stance）并写入 agent.yaml
- [ ] **分配的生命周期状态**：每个技能都有已验证/实验/存档_候选状态，基于质量 ≥ 17 + 双门（agent_native ≥ 4，stance ≥ 3）
- [ ] **检测到重叠**：使用 Git-repo 表单（所有者/存储库：技能名称）在每个技能的 agent.yaml 中填充重叠字段
- [ ] **文档标准化**：每个技能都按照标准结构更新了agent.yaml和README.md
- [ ] **生成的审计产品**：ASQM_AUDIT.md 在回购级别编写，包含生命周期、分数、重叠、生态系统、调查结果和最终建议部分

### 流程质量检查

- [ ] 扫描给定根目录下的所有技能目录？
- [ ] agent.yaml 在 README 存​​在时被读取？
- [ ] 分数 (0–5) 严格分配（基于证据；agent_native 5 仅具有明确的输出合约）？
- [ ] asqm_quality (0–20) 计算和写入是否一致？
- [ ] 按指定编写或更新了每个技能的 agent.yaml 和 README？
- [ ] Overlaps_with (owner/repo:skill-name) 和 market_position 为每个技能分配和写入？
- [ ] 如果交互策略需要，用户在批量覆盖之前确认？

### 验收测试

**AI 代理是否可以使用 agent.yaml 文件来了解技能质量、状态和关系，而无需阅读 SKILL.md 或 README？**

如果否：评分或文档记录不完整。返回评分或标准化步骤。

如果是：管理已完成。继续转交或用户评论。

## 示例（示例）

### 示例 1：全面管理运行

- **输入**：`技能目录：技能/`；用户说“整理此存储库中的所有技能。”
- **预期**：扫描`skills/`的所有子目录；阅读每个技能的agent.yaml或README/SKILL.md；分数;为每个技能分配overlaps_with (owner/repo:skill-name) 和market_position；写回agent.yaml和标准化README；报告重叠和市场位置；写入 ASQM_AUDIT.md 或打印结构化摘要。如果政策适用，请在撰写前确认一次。

### 示例2：单项技能重新评分

- **输入**：用户说“重新评分并仅更新精炼技能设计。”
- **预期**：阅读该技能的 agent.yaml 或文档；计算分数、状态、overlaps_with 和 market_position；仅更新该技能的 agent.yaml 和 README；除非有要求，否则不要写入 ASQM_AUDIT.md。

### 边缘情况：没有 agent.yaml 的新技能

- **输入**：新的技能目录只有SKILL.md（没有agent.yaml，没有README）。
- **预期**：阅读 SKILL.md；导出分数、overlaps_with 和 market_position；创建包含分数、状态、overlaps_with 和 market_position 的 agent.yaml；从 SKILL.md 生成最小标准化自述文件。总结报告该技能是新装备的。

---

## 附录：输出合约（每个技能的agent.yaml）

当此技能写入或更新技能的“agent.yaml”时，它会使用此结构，以便代理可以在不阅读 README 的情况下使用它：


```yaml
name: [kebab-case skill name]
status: validated | experimental | archive_candidate

primary_use: [one-line purpose]

inputs:
  - [list of input names]

outputs:
  - [list of output artifacts]

scores:
  agent_native: [0-5]
  cognitive: [0-5]
  composability: [0-5]
  stance: [0-5]

asqm_quality: [0-20, linear: agent_native + cognitive + composability + stance]

overlaps_with:   # Git-repo form: owner/repo:skill-name (this repo and others alike)
  - [owner/repo:skill-name]
  - [owner/repo:other-skill]

market_position: differentiated | commodity | experimental
```


- **分数** (ASQM) 衡量内在质量。 **asqm_quality** = agent_native + cognitive + composability + stance (0–20)。 **生命周期**：已 ↔ 质量 ≥ **17** 且 agent_native ≥ 4 且stance ≥ 3；实验↔质量≥10； archive_candidate ↔ 否则。
- **overlaps_with** 以 `owner/repo:skill-name` 形式列出 Git 存储库中的重叠技能（此存储库和其他存储库的格式相同）；如果没有则空“[]”。