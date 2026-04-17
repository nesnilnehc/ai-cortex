# define-roadmap

从战略目标推导由里程碑节点组成的路线图；每节点为阶段检查点，含成功标准与目标可追溯性。

## 用途

生成路线图文档，其中每个节点为里程碑（名称、范围、成功标准、目标映射）。不定义目标或待办事项。输出保存至 `docs/process-management/roadmap.md` 或 `milestones.md`（依项目规范）。

## 何时使用

- **战略目标之后**：定义阶段或主要检查点，表示各目标的进展水平。
- **规划周期**：为接下来 1–2 个阶段确定「完成的内容」。
- **治理门**：提供里程碑路线图，供 `plan-next` 或 `align-planning` 评估。
- **待办之前**：提供路线图，待办项目可按倡议或主题分组。

## 输入

- 战略目标（文档或路径）；项目背景。
- 可选：vision/NSM；时间范围；阶段偏好。

## 输出

- 路线图文档（roadmap.md 或 milestones.md）：有序里程碑节点，含范围、成功标准、目标映射。

## 安装

```bash
npx skills add nesnilnehc/ai-cortex --skill define-roadmap
```

## 相关技能

- `design-strategic-goals` — 上游：路线图节点（里程碑）源自战略目标。
- `define-strategic-pillars` — 可选输入：支柱可引导路线图主题分组。
- `align-planning`、`plan-next` — 下游：治理时引用里程碑状态。

## 完整定义

请参阅 [SKILL.md](./SKILL.md) 了解行为、限制与示例。
