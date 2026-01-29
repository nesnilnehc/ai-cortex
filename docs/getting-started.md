# 快速开始与使用

本文说明如何安装、配置并使用本库。运行时契约（发现、注入、自检、模式开关）的正式定义见 [spec/usage.md](../spec/usage.md)。

---

## 1. 快速开始（安装与配置）

安装与配置均通过一行命令完成，不推荐手动拷贝文件。

在目标仓库根目录执行（若从 fork 安装，将 `nesnilnehc/ai-cortex` 换成你的 组织/仓库名）：

```bash
curl -sL https://raw.githubusercontent.com/nesnilnehc/ai-cortex/main/scripts/install.sh | bash
```

**依赖**：`jq`。未安装时脚本会提示。

**结果**：当前目录下生成 `.cortex/`（含 `config.json`、`skills/`、`rules/`、`commands/`）与根目录 `AGENTS.md`。脚本会询问或通过参数指定是否注入 Bridges；若为交互模式，会**根据当前环境给出建议**（例如检测到 Git/ GitHub 仓库时建议注入 `github-actions`，检测到 Cursor 相关配置时建议注入 `cursor`）。可注入的 Bridges 及适用环境见 [spec/installation.md](../spec/installation.md) 与 [spec/bridges.md](../spec/bridges.md)。

**可选**：指定安装目录、来源 URL、要注入的 Bridges，见 [spec/installation.md](../spec/installation.md)。入口文件（AGENTS.md、llms.txt、manifest.json）用途见 [spec/distribution.md](../spec/distribution.md)。

---

## 2. 用户怎么用（安装完成后）

安装完成后，**你不需要再执行任何命令**。像平时一样在你的项目里使用 Agent（如 Cursor、Claude 等）即可。

### 你只需要做两件事

1. **让 Agent 知道要遵循本库**  
   若你的环境会自动读取项目根目录的 `AGENTS.md`（例如部分 IDE 会将其作为规则来源），则无需额外操作。否则，在对话开始时说一句：**「请先读取本项目根目录的 AGENTS.md」**，或在该环境中把 `AGENTS.md` 设为规则/系统提示来源。

2. **用自然语言提出任务**  
   直接向 Agent 描述你想要做的事，例如：
   - *「按规范给这个项目写一个 README」* → Agent 会匹配并加载「生成标准 README」技能后执行。
   - *「把这段文档里的敏感信息脱敏」* → Agent 会匹配并加载「脱敏」技能后执行。
   - *「帮我优化一个 SKILL 的写法」* → Agent 会匹配并加载「优化技能设计」等元技能。

**你不需要掌握任何 Cortex 专用命令**。Agent 会按 `AGENTS.md` 的指引，从本库的 [skills/INDEX.md](../skills/INDEX.md) 中发现对应技能、注入、执行并自审。只需用自然语言描述任务即可。

### 可选：Slash 命令

若你的 IDE 支持 Slash 命令（如 `/readme`），可使用 [commands/INDEX.md](../commands/INDEX.md) 中定义的快捷方式触发对应技能；**不掌握这些命令也可以正常使用**，自然语言已足够。

### 模式与原理（供查阅）

资产来源由根目录 `AGENTS.md` 中的 **`CORTEX_MODE`** 决定：`static`（优先读本地）/ `dynamic`（按需从远程拉取）/ `auto`（默认，有本地则 static 否则 dynamic）。如需切换，编辑 `AGENTS.md` 中的该行即可。  
运行时行为（发现、注入、自检）的正式定义见 [spec/usage.md](../spec/usage.md)。
