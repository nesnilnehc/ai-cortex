---
artifact_type: guide
created_by: ai-cortex
lifecycle: living
created_at: 2026-03-26
status: active
---

# 主动建议表（阶段→技能）

本表用于在不同协作阶段给出建议技能入口。  
说明：该表为建议映射，不替代任务语义匹配。

| 阶段 | 建议技能 | 说明 |
| :--- | :--- | :--- |
| 路线图规划 | `orchestrate-roadmap-planning` | 从战略目标到条目进入 Now 走完一轮；先体检再决定执行哪几步 |
| 路线图体检 | `review-roadmap` | 按 roadmap-quality 判据评估既有路线图，出 findings |
| 路线图运维 | `update-roadmap` | 改条目状态、挪期并计算下游影响 |
| 需求登记 | `capture-work-items` | 把自由文本快速登记为结构化条目 |
| 优先级排序 | `prioritize-backlog` | 四框架并行重评积压，呈现分歧由人决策 |
| 依赖排查 | `map-item-dependencies` | 晋升前登记条目间依赖，阻断被卡住的条目 |
| 需求评审 | `review-requirements` | 对需求文档做 5 维质量评审 |
| 代码审查 | `orchestrate-code-review` | 统一编排多维度代码审查 |
| 提交交付 | `commit-work` | 生成规范提交并附质量检查 |

> 路线图这条链的完整用法（入口、常见 halt、依赖为什么排在晋升前）见 [roadmap-planning-usage.md](./roadmap-planning-usage.md)。

> 文档健康检测、SSOT 评估、设计、任务拆解等工作流由 AgentFabric runtime 与 linter / CI 工具承接；判据参考 [rules/doc-health-criteria.md](../../rules/doc-health-criteria.md)、[specs/functional-design-modeling.md](../../specs/functional-design-modeling.md)、[specs/technical-design-modeling.md](../../specs/technical-design-modeling.md)、[specs/task-modeling.md](../../specs/task-modeling.md)。
