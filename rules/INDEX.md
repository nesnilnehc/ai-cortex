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

---

## 2. 规则列表 (Registry)

规则按分类与适用场景列出。

| 规则名称 | 分类 | 核心价值 | 适用场景 |
| :--- | :--- | :--- | :--- |
| [writing-chinese-technical](./writing-chinese-technical.md) | content | 规范中文技术写作与文案排版，含数字/单位空格与界面文字。 | 所有中文输出场景 |
| [standards-import](./standards-import.md) | standards | 代码重构时引用同步与排序，减少编译/运行失败。 | 含模块引用的代码变更 |
| [workflow-documentation](./workflow-documentation.md) | workflow | 文档管理约束（最小化、DRY、临时文档命名等）；决策树外移至 docs/guides。 | 新建或维护 .md 文档 |
| [standards-coding](./standards-coding.md) | standards | 通用编码原则：组织、注释、命名、错误处理、日志、简洁性、复杂度阈值。 | 全库代码 |
| [standards-shell](./standards-shell.md) | standards | Shell 脚本：严格模式、日志函数、trap、命名与变量引用规范。 | *.sh 脚本 |
| [requirement-quality](./requirement-quality.md) | content | 需求文档的 5 维评审清单与 spec 合规检查。 | 评审需求文档时 |
| [design-quality](./design-quality.md) | content | 设计文档的 5 维评审清单与 spec 合规检查。 | 评审设计文档时 |
| [task-quality](./task-quality.md) | content | 任务列表的字段、依赖、可追溯性评审与 spec 合规检查。 | 评审任务列表时 |
| [doc-health-criteria](./doc-health-criteria.md) | content | 文档健康判据集合（规范合规、链接图、SSOT、代码对齐、层级就绪度）。 | runtime / linter / CI 检测文档健康时 |
| [repo-structure-hygiene](./repo-structure-hygiene.md) | workflow | 仓库目录结构卫生（错放、命名、空目录、过期制品）。 | 审计或自检仓库结构时 |

---

## 3. 使用规范

规则应作为“长期背景”注入 AI 运行时。在执行任何原子技能（Skill）时，规则定义的约束具有最高优先级。
