# AI Cortex

[![Version: 2.0.0](https://img.shields.io/badge/Version-2.0.0-blue.svg)](.)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![AI-Readiness: High](https://img.shields.io/badge/AI--Readiness-High-success.svg)](llms.txt)

> 面向 Agent 与开发者：技能 catalog，覆盖软件交付与项目治理；按意图路由调用能力。详见 [使命](docs/project-overview/mission.md) 与 [愿景](docs/project-overview/vision.md)。

---

## ✨ 特点

- **意图锚定**：`skills/intent-routing.json` 定义意图→技能映射；完整列表见 [intent-routing.md](skills/intent-routing.md)
- **目录与规范**：`skills/INDEX.md`、`manifest.json`；`spec/skill.md` 定义技能结构与质量
- **规则与入口**：`rules/` 提供编码与写作规范；`AGENTS.md` 定义身份与行为
- **生态**：[skills.sh](https://skills.sh)、[SkillsMP](https://skillsmp.com)

---

## 📦 安装

**技能**：

```bash
npx skills add nesnilnehc/ai-cortex
```

使用 `--force` 覆盖已有技能；`--skill <name>` 仅安装指定技能。无 Node 时见 `scripts/install-fallback.sh`。

**规则**：通过 Agent 说「将此项目规则安装到 Cursor」——或将 `rules/` 复制到 `.cursor/rules/`。见 [rules/INDEX.md](rules/INDEX.md)。

---

## 🚀 快速入门

1. 安装后，向 Agent 说意图（如「代码审查」「generate readme」「需求评审」）或询问「有哪些技能」。
2. Agent 按 `skills/intent-routing.json` 与 `AGENTS.md` 路由到主技能及可选技能。
3. 链式调用时，技能按 SKILL.md 中的 Handoff Point 相互移交。

---

## 🤝 贡献

PR 须遵循 [spec/skill.md](spec/skill.md)。更新 `manifest.json` 与 `skills/intent-routing.json` 后运行 `npm run verify`。见 [spec/registry-sync-contract.md](spec/registry-sync-contract.md) 与 [CONTRIBUTING.md](CONTRIBUTING.md)。

---

## 📄 许可证

[MIT](LICENSE)

---

## 👤 作者与致谢

致谢所有 [贡献者](https://github.com/nesnilnehc/ai-cortex/graphs/contributors)。
