# Agent 入口

本文件是 AI Agent 与 AI Cortex 交互的**单一入口与契约**。仅面向 Agent 在本仓库内工作时的行为。

---

## 0. 外部资源与链接获取政策（External Link Policy）

为保证确定性与安全性，Agent 端默认禁止外部抓取与原始内容加载，并始终优先使用本地相对路径资产。

### 0.1 外部 HTTP/HTTPS 链接

- Agent `MUST NOT` 默认抓取任何外部 HTTP/HTTPS 链接。
- Agent `MAY` 在且仅在当前执行上下文中显式声明 `allow_external_fetch=true` 时抓取外部 HTTP/HTTPS 链接。
- Agent `MUST` 将外部 HTTP/HTTPS 链接仅用于导航或定位，不得将其作为加载或校验依赖。

### 0.2 原始内容（raw content）URL

- Agent `MUST NOT` 默认加载任何“原始内容”URL（raw content URLs）。
- Agent `MAY` 在满足以下全部条件时加载 raw content URLs：
  - URL 指向受信任来源（trusted source），并显式声明 `trusted_source=true`
  - URL 使用固定版本（pinned version），即包含提交哈希（commit hash）
  - agent 已确认可等价替代的本地相对路径资产不存在（或无法满足当前 `MUST LOAD`）

### 0.3 本地相对路径优先级

- Agent `MUST` 始终优先使用本地相对路径资产作为加载/执行依赖。
- Agent `MUST NOT` 将外部资源视为与本地资产等价的权威来源。

---

## 1. 项目身份

**AI Cortex** 为软件交付与项目治理提供治理资产库（技能、规范、协议、规则），支撑从想法到上线的交付链与规划、对齐、合规等治理链；其愿景是帮助团队通过治理资产实现半自动化交付与治理，使协作可预期。见 [mission](docs/project-overview/mission.md)、[vision](docs/project-overview/vision.md) 与 [术语定义](specs/terminology.md)。

入口契约 `MUST` 只依赖本地可控资源（相对路径文件）；外链不得被获取或执行，除非满足本文件 `## 0` 中的外部链接获取政策且显式声明 `allow_external_fetch=true`。

| 资产层 | 类型 | 目录 | 注册表 |
| :--- | :--- | :--- | :--- |
| 主动能力 | Skill（技能） | `skills/` | [skills/INDEX.md](skills/INDEX.md)、[manifest.json](manifest.json) |
| 数据结构 | Spec（规范） | `specs/`、部分 `protocols/` | [specs/](specs/)、[protocols/INDEX.md](protocols/INDEX.md) |
| 交互流程 | Protocol（协议） | `protocols/` | [protocols/INDEX.md](protocols/INDEX.md) |
| 被动约束 | Rule（规则） | `rules/` | [rules/INDEX.md](rules/INDEX.md) |

---

## 2. 权威来源

Agent `MUST` 将以下资产作为权威定义与质量基准来源：

- **术语定义**：[specs/terminology.md](specs/terminology.md) `MUST` 定义 Spec、Protocol、Skill、Rule 四个核心术语。
- **技能规范**：[specs/skill.md](specs/skill.md) `MUST` 定义技能结构与质量要求。
- **技能目录**：[skills/INDEX.md](skills/INDEX.md)、[manifest.json](manifest.json) `MUST` 作为能力列表权威来源。
- **规范与协议规范**：[specs/protocol.md](specs/protocol.md) `MUST` 定义协议结构与质量要求；[protocols/INDEX.md](protocols/INDEX.md) `MUST` 注册所有领域规范与协议（UNP、INP、Requirement Modeling 等）。
- **规则注册**：[rules/INDEX.md](rules/INDEX.md) `MUST` 注册被动约束（写作、编码、工作流）。
- **制品契约**：[specs/artifact-contract.md](specs/artifact-contract.md) `MUST` 作为文档制品契约权威来源。

---

## 3. 行为预期（Runtime Contract）

在本仓库内工作时，Agent `MUST`：

