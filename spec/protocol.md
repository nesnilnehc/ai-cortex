# 协议规范 (Protocol Specification)

状态：必选
版本：1.0.0
范围：`protocols/` 下所有文件。

**变更日志**：

- v1.0.0 (2026-03-25)：初稿 — 定义 Protocol 的元数据、8 个必选标题节、文件结构规范、质量要求

---

## 1. 文件结构与命名

### 1.1 目录规范

**单文件协议**（推荐）：
```
protocols/{kebab-case-name}.md
```
示例：`protocols/universal-notification-protocol.md`、`protocols/requirement-modeling-protocol.md`

**协议簇（复杂协议，目录结构）**：
```
protocols/{domain}/{protocol-name}/
├── PROTOCOL.md           # 核心协议定义（必需，自包含）
└── examples/             # 示例文件（可选）
    ├── example-1.md
    └── example-2.md
```

### 1.2 协议命名规范

**`name` 字段（元数据中）**：
- **推荐**：使用全名（如 `Universal Notification Protocol`）
- **避免**：纯缩写（如 ~~`UNP`~~）
- **原因**：全名便于发现、可读性强、避免缩写歧义

**文件路径命名**：
- 采用 `kebab-case`
- 应与 `name` 字段语义对应
- 例：`name: "Universal Notification Protocol"` → 文件路径 `protocols/universal-notification-protocol.md`

**向后兼容**：
- 现有缩写协议（UNP、INP）可逐步改为全名
- 过渡期间可保留短别名文件（如 `protocols/unp.md` 作为指向新文件的参考）

### 1.3 自包含原则

**单文件自包含**（对标 Skill 规范）：
- 主协议文件（`PROTOCOL.md` 或 `{name}.md`）必须完全自包含
- Agent 加载该文件即可获取完整的协议定义
- 不依赖目录下其他 MD 文件即可理解协议

**外部资源引用**：
- `examples/` 子目录存放完整的应用示例
- 在主文件中通过 Markdown 链接 (`[example](examples/xxx.md)`) 引用
- 不创建 `references/` 子目录（项目特定的集成指南应在项目内部，不在协议中）

---

## 2. 必选 YAML 元数据

每个 `PROTOCOL.md` 或 `*.md` 协议文件必须以以下内容开头：

```yaml
---
id: [NAME_SPEC_V{major}]              # 全局唯一标识
name: [Protocol Name]                 # 协议全名
description: [One-line summary]       # 简要描述（供发现和语义匹配）
version: [x.y.z]                      # 语义版本号
status: active                        # active | deprecated | retired
lifecycle: living                     # living | stable
created_at: [ISO 8601 date]          # 协议首次发布日期
scope: |                              # 多行：适用场景、问题域、业务背景
  Applicable whenever...
related: [optional array]             # 可选：关联协议的相对路径
canonical_url: [optional]             # 可选：远程 URL（用于 manifest.json）
---
```

### 2.1 元数据字段规范

| 字段 | 类型 | 必/可 | 说明 |
|------|------|-------|------|
| `id` | string | 必 | 全局唯一标识，格式：`{PROTOCOL_NAME}_SPEC_V{MAJOR}`（全大写，下划线分隔）。例：`UNP_SPEC_V1`、`REQUIREMENT_MODELING_SPEC_V1` |
| `name` | string | 必 | 协议全名（1-80 字）。例：`Universal Notification Protocol`（✅）、~~`UNP`~~（❌） |
| `description` | string | 必 | 单行摘要（供语义搜索）。≤120 字。 |
| `version` | semver | 必 | 语义化版本（MAJOR.MINOR.PATCH）。见 §2.2 版本管理 |
| `status` | enum | 必 | 协议状态。`active` \| `deprecated` \| `retired` |
| `lifecycle` | enum | 必 | 生命周期模型。`living`（允许 breaking changes）\| `stable`（breaking changes 需新版本） |
| `created_at` | ISO 8601 | 必 | 协议首次发布日期。格式：`YYYY-MM-DD` |
| `scope` | text | 必 | 多行文本，详细说明：协议适用的问题域、被应用的场景、边界条件 |
| `related` | array | 可 | 关联协议的相对路径或 canonical URL。例：`[./inp.md]` |
| `canonical_url` | URL | 可 | 远程 URL，用于 manifest.json。例：`https://raw.githubusercontent.com/.../protocol.md` |

