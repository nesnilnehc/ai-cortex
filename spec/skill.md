# 技能编写规范 (Skill Specification)

状态：强制执行 (MANDATORY)
范围：`skills/` 目录下的所有文件。

---

## 1. 文件结构与命名

- **目录**：必须使用 `kebab-case` 命名，且与 YAML 中的 `name` 字段一致。
- **文件名**：必须固定为 `SKILL.md`。
- **命名契约**：使用 `动词-名词` (例如 `decontextualize-text`)。避免使用含义模糊的通用词汇。
- **单文件与自包含（最佳实践）**：技能的常规使用方式为**仅提供一份 SKILL.md**；执行时 Agent 仅需加载该文件即可获得完整能力定义。不得依赖技能目录下的其他 MD 文档作为执行依据。若技能的产出有固定格式或契约（如「产出的 AGENTS.md 须符合某结构」），须将该契约**内嵌于 SKILL.md**（例如增加「## 附录：产出契约」），而非单独 MD 文件，以便一次注入、自包含可用。

## 2. 强制性 YAML 元数据

每个 `SKILL.md` 必须以以下格式开头：

```yaml
---
name: [kebab-case-名称]
description: [一句话简介]
tags: [至少包含一个来自 INDEX 的标签]
version: [x.x.x]
related_skills: [可选关联列表]
recommended_scope: [可选] user | project | both  # 供安装/同步脚本使用，未写时按 both
---
```

## 3. 强制性标题层级

- `# Skill: [中文标题] ([英文标题])`
- `## 目的 (Purpose)`
- `## 适用场景 (Use Cases)`
- `## 行为要求 (Behavior)`
- `## 输入与输出 (Input & Output)`
- `## 禁止行为 (Restrictions)`
- `## 质量检查 (Self-Check)`
- `## 示例 (Examples)`

## 4. 内容质量要求

- **语言 (Language)**：技能的标题、描述、正文及示例以简体中文为主。YAML 元数据中面向人的字段（如 `description`）须为简体中文；`name`、`tags` 等标识符可保持英文/kebab-case。与项目语言规则一致，见 [spec/rule.md](rule.md) §0 语言与描述。
- **指令风格**：使用命令式和技术化语言。避免口语化的废话。
- **示例要求**：必须包含至少 2 个示例，其中必须包含一个边界情况 (Edge Case) 或复杂场景。
- **交互策略**：对于复杂逻辑，必须定义用户核核对/确认策略。

## 5. 元数据同步

- 创建新技能后，必须更新 `skills/INDEX.md` 以包含新条目。
- 版本号必须遵循语义化版本 (SemVer) 规范。

## 6. 扩展与贡献流

- 新技能须通过本规范静态检查；可调用 `skills/refine-skill-design` 做逻辑优化。
- 版本注册：更新 `skills/INDEX.md`，版本号线性增长。
- 测试：`tests/` 下文件格式与运行策略见 [spec/test.md](test.md)；合并前建议对改动技能执行一次自测。
