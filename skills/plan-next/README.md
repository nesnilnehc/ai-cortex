# 计划下一步（默认仅规划）

盘点治理输入源并给出下一步技能路由，默认不执行下游技能。

## 三步诊断

1. **扫**：5 主题资产盘点（Why / What/When / How / Is / Rules）
2. **诊**：状态识别 + 缺口判定（状态机决定聚焦范围，矩阵定位具体缺口）
3. **荐**：按优先级生成路由，分"现在该做 / 其他可留意"两层

## 用户报告结构（顺序固定）

1. **现在该做**：1-3 条完整路由（六字段齐全）
2. **其他可留意**：≤5 条简短列表
3. **诊断依据**：项目情况、资产清单、判定规则（含内部追溯编号）

## 默认行为

- `execute=false`
- 前两节仅用自然语言（缺 / 不全 / 漂移 / 错位；现在 / 下次 / 以后）
- 内部编号（S1-S7、G1-G4、P0-P3）只在"诊断依据"末尾作追溯
- stateless：每次调用从零重扫
- 下游就绪度仅评估 roadmap **Now tier** 条目；Next/Later 不报缺口
- 执行健康用**任务状态 × 代码活动**双信号交叉判（卡点 / 追踪漂移 / 完成漂移 / 归档漂移）
- Now tier 下游扫描按物理信号工作：resolved path_pattern glob + 可选 parent: frontmatter + 可选 manifest 文件

## 何时跳过本技能

单一维度问题可直接调用专用技能：
- 只查就绪度 → `assess-docs`
- 只查漂移 → `align-planning`
- 已知某项缺失 → `define-*` / `design-*`

## 显式执行

仅当 `execute=true` 时执行下游路由。

## 典型路由

- 规范缺失：`discover-docs-norms → define-docs-norms`
- 就绪不足：`assess-docs`
- 漂移问题：`align-planning`
