# Agent 入口

本文件是 AI Agent 与 AI Cortex 交互的**单一入口与契约**。仅面向 Agent 在本仓库内工作时的行为。

---

## 1. 项目身份

**AI Cortex** 将技能锚定在软件交付与项目治理领域；规范与编排支撑技能协作。见 [mission](docs/project-overview/mission.md)、[vision](docs/project-overview/vision.md)。

| 资产类型 | 目录 | 规范 |
| :--- | :--- | :--- |
| Skill（技能） | `skills/` | [spec/skill.md](spec/skill.md) |

目录：`skills/INDEX.md`。能力列表：`manifest.json`。

---

## 2. 权威来源

- **定义**：[spec/skill.md](spec/skill.md) 定义技能结构与质量要求。
- **目录**：[skills/INDEX.md](skills/INDEX.md)、[manifest.json](manifest.json) 为能力列表权威来源。
- **规则**：[rules/INDEX.md](rules/INDEX.md) 为规则注册表。

---

## 3. 行为预期

在本仓库内工作时，Agent 必须：

1. **遵循规范**：编写或修改技能时遵守 [spec/skill.md](spec/skill.md)；在 `docs/` 下创建或移动文档时遵循 [spec/artifact-contract.md](spec/artifact-contract.md)。
2. **提交前自检**：产出内容后运行技能的 Self-Check；通过后再提交。
3. **询问时列举能力**：当用户问「有哪些技能」时，阅读 `skills/INDEX.md`，列举名称与用途，勿仅回复 URL。
4. **改进本仓库时使用资产**：查阅 `skills/INDEX.md`，按任务语义匹配并注入对应技能；勿忽视可用资产。

---

## 4. 发现与自引用

- **资产根**：本仓库根或显式提供的 Raw 根 URL。
- **发现**：阅读 `skills/INDEX.md` 与 `manifest.json`；按 `description`、`tags`、`triggers` 与任务语义匹配。
- **注入**：将所选 SKILL 的**完整 Markdown** 作为系统或上下文加载。
- **自引用**：用 `manifest.json` 的 `capabilities` 获取技能路径。

细则见 [docs/guides/discovery-and-loading.md](docs/guides/discovery-and-loading.md)。主动建议见 [docs/guides/proactive-suggestions.md](docs/guides/proactive-suggestions.md)。

---

## 5. 语言与沟通

人工消费资产中文优先。详见 [docs/LANGUAGE_SCHEME.md](docs/LANGUAGE_SCHEME.md)。机器消费字段（manifest、SKILL 元数据）保持英文。

---

## 参考

| 项目 | 说明 |
| :--- | :--- |
| Spec 来源 | [AI Cortex](https://github.com/nesnilnehc/ai-cortex) |
| 本入口 (Raw) | <https://raw.githubusercontent.com/nesnilnehc/ai-cortex/main/AGENTS.md> |
| 规范 | [spec/skill.md](spec/skill.md)、[spec/artifact-contract.md](spec/artifact-contract.md) |
| 目录 | [skills/INDEX.md](skills/INDEX.md) |
| 自引用 | 编写 AGENTS.md → [generate-agent-entry](skills/generate-agent-entry/SKILL.md)；设计/重构技能 → [refine-skill-design](skills/refine-skill-design/SKILL.md)；生成 README → [generate-standard-readme](skills/generate-standard-readme/SKILL.md)。完整列表见 [INDEX](skills/INDEX.md)。 |
| 入口撰写 | [skills/generate-agent-entry/SKILL.md](skills/generate-agent-entry/SKILL.md) |

### 本地命令

| 命令 | 说明 |
| :--- | :--- |
| `npm run verify` | 验证 manifest、INDEX 一致性 |
| `npm run verify:skill-structure` | 验证技能结构符合 spec |
| `npm run skill:check` | 技能健康检查 |
