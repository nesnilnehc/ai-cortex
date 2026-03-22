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

### 2.2 技能关系（Handoff 与 Scope Boundaries）

技能依赖与建议的后续步骤在 prose 中说明，而非元数据：

- **Handoff Point**（位于 Core Objective 或 Scope Boundaries 下）：何时及如何切换到其他技能。必须指名具体技能（如 `breakdown-tasks`、`review-code`）。
- **Scope Boundaries**：本技能不负责的内容，并列出由其他技能负责的职责及技能名（如「需求 elicitation 使用 `analyze-requirements`」）。
- **Intent routing**：`skills/intent-routing.json` 为意图→技能映射的规范来源（primary、optional）。

不存在 `related_skills` 元数据。作者在技能正文中记录流程与依赖，供 Agent 与工具作为单一事实来源。

### 可选调用字段

- **triggers**（可选）：英文短语数组（如 `["review", "code review"]`），3–5 个，供精确匹配。不替代 description/tags 的语义匹配。
- **description_zh**（可选）：中文一句话摘要，当项目存在 `docs/LANGUAGE_SCHEME.md` 时供 INDEX 的 Purpose 列使用。

## 3. 必选标题结构

- `# Skill: [英文标题]` 或 `# 技能： [中文标题]`（项目级语言 override 下可用中文）
- `## Purpose` / `## 目的`
- `## Core Objective` / `## 核心目标`（必选）
- `## Scope Boundaries` / `## 范围边界`（可选 — 也可作为 Core Objective 的子节；见 §3.1）
- `## Use Cases` / `## 使用场景`
- `## Behavior` / `## 行为`
- `## Input & Output` / `## 输入与输出`
- `## Restrictions` / `## 限制`
- `## Self-Check` / `## 自检`
- `## Examples` / `## 示例`

### 3.1 核心目标节（必选）

每个技能必须定义其核心目标，以防范范围蔓延、技能重叠及「brain split」（AI 困惑于选用哪项技能）。

**必选子节**：

1. **Primary Goal / 首要目标**：一句话说明技能产出或达成的结果。
2. **Success Criteria / 成功标准**：可测量、可验证的条件（3–6 条），完成技能时须全部满足。
3. **Acceptance Test / 验收测试**：用于验证技能达成目标的简单问题或测试。

**可选子节**（也可作为 Core Objective 后的独立 `## Scope Boundaries` 节）：

1. **Scope Boundaries / 范围边界**：本技能负责 vs 不负责的内容。
2. **Handoff Point / 交接点**：何时及如何切换至其他技能或工作流。

两种放置均有效：作为 `## Core Objective` 的子节（内联）或独立 `## Scope Boundaries` 节。按技能复杂度选择合适形式。

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

## 4. 内容质量

- **语言与调用**：YAML `description`、`triggers` 须为英文（生态约束）；`name`、`tags` 保持英文/kebab-case。项目存在 `docs/LANGUAGE_SCHEME.md` 时，正文/标题/示例可用中文；`description_zh` 供 INDEX（见 §2）。triggers 供精确匹配；语义匹配（description/tags）支持任意语言；intent-routing 的 `short_triggers_zh` 在项目有 LANGUAGE_SCHEME 时优先匹配中文调用。
- **语气**：祈使、技术化表述。避免填充语或口语化。
- **示例**：至少 2 个，其中 1 个须为边界或复杂场景。
- **交互**：对非平凡逻辑，定义何时向用户确认。
- **Divergent + Convergent**（仅探索/决策类）：见 §8.5。
- **文档制品原则**（适用于产出 document-artifact 的技能）：产出 mission、vision、design、readme 等文档时，应用 YAGNI（避免不必要段落或可选内容）、DRY（引用已有内容而非重复）、简洁（战略陈述 1–3 句，清晰可读）。

### 4.1 自检要求

Self-Check 节必须包含：

1. **Core Success Criteria**：直接复制 Core Objective 的 Success Criteria 为 checklist（- [ ] 格式）。
2. **Process Quality Checks**（可选但推荐）：过程质量检查。
3. **Acceptance Test**：复制 Core Objective 的 Acceptance Test 便于引用。
4. **阶段级检查**（Divergent/Convergent 技能）：见 §8.5。

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

Restrictions 节必须包含以下内容。**Skill Boundaries**（don't）为必选以避免重叠；**When to Stop**（handoff）为可选但推荐用于可组合技能。

1. **Hard Boundaries**：技能绝不可违反的绝对约束。
2. **Skill Boundaries（必选）**：本技能不做之事及由哪些技能负责（如「… → Use `skill-name`」）。即 don't / out-of-scope 清单。
3. **When to Stop（可选，链式推荐）**：何时停止并交接（如「User says 'approved' → hand off to X」）。
4. **Divergent vs. Convergent 范围**（适用时）：见 §8.5。

**示例**：

