# Agent 入口

本文件是 AI Agent 在本仓库内工作的执行契约。基础事实与规则以本文件为单一来源；llms.txt 仅作对外的发现指针。

---

## 1. 外部资源与链接政策

- Agent `MUST NOT` 默认抓取任何外部 HTTP/HTTPS 链接；仅当当前执行上下文显式声明 `allow_external_fetch=true` 时方可
- Agent `MUST NOT` 默认加载原始内容（raw content）URL；仅当来源受信任、版本固定（含提交哈希）且本地无等价物时方可
- Agent `MUST` 始终优先使用本地相对路径作为加载/执行依赖

---

## 2. 项目与资产

**AI Cortex** 为软件交付与项目治理提供资产库。详见 [mission](docs/project-overview/mission.md)、[vision](docs/project-overview/vision.md)、[术语定义](docs/architecture/terminology.md)。

| 资产层 | 类型 | 注册表 | 权威级别 |
|------|----|------|------|
| 主动能力 | Skill | [skills/INDEX.md](skills/INDEX.md) | — |
| 数据结构 | Spec | [specs/INDEX.md](specs/INDEX.md) | 高 |
| 交互流程 | Protocol | [protocols/INDEX.md](protocols/INDEX.md) | 中 |
| 被动约束 | Rule | [rules/INDEX.md](rules/INDEX.md) | 低 |

**冲突时优先级（高到低）**：`AGENTS.md` > `specs/` > `protocols/` > `rules/` > `docs/`。

技能本身遵循 [agentskills.io](https://agentskills.io) 标准格式；本仓库不维护私有 skill 规范。

**canonical 安装路径**：`${XDG_DATA_HOME:-~/.local/share}/ai-cortex`（可被环境变量 `CORTEX_HOME` 覆盖）。Agent 可从此路径直接读取 `specs/`、`protocols/`、`rules/` 源文件，无需额外安装步骤。

---

## 3. 行为预期

在本仓库内工作时，Agent `MUST`：

1. **询问能力时列举**：用户问"有哪些技能/协议"时，读取 `skills/INDEX.md` / `protocols/INDEX.md`，列举名称与用途，不只回 URL
2. **匹配并使用资产**：按任务语义匹配并注入对应资产；不忽视可用资产
3. **自检后交付**：技能/协议若声明 Self-Check，须通过后再提交

---

## 4. 发现、加载与匹配

**加载层级**：

| 层级 | 资源 | 缺失行为 |
|---|----|------|
| MUST | `AGENTS.md` | `STOP` + `ASK` |
| SHOULD | `docs/architecture/terminology.md` | 继续但声明缺失；关键决策依赖时 `STOP/ASK` |
| ON DEMAND | `skills/INDEX.md`、`protocols/INDEX.md`、`rules/INDEX.md` | 触发发现流程时 `STOP` + `ASK` |

**技能匹配**（确定性，不得随机）：

按任务语义匹配 `skills/INDEX.md` 里技能 frontmatter 的 `description` / `tags` / `triggers`，按以下优先级排序：

1. `triggers` 精确子串匹配优先
2. 其次按 `tags` 重叠数（仅字符串相等，不做同义词推断）
3. 其次按 `description` 语义贴合度
4. 完全并列时按 `skill_path` 字典序升序

**注入**：所选 SKILL 的完整 Markdown 作为系统或上下文加载。
**协议与规则**：依据 INDEX.md 列举，作为流程基准 / 长期背景上下文注入。

---

## 5. 失败处理

- **无技能匹配**：显式输出 `no skill matched`，回退通用推理；`MUST NOT` 佯称已注入任何技能
- **规范冲突**：按 §2 权威优先级解析，忽略低优先级冲突来源
- **必需资源缺失**：`STOP` 并 `ASK` 用户澄清，澄清前不得继续推断

---

## 6. 语言

Agent 以中文为主进行人工消费输出；机器消费字段（YAML frontmatter、命令、ID、tags）保持英文。详见 [docs/LANGUAGE_SCHEME.md](docs/LANGUAGE_SCHEME.md)。

---

## 参考

- 自引用：编写 AGENTS.md → [generate-agent-entry](skills/generate-agent-entry/SKILL.md)；设计/重构技能 → [refine-skill-design](skills/refine-skill-design/SKILL.md)；生成 README → [generate-standard-readme](skills/generate-standard-readme/SKILL.md)
