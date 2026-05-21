---
id: SPEC_MODELING_SPEC_V1
name: Spec Modeling Schema (Meta-Spec)
description: Meta-spec defining the structural contract that all specs under specs/ must follow — frontmatter contract, body section skeleton, and required/conditional/optional section taxonomy.
version: 1.0.0
status: active
lifecycle: living
created_at: 2026-05-21
scope: |
  Defines the structural contract for all spec documents under specs/.
  Applies recursively to this file itself. Establishes the required / conditional /
  optional section taxonomy and frontmatter requirements that downstream specs inherit.
related:
  - ./adr-modeling.md
  - ./claude-md-modeling.md
  - ./design-modeling.md
  - ./requirement-modeling.md
  - ./task-modeling.md
  - ./universal-notification.md
---

# Spec 建模规范（Meta-Spec）

> **数据契约**：定义 `specs/` 下所有 spec 文档的结构骨架与字段约束
>
> 本规范是 spec 的 spec——所有 `specs/` 下的 spec 文档（包含本文件自身）必须遵循此处定义的章节骨架与 frontmatter 契约。

---

## 1. 定位与适用范围

本规范约束 `specs/` 目录下所有 spec 文档的写作骨架。每份 spec 定义一类制品的数据契约（字段、章节、状态、校验）；本 meta-spec 定义这些 spec 自身应如何组织。

适用：

- `specs/` 下的所有 `*.md` 文件（含本文件）

不适用：

- 配套的 rule（行为约束，结构由 [rules/](../rules/) 自治）
- protocols（流程描述，结构由 [protocols/](../protocols/) 自治）
- 制品本身（spec 描述的对象，由具体 spec 定义）

---

## 2. 核心心智模型：章节的三态

一份合格 spec 的本质维度是"它的每个章节按何时该写如何分类"。三态（必备 / 条件必备 / 可选）就是这个维度的答案——所有后续章节都依赖此分类。

每份 spec 的章节按"何时该写"分为三态：

| 类型 | 触发条件成立时 | 触发条件不成立时 |
|---|---|---|
| **必备** | 必须写（恒成立，无条件） | — |
| **条件必备** | 必须写 | **不该写**（写了即冗余） |
| **可选** | 可写 | 可不写 |

### 关键差异

- **必备 vs 条件必备**：必备无触发条件；条件必备只在某个特征成立时才该出现
- **条件必备 vs 可选**：条件必备是二值开关（满足条件就必须写，不满足就不该写）；可选是作者自由判断

### 章节分类速查

| 章节 | 类型 | 触发条件（如有） |
|---|---|---|
| §1 定位与适用范围 | 必备 | — |
| §2 核心心智模型 | 条件必备 | 制品有显著思维框架（N 个核心问题） |
| §3 路径与命名约定 | 条件必备 | 制品落盘且文件名 / 路径需约束 |
| §4 Frontmatter 契约 | 条件必备 | 制品是 markdown 且有 frontmatter |
| §5 正文结构契约 | 必备 | — |
| §6 状态枚举 | 条件必备 | 制品有生命周期状态机 |
| §7 反模式 | 必备 | — |
| §8 示例 | 必备 | — |
| §9 与其他资产关系 | 可选 | — |

---

## 3. 路径与命名约定

```
specs/<artifact-name>-modeling.md
```

- 一份 spec 一个文件，扁平存放于 `specs/` 根目录
- 文件名格式：`<artifact-name>-modeling.md`（如 `adr-modeling.md`）
- 例外：meta-spec 本身命名为 `spec-modeling.md`，描述运行时对象的 spec 可不带 `-modeling` 后缀（如 `universal-notification.md`）

---

## 4. Frontmatter 契约

```yaml
---
id: <UPPER_SNAKE>_SPEC_V<n>
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
---
```

### 字段表

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `id` | string | 必 | 格式 `<UPPER_SNAKE>_SPEC_V<n>`（如 `ADR_MODELING_SPEC_V1`） |
| `name` | string | 必 | 英文 spec 名称 |
| `description` | string | 必 | 一句话英文摘要（≤ 200 字符） |
| `version` | string | 必 | SemVer 版本号 |
| `status` | enum | 必 | `active` / `draft` / `superseded` / `archived` |
| `lifecycle` | enum | 必 | 固定 `living`（spec 本身持续演化） |
| `created_at` | date | 必 | spec 首次发布日期（`YYYY-MM-DD`） |
| `scope` | string | 必 | 多行说明适用范围；使用 `\|` 而非 `>`（保留换行） |
| `related` | list[path] | 可选 | 关联资产相对路径列表 |

---

## 5. 正文结构契约

### 5.1 章节顺序

