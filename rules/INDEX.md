# 全局规则索引 (Rules Index)

本文档定义了 AI Cortex（面向 Agent 的可治理能力资产库）中所有跨技能生效的全局行为准则（Passive Constraints）。

## 英文摘要 (English Summary)

- 本文件为 `rules/` 下全局被动约束的规范注册表。
- 这些规则跨技能生效，作为长期运行时约束加载。
- 治理关系：`AGENTS.md` 定义行为契约与权威边界，本注册表枚举具体规则资产。
- 优先级模型：规则与技能局部偏好冲突时，遵循全局规则；除非更高优先级的项目契约显式覆盖。

---

## 1. 规则分类

| 分类 | 描述 |
| :--- | :--- |
| `content` | 定义文本/文档的格式、语调、术语与排版规范（含 writing 与 documentation）。 |
| `workflow` | 定义开发流程与文档管理策略。 |
| `standards` | 定义通用与语言特定的编码标准。 |
| `architecture` | 定义跨切的架构与设计原则（如智能体制品生产范式）。 |

---

## 2. 规则列表 (Registry)

规则按分类与适用场景列出。

| 规则名称 | 分类 | 核心价值 | 适用场景 |
| :--- | :--- | :--- | :--- |
| [agentic-artifact-paradigm](./agentic-artifact-paradigm.md) | architecture | 智能体制品生产范式：结构是脚手架非议程、实质优先、提取优先、质量规则当 oracle 且防 oracle 填表化；交互式与一次性能力共用的上位原则。 | 设计/实现「输入→spec 制品」的智能体能力时 |
| [writing-chinese-technical](./writing-chinese-technical.md) | content | 规范中文技术写作与文案排版，含数字/单位空格与界面文字。 | 所有中文输出场景 |
| [standards-import](./standards-import.md) | standards | 代码重构时引用同步与排序，减少编译/运行失败。 | 含模块引用的代码变更 |
| [workflow-documentation](./workflow-documentation.md) | workflow | 文档管理约束（最小化、DRY、临时文档命名等）；决策树外移至 docs/guides。 | 新建或维护 .md 文档 |
| [standards-coding](./standards-coding.md) | standards | 通用编码原则：组织、注释、命名、错误处理、日志、简洁性、复杂度阈值。 | 全库代码 |
| [standards-shell](./standards-shell.md) | standards | Shell 脚本：严格模式、日志函数、trap、命名与变量引用规范。 | *.sh 脚本 |
| [standards-test-code](./standards-test-code.md) | standards | 测试代码编码标准：AAA、命名三要素、隔离、确定性、Covers 追溯、mock 克制；不覆盖 QA 业务测试用例。 | 编写或评审 *_test 代码文件 |
| [standards-agent-testing](./standards-agent-testing.md) | standards | LLM Agent 测试标准：确定性 / 非确定性分流、oracle 扩展（契约 / 轨迹 / rubric / golden / 统计）、真实模型测试隔离、模型 / prompt 变更回归门禁；与 standards-test-code 叠加。 | 测试 LLM Agent 行为的代码与契约时 |
| [requirement-quality](./requirement-quality.md) | content | 需求文档的 5 维评审清单与 spec 合规检查。 | 评审需求文档时 |
| [requirement-intake-triage](./requirement-intake-triage.md) | content | 原始进件性质分诊词表（功能/非功能/设计方案/任务/缺陷/信息不足）+ 判别问句 + 合理性镜头；澄清与评审共用的诊断 SSOT。 | 分诊或评审原始进件时 |
| [functional-design-quality](./functional-design-quality.md) | content | 功能设计文档的 5 维评审清单与 spec 合规检查。 | 评审功能设计文档时 |
| [technical-design-quality](./technical-design-quality.md) | content | 技术设计文档的 5 维评审清单与 spec 合规检查。 | 评审技术设计文档时 |
| [task-quality](./task-quality.md) | content | 任务列表的字段、依赖、可追溯性评审与 spec 合规检查。 | 评审任务列表时 |
| [test-case-quality](./test-case-quality.md) | content | QA 业务测试用例文档的 5 维评审清单与 spec 合规检查（不覆盖代码级测试）。 | 评审业务测试用例文档时 |
| [test-coverage-quality](./test-coverage-quality.md) | content | 测试覆盖评估报告的 5 维评审清单（完整性 / 真实性 / 可解释 / 风险匹配 / 时效追溯）与 spec 合规检查；用例集覆盖评审与跨制品对齐评审使用。 | 评审覆盖评估报告时（发布门禁 / 季度审计 / 上游变更） |
| [doc-health-criteria](./doc-health-criteria.md) | content | 文档健康判据集合（规范合规、链接图、SSOT、代码对齐、层级就绪度）。 | runtime / linter / CI 检测文档健康时 |
| [repo-structure-hygiene](./repo-structure-hygiene.md) | workflow | 仓库目录结构卫生（错放、命名、空目录、过期制品）。 | 审计或自检仓库结构时 |
| [adr-management](./adr-management.md) | workflow | ADR 写作纪律：准入门槛（两问验证）、状态字段强制（5 值枚举）、衰减政策（12 月归档 / 6 月可删 / ADR 例外不删）、与 decisions 边界。 | 写或维护 ADR 时 |
| [claude-md-management](./claude-md-management.md) | workflow | CLAUDE.md 写作纪律：篇幅控制（项目级 ≤300 行）、表达方式、内容禁区、修订原则、自检清单（逐项引用 spec 标尺）。 | 撰写或维护任一层级 CLAUDE.md 时 |
| [diagram-selection](./diagram-selection.md) | content | 图表选型判据：关系类型 → 图类型 → 工具速查表、跨工具选型启发式（默认 Mermaid，何时离开 PlantUML / Graphviz / flowchart.js）、渲染避坑清单、多图拆分约束。 | 画技术图表或设计文档嵌图时 |

---

## 3. 使用规范

规则应作为“长期背景”注入 AI 运行时。在执行任何原子技能（Skill）时，规则定义的约束具有最高优先级。
