# Agent 入口

本文件是 AI Agent 与 AI Cortex 交互的**单一入口与契约**。定义**项目身份**、**权威来源**与**行为预期**，使 Agent 在本仓库内或引用时行为一致、可预测。

---

## 1. 项目身份

**AI Cortex** 将技能锚定在软件交付与项目治理领域的意图-路由表，使「意图→路由→技能」成为调用入口；规范与编排支撑技能在意图内的协作。见 [mission](docs/project-overview/mission.md)、[vision](docs/project-overview/vision.md)。

| 资产类型 | 目录 | 规范 |
| :--- | :--- | :--- |
| Skill（技能） | `skills/` | [spec/skill.md](spec/skill.md) |

目录与元数据：`skills/INDEX.md`。可执行能力列表：仓库根目录的 `manifest.json`。

---

## 2. 权威来源

- **定义**：`spec/skill.md` 定义技能的结构、元数据与质量要求。
- **文档制品**：`spec/artifact-contract.md` 为默认；`spec/artifact-norms-schema.md` 定义项目级覆盖。项目规范（docs/ARTIFACT_NORMS.md 或 .ai-cortex/artifact-norms.yaml）优先。
- **目录**：`skills/INDEX.md` 与 `manifest.json` 为能力列表的权威来源。
- **规则注册**：`rules/INDEX.md` 为全局规则注册表；`rules/` 下的规则文件为跨技能应用的被动约束。
- **入口契约**：本文件定义发现、注入与自检行为（§4）。

---

## 3. 行为预期

在本项目中工作或引用时，Agent 必须：

1. **遵循规范**：理解、编写或修改技能时遵守 [spec/skill.md](spec/skill.md)。在 `docs/` 下创建或移动文档制品时遵循 [spec/artifact-contract.md](spec/artifact-contract.md)。
2. **提交前自检**：产出内容后运行技能的 Self-Check；通过后再提交。若技能定义交互策略（如询问用户），则先行暂停确认。
3. **询问时列举能力**：当用户问「有哪些技能」时，阅读 `skills/INDEX.md`，**列举名称与用途**，可选附链接；勿仅回复 URL。
4. **改进本仓库时使用资产**：改进本项目的任务（如编写或修订 AGENTS.md、设计或重构技能、生成 README）应查阅 `skills/INDEX.md`，按任务语义匹配并注入对应技能；勿忽视可用资产。

---

## 4. 发现与加载（概要）

- **资产根**：当前仓库根、本文件所在仓库根，或用户提供的 Raw 根 URL。
- **发现**：阅读 `skills/INDEX.md` 与 `manifest.json`；按 `description`、`tags` 与任务语义匹配。链式调用时遵循各技能 prose 中的 Handoff Point 与 Scope Boundaries；使用 `skills/intent-routing.json` 做意图→技能映射。
- **注入**：将所选 SKILL 的**完整 Markdown** 作为系统或上下文加载；按原子单元注入。
- **自引用**：在本仓库工作时，发现并加载 `skills/` 下资产；用 `manifest.json` 的 `capabilities` 获取路径。

### 4.1 调用与匹配

- **匹配优先级**（多源同时适用时）：intent 的 `short_triggers` 或 `short_triggers_zh`（用户输入为中文时）→ SKILL 的 `triggers` → `description`/`tags` 语义匹配。
- **意图优先**：优先使用 `skills/intent-routing.json`（及生成的 `intent-routing.md`）的 `when_to_use`、`short_triggers`、`short_triggers_zh` 将用户意图映射到技能。
- **主技能优先路由**：每个请求先路由到主技能；仅当主技能输出暴露明确缺口时再调用可选技能。
- **升级规则**：一周期内多意图活跃时，将编排升级至 `run-checkpoint`。
- **Triggers**：若 SKILL 在 frontmatter 中有 `triggers`，用于精确短语匹配。
- **语义回退**：按 `description` 与 `tags` 匹配；支持自然语言（含中文）。
- **默认值**：若存在 `input_schema.defaults` 且用户未显式输入，使用该默认值。
- **语言**：中文与英文调用均支持；用户输入为中文时，优先使用 intent-routing 的 `short_triggers_zh`（若存在）。

---

## 5. 语言与沟通

- 本项目对人工消费资产采用中文优先。详见 [docs/LANGUAGE_SCHEME.md](docs/LANGUAGE_SCHEME.md) 的语言规则与 MECE 分类。
- 机器消费字段（manifest、SKILL 的 description/triggers、目录元数据）保持英文以兼容生态。

---

## 参考

| 项目 | 说明 |
| :--- | :--- |
| Spec 来源 | [AI Cortex](https://github.com/nesnilnehc/ai-cortex) |
| skills.sh 安装 | `npx skills add nesnilnehc/ai-cortex` |
| 本入口 (Raw) | <https://raw.githubusercontent.com/nesnilnehc/ai-cortex/main/AGENTS.md> |
| 规范 | [spec/skill.md](spec/skill.md)、[spec/artifact-contract.md](spec/artifact-contract.md)、[spec/artifact-norms-schema.md](spec/artifact-norms-schema.md) |
| 用法 | 本文件 §4 |
| 入口撰写 | [skills/generate-agent-entry/SKILL.md](skills/generate-agent-entry/SKILL.md)（含其他项目的输出契约） |
| 目录 | [skills/INDEX.md](skills/INDEX.md) |
| 自引用任务→资产 | **Skill**：编写/修订 AGENTS.md → [generate-agent-entry](skills/generate-agent-entry/SKILL.md)；设计/重构技能 → [refine-skill-design](skills/refine-skill-design/SKILL.md)；生成 README → [generate-standard-readme](skills/generate-standard-readme/SKILL.md)；发现文档规范 → [discover-docs-norms](skills/discover-docs-norms/SKILL.md)；验证文档/文档就绪 → [assess-docs](skills/assess-docs/SKILL.md)。完整列表：[skills/INDEX.md](skills/INDEX.md)。 |
| 执行链（需求→设计→任务） | [analyze-requirements](skills/analyze-requirements/SKILL.md) → [design-solution](skills/design-solution/SKILL.md) → [breakdown-tasks](skills/breakdown-tasks/SKILL.md)；产出：requirements.md、design.md、tasks.md。见 [docs/process-management/decisions/20260316-execution-chain-requirements-design-tasks.md](docs/process-management/decisions/20260316-execution-chain-requirements-design-tasks.md)。 |

### 调用示例

| 意图 | English | 中文（语义） |
| :--- | :--- | :--- |
| 代码审查 | review, code review | 代码审查、帮我 review |
| 提交 | commit, commit work | 提交、commit |
| 快速抓取 | capture bug: ... | 记一个 bug：... |
