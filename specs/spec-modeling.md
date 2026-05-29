---
id: SPEC_MODELING_SPEC_V2
name: Spec Modeling Schema (Meta-Spec)
description: Meta-spec defining the structural contract that any spec document must follow — frontmatter contract, body section skeleton, and required/conditional/optional section taxonomy.
version: 2.0.1
status: active
lifecycle: living
created_at: 2026-05-21
scope: |
  Defines the structural contract for any spec document.
  Applies recursively to this file itself. Establishes the required / conditional /
  optional section taxonomy and frontmatter requirements that downstream specs inherit.
related:
  - ./adr-modeling.md
  - ./claude-md-modeling.md
  - ./functional-design-modeling.md
  - ./technical-design-modeling.md
  - ./requirement-modeling.md
  - ./task-modeling.md
  - ./universal-notification.md
---

# Spec 建模规范（Meta-Spec）

> **数据契约**：定义任何 spec 文档的结构骨架与字段约束

---

## 1. 定位与适用范围

本规范是 spec 的 spec——任何 spec 文档（包含本文件自身）必须遵循此处定义的章节骨架与 frontmatter 契约。

每份 spec 定义一类制品的数据契约（字段、章节、状态、校验）；本 meta-spec 定义这些 spec 自身应如何组织。

适用：

- 任何描述制品数据契约的 spec 文档

不适用：

- 配套的 rule（行为约束）
- protocols（流程描述）
- 制品本身（spec 描述的对象，由具体 spec 定义）

具体存放路径由各项目治理决定（如本仓库的 `specs/` 目录、其他项目的 `docs/specs/` 等），不在本规范约束范围。

---

## 2. 心智模型（Mental Model）

> 一份合格制品要回答的核心问题。

每份 spec 描述的制品，往往有少数几个"核心问题"——一份合格制品必须能在这些问题上立得住。把这些问题前置在 §2，能让 spec 作者和读者抓住要点、避免偏离本质。

| 制品 | 核心问题示例 |
|---|---|
| ADR | What / Why / Alternatives / Consequences（4 问） |
| CLAUDE.md | What / With / How / Don't（4 问） |
| spec 自身 | 章节按何时该写的三态分类（必备 / 条件必备 / 可选） |

### 2.1 spec 自身的心智模型：章节的三态

一份合格 spec 的本质维度是"它的每个章节按何时该写如何分类"。三态就是这个维度的答案——所有后续章节都依赖此分类。

| 类型 | 触发条件成立时 | 触发条件不成立时 |
|---|---|---|
| **必备** | 必须写（恒成立，无条件） | — |
| **条件必备** | 必须写 | **不该写**（写了即冗余） |
| **可选** | 可写 | 可不写 |

#### 关键差异

- **必备 vs 条件必备**：必备无触发条件；条件必备只在某个特征成立时才该出现
- **条件必备 vs 可选**：条件必备是二值开关（满足条件就必须写，不满足就不该写）；可选是作者自由判断

### 2.2 章节分类与触发条件速查

| 章节 | 类型 | 触发条件（如有） |
|---|---|---|
| §1 定位与适用范围 | 必备 | — |
| §2 心智模型 | 条件必备 | 制品有显著思维框架（N 个核心问题） |
| §3 命名约定 | 条件必备 | 制品落盘且文件名有惯用模式 |
| §4 Frontmatter 契约 | 条件必备 | 制品是 markdown 且有 frontmatter |
| §5 正文结构契约 | 必备 | — |
| §6 反模式 | 必备 | — |
| §7 示例 | 必备 | — |
| §8 与其他资产关系 | 可选 | — |

---

## 3. 命名约定

每份 spec 描述其所建模制品的**文件命名规则**（如有）。不规定具体存放路径——路径由各项目治理决定。

### 3.1 spec 自身的命名约定

- 文档建模类 spec：`<artifact-name>-modeling.md`（如 `adr-modeling.md`）
- 运行时对象类 spec：`<concept>.md`（不带 `-modeling` 后缀，如 `universal-notification.md`）
- Meta-spec 本身：`spec-modeling.md`

