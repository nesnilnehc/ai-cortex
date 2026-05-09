# CLAUDE.md

Claude Code 在本仓库工作时的简报。

## 这是什么仓库

不是代码项目，是 markdown 资产库（技能、协议、规则、规范）。**不要**尝试 `npm test` / `npm run build` / `npm run verify`——本仓库的 `package.json` `scripts` 为空，没有可运行的命令。

工作树是 `skills/`、`protocols/`、`rules/`、`specs/`，改动以 markdown 编辑为主。

## 进一步指引

- **行为契约（必读）**：[AGENTS.md](AGENTS.md) — 加载顺序、技能匹配、失败处理、权威优先级
- **贡献流程**：[CONTRIBUTING.md](CONTRIBUTING.md) — fork、PR、版本号
- **术语**：[docs/architecture/terminology.md](docs/architecture/terminology.md) — 4 类资产定义与边界
- **命名规范**：[docs/architecture/asset-naming.md](docs/architecture/asset-naming.md) — 4 类资产命名公式与例子

## Claude Code 易踩的坑

- 技能遵循 [agentskills.io](https://agentskills.io) 标准格式；本仓库不再维护私有 spec（无 `agent.yaml`、无 `manifest.json`、无 `specs/skill.md`）
- 修改 SKILL.md 后只需同步 `skills/INDEX.md` 一处，没有其他注册表
- 历史 ADR 与 CHANGELOG 含已删机制（manifest、agent.yaml、artifact-contract、Stage 0 Norms Resolution 等）；阅读时注意时间线，不要按这些历史描述去找文件
