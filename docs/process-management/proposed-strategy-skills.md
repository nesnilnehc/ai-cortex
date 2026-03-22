# 拟议战略技能（策略能力链）

针对从长期方向到执行检查点的战略规划链，拟议补充 AI Cortex 技能。现有技能：`define-mission`、`define-vision`、`define-north-star`、`design-strategic-goals`、`define-roadmap`。新增/保留技能填补**战略结构**（支柱）与**规划转化**（路线图）的缺口。

**链**：Mission → Vision → North Star → **Strategic Pillars（战略支柱）** → Strategic Goals → Roadmap（里程碑节点）。注：`define-milestones` 已移除并合并至 `define-roadmap`（2026-03-22），里程碑即路线图节点。

**Align 系列技能重规划**：见 [20260316-align-skills-replan.md](decisions/20260316-align-skills-replan.md)。不保留 define-okrs、define-initiatives、validate-strategy-chain、align-backlog-to-strategy；align 家族按「对齐层」拆分（align-planning = 规划层，align-architecture = 设计/代码层）。

---

## 1. define-roadmap

**目的**：将战略目标与里程碑转化为有时限的路线图（倡议或主题，可含时间框架）。产出单一路线图文档，作为战略与交付规划之间的桥梁，不定义目标或编写 backlog 条目。

**产出 artifact**：`docs/process-management/roadmap.md`（或项目规范约定路径）。Living 文档：倡议/主题、可选的季度或阶段、与里程碑及目标的追溯关系。

**何时使用**：在 `design-strategic-goals` 之后；当团队需要连接战略与发布或 Sprint 规划的可见计划时。在 backlog 填充之前或与之并行。路线图节点即里程碑。

**Spec 对齐**：动词-名词；单一 document-artifact；Core Objective；Skill Boundaries（不定义 mission/vision/NSM/goals/milestones；不创建 backlog 条目）；Handoff 至 backlog 规划。

---

## 2. define-strategic-pillars

**目的**：从 vision 与 North Star 推导 3–5 个战略支柱（高层主题），用于组织并引导战略目标与路线图。目标与路线图主题可按支柱分组。

**产出 artifact**：`docs/project-overview/strategic-pillars.md`（或项目规范约定路径）。Living：3–5 个支柱，含名称、简短描述、与 vision/NSM 的对齐关系。

**何时使用**：在 vision 与 North Star 之后；在 `design-strategic-goals` 之前或与之并行，以便目标可映射到支柱。第四层：Mission → Vision → North Star → Pillars → Goals → Milestones → Roadmap。

**Spec 对齐**：动词-名词；document-artifact；Core Objective；Skill Boundaries（不定义 mission/vision/NSM/goals/roadmap）；Handoff 至 `design-strategic-goals` 或 `define-roadmap`。

---

## Summary Table（汇总表）

| Skill | Artifact | Position in chain |
| :--- | :--- | :--- |
| define-roadmap | roadmap.md | Goals + Milestones → execution plan |
| define-strategic-pillars | strategic-pillars.md | Vision + North Star → structure for goals/roadmap |

---

## Implementation Notes（实施说明）

- **命名**：动词-名词；与现有战略技能无重叠。
- **Artifact 路径**：路线图置于 `docs/process-management/`；战略支柱置于 `docs/project-overview/`。遵循 [spec/artifact-contract.md](../../spec/artifact-contract.md) 及项目规范。
- **related_skills**：每个技能列出上下游战略技能，以及（在适用时）`align-planning`、`run-checkpoint`。
