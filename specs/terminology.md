---
id: TERMINOLOGY_SPEC_V1
name: Terminology Definition
description: Core concepts (Spec, Protocol, Skill, Rule) and definitions for AI Cortex
version: 1.0.0
status: active
lifecycle: stable
created_at: 2026-03-25
---

# AI Cortex 核心术语

> **这是一份元规范**：定义项目中 Spec、Protocol、Skill、Rule 四个核心概念的含义和边界。
> 所有项目文档必须遵循此术语定义，保持一致性。

---

## 1. 术语表

| 英文 | 中文 | 定义 | 位置 | 示例 |
| ------ | ------ | ------ | ------ | ------ |
| **Spec** | **规范** | 定义"是什么"：数据结构、字段、接口契约、必需格式 | `specs/`、`specs/` | `specs/universal-notification.md`（UNP 定义通知结构） |
| **Protocol** | **协议** | 定义"怎么做"：交互流程、各步骤的约束、应用哪些 Rule | `protocols/` | `protocols/im-notification-delivery.md`（INP 定义通知投递流程） |
| **Skill** | **技能** | 定义能力目标、执行流程、输入输出、处理规范 | `skills/` | `review-code`、`capture-work-items` |
| **Rule** | **规则** | 最小可执行约束：行为准则、风格约束、质量要求 | `rules/` | `writing-chinese-technical`、`standards-coding` |

---

## 2. 详细定义

### 2.1 Spec（规范）

**定义**：定义"是什么"——数据结构、必需字段、接口契约。

**特征**：

- 描述数据的样子或系统应有的接口
- 包含强制字段、可选字段、数据类型、验证规则
- 不描述流程或交互
- 是 Protocol 和 Skill 的基础

**何时使用**：

- 定义某个数据对象的结构（如通知、需求）
- 定义 API 的输入输出契约
- 定义文档或制品的必需字段

**示例**：

- UNP (Universal Notification Protocol)：定义通知对象有哪些字段（id、title、priority、intent 等）
- Requirement Modeling Protocol：定义需求有哪些必填字段（需求 ID、标题、验收标准等）

---

### 2.2 Protocol（协议）

**定义**：定义"怎么做"——交互流程、各步骤的约束、应用哪些 Rule。

**特征**：

- 描述多个步骤如何流转
- 每个步骤可能应用特定的 Spec 或 Rule
- 有明确的起点、中间步骤、终点
- 在步骤间定义验证和转换规则

**何时使用**：

- 定义某个系统/渠道的投递流程
- 定义代码审查、需求评审的具体步骤
- 定义数据从一个系统流向另一个系统的过程

**示例**：

- INP (IM Notification Protocol)：定义通知如何流转（UNP 通知对象 → 渲染规则 → 企业微信格式 → 投递）
- 需求评审协议（未来）：定义需求从创建 → 初审 → 技术审 → 批准的步骤

---

### 2.3 Skill（技能）

**定义**：定义能力目标、执行流程、输入输出、处理规范。

**特征**：

- 目标驱动：执行某个明确的目标（如"代码审查"、"生成 README"）
- 有清晰的输入（用户意图）和输出（制品或报告）
- 可能调用或遵循多个 Protocol 和 Rule
- 是 Agent 可以选择并执行的主动能力

**何时使用**：

- 定义 Agent 可执行的一个具体任务
- 定义某个工作流程的完整执行步骤
- 定义输出物的生成规范

**示例**：

- `review-code`：目标是代码审查；遵循特定的 Rule（编码规范）；可能应用多个 Spec（如需求）
- `capture-work-items`：目标是创建符合 Requirement Modeling Protocol 的需求条目
- `generate-readme`：目标是生成符合制品契约的 README

---

### 2.4 Rule（规则）

**定义**：最小可执行约束——行为准则、风格约束、质量要求。

**特征**：

- 独立可验证：可单独检查某个行为是否符合
- 被动约束：不描述能做什么，而是不能怎么做 / 必须怎么做
- 可被多个 Protocol 和 Skill 引用
- 通常是"黑名单"或"检查清单"的形式

**何时使用**：

- 定义编码风格（如缩进、命名）
- 定义文档写作规范（如标题大小写、术语一致）
- 定义行为约束（如 Git 提交规范、PR 审查检查点）

**示例**：

