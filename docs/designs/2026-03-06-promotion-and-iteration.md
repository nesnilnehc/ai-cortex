# 推广与迭代 Design

**Date:** 2026-03-06
**Status:** Approved
**Approved by:** User
**Method:** design-solution skill (structured design breakdown)

## Goal

将「推广」与「迭代」需求拆分为可执行的设计方案，与 Evolution Roadmap 和 milestones 对齐，形成可持续的发布与推广节奏。

## Architecture

- **推广层**：基于现有渠道（skills.sh、SkillsMP、Claude Plugin）制定渠道级动作清单，辅以 README/AGENTS.md 等可分享素材。
- **迭代层**：以 roadmap Phase 1–4 和 milestones 为骨架，将「推广与迭代」作为横切关注点注入各阶段。
- **度量层**：定义可量化指标及采集方式，用于评估推广与迭代效果。

## Components

### 1. 推广策略 (Promotion Strategy)

推广渠道的**唯一权威清单**为 `docs/process-management/promotion-channel-checklist.md`，本文档仅描述策略原则与迭代节奏。

**V1 交付**：推广渠道清单维护在 `docs/process-management/promotion-channel-checklist.md`，每季度检视一次。

### 2. 迭代计划拆分 (Iteration Breakdown)

按 roadmap Phase 映射到 milestones，并显式标注推广与迭代相关事项：

| Phase | Roadmap 条款 | Milestone 映射 | 推广/迭代相关 |
| :--- | :--- | :--- | :--- |
| 1 | E12, A1, A2 | v2.0.0（已完成） | CI 与质量门自动化支撑可发布质量 |
| 2 | E11, B3, B4 | v2.2.x | TS/React 技能覆盖；推广 README 中的技能列表 |
| 3 | C8, C7, B5 | v2.x（composition） | 编排与库级 review；推广 onboarding 场景 |
| 4 | D9, D10 | v3.0 候选 | Plugin 同步策略；CONTRIBUTING + Issue 模板 |

**V1 交付**：milestones 增加「推广与迭代」作为横切 scope；每个 milestone 的 scope 列中包含 1–2 条推广/迭代条目。

### 3. 成功指标 (Success Metrics)

| 指标 | 说明 | 基准（2026-03） | 目标 |
| :--- | :--- | :--- | :--- |
| Skills 数量 | `skills/` 下 canonical 技能数 | ~36 | 持续增长，符合 roadmap |
| Spec 采纳率 | 符合 spec 的技能占比 | 100% | 维持 100% |
| 分发渠道 | skills.sh、Plugin、INDEX 可访问性 | 3 渠道 | 保持并验证可用 |
| 文档就绪 | README、AGENTS.md、INDEX 更新及时性 | 随版本 | 随每次 release 更新 |

**V1 交付**：指标定义写入本文档；基准与目标在 milestones 检视时更新。

## Data Flow

- 发布新版本 → 更新 CHANGELOG → 同步 README/AGENTS.md → 必要时更新 Plugin/marketplace
- 新增/修改技能 → 运行 curate-skills / ASQM → 更新 INDEX → 符合 D9 则考虑 Plugin 同步
- 季度检视 → 对照指标与推广动作清单 → 更新 milestones 与本文档

## Error Handling

- 若某渠道不可用（如 skills.sh 变更），记录在 Open Questions，并在文档中标注备用方案。
- 若指标无法采集，采用替代指标（如 GitHub stars、 forks）并注明限制。

## Trade-offs Considered

| 方案 | 优点 | 缺点 | 选择理由 |
| :--- | :--- | :--- | :--- |
| A: 轻量策略（推荐） | 低人力；与现有 roadmap 一致 | 推广效果依赖被动发现 | 符合 solo 维护约束 |
| B: 主动社区运营 | 曝光度高 | 需持续投入；超出当前人力 | 留作 Post-V1 |
| C: 付费推广 | 可控流量 | 成本与 ROI 未知 | 不在 V1 范围 |

## Acceptance Criteria

- [x] 推广渠道清单已定义并写入设计文档
- [x] 迭代计划与 roadmap Phase 一一对应
- [x] 成功指标有说明、基准与目标
- [x] milestones 已更新，包含推广与迭代 scope
- [x] 需求文档 `docs/requirements-planning/promotion-and-iteration.md` 已创建
