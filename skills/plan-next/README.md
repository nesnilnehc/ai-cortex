# 计划下一步（read-only 诊断）

盘点治理输入源并给出下一步技能路由——**永不执行下游技能**。

## 三步法

1. **扫**：3 抽象层 × 5 主题资产盘点（意图层 Why/What-When/How、实施层 Is、元规则层 Rules）
2. **诊**：目标链遍历——逐目标从 L1 战略目标向下找首个未就绪层级（战略目标 → 路线图 → 需求 → 设计 → 任务 → 完成）
3. **荐**：按治理紧迫性生成路由，分"现在该做 / 其他可留意"两层

## 用户报告结构（顺序固定）

1. **现在该做**：1-3 条完整路由（六字段齐全）
2. **其他可留意**：≤5 条简短列表
3. **诊断依据**：项目情况、资产清单、判定规则（含内部追溯编号）

## 默认行为

- **read-only**：永不执行下游技能
- 前两节仅用自然语言（缺 / 不全 / 漂移 / 错位；现在 / 下次 / 以后）
- 内部编号（G1-G4、P0-P3）只在"诊断依据"末尾作追溯
- stateless：每次调用从零重扫
- 完成判定仅依赖任务 `status = done`，不读 git 信号
- 并行决策主动给出建议（专注 / 并行 / 收敛 / 启动）
- 下游扫描按物理信号工作：resolved path_pattern glob + 可选 parent: + 可选 manifest
- 路线图未分层时路由 `promote-roadmap-items`，不评估下游

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

- 无目标：`define-mission` / `design-strategic-goals`
- 路线图未分层：`promote-roadmap-items`
- 路线图缺失或未对齐：`define-roadmap` / `align-backlog`
- 需求缺失：`analyze-requirements`
- 设计缺失：`design-solution`
- 任务未拆解：`breakdown-tasks`
- 规范缺失：`discover-docs-norms → define-docs-norms`
- 漂移问题：`align-planning`
