# Proposed Strategy Skills (Strategy Capability Chain)

Proposal for additional AI Cortex Skills that complete the strategic planning chain from long-term direction to execution checkpoints. Existing skills: `define-mission`, `define-vision`, `define-north-star`, `design-strategic-goals`, `define-milestones`. New/retained skills fill gaps in **strategic structure** (pillars) and **planning translation** (roadmap).

**Chain**: Mission → Vision → North Star → **Strategic Pillars** → Strategic Goals → Milestones → Roadmap.

**Align 系列技能重规划**: 见 [20260316-align-skills-replan.md](decisions/20260316-align-skills-replan.md)。不保留 define-okrs、define-initiatives、validate-strategy-chain、align-backlog-to-strategy；align 家族按「对齐层」拆分（align-planning = 规划层，align-architecture = 设计/代码层）。

---

## 1. define-roadmap

**Purpose**: Translate strategic goals and milestones into a time-bound roadmap of initiatives or themes (with optional timeframes). Produces a single roadmap document that bridges strategy and delivery planning without defining goals or writing backlog items.

**Artifact produced**: `docs/process-management/roadmap.md` (or project norms). Living document: initiatives/themes, optional quarters or phases, traceability to milestones and goals.

**When to use**: After `define-milestones`; when the team needs a visible plan that connects strategy to release or sprint planning. Before or in parallel with backlog population.

**Spec alignment**: Verb-noun; single document-artifact; Core Objective; Skill Boundaries (do not define mission/vision/NSM/goals/milestones; do not create backlog items); Handoff to backlog planning.

---

## 2. define-strategic-pillars

**Purpose**: Derive 3–5 strategic pillars (high-level themes) from vision and North Star that structure and guide strategic goals and roadmap. Goals and roadmap themes can be grouped under pillars.

**Artifact produced**: `docs/project-overview/strategic-pillars.md` (or project norms). Living: 3–5 pillars with name, short description, alignment to vision/NSM.

**When to use**: After vision and North Star; before or with `design-strategic-goals` so goals can map to pillars. Fourth layer: Mission → Vision → North Star → Pillars → Goals → Milestones → Roadmap.

**Spec alignment**: Verb-noun; document-artifact; Core Objective; Skill Boundaries (do not define mission/vision/NSM/goals/roadmap); Handoff to `design-strategic-goals` or `define-roadmap`.

---

## Summary Table

| Skill | Artifact | Position in chain |
| :--- | :--- | :--- |
| define-roadmap | roadmap.md | Goals + Milestones → execution plan |
| define-strategic-pillars | strategic-pillars.md | Vision + North Star → structure for goals/roadmap |

---

## Implementation Notes

- **Naming**: Verb-noun; no overlap with existing strategy skills.
- **Artifact paths**: `docs/process-management/` for roadmap; `docs/project-overview/` for strategic-pillars, strategy-summary. Follow [spec/artifact-contract.md](../spec/artifact-contract.md) and project norms.
- **related_skills**: Each skill lists upstream/downstream strategy skills and, where relevant, `align-planning`, `run-checkpoint`.
