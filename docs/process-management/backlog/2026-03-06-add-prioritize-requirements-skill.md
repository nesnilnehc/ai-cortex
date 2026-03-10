---
type: requirement
date: 2026-03-06
status: captured
source: user
trace_id:
---

# 增加需求排序技能 (Add Prioritize Requirements Skill)

## Problem / Need

项目缺少对 backlog 或需求列表进行优先级排序的专门技能。当 Agent 或用户需要从多条目中决定执行顺序时（例如 capture-work-items 产出多条、triaged 前排序、里程碑规划前选优），缺乏可注入的、可复用的排序/优先级方法论，导致依赖临时判断或手工整理。

## Acceptance Criteria

- [ ] 新增 SKILL 符合 `spec/skill.md` 结构，包含 Core Objective、Scope Boundaries、Self-Check
- [ ] 技能提供明确的 prioritization 框架或方法（如 MoSCoW、RICE、价值/成本矩阵、或与 orchestrate-governance-loop 兼容的排序流程）
- [ ] 技能已注册到 `skills/INDEX.md` 与 `manifest.json`，通过 `verify-registry.mjs` 校验
- [ ] 可与 `capture-work-items`、`analyze-requirements`、`orchestrate-governance-loop` 等形成清晰 handoff

## Notes

- 可与 `capture-work-items`（产出 captured 条目）、`align-execution`（目标对齐）衔接
- 技能命名建议：`prioritize-requirements` 或 `prioritize-work-items`