- `writing-chinese-technical`：中文技术文档的写作规范
- `standards-coding`：代码编写标准（如变量命名、注释规范）
- `standards-shell`：Shell 脚本编写规范

---

## 3. 边界澄清

### ❌ 常见混淆 1：Spec vs Protocol

**错误**：把 Protocol 当 Spec，或反过来。

| 特征 | Spec | Protocol |
|------|------|----------|
| 关键词 | "是什么"、结构、字段 | "怎么做"、流程、步骤 |
| 重点 | 数据样子 | 交互过程 |
| 时间维度 | 静态的、描述状态 | 动态的、描述变化 |

**✅ 正确做法**：

- UNP 定义"通知对象长什么样" → **Spec**
- INP 定义"通知对象如何流向企业微信" → **Protocol**（使用 UNP 的字段）

**❌ 错误做法**：

- ~~把 UNP 叫"通知协议"（其实是"通知规范"）~~
- ~~把 INP 的投递过程叫"通知规范"~~

---

### ❌ 常见混淆 2：Skill vs Protocol

**错误**：技能和协议不加区分。

| 维度 | Skill | Protocol |
|------|-------|----------|
| 谁来执行 | Agent（主动执行） | Skill/Agent（被调用时遵循） |
| 目标 | 用户意图驱动（如"代码审查"） | 接口和流程约束（如"怎么投递通知"） |
| 结果 | 输出物/报告 | 流程完成或验证通过 |

**✅ 正确做法**：

- `review-code` 是 Skill（目标是审查代码）
- 代码审查应遵循的 Rule（如检查列表）被 Skill 引用

**❌ 错误做法**：

- ~~把 Skill 叫"协议"~~
- ~~把 Protocol 当成能执行的任务~~

---

### ❌ 常见混淆 3：Rule vs Spec

**错误**：规则和规范混淆。

| 维度 | Rule | Spec |
|------|------|------|
| 形态 | 约束、检查点、黑名单 | 定义、字段列表、白名单 |
| 方向 | "不能"、"必须" | "应有"、"包含" |

**✅ 正确做法**：

- Spec 定义："需求必须有 7 个字段"
- Rule 定义："验收标准不能包含模糊词"

---

## 4. 使用规范

### 4.1 文档中的术语使用

所有文档中必须遵循以下规则：

1. **首次出现时，用中英文并列**

   ```markdown
   规范（Spec）定义数据结构...
   协议（Protocol）定义交互流程...
   ```

2. **后续可简化为中文或英文，但保持一致**

   ```markdown
   本协议（Protocol）定义...
   遵循该规范（Spec）的...
   ```

3. **在表格和代码注释中，使用英文术语**

   ```markdown
   | Type | Spec | Protocol | Skill | Rule |
   ```

4. **不得混淆或替代**

   ```markdown
   ❌ "通知协议规范" — 歧义，不知道是 Spec 还是 Protocol
   ✅ "通知规范（UNP）" 或 "通知投递协议（INP）"
   ```

### 4.2 文件位置与术语对应

| 术语 | 应放在 | 例外 |
|------|--------|------|
| Spec | `specs/`、`protocols/` | 若作为 Protocol 的一部分，可在 Protocol 文件内定义 |
| Protocol | `protocols/` | 无 |
| Skill | `skills/` | 无 |
| Rule | `rules/` | 无 |

---

## 5. 验证清单

发布新的 Spec/Protocol/Skill/Rule 前，检查：

- [ ] 术语分类准确（不混淆 Spec vs Protocol，Rule vs Spec）
- [ ] 文件位置正确（Spec 在 specs/ 或 protocols/，Protocol 在 protocols/ 等）
- [ ] 首次出现术语时用中英文并列
- [ ] 定义中没有循环引用或歧义
- [ ] 与其他资产的边界清晰（scope boundaries）
- [ ] 若引用其他术语，确保一致性

---

## 6. 相关文档

- [specs/protocol.md](./protocol.md) — Protocol 的详细规范
- [specs/skill.md](./skill.md) — Skill 的详细规范
- [rules/INDEX.md](../rules/INDEX.md) — Rule 的注册表
- [protocols/INDEX.md](../protocols/INDEX.md) — Protocol 的注册表

---

**版本历史**：

- v1.0.0 (2026-03-25)：初稿 — 定义四个核心术语、边界澄清、使用规范
