# 配置与使用规范 (Configuration & Usage)

本规范定义如何**由 Agent** 使用本项目：通过入口文件发现资产，无需安装脚本。

---

## 1. 使用方式

本项目**不提供安装/卸载脚本**，由 **Agent** 直接读取本仓库的入口文件并发现技能与规则。

### 入口文件

| 入口 | 用途 |
| :--- | :--- |
| **AGENTS.md** | Agent 操作手册：如何发现技能/规则与自检。 |
| **skills/INDEX.md** | 技能索引；按 description、tags 与任务语义匹配。 |
| **rules/INDEX.md** | 规则索引。 |
| **commands/INDEX.md** | 命令索引（如 Slash 命令映射）。 |
| **llms.txt** | 机器发现入口；全库文档路径索引。 |
| **manifest.json** | 注册表：Skill/Rule/Command 路径与版本；供程序化拉取。 |

### 推荐用法

1. **在 Agent 中**：让 Agent 读取本仓库根目录的 **AGENTS.md**（或本仓库的 Raw 根 URL + AGENTS.md）。
2. Agent 按 AGENTS.md 的指引读取 **skills/INDEX.md**、**rules/INDEX.md**、**commands/INDEX.md**，按任务匹配并加载对应 SKILL/RULE。
3. 无需在本机执行任何安装命令；资产从本仓库（或 Raw URL）按需发现与加载。

### 可选：在消费方项目中引用

- 若希望消费方项目内“固定引用”本仓库，可将 **AGENTS.md** 复制到消费方项目根目录，并让 Agent 读取该文件；AGENTS.md 中的入口路径（如 skills/INDEX.md）需指向本仓库（如 Raw 根 URL + 路径）或消费方项目内已复制的副本。
- 或通过 Git submodule 将本仓库挂到消费方项目下，Agent 直接读子模块内的 AGENTS.md 与索引。

---

## 2. 运行时契约

发现、注入、自检等运行时行为见 [spec/usage.md](usage.md)。

---

## 3. 分发与入口

入口文件（AGENTS.md、llms.txt、manifest.json）的用途与场景见 [spec/distribution.md](distribution.md)。
