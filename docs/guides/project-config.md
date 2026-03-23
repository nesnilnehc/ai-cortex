# 项目配置指引

依赖项目配置的技能（如 automate-tests、automate-repair、commit-work、generate-github-workflow）应遵循以下行为，以实现平台无关设计。

---

## 1. 优先读取

若存在以下配置之一，优先读取其中的项目特定值：

- **CLAUDE.md**：项目根目录下的 Claude/Agent 配置（若项目采用该约定）
- **.ai-cortex/config.yaml**：AI Cortex 项目级配置（机器可读）

**可配置字段**（按需扩展）：

| 字段 | 说明 | 适用技能 |
| :--- | :--- | :--- |
| `test_command` | 测试命令或脚本 | automate-tests、automate-repair、commit-work |
| `base_branch` | 主分支名（如 main、master） | 涉及 PR 或分支检测的技能 |
| `deploy_command` | 部署命令 | 部署相关技能 |

---

## 2. 缺失时询问

若无配置或所需字段缺失，使用 AskUserQuestion 获取；勿猜测或硬编码。

---

## 3. 持久化

将用户确认的配置写入 `.ai-cortex/config.yaml` 或项目约定的位置，供后续复用。写入前征求用户同意。

---

## 4. 与现有逻辑的关系

本指引不替代技能既有的发现逻辑（如从 `package.json`、CI 配置、文档中推断）。配置优先于推断；推断结果可建议写入配置供下次使用。
