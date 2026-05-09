# AI Cortex

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> 面向 Agent 与开发者的软件交付与项目治理资产库（技能、规范、协议、规则）。使命与愿景见 [使命](docs/project-overview/mission.md)、[愿景](docs/project-overview/vision.md)。

在本仓库内使用 Agent 时：**契约、四层资产与注册表、权威来源、发现与加载、技能匹配规则**均以 [AGENTS.md](AGENTS.md) 为准；术语定义见 [docs/architecture/terminology.md](docs/architecture/terminology.md)。

---

## 📦 安装与使用

**用提示词完成安装与接入**，在编码 Agent（Claude Code、Cursor 等）里粘贴下文，由 Agent 执行克隆、路径放置与项目侧说明。

### Claude Code

打开 Claude Code，粘贴：

> 安装 AI Cortex：执行 `git clone --single-branch --depth 1 https://github.com/nesnilnehc/ai-cortex.git ~/.claude/skills/ai-cortex`。若目录已存在则改为在该目录内执行 `git fetch origin && git reset --hard origin/main`。然后在当前项目的 `CLAUDE.md` 增加一节「AI Cortex」，写明：发现与加载技能时读取 `~/.claude/skills/ai-cortex/skills/INDEX.md`，执行某项技能时加载对应目录下完整 `SKILL.md`；与本仓库协作时的契约与权威来源以该克隆路径中的 `AGENTS.md` 为准（若当前仓库自带 `AGENTS.md`，以项目内版本约定为准）。完成后根据任务语义从 `skills/INDEX.md` 帮我选用技能。

### Cursor

打开 Cursor Agent，粘贴：

> 安装 AI Cortex：执行 `git clone --single-branch --depth 1 https://github.com/nesnilnehc/ai-cortex.git ~/.cursor/skills/ai-cortex`。若目录已存在则在该目录内执行 `git fetch origin && git reset --hard origin/main`。之后在对话或规则中约定：需要调用 AI Cortex 能力时，从 `~/.cursor/skills/ai-cortex/skills/<skill-name>/SKILL.md` 载入完整技能正文；入口契约见 `~/.cursor/skills/ai-cortex/AGENTS.md`，目录见 `skills/INDEX.md`。

### 升级 / 重装

向 Agent 说明即可，例如：「在 `~/.claude/skills/ai-cortex`（或 Cursor 对应路径）执行 `git fetch origin && git reset --hard origin/main` 升级到默认分支最新提交」。无需依赖额外重装脚本。

**规则**：将 `rules/` 复制或符号链接到 IDE 的规则目录（如 `.cursor/rules/`）。见 [rules/INDEX.md](rules/INDEX.md)。

**协议**：无需安装；加载方式见 [AGENTS.md](AGENTS.md)（发现与加载、加载策略）。

---

## 🤝 贡献

见 [CONTRIBUTING.md](CONTRIBUTING.md)。

---

## 📄 许可证

[MIT](LICENSE)

---

## 🙏 致谢

- 贡献者：[contributors](https://github.com/nesnilnehc/ai-cortex/graphs/contributors)
- 部分技能 fork/integration 自 gstack、anthropics/skills 等；完整列表见 [ATTRIBUTIONS.md](docs/references/ATTRIBUTIONS.md)
