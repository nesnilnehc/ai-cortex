# AI Cortex

[![Version: 2.0.0](https://img.shields.io/badge/Version-2.0.0-blue.svg)](.)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![AI-Readiness: High](https://img.shields.io/badge/AI--Readiness-High-success.svg)](llms.txt)

> 面向 Agent 与开发者：将技能锚定在软件交付与项目治理领域的意图-路由表，使「意图→路由→技能」成为调用入口。

---

## 核心说明

AI Cortex 面向使用 AI Agent、希望按意图（项目启动、代码审查、需求评审、交付收敛、规划对齐等）发现与调用能力的团队。技能目录多按类别组织，而用户按情境思考（「我要合并代码了」「任务做完了要确认方向」）。缺乏意图→路由→技能的映射，导致难以在合适时机找到合适技能。本仓库提供该映射：覆盖软件交付（从想法到上线）与项目治理（规划、对齐、合规）两条主线。

**长期愿景**：团队在项目启动、需求评审、代码审查等意图中，能像查手册一样找到并执行对应技能——按「我在做什么」调用能力，而非按技能列表浏览。

---

## ✨ 特点

- **意图锚定**：`skills/intent-routing.json` 定义意图→技能映射；完整列表见 [intent-routing.md](skills/intent-routing.md)
- **目录与规范**：`skills/INDEX.md`、`manifest.json`；`spec/skill.md` 定义技能结构与质量
- **规则与入口**：`rules/` 提供编码与写作规范；`AGENTS.md` 定义身份与行为
- **生态**：[skills.sh](https://skills.sh)、[SkillsMP](https://skillsmp.com)

---

## 📦 安装

```bash
npx skills add nesnilnehc/ai-cortex
```

使用 `--force` 覆盖已有技能；`--skill <name>` 仅安装指定技能。无 Node 时见 `scripts/install-fallback.sh`。

---

## 🚀 快速入门

1. 安装后，向 Agent 说意图（如「代码审查」「generate readme」「项目启动」）或询问「有哪些技能」。
2. Agent 按 `skills/intent-routing.json` 与 `AGENTS.md` 路由到主技能及可选技能。
3. 链式调用时，技能按 SKILL.md 中的 Handoff Point 相互移交。

**规则**：通过 Agent 说「将此项目规则安装到 Cursor」——或将 `rules/` 复制到 `.cursor/rules/`。见 [rules/INDEX.md](rules/INDEX.md)。

---

## 📖 使用 / 配置

**发现**：优先按 [intent-routing.md](skills/intent-routing.md) 的意图/关键词匹配；或阅读 `skills/INDEX.md`、`manifest.json`。

**调用**：将 SKILL.md 作为上下文加载；执行技能；按 Handoff Point 链式调用。

**治理**：使用 `AGENTS.md` 作为权威来源；提交前运行 `npm run verify`。

---

## 🤝 贡献

PR 须遵循 [spec/skill.md](spec/skill.md)。更新 `manifest.json` 与 `skills/intent-routing.json` 后运行 `npm run verify`。见 [spec/registry-sync-contract.md](spec/registry-sync-contract.md) 与 [CONTRIBUTING.md](CONTRIBUTING.md)。

---

## 📄 许可证

[MIT](LICENSE)

---

## 👤 作者与致谢

见 [CONTRIBUTING.md](CONTRIBUTING.md) 及仓库贡献者。