### 2.2 版本管理

采用**语义化版本**（MAJOR.MINOR.PATCH）：

- **MAJOR** 递增：协议核心内容重大变更或破坏性变更（如删除必需字段、改变强制规则语义）
- **MINOR** 递增：向后兼容的扩展（如新增可选字段、新增 Hard Rules、示例补充）
- **PATCH** 递增：勘误、措辞优化、明确说明（无逻辑变更）

**breaking changes 处理**：
- `lifecycle: living` — 允许 breaking changes，需明确通知消费者（更新日志、AGENTS.md 等）
- `lifecycle: stable` — breaking changes 需创建新的 MAJOR 版本，旧版本标记为 `deprecated`

---

## 3. 必选标题结构（8 个必选节）

每个协议必须包含以下 8 个标题节（可选的附录除外）：

```markdown
# [Protocol Name]

> **Semantic Role**: [WHAT vs HOW] 说明协议在系统中的语义角色

## 1. Purpose / 目的

## 2. Core Principles / 核心原则

## 3. Required Schema / 必需规范

## 4. Hard Rules / 强制规则

## 5. Anti-Patterns / 反模式

## 6. Scope Boundaries / 范围边界

## 7. Examples / 示例

## 8. AI Refactor Instruction / AI 重构指令

## Appendix / 附录（可选）
```

### 3.1 各节的详细说明

#### 标题前的 Semantic Role 块（必选）

使用 blockquote 说明协议在系统中的语义角色（WHAT 还是 HOW）。

示例：
```
> **Semantic Role**: UNP 定义通知的"是什么"（结构、意图、优先级），
> 与 INP 的"怎么做"（渠道、投递）形成分层。
```

#### 1. Purpose / 目的（必选）

一段话（2-3 句）说明协议的核心价值与解决的问题。

**示例**：
```markdown
## Purpose / 目的

定义需求建模的标准框架，确保所有需求在提交评审前包含关键信息
（背景、验收标准、风险评估等），提高需求质量和可追踪性。
```

#### 2. Core Principles / 核心原则（必选，4-5 条）

列举协议的基础承诺。每条包括原则名和 1-2 句说明。

范围：3-6 条（推荐 4-5 条）。太少无法覆盖，太多容易失焦。

**示例**：
```markdown
## 2. Core Principles / 核心原则

- **Completeness**: 需求必须包含所有 7 个必填字段，确保信息完整。
- **Verifiability**: 验收标准必须可测试、无歧义（采用 BDD 格式）。
- **Traceability**: 需求必须明确来源和依赖，支持端到端追踪。
- **Simplicity**: 不同需求类型有相应的简化规则，避免过度流程。
- **Risk-Awareness**: 风险和假设必须提前识别，采用定量评估（概率×影响）。
```

#### 3. Required Schema / 必需规范（必选）

定义协议的核心数据结构或要素。通常采用表格形式。

**示例**：
```markdown
## 3. Required Schema / 必需规范

| 字段 | 类型 | 必/可 | 说明 |
|------|------|-------|------|
| Requirement ID | String | 必 | 唯一标识，格式：`M{n}-REQ-{nn}` |
| Title | String | 必 | 一句话概括，≤80 字 |
| Background | Text | 必 | 问题背景和期望状态 |
| Acceptance Criteria | List | 必 | ≥3 个可测试的验收标准 |
| Dependencies | List | 必 | 依赖的需求和前置条件 |
| Risks & Constraints | Object | 必 | 风险（优先度）、约束、假设 |
| Requirement Source | Object | 必 | 需求来源、决策背景 |
```

#### 4. Hard Rules / 强制规则（必选）

编号列表，描述协议的强制性约束。使用 **MUST**、**MUST NOT**、**FORBIDDEN** 等强制性词汇。

每条规则需包括：(1) 规则标题，(2) 强制级别，(3) 说明，(4) 验证方式。

