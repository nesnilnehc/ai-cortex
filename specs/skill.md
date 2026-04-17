# 技能规范 (Skill Specification)

状态：必选  
版本：2.7.5  
范围：`skills/` 下所有文件。

**变更日志**：

- v2.7.5 (2026-03-22)：§4 新增文档制品原则 — YAGNI、DRY、简洁适用于产出 document-artifact 的技能
- v2.7.4 (2026-03-22)：内容与结构精简 — 变更日志归档；§1 命名收敛；§3.1 重要性缩句；§4 去重、§4.4 合并；§5 与 §9 合并；§7.1 流程合并
- v2.7.3 (2026-03-22)：YAGNI/DRY 优化 — 精简演进元数据、§8.5 D/C 模式；合并重复定义；修正示例技能名与路径
- v2.7.2 (2026-03-21)：移除 `related_skills` 元数据；技能关系改由 prose 中的 Handoff Point 与 Scope Boundaries 说明
- v2.7.0 (2026-03-16)：新增 Divergent（探索）与 Convergent（决策/制品）两阶段模型
- v2.6.0 (2026-03-16)：§4.2 Skill Boundaries 必选；When to Stop 可选推荐

---

## 1. 文件结构与命名

- **目录**：必须使用 `kebab-case` 并与 YAML `name` 字段一致。
- **文件名**：必须为 `SKILL.md`。
- **命名**：使用 `verb-noun`（如 `decontextualize-text`）。避免模糊或泛化术语。
  - **首选**：`verb-noun`（如 `generate-readme`、`discover-skills`、`capture-work-items`），或 review/action 族使用 `verb-target`（如 `review-code`、`review-python`）。
