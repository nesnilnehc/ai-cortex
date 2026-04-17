# 对齐规划

执行任务后追溯、偏差检测和自上而下的重新校准，以保持规划（目标、需求、里程碑、路线图）与任务执行保持一致。

**定位（ADR 20260417-work-lifecycle 决策 3.3）**：本技能是**后向（backward）**治理技能 —— 在工作完成后追溯对齐。与**前向（forward）**的 `plan-next`（诊断当前治理缺口）互补不竞争：
- `plan-next`（前向）：cycle 开始 / 工作启动前 → 现在有哪些治理缺口？下一步做什么？
- `align-planning`（后向）：cycle 结束 / merge / release 后 → 已经做了什么？跟 plan 对得上吗？漂移在哪？

用户的 "pull-based / 反向推导" 工作流（有任务先做，完成后追溯补齐 backlog → requirement → task）由本技能承担，**不属于 plan-next 职责**。

## 用途

任务完成后，运行从工作到策略的追溯，使用四种类型的规划模型（目标、要求、路线图、优先级）检测偏差，并生成优先级重新校准建议。支持具有确定性选择的轻量级和完整模式。架构与代码合规性由 `align-architecture` 处理。

## 何时使用

- 任务后检查点 - 在任何完成的工单后验证计划一致性
- 里程碑关闭审查——在标记里程碑完成之前运行全面对齐
- 发布准备就绪——在发布削减之前检测计划偏差
- 范围转移诊断——调查最近的工作是否仍然支持当前目标

## 输入

- 完成的任务描述和结果
- 可选模式覆盖（“轻量级”|“完整”）
- 可选的文档根和路径映射
- 可选上下文（发布、里程碑、史诗标记）

## 输出

- 规划调整报告写入“docs/calibration/planning-alignment.md”（除非请求快照，否则将被覆盖）
- 机器可读的偏差和证据准备块

## 安装


```bash
npx skills add nesnilnehc/ai-cortex --skill align-planning
```


## 相关技能

- `plan-next` — **前向互补**：cycle 开始做体检；align-planning 是 cycle 结束做追溯
- `align-architecture` — 验证 ADR / 设计与代码合规性
- `align-backlog` — 对齐 backlog 与战略
- `assess-docs` — 在对齐之前或之后评估文档证据
- `analyze-requirements` — 当需求需要重新验证时进行切换

## 完整定义

请参阅 [SKILL.md](./SKILL.md) 了解行为、限制和示例。