# AI 技能资产索引 (Skills Index)

本文档是 **AI Cortex**（面向 Agent 的可治理能力资产库，仓库 [ai-cortex](https://github.com/nesnilnehc/ai-cortex)）的核心技能索引，定义了 SKILL 的标准化元数据、分类系统及版本规范。

---

## 1. 分类标签系统 (Tagging System)

库中的所有 SKILL 均按以下维度进行标注，以便于 Agent 进行任务匹配和调度。

| 标签 | 描述 | 应用领域 |
| :--- | :--- | :--- |
| `writing` | 内容创作与风格修饰 | 文档、博客、邮件内容生产 |
| `security` | 合规性与敏感信息处理 | 脱敏、匿名化、漏洞提示 |
| `privacy` | 隐私保护与数据匿名化 | 个人信息/组织秘密保护 |
| `documentation` | 标准化文档产出 | README, API Docs, Wiki |
| `generalization` | 知识抽象与泛化 | 方法论提取、黑话消除 |
| `eng-standards` | 工程规范与最佳实践 | 代码评审、架构文档、基建配置 |
| `devops` | 交付与运维自动化 | CI/CD 文档、部署指南 |

---

## 2. 版本规范 (Versioning)

本项目遵循 **[语义化版本 (SemVer)](https://semver.org/)** 规范。

- **MAJOR (主版本)**：SKILL 结构发生重大变更，或核心逻辑不兼容。
- **MINOR (次版本)**：增加了新的处理步骤、交互策略或显著增强了示例。
- **PATCH (修订号)**：修复错别字、微调元数据描述、补全参考资源。

---

## 3. Skill 列表 (Registry)

| Skill 名称 | 版本 | 核心价值 | 验证状态 |
| :--- | :--- | :--- | :--- |
| [decontextualize-text](./decontextualize-text/SKILL.md) | `1.2.0` | 消除环境依赖，实现跨边界知识流动。 | [Verified](./decontextualize-text/tests/) |
| [generate-standard-readme](./generate-standard-readme/SKILL.md) | `1.2.0` | 为工程资产建立标准化的“第一面孔”。 | [Verified](./generate-standard-readme/tests/) |
| [bootstrap-skills](./bootstrap-skills/SKILL.md) | `1.2.0` | 使智能体能够动态发现并热加载远程技能。 | [Verified](./bootstrap-skills/tests/) |
| [refine-skill-design](./refine-skill-design/SKILL.md) | `1.2.0` | 审计并重构 SKILL，确保其符合工业级标准。 | [Verified](./refine-skill-design/tests/) |
| [write-agents-entry](./write-agents-entry/SKILL.md) | `1.0.0` | 按本技能内嵌「产出契约」为项目撰写或修订 AGENTS.md，建立 Agent 入口与行为契约。 | [Verified](./write-agents-entry/tests/) |
| [clean-project](./clean-project/SKILL.md) | `1.0.0` | 自动分析项目并执行结构化清理（删除/归位/合并/重命名/整理 docs 与 .gitignore），静默执行不输出报告。 | [Verified](./clean-project/tests/) |
| [generate-commit-message](./generate-commit-message/SKILL.md) | `1.0.0` | 根据 git diff 生成符合 Conventional Commits 的专业 Git 提交信息。 | [Verified](./generate-commit-message/tests/) |
| [review-code](./review-code/SKILL.md) | `1.0.0` | 针对 git diff 的变更影响与回归风险评审，关注正确性、兼容性与副作用。 | [Verified](./review-code/tests/) |
| [review-codebase](./review-codebase/SKILL.md) | `1.0.0` | 针对指定范围的架构、设计与技术债评审，关注边界、模式与整体质量。 | [Verified](./review-codebase/tests/) |

---

## 4. 框架扩展建议

Agent 在调度 Skill 时，应优先解析 `INDEX.md` 以确定能力的拓扑结构，并通过 `related_skills` 实现链式任务处理。
