# Agent 入口：AI Cortex 操作手册

本文件是 **AI Agent** 与 AI Cortex 资产交互的**操作入口**。Agent 读取本文件后，按下列策略发现并加载技能、规则与命令。适用于：本仓库内使用、从 Raw URL 拉取、或在消费方项目中引用（无安装脚本，由 Agent 按入口发现）。

---

## 1. 资产根与入口

- **资产根**：当前仓库根、本文件所在仓库根、或用户给定的 Raw 根 URL（如 `https://raw.githubusercontent.com/.../main/`）。所有索引与 SKILL/RULE 路径均**相对于该根**解析。
- **入口索引**：[skills/INDEX.md](skills/INDEX.md)、[rules/INDEX.md](rules/INDEX.md)、[commands/INDEX.md](commands/INDEX.md)。发现能力与约束时优先读取上述三个索引。

## 2. 发现与加载

- **发现**：读取 `skills/INDEX.md`、`rules/INDEX.md`、`commands/INDEX.md`；按 `description`、`tags` 与当前任务语义匹配，选中 SKILL/RULE；若 SKILL 声明 `related_skills`，按需递归或并行加载。当资产根为远程 Raw URL 时，可选用 **bootstrap-skills** 等能力按需拉取索引与技能。详见 [spec/usage.md](spec/usage.md)。
- **注入**：将选中的 SKILL 或 RULE 的**完整 Markdown** 作为系统指令或即时约束载入上下文；以原子单位注入，避免碎片化复制。
- **自检**：产出内容后，按该技能的「质量检查 (Self-Check)」章节自审，仅在所有项通过后提交；若技能定义交互策略（如遇事询问），先暂停并向用户确认。

## 3. 规范与约束

- **新技能合规**：产出的与**新技能**相关的内容须通过 [spec/skill.md](spec/skill.md) 中的检查。
- **规则前置**：在执行任何 Skill（尤其通过 /command 触发时），优先读取 `rules/` 下相关准则，并将强制性要求动态注入为恒久约束。即使当前环境无物理 `.cursorrules` 等配置文件，也须主动维护系统合法性。

## 4. 沟通与语言

- 本项目主要资产以**简体中文**描述；文档以专业、技术向中文为主。
- 行业通用英文术语保留英文，可括号内加中文说明。
- 若技能定义「交互策略 (Interaction Policy)」，遇歧义时先暂停并向用户确认。
- 与 [spec/rule.md](spec/rule.md)、[spec/skill.md](spec/skill.md)、[spec/command.md](spec/command.md) 中的语言规则一致。

---

## 引用 (Reference)

| 项 | 说明 |
| :--- | :--- |
| **规范来源** | [AI Cortex](https://github.com/nesnilnehc/ai-cortex) |
| **本手册权威版（Raw）** | <https://raw.githubusercontent.com/nesnilnehc/ai-cortex/main/AGENTS.md>（消费方项目内可据此拉取或对比最新内容） |
| **入口索引** | [skills/INDEX.md](skills/INDEX.md)、[rules/INDEX.md](rules/INDEX.md)、[commands/INDEX.md](commands/INDEX.md) |
