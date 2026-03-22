---
name: define-vision
description: Define the long-term future the project aims to create. Answers what future we are building; produces a vision statement aligned with mission, persisted to docs.
description_zh: 定义项目旨在创造的长远未来；回答我们在构建什么未来；产出 vision 陈述并持久化到 docs。
tags: [documentation, workflow]
version: 1.2.0
license: MIT
recommended_scope: both
metadata:
  author: ai-cortex
triggers: [define vision, vision, what future]
input_schema:
  type: free-form
  description: Mission (statement or path); project/product context; optional existing vision draft
output_schema:
  type: document-artifact
  description: Vision statement written to docs/project-overview/vision.md (or project norms)
  artifact_type: vision
  path_pattern: docs/project-overview/vision.md
  lifecycle: living
---

# 技能：定义愿景

## 目的

定义并记录**愿景**：项目旨在创造的长期未来。愿景声明回答「我们正在建设什么样的未来？」并与使命保持一致。不定义指标、目标或里程碑。

**愿景不同于**：

- **使命**：项目存在的根本目的（使用 `define-mission`）。
- **北极星**：表示交付价值的单个指标（使用 `define-north-star`）。
- **战略目标**：实现愿景的 3–5 个结果（使用 `design-strategic-goals`）。
- **里程碑**：执行的阶段检查点（使用 `define-milestones`）。

---

## 核心目标

**首要目标**：生成与使命一致的、经用户确认的愿景声明，并持久化到项目商定的路径。

**成功标准**（必须满足所有要求）：

1. ✅ **存在愿景陈述**：一到三句话仅描述期望的未来状态（没有指标、OKR、路线图）。
2. ✅ **与使命一致**：愿景与使命不矛盾；若缺少使命，建议先运行 `define-mission` 或说明假定目的。
3. ✅ **用户确认**：用户明确批准（如「已批准」「看起来不错」「继续」或同等内容）。
4. ✅ **文档持久化**：写入商定的路径（默认 `docs/project-overview/vision.md` 或项目规范）。
5. ✅ **尊重范围**：声明未定义北极星指标、战略目标或里程碑。
6. ✅ **YAGNI/DRY/简洁**：遵循 spec §4 文档制品原则；愿景陈述即核心，避免不必要的可选段落（如与使命对齐、时间范围的显式说明）。

**验收测试**：读者能否理解该项目试图创造什么样的长期未来，并看到其与使命一致？

**交接点**：愿景批准并持久化后，交接至 `define-north-star` 或 `design-strategic-goals`；若仅请求愿景则停止。

---

## 范围边界

### 本技能必须做什么

- 阐明项目或产品期望的长期未来状态。
- 制作愿景声明（1–3 句话）。
- 确保与使命一致（从 `define-mission` 输出或现有文档读取使命）。
- 持久化到项目约定的路径（默认 `docs/project-overview/vision.md`）。

### 本技能不能做什么

- 定义根本目的（使用 `define-mission`）。
- 定义北极星指标或战略目标（使用 `define-north-star`、`design-strategic-goals`）。
- 定义里程碑（使用 `define-milestones`）。
- 书写路线图、需求或待办（使用 `analyze-requirements`、`capture-work-items` 等）。

---

## 愿景质量指南

强有力的愿景声明应具备：

- **简洁**：1–3 句话；聚焦未来状态。
- **与使命一致**：支持使命中的根本目的；不引入新目的。
- **可想象**：2–5 年后的成功画面；读者可勾勒具体景象。
- **无指标**：不包含 KPI、OKR 或数字目标；指标由 `define-north-star` 或 `design-strategic-goals` 负责。

愿景中应避免：

- **实施细节**：技术、可交付成果或「如何」做到。
- **流行语**：模糊术语，无法阐明未来状态。

---

## 使用场景

- **使命完成后**：明确「我们为何存在」后，建立「我们构建的未来」。
- **战略或方向重置**：根据长期目标重新对齐团队。
- **路线图缺乏目标时**：创建清晰的愿景，使路线图与目标一致。
- **战略链第二层**：构建完整层次结构时，在 `define-mission` 之后运行。

---

## 行为

### 交互策略

- **默认**：项目规范的输出路径（`docs/ARTIFACT_NORMS.md` 或 `.ai-cortex/artifact-norms.yaml`）；否则为 `docs/project-overview/vision.md`。从 `docs/project-overview/mission.md` 或用户处推断使命。
- **选择选项**：若存在多个可能的未来，提供 1–3 个候选陈述并要求用户选择或完善。
- **确认**：覆盖现有愿景文件前；最终持久化前。若缺少使命，确认是否假定目的或建议先运行 `define-mission`。

