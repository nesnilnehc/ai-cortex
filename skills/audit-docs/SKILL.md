---
name: audit-docs
description: Audit complete documentation governance (norms, structure, health) in one command with unified report and roadmap.
description_zh: 一条命令完成文档治理审计（规范、结构、健康度），生成统一报告和路线图。
tags: [documentation, governance, orchestration, workflow]
version: 1.1.2
license: MIT
recommended_scope: project
metadata:
  author: ai-cortex
triggers: [docs governance, documentation governance, governance check, doc audit]
input_schema:
  type: free-form
  description: Project path (default CWD), mode (full | quick | code-review), optional code-diff base branch
  defaults:
    mode: full
    code_diff: null
output_schema:
  type: document-artifact
  description: Unified governance report with compliance, health scores, and prioritized action plan
  artifact_type: audit-docs
  path_pattern: docs/calibration/audit-docs.md
  lifecycle: living
---

# 技能（Skill）：文档治理审计

## 目的 (Purpose)

在单条命令中自动化完整的文档治理工作流：建立规范 → 整理仓库结构 → 评估文档健康度。生成统一的治理报告，整合所有阶段的发现，包含集成评分和优先级行动计划。

## 核心目标 (Core Objective)

**首要目标**：建立和维护完整的**文档治理基础**，确保项目全生命周期中文档结构、命名和质量标准的一致性。

**成功标准**（必须满足所有要求）：

1. ✅ **规范已建立或验证**：`docs/ARTIFACT_NORMS.md` 存在且准确
2. ✅ **仓库结构已整理**：无显著错放文件、命名不一致或孤立制品
3. ✅ **文档已评估**：合规性、准备度、图健康度和代码对齐（若提供 code-diff）已评估
4. ✅ **统一报告已生成**：单一文档（`docs/calibration/audit-docs.md`）汇总所有阶段发现并排定优先级
5. ✅ **可操作的路线图已生成**：20-30 个具体的、排定优先级的改进项用户可执行

**验收测试**：新团队成员仅凭此报告能否理解项目的文档状态，并准确知道首先要改进的 10 项？

## 范围边界 (Scope Boundaries)

**本技能负责**：
- 发现和验证文档规范（通过 `discover-docs-norms`）
- 根据规范整理仓库结构（通过 `tidy-repo`）
- 评估文档健康度（通过 `assess-docs`）
- 将所有发现合成为统一治理报告
- 计算集成健康评分（0-100）
- 生成优先级行动计划

**本技能不负责**：
- 实际实现文档改进 → 分配给团队或使用下游技能
- 提交仓库变更 → 使用 `commit-work`
- 详细代码审查 → 使用 `review-code` 或 `review-codebase`
- 需求分析 → 使用 `analyze-requirements`

**交接点**：当报告完成且优先级路线图明确时，交接给团队执行或下游技能（如 `bootstrap-docs` 用于模板创建）。

## 使用场景 (Use Cases)

| 场景 | 模式 | 何时 | 输出焦点 |
| --- | --- | --- | --- |
| **新项目启动** | `full` | 项目开始 | 建立规范、初始评估 |
| **新团队成员** | `quick` | 贡献者加入 | 快速状态 & 需要阅读什么 |
| **PR 文档检查** | `code-review` | 合并前 | 验证代码变更有文档更新 |
| **发版前准备** | `full` | 版本号更新前 | 完整治理检查、阻塞检测 |
| **月度评审** | `quick` | 定期检查 | 健康趋势追踪 |

---

## 行为 (Behavior)

### 交互策略 (Interaction Policy)

遵循规范 §4.3（默认优先，选择优先，上下文推理）：

| 参数 | 默认值 | 推理 | 用户覆盖 |
| --- | --- | --- | --- |
| **project-path** | CWD | Git 根目录自动检测 | `--project <path>` |
| **mode** | `full` | 自动检测：若 `GITHUB_REF` 则 → `code-review`；否则 `full` | `--mode quick/full/code-review` |
| **code-diff** | 无 | 若 `code-review` 模式：`origin/main` | `--code-diff <branch>` |
| **apply-tidy** | false | （无） | `--apply-tidy yes/no` |
| **auto-confirm** | false | （无） | `--auto-confirm`（谨慎使用） |

### 执行流程 (Execution Flow)

**第 1 步：预飞行检查** (2 分钟)
- 验证 git 仓库（否则 ERROR）
- 检查 docs/ 存在（若缺失 WARN，继续）
- 验证规范存在（否则提示 discover-docs-norms）

