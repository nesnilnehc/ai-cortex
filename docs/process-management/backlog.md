---
artifact_type: backlog
created_by: capture-work-items
lifecycle: living
created_at: 2026-03-24
status: active
---

# Backlog 索引

**目的**：工作条目、技能请求与计划任务的权威索引。支持 assess-doc-readiness 的 Backlog 层追溯。

**相关**：
- [roadmap (strategic-plan)](roadmap.md) — 项目路线图和里程碑
- [promotion-iteration-tasks (execution-plan)](promotion-iteration-tasks.md) — 发版与迭代任务详情
- [skills/INDEX.md (reference)](../../skills/INDEX.md) — 技能目录
- [manifest.json (reference)](../../manifest.json) — 机器可读的能力列表

---

## 已捕获的 Backlog 条目

通过 `capture-work-items` 或等效方式捕获的单项工作。每项对应 `backlog/` 下的一个文件。

| Date | Item | Status | Path |
| :--- | :--- | :--- | :--- |
| 2026-03-06 | 增加需求排序技能 (Add Prioritize Requirements Skill) | captured | [backlog/2026-03-06-add-prioritize-requirements-skill.md](backlog/2026-03-06-add-prioritize-requirements-skill.md) |
| 2026-03-23 | AGENTS.md 重构计划 | completed | [backlog/2026-03-23-agents-md-refactor-plan.md](backlog/2026-03-23-agents-md-refactor-plan.md) |

---

## 计划工作（来自设计）

下表汇总了来自 [推广与迭代设计 (design)](../designs/2026-03-06-promotion-and-iteration.md) 的计划 Epic。

**详细的任务、验收标准、质量门禁请见** [promotion-iteration-tasks.md (execution-plan)](promotion-iteration-tasks.md)。

本表的职责：
- 提供 Epic 的快速导航
- 显示与需求和设计文档的追溯关系

完整的任务定义和执行细节：[promotion-iteration-tasks.md (execution-plan)](promotion-iteration-tasks.md)

| Epic | Scope | Priority |
| :--- | :--- | :--- |
| T1 分发渠道验证 | scripts/verify-* | Phase A |
| T2 发布流程自动化 | pre-release-check、CHANGELOG 辅助 | Phase A/B |
| T3 指标采集与报告 | metrics、季度模板 | Phase B |
| T4 CI 集成 | .github/workflows | Phase C |
| T5 季度检视流程 | quarterly-review-sop | Phase D |

---

## 技能目录引用

- **skills/INDEX.md** — canonical 技能列表、tags、版本、稳定性
- **manifest.json** — 机器可读的能力列表，用于发现

新增技能请求（如来自已捕获条目）需按 `spec/skill.md` 校验，并在关闭前通过 INDEX 与 manifest 注册。
