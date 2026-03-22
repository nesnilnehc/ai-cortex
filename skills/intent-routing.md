# 意图-技能映射

*由 `scripts/generate-intent-routing.mjs` 从 intent-routing.json 自动生成。请编辑 JSON，勿直接修改本文件。*

按用户工作习惯（意图）选择技能，无需记忆技能名。

规范技能注册见 [INDEX.md](./INDEX.md)。

---

## 1) 项目启动

- **适用情境**：新项目、新计划或重大方向重置
- **意图**：当 有新想法或需求待澄清，用户想 把模糊意图转为可验证需求，以便 进入设计或实现
- **主技能**：[analyze-requirements](./analyze-requirements/SKILL.md)
- **可选技能**：
  - [review-requirements](./review-requirements/SKILL.md)
  - [design-solution](./design-solution/SKILL.md)
  - [bootstrap-docs](./bootstrap-docs/SKILL.md)
- **Short triggers**：project start, start project, requirements, analyze requirements
- **中文触发**：项目启动, 开始项目, 需求, 分析需求
- **产出**：已验证需求与初始设计/文档结构
- **停止条件**：需求获批且设计路径已选

## 2) 需求评审

- **适用情境**：设计开始前需对既有需求文档做质量评估
- **意图**：当 设计开始前，用户想 对既有需求文档做质量评估，以便 发现缺口并修复
- **主技能**：[review-requirements](./review-requirements/SKILL.md)
- **可选技能**：
  - [analyze-requirements](./analyze-requirements/SKILL.md) (发现缺口且需求需重做时)
- **Short triggers**：review requirements, requirements review, requirements quality
- **中文触发**：评审需求, 需求评审, 需求质量
- **产出**：覆盖六项质量维度的需求质量发现列表
- **停止条件**：无发现或所有严重/重大发现已有修复计划

## 3) 任务后治理

- **适用情境**：任务完成且需验证方向
- **意图**：当 任务完成，用户想 验证执行方向是否偏离规划，以便 校准下一步
- **主技能**：[align-planning](./align-planning/SKILL.md)
- **可选技能**：
  - [assess-docs](./assess-docs/SKILL.md)
  - [align-architecture](./align-architecture/SKILL.md)
  - [align-backlog](./align-backlog/SKILL.md)
  - [plan-next](./plan-next/SKILL.md)
- **Short triggers**：post task, alignment, planning alignment, align planning
- **中文触发**：任务后治理, 对齐, 规划对齐, 对齐规划
- **产出**：含漂移与校准动作的规划对齐报告
- **停止条件**：下 1–3 项任务已按信心等级重排

## 4) 架构合规

- **适用情境**：验证实现是否符合 ADR 或设计文档
- **意图**：当 需验证实现与设计一致，用户想 产出架构合规报告，以便 识别缺口并修复
- **主技能**：[align-architecture](./align-architecture/SKILL.md)
- **可选技能**：
  - [align-planning](./align-planning/SKILL.md)
  - [design-solution](./design-solution/SKILL.md)
- **Short triggers**：align architecture, architecture compliance, design vs code
- **中文触发**：架构对齐, 架构合规, 设计 vs 代码
- **产出**：含缺口与修复建议的架构合规报告
- **停止条件**：合规缺口已识别并建议移交

## 5) 文档缺口分流

- **适用情境**：文档薄弱或缺失导致对齐信心低
- **意图**：当 文档薄弱导致对齐信心低，用户想 评估文档就绪度并产出补齐计划，以便 提升证据质量
- **主技能**：[assess-docs](./assess-docs/SKILL.md)
- **可选技能**：
  - [bootstrap-docs](./bootstrap-docs/SKILL.md)
  - [analyze-requirements](./analyze-requirements/SKILL.md)
- **Short triggers**：doc gap, documentation readiness, doc triage
- **中文触发**：文档缺口, 文档就绪, 文档分流
- **产出**：文档就绪报告与最小补齐计划
- **停止条件**：关键层达至少 weak 且高优缺口有负责人

## 6) 迭代编排

- **适用情境**：里程碑收尾、发布门禁或定期治理周期；以存量 mission/vision/backlogs 为输入源，含阶段 0 输入源盘点与 Phase 0.5 准备
- **意图**：当 里程碑收尾或定期治理，用户想 运行对齐与文档检查并产出下一任务，以便 保持执行与战略一致
- **主技能**：[plan-next](./plan-next/SKILL.md)
- **可选技能**：
  - [align-planning](./align-planning/SKILL.md)
  - [assess-docs](./assess-docs/SKILL.md)
  - [discover-docs-norms](./discover-docs-norms/SKILL.md)
  - [bootstrap-docs](./bootstrap-docs/SKILL.md)
