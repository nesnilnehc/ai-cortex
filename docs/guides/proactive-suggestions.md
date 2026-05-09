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
| 需求登记 | `capture-work-items` | 把自由文本快速登记为结构化条目 |
| 需求评审 | `review-requirements` | 对需求文档做 5 维质量评审 |
| 结构整理 | `tidy-repo` | 检测并清理仓库结构问题 |
| 代码审查 | `orchestrate-code-review` | 统一编排多维度代码审查 |
| 提交交付 | `commit-work` | 生成规范提交并附质量检查 |

> 文档健康检测、SSOT 评估、设计、任务拆解等工作流由 AgentFabric runtime 与 linter / CI 工具承接；判据参考 [rules/doc-health-criteria.md](../../rules/doc-health-criteria.md)、[specs/design-modeling.md](../../specs/design-modeling.md)、[specs/task-modeling.md](../../specs/task-modeling.md)。
