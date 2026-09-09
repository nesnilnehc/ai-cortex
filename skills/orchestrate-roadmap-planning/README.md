# 编排路线图规划（Orchestrate Roadmap Planning）

按固定 9 步串联从战略目标到晋升的原子技能，跑完一轮 roadmap planning ceremony。只做编排，不做领域分析。

## 用途

**存在价值是提前满足下游的 halt 条件。** 手工调用时最常见的浪费是：一路做到 `promote-roadmap-items` 才发现 roadmap 缺容量分配，halt，回头跑 `define-roadmap`，再重来一遍。本技能把这类前置条件在调用前就检查并补齐。

每步标注三档——**必选**（条件命中即执行，不可跳过）、**默认**（可显式跳过）、**推荐**（只提示不自动执行）。档位是各原子技能既有约束的机械映射，不是编排层的判断。

## 何时使用

- **完整规划**：需要从战略到晋升走完一轮，而不是单点操作
- **不确定卡在哪**：不清楚当前该跑哪个技能时，由体检步骤判定
- **新项目冷启动**：治理文档大面积缺失，需要按序补齐

单步操作请直接调用对应原子技能——只想晋升用 `promote-roadmap-items`，只想体检用 `review-roadmap`。

## 输入

- 可选的范围提示与未登记的原始输入
- 治理文档路径按项目规范自动发现

## 输出

单一聚合报告：各步执行结果、跳过步骤及原因、roadmap 变更清单、容量使用报告、未解决 findings、下一步建议。

## 与既有编排层的边界

| 技能 | 覆盖面 | 关系 |
| :--- | :--- | :--- |
| `plan-next` | 跨层，只读 | 本技能不重新实现其目标树遍历 |
| `orchestrate-governance-step` | 跨层，执行 1 条建议 | 可将本技能当作一条可执行动作调用 |
| 本技能 | 仅路线图纵切片 | 不得反向调用上述两者 |

一句话区分：`plan-next` 回答「整个项目下一步该干什么」，本技能回答「路线图这条线，从战略到晋升一次走完」。

## 安装

统一由 AI Cortex 的 canonical 安装管理，见仓库根 [README](../../README.md#-安装与使用)。

## 相关技能

编排的原子技能：`review-roadmap`、`design-strategic-goals`、`define-roadmap`、`capture-work-items`、`prioritize-backlog`、`map-item-dependencies`、`promote-roadmap-items`、`update-roadmap`、`archive-milestone`。

## 完整定义

参见 [SKILL.md](./SKILL.md)。