**示例**：
```markdown
## 4. Hard Rules / 强制规则

1. **All 7 Required Fields MUST be Present** (MUST)
   每个需求提交前必须包含全部 7 个必填字段。
   验证：通过自检清单逐一检查。

2. **Acceptance Criteria MUST NOT Contain Ambiguous Words** (MUST NOT)
   验收标准不得使用 "significant"、"fast"、"good" 等模糊词。
   使用 Gherkin BDD 格式（Given/When/Then）。

3. **Risk Priority MUST be Calculated as Probability × Impact** (MUST)
   风险优先度不得凭主观判断，必须用公式计算。
   验证：检查是否有 P（概率）和 I（影响）的量化值。
```

#### 5. Anti-Patterns / 反模式（必选）

对比正确与错误的做法。采用 ✅ 和 ❌ 标记。

**示例**：
```markdown
## 5. Anti-Patterns / 反模式

### ✅ 正确做法

**Acceptance Criteria**:
- Given 用户输入有效的电子邮件地址
- When 点击提交按钮
- Then 系统返回成功消息并存储该地址

### ❌ 错误做法

**Acceptance Criteria**:
- 系统应该能处理电子邮件
- 需要支持快速验证

**问题**："能处理"、"快速" 都是模糊词，无法验证。
```

#### 6. Scope Boundaries / 范围边界（必选）

明确协议**负责什么**和**不负责什么**。

**示例**：
```markdown
## 6. Scope Boundaries / 范围边界

**在范围内**：
- 定义需求的必填字段和验证标准
- 指导如何编写验收标准（Gherkin 格式）
- 定义风险评估方法和自检清单

**超出范围**：
- 项目特定的工具集成（如禅道配置）
- 组织级的工作流（如评审人员角色定义）
- 工作量估算和容量规划（未来的 v2.0 功能）
```

#### 7. Examples / 示例（必选，≥2 个）

展示协议的完整、可工作的示例。至少 2 个不同场景。

示例可：
- 内联于 PROTOCOL.md 中
- 或链接到 `examples/` 子目录的独立文件

**示例**：
```markdown
## 7. Examples / 示例

### 示例 1：功能需求

[参考 examples/functional-requirement.md](examples/functional-requirement.md)

### 示例 2：缺陷修复

[参考 examples/bug-fix.md](examples/bug-fix.md)
```

#### 8. AI Refactor Instruction / AI 重构指令（必选）

给 AI Agent 的具体行动指令，支持自动应用和检查。

**示例**：
```markdown
## 8. AI Refactor Instruction / AI 重构指令

当 Agent 遇到不符合协议的需求时，执行以下步骤：

1. **检查必填字段**：逐一验证 7 个必填字段是否存在
2. **检查验收标准**：确保使用 Gherkin BDD 格式（Given/When/Then）
3. **计算风险优先度**：如果风险缺少量化值（P×I），提示补充
4. **建议修复方案**：生成修复后的需求草稿，供用户确认

工具支持：
- 可集成 markdown-linter 检查语法
- 可调用 `capture-work-items` 技能创建符合协议的项目条目
```

### 3.2 可选附录

```markdown
## Appendix: Versioning & Breaking Changes / 附录：版本与破坏性变更

说明该协议的版本化政策和 breaking changes 如何处理。

## Appendix: Related Artifacts / 附录：相关制品

引用 manifest.json、设计文档、相关协议等的链接。
```

---

## 4. 质量要求

协议必须满足以下条件方可发布：

### 4.1 完整性（Completeness）

- ✅ 包含所有 8 个必选标题节（不计可选附录）
- ✅ 元数据完整（id、name、version、status、lifecycle、created_at、scope 等）
- ✅ Core Principles ≥ 4 条
- ✅ Required Schema 清晰（表格或列表）
- ✅ Hard Rules ≥ 3 条，每条有明确的强制级别和验证方式
- ✅ Examples ≥ 2 个完整示例

### 4.2 可验证性（Verifiability）

- ✅ Hard Rules 使用明确的强制性词汇（**MUST**、**MUST NOT**、**FORBIDDEN**）
- ✅ 每条规则有明确的验证方式或检查清单
- ✅ Anti-Patterns 包含具体的代码/文本示例和问题分析
- ✅ Examples 可直接应用或参考，不含项目特定内容

