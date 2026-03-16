# 决策：Skill Spec 整体结构审查

**日期**: 2026-03-16  
**状态**: 已采纳  
**范围**: [spec/skill.md](../../../spec/skill.md) 结构合理性与表述一致性

---

## 1. 结构合理性

### 1.1 章节顺序

| 顺序 | 章节 | 评价 |
| :--- | :--- | :--- |
| 1 | File Structure and Naming | 合理：先约定产物形态与命名，再展开元数据与内容要求。 |
| 2 | Required YAML Metadata | 合理：元数据紧跟命名与目录。 |
| 3 | Required Heading Structure | 合理：先规定 SKILL.md 的标题骨架，再在 §4 规定各节内容质量。 |
| 4 | Content Quality | 合理：集中 Self-Check、Restrictions、Interaction、Invocation，与 §3 标题一一对应。 |
| 5 | Metadata Sync | 合理：从单 Skill 写作过渡到仓库级注册与同步。 |
| 6 | agentskills Compatibility | 合理：对外兼容性独立成节，不干扰内部规范。 |
| 7 | Extension and Contribution | 合理：QA 流程与质量门放在扩展与贡献章节。 |
| 8 | I/O Contracts | 合理：可选契约与 §4 行为要求互补；§8.5 发散/收敛与 §1、§4 呼应。 |
| 9 | Repo-level docs | 合理：收尾仓库级产物与脚本依赖。 |

结论：**整体结构清晰，从“单文件结构 → 元数据 → 内容质量 → 仓库与生态 → 可选 I/O → 仓库文档”的递进关系成立。**

### 1.2 层级与冗余

- **§4 与 §8.5**：§4 规定“若 Skill 含发散/收敛则必须满足”的约束（Behavior、Input & Output、Scope、Handoff）；§8.5 提供可选模式、命名建议、示例与 Handoff 规则。二者为“约束 + 指南”关系，**不冗余**。
- **§3.1 与 §4 Scope Boundaries**：§3.1 规定 Scope Boundaries 可放在 Core Objective 内或独立成节；§4 要求“SHOULD 定义 scope”。**一致**：一处规定位置，一处规定必要性。
- **发散/收敛在多处出现**：§1 命名、§4 质量、§4.1 Self-Check、§4.2 Restrictions、§4.3 Execution process、§8.5。已在 §1 增加“详见 §8.5”的交叉引用，**结构可接受**。

### 1.3 建议的微调

- **§8.5 在目录中的可见性**：若 spec 未来增加目录（TOC），建议将 §8.5 列为“Divergent + Convergent Phase Patterns”，便于直达。
- **§7.1 迁移清单**：现有技能迁移到 2.7.0 时，若技能包含发散/收敛，可在“Add Skill Boundaries”后增加一步：“若为两阶段技能：在 Behavior 中标注阶段名称与触发方式，在 Self-Check 中增加阶段别检查”（可选，非必须）。

---

## 2. 内容表述冲突与一致性

### 2.1 已识别并处理的冲突

| 问题 | 处理 |
| :--- | :--- |
| §4 中 “Divergent + Convergent clarity” 条目前有误用的首字符空格 | 已改为与其他列表项一致的 “-” 列表格式。 |

### 2.2 无冲突但需注意的表述

| 位置 | 表述 | 说明 |
| :--- | :--- | :--- |
| §4 “Divergent + Convergent clarity” | “the SKILL **MUST**” | 仅当技能“同时包含发散与收敛”时 MUST 生效；纯发散或纯收敛技能不强制满足全部子项。 |
| §4.1 第 4 点 | “Phase-specific checks (**for Divergent + Convergent skills**)” | 仅两阶段或分阶段技能需要；与 §4 条件一致。 |
| §4.2 第 4 点 | “**when applicable**” | 仅适用于含发散/收敛的 Skill，与 §4、§4.1 一致。 |

### 2.3 与 artifact-contract 的交叉

- **artifact_type 枚举**：[spec/artifact-contract.md](../../../spec/artifact-contract.md) §5 目前仅列 `backlog-item`, `adr`, `design`, `doc-readiness`。skill.md §8.5.3 示例使用 `mission`, `strategic-goals` 及 `path_pattern: docs/project-overview/...`。
- **建议**：在 artifact-contract 的 §2 或 §7 中扩展 artifact 类型表，增加 mission、vision、strategic-goals、roadmap、milestones 等及其 path_pattern，或在 skill spec 中注明“项目可依 artifact-contract §7 扩展类型，此处示例为约定路径”。
- **lifecycle 取值**：artifact-contract §5 为 `snapshot` | `living`；§8.5.3 示例使用 `source-of-truth`。建议二选一：（1）在 artifact-contract 中承认 `source-of-truth` 为合法取值，或（2）将 skill 示例改为 `snapshot`/`living` 以与合同一致。

### 2.4 tags 与 INDEX 的歧义

- **当前**：YAML 模板中 `tags: [at least one tag from INDEX]`。
- **歧义**：`skills/INDEX.md` 为自动生成的技能目录，并非“标签词表”的权威来源；标签通常来自项目约定或 INDEX 生成脚本所读的 manifest/前端。
- **建议**：改为“at least one tag (see project tag vocabulary or INDEX)”或“at least one tag; prefer tags used in `skills/INDEX.md` for consistency”，以明确 INDEX 在此处指“与现有技能标签保持一致”而非“从 INDEX 文件取值”。

---

## 3. 规范强度一致性（MUST / SHOULD / MAY）

- **MUST**：Core Objective、Success Criteria、Acceptance Test、Self-Check 对齐、Restrictions 中的 Skill Boundaries、两阶段技能的四项 Divergent+Convergent 要求。**无冲突**。
- **SHOULD**：Scope Boundaries、Handoff、Behavior 中的 execution process、Phase-specific checks 的“MUST verify”仅针对“含该阶段的技能”。**一致**：SHOULD 用于“建议有”，MUST 用于“若有则必须满足”。
- **MAY**：§8 I/O Contracts、§8.5 模式、evolution metadata、triggers/aliases。**与 MUST/SHOULD 分层清晰。**

---

## 4. 交叉引用与脚本名

- **§5、§9**：`scripts/verify-registry.mjs` 调用 `scripts/generate-skills-docs.mjs`，后者再调用 `generate-skills-index.mjs` 等；§9 描述“verify-registry 先 regen INDEX、skillgraph、scenario-map”与实现一致。
- **§3、§3.1、§4.2**：对 Scope Boundaries、Handoff、§4.2 的引用（如“see §3.1”“see §4.2”）正确。

---

## 5. 结论与后续

- **结构**：章节顺序与层级合理，发散/收敛通过 §1 指向 §8.5 形成闭环。
- **冲突**：无逻辑冲突；已修正 §4 列表缩进。
- **建议后续**：
  1. 与 [spec/artifact-contract.md](../../spec/artifact-contract.md) 对齐：扩展 artifact_type 或约定 mission/vision/roadmap 等路径与 lifecycle 取值。
  2. 澄清 YAML 中 `tags` 与 INDEX 的关系（见 2.4）。
  3. （可选）在 §7.1 迁移清单中为两阶段技能增加一句提醒。
