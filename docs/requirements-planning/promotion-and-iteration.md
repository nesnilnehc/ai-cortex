---
artifact_type: requirements
created_by: ai-cortex
lifecycle: living
created_at: 2026-03-24
status: active
---

# 推广与迭代 Requirements

**Date:** 2026-03-06
**Status:** Validated
**Approved by:** User

## Problem Statement

AI Cortex 作为 skill 资产库，需要扩大认知度与采用率，并建立可持续的迭代节奏。当前痛点：技能定义完备但推广渠道有限、迭代优先级依赖临时决策，缺乏可度量的推广效果与迭代计划，制约项目长期价值释放。

## Need Hierarchy

### Must Have (V1)

| ID | Need | Acceptance Criteria |
| :--- | :--- | :--- |
| R-01 | 推广策略可执行 | 存在至少 2 个明确的推广渠道及每季度可执行动作清单 |
| R-02 | 迭代计划可追溯 | 里程碑与 roadmap 阶段一一对应，未完成项可追溯到具体 roadmap 条款 |
| R-03 | 成功指标可度量 | 至少 3 个可量化指标（如 install 量、技能数、spec 采纳）及基准值 |
| R-04 | 设计文档已落稿 | 推广与迭代设计拆分写入 `docs/designs/`，并纳入 milestones 引用 |

### Should Have (V1 if time permits)

| ID | Need | Acceptance Criteria |
| :--- | :--- | :--- |
| R-05 | 社区基础设施就绪 | CONTRIBUTING.md、Issue 模板已存在（roadmap D10 Phase 1 已完成） |
| R-06 | 推广素材可复用 | README、AGENTS.md、技能索引具备可直接分享的表述 |

### Could Have (Post-V1)

| ID | Need | Trigger to reconsider |
| :--- | :--- | :--- |
| R-07 | 社区活动/分享 | 当贡献者或外部关注度达到一定阈值时评估 |
| R-08 | 多语言文档 | 当非英文用户反馈成为显著需求时 |
| R-09 | 推广自动化（如发布推文） | 当手动推广成为瓶颈时 |

## Constraint Inventory

### Real Constraints (Validated)

- Solo 或小团队维护；推广与迭代需低人力投入
- skills.sh、SkillsMP、Claude Plugin 为已有分发渠道
- roadmap Layer D（Ecosystem & Distribution）已定义 D9/D10

### Assumptions (Unvalidated)

- 当前 install/使用数据可通过 skills.sh 或 Plugin 获取
- 推广效果可通过 GitHub stars、 forks、引用量间接反映

## Scope Definition

- **In scope (V1):** 推广策略文档、迭代计划拆分、里程碑更新、成功指标定义
- **Out of scope:** 付费推广、跨平台自动化发布、社区活动执行
- **Walking skeleton:** 设计文档 + milestones 中明确列出「推广与迭代」相关条目

## Open Questions

- 基准指标（如当前 install 量）如何获取，需与 skills.sh / Plugin 维护方确认
