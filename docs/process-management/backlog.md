# Backlog Index

**Purpose:** Canonical index for work items, skill requests, and planned tasks. Enables assess-doc-readiness Backlog layer traceability.

**Related:** [milestones](milestones.md) | [promotion-iteration-tasks](promotion-iteration-tasks.md) | [skills/INDEX.md](../../skills/INDEX.md) | [manifest.json](../../manifest.json)

---

## Captured Backlog Items

Individual work items captured via `capture-work-items` or equivalent. One file per item under `backlog/`.

| Date | Item | Status | Path |
| :--- | :--- | :--- | :--- |
| 2026-03-06 | 增加需求排序技能 (Add Prioritize Requirements Skill) | captured | [backlog/2026-03-06-add-prioritize-requirements-skill.md](backlog/2026-03-06-add-prioritize-requirements-skill.md) |

---

## Planned Work (from Design)

Task breakdown derived from [promotion-and-iteration design](../designs/2026-03-06-promotion-and-iteration.md). See [promotion-iteration-tasks](promotion-iteration-tasks.md) for Epic/Task detail and traceability to requirements.

| Epic | Scope | Priority |
| :--- | :--- | :--- |
| T1 分发渠道验证 | scripts/verify-* | Phase A |
| T2 发布流程自动化 | pre-release-check, CHANGELOG 辅助 | Phase A/B |
| T3 指标采集与报告 | metrics, 季度模板 | Phase B |
| T4 CI 集成 | .github/workflows | Phase C |
| T5 季度检视流程 | quarterly-review-sop | Phase D |

---

## Skill Catalog References

- **skills/INDEX.md** — canonical skill list, tags, versions, stability
- **manifest.json** — machine-readable capability list for discovery

New skill requests (e.g. from captured items) are validated against `spec/skill.md` and registered via INDEX + manifest before closure.