### 4.3 清晰性（Clarity）

- ✅ Semantic Role 明确说明协议的定位（WHAT vs HOW）
- ✅ Scope Boundaries 清晰列举范围内外的职责
- ✅ 无模糊或歧义的术语（使用术语表或明确定义）
- ✅ 示例与反例形成对比

### 4.4 可执行性（Executability）

- ✅ AI Refactor Instruction 提供具体的行动指令
- ✅ 支持自动化检查或应用（如通过 linting 工具）
- ✅ 提供表格化的规则映射或检查清单

### 4.5 可追踪性（Traceability）

- ✅ 有明确的版本号（MAJOR.MINOR.PATCH）和创建时间
- ✅ breaking changes 需在版本号（MAJOR 递增）中反映
- ✅ 相关协议通过 `related` 字段明确链接
- ✅ 更新日志清晰记录各版本的变更内容

---

## 5. 协议与 Skill/Rule 的边界

### 5.1 三层治理资产对比

| 资产 | 用途 | 定义内容 | 加载方式 | 生命周期 | 示例 |
|------|------|---------|---------|---------|------|
| **Protocol** | 接口契约 | 数据结构、必需字段、强制规则 | 常驻或按需 | 版本化、breaking changes 管理 | UNP（通知结构）、Requirement Modeling（需求字段） |
| **Skill** | 主动能力 | 目标、流程、输入输出 | 按需注入（任务触发时） | 版本化、依赖管理 | `review-code`、`capture-work-items` |
| **Rule** | 被动约束 | 行为约束、工作流规范、质量标准 | 常驻加载（长期背景） | 版本化、优先级管理 | `writing-chinese-technical`、`standards-coding` |

### 5.2 使用场景示例

**场景 1：设计通知系统**
- 加载 Protocol：UNP（语义层）+ INP（投递层）→ 定义通知结构
- 调用 Skill：无需调用（Protocol 本身是设计基准）
- 遵守 Rule：`writing-chinese-technical` 等通用约束

**场景 2：创建需求条目**
- 加载 Protocol：Requirement Modeling Protocol → 确保需求包含 7 个字段
- 调用 Skill：`capture-work-items` → 自动创建符合协议的条目
- 遵守 Rule：`standards-coding`（如有代码字段）等约束

---

## 6. Protocol 在 manifest.json 中的注册

协议在 `manifest.json` 中的注册示例：

```json
{
  "protocols": [
    {
      "id": "UNP_SPEC_V1",
      "name": "Universal Notification Protocol",
      "version": "1.0.0",
      "status": "active",
      "lifecycle": "living",
      "path": "protocols/universal-notification-protocol.md",
      "canonical_url": "https://raw.githubusercontent.com/nesnilnehc/ai-cortex/main/protocols/universal-notification-protocol.md"
    }
  ]
}
```

**注册时更新协议索引**：在提交前，更新 `protocols/INDEX.md` 中的协议列表。

---

## 7. Self-Check / 自检清单

发布新协议前，使用以下清单进行自检：

- [ ] **元数据**：id、name、version、status、lifecycle、created_at、scope 齐全
- [ ] **必选节**：包含 8 个必选标题节（不计可选附录）
- [ ] **Core Principles**：≥ 4 条，清晰表达核心承诺
- [ ] **Hard Rules**：≥ 3 条，使用强制性词汇，有验证方式
- [ ] **Examples**：≥ 2 个完整示例，无项目特定内容
- [ ] **Scope Boundaries**：清晰列举范围内外的职责
- [ ] **AI Refactor Instruction**：提供具体的行动指令
- [ ] **Semantic Role**：明确说明 WHAT vs HOW 的定位
- [ ] **Anti-Patterns**：包含具体的反面示例和问题分析
- [ ] **版本管理**：确认版本号符合语义化版本规范
- [ ] **可读性**：无模糊术语，示例清晰可应用

---

## 相关文档

- `AGENTS.md` — Protocol 的加载和使用机制
- `protocols/INDEX.md` — 协议注册表和索引
- `manifest.json` — 协议的 canonical URL 和元数据
- `spec/skill.md` — Skill 规范（Protocol 的文件结构对标）
