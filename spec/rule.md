# 规则编写规范 (Rule Specification)

状态：强制执行 (MANDATORY)
范围：`rules/` 目录下的所有文件。

---

## 0. 语言与描述 (Language)

- 本项目**主要资产**（规则、技能、命令及 `spec/`、`docs/`、各 INDEX）的**描述与正文须以简体中文**书写。
- 行业通用英文术语可保留英文，并可在括号内加中文说明。
- 本约定适用于 `rules/` 下所有规则文件及本规范自身。

## 1. 规则与技能的区别

- **技能 (Skill)**：是“如何做某事”的增量能力（有输入输出、有起点终点）。
- **规则 (Rule)**：是“如何保持状态”的全局约束（被动激活、全程生效）。

## 2. 文件结构与命名

- **存放位置**：必须位于 `rules/` 根目录下或按分类划分子目录。
- **命名规范**：使用 `kebab-case` 命名；文件名即规则标识符，须与 YAML 元数据中的 `name` 字段一致。
- **命名约定**（与 [rules/INDEX.md](../rules/INDEX.md) §1 分类对应）：
  - **模式**：`{分类}-{主题}.md`，其中「分类」取 INDEX 中的一类：`writing`、`workflow`、`documentation`、`standards`、`tools`、`security`、`interaction`；「主题」为该类下的具体领域或对象，kebab-case。
  - **示例**：`writing-chinese-technical.md`（写作类）、`workflow-import.md`（流程类）、`standards-shell.md`（标准类）、`tools-list-dir-dotfiles.md`（工具类）。
  - **长度**：宜 2–3 段（一至两处连字符）；超过 3 段时评估是否可缩写或是否适合放入子目录。
- **文件格式**：标准的 Markdown 文件，必须包含 YAML 元数据块。
- **强制性 YAML 元数据**：每个规则文件必须以如下格式开头，且 `name` 与文件名（不含扩展名）一致；`version` 须遵循语义化版本 (SemVer)，并与 [rules/INDEX.md](../rules/INDEX.md) 中该规则的版本列保持一致。

```yaml
---
name: [kebab-case-名称]
version: [x.x.x]
scope: [可选，如 全局文档产出]
recommended_scope: [可选] user | project | both  # 未写时按 both
---
```

- **版本同步**：修改规则内容后须更新本文件 YAML 中的 `version` 及 `rules/INDEX.md` 对应条目的版本列；重大约束变更或结构性调整时递增主/次版本，勘误或措辞优化可仅递增修订号。

## 3. 核心章节要求

- `# Rule: [规则中文名称] ([英文名称])`
- `## 适用范围 (Scope)`：定义该规则是在全库生效，还是仅在特定语言/框架下生效。
- `## 强制约束 (Constraints)`：以清晰、无歧义的列表形式列出禁止或必须执行的行为。
- `## 违规示例 (Bad Patterns)`：列举可能触发规则违约的行为。
- `## 修正指南 (Remediation)`：当规则被触发时，Agent 应如何修正其行为。

## 4. 集成要求

- 规则应按 [AGENTS.md](../AGENTS.md) §4 的发现与加载约定，在执行任何 Skill 之前自动注入上下文。
