# Agent 入口 (Agent Entry)

本文件是 **AI Agent** 与 AI Cortex 交互的**唯一入口与契约**。目的：在 Agent 接触本项目时，明确**项目身份**、**权威来源**与**行为约定**，使 Agent 在本仓库内或引用本仓库时行为一致、可预期。

---

## 1. 项目身份

**AI Cortex** 是一个 **Spec 驱动的 Skills/Rules/Commands 资产库**：可复用能力由 `spec/` 定义与约束，由测试与自检保障质量。详见 [docs/vision.md](docs/vision.md)、[docs/architecture.md](docs/architecture.md)。

| 资产类型 | 目录 | 定义规范 |
| :--- | :--- | :--- |
| 技能 (Skill) | `skills/` | [spec/skill.md](spec/skill.md) |
| 规则 (Rule) | `rules/` | [spec/rule.md](spec/rule.md) |
| 命令 (Command) | `commands/` | [spec/command.md](spec/command.md) |
| 技能测试 | `skills/*/tests/` | [spec/test.md](spec/test.md) |

能力目录与元数据：`skills/INDEX.md`、`rules/INDEX.md`、`commands/INDEX.md`；可执行能力列表（含测试路径）：仓库根目录 `manifest.json`。

---

## 2. 权威来源

- **定义**：各类资产的**结构、元数据、质量要求**以 `spec/` 下对应规范为准；Agent 理解或产出技能/规则/命令时须遵循这些规范。
- **目录**：能力列表以各 `INDEX.md` 及 `manifest.json` 为准；发现与加载时以当前仓库根或给定的资产根（含 Raw 根 URL）解析路径。
- **使用契约**：发现、注入、自检的运行时约定见本文件 §4。

---

## 3. 行为约定

Agent 在本项目内或引用本项目时，应当：

1. **以 spec 为据**：理解定义、编写或修改资产时，遵循 [spec/skill.md](spec/skill.md)、[spec/rule.md](spec/rule.md)、[spec/command.md](spec/command.md)；运行或验证测试时遵循 [spec/test.md](spec/test.md)。
2. **规则优先**：在执行任何 Skill 之前，须先加载 `rules/` 下相关规则为恒久约束（本文件 §4 嵌套加载）。
3. **自检后提交**：产出内容后，须按该技能的「质量检查 (Self-Check)」自审，通过后再提交；若技能定义交互策略（如遇事询问），须先暂停并向用户确认。
4. **能力列表类询问**：当用户问「有什么技能/规则/命令」时，须先读取对应 INDEX，**枚举名称与用途**，再可提供链接；不得仅回复 URL。

---

## 4. 发现与加载（概要）

- **资产根**：当前仓库根、本文件所在仓库根、或用户给定的 Raw 根 URL。
- **发现**：读取 `skills/INDEX.md`、`rules/INDEX.md`、`commands/INDEX.md`，按 `description`、`tags` 与任务语义匹配；SKILL 的 `related_skills` 按需递归或并行加载。
- **注入**：将选中的 SKILL/RULE 的**完整 Markdown** 作为系统指令或即时约束载入；以原子单位注入。规则须在技能之前注入。

细节见上文 §2–§3。

---

## 5. 语言与沟通

- 本项目主要资产以**简体中文**描述；与 [spec/rule.md](spec/rule.md) §0 及 skill/command 规范中的语言约定一致。
- 行业通用英文术语可保留英文，可括号内加中文说明。

---

## 引用 (Reference)

| 项 | 说明 |
| :--- | :--- |
| 规范来源 | [AI Cortex](https://github.com/nesnilnehc/ai-cortex) |
| 本手册 Raw | <https://raw.githubusercontent.com/nesnilnehc/ai-cortex/main/AGENTS.md> |
| 定义与测试 | [spec/skill.md](spec/skill.md) · [spec/rule.md](spec/rule.md) · [spec/command.md](spec/command.md) · [spec/test.md](spec/test.md) |
| 使用约定 | 本文件 §4 |
| 入口撰写规范 | [skills/write-agents-entry/SKILL.md](skills/write-agents-entry/SKILL.md)（本技能内嵌「产出契约」章节，供他项目参考） |
| 入口索引 | [skills/INDEX.md](skills/INDEX.md) · [rules/INDEX.md](rules/INDEX.md) · [commands/INDEX.md](commands/INDEX.md) |
