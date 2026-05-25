# AI Cortex

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> 面向 Agent 与开发者的软件交付与项目治理资产库（技能、规范、协议、规则）。使命与愿景见 [使命](docs/project-overview/mission.md)、[愿景](docs/project-overview/vision.md)。

在本仓库内使用 Agent 时：**契约、四层资产与注册表、权威来源、发现与加载、技能匹配规则**均以 [AGENTS.md](AGENTS.md) 为准；术语定义见 [docs/architecture/terminology.md](docs/architecture/terminology.md)。

---

## 📦 安装与使用

### 快速开始

```bash
mkdir -p ~/.local/share
git clone --depth 1 https://github.com/nesnilnehc/ai-cortex.git ~/.local/share/ai-cortex
~/.local/share/ai-cortex/bin/cortex install
```

`cortex install` 会将每个 skill 以 symlink 方式接入 `~/.agents/skills/<skill>`，供 Codex 等读取该路径的 Agent 在新会话中发现；同时自动检测已安装的 IDE（Claude Code、Cursor）并同步其专用 skills 路径。rules 以 symlink（Claude Code）或 .mdc 转换（Cursor）方式接入。`specs/`、`protocols/` 无需安装——Agent 从 canonical 路径直读。

### 升级

```bash
cortex update
```

拉取最新提交并重新同步；自动清理已删除 skill/rule 的孤儿链接。

### 查看状态

```bash
cortex status
```

显示 CORTEX_HOME、当前 commit、各 IDE 链接数量，以及检测到的历史残留。

### 清理历史残留

首次安装前，若本地曾使用其他方式安装过 AI Cortex，可先审查再清理：

```bash
cortex clean --dry-run   # 只报告，不动手
cortex clean             # 交互式逐类确认后清理
```

### 卸载

```bash
cortex uninstall              # 移除 cortex 管理的 symlink 与 .mdc，保留 CORTEX_HOME
cortex uninstall --remove-home  # 同上，并删除 CORTEX_HOME 目录
```

设计说明见 [ADR 0010](docs/adr/0010-installation-strategy.md)。

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