```markdown
## Restrictions

### Hard Boundaries

- **No premature implementation**: Do NOT write code until design is approved.
- **One question at a time**: Do not overwhelm user with multiple questions.
- **YAGNI ruthlessly**: Remove unnecessary features from all designs.

### Skill Boundaries (Avoid Overlap)

**Do NOT do these (other skills handle them)**:

- **Implementation planning**: Creating detailed task lists → Use `breakdown-tasks`
- **Code writing**: Writing actual code → Use implementation skills
- **Code review**: Reviewing existing code → Use `review-code`
- **Debugging**: Investigating bugs → Use `automate-repair`

**When to stop and hand off**:

- User says "approved" → Design complete, hand off to implementation
- User asks "how do we implement?" → Hand off to `breakdown-tasks`
- User asks "can you write code?" → Hand off to development workflow
```

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
- 新增、移除或重大变更技能后，若技能应出现在基于意图的发现中，更新 `skills/intent-routing.json`。
- **检查清单**：确认已更新 `manifest.json` 及（如需要）`skills/intent-routing.json`；运行 `node scripts/verify-registry.mjs` 重生成 INDEX/skillgraph/intent-routing 并校验（见 §7.2）。
- **发布**：`npx skills add owner/repo --skill <name>` 从远端克隆；推送含新增技能及 manifest 的提交，使技能可发现、可安装。
- 版本须遵循 [SemVer](https://semver.org/)。

**仓库级文档**（`skills/` 目录，勿手动编辑）：

- **`skills/INDEX.md`**：由 `generate-skills-index.mjs` 自动生成；人工可读目录。
- **`skills/skillgraph.md`**：由 `generate-skillgraph.mjs` 自动生成；技能组合说明。
- **`skills/intent-routing.json`**：意图→技能映射的规范来源；编辑此文件变更映射。
- **`skills/intent-routing.md`**：由 `generate-intent-routing.mjs` 从 JSON 自动生成。
- **`skills/ASQM_AUDIT.md`**：由 `curate-skills` 产出；含 ASQM 分与生命周期。

## 6. agentskills 兼容性

- 本规范与 [agentskills.io](https://agentskills.io) 及 skills.sh 对齐。`license` 与 `metadata.author` 用于目录与信任；`metadata.author` 为 `ai-cortex`。
- 只要不与上游要求冲突，本规范可比 agentskills.io 更严格。
- **可选目录**（agentskills.io）：`scripts/`、`references/`、`assets/`。使用相对路径，保持层级浅。
- **Progressive disclosure**：主 `SKILL.md` 保持在 ≤500 行；将细节移至 `references/` 并按需加载。

## 7. 扩展与贡献

- 新技能须满足本规范；设计审查使用 `skills/refine-skill-design`。
- 版本注册：更新 SKILL frontmatter 并以线性版本号重新生成 `skills/INDEX.md`。
- 安装说明见 [README.md](../README.md)。

### 7.1 质量保证流程

**新技能**：创建草稿 → 自检（Self-Check）→ Refine → Curate → 注册（manifest、intent-routing）→ 验证（verify-registry）。

**既有技能（迁移）**：新增 Core Objective、更新 Self-Check、新增 Skill Boundaries → Refine → Curate → 验证。

共同步骤：Refine（`refine-skill-design`）、Curate（`curate-skills`）、验证（`verify-registry.mjs`）。

**质量门**：

- ❌ **REJECT**：缺少 Core Objective 节
- ❌ **REJECT**：Success Criteria 少于 3 条或多于 6 条
- ❌ **REJECT**：Self-Check 与 Success Criteria 不一致
- ❌ **REJECT**：Restrictions 节缺少 **Skill Boundaries**（don't — 本技能不做之事及由哪些技能负责）
- ⚠️ **WARN**：Restrictions 节缺少 **When to Stop**（handoff 条件；推荐用于可组合技能）
- ⚠️ **WARN**：ASQM 分 < 0.7（质量关注）

### 7.2 自动化质量检查

- **必选**：`node scripts/verify-registry.mjs`（重生成 INDEX、skillgraph、intent-routing 并校验）
- **推荐**：`curate-skills` 产出 ASQM 分与重叠检测；`refine-skill-design` 审计新技能

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
  # For document-artifact: optionally add artifact_type, path_pattern, lifecycle per spec/artifact-contract.md
  # For two-phase skills, clarify whether this is the Divergent (transient) or Convergent (persistent) output, or both
```

### 8.2 标准制品类型

| Artifact type | 结构 | 使用技能 |
| :--- | :--- | :--- |
| `findings-list` | {Location, Category, Severity, Title, Description, Suggestion} 数组 | 所有 review 技能 |
| `document-artifact` | 写入指定路径的 Markdown 文件 | generate-standard-readme、generate-agent-entry、define-mission、define-vision、define-roadmap、design-solution。路径与命名见 [spec/artifact-contract.md](artifact-contract.md)。 |
| `diagnostic-report` | 含 (Goal, Findings, Recommendations) 等节的结构化摘要 | review-codebase、run-checkpoint |
| `code-scope` | 调用方提供的文件、目录或 git diff | review-diff、review-codebase |
| `free-form` | 非结构化文本或用户输入 | design-solution、discover-skills 及探索类技能 |

### 8.3 文档制品路径契约

产出 `document-artifact` 的技能（如 capture-work-items、design-solution、assess-docs、bootstrap-docs）应将输出路径与命名与 [spec/artifact-contract.md](artifact-contract.md) 对齐。适用时在 output_schema 中声明 `artifact_type`、`path_pattern`、`lifecycle`。

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
