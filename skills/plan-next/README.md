# 计划下一步

以存量 mission、vision、backlogs 等为输入源，分析项目治理状态并产出下一行动建议。输入源缺失时，优先建议完善输入源。

## 用途

**阶段 0（输入源盘点）**：检查 mission、vision、north-star、strategic-goals、milestones、roadmap、backlog 存在性与质量；缺失时，将完善输入源作为首要推荐行动。

**阶段 0.5（规划准备门）**：当项目文档结构缺失时，运行 discover-docs-norms、bootstrap-docs 或 assess-docs；准备度过低时短路。

**阶段 1**：运行 align-planning（完整）→ assess-docs，按输出驱动添加 align-architecture、run-repair-loop、design-solution、analyze-requirements。汇总到单一周期报告。

## 何时使用

- 任务完成后 — 验证对齐与文档充分性前处理下一优先级
- 里程碑收尾 — 全面治理检查
- 发布候选 — 运行设计/对齐/文档准备门
- 定期迭代 — 检查项目状态并获取下一步行动
- 输入源缺失 — 发现 mission/vision/backlog 等缺失时产出补齐建议

## 输入

- 存量治理文档（mission、vision、north-star、strategic-goals、milestones、roadmap、backlog）
- 可选：触发事件、目标范围、模式覆盖

## 输出

- 周期报告：`docs/calibration/cognitive-loop.md`
- 输入源清单、路由顺序、汇总发现、阻碍、Recommended Next Tasks

## 安装

```bash
npx skills add nesnilnehc/ai-cortex --skill plan-next
```

## 相关技能

- `align-planning` — 规划回溯与漂移检测
- `align-architecture` — 架构与代码合规
- `assess-docs` — 文档证据评估
- `discover-docs-norms` — 建立制品路径（阶段 0.5）
- `bootstrap-docs` — 创建文档结构（阶段 0.5）
- `define-mission`、`define-vision`、`define-north-star` 等 — 完善缺失输入源

## 完整定义

请参阅 [SKILL.md](./SKILL.md) 了解行为、限制与示例。
