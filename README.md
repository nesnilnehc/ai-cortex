# AI Cortex

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> 面向 Agent 与开发者的软件交付与项目治理资产库（技能、规范、协议、规则）。使命与愿景见 [使命](docs/project-overview/mission.md)、[愿景](docs/project-overview/vision.md)。

在本仓库内使用 Agent 时：**契约、四层资产与注册表、权威来源、发现与加载、技能匹配规则**均以 [AGENTS.md](AGENTS.md) 为准；术语定义见 [docs/architecture/terminology.md](docs/architecture/terminology.md)。

---

## 🧭 能力概览

**55 个技能**（[完整索引](skills/INDEX.md)）、**21 条规则**（[索引](rules/INDEX.md)）、**16 份规范**（[索引](specs/INDEX.md)）、协议（[索引](protocols/INDEX.md)）。

| 领域 | 数量 | 代表技能 |
| :--- | ---: | :--- |
| **治理与规划** | 17 | 使命 / 愿景 / 北极星 / 战略目标 / 路线图的逐层推导；backlog 评分、依赖排查、晋升与归档；`plan-next` 诊断下一步 |
| **代码审查** | 20 | `orchestrate-code-review` 按 scope → language → framework → library → cognitive 编排；8 种语言与 React / Vue / ORM 的原子审查技能 |
| **交付与发布** | 9 | 提交、worktree 交付与合流、发布包构建与发布、变更公告、测试执行、本地重部署 |
| **文档与资产** | 5 | README / AGENTS.md / GitHub Actions 生成；技能设计精炼；文本去上下文化 |
| **集成与运维** | 4 | NATS 跨团队消息收发、macOS Keychain 凭据管理、Agent 测试套件脚手架 |

技能可被 Claude Code、Cursor、Codex 等 20+ Agent 直接调用。一次完整的路线图规划流程见 [路线图规划链路使用指南](docs/guides/roadmap-planning-usage.md)；按协作阶段找入口见 [主动建议表](docs/guides/proactive-suggestions.md)。

### 与同类资产库的区别

- **四层资产分离**：Skill（能做什么）/ Spec（长什么样）/ Protocol（多方怎么协调）/ Rule（不能做什么）边界明确，见 [术语定义](docs/architecture/terminology.md)
- **编排与原子分层**：`orchestrate-*` 只做「检测上下文 / 串联调用 / halt-on-failure / 聚合输出」四件事，不内嵌领域逻辑
- **判据外置**：评审类技能的判据落在 `rules/*-quality.md`，一处维护多方引用
- **vendored-only 分发**：外部派生技能固定到 commit 与摘要并登记许可证，运行时不联网安装，见 [ADR 0011](docs/adr/0011-vendor-external-skills.md)

---

## 📦 安装与使用

### 快速开始

```bash
mkdir -p ~/.local/share
git clone --depth 1 https://github.com/nesnilnehc/ai-cortex.git ~/.local/share/ai-cortex
~/.local/share/ai-cortex/bin/cortex install
```

`cortex install` 会将每个 skill（包括审核后的外部派生本地副本）以 symlink 方式接入 `~/.agents/skills/<skill>`，供 Codex 等读取该路径的 Agent 在新会话中发现；同时自动检测已安装的 IDE（Claude Code、Cursor）并同步其专用 skills 路径。rules 以 symlink（Claude Code）或 .mdc 转换（Cursor）方式接入。`specs/`、`protocols/` 无需安装——Agent 从 canonical 路径直读。运行时不会从 skills.sh 或 GitHub 追加安装 Skill。

### 升级

```bash
cortex update
```

拉取最新的 AI Cortex 提交并重新同步；自动清理已删除 skill/rule 的孤儿链接。外部派生 Skill 的上游更新由维护者审核后进入 AI Cortex，不在用户运行时单独升级。

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

安装设计见 [ADR 0010](docs/adr/0010-installation-strategy.md)，外部 Skill 管理见 [ADR 0011](docs/adr/0011-vendor-external-skills.md)。

---

## 🤝 贡献

见 [CONTRIBUTING.md](CONTRIBUTING.md)；参与前请阅读 [行为准则](CODE_OF_CONDUCT.md)。安全问题请按 [安全策略](SECURITY.md) 私下报告，不要提交公开 issue。

---

## 📄 许可证

AI Cortex 原创内容使用 [MIT](LICENSE)；vendored 外部派生 Skill 保留各自许可证，见 [许可证策略](docs/references/LICENSE_POLICY.md) 和 [第三方通知](docs/references/THIRD_PARTY_NOTICES.md)。

---

## 🙏 致谢

- 贡献者：[contributors](https://github.com/nesnilnehc/ai-cortex/graphs/contributors)
- 当前外部派生 Skill 的固定来源和本地修改见 [ATTRIBUTIONS.md](docs/references/ATTRIBUTIONS.md) 与 [skills/SOURCES.yaml](skills/SOURCES.yaml)
