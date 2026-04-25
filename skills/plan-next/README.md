# 计划下一步（read-only 诊断）

盘点治理输入源并给出下一步技能路由——**永不执行下游技能**。

## 三步法

1. **扫**：3 抽象层 × 5 主题资产盘点（意图层 Why/What-When/How、实施层 Is、元规则层 Rules）
2. **诊**：识别项目治理阶段 7 态 + 资产缺陷 4 类（MECE）
3. **荐**：按治理紧迫性生成路由，分"现在该做 / 其他可留意"两层

## 用户报告结构（顺序固定）

1. **现在该做**：1-3 条完整路由（六字段齐全）
2. **其他可留意**：≤5 条简短列表
3. **诊断依据**：项目情况、资产清单、判定规则（含内部追溯编号）

## 默认行为

- **read-only**：永不执行下游技能
- 前两节仅用自然语言（缺 / 不全 / 漂移 / 错位；现在 / 下次 / 以后）
- 内部编号（S1-S7、G1-G4、P0-P3）只在"诊断依据"末尾作追溯
- stateless：每次调用从零重扫
- 下游就绪度仅评估 roadmap **Now tier** 条目；Next/Later 不报缺口
- S5 执行健康用**任务状态 × 代码活动**双信号交叉判
- Now tier 下游扫描按物理信号工作：resolved path_pattern glob + 可选 parent: + 可选 manifest

## 何时跳过本技能

单一维度问题可直接调用专用技能：
- 只查就绪度 → `assess-docs`
- 只查漂移 → `align-planning`
- 已知某项缺失 → `define-*` / `design-*`

## 自动化组合

plan-next 永不执行下游。自动化迭代由外层组合驱动：

- `/plan-next` —— 一次性诊断
- `/loop /plan-next 30m` —— 周期诊断（持续监控，人工反应）
- `/loop /auto-iterate 30m` —— 全自动 autopilot（外层 orchestrator 驱动）

## 典型路由

- 规范缺失：`discover-docs-norms → define-docs-norms`
- 就绪不足：`assess-docs`
- 漂移问题：`align-planning`