```markdown
# {制品名}建模规范

> **数据契约**：<一句话定位>

## 1. 定位与适用范围            【必备】
## 2. 核心心智模型              【条件必备】
## 3. 路径与命名约定            【条件必备】
## 4. Frontmatter 契约          【条件必备】
## 5. 正文结构契约              【必备】
## 6. 状态枚举                  【条件必备】
## 7. 反模式                    【必备】
## 8. 示例                      【必备】
## 9. 与其他资产关系            【可选】
```

### 5.2 编号规则

- **统一数字编号**：所有 spec 用 `## N. <名>`，不用主题词标题
- **跳号允许**：若某章节不适用（条件必备的触发条件不成立），跳过该编号，**不重新排号**——保持跨 spec 的编号对位
- **首段统一**：H1 下紧跟 blockquote：`> **数据契约**：<一句话定位>`

### 5.3 校验集中

所有字段 / 章节的校验规则必须集中在 §5 正文结构契约内一次性列出；不允许散落到各字段定义后或 §7 反模式中。

§7 反模式列举"违反 §5 校验规则"的具体形态，不重复定义规则本身。

### 5.4 示例集中

所有示例集中在 §8；不在每个字段定义后追加示例（保持 §5 结构紧凑）。

### 5.5 条件必备的触发判断

| 章节 | 触发条件成立的判断 |
|---|---|
| §2 核心心智模型 | 制品有"N 个核心问题"心智框架（如 ADR 的 What/Why/Alt/Consequences）？ |
| §3 路径与命名约定 | 制品落盘且文件路径 / 命名需要约束（如 `NNNN-{slug}.md`）？ |
| §4 Frontmatter 契约 | 制品是 markdown 且有 frontmatter？运行时 JSON 对象 / 无 frontmatter → 不该写此节 |
| §6 状态枚举 | 制品有生命周期状态机（如 ADR / task 的状态流转）？ |

---

## 6. 状态枚举（spec 自身）

| 状态 | 含义 |
|---|---|
| `draft` | 初稿，尚未稳定 |
| `active` | 当前有效 |
| `superseded` | 已被新版本 spec 替代（需在 frontmatter 标注替代关系） |
| `archived` | 已归档，不再维护 |

---

## 7. 反模式

- ❌ 章节用主题词而非数字编号（如 `## 适用范围` 而非 `## 1. 定位与适用范围`）
- ❌ 不适用的条件必备章节强行加上（如运行时对象 spec 加 §4 Frontmatter 契约节）
- ❌ 校验规则散落到各字段定义内（应集中在 §5）
- ❌ 示例散落到各字段定义后（应集中在 §8）
- ❌ 反模式节重复定义校验规则（应只列违规形态，规则在 §5）
- ❌ frontmatter 缺 `id` / `name` / `description` / `version` 等必填字段
- ❌ `scope` 字段用 `>` 折叠而非 `|` 保留（前者吞掉换行）
- ❌ 因某节不适用而重新排号（应跳号保持对位）
- ❌ 设立独立的"术语表"章节——术语不是制品本身的维度，应按性质分流：
  - 后续章节依赖的基础概念 / 心智框架 → 写入 §2 核心心智模型
  - 仅服务单个字段的术语 → 嵌入 §5 该字段的定义内（就近原则）
  - 行业通识术语（Gherkin / C4 模型 / IEEE 830 等） → 链接到 [docs/architecture/terminology.md](../docs/architecture/terminology.md) 或外部参考

---

## 8. 示例

### 8.1 最小合规骨架（仅必备章节）

适用于运行时对象类 spec（无 frontmatter / 无状态机 / 无路径约束 / 无心智框架）：

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

## 7. 反模式
- ❌ ...

## 8. 示例
```json
{ "id": "...", "type": "..." }
```
````

注：跳过 §2 / §3 / §4 / §6 / §9，因为不适用。

### 8.2 完整骨架（含所有条件必备章节）

适用于文档类 spec（markdown 制品 + frontmatter + 状态机 + 路径约束 + 心智框架），例如 ADR：

```
# ADR 建模规范

> **数据契约**：...

## 1. 定位与适用范围
## 2. 核心心智模型           ← What/Why/Alternatives/Consequences
## 3. 路径与命名约定         ← docs/adr/NNNN-{slug}.md
## 4. Frontmatter 契约       ← artifact_type / status / superseded_by / ...
## 5. 正文结构契约           ← 4 节正文：背景 / 决策 / 替代方案 / 后果
## 6. 状态枚举               ← proposed / accepted / superseded / archived / rejected
## 7. 反模式
## 8. 示例
## 9. 与其他资产关系         ← 配套 rule、衰减政策
```

---

## 9. 与其他资产关系

- **递归适用**：本文件自身遵循此 meta-spec 定义的骨架（自示范）
- **下游 spec**：`specs/*.md` 全部继承本规范
- **写作纪律**：通用 markdown 写作纪律见 [rules/workflow-documentation.md](../rules/workflow-documentation.md)；本 meta-spec 暂无独立 rule
