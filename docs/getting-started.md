# 快速开始与使用

由 **Agent** 通过入口文件发现与使用本库。运行时契约见 [spec/usage.md](../spec/usage.md)。

---

## 给 Agent 的提示词

用户可**直接对 Agent 说下面任一句**，即可完成“安装/配置”或“卸载”本项目的效果（本项目无安装脚本，依赖 Agent 是否遵循入口文件）。以下使用**本仓库绝对地址**，fork 或自托管时请替换为你的仓库地址。

> **说明**：涉及「在项目内创建/修改/删除 AGENTS.md」的操作，仅在**用户已授权 Agent 写入当前项目文件**时执行；否则仅进行会话内加载，不修改磁盘。

**本仓库绝对地址**：<https://github.com/nesnilnehc/ai-cortex>

### 安装 / 配置

让 Agent 从 AI Cortex 的绝对地址读取 AGENTS.md 并发现索引（从 Raw URL 按需加载）。复制以下提示词发给 Agent（已使用上述绝对地址）：

```text
读取 https://raw.githubusercontent.com/nesnilnehc/ai-cortex/main/AGENTS.md，按指引发现并加载 skills/INDEX.md、rules/INDEX.md、commands/INDEX.md，后续按需使用 AI Cortex。无 AGENTS.md 则创建并写入其内容，有则追加 AI Cortex 引用。
```

### 卸载（让 Agent 停止使用并移除已加载内容）

**移除内容包括**：

- **会话/上下文中**：已加载的 AI Cortex 技能（SKILL 内容）、规则（rules/ 下约束）、以及由 AGENTS.md 注入的操作策略与沟通准则。
- **可选（若曾主动复制）**：若曾将 AGENTS.md 或 AI Cortex 引用复制到当前项目，请从当前项目中删除该文件或其中对 AI Cortex 的引用。（修改项目内文件仅在被授权 Agent 写入时执行。）

复制以下提示词发给 Agent（明确要求**移除**已加载的 Cortex 相关内容）：

```text
不再遵循 AI Cortex，从会话/上下文中移除已加载的技能、规则与约束，后续不再从 https://github.com/nesnilnehc/ai-cortex 或 https://raw.githubusercontent.com/nesnilnehc/ai-cortex/main/ 加载。若项目根目录 AGENTS.md 含 AI Cortex 引用，则移除该文件或删除其中相关引用。
```

---

## 如何使用

本项目**不提供安装/卸载脚本**。使用方式：**让 Agent 读取本仓库的入口文件**，按指引发现技能与规则并执行。

### 入口文件

| 入口 | 用途 |
| :--- | :--- |
| **AGENTS.md** | Agent 操作手册：如何发现技能/规则与自检。 |
| **skills/INDEX.md** | 技能索引；按任务语义匹配并加载 SKILL。 |
| **rules/INDEX.md** | 规则索引。 |
| **commands/INDEX.md** | 命令索引（如 Slash 命令映射）。 |
| **llms.txt** | 机器发现入口；全库文档路径索引。 |
| **manifest.json** | 注册表：Skill/Rule/Command 路径与版本。 |

### 推荐用法

1. **在 Agent 中**：让 Agent 读取本仓库根目录的 **AGENTS.md**（或本仓库的 Raw 根 URL + `AGENTS.md`）。
2. Agent 按 AGENTS.md 的指引读取 **skills/INDEX.md**、**rules/INDEX.md**、**commands/INDEX.md**，按任务匹配并加载对应 SKILL/RULE。
3. **用自然语言提任务**：如「按规范写 README」「脱敏这段文档」「优化一个 SKILL」等，Agent 会从技能索引匹配并执行对应技能。
4. 无需在本机执行任何安装命令；资产从本仓库（或 Raw URL）按需发现与加载。

### 可选：在消费方项目中引用

- 若希望消费方项目内“固定引用”本仓库，可将 **AGENTS.md** 复制到消费方项目根目录，并让 Agent 读取该文件；AGENTS.md 中的入口路径需指向本仓库（如 Raw 根 URL + 路径）或消费方项目内已复制的副本。
- 或通过 Git submodule 将本仓库挂到消费方项目下，Agent 直接读子模块内的 AGENTS.md 与索引。

---

更多说明见 [spec/installation.md](../spec/installation.md)；入口文件用途见 [spec/distribution.md](../spec/distribution.md)。