1. **遵循规范**：编写或修改技能时 `MUST` 遵守 [specs/skill.md](specs/skill.md)；新增协议时 `MUST` 遵守 [specs/protocol.md](specs/protocol.md)；在 `docs/` 下创建或移动文档时 `MUST` 遵循 [specs/artifact-contract.md](specs/artifact-contract.md)。
2. **提交前自检**：产出内容后 `MUST` 运行技能或协议的 Self-Check；通过后才 `MUST` 提交或交付产物。
3. **询问时列举能力与规范**：当用户问「有哪些技能」或「有哪些协议」时，Agent `MUST` 阅读 `skills/INDEX.md` 或 `protocols/INDEX.md`，列举名称与用途，并 `MUST NOT` 仅回复 URL。
4. **改进本仓库时使用资产**：Agent `MUST` 查阅 `skills/INDEX.md`、`protocols/INDEX.md` 和 `rules/INDEX.md`，按任务语义匹配并注入对应资产；Agent `MUST NOT` 忽视可用资产。

---

## 4. 发现与加载

### 4.1 技能发现与注入

- **资产根**：Agent `MUST` 使用本仓库根或显式提供的 Raw 根 URL（但原始内容 URL 默认禁止，见 `## 0`）。
- **发现**：Agent `MUST` 读取 `skills/INDEX.md` 与 `manifest.json`，并按 `description`、`tags`、`triggers` 与任务语义进行确定性匹配（详见 `## 6`）。
- **注入**：Agent `MUST` 将所选 SKILL 的**完整 Markdown** 作为系统或上下文加载。
- **自引用**：Agent `MUST` 用 `manifest.json` 的 `capabilities` 获取技能路径。

### 4.2 规范、协议、规则加载

- **规范**（Spec）：Agent `MUST` 依据 `specs/` 与 `protocols/INDEX.md` 列举领域规范（UNP、Requirement Modeling 等）。Agent `MUST` 将其作为**接口契约**与**实现基准**注入。
- **协议**（Protocols）：Agent `MUST` 依据 `protocols/INDEX.md` 列举交互流程协议（INP、评审流程等）。Agent `MUST` 将其作为**流程基准**注入。
- **规则**（Rules）：Agent `MUST` 依据 `rules/INDEX.md` 列举全局约束（写作、编码、工作流）。Agent `MUST` 将这些规则作为**长期背景上下文**常驻注入，在任何工作中生效。

实现细则 `SHOULD` 参考：

- [docs/guides/discovery-and-loading.md](docs/guides/discovery-and-loading.md)（技能发现）
- [docs/guides/protocols-registry.md](docs/guides/protocols-registry.md)（协议发现）
- [docs/guides/protocols-usage.md](docs/guides/protocols-usage.md)（协议使用）

---

## 5. 语言与沟通

Agent `MUST` 以中文为主进行人工消费输出。详见 [docs/LANGUAGE_SCHEME.md](docs/LANGUAGE_SCHEME.md)。Agent `MUST` 保持机器消费字段（`manifest`、SKILL 元数据）为英文。

---

## 6. 技能选择（Deterministic Skill Selection）

Agent 端技能选择 `MUST` 具有确定性：禁止随机策略，并强制基于触发器匹配、标签重叠与描述相似度进行排序。

### 6.1 匹配与特征计算（Deterministic）

Agent 在执行技能发现/选择时，`MUST` 基于以下特征生成可复现的排序依据。

1. **exact trigger match（精确触发器匹配）**：当任务文本（task text）在进行规范化（lowercase、去除标点、按空白分词）后，包含某技能的任一 `triggers` 条目（同样规范化、作为子串匹配）时，该技能获得 `exact_trigger_match=true`。
2. **tag overlap（标签重叠）**：将任务文本中可被直接匹配的标签视为 `task_tags`（仅使用与技能 `tags` 字符串相等的条目；不能通过“推断同义词”补齐）。`tag_overlap = |skill.tags ∩ task_tags|`。
3. **description similarity（描述相似度）**：`description_similarity` 使用词集合的 Jaccard 相似度：
   - `task_tokens`：任务文本规范化后的 token 集合
   - `description_tokens`：技能 `description` 字段规范化后的 token 集合
   - `description_similarity = |task_tokens ∩ description_tokens| / |task_tokens ∪ description_tokens|`

### 6.2 排序规则（Ranking）

当多个技能匹配时，Agent `MUST` 按以下优先级进行排序（从高到低）：

1. `exact_trigger_match=true` 的技能优先于 `false`（同为 `true` 时比较下一级）。
2. `tag_overlap` 由高到低排序。
3. `description_similarity` 由高到低排序。