### 3.2 适用判断

- 制品是固定单文件（如 `CLAUDE.md`） → §3 可省略，命名是常量
- 制品是模式化命名的多文件（如 ADR 的 `NNNN-{slug}.md`） → §3 必备
- 制品是运行时对象（无文件） → §3 不该写

---

## 4. Frontmatter 契约

```yaml
---
id: <UPPER_SNAKE>_MODELING_SPEC_V<n>
name: <English Name>
description: <一句话英文摘要>
version: <SemVer>
status: active | draft | superseded | archived
lifecycle: living
created_at: YYYY-MM-DD
scope: |
  <多行说明 spec 约束什么、不约束什么>
related:
  - <相关 rule / spec / 文档的相对路径>
# 条件字段（按 status 必填）
superseded_by: <new-spec-id>      # status: superseded 时必填
archived_at: YYYY-MM-DD            # status: archived 时必填
---
```

### 4.1 字段表

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `id` | string | 必 | 格式 `<UPPER_SNAKE>_MODELING_SPEC_V<n>`（如 `ADR_MODELING_SPEC_V1`）；运行时对象类 spec 可省略 `_MODELING_`（如 `UNIVERSAL_NOTIFICATION_SPEC_V2`） |
| `name` | string | 必 | 英文 spec 名称 |
| `description` | string | 必 | 一句话英文摘要（≤ 200 字符） |
| `version` | string | 必 | SemVer 版本号 |
| `status` | enum | 必 | `active` / `draft` / `superseded` / `archived`（语义见 §4.2） |
| `lifecycle` | enum | 必 | 固定 `living`（spec 本身持续演化） |
| `created_at` | date | 必 | spec 首次发布日期（`YYYY-MM-DD`） |
| `scope` | string | 必 | 多行说明适用范围；使用 `\|` 而非 `>`（保留换行） |
| `related` | list[path] | 可选 | 关联资产相对路径列表 |
| `superseded_by` | string | 条件 | `status: superseded` 时必填，指向替代 spec 的 id |
| `archived_at` | date | 条件 | `status: archived` 时必填 |

### 4.2 状态机语义

`status` 的 4 个枚举值含义与转入条件：

| 状态 | 含义 | 转入条件 |
|---|---|---|
| `draft` | 初稿，尚未稳定 | spec 首次落地，未在生产中被引用 |
| `active` | 当前有效 | spec 已稳定，被下游引用 |
| `superseded` | 已被新版本 spec 替代 | 新版本 spec 已发布并接管职责 |
| `archived` | 已归档，不再维护 | 描述的制品已淘汰或概念已合并 |

**何时写本子节**：当制品的状态机有非平凡含义（≥3 状态 + 有条件字段）时必写；若 status 仅是简单标记（如 `draft` / `published` 二值且无附加语义），可省略本子节，§4.1 字段表已足够。

---

## 5. 正文结构契约

### 5.1 章节顺序

```markdown
# {制品名}建模规范

> **数据契约**：<一句话定位>

## 1. 定位与适用范围            【必备】
## 2. 心智模型                  【条件必备】
## 3. 命名约定                  【条件必备】
## 4. Frontmatter 契约          【条件必备】
## 5. 正文结构契约              【必备】
## 6. 反模式                    【必备】
## 7. 示例                      【必备】
## 8. 与其他资产关系            【可选】
```

### 5.2 编号规则

- **统一数字编号**：所有 spec 用 `## N. <名>`，不用主题词标题
- **跳号允许**：若某章节不适用（条件必备的触发条件不成立），跳过该编号，**不重新排号**——保持跨 spec 的编号对位
- **首段统一**：H1 下紧跟单行 blockquote：`> **数据契约**：<一句话定位>`；附加说明应进 §1，不进 blockquote

### 5.3 校验集中

所有**正文结构**字段 / 章节的校验规则集中在 §5 内一次性列出；不允许散落到各字段定义后或 §6 反模式中。

