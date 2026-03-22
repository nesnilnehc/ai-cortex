# 语言方案 (Language Scheme)

**状态**：项目级规范  
**权威**：本文档定义 AI Cortex 项目内各资产的语言归属。

---

## §1 原则

**中文是一等公民，非必要就用简体中文。**

- 默认：简体中文
- 例外：仅当存在硬性约束时使用英文（生态 API、工具解析、标识符规范）

---

## §2 例外清单（用英文的情形）

| 类型 | 内容 |
| :--- | :--- |
| 生态约束 | SKILL 的 `description`、`triggers`（被 skills.sh、agentskills 解析） |
| 工具解析 | manifest.json、.claude-plugin/marketplace.json |
| 标识符 | 文件名、目录名、`name`、`tags`、`path`（kebab-case 英文） |

---

## §3 MECE 分类规则表

以**消费方**为唯一划分维度：机器/生态 → 英文；人工/LLM → 中文。

### 机器消费（英文）

| 资产 | 路径/字段 |
| :--- | :--- |
| manifest.json | 全部 |
| SKILL 元数据 | name, path, tags, triggers, description |
| 文件/目录名 | `skills/*/`、`*.md` 等 |
| intent-routing.json | id, primary, optional, short_triggers |
| INDEX §3 表头 | Name, Tags, Version, Stability |
| .claude-plugin/marketplace.json | 全部 |

### 人工消费（中文）

| 资产 | 路径/字段 |
| :--- | :--- |
| README.md, AGENTS.md, CONTRIBUTING.md | 根目录 |
| docs/* | 全部 |
| rules/*, .cursor/rules/* | 全部 |
| spec/* | 全部 |
| skills/INDEX.md | §1–2, §4+ 及 Purpose 列 |
| skills/*/README.md | 各技能目录 |
| skills/*/SKILL.md | 正文（非 YAML） |
| intent-routing | title, when_to_use, output, stop_condition, routing_rules, short_triggers_zh |
| CHANGELOG.md, ASQM_AUDIT.md | 根目录 + skills/ |
| llms.txt, docs/ARTIFACT_NORMS.md | 根目录 |
| .claude-plugin/README.md | 全部 |
| .github/ISSUE_TEMPLATE/*.md | 全部 |

---

## §4 双语与扩展

| 字段 | 归属 | 用途 |
| :--- | :--- | :--- |
| description_zh | SKILL frontmatter（可选） | INDEX Purpose 列优先来源；无则回退 description |
| short_triggers_zh | intent-routing 每 intent | 中文触发词，供 intent-routing.md 展示 |

- **术语**：首次出现时保留英文括号（如：技能 (Skill)）
- **input_schema / output_schema**：若 SKILL 正文中文化，其 description 一并中文

---

## §5 与既有规范的关系

- **spec/skill.md**：当项目存在本方案且声明「中文为主」时，项目级文档可中文；`description`、`triggers` 仍为英文；新增可选 `description_zh`；§4.4 在 override 下允许 intent-routing 使用 `short_triggers_zh`
- **writing-chinese-technical**：凡使用中文的文档，须符合该规则（中英间距、数字单位、标点等）

---

## §6 迁移策略

| 阶段 | 资产 |
| :--- | :--- |
| P0 | README, AGENTS, CONTRIBUTING |
| P1 | spec/*, docs/ARTIFACT_NORMS |
| P2 | docs/* |
| P3 | rules/*, .cursor/rules/* |
| P4 | skills/INDEX.md 非生成部分 |
| P5 | skills/*/SKILL.md 正文 + description_zh, skills/*/README.md |
| P6 | intent-routing 中文字段，重生成 intent-routing.md |
| P7 | llms.txt, .claude-plugin/README.md, CHANGELOG, ASQM_AUDIT, .github/ISSUE_TEMPLATE |
| P8 | skills/skillgraph.md（延后） |
