---
artifact_type: adr
path_pattern: docs/process-management/decisions/YYYYMMDD-{slug}.md
created_at: "2026-03-16"
lifecycle: living
---

# 执行链：Requirements → Design → Tasks

**日期**: 2026-03-16  
**状态**: 已采纳  
**类型**: 流程约定  
**相关**: [analyze-requirements](../../../skills/analyze-requirements/SKILL.md)、[design-solution](../../../skills/design-solution/SKILL.md)、[breakdown-tasks](../../../skills/breakdown-tasks/SKILL.md)

---

## 1. 目标与范围

针对「从想法到可执行任务」的交付路径，约定三个核心技能及其产出物，形成可被下游消费的单一事实源链：**需求 → 设计 → 任务**。

---

## 2. 执行链概览

| 阶段 | Skill 名称 | 输出 artifact | 目的 | 特点 |
| :--- | :--- | :--- | :--- | :--- |
| 1. 需求 | `analyze-requirements` | `requirements.md`（或 `docs/requirements-planning/<topic>.md`） | 把用户想法、业务需求、约束条件、验收标准转成结构化需求文档 | 清晰定义「做什么」；可被下游 design/tasks 消费 |
| 2. 设计 | `design-solution` | `design.md`（或 `docs/design-decisions/YYYY-MM-DD-<topic>.md`） | 基于 requirements 生成详细设计（架构、组件、数据流、trade-offs） | 严格 No implementation；文档为单一事实源；保证下游可直接拆任务 |
| 3. 拆任务 | `breakdown-tasks` | `tasks.md`（或 `docs/process-management/tasks/YYYY-MM-DD-<topic>.md`） | 把 design 拆解成可执行任务清单 | 每条任务含依赖、验收标准、负责人或 AI 执行线索；形成可追踪的 implementation plan |

---

## 3. Artifact 与路径

- **requirements**：以 [specs/artifact-contract.md](../../../specs/artifact-contract.md) 及项目 `docs/ARTIFACT_NORMS.md` 为准；默认可落盘为单文件 `requirements.md` 或 `docs/requirements-planning/<topic>.md`。
- **design**：遵循 artifact-contract 的 `design` 类型，路径 `docs/design-decisions/YYYY-MM-DD-<topic>.md`；单文件别名 `design.md` 可在项目约定下使用。
- **tasks**：任务清单；默认路径 `docs/process-management/tasks/YYYY-MM-DD-<topic>.md` 或项目约定的 `tasks.md`。

---

## 4. Handoff 与顺序

- **analyze-requirements → design-solution**：需求文档经用户确认后，将 requirements 文档路径或内容作为 design-solution 的输入。
- **design-solution → breakdown-tasks**：设计文档经用户确认后，将 design 文档路径或内容作为 breakdown-tasks 的输入。
- 任一阶段可独立调用（例如已有 requirements 则直接调用 design-solution）；完整执行时建议按 1 → 2 → 3 顺序。

---

## 5. 与现有技能的关系

- `design-solution`：可从「模糊想法」直接产出设计，也可明确以 requirements 为输入；执行链推荐在需求已有时以 requirements 为输入调用，以保证「需求 → 设计」可追溯。
- `capture-work-items`：轻量记录需求/缺陷/事项，不做深度需求分析；需深度需求时 hand off 到 `analyze-requirements`。

---

## 6. 参考

- [specs/skill.md](../../../specs/skill.md) — 技能结构与本约定一致
- [specs/artifact-contract.md](../../../specs/artifact-contract.md) — 文档路径与命名