**第 2 步：建立或验证规范**（如需，~1 分钟）
- 若规范缺失：调用 `discover-docs-norms`（置信度 > 90% 自动接受）
- 若规范存在：验证完整性

**第 3 步：整理仓库** (1-2 分钟，按模式条件执行)
- 仅 `full` 模式：运行 `tidy-repo --report-only`
- 询问用户：应用安全变更？[是][否][先审查]

**第 4 步：评估文档** (1-2 分钟)
- 运行 `assess-docs [--code-diff=<base>]`（基于模式）
- 收集：合规性、准备度、图健康度、代码对齐（如适用）

**第 5 步：生成统一报告** (~1 分钟)
- 合成步骤 2-4 的发现
- 计算 5 个健康评分（结构、准备度、对齐、图、集成）
- 写入 `docs/calibration/audit-docs.md`
- 输出：健康评分 + 前 10 项改进 + 下一步建议

**总预计时间**：5-10 分钟（取决于项目大小和模式）

---

## 输入与输出 (Input & Output)

### 输入 (Input)

```bash
audit-docs [--project <path>]
                [--mode full|quick|code-review]
                [--code-diff <base>|auto]
                [--apply-tidy yes|no]
                [--auto-confirm]
```

**参数**：

| 参数 | 默认值 | 类型 | 说明 |
| --- | --- | --- | --- |
| `--project` | CWD | path | Git 根目录自动检测；用于覆盖 |
| `--mode` | `full` | enum | 自动检测：GITHUB_REF 已设置？使用 `code-review`；否则 `full` |
| `--code-diff` | 无 | branch | 基准分支（例 `origin/main`）；`auto` 自动检测；`quick` 模式下忽略 |
| `--apply-tidy` | `no` | bool | 默认安全：仅报告；应用前询问用户 |
| `--auto-confirm` | `false` | flag | 跳过所有确认（用于 CI/自动化；谨慎使用） |

### 输出 (Output)

**总是生成**：
- `docs/calibration/audit-docs.md`：统一治理报告（artifact_type: audit-docs, lifecycle: living）

**按模式条件生成**：
- `docs/ARTIFACT_NORMS.md`：项目文档规范（若在第 2 步创建）
- `docs/calibration/repo-tidy.md`：仓库整理报告（来自 tidy-repo）
- `docs/calibration/doc-assessment.md`：完整评估报告（来自 assess-docs）

---

## 限制 (Restrictions)

### 硬边界 (Hard Boundaries)

- **未经确认无持久化变更**：应用整理或接受规范前总是询问
- **已提交文件无破坏性变更**：所有整理必须可逆转
- **文档化结构无删除**：存档而非删除

### 技能边界 (Skill Boundaries)（避免重叠）

**不要做这些**（其他技能处理）：

- **规范发现（若不存在）**：使用 `discover-docs-norms`
- **仓库整理（应用模式）**：使用 `tidy-repo`
- **详细合规检查**：使用 `assess-docs`
- **实现计划**：使用 `breakdown-tasks`
- **提交变更**：使用 `commit-work`
- **代码审查**：使用 `review-code`

### 何时停止并交接

| 条件 | 行动 | 交接目标 |
| --- | --- | --- |
| 用户在规范/结构后说"已批准" | 继续评估阶段 | （内部进行） |
| 用户在报告上说"继续"/"看起来不错" | 评估完成 | 团队实现或 `bootstrap-docs` 创建模板 |
| 代码审查检查显示严重缺口 | 建议 3-5 个具体改进 | 回到开发者（PR 未就绪） |
| 评分 > 80% | 切换到维护模式 | 每周运行 `audit-docs --quick` |
| 用户要求质量指标 / ASQM 评分 | 交接给 `curate-skills` | （工具提供评分） |
| 用户问"如何创建新技能？" | 交接给技能创建文档 | （文档） |

---

## 自检 (Self-Check)

### 核心成功标准（必须满足所有）

- [ ] **规范已建立或验证**：`docs/ARTIFACT_NORMS.md` 存在且准确
- [ ] **仓库结构已整理**：无显著错放文件、命名不一致或孤立制品
- [ ] **文档已评估**：合规性、准备度、图健康度和代码对齐（若提供 code-diff）已评估
- [ ] **统一报告已生成**：单一文档（`docs/calibration/audit-docs.md`）汇总所有发现并排定优先级
- [ ] **可操作的路线图已生成**：20-30 个具体的、排定优先级的改进项用户可执行

