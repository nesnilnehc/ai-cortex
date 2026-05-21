---
artifact_type: terminology
created_by: ai-cortex
lifecycle: living
created_at: 2026-03-25
status: active
---

# AI Cortex 核心术语

> 四层治理资产 Spec / Protocol / Skill / Rule 的权威定义、独立点与交叉判别。所有项目文档以此为单一真理来源。

---

## 一、四个概念

### Spec（规范）

> 定义事物本身——其结构与行为契约。

- **业界对位**：HTTP RFC、OpenAPI Specification、JSON Schema、IEEE 830
- **核心问题**：这个东西**是什么样的**？
- **典型内容**：字段定义、类型契约、校验规则、行为约束（如 "GET 必须幂等"）
- **特征**：静态描述、面向所有读者、不限于某次交互

### Protocol（协议）

> 定义多个实体之间如何交互——步骤、状态、消息序列。

- **业界对位**：TCP、OAuth 2.0 Authorization Code Flow、TLS Handshake、SMTP
- **核心问题**：这两个或更多角色**怎么配合**？
- **典型内容**：消息序列、状态机、错误处理、超时与重试
- **特征**：动态、必涉及 ≥ 2 个角色、有明确起点与终点

### Skill（技能）

> 定义单一 Agent 可调用的能力——目标 + 执行 + 示例。

- **业界对位**：Anthropic Skills（agentskills.io）、LangChain Tool、OpenAI Function
- **核心问题**：Agent **能完成什么任务**？
- **典型内容**：目标声明、执行流程、输入输出、示例、可选工具
- **特征**：单方执行（Agent 一方完成全程）、目标驱动、产出物明确

### Rule（规则）

> 定义不可逾越的约束——每条独立可验证。

- **业界对位**：ESLint Rule、Google Style Guide、GDPR、Pre-commit hook
- **核心问题**：这里具体**不能做什么 / 必须做什么**？
- **典型内容**：禁令或必为；可机器或人工逐条核验
- **特征**：可校验、不带流程；一份 rule 文档可承载共享 scope 下的多条约束（如 shell 风格指南），每条独立可验证即可，不要求文档本身原子化

---

## 二、独立点（各自专属领地）

| 概念 | 独占语义 |
|----|----|
| Spec | "事物的契约描述"——别处不该重复定义结构 |
| Protocol | "多方协调的字节级 / 消息级序列"——别处不该规定交互步骤 |
| Skill | "Agent 可路由的目标导向能力"——别处不该声明可被 description / tags 匹配的可调用能力 |
| Rule | "原子可校验约束"——别处不该说 "禁止 X" 或 "必须 Y" 而不附验证手段 |

---

## 三、交叉判别（4 组易混淆问题）

### 1. Spec vs Protocol

- 共同点：都可能含 "MUST / MUST NOT" 字样
- **判别问题**：这是描述一个名词的契约，还是描述若干动词的序列？
- 名词契约 → Spec；动词序列 → Protocol
- **例**：UNP "通知对象的字段表" = Spec；INP "通知从发送方到 IM 渠道的渲染投递步骤" = Protocol

### 2. Skill vs Protocol

- 共同点：都涉及 "执行 / 流程"
- **判别问题**：完成这件事是单方执行，还是多方配合？
- 单方 → Skill；多方 → Protocol
- **例**：`review-typescript`（Agent 单方扫码出 findings）= Skill；INP（发送方 + IM 渠道）= Protocol

### 3. Spec vs Rule

- 共同点：都可能含约束语句
- **判别问题**：它定义事物长什么样，还是约束行为边界？
- 结构定义 → Spec；行为约束 → Rule（可单条，也可同 scope 多条合订）
- **例**：UNP "通知对象有 7 字段" = Spec；`standards-shell` 列 8 条 Shell 风格约束 = Rule（多条共享同一 scope）

### 4. Skill vs Rule

- 共同点：都规定行为
- **判别问题**：这是端到端任务，还是单点检查？
- 任务 → Skill；检查 → Rule
- **例**：`commit-work`（写消息、暂存、验证、提交全流程）= Skill；"提交消息必须 ≤ 72 字符" 单条 = Rule

---

## 四、内嵌允许 vs 不允许

### 允许的内嵌（无需强行拆分）

- **Spec 内嵌 Rule**：Spec 在描述字段时附带校验规则（如 "priority ∈ [P0, P1] 时 actions 必填"）——这是 Spec 的内禀部分
- **Protocol 内嵌 Spec**：Protocol 在描述消息序列时引用消息 Spec（INP 引用 UNP）——通过 `related` 字段
- **Skill 引用 Spec / Protocol / Rule**：Skill 说明产出物时引用相关 Spec、执行步骤时遵守相关 Rule——通过链接

### 不允许的内嵌

- **Skill 内嵌 Protocol**：多方流程应外置为 Protocol，不应埋在某个 Skill 内
- **Rule 内嵌流程**：流程应外置为 Skill；Rule 必须保持原子可校验

---

## 五、文件位置与术语对应

| 术语 | 默认目录 | 备注 |
|----|----|----|
| Spec | `specs/` | 内嵌于 Protocol 中的小型 Spec 可留在 `protocols/` |
| Protocol | `protocols/` | — |
| Skill | `skills/` | — |
| Rule | `rules/` | — |

---

## 六、术语使用约定（文档中）

1. **首次出现时中英并列**：`规范（Spec）`、`协议（Protocol）`
2. **后续可简化为单语**，但保持一致
3. **机器消费字段（YAML / 命令 / ID）保持英文**
4. **不得混淆或替代**：避免 "通知协议规范" 之类歧义；用 "通知规范（UNP）" 或 "通知投递协议（INP）"

---

## 七、相关文档

- [protocols/INDEX.md](../../protocols/INDEX.md) — Protocol 注册表
- [rules/INDEX.md](../../rules/INDEX.md) — Rule 注册表
- [skills/INDEX.md](../../skills/INDEX.md) — Skill 清单

技能本身遵循 [agentskills.io](https://agentskills.io) 的标准格式。
