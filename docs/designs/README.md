# Design snapshots

Functional and technical designs, and the task lists derived from them. Each file records a design **as it stood on its date** — `lifecycle: snapshot`, so it is not revised as the code moves on. To find out what is true today, read the asset the design produced, not the design.

The data contract for each type is in [specs/functional-design-modeling.md](../../specs/functional-design-modeling.md), [specs/technical-design-modeling.md](../../specs/technical-design-modeling.md) and [specs/task-modeling.md](../../specs/task-modeling.md). Paths and naming follow [docs/ARTIFACT_NORMS.md](../ARTIFACT_NORMS.md).

Two of the snapshots below are written in Chinese. They predate the English-first conversion and stay as written, for the reason given in [docs/LANGUAGE_SCHEME.md](../LANGUAGE_SCHEME.md) §2.

## The index

| Date | Design | Type | Anchor |
|---|---|---|---|
| 2026-04-28 | [ASQM Skill Governance Refactor](./2026-04-28-asqm-skill-governance-refactor-technical-design.md) | technical-design | [ADR 0008](../adr/0008-replace-asqm-with-acceptance-criteria.md) |
| 2026-05-08 | [治理熵清理：孤儿技能触发路径与里程碑归档生命周期](./2026-05-08-orphan-skills-cleanup-technical-design.md) | technical-design | — |
| 2026-09-11 | [Profiled engineering Rule governance](./2026-09-11-engineering-rule-governance-technical-design.md) | technical-design | [ADR 0012](../adr/0012-adopt-profiled-engineering-rules.md) |
| 2026-09-17 | [Research skill user journeys](./2026-09-17-research-skills-functional-design.md) | functional-design | [AIC-REQ-01](../requirements-planning/AIC-REQ-01.md) |
| 2026-09-17 | [Composable research skills](./2026-09-17-research-skills-technical-design.md) | technical-design | [the functional design](./2026-09-17-research-skills-functional-design.md) |
| 2026-09-17 | [Implement composable research skills](./research-skills-tasks.md) | tasks | [the technical design](./2026-09-17-research-skills-technical-design.md) |

## Adding one

Name the file `YYYY-MM-DD-{topic}-{functional,technical}-design.md`, fill in the frontmatter its Spec requires including `parent`, and append a row here. A design nothing links to cannot be found by a reader, and CI reports it as an orphan.

Write it for someone who took part in no conversation. A snapshot is not revised once it is dated, so a sentence that leans on a discussion the reader cannot reach stays unhelpful for good: `2026-09-17-research-skills-technical-design.md` argues against a layout "from the earlier discussion", and nothing in the repository says which discussion or what it concluded. Name the option and the reason instead. The temporary-document check in CI does not catch this — a dated design in this directory is a labelled temporary document, which is exactly what it is allowed to be.