### 过程质量检查

- [ ] 所有用户输入在继续前已确认
- [ ] 每个阶段生成清晰、可操作的输出
- [ ] 无破坏性变更未明确批准而应用
- [ ] 报告可读且可操作（非仅数据转储）

### 验收测试

在成熟项目上运行 `audit-docs --mode quick`。团队成员能否理解：
1. 文档健康度是"好"/"可以"/"令人担忧"？
2. 5 项最高优先级改进是什么？
3. 本周应该做什么？

如有任何问题答"否" → 修订报告清晰度。

---

## 示例 (Examples)

### 示例 1：新项目完整评估

```bash
$ audit-docs --mode full

✓ Phase 1: Pre-flight checks passed
✓ Phase 2: Deriving norms from existing docs/
  Confidence: 92%
  Rules: kebab-case, YYYY-MM-DD dates, 5 artifact types

? Apply repository tidying? (will move misplaced files)
[Y] Yes  [N] No  [R] Review first
> Y

✓ Phase 3: Tidying complete
  - Moved 3 files to correct paths
  - Renamed 2 files for consistency
  - Archived 1 obsolete document

✓ Phase 4: Assessing documentation
  - Compliance: 92% (2 front-matter fields missing)
  - Readiness: 60% (3 layers weak)
  - Graph health: 78% (1 broken link)

✓ Phase 5: Report generated
  → docs/calibration/audit-docs.md

Integrated score: 77/100
Status: GOOD (focus on top 10 improvements)
Next: Review action plan in report
```

### 示例 2：PR 代码审查

```bash
$ audit-docs --mode code-review --code-diff origin/main

✓ Phase 1: Pre-flight checks passed
✓ Phase 2: Norms validated (existing)
✓ Phase 3: Structure check (no issues)
✓ Phase 4: Assessing with code diff

Code changes detected:
  - src/api/auth.py [Modified] → should update docs/architecture/api-design.md
  - src/db/migration.sql [Added] → should update docs/architecture/data-model.md

Docs status:
  - docs/architecture/api-design.md: ❌ NOT UPDATED
  - docs/architecture/data-model.md: ❌ NOT UPDATED
  - docs/CHANGELOG.md: ✓ UPDATED

✗ Code-docs alignment: 2 critical gaps

Recommendation:
  1. Update docs/architecture/api-design.md (15 min)
  2. Update docs/architecture/data-model.md (20 min)
  → Ready to merge after these updates
```

### 示例 3：维护检查

```bash
$ audit-docs --mode quick

✓ Quick assessment (no scanning)
  Structure score: 95/100
  Readiness score: 82/100
  Graph health: 89/100

Integrated score: 88/100
Status: EXCELLENT (maintenance mode)

Issues: None critical
Minor suggestions: 1

Last full check: 2 weeks ago
Next full check recommended: in 1 month
```

### 示例 4：边缘情况 — 规范无法推导（置信度 < 70%）

```bash
$ audit-docs --mode full

✓ Phase 1: Pre-flight checks passed
✓ Phase 2: Attempting to derive norms...

⚠️ Norms derivation LOW CONFIDENCE (58%)

  Reason: docs/ contains mixed structure:
    - Some files use docs/design-decisions/ (5 files)
    - Some use docs/decisions/ (3 files)
    - Some use docs/design/ (2 files)

  Cannot auto-accept. Need user review.

? Review suggested norms and confirm?
  [Y] Accept suggested norms
  [N] Run discover-docs-norms for interactive mode
  [R] Review details first
> R

Suggested paths (confidence scores):
  - design-decisions: 70% (5 files)
  - design: 60% (2 files)
  - decisions: 55% (3 files)

? Which should be the canonical path?
  [1] design-decisions (recommended)
  [2] design
  [3] Start fresh with discover-docs-norms
> 1

✓ Using docs/design-decisions/ as canonical path
✓ Norms established (manually confirmed)

⚠️ Recommendation: Run /discover-docs-norms in interactive mode
   to formalize remaining decisions (naming convention, front-matter standard)

Continue with full governance check? [Y/N]
> Y

✓ Phase 3-5: Proceeding...
```

**Why this edge case matters**: When docs structure is inconsistent, automatic derivation can produce false confidence or incorrect patterns. The skill must detect this and either ask the user to clarify or escalate to interactive mode.

---

## 输出报告示例

请参阅下方 `## 附录：示例报告` 以了解 `audit-docs.md` 输出的完整示例。

---

## 附录：示例报告