- **避免**：纯名词复合（如 `documentation-readiness` → 改用 `assess-docs`）；无明确动词的抽象复合名。
- **命名优先级**：语义正确与规范性优先，不得为口语化牺牲语义；在上述约束下优先自然、易记的名称。
- **术语一致性**：跨技能同一语义概念使用同一术语（如文档相关用 `doc`：`assess-docs`、`bootstrap-docs`）。
- **探索/决策类技能命名**：见 §8.5。
- **name**（与 [agentskills.io](https://agentskills.io/specification) 对齐）：1–64 字符；仅小写字母、数字、连字符；不得以 `-` 开头或结尾；不得出现连续连字符 `--`；须与父目录名一致。
- **单文件自包含**（最佳实践）：技能通常为**一个 SKILL.md**；Agent 加载该文件获取完整定义。执行时不依赖技能目录下其他 MD 文件。若技能有固定输出格式或契约（如「AGENTS.md 须遵循给定结构」），**将契约内嵌于 SKILL.md**（如 `## Appendix: Output contract`）而非单独文件，以便一次注入即可。

## 2. 必选 YAML 元数据

每个 `SKILL.md` 必须以以下内容开头：

```yaml
---
name: [kebab-case-name]
description: [one-line summary in English; for discoverability and semantic search in agentskills / skills.sh]
tags: [at least one tag from INDEX]
version: [x.x.x]
license: MIT
recommended_scope: [optional] user | project | both  # default both
metadata:
  author: ai-cortex
  # evolution.sources: optional, for forked/derived skills; see agentskills.io
# Optional: triggers, description_zh (见下方「可选调用字段」)
---
```

### 2.1 演进元数据（可选）

当技能派生自、分叉自或整合其他技能时，使用 `metadata.evolution.sources` 记录：name、repo、version、license、type（fork | integration | reference）、borrowed。详见 [agentskills.io](https://agentskills.io/specification)。

### 2.2 Skill 在四层治理中的位置

> 详细术语定义请见 [specs/terminology.md](./terminology.md)。

**四层治理资产对比**：

| 资产 | 中文 | 定义内容 | 加载方式 | 生命周期 | 示例 |
|------|------|---------|---------|---------|------|
| **Spec** | 规范 | 数据结构、必需字段、接口契约（"是什么"） | 常驻或按需 | 版本化、breaking changes 管理 | [UNP](../specs/universal-notification.md)（通知结构）、[Requirement Modeling](../specs/requirement-modeling/SPEC.md)（需求字段） |
| **Protocol** | 协议 | 交互流程、各步骤约束、应用哪些 Rule（"怎么做"） | 常驻或按需 | 版本化、breaking changes 管理 | [INP](../protocols/im-notification-delivery.md)（通知投递流程）、（评审协议 - 待定） |
| **Skill** | 技能 | 能力目标、执行流程、输入输出 | 按需注入（任务触发时） | 版本化、依赖管理 | **`review-code`、`capture-work-items`** |
| **Rule** | 规则 | 行为约束、工作流规范、质量标准 | 常驻加载（长期背景） | 版本化、优先级管理 | `writing-chinese-technical`、`standards-coding` |

**Skill 处于中间执行层**，既要满足 Spec 和 Protocol 的约束，又要遵守 Rule 规范边界。详见 [specs/protocol.md](./protocol.md) §5 和 [specs/terminology.md](./terminology.md)。

### 2.3 技能关系（Handoff 与 Scope Boundaries）

技能依赖与建议的后续步骤在 prose 中说明，而非元数据：

- **Handoff Point**（位于 Core Objective 或 Scope Boundaries 下）：何时及如何切换到其他技能。必须指名具体技能（如 `breakdown-tasks`、`review-code`）。
- **Scope Boundaries**：本技能不负责的内容，并列出由其他技能负责的职责及技能名（如「需求 elicitation 使用 `analyze-requirements`」）。

不存在 `related_skills` 元数据。作者在技能正文中记录流程与依赖，供 Agent 与工具作为单一事实来源。

### 2.4 Protocol 与 Skill 概念映射

为了帮助理解两个 spec 的关系，以下表格列出了两者在各方面的对应：

| 核心概念 | Protocol 叫法 | Skill 叫法 | 说明 |
|---------|-------------|---------|------|
| **定位** | Semantic Role | Semantic Role | 在系统中的语义角色（WHAT vs HOW） |
| **目标/承诺** | Core Principles（5 条价值观） | Core Objective（目标 + 成功标准） | 协议承诺什么 / 技能目标什么 |
| **验证标准** | Hard Rules（MUST/MUST NOT） | Success Criteria（≥3 条） | 怎样算符合要求 |
| **边界澄清** | Scope Boundaries | Scope Boundaries | 包含什么 / 不包含什么 |
| **约束与禁止** | Hard Rules + Anti-Patterns | Restrictions（Hard Boundaries + Skill Boundaries）+ Anti-Patterns | 不能做什么 / 为什么不能 |
| **反例学习** | Anti-Patterns（✅ vs ❌） | Anti-Patterns（✅ vs ❌） | 正确做法 vs 错误做法与问题分析 |
| **具体定义** | Required Schema + Examples | Behavior + Input & Output + Examples | 如何定义 / 如何执行 |
| **应用示例** | Examples（≥2 个） | Examples（≥2 个） | 完整的可工作示例 |
| **自动纠正** | AI Refactor Instruction | AI Refactor Instruction | 出错时的诊断和修复步骤 |
| **验收检查** | Self-Check 清单 | Self-Check 清单 | 发布前的质量门检查 |

**如何使用此表**：
- 学习了 Protocol 中的某个概念后，可查表找到对应的 Skill 概念
- 理解映射关系可加快跨 spec 学习
- Agent 可用此表进行语义匹配和导航

### 可选调用字段

- **triggers**（可选）：英文短语数组（如 `["review", "code review"]`），3–5 个，供精确匹配。不替代 description/tags 的语义匹配。
- **description_zh**（可选）：中文一句话摘要，当项目存在 `docs/LANGUAGE_SCHEME.md` 时供 INDEX 的 Purpose 列使用。
- **allowed_tools**（可选）：字符串数组，列出该技能允许使用的工具名（如 `Read`、`Write`、`Grep`、`Bash`）。供支持工具白名单的主机（如 Claude）使用，减少越权调用。若不指定，则不施加工具限制。主机不支持时忽略该字段。与 agentskills.io、gstack 的 `allowed-tools` 对齐。

**示例**：

```yaml
allowed_tools: [Read, Grep, Write]
```

## 🔍 快速导航（新用户必看）

| 我想... | 查看 | 说明 |
|--------|------|------|
| **了解这个技能的用途** | § Purpose（目的） | 解决什么问题 |
| **确认技能是否适合我** | § Semantic Role & Scope（定位和范围） | WHAT vs HOW、包含/不包含 |
| **看具体的使用示例** | § Examples（示例） | ≥2 个完整示例 |
| **了解成功的标准** | § Core Objective（核心目标） | Success Criteria + Acceptance Test |
| **检查我的使用方式** | § Anti-Patterns（反模式） | ✅ 正确 vs ❌ 错误做法 |
| **了解有什么限制** | § Restrictions（限制） | Hard Boundaries + Skill Boundaries |
| **我遇到了错误** | § AI Refactor Instruction（纠正指令） | 如何自动诊断和修复 |
| **完整的执行流程** | § Behavior（行为） + Input & Output | 默认值、选项、接口 |
| **最后的自检清单** | § Self-Check（自检） | 质量门检查 |

> **Protocol vs Skill 的区别**：
> Protocol 定义"什么"（数据结构、规则）；Skill 定义"怎么做"（目标、流程、决策）。详见 §2.2 三层治理对比。

---

## 3. 必选标题结构（10 个必选）

每个 Skill 必须包含以下标题结构，顺序与名称不可变（Appendix 可选除外）：

**技能主标题**：
- `# Skill: [英文标题]` 或 `# 技能： [中文标题]`（项目级语言 override 下可用中文）

**Semantic Role 定位块（必选，标题前）**：
- blockquote 说明此技能在系统中的语义定位（WHAT vs HOW、与相似技能的区别）

**11 个必选节**（顺序固定）：
1. `## Purpose` / `## 目的`
2. `## Core Objective` / `## 核心目标`（含 Primary Goal、Success Criteria、Acceptance Test）
3. `## Scope Boundaries` / `## 范围边界`（必选，不可省或内联到 Core Objective）
4. `## Use Cases` / `## 使用场景`
5. `## Behavior` / `## 行为`
6. `## Input & Output` / `## 输入与输出`
7. `## Restrictions` / `## 限制`
8. `## Anti-Patterns` / `## 反模式`（新增必选）
9. `## Examples` / `## 示例`（提前至第 9 位，与 protocol.md 顺序对齐）
10. `## AI Refactor Instruction` / `## AI 重构指令`（新增必选）
11. `## Self-Check` / `## 自检`（移至最后，作为最终验收）

**可选附录**：
- `## Appendix: [内容]`（可选）

**节点顺序设计理由**（与 Protocol 对齐）：
- **第 1-3 位**（认识阶段）：Purpose + Core Objective + Scope Boundaries — 帮助用户快速判断"这个技能是否适用"
- **第 4-7 位**（应用阶段）：Use Cases + Behavior + Input & Output + Restrictions — 定义"怎么执行、接口、限制"
- **第 8-11 位**（验证阶段）：Anti-Patterns + Examples + AI Refactor Instruction + Self-Check — 学习正确做法、看示例、遇错自纠正、最后验收

### 3.0 Semantic Role 定位块（必选，标题前）

在技能主标题后、`## Purpose` 前，使用 blockquote 说明本技能在系统中的语义定位。

**目的**：明确此技能的角色（WHAT vs HOW）、与相似技能的区别，防范「brain split」。

**格式**：
```markdown
# Skill: analyze-requirements

> **角色**：需求分析与转化
> **WHAT**：将模糊需求转化为结构化、可测试的需求文档
> **HOW**：不负责实现；关联技能 `capture-work-items` 用于创建条目
> **区别**：不同于 `clarify-requirements`（后者仅澄清歧义，本技能进行深度转化）

## 1. Purpose / 目的
...
```

### 3.1 核心目标节（第 2 位，必选）

每个技能必须定义其核心目标，以防范范围蔓延、技能重叠及「brain split」（AI 困惑于选用哪项技能）。

**必选子节**：

1. **Primary Goal / 首要目标**：一句话说明技能产出或达成的结果。
2. **Success Criteria / 成功标准**：可测量、可验证的条件（3–6 条），完成技能时须全部满足。
3. **Acceptance Test / 验收测试**：用于验证技能达成目标的简单问题或测试。

**可选子节**（也可作为 Core Objective 后的独立 `## Scope Boundaries` 节）：

1. **Scope Boundaries / 范围边界**：本技能负责 vs 不负责的内容。
2. **Handoff Point / 交接点**：何时及如何切换至其他技能或工作流。

Scope Boundaries 作为 Core Objective 的必选子节（或后续独立节，但必须存在）。

**示例**：

```markdown
## Core Objective

**Primary Goal**: Produce a validated design document that serves as the single source of truth for implementation.

**Success Criteria** (ALL must be met):

1. ✅ **Design document exists**: Written to `docs/design-decisions/YYYY-MM-DD-<topic>.md` and committed
2. ✅ **User explicitly approved**: User said "approved", "looks good", "proceed", or equivalent confirmation
3. ✅ **Alternatives documented**: At least 2-3 approaches considered with trade-offs analysis
4. ✅ **YAGNI applied**: Design focuses on minimum viable solution, unnecessary features removed
5. ✅ **DRY applied**: Design references existing patterns/components rather than reinventing
6. ✅ **No code written**: Zero implementation code exists (design only)

**Acceptance Test**: Can a developer with zero project context implement this design without asking clarifying questions?

**Scope Boundaries**:
- This skill handles: Rough idea → Validated design document
- This skill does NOT handle: Implementation planning (use `breakdown-tasks`), Code writing (use implementation skills)

**Handoff Point**: When design is approved and documented, hand off to implementation planning or development workflow.
```

**重要性**：防止 brain split、范围蔓延，提供可验证的完成标准与清晰交接。

---

### 3.4 Anti-Patterns 节（第 8 位，必选）

对比正确与错误的做法。采用 ✅ 和 ❌ 标记。

**目的**：通过具体示例警示常见错误，比单纯的限制清单更有效。

**结构**：

```markdown
## Anti-Patterns / 反模式

### ✅ 正确做法

[示例代码或流程]

**为什么正确**：...

### ❌ 错误做法

[反面示例]

**问题分析**：
- 为什么错误
- 可能的后果
- 如何避免

### 示例 2：...（至少 2-3 个对比）
```

**示例**：

```markdown
## Anti-Patterns / 反模式

### ✅ 正确做法：逐步澄清

1. 用户提出需求："系统应该快速响应"
2. Agent 提问："快速"的具体含义？目标延迟是多少？
3. 用户回答："API 应在 100ms 内响应"
4. Agent 记录明确的验收标准

### ❌ 错误做法：直接转化

1. 用户提出需求："系统应该快速响应"
2. Agent 直接记录为需求："实现快速响应"

**问题分析**："快速"是模糊词；"实现"混淆了 WHAT 和 HOW；无法验证是否满足。
```

---

### 3.5 AI Refactor Instruction 节（第 10 位，必选）

给 AI Agent 的具体纠正指令，支持自动检测和修复不符合协议的调用。

**目的**：当技能被错误使用时，引导 Agent 自动纠正而非失败。

**结构**：

```markdown
## AI Refactor Instruction / AI 重构指令

当 Agent 遇到以下不符合协议的调用模式时，执行纠正步骤：

### 问题 1：[不符合现象]

- **识别标志**：[如何识别此问题]
- **纠正步骤**：
  1. ...
  2. ...
  3. 重新执行或回溯

---

### 问题 2：[另一个不符合现象]

- **识别标志**：...
- **纠正步骤**：...

### 示例

[具体的纠正案例，展示问题 → 识别 → 纠正过程]
```

**示例**：

```markdown
## AI Refactor Instruction / AI 重构指令

### 问题：Success Criteria 包含模糊词

- **识别标志**：Success Criteria 中出现 "good"、"fast"、"significant" 等词
- **纠正步骤**：
  1. 识别每个模糊词
  2. 用 Agent 询问用户的量化定义
  3. 将模糊词替换为可测试的标准（如 "< 100ms" 替代 "fast"）
  4. 重新提交 Success Criteria

### 示例

用户："我需要系统的响应速度要快"

Agent 检测：描述中有模糊词 "快"

Agent 纠正：
1. 询问："'快' 具体是多少毫秒？"
2. 用户回答："应该在 100ms 内"
3. 记录为：Success Criteria = "API 响应时间 < 100ms"
```

## 4. 内容质量

技能必须满足以下 5 维质量框架方可发布。每维都有明确的自检清单。

### 4.0 五维质量框架

| 维度 | 定义 | 自检关键问题 |
|------|------|-----------|
| **Completeness** | 所有必选节齐全 | 10 个必选节都存在吗？ |
| **Verifiability** | 所有要求都可被测试和评估 | Success Criteria 可量化吗？能否独立验证是否完成？ |
| **Clarity** | 表述清晰无歧义 | Semantic Role 明确定位吗？技能名称和目标是否清晰？ |
| **Executability** | Agent 能自主执行，不依赖过度猜测 | Behavior 定义默认值吗？交互策略清晰吗？ |
| **Traceability** | 版本、来源、依赖关系清晰 | 版本号符合 SemVer 吗？与其他技能的关系明确吗？ |

---

### 4.1 Completeness（完整性）

所有必选节齐全，无缺失。

**自检清单**：
- [ ] 11 个必选节都存在（Purpose/Semantic Role/Core Objective/…）
- [ ] Metadata 完整（name、version、description、tags、author）
- [ ] Core Objective 包含 Primary Goal、Success Criteria（3-6 条）、Acceptance Test
- [ ] Scope Boundaries 明确列举"包含"和"不包含"
- [ ] Anti-Patterns 至少 2-3 个对比示例
- [ ] Examples ≥ 2 个，其中 ≥ 1 个是边界或复杂场景
- [ ] AI Refactor Instruction 覆盖 ≥ 2 种常见错误模式

**验收标准**：Completeness Score = (已有节数 / 11) × 100%

---

### 4.2 Verifiability（可验证性）

所有要求都可被测试和评估。

**自检清单**：
- [ ] Success Criteria 可量化（避免 "良好"、"充分"、"重要"）
- [ ] Hard Boundaries 使用 MUST / MUST NOT，有验证方式
- [ ] Acceptance Test 是明确的验证问题（非模糊陈述）
- [ ] Anti-Patterns 的"错误做法"能被识别或自动检测
- [ ] AI Refactor Instruction 指导能否自动应用（或至少人工易于应用）

---

### 4.3 Clarity（清晰性）

表述清晰，无歧义。

**自检清单**：
- [ ] Semantic Role 明确定位（WHAT vs HOW、与其他技能的区别）
- [ ] 技能名称遵循 Verb-Noun 约定（如 `analyze-requirements`）
- [ ] Scope Boundaries 清晰列举"包含"和"不包含"
- [ ] 无歧义术语，或已明确定义
- [ ] 示例与反例形成清晰对比

---

### 4.4 Executability（可执行性）

Agent 能自主执行，不依赖过度的上下文猜测。

**自检清单**：
- [ ] Behavior 定义默认值（Defaults First 原则）
- [ ] 可选项用清单呈现（Prefer Choices 原则）
- [ ] 用户确认点明确标注（何时需要 Yes/No 决策）
- [ ] AI Refactor Instruction 指导 Agent 自纠正
- [ ] 交互策略遵循 Progressive Disclosure（逐步展开）
- [ ] 文档制品原则（YAGNI、DRY、简洁）被应用（若产出 document-artifact）

---

### 4.5 Traceability（可追踪性）

版本、来源、依赖关系清晰。

**自检清单**：
- [ ] 遵循 SemVer 版本号（如 v1.2.3）
- [ ] Handoff Point 明确指向后续技能
- [ ] Input/Output Schema 明确声明（若适用）
- [ ] 与其他技能的关系在 Scope Boundaries 中明确说明
- [ ] 技能演进（若派生自其他技能）在 metadata.evolution 中记录

---

### 4.6 语言与调用规范

- **语言与调用**：YAML `description`、`triggers` 须为英文（生态约束）；`name`、`tags` 保持英文/kebab-case。项目存在 `docs/LANGUAGE_SCHEME.md` 时，正文/标题/示例可用中文；`description_zh` 供 INDEX（见 §2）。triggers 供精确匹配；语义匹配（description/tags）支持任意语言。
- **语气**：祈使、技术化表述。避免填充语或口语化。
- **Divergent + Convergent**（仅探索/决策类）：见 §8.5。

---

### 原有自检要求（保留）

### 4.1 自检要求

Self-Check 节（作为最后一步）必须包含：

1. **必选节完整性检查**：所有 11 个必选节都存在吗？
2. **Core Success Criteria**：直接复制 Core Objective 的 Success Criteria 为 checklist（- [ ] 格式）。
3. **质量门检查**：按 §4.6 的质量门标准自检（REJECT/WARN/APPROVE）。
4. **Process Quality Checks**（可选但推荐）：过程质量检查。
5. **Acceptance Test**：复制 Core Objective 的 Acceptance Test 便于引用。
6. **阶段级检查**（Divergent/Convergent 技能）：见 §8.5。

**示例**（以 design-solution 为例；Success Criteria 与 Core Objective 一致）：

```markdown
## Self-Check

### Core Success Criteria (ALL must be met)

- [ ] Design document exists: Written to `docs/design-decisions/YYYY-MM-DD-<topic>.md` and committed
- [ ] User explicitly approved
- [ ] Alternatives documented (2-3 with trade-offs)
- [ ] YAGNI applied; DRY applied; No code written

### Acceptance Test

Can a developer with zero context implement without clarifying questions? If NO → return to clarification. If YES → handoff.
```

### 4.2 限制要求

Restrictions 节必须包含以下内容。**Hard Boundaries** 和 **Skill Boundaries** 均为必选；**When to Stop** 为可选但推荐用于可组合技能。

1. **Hard Boundaries**：技能绝不可违反的绝对约束（使用 MUST NOT / FORBIDDEN）。
2. **Skill Boundaries（必选）**：本技能不做之事及由哪些技能负责。即 don't / out-of-scope 清单。
3. **When to Stop（可选，链式推荐）**：何时停止并交接。
4. **Divergent vs. Convergent 范围**（适用时）：见 §8.5。

**标准化表达**（参考 Protocol Hard Rules 格式）：

```markdown
## Restrictions / 限制

### Hard Boundaries

**Rule 1**: Do NOT write code before design approval (MUST NOT)
- Verification：Code presence in work artifacts
- Consequence：REJECT (协议不符)

**Rule 2**: Each user interaction must ask at most one question (MUST)
- Verification：Count of `?` marks in single response ≤ 1
- Consequence：WARN (建议改进)

**Rule 3**: Remove unnecessary features ruthlessly (MUST)
- Verification：Design review confirms YAGNI applied
- Consequence：REJECT (设计不完整)

### Skill Boundaries (Avoid Overlap)

**Do NOT do these** (other skills handle them):

- **Implementation planning**: Creating detailed task lists → Use `breakdown-tasks`
- **Code writing**: Writing actual code → Use language-specific skills
- **Code review**: Reviewing existing code → Use `review-code`

**When to stop and hand off**:

- User says "approved" → Design complete, hand off to `breakdown-tasks`
- User asks "how do we implement?" → Hand off to `breakdown-tasks`
- User asks "can you write code?" → Hand off to development workflow
```

**关键点**：
- 每条 Hard Boundary 使用明确的强制词（MUST / MUST NOT / FORBIDDEN）
- 附带"验证方式"和"后果"（REJECT/WARN）
- Skill Boundaries 明确指出相关技能名称

### 4.3 交互策略

技能应通过以下原则最小化用户输入。**新技能**（本规范版本后注册）必须满足；**既有技能**应在后续版本中尽量对齐。

- **Defaults first**：存在合理默认值时，直接使用，不问用户。可推断参数不要求用户输入。
- **Prefer choices**：尽可能提供 `[A][B][C]` 选项而非自由文本。除非需探索，避免「please describe」。
- **Context inference**：从 git（status、diff、branch）、当前打开文件与工作目录推断。Agent 执行推断；仅当推断失败或含糊时再请用户确认。
- **Progressive disclosure**：先用默认值运行，用户需要更多控制时再提供后续选项。

每项技能的 `## Behavior` 必须说明：默认值、选项，以及哪些项需用户显式确认。

阶段分离技能（Divergent/Convergent）的执行过程描述见 §8.5。

---

## 5. 元数据同步与仓库文档

**同步流程**：

- 新增技能后，更新 `manifest.json` 与 SKILL frontmatter。
- 新增或移动技能后，在 `manifest.json` 的 `capabilities` 中更新路径。
- **检查清单**：确认已更新 `manifest.json`；运行 `npm run verify` 校验 INDEX 与 manifest 一致性（见 §7.1）。
- **发布**：`npx skills add owner/repo --skill <name>` 从远端克隆；推送含新增技能及 manifest 的提交，使技能可发现、可安装。
- 版本须遵循 [SemVer](https://semver.org/)。

**仓库级文档**（`skills/` 目录）：

- **`skills/INDEX.md`**：手动维护的人工可读目录；`npm run verify` 校验与 manifest 与 SKILL 文件的一致性。
- **`skills/ASQM_AUDIT.md`**：由 `curate-skills` 产出；含 ASQM 分与生命周期。

## 6. agentskills 兼容性

- 本规范与 [agentskills.io](https://agentskills.io) 及 skills.sh 对齐。`license` 与 `metadata.author` 用于目录与信任；`metadata.author` 为 `ai-cortex`。
- 只要不与上游要求冲突，本规范可比 agentskills.io 更严格。
- **可选目录**（agentskills.io）：`scripts/`、`references/`、`assets/`。使用相对路径，保持层级浅。
- **Progressive disclosure**：主 `SKILL.md` 保持在 ≤500 行；将细节移至 `references/` 并按需加载。

## 7. 扩展与贡献

- 新技能须满足本规范；设计审查使用 `skills/refine-skill-design`。
- 版本注册：更新 SKILL frontmatter 与 `skills/INDEX.md` 中的版本号。
- 安装说明见 [README.md](../README.md)。

### 7.1 质量保证流程

**新技能**：创建草稿 → 自检（Self-Check）→ Refine → Curate → 注册（manifest）→ 验证（verify-registry）。

**既有技能（迁移）**：新增 Core Objective、更新 Self-Check、新增 Skill Boundaries → Refine → Curate → 验证。

共同步骤：Refine（`refine-skill-design`）、Curate（`curate-skills`）、验证（`verify-registry.mjs`）。

**质量门标准**：

| 分数范围 | 状态 | 处理方式 |
|---------|------|---------|
| ≥ 0.9 | ✅ APPROVE | 可直接发布 |
| 0.7-0.9 | ⚠️ WARN | 建议改进后发布 |
| < 0.7 | ❌ REJECT | 必须修复，不可发布 |

**REJECT 条件**（任一满足则拒绝）：
- ❌ 缺少任何 10 个必选节（包括 Semantic Role、Anti-Patterns、AI Refactor Instruction）
- ❌ Core Objective 缺少 Acceptance Test
- ❌ Success Criteria 少于 3 条或多于 6 条
- ❌ Semantic Role 未定位（WHAT vs HOW、与他技能区别）
- ❌ Hard Boundaries 未使用标准强制词（MUST / MUST NOT）
- ❌ Anti-Patterns 无具体示例
- ❌ Examples 少于 2 个

**WARN 条件**（建议改进）：
- ⚠️ Scope Boundaries 表述不够清晰
- ⚠️ Restrictions 缺少 When to Stop 条件
- ⚠️ AI Refactor Instruction 覆盖 < 2 个错误模式
- ⚠️ Examples 只有 1 个边界/复杂场景（需要 ≥ 1）

### 7.2 质量检查（规范约束）

本规范本身独立，不强依赖具体工具。工程团队可选择以下方式来验证质量门：

**验证方式**（可选一种或多种）：
- **人工审查**：通过 Self-Check 清单逐一检查（§4.6 质量门标准）
- **自动化脚本**：可选使用 `verify-registry.mjs` 进行形式检查（非强制）
- **CI 流程**：在 PR 检查中集成质量门验证
- **代码审查工具**：使用 `refine-skill-design` 或 `curate-skills` 进行深度审计

**关键**：确保通过上述质量门（§4.6），具体工具选择由项目自决。

## 8. I/O 契约（可选）

技能可声明结构化输入与输出契约，以支持编排、链式调用与自动化 schema 匹配。

### 8.1 YAML 字段

在 YAML front-matter 中添加以下可选字段：

```yaml
input_schema:
  type: [artifact type]   # findings-list | document-artifact | diagnostic-report | code-scope | free-form
  description: [what this skill consumes]
  defaults:               # optional; for "zero-arg launch" and orchestration
    [param]: [value]      # e.g. scope: diff, untracked: include
output_schema:
  type: [artifact type]
  description: [what this skill produces]
  # For document-artifact: optionally add artifact_type, path_pattern, lifecycle per specs/artifact-contract.md
  # For two-phase skills, clarify whether this is the Divergent (transient) or Convergent (persistent) output, or both
```

### 8.2 标准制品类型

| Artifact type | 结构 | 使用技能 |
| :--- | :--- | :--- |
| `findings-list` | {Location, Category, Severity, Title, Description, Suggestion} 数组 | 所有 review 技能 |
| `document-artifact` | 写入指定路径的 Markdown 文件 | generate-standard-readme、generate-agent-entry、define-mission、define-vision、define-roadmap、design-solution。路径与命名见 [specs/artifact-contract.md](artifact-contract.md)。 |
| `diagnostic-report` | 含 (Goal, Findings, Recommendations) 等节的结构化摘要 | review-codebase |
| `code-scope` | 调用方提供的文件、目录或 git diff | review-diff、review-codebase |
| `free-form` | 非结构化文本或用户输入 | design-solution、discover-skills 及探索类技能 |

### 8.3 文档制品路径契约

产出 `document-artifact` 的技能（如 capture-work-items、design-solution、assess-docs、bootstrap-docs）应将输出路径与命名与 [specs/artifact-contract.md](artifact-contract.md) 对齐。适用时在 output_schema 中声明 `artifact_type`、`path_pattern`、`lifecycle`。

### 8.4 编排器用法

编排器（元技能）使用 `input_schema` 与 `output_schema` 实现：

1. **自动匹配**：按制品类型连接上游技能输出与下游技能输入。
2. **验证**：执行前确保链式技能 schema 兼容。
3. **聚合**：将多个 findings-list 合并为单一报告。

向后兼容：无 I/O 契约的技能照常工作。契约缺失时编排器回退至手动传递上下文。

### 8.5 Divergent + Convergent 阶段模式（可选，探索/决策类技能）

| 阶段 | 目的 | 输出 | 范围约束 |
| :--- | :--- | :--- | :--- |
| **Divergent** | 生成多选项、想法、候选 | 非持久、探索性（transient） | 不得做最终决策或书写持久制品 |
| **Convergent** | 从候选中选择、评估、聚合 | 持久 `document-artifact` | 不得引入全新选项，聚焦 refinement |

**命名**：Divergent 优先 `brainstorm-`、`ideate-`、`explore-`；Convergent 优先 `define-`、`design-`、`plan-`。两阶段技能可保留单一名称，须在 Behavior 中标注阶段与触发方式。

**交接**：D 完成时汇总选项、询用户是否收敛 → 触发 C 或推荐 Convergent 技能；C 完成时确认制品路径、提及下游技能、说明再探索超出范围。
