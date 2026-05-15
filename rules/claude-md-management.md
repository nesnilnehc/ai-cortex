---
artifact_type: rule
name: claude-md-management
version: 1.0.0
scope: 所有层级 CLAUDE.md（个人 / 项目 / 模块）的撰写与维护
status: active
---

# Rule: CLAUDE.md 写作纪律（CLAUDE.md Management）

## 适用范围 (Scope)

所有撰写、修改、审计 CLAUDE.md 的行为，包括：

- 人工撰写
- AI 协助撰写
- Claude Code 内置 `/init` skill 自动生成的草案

`/init` 输出**不直接入库**，需经本 Rule §5 自检通过后方可 commit。

数据契约（章节结构、形态要求）见 [specs/claude-md-modeling.md](../specs/claude-md-modeling.md)；本 rule 约束行为面（篇幅、表达、禁区、修订、自检）。

---

## §1 篇幅控制

| 层级 | 上限 |
|---|---|
| 项目级（仓库根 `CLAUDE.md`） | ≤ 300 行 |
| 模块级（子目录 `CLAUDE.md`） | ≤ 100 行 |
| 个人级（`~/.claude/CLAUDE.md`） | 不强制，建议同等克制 |

超出项目级上限时，先拆分模块级 CLAUDE.md，再精简（删低价值条目）。**不允许通过加副 spec 链接绕过上限**——CLAUDE.md 是直接加载的，加载量本身即成本。

---

## §2 表达方式

### 使用祈使句或断言

✅ "使用 pnpm，不要用 npm"
❌ "本项目的包管理器经过团队讨论后决定使用 pnpm，因为..."

### 关键约束显式标注

不可违反的规则用 `IMPORTANT:` / `NEVER:` / `ALWAYS:` 前缀。模型对这些信号敏感，标注后更易在生成时被遵守。

### 负面清单优于正面要求

"不要做 X" 比 "应该做 Y" 更易被遵守。能用禁令表达的，优先用禁令。

### 不使用模糊措辞

避免 "尽量"、"建议"、"最好"。规则的约束强度需明确：要么是强制，要么删除。

---

## §3 内容禁区

CLAUDE.md 中**禁止**写以下内容：

| 禁区 | 理由 |
|---|---|
| 通用编程知识（Docker / REST / 测试金字塔等） | AI 已知，写入只稀释 context |
| 易变状态（sprint、owner、待办、临时分支名） | 此类信息应在 issue tracker / wiki 中维护 |
| 敏感信息（密钥、token、生产 IP、内部域名、PII） | 安全风险；CLAUDE.md 进入 git 即泄露 |
| README / CONTRIBUTING / 架构文档的完整复述 | 双源不一致；用链接引用即可 |
| "以防万一" 的预测性规则 | 规则必须来自真实痛点，不来自预测 |

---

## §4 修订原则

### 删除测试（每条规则必过）

新增任何规则前自问：**删掉这条之后，AI 行为是否会变差？**

- 是 → 保留
- 否 → 不加

### 何时修订

- AI 反复犯同样的错（说明规则缺失或不清晰）
- 团队约定发生变化
- 关联 spec 升级，需对齐——特别是 [spec §5 必备章节](../specs/claude-md-modeling.md#5-必备章节项目级) 或 [§3 强制范围](../specs/claude-md-modeling.md#3-适用范围与强制范围) 变更时，必须同步审查本 rule §1 篇幅控制 与 §5 自检清单
- 月度回顾发现的改进点

### 何时不修订

- 一次性偶发问题
- 单个项目的特殊情况（应放进项目 CLAUDE.md，而非提升为通用规则）
- 未实践验证的设想

### DRY

重叠内容用链接引用而非复制。同一信息只在一处维护。

---

## §5 自检清单

Commit 任何 CLAUDE.md 变更前，逐项确认：

- [ ] 必备章节齐全（见 [spec §5](../specs/claude-md-modeling.md#5-必备章节项目级)）
- [ ] 层级职责无串台（见 [spec §4](../specs/claude-md-modeling.md#4-三层结构与职责切分)）
- [ ] 形态要求达标——简洁 / 可执行 / 决策导向 / 就近原则（见 [spec §7](../specs/claude-md-modeling.md#7-形态要求)）
- [ ] 篇幅符合本 rule §1 上限
- [ ] 关键约束已用 `IMPORTANT:` / `NEVER:` / `ALWAYS:` 标注（见 §2）
- [ ] 无 §3 禁区内容（通用知识 / 易变状态 / 敏感信息 / README 复述 / 预测性规则）
- [ ] 重叠内容用链接而非复制（见 §4 DRY）
- [ ] 每条新增规则通过删除测试（见 §4）

---

## 违规示例

```markdown
<!-- ❌ 通用知识科普 -->
## Docker

Docker 是一个容器化平台，使用 Dockerfile 定义镜像...
```

```markdown
<!-- ❌ 易变状态 -->
## 当前任务

- [ ] @zhangsan 在做 OAuth 重构（预计 Q3 完成）
- [ ] @lisi 负责数据库迁移
```

```markdown
<!-- ❌ 模糊措辞 -->
## 测试

尽量写测试，最好覆盖率高一些。
```

```markdown
<!-- ❌ README 复述 -->
## 项目介绍

（粘贴了 README 前 50 行）
```

---

## 修正指南

1. **超长**：拆模块级 CLAUDE.md，或删除"通用知识"段
2. **散文化**：改写为祈使句；保留约束，删除论证
3. **禁区内容渗入**：通用知识删除；易变状态移到 issue tracker；敏感信息立即移除并轮换
4. **缺关键标注**：高代价规则加 `IMPORTANT:` 前缀并挪至文末
5. **README 复述**：替换为 `> 项目介绍见 [README.md](README.md)` 链接

---

## 相关指引

- 数据契约：[specs/claude-md-modeling.md](../specs/claude-md-modeling.md)
- 文档管理通则：[rules/workflow-documentation.md](./workflow-documentation.md)

---

## 变更记录

### 1.0.0 — 2026-05-15

**Initial Release**：定义 5 §约束（篇幅、表达、禁区、修订、自检），自检清单逐项引用 spec 作为标尺，与 [specs/claude-md-modeling.md](../specs/claude-md-modeling.md) 配套。