```markdown
---
artifact_type: doc-governance
created_by: audit-docs
lifecycle: living
created_at: 2026-03-24
status: draft
---

# Documentation Governance Report

## Executive Summary

This report assesses the project's documentation governance maturity across norms, structure, content quality, and code alignment.

**Integrated Score**: 72/100 (GOOD)

| Dimension | Score | Trend | Status |
| --- | --- | --- | --- |
| Norms Completeness | 95% | ✓ Excellent | All artifact types covered |
| Structure Tidiness | 68% | ⚠️ Good | 3 orphaned docs, 2 naming issues |
| Content Readiness | 60% | ⚠️ Needs Work | Milestones layer missing |
| Code Alignment | 85% | ✓ Good | Auth changes documented |
| Graph Health | 78% | ⚠️ Good | 1 broken link, 3 isolated docs |

**Action Priority**: Medium (score sufficient; focus on improvement)

---

## Detailed Findings

### 1. Norms Status: ✓ ESTABLISHED

Documentation norms formalized with:
- 8 artifact types (goals, requirements, architecture, etc.)
- Naming convention: kebab-case with YYYY-MM-DD dates
- 5 required front-matter fields
- Confidence: 95%

### 2. Structure Health: 68/100

**Issues Found**:
- ❌ 3 orphaned documents (no links from other docs)
- ⚠️ 2 files using snake_case instead of kebab-case
- ✓ No misplaced files
- ✓ No empty directories

**Recommendations**:
1. Archive or link 3 orphaned documents
2. Rename 2 snake_case files to kebab-case

### 3. Content Readiness: 60/100

**By Layer**:
- Goals: Strong ✓
- Requirements: Weak ⚠️ (1 file outdated)
- Architecture: Strong ✓
- Design Decisions: Weak ⚠️ (missing 3 recent decisions)
- Milestones: Missing ✗
- Roadmap: Weak ⚠️

**Critical Gaps**:
1. Milestones documentation missing entirely
2. 3 design decisions from past 2 weeks not documented
3. 1 requirements document outdated (last updated 3 months ago)

### 4. Code Alignment: 85/100

(from `--code-diff origin/main`)

**Code Changes**:
- src/api/auth.py [Modified]
- src/db/migration.sql [Added]
- src/utils/cache.ts [Added]

**Document Status**:
- ✓ docs/architecture/api-design.md: UPDATED (refresh_token added)
- ❌ docs/architecture/data-model.md: NOT UPDATED (schema changed)
- ⚠️ docs/guides/api-endpoints.md: PARTIALLY (endpoint list outdated)

### 5. Graph Health: 78/100

- Total docs: 42
- Internal links: 127
- Broken links: 1 (in docs/architecture/api.md → old path)
- Orphaned docs: 3
- Cycles: 0

---

## Prioritized Action Plan

### High Priority (Week 1) - 5 items

1. [ ] **Update docs/architecture/data-model.md**
   - Why: Database schema changed in code
   - Effort: 20 min
   - Impact: High (internal reference)

2. [ ] **Document 3 missing design decisions**
   - Why: ADRs from past 2 weeks not recorded
   - Effort: 45 min
   - Impact: High (architectural clarity)

3. [ ] **Create milestones documentation**
   - Why: Layer completely missing
   - Effort: 1 hour
   - Impact: High (project planning)

4. [ ] **Fix 1 broken link**
   - Why: docs/architecture/api.md → old path
   - Effort: 5 min
   - Impact: Low (visibility)

5. [ ] **Update outdated requirements document**
   - Why: Last updated 3 months ago
   - Effort: 30 min
   - Impact: Medium (requirements accuracy)

### Medium Priority (Week 2-3) - 10 items

6. [ ] Archive 3 orphaned documents
7. [ ] Rename 2 snake_case files
8. [ ] Refresh api-endpoints guide
... (15 more items)

### Success Indicators

- [ ] Integrated score ≥ 80% (target: 1 month)
- [ ] All artifact types have ≥ 1 canonical document
- [ ] 0 broken links
- [ ] 0 orphaned documents
- [ ] Code-docs alignment > 90%

### Maintenance Mode

Once score > 80%, switch to:
```bash
# Weekly quick check
audit-docs --mode quick

# PR checks
audit-docs --mode code-review --code-diff origin/main

# Monthly full review
audit-docs --mode full
```
```

---

**Generated by**: audit-docs v1.0.0
**Command**: `audit-docs --mode full`
**Duration**: ~2 minutes