§4 frontmatter 字段的校验（必填 / 类型 / 枚举）天然属于 §4，不视为散落。

§6 反模式列举"违反 §4 / §5 校验规则"的具体形态，不重复定义规则本身。

### 5.4 示例集中

所有示例集中在 §7；不在每个字段定义后追加示例（保持 §5 结构紧凑）。

---

## 6. 反模式

- ❌ 章节用主题词而非数字编号（如 `## 适用范围` 而非 `## 1. 定位与适用范围`）
- ❌ 不适用的条件必备章节强行加上（如运行时对象 spec 加 §3 命名约定 / §4 Frontmatter 契约）
- ❌ 校验规则散落到各字段定义内（应集中在 §5）
- ❌ 示例散落到各字段定义后（应集中在 §7）
- ❌ 反模式节重复定义校验规则（应只列违规形态，规则在 §4 / §5）
- ❌ frontmatter 缺 `id` / `name` / `description` / `version` 等必填字段
- ❌ `scope` 字段用 `>` 折叠而非 `|` 保留（前者吞掉换行）
- ❌ 因某节不适用而重新排号（应跳号保持对位）
- ❌ 首段 blockquote 含多段或附加说明（应只含一句话定位，附加说明进 §1）
- ❌ 把状态机语义独立成章节（应作为 §4.x 子节并入 Frontmatter 契约）
- ❌ 把文件存放路径写进 §3（§3 只规定命名，路径由项目治理决定）
- ❌ 正文写"变更记录"章节——spec 版本史由 git 历史 + frontmatter `version` 承担，不在正文重复
- ❌ 设立独立的"术语表"章节——术语不是制品本身的维度，应按性质分流：
  - 后续章节依赖的基础概念 / 心智框架 → 写入 §2 心智模型
  - 仅服务单个字段的术语 → 嵌入 §5 该字段的定义内（就近原则）
  - 行业通识术语（Gherkin / C4 模型 / IEEE 830 等） → 链接到外部术语表或外部参考

---

## 7. 示例

### 7.1 最小合规骨架（仅必备章节）

适用于描述运行时对象的 spec（制品本身无 frontmatter / 无状态机 / 无命名模式 / 无心智框架；spec 文档自身仍有 frontmatter）：

````markdown
---
id: WIDGET_SPEC_V1
name: Widget Schema
description: Spec defining the widget runtime object contract.
version: 1.0.0
status: active
lifecycle: living
created_at: 2026-05-21
scope: |
  Defines the structural contract for widget runtime objects passed between services.
---

# Widget 规范

> **数据契约**：定义 widget 运行时对象的字段与校验

## 1. 定位与适用范围
适用于 ...；不适用于 ...

## 5. 正文结构契约
| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| ... | ... | ... | ... |

## 6. 反模式
- ❌ ...

## 7. 示例
```json
{ "id": "...", "type": "..." }
```
````

注：跳过 §2 / §3 / §4 / §8，因为不适用。

### 7.2 完整骨架（含所有条件必备章节）

适用于文档类 spec（markdown 制品 + frontmatter + 状态机 + 命名模式 + 心智框架），例如 ADR：

```
# ADR 建模规范

> **数据契约**：...

## 1. 定位与适用范围
## 2. 心智模型               ← What/Why/Alternatives/Consequences
## 3. 命名约定               ← NNNN-{slug}.md
## 4. Frontmatter 契约       ← artifact_type / status / superseded_by / ...
   ### 4.2 状态机语义        ← proposed/accepted/superseded/archived/rejected
## 5. 正文结构契约           ← 4 节正文：背景 / 决策 / 替代方案 / 后果
## 6. 反模式
## 7. 示例
## 8. 与其他资产关系         ← 配套 rule、衰减政策
```

---

## 8. 与其他资产关系

- **递归适用**：本文件自身遵循此 meta-spec 定义的骨架（自示范）
- **下游 spec**：任何 spec 都继承本规范
- **写作纪律**：通用 markdown 写作纪律见各项目自身的文档管理 rule；本 meta-spec 暂无独立 rule
