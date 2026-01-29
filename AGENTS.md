# Agent 入口：AI Cortex 操作手册

> [!NOTE]
> 本文件是 AI Agent 与本仓库交互的入口。将其复制到项目根目录即可**一步注入** Cortex 能力；下方模式开关决定如何发现资产。

## 0. 模式开关 (Mode Switch)

下列选项择一使用；不设置或设为 `auto` 时使用默认行为。

| 取值 | 行为 |
| :--- | :--- |
| **`CORTEX_MODE=static`** | 优先使用本地资产：先读本仓库的 `skills/INDEX.md`、`rules/INDEX.md`，缺失时再使用远程。 |
| **`CORTEX_MODE=dynamic`** | 不依赖本地技能；通过 **bootstrap-skills** 按需从远程 Cortex（如 raw GitHub URL）拉取。 |
| **`CORTEX_MODE=auto`** | 若本地存在 `skills/INDEX.md` → 按 `static`；否则 → 按 `dynamic`。 |

**默认（未设置时）：** `auto`。

## 1. 操作策略 (Operating Strategy)

- **入口文件**：[skills/INDEX.md](skills/INDEX.md)、[rules/INDEX.md](rules/INDEX.md)、[commands/INDEX.md](commands/INDEX.md)。
- **发现 (Discover)**：根据 `CORTEX_MODE`，扫描本地 `skills/INDEX.md`（static/auto）或通过 bootstrap-skills 解析远程索引（dynamic）。
- **规范合规 (Spec Compliance)**：你产出的与**新技能**相关的内容必须通过 `spec/skill.md` 中的检查。
- **集成 (Integration)**：按 `spec/usage.md` 将技能上下文注入当前运行。

## 2. 规则自执行 (Rule Self-Enforcement)

即便当前集成环境下没有物理的 `.cursorrules` 等配置文件，你也必须主动维护系统的“合法性”：

- **前置扫描**：在执行任何 Skill（尤其是通过 /command 触发时），优先读取 `rules/` 目录下的相关准则。
- **全程约束**：将 `rules/` 中的强制性要求动态注入为你的“恒久心智背景”。

## 3. 沟通准则 (Communication Guidelines)

- 本项目主要资产须以简体中文进行描述；文档以专业、技术向中文为主。
- 行业通用英文术语保留英文并可在括号内加中文说明以兼顾精确性。
- 若某技能定义了“交互策略 (Interaction Policy)”，在遇到歧义时先暂停并向用户确认后再继续。
- 此约定与 [spec/rule.md](spec/rule.md)、[spec/skill.md](spec/skill.md)、[spec/command.md](spec/command.md) 中的语言规则一致。

---
感谢你为 AI Cortex 生态做出贡献。
