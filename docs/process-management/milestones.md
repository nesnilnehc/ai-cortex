# 里程碑

里程碑由 [strategic goals](../project-overview/strategic-goals.md) 推导而来。每个里程碑至少映射到一个目标。此处不含 backlog 或需求；详见 backlog 与 roadmap 以获取具体工作。

---

## 目标衍生里程碑

### M1：可发现性基线

**范围**：意图优先路由、INDEX、manifest 为发现能力的主要稳定入口。

**成功标准**：团队能按任务或意图找到正确能力；intent-routing、INDEX.md、manifest.json 为 canonical 且持续维护。

**映射至**：目标 1（Discoverability，可发现性）。

---

### M2：可复用性基线

**范围**：技能为单文件、可组合，且可跨项目采纳。

**成功标准**：Spec 与 related_skills 支持组合；技能可以最低摩擦安装或加入项目；核心能力定义无重复。

**映射至**：目标 2（Reusability，可复用性）。

---

### M3：治理基线

**范围**：共享 Spec、质量门槛与生命周期，使 Agent 行为可审查、可治理。

**成功标准**：Spec（skill.md）定义结构与质量；ASQM/curate-skills 与 Self-Check 已在使用；技能边界与 Handoff 清晰。

**映射至**：目标 3（Governance，治理）。

---

### M4：生态存在

**范围**：能力层可通过团队已使用的渠道与工具获取。

**成功标准**：目录可通过 skills.sh、SkillsMP 及至少一种 IDE 或 Agent 生态路径安装或发现；采纳摩擦低。

**映射至**：目标 4（Ecosystem adoption，生态采纳）。

---

## 完成状态（截至评估时）

| Milestone | Status | Evidence |
| :--- | :--- | :--- |
| **M1: Discoverability baseline** | Done | `skills/intent-routing.json`、`skills/intent-routing.md`、`skills/INDEX.md`、`manifest.json` 为 canonical；`verify-registry.mjs` 保持同步；AGENTS.md 描述意图优先发现。 |
| **M2: Reusability baseline** | Done | Spec 定义结构与 related_skills；技能为单文件（SKILL.md）；`npx skills add`、install-fallback 及按技能安装降低采纳摩擦。 |
| **M3: Governance baseline** | Done | `spec/skill.md` 定义结构与质量；`curate-skills` 与 `ASQM_AUDIT.md` 已在使用；技能具备 Restrictions、Scope Boundaries 与 Self-Check。 |
| **M4: Ecosystem presence** | Done | 目录可通过 skills.sh（`npx skills add`）安装；SkillsMP 已文档化；Cursor 与 Trae 通过 `install-rules` 与 rules 注册表支持；README 与 INDEX 记录渠道。 |

四个目标衍生里程碑均已达成。下一步：将其作为发布对齐的稳定检查点，并在评估漂移时供 `align-planning` / `run-checkpoint` 使用。

---

## Release alignment（发布对齐参考）

版本与发布里程碑在 [CHANGELOG](../../CHANGELOG.md) 与 [Evolution Roadmap](../designs/2026-03-02-ai-cortex-evolution-roadmap.md) 中追踪。上述战略衍生里程碑为成果检查点；发布里程碑（如 v2.1.0、v2.2.x）在完成时可与 M1–M4 之一或多条对齐。