### 执行过程

1. **加载使命**：从 `docs/project-overview/mission.md` 或用户提供的摘要中读取使命。
2. **引出**：2–5 年后「成功」会是什么样子？我们正在为用户创造什么样的世界？
3. **草案**：愿景陈述（1–3 句）；仅未来状态，无指标或 KPI。
4. **检查一致性**：确保愿景支持使命；必要时与用户一起完善。
5. **持久化**：写入项目约定的路径；若缺少，创建 `docs/project-overview/`。

---

## 输入与输出

**输入**：

- **必填**：使命（使命文档的声明或路径）；项目/产品背景。
- **可选**：现有愿景草案、时间范围、受众。

**输出**：

- **Artifact**：愿景陈述（1–3 句话）。
- **位置**：`docs/project-overview/vision.md`（或按项目规范）。
- **内容**：愿景声明；可选（YAGNI：仅当确有需要时）「与使命一致」「时间范围」说明。
- **生命周期**：living（战略方向改变时更新）。

---

## 限制

### 硬边界（Hard Boundaries）

- 请勿在愿景声明中包含北极星指标、战略目标、OKR 或里程碑。
- 未经用户明确确认，请勿覆盖现有愿景文件。
- 请勿生产超过一份愿景文档；该技能仅生成愿景制品。
- **YAGNI**：愿景文档以陈述为核心；不添加不必要的可选段落。

### Skill Boundaries（避免重叠）

**不要做这些（其他技能负责）**：

- **使命**：根本目的 → Use `define-mission`
- **北极星指标**：单关键指标 → Use `define-north-star`
- **战略目标**：3–5 个结果 → Use `design-strategic-goals`
- **里程碑**：阶段检查点 → Use `define-milestones`
- **路线图、需求或待办** → Use `analyze-requirements`、`capture-work-items` 等

**何时停止并交接**：

- 用户说「已批准」或同等内容 → 愿景完成，hand off to `define-north-star` 或 `design-strategic-goals`
- 用户请求「一个指标」或「北极星」 → Hand off to `define-north-star`
- 用户询问目标或里程碑 → Hand off to `design-strategic-goals` 或 `define-milestones`

---

## 自检

### 核心成功标准（必须满足所有标准）

- [ ] **存在愿景陈述**：一到三句话，仅未来状态（无指标、目标、里程碑）。
- [ ] **与使命一致**：与使命不矛盾；或已注明使命缺失并由用户确认。
- [ ] **用户确认**：用户说「已批准」「看起来不错」「继续」或类似内容。
- [ ] **文档持久化**：写入约定路径（默认 `docs/project-overview/vision.md` 或项目规范）。
- [ ] **尊重范围**：声明中没有北极星、目标或里程碑。
- [ ] **YAGNI/DRY/简洁**：遵循 spec §4 文档制品原则。

### 流程质量检查

- [ ] **使用使命**：起草愿景前是否阅读或请求了使命？
- [ ] **仅未来状态**：是否避免混合指标或 OKR？
- [ ] **质量指南**：是否应用了愿景质量指南（简洁、与使命一致、可想象、无流行语）？
- [ ] **文档制品原则**：是否遵循 YAGNI、DRY、简洁（spec §4）？

### 验收测试

**读者能否理解该项目试图创造什么样的长期未来，并看到其支持使命？**

如果否：愿景不完整或错位。根据使命进行细化和重新检查。
如果是：愿景完成。继续交接或停止。

---

## 示例

### 示例 1：使命已存在时定义愿景

**背景**：使命为「我们的存在是为工程团队提供单一、可靠的方式将服务从代码部署到生产。」用户要求定义愿景。

**流程**：引出 2–5 年目标，如「每个团队仅需一键，即可在 5 分钟内交付生产，并具备全面审核与回滚。」起草愿景；检查是否支持使命。用户确认。写入 `docs/project-overview/vision.md`。

**结果**：愿景持久化；交接至 `define-north-star`（如「每周 5 分钟内成功部署数」）或 `design-strategic-goals`。

### 示例 2：使命尚未定义（边界场景）

**背景**：用户要求「定义我们的愿景」，但不存在使命文档。

**流程**：询问是否从 README 或上下文中假定目的，或建议先运行 `define-mission`。若用户同意继续，在愿景文档中注明假定目的；起草愿景并与用户确认。持久化；建议稍后补充使命以完善战略链。

**结果**：愿景持久化，附可选「假定目的」注释；用户可稍后运行 `define-mission` 完成链。