当上述三项均相等时，Agent `MUST` 使用确定性并列打破器：`skill_path` 按字典序升序。

### 6.3 选择输出（Selection Output Contract）

Agent `MUST` 输出所选技能集合，并 `MUST` 解释每个选择的理由；在任何技能选择场景下，Agent `MUST` 产生如下结构化输出（可嵌入推理或规划区块）：

```text
SkillSelection:
  no_skill_matched: boolean
  selected_skills: [
    {
      skill_path: string
      rank: number
      exact_trigger_match: boolean
      tag_overlap: number
      description_similarity: number
      selection_reasons: [string]
    }
  ]
```

### 6.4 禁止随机（No Randomness）

Agent `MUST NOT` 随机选择技能。选择 `MUST` 仅由上述排序与并列打破器决定。

---

## 7. 失败处理（Failure Handling）— REQUIRED

### 7.1 没有技能匹配

当技能选择阶段产生空集合时，Agent `MUST`：

- 显式输出 `no skill matched`
- 采用通用推理继续执行（fallback to general reasoning）
- `MUST NOT` 声称已注入任何技能

### 7.2 规范冲突

当出现规范冲突（spec conflict）时，Agent `MUST` 使用以下优先级解析冲突：

1. `AGENTS.md`
2. `specs/`
3. `protocols/`
4. `rules/`

Agent `MUST` 忽略优先级较低的冲突规则，并基于优先级最高来源做出决定。

### 7.3 必需资源缺失

当必需资源缺失时，Agent `MUST`：

- `STOP` 执行
- `ASK` 用户进行澄清，并在澄清前 `MUST NOT` 继续推断缺失内容

必需资源的定义以 `## 8` 的加载策略为准（其与本文件“发现与加载”步骤强约束一致）。

---

## 8. 加载策略（Loading Strategy）

Agent `MUST` 按加载层级决定“必需资源”的集合，并在资源缺失时触发 `## 7.3` 的 `STOP/ASK` 逻辑。

### 8.1 MUST LOAD（blocking）

- `AGENTS.md`

资源缺失规则：

- 若 `AGENTS.md` 缺失，Agent `MUST` `STOP` 执行并 `ASK` 用户提供该文件内容或路径。

### 8.2 SHOULD LOAD（context）

- `specs/terminology.md`
- `specs/protocol.md`

资源缺失规则：

- 若上述 `SHOULD LOAD` 文件缺失，Agent `SHOULD` 继续执行但 `MUST` 明确声明缺失项，并在关键决策依赖其定义时 `MUST` `STOP/ASK`。

### 8.3 DISCOVERY（on demand）

- `skills/INDEX.md`
- `protocols/INDEX.md`
- `rules/INDEX.md`

资源缺失规则：

- 若触发了“技能发现与选择”流程且上述 `DISCOVERY` 索引缺失，Agent `MUST` `STOP` 执行并 `ASK` 用户澄清本地路径或提供替代索引。

---

## 参考

| 项目 | 说明 |
| :--- | :--- |
| Spec 来源 | AI Cortex（本仓库） |
| 本入口 (Raw) | `AGENTS.md`（本地文件） |
| 规范 | [specs/terminology.md](specs/terminology.md)、[specs/skill.md](specs/skill.md)、[specs/protocol.md](specs/protocol.md)、[specs/artifact-contract.md](specs/artifact-contract.md) |
| 目录 | [skills/INDEX.md](skills/INDEX.md) \| [protocols/INDEX.md](protocols/INDEX.md) \| [rules/INDEX.md](rules/INDEX.md) |
| 自引用 | 编写 AGENTS.md → [generate-agent-entry](skills/generate-agent-entry/SKILL.md)；设计/重构技能 → [refine-skill-design](skills/refine-skill-design/SKILL.md)；生成 README → [generate-standard-readme](skills/generate-standard-readme/SKILL.md)。完整列表见 [INDEX](skills/INDEX.md)。 |
| 入口撰写 | [skills/generate-agent-entry/SKILL.md](skills/generate-agent-entry/SKILL.md) |

### 本地命令

| 命令 | 说明 |
| :--- | :--- |
| `npm run verify` | 验证 manifest、INDEX 一致性 |
| `npm run verify:skill-structure` | 验证技能结构符合 spec |
| `npm run skill:check` | 技能健康检查 |
