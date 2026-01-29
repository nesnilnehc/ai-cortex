# 命令编写规范 (Command Specification)

状态：可选 (OPTIONAL)
范围：`commands/` 目录下的所有文件。

---

## 1. 命令的定义
**命令 (Command)** 是指触发特定技能或规则组合的“快捷指令”或“意图句式”。它通常映射到一个或多个 Skill。

## 2. 文件结构与命名
- **存放位置**：必须位于 `commands/` 目录下。
- **命名规范**：使用 `kebab-case` 命名（例如 `readme-gen.md`）。

## 3. 核心章节要求
- `# Command: /[命令名称]`
- `## 触发意图 (Intent)`：描述该命令在什么语境下被激活。
- `## 映射技能 (Mapped Skills)`：该命令会激活哪些 `skills/` 中的能力。
- `## 参数化指令 (Params)`：定义命令可接受的参数（如：`/[cmd] [language] [path]`）。
- `## 交互反馈 (UX)`：命令执行后的瞬间反馈话术。
- **语言 (Language)**：命令的说明、触发意图、映射技能描述、参数化指令、交互反馈等面向读者的内容须以简体中文书写。与项目语言规则一致，见 [spec/rule.md](rule.md) §0 语言与描述。

## 4. 调用示例
- `/readme` -> 自动调用 `generate-standard-readme`。
- `/gen-skill` -> 自动启动 `refine-skill-design` 的审计流。