- **Short triggers**：iteration, governance, project cognitive loop
- **中文触发**：迭代, 治理, 项目认知循环
- **产出**：含输入源清单、已执行/跳过步骤与推荐下一步任务的周期报告；输入源缺失时优先建议完善
- **停止条件**：所有必需检查已完成或已明确推迟

## 7) 代码质量审查

- **适用情境**：合并或发布前审查质量/安全/性能/测试
- **意图**：当 合并或发布前，用户想 审查代码质量/安全/性能，以便 发现问题并修复
- **主技能**：[review-code](./review-code/SKILL.md)
- **可选技能**：
  - [review-diff](./review-diff/SKILL.md)
  - [review-codebase](./review-codebase/SKILL.md)
- **Short triggers**：review, code review, pr review, review code
- **中文触发**：review, 代码审查, PR 审查, 审查代码
- **产出**：聚合发现报告
- **停止条件**：严重/重大问题已有缓解计划

## 8) 交付收敛

- **适用情境**：提交前需运行测试、修复失败并稳定
- **意图**：当 提交前，用户想 运行测试、修复失败并稳定，以便 形成可提交状态
- **主技能**：[automate-repair](./automate-repair/SKILL.md)
- **可选技能**：
  - [automate-tests](./automate-tests/SKILL.md)
  - [commit-work](./commit-work/SKILL.md)
- **Short triggers**：repair, fix tests, delivery, stabilize
- **中文触发**：修复, 修测试, 交付, 稳定
- **产出**：收敛状态 + 清晰提交计划
- **停止条件**：测试通过且提交范围明确

## 9) 技能系统治理

- **适用情境**：审计/重构技能清单并维护质量
- **意图**：当 需审计技能清单，用户想 产出 ASQM 审计与改进动作，以便 维持质量与注册表
- **主技能**：[curate-skills](./curate-skills/SKILL.md)
- **可选技能**：
  - [refine-skill-design](./refine-skill-design/SKILL.md)
  - [discover-skills](./discover-skills/SKILL.md)
- **Short triggers**：curate, curate skills, skill audit
- **中文触发**：治理技能, 技能审计
- **产出**：ASQM 审计与改进动作
- **停止条件**：注册表与质量信号已更新

## 10) 快速抓取（工作项）

- **适用情境**：用户希望快速记录需求、bug 或 issue，无需深度验证
- **意图**：当 需快速记录，用户想 将需求/bug/issue 转为结构化工作项，以便 持久化且可追溯
- **主技能**：[capture-work-items](./capture-work-items/SKILL.md)
- **可选技能**：
  - [analyze-requirements](./analyze-requirements/SKILL.md) (当条目模糊且需验证时)
- **Short triggers**：capture, quick capture, record bug
- **中文触发**：抓取, 快速抓取, 记 bug
- **产出**：docs/backlog/ 或项目约定中的结构化工作项
- **停止条件**：条目已持久化且用户确认

## 11) 战略基础

- **适用情境**：定义或刷新战略基础：使命、愿景、北极星指标、战略支柱、战略目标、里程碑、路线图；或记录战略上下文
- **意图**：当 定义或刷新战略，用户想 产出使命/愿景/目标/里程碑/路线图等文档，以便 确立战略上下文
- **主技能**：[define-mission](./define-mission/SKILL.md)
- **可选技能**：
  - [define-vision](./define-vision/SKILL.md)
  - [define-north-star](./define-north-star/SKILL.md)
  - [define-strategic-pillars](./define-strategic-pillars/SKILL.md)
  - [design-strategic-goals](./design-strategic-goals/SKILL.md)
  - [define-milestones](./define-milestones/SKILL.md)
  - [define-roadmap](./define-roadmap/SKILL.md)
  - [align-backlog](./align-backlog/SKILL.md)
- **Short triggers**：north star, define mission, define vision, strategic goals, strategic pillars, define milestones, strategy, roadmap, align backlog, backlog alignment
- **中文触发**：北极星, 定义使命, 定义愿景, 战略目标, 战略支柱, 定义里程碑, 战略, 路线图, 对齐待办, 待办对齐
- **产出**：docs/project-overview/ 与 docs/process-management/ 中的战略层文档
- **停止条件**：请求的战略制品已持久化且用户确认

---

## 路由规则

1. 每个意图优先选用一个主技能。
2. 仅当主技能输出暴露出缺口时再调用可选技能。
3. 一周期内多意图活跃时升级至 plan-next。
4. 使用制品移交（需求/设计/对齐/文档就绪报告）而非隐式上下文传递。
