# 计划下一步（read-only 诊断）

盘点治理输入源并给出下一步技能路由——**永不执行下游技能**。

## 三步法

1. **扫**：3 抽象层 × 5 主题资产盘点（意图层 Why/What-When/How、实施层 Is、元规则层 Rules）
2. **诊**：目标链遍历——逐目标从 L1 战略目标向下找首个未就绪层级（战略目标 → 路线图 → 需求 → 设计 → 任务 → 完成）
3. **荐**：按治理紧迫性生成路由，分"现在该做 / 其他可留意"两层

## 用户报告结构（顺序固定）

1. **现在该做**：1-3 条完整路由卡片
   - 卡片头：行动名称 + 优先级标签（紧急 / 重要 / 缓 / 可略 / 待执行）
   - **TL;DR 引用块**（≤30 字）：做什么 → 立刻可见的收益
   - **6 核心字段**：治理上下文（多行短链每行 ≤25 字）/ 推荐技能 / 依据 / 完成标志（其余 2 字段为主题与优先级标签，体现于卡片头）
   - **2 选填字段**：暂缓代价 / 上手门槛（信息不足时省略，禁止臆造）
   - 多任务并行启动 → 渲染多张并列卡片（每张聚焦 1 个任务）
2. **也要留意**：≤5 条简短列表（漂移 + 卫生 + chains_to 链调）
3. **诊断依据**：项目情况、资产清单、判定逻辑表格（4 列：层级 / 节点 / 状态 / 推断）；含内部追溯编号

## 默认行为

- **read-only**：永不执行下游技能
- 前两节仅用自然语言；项目代号（T\d+/M\d+/Goal \d+/BL-\d+/ADR-\d+）首次出现自动附自然语言副标题（字典源：`.ai-cortex/glossary.yaml` → `docs/glossary.md` → 源制品 frontmatter `title:` fallback）
- KPI / 阈值首次出现含三件套（当前值 / 目标值 / 参考系）
- MoSCoW 词与治理流程黑话（前置闸门 / 短路 / soft-blocked / 兄弟扫描）禁止出现在用户输出节
- 内部编号（G1-G4、P0-P3）只在"诊断依据"末尾作追溯
- stateless：每次调用从零重扫
- 完成判定仅依赖任务 `status = done`，不读 git 信号
- 并行决策主动给出建议（专注 / 并行 / 收敛 / 启动）
- 下游扫描按物理信号工作：resolved path_pattern glob + 可选 parent: + 可选 manifest
- 路线图未分层时路由 `promote-roadmap-items`，不评估下游

## 何时跳过本技能

单一维度问题可直接调用专用技能：
- 已知某项缺失 → `define-*`
- 文档健康检测 → AgentFabric runtime + linter / CI 工具（按 `rules/doc-health-criteria.md`）

## 自动化组合

plan-next 永不执行下游。自动化迭代由外层组合驱动：

- `/plan-next` —— 一次性诊断
- `/loop /plan-next 30m` —— 周期诊断（持续监控，人工反应）
- `/loop /orchestrate-governance-step 30m` —— 全自动 autopilot（外层 orchestrator 驱动）

## 典型路由

- 无目标：`define-mission` / `design-strategic-goals`
- 路线图未分层：`promote-roadmap-items`
- 路线图缺失：`define-roadmap`
- 需求缺失：`capture-work-items`
- 设计缺失：输出"待执行"卡片（设计工作流由 AgentFabric runtime 承接）
- 任务未拆解：输出"待执行"卡片（任务拆分由 AgentFabric runtime 承接）
- 规范缺失：`define-docs-norms`
