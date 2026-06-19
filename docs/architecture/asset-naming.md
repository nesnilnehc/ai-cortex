---
artifact_type: naming-convention
created_by: ai-cortex
lifecycle: living
created_at: 2026-05-09
status: active
---

# 资产命名规范

> 4 类资产（Spec / Protocol / Skill / Rule）的命名约定。新增资产前必读。
>
> 类型边界与判别见 [terminology.md](terminology.md)。

---

## 一、通用规则（4 类共同遵守）

1. **kebab-case**：全小写，单词间用连字符 `-`
2. **路径与 frontmatter `name` 字段一致**：文件 `skills/foo-bar/SKILL.md` 的 `name: foo-bar`
3. **英文，禁拼音 / 中文**：机器消费字段保持英文便于跨工具协作
4. **不连续连字符**：`foo--bar` 禁；`foo-bar` 通
5. **不以 `-` 开头或结尾**

---

## 二、Spec（规范）

定位：定义事物本身的结构与行为契约（见 [terminology.md §一](terminology.md#一四个概念)）。

**命名公式**：**主词为被定义对象的名词**（noun-first）

- `<thing-being-specified>`
- 例：`universal-notification`（定义通知对象）、`requirement-modeling`（定义需求文档结构）

**反例**：

- ❌ `define-notification`（动词开头是 Skill 风格）
- ❌ `notification-protocol`（"协议" 是 Protocol 类型，混淆）

---

## 三、Protocol（协议）

定位：定义多个实体之间如何交互——步骤、状态、消息序列。

**命名公式**：**对象 + 行为**（表达谁在跟谁做什么）

- `<actor-or-domain>-<action>`
- 例：`im-notification-delivery`（IM 渠道 + 投递通知）

**反例**：

- ❌ `notification`（仅名词，是 Spec 风格）
- ❌ `delivery-protocol`（在 Protocol 后缀里再加 "protocol" 冗余）

---

## 四、Skill（技能）

定位：单一 Agent 可调用的能力（目标 + 执行 + 示例）。遵循 [agentskills.io](https://agentskills.io) 标准。

**命名公式**：**verb-noun**（动宾结构）

- `<verb>-<noun>`
- 例：`commit-work`、`generate-readme`、`review-typescript`、`define-mission`

### 4.1 Review 家族

```
review-<language>            如 review-python、review-typescript
review-<framework>           如 review-react、review-vue
review-<domain>-usage        如 review-orm-usage
review-<concern>             如 review-security、review-performance、review-architecture、review-testing
```

### 4.2 Define 家族

```
define-<noun>                如 define-mission、define-roadmap、define-vision
```

### 4.3 其他常见 verb 前缀

```
generate-<noun>              如 generate-standard-readme、generate-github-workflow
orchestrate-<noun>           编排技能强制 orchestrate- 前缀（详见 §四 编排 vs 原子 vs 元）
archive-<noun>               如 archive-milestone
capture-<noun>               如 capture-work-items
prioritize-<noun>            如 prioritize-backlog
promote-<noun>               如 promote-roadmap-items
deliver-<noun>               如 deliver-feature
integrate-<noun>             如 integrate-branches
refine-<noun>                如 refine-skill-design
plan-<noun>                  如 plan-next
automate-<noun>              如 automate-tests
commit-<noun>                如 commit-work
decontextualize-<noun>       如 decontextualize-text
```

### 4.4 反例

- ❌ `code-review`（noun-verb 反向，应为 `orchestrate-code-review`）
- ❌ `documentation`（仅名词，看不出动作）
- ❌ `ts-review`（缩写不明）

---

## 五、Rule（规则）

定位：单一可校验约束。

**命名公式**：**前缀 + 被约束对象**

```
standards-<technology-or-domain>     技术规范（编码、Shell、import 等）
workflow-<concern>                   工作流约束（文档、文档生命周期等）
documentation-<aspect>               文档输出约束（如 markdown 格式）
tools-<tool-or-action>               工具使用约束（如 list-dir 行为）
writing-<style-or-language>          写作风格约束（如中文技术文）
```

### 现有 Rule 命名例

```
standards-coding              编码通用准则
standards-shell               Shell 脚本规范
standards-import              引用管理
workflow-document-lifecycle   治理文档生命周期
workflow-documentation        文档管理策略
documentation-markdown-format Markdown 格式
tools-list-dir-dotfiles       目录列举工具行为
writing-chinese-technical     中文技术写作
requirement-quality           需求文档质量评审清单（无标准前缀，名词主导，仅当前缀都不贴切时使用）
```

### 反例

- ❌ `coding`（缺前缀，不知约束哪一类）
- ❌ `markdown-rule`（"rule" 后缀冗余）

---

## 六、检查清单（新增资产前自检）

- [ ] 类型已确定（Spec / Protocol / Skill / Rule，按 [terminology.md](terminology.md) 4 组判别）
- [ ] 命名遵循通用规则（kebab-case、英文、与目录一致）
- [ ] 命名遵循对应类型的命名公式
- [ ] 在同类资产中无名称冲突
- [ ] 不与已弃用资产同名

---

## 七、相关文档

- [terminology.md](terminology.md) — 4 类资产的定义与判别
- [agentskills.io](https://agentskills.io) — Skill 标准格式（外部权威）
- [CONTRIBUTING.md](../../CONTRIBUTING.md) — 贡献流程
