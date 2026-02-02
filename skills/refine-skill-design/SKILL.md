---
name: refine-skill-design
description: 用于审计、重构和升维其他 SKILL 的元能力。通过多维度评估，确保 SKILL 达到工业级标准。
tags: [writing, eng-standards, meta-skill, optimization]
related_skills: [decontextualize-text, generate-standard-readme]
version: 1.2.0
recommended_scope: user
---

# Skill: 技能优化专家 (Refine Skill Design)

## 目的 (Purpose)

作为“Skill 的 Skill”，本技能旨在对初稿状态的 AI 能力定义进行**深度审计与重构**。通过注入资深 Prompt 工程师的视角，提升 Skill 的逻辑鲁棒性、场景覆盖度和指令遵循率，确保资产库中的每一项能力都符合 LLM 最佳实践。

---

## 适用场景 (Use Cases)

- **新技能入库**：当 Agent 自动生成了一个新 Skill 的草稿后，进行“专家评审”。
- **性能劣化修复**：当某个 Skill 在新模型下表现不稳定时，进行逻辑对齐和示例加固。
- **一致性审计**：检查新 Skill 是否符合 `INDEX.md` 定义的标签系统和命名契约。
- **思维升维**：将一个简单的“格式化工具”升级为一个带“交互策略”和“异常处理”的专业 Agent 能力。

---

## 行为要求 (Behavior)

### 核心思维模型 (The Meta-Audit Model)

1. **意图锚定**：目的 (Purpose) 是否足够具体？是否避免了“Helper”、“Utilities”等泛滥词汇？
2. **逻辑闭环**：`Input -> Behavior -> Output` 是否形成了确定性链路？
3. **负向约束**：`Restrictions` 是否锁定了该领域最常见的失败路径？
4. **Few-shot 演进**：`Examples` 是否由浅入深？是否包含了边界 case (Edge cases)？

### 优化流程 (The Optimization Loop)

1. **结构对齐**：强制应用标准 Markdown 模板（YAML, Purpose, Use cases, Behavior, I/O, Restrictions, Self-Check, Examples）。
2. **动词精准化**：使用更强力、无歧义的动词（如：将“处理”改为“解析、转换、修剪”）。
3. **增加交互协议**：为复杂逻辑注入“二次确认”或“多方案选择”逻辑。
4. **元数据校准**：根据 `INDEX.md` 补全 tags 并建议合理的 SemVer 版本号。

---

## 输入与输出 (Input & Output)

### 输入 (Input)

- 一个待优化的 SKILL MD 文档或初步的想法草拟。

### 输出 (Output)

- **优化后的 SKILL 文档**：完全符合 specifications 的生产级 MarkDown。
- **差异变更说明 (Diff Summary)**：说明进行了哪些关键逻辑修正及原因。
- **版本建议**：基于 SemVer 的建议版本号。

---

## 禁止行为 (Restrictions)

- **禁破坏语义**：优化过程中不得偏离原始技能的核心意图。
- **禁冗余话术**：README 式的解释文本应尽量精简，优先使用列表和表格。
- **禁单一示例**：严禁只保留一个“Happy path”示例，必须增加至少一个挑战性示例。

---

## 质量检查 (Self-Check)

- [ ] **自举性**：该 Skill 能否成功优化它自己？
- [ ] **语义清晰度**：不具备该专业背景的 Agent 能否根据 `Behavior` 稳定复现结果？
- [ ] **结构合规性**：是否包含了所有必填章节和元数据字段？

---

## 示例 (Examples)

### 优化前 (Before)
> name: spell-check
> 这是一个检查拼写的技能。
> 输入：一段多语言文本。
> 输出：纠正后的文本。

### 优化后 (After)
> name: polish-text-spelling
> description: 针对多语言文档进行语境敏感的拼写纠错与术语统一。
> tags: [writing, quality-control]
> version: 1.1.0
> ---
> # Skill: 语义纠错专家
> ## 目的：在不改变作者原意和语气的前提下，识别并修正低级拼写错误及术语不一致。
> ## 行为：
>
> 1. 识别语种。
> 2. 建立术语表（如果文本较长）。
> 3. 区分“错别字”与“特定风格表达”。
>
> ## 禁止：严禁修改专有名词或特定缩写，除非能确定其错误。

### 示例 2：边界情况——含歧义意图的草稿

- **输入**：某 Skill 草稿的「目的」写为“帮助用户处理文件”，无 Use Cases、无 Restrictions。
- **预期优化**：意图锚定（“处理”拆解为解析/转换/合并等具体动词）；补全适用场景与禁止行为（如禁止覆盖源文件、禁止修改二进制）；增加至少一个边界示例（如空文件、超大文件、权限不足时的行为）。
