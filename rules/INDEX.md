# 全局规则索引 (Rules Index)

本文档定义了 AI Cortex 中所有跨技能生效的全局行为准则（Passive Constraints）。

---

## 1. 规则分类

| 分类 | 描述 |
| :--- | :--- |
| `writing` | 定义文本输出的语调、术语和排版规范。 |
| `workflow` | 定义开发流程、引用管理与文档管理策略。 |
| `documentation` | 定义文档格式与 Markdown 规范。 |
| `standards` | 定义通用与语言特定的编码标准。 |
| `tools` | 定义工具使用约束与注意事项。 |
| `security` | 定义数据处理、隐私边界和合规性要求。 |
| `interaction` | 定义 Agent 与用户的交互深度与反馈机制。 |

---

## 2. 规则列表 (Registry)

表中「版本」为规则内容的语义化版本；重大约束变更或结构性调整时递增主/次版本，勘误或措辞优化可仅递增修订号。新增规则从 `1.0.0` 起。

| 规则名称 | 分类 | 版本 | 核心价值 | 适用场景 |
| :--- | :--- | :--- | :--- | :--- |
| [writing-chinese-technical](./writing-chinese-technical.md) | writing | `1.3.0` | 规范中文技术写作与文案排版，含数字/单位空格与界面文字。 | 所有中文输出场景 |
| [workflow-import](./workflow-import.md) | workflow | `1.0.0` | 代码重构时引用同步与排序，减少编译/运行失败。 | 含模块引用的代码变更 |
| [workflow-documentation](./workflow-documentation.md) | workflow | `1.0.0` | 文档创建决策树与临时文档生命周期，保持文档库精简。 | 新建或维护 .md 文档 |
| [standards-coding](./standards-coding.md) | standards | `1.0.0` | 通用编码原则：组织、注释、命名、错误处理、日志、简洁性、重构。 | 全库代码 |
| [standards-shell](./standards-shell.md) | standards | `1.0.0` | Shell 脚本：严格模式、日志函数、trap、命名与变量引用规范。 | *.sh 脚本 |
| [tools-list-dir-dotfiles](./tools-list-dir-dotfiles.md) | tools | `1.0.0` | list_dir 不显示点文件时的替代做法与验证要求。 | Agent 使用目录列举时 |
| [documentation-markdown-format](./documentation-markdown-format.md) | documentation | `1.0.0` | 尾随空格、围栏代码块与列表前后空行等 Markdown 格式约束。 | 所有 .md 文件 |

---

## 3. 使用规范
规则应作为“长期背景”注入 AI 运行时。在执行任何原子技能（Skill）时，规则定义的约束具有最高优先级。
