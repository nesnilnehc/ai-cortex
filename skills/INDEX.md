# 技能索引

**规范能力清单**：技能注册表（name、tags、version、purpose）与标签/版本策略的权威来源。ASQM 质量、生命周期状态、重叠检测与生态定位见 [ASQM_AUDIT.md](./ASQM_AUDIT.md) 或各技能的 `agent.yaml`。

本文档是 **AI Cortex**（面向 Agent、具备治理能力的能力资产库；仓库 [ai-cortex](https://github.com/nesnilnehc/ai-cortex)）的中心技能索引。定义标准化 SKILL 元数据、标签体系与版本策略。安装：`npx skills add nesnilnehc/ai-cortex`；兼容 [skills.sh](https://skills.sh) 与 [SkillsMP](https://skillsmp.com)。

---

## 1. 标签体系

本仓库中所有 SKILL 按下列维度打标签，供 Agent 做任务匹配与调度。

| Tag | 说明 | 典型用途 |
| :--- | :--- | :--- |
| `writing` | 内容创作与风格 | 文档、博客、邮件 |
| `security` | 合规与敏感数据 | 去标识化、匿名化、漏洞说明 |
| `privacy` | 隐私与数据匿名化 | 个人或组织机密 |
| `documentation` | 标准化文档 | README、API 文档、Wiki |
| `generalization` | 抽象与泛化 | 方法提取、术语去专业化 |
| `code-review` | 代码与制品审查 | 语言、框架、安全、性能、架构、测试审查 |
| `devops` | 交付与运维自动化 | CI/CD 文档、部署 |
| `meta-skill` | 技能/规范的设计与重构 | SKILL 审计、规范化、质量 |
| `automation` | 自动化与动态加载 | 技能发现、热加载、批量操作 |
| `infrastructure` | 基础设施与运行时能力 | 发现、加载、运行时支持 |
| `optimization` | 优化与重构 | 设计与结构改进 |
| `git` | Git 工作流与版本控制 | 提交、分支、历史 |
| `workflow` | 开发工作流编排 | 多步骤流程、流水线 |

---

## 2. 版本与稳定性

本项目遵循 **[Semantic Versioning (SemVer)](https://semver.org/)**。

- **MAJOR**：SKILL 的破坏性或重大结构变更。
- **MINOR**：新步骤、交互策略或实质性改进的示例。
- **PATCH**：勘误、元数据调整或引用更新。

### 稳定性等级

每个技能有 **Stability** 指标，反映契约成熟度，与 ASQM 质量分（衡量结构质量）无关。

| Stability | 版本约定 | 含义 |
| :--- | :--- | :--- |
| `experimental` | `0.x.x` | 版本间 API 与行为可能显著变化。 |
| `stable` | `≥ 1.0.0` | 契约已稳定；破坏性变更需主版本升级。 |
| `mature` | `≥ 2.0.0` 或长期稳定的 `1.x` | 久经考验；广泛使用；预期变动极小。 |

惯例：ASQM 状态为 "validated" 的 `0.x.x` 技能，契约稳定后应升级至 `1.0.0`。

---

## 3. Skill registry

| Skill name | Tags | Version | Stability | Purpose |
| :--- | :--- | :--- | :--- | :--- |
| [decontextualize-text](./decontextualize-text/SKILL.md) | generalization, privacy, security, writing | `1.3.1` | stable | 将含私有上下文或内部依赖的文本转为通用、无偏向的表述，保留逻辑、移除组织标识，便于交接、开源或跨团队共享。. |
| [generate-standard-readme](./generate-standard-readme/SKILL.md) | devops, documentation, writing | `1.2.1` | stable | 生成固定结构的转换导向 README：10 秒理解、1 分钟运行、清晰的用途与场景；支持治理与采纳模式。. |
| [discover-docs-norms](./discover-docs-norms/SKILL.md) | documentation, workflow | `1.0.1` | stable | 通过对话与扫描，帮助建立项目级文档制品规范（路径、命名、生命周期）；产出 docs/ARTIFACT_NORMS.md。. |
| [discover-skills](./discover-skills/SKILL.md) | automation, generalization, infrastructure | `1.3.1` | stable | 识别能力缺口并从 AI Cortex 或公共技能目录推荐安装；提供前 1–3 条匹配及安装命令。. |
| [refine-skill-design](./refine-skill-design/SKILL.md) | meta-skill, optimization, writing | `1.4.0` | stable | 审计并重构既有 SKILL，使其符合规范与 LLM 最佳实践；适用于改进草稿、修复质量或对齐规范。. |
| [generate-agent-entry](./generate-agent-entry/SKILL.md) | documentation | `1.0.1` | stable | 按嵌入式输出契约编写或修订 AGENTS.md，确立项目身份、权威来源与行为预期；采用 AI Cortex 入口格式。. |
| [review-code](./review-code/SKILL.md) | code-review | `2.6.0` | mature | 编排完整代码审查流水线：依次执行 scope、语言、框架、库与认知类审查技能，并聚合为统一报告。. |
| [review-codebase](./review-codebase/SKILL.md) | code-review | `1.3.1` | stable | 对指定文件/目录/仓库进行架构与设计审查；涵盖技术债、模式与质量；diff 审查使用 review-diff。. |
| [review-diff](./review-diff/SKILL.md) | code-review | `1.3.1` | stable | 仅针对 git diff 审查影响、回归、正确性、兼容性与副作用；scope 原子技能，输出 findings 列表。. |
| [review-dotnet](./review-dotnet/SKILL.md) | code-review | `1.0.0` | stable | 按 .NET (C#/F#) 语言与运行时规范审查代码：async/await、nullable、API 版本、IDisposable、LINQ、可测性。. |
| [review-java](./review-java/SKILL.md) | code-review | `1.0.0` | stable | 按 Java 语言与运行时规范审查代码：并发、异常、try-with-resources、API 版本、集合与 Stream、NIO、可测性。. |
| [review-go](./review-go/SKILL.md) | code-review | `1.0.0` | stable | 按 Go 语言与运行时规范审查代码：并发、context、错误处理、资源管理、API 稳定性、类型语义、可测性。. |
| [review-php](./review-php/SKILL.md) | code-review | `1.0.0` | stable | 按 PHP 语言与运行时规范审查代码：strict types、错误处理、资源管理、PSR、命名空间、null 安全、生成器、可测性。. |
| [review-powershell](./review-powershell/SKILL.md) | code-review | `1.0.0` | stable | 按 PowerShell 规范审查代码：高级函数、参数设计、错误处理、对象管道、兼容性与可测性。. |
| [review-python](./review-python/SKILL.md) | code-review | `1.0.0` | stable | 按 Python 规范审查代码：类型提示、异常、async/await、上下文管理器、依赖与可测性。. |
| [review-sql](./review-sql/SKILL.md) | code-review | `1.0.1` | stable | 审查 SQL 与查询代码：注入风险、参数化、索引与性能、事务、NULL 与约束、方言可移植性。. |
| [review-vue](./review-vue/SKILL.md) | code-review | `1.0.0` | stable | 审查 Vue 3 代码：Composition API、响应式、组件、状态 (Pinia)、路由与性能；框架级原子技能。. |
| [review-security](./review-security/SKILL.md) | code-review, security | `1.0.0` | stable | 审查代码安全性：注入、敏感数据、认证、依赖、配置与加密；原子技能，输出 findings 列表。. |
| [review-architecture](./review-architecture/SKILL.md) | code-review | `1.0.1` | stable | 审查代码架构：模块与层次边界、依赖方向、单一职责、循环依赖、接口稳定性与耦合。. |
| [review-testing](./review-testing/SKILL.md) | code-review | `1.0.0` | stable | 审查测试：存在性、覆盖度、质量与结构、边界与错误路径覆盖、可维护性；认知原子技能。. |
| [generate-github-workflow](./generate-github-workflow/SKILL.md) | devops | `1.0.0` | stable | 生成嵌有输出契约的 GitHub Actions YAML：安全优先、最小权限、版本锁定；适用于 CI、发布与 PR 检查。. |
| [curate-skills](./curate-skills/SKILL.md) | documentation, meta-skill | `1.0.1` | stable | 通过 ASQM 评分、生命周期管理与重叠检测治理技能清单；产出全库技能的质量评分与规范化文档。. |
| [install-rules](./install-rules/SKILL.md) | automation, infrastructure | `1.2.1` | stable | 从源仓库将规则安装到 Cursor 或 Trae IDE；需显式确认与冲突检测；写盘前需用户批准。. |
| [review-performance](./review-performance/SKILL.md) | code-review, optimization | `1.0.0` | stable | 审查性能：复杂度、数据库/查询效率、I/O 与网络成本、内存与分配、并发竞争、缓存与延迟/吞吐回归。. |
| [bootstrap-docs](./bootstrap-docs/SKILL.md) | documentation, writing | `1.1.2` | stable | 使用 project-documentation-template 初始化或适配项目文档；产出结构化生命周期文档；支持 Initialize / Adjust。. |
| [capture-work-items](./capture-work-items/SKILL.md) | documentation, workflow, writing | `1.0.1` | stable | 将自由形式输入快速捕获为结构化、可持久的需求、缺陷或问题制品；无需深度验证。. |
| [commit-work](./commit-work/SKILL.md) | automation, git, workflow | `2.0.0` | mature | 创建高质量 git 提交：清晰消息与合理范围；遵循 Conventional Commits，含 pre-commit 质量检查。. |
| [design-solution](./design-solution/SKILL.md) | documentation, writing | `1.1.1` | stable | 从需求产出验证过的设计文档（架构、组件、数据流、权衡）；不含实现；用于下游任务拆解。. |
| [breakdown-tasks](./breakdown-tasks/SKILL.md) | documentation, workflow, writing | `1.1.0` | stable | 将设计文档拆解为可执行任务列表：依赖、验收标准、负责人或 AI 执行提示。. |
| [review-typescript](./review-typescript/SKILL.md) | code-review | `1.0.0` | stable | 审查 TypeScript/JavaScript 代码：类型安全、异步模式、错误处理与模块设计；原子技能。. |
| [review-react](./review-react/SKILL.md) | code-review | `1.0.0` | stable | 审查 React 代码：组件设计、hooks 正确性、状态管理、渲染性能与可访问性；框架级原子技能。. |
| [review-orm-usage](./review-orm-usage/SKILL.md) | code-review, optimization | `1.0.0` | stable | 审查 ORM 使用：N+1 查询、连接管理、迁移安全、事务与查询效率；库级原子技能。. |
| [analyze-requirements](./analyze-requirements/SKILL.md) | documentation, writing | `1.1.1` | stable | 通过诊断状态推进与结构化对话，将模糊意图或不完整需求转为可验证、可测试的需求。. |
| [review-requirements](./review-requirements/SKILL.md) | code-review | `1.0.1` | stable | 审查既有需求文档质量：问题清晰度、可测试需求、约束清单、范围边界、需求 ID 与遗留问题。. |
| [align-planning](./align-planning/SKILL.md) | documentation, workflow | `1.3.0` | stable | 执行任务后追溯、漂移检测与自上而下校准，使规划（目标、需求、里程碑、路线图）与执行对齐。. |
| [align-architecture](./align-architecture/SKILL.md) | documentation, workflow | `1.2.0` | stable | 对照代码实现验证架构与设计文档；当实现偏离 ADR 或设计时，产出架构合规报告。. |
| [align-backlog](./align-backlog/SKILL.md) | documentation, workflow | `1.0.0` | stable | 将产品/工作待办与当前战略、目标、路线图对齐；分析待办项，识别脱节或孤儿工作，提出变更建议。. |
| [assess-docs](./assess-docs/SKILL.md) | documentation, workflow | `3.0.0` | mature | 一次性评估文档健康：验证制品规范合规（路径、命名、front-matter）与各层证据就绪；产出缺口与最小补齐计划。. |
| [automate-tests](./automate-tests/SKILL.md) | automation, devops | `1.0.0` | stable | 安全发现并执行仓库测试命令；基于证据选择命令并设安全护栏。. |
| [automate-repair](./automate-repair/SKILL.md) | automation, devops, optimization | `1.1.0` | stable | 迭代审查变更、运行自动化测试并实施定向修复，直至问题解决或满足停止条件。. |
| [plan-next](./plan-next/SKILL.md) | automation, meta-skill, workflow | `2.0.0` | mature | 以存量 mission/vision/backlogs 等为输入源分析项目状态并产出下一行动建议；输入缺失时优先建议完善输入源。. |
| [define-mission](./define-mission/SKILL.md) | documentation, workflow | `1.2.0` | stable | 定义项目或组织的根本目的；回答项目为何存在；产出 mission 陈述并持久化到 docs。. |
| [define-vision](./define-vision/SKILL.md) | documentation, workflow | `1.2.0` | stable | 定义项目旨在创造的长远未来；回答我们在构建什么未来；产出 vision 陈述并持久化到 docs。. |
| [define-north-star](./define-north-star/SKILL.md) | documentation, workflow | `1.1.0` | stable | 定义代表向用户交付核心价值的单一最重要指标；产出 North Star Metric 及理由、辅助指标与反例。. |
| [design-strategic-goals](./design-strategic-goals/SKILL.md) | documentation, workflow | `1.0.0` | stable | 定义 3–5 个推动项目走向 vision 与 North Star 的长期战略目标；产出 goals 文档。. |
| [define-roadmap](./define-roadmap/SKILL.md) | documentation, strategy, workflow | `3.0.0` | mature | 从战略目标推导路线图，包含里程碑、关键举措、成功指标与推进条件，产出可用于决策的路线图文档。. |
| [define-strategic-pillars](./define-strategic-pillars/SKILL.md) | documentation, workflow | `1.0.0` | stable | 从 vision 与 North Star 推导 3–5 个战略支柱（高层次主题），指导战略目标与路线图。. |
| [conduct-retro](./conduct-retro/SKILL.md) | documentation, workflow | `1.0.0` | stable | 周/迭代工程回顾：分析提交历史、工作模式与代码质量指标；按人分解贡献，含表扬与成长建议。适用于「周回顾」「发了什么」「工程复盘」。. |
| [investigate-root-cause](./investigate-root-cause/SKILL.md) | optimization, workflow | `1.0.0` | stable | 系统性根因调试：investigate → analyze → hypothesize → implement。铁律：无根因不修复。适用于报错、异常行为、故障排查。. |
| [sync-release-docs](./sync-release-docs/SKILL.md) | documentation, workflow | `1.0.0` | stable | 发版后同步项目文档：交叉引用 diff，更新 README/ARCHITECTURE/CONTRIBUTING/CLAUDE.md，润色 CHANGELOG，清理 TODOS。发版后或 PR 合并后建议使用。. |
| [warn-destructive-commands](./warn-destructive-commands/SKILL.md) | security, workflow | `1.0.0` | stable | 在破坏性命令执行前发出警告。检查 Bash 命令中的 rm -rf、DROP TABLE、force-push、git reset --hard、kubectl delete 等模式。用户可覆盖每次警告。适用于接触生产、调试线上或共享环境。. |

---

## 4. 调度与扩展

调度技能时，Agent 应先解析 `INDEX.md` 以理解能力图。按 `description`、`tags`、`triggers` 语义匹配技能；链式调用时遵循各技能 prose 中的 Handoff Point 与 Scope Boundaries。细则见 [docs/guides/discovery-and-loading.md](../docs/guides/discovery-and-loading.md)。
