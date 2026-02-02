# 快捷指令索引 (Commands Index)

本文档定义了 AI Cortex 中用于快速触发复杂能力组合的意图映射（Intent Mapping）。

---

## 1. 指令类型

| 类型 | 描述 |
| :--- | :--- |
| `shortcut` | 单个技能的快速映射（Alias）。 |
| `workflow` | 多个技能的链式组合（Pipeline）。 |
| `meta` | 针对库本身的管理与审计指令。 |

---

## 2. 指令列表 (Registry)

| 指令 | 目标技能/工作流 | 描述 | 版本 |
| :--- | :--- | :--- | :--- |
| [`/readme`](./readme.md) | `generate-standard-readme` | 快速启动标准化 README 生成流程。 | `1.2.0` |
| [`/clean-project`](./clean-project.md) | `clean-project` | 自动执行项目结构化清理，静默不输出分析报告。 | `1.0.0` |
| [`/generate-commit-message`](./generate-commit-message.md) | `generate-commit-message` | 根据当前 git diff 生成 Conventional Commits 提交信息。 | `1.0.0` |
| [`/review-code`](./review-code.md) | `review-code` | 对当前 git diff 进行生产级代码评审。 | `1.0.0` |
| [`/review-codebase`](./review-codebase.md) | `review-codebase` | 对指定文件/目录/仓库范围进行通用代码评审（不限于 diff）。 | `1.0.0` |

---
