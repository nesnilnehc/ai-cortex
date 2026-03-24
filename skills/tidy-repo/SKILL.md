---
name: tidy-repo
description: Audit repository structure in one pass — detect misplaced files, naming inconsistencies, empty directories, and stale artifacts; produce a prioritized tidy report; optionally apply safe, reversible changes.
description_zh: 一次性审计仓库目录结构——检测错放文件、命名不一致、空目录和过期制品；输出优先级整理报告；可选地应用安全、可逆的清理操作。
tags: [repository, workflow, cleanup, structure]
version: 1.0.0
license: MIT
recommended_scope: both
metadata:
  author: ai-cortex
triggers: [tidy repo, clean up repo, organize repository, repo structure, messy repo, clean repo, 整仓整理, 整理仓库, 目录整理]
input_schema:
  type: free-form
  description: Repository root (default CWD), optional scope filter, optional mode (report-only | apply-safe)
output_schema:
  type: document-artifact
  description: Tidy Report with findings, cleanup plan, and optional apply log
  artifact_type: repo-tidy
  path_pattern: docs/calibration/repo-tidy.md
  lifecycle: living
---

# 技能 (Skill)：整仓整理

## 目的 (Purpose)

在单次运行中，扫描仓库（或指定范围）的目录结构，识别结构性问题——错放文件、命名不一致、空目录、过期制品、重复条目——并输出一份**带优先级的整理报告**，指导人工或自动清理。在 `apply-safe` 模式下，可直接执行安全、可逆的操作。

---

## 核心目标 (Core Objective)

**治理目标**：生成一份仓库整理报告，其中 (1) 以标准格式列出所有结构问题及建议操作，(2) 按影响和代价排序，给出具体的清理步骤，(3) 可选地在 `apply-safe` 模式下执行并记录操作日志。

**成功标准**（必须满足所有要求）：

1. ✅ **范围已确定**：明确扫描根路径和排除列表（`.git`、`node_modules`、`.venv` 等）
2. ✅ **问题已枚举**：所有发现以标准格式输出（位置、类别、严重性、标题、描述、建议）
3. ✅ **优先级已排序**：按影响（高|中|低）和操作代价（小|中|大）排序
4. ✅ **清理计划可操作**：每步包含具体路径、操作类型、完成条件
5. ✅ **安全边界已遵守**：`report-only` 模式不修改任何文件；`apply-safe` 仅执行可逆操作
6. ✅ **报告已持久化**：写入商定路径，包含合规前置事项

**验收测试**：团队是否可以仅凭此报告的前 5 项行动，让仓库结构显著改善？若否，减少歧义并强化优先级。

---

## 范围边界 (Scope Boundaries)

**本技能负责**：

- 枚举并分析仓库文件和目录结构
- 识别：错放文件、命名不一致、空目录、过期/废弃制品、重复条目
- 按类别和严重性输出标准格式的发现列表
- 生成优先级清理计划
- （可选）在 `apply-safe` 模式下执行移动、删除空目录等可逆操作，并记录日志

**本技能不负责**：

- 代码质量或架构问题 → `review-codebase`
- 文档规范合规性 → `assess-docs`
- 需求或计划文档的内容质量 → `align-planning`
- 危险操作（批量删除有内容的目录、修改 git 历史等）→ 人工执行
- 提交整理后的变更 → `commit-work`

**转交点**：报告交付后，可将提交操作交给 `commit-work`；若发现文档规范问题，交给 `assess-docs`；若发现架构问题，交给 `review-codebase`。

---

## 使用场景 (Use Cases)

- **日常维护**：仓库积累文件后的定期结构健康检查
- **入职对齐**：新成员加入时，快速了解并对齐目录约定
- **重构后清理**：代码重构或模块拆分后，清除残留的旧路径和废弃文件
- **CI/CD 门控**：在流水线中作为结构合规检查步骤
- **发布前整理**：在版本发布前确保仓库整洁

---

## 行为 (Behavior)

### 交互策略

- **前置条件**：项目必须有文档规范（新增）
- **默认模式**：`report-only`，不修改任何文件
- **apply-safe 模式**：执行前向用户确认操作列表；失败时回滚已执行步骤
- **范围**：默认扫描当前工作目录；排除 `.git`、`node_modules`、`.venv`、`dist`、`build`、`__pycache__`、`.DS_Store` 等

### 前置条件检查（新增）

**目的**：确保项目已建立文档规范，以便准确检测命名和路径问题

**检查**：
1. 查找 `docs/ARTIFACT_NORMS.md`
2. 若不存在，**拒绝继续**并输出：
   ```
   ✗ 找不到文档规范

   tidy-repo 需要项目先建立文档规范来准确检测文件位置和命名问题。

   请先运行：
   /discover-docs-norms

   此命令将：
   - 扫描现有 docs/ 结构
   - 推导出项目的命名和路径约定
   - 生成 docs/ARTIFACT_NORMS.md

   然后重新运行 tidy-repo。
   ```

### 第 0 阶段：范围解析

1. 解析仓库根路径（默认 CWD）和可选范围过滤
2. **强制加载**项目约定（前置条件已验证存在）：从 `docs/ARTIFACT_NORMS.md` 解析命名规则和目录结构期望
3. 构建排除列表（二进制文件目录、依赖目录、构建产物目录）

### 第 1 阶段：结构扫描

1. 递归枚举所有文件和目录（遵循排除列表）
2. 构建目录树快照，记录：路径、类型（文件|目录）、大小、最后修改时间、扩展名

### 第 2 阶段：问题检测

对每个条目按以下类别检测：

| 类别 | 检测逻辑 |
| :--- | :--- |
| `misplaced` | 文件所在目录与其类型/内容不符（如 `.md` 在 `src/`，`.py` 在 `docs/`） |
| `naming` | 文件或目录名违反项目约定（大小写、分隔符、前缀/后缀不一致） |
| `empty-dir` | 目录下无任何有效文件（仅含 `.gitkeep` 除外） |
| `dead-artifact` | 明显废弃的文件（扩展名为 `.bak`、`.tmp`、`.orig`；名称含 `DEPRECATED`、`OLD`、`UNUSED`；超过 180 天未修改且无引用） |
| `duplicate` | 文件名或路径高度相似，疑似重复（如 `util.py` 与 `utils.py` 在同目录） |
| `structure` | 顶层出现非预期目录，或缺少约定的标准目录（如 `docs/`、`src/`） |

### 第 3 阶段：发现输出

每个发现必须遵循标准格式：

| 字段 | 内容 |
| :--- | :--- |
| 位置 | `path/to/file-or-dir` |
| 类别 | `misplaced` \| `naming` \| `empty-dir` \| `dead-artifact` \| `duplicate` \| `structure` |
| 严重性 | `critical` \| `major` \| `minor` \| `suggestion` |
| 标题 | 简短问题摘要 |
| 描述 | 具体说明哪里不对 |
| 建议 | 具体操作（如"移至 X"、"重命名为 Y"、"删除空目录"、"确认是否废弃后删除"） |

汇总：扫描文件总数、目录总数、各类别发现数量、各严重性发现数量。

### 第 4 阶段：优先级排序

对每个发现评估：
- **影响**（高|中|低）：对可导航性、CI、新成员入职的阻碍程度
- **操作代价**（小|中|大）：执行建议操作的工作量

排序原则：优先处理高影响、低代价的问题（快速胜利）；其次为高影响、高代价（需规划）；最后为低影响问题（可选）。

### 第 5 阶段：清理计划

输出最小可操作步骤集：

每步包含：
- 操作路径
- 操作类型（`move` | `rename` | `delete-empty-dir` | `archive` | `review-manually`）
- 原因（Why now）
- 完成条件
- 是否可在 `apply-safe` 模式自动执行

### 第 6 阶段（可选）：apply-safe 执行

仅在用户明确传入 `apply-safe` 模式时激活：

1. 向用户展示将要执行的操作列表，等待确认
2. 仅执行以下安全操作：
   - 移动/重命名文件（`git mv` 优先）
   - 删除**空目录**
3. 跳过（并标记为"需人工处理"）：
   - 删除有内容的目录
   - 覆盖已有文件
   - 任何不可逆操作
4. 记录操作日志，追加到报告末尾

### 第 7 阶段：持久化报告

写入路径（按项目规范或默认 `docs/calibration/repo-tidy.md`）。报告前置事项：

```yaml
artifact_type: repo-tidy
created_by: tidy-repo
lifecycle: living
created_at: YYYY-MM-DD
```

---

## 输入与输出 (Inputs & Outputs)

### 输入

- 仓库根路径（默认 CWD）
- 可选范围过滤（子目录或 glob）
- 可选模式：`report-only`（默认）| `apply-safe`

### 输出

```markdown
---
artifact_type: repo-tidy
created_by: tidy-repo
lifecycle: living
created_at: YYYY-MM-DD
---

# Repository Tidy Report

**Date:** YYYY-MM-DD
**Scope:** /path/to/root (filtered: src/)
**Mode:** report-only | apply-safe
**Summary:** N files, M dirs scanned; K findings (critical: X, major: Y, minor: Z, suggestion: W)

## Findings

| Location | Category | Severity | Title | Description | Suggestion |
| :--- | :--- | :--- | :--- | :--- | :--- |
| src/utils.bak | dead-artifact | major | Backup file in source | .bak file committed to source tree | Remove or archive to .archive/ |

(If no findings: "No structural issues found.")

## Cleanup Plan

### Quick Wins (high impact, low effort)

1. **Path:** src/utils.bak
   **Action:** delete
   **Why now:** Dead artifact pollutes source tree
   **Done condition:** File removed; no references in codebase
   **Auto-apply:** yes

### Plan Next Sprint (high impact, high effort)

...

### Optional / Low Priority

...

## Apply Log (apply-safe mode only)

| Action | Path | Result |
| :--- | :--- | :--- |
| delete-empty-dir | tmp/ | success |
| move | docs/OLD-arch.md → .archive/OLD-arch.md | success |
| skipped (manual) | src/legacy/ | non-empty directory — review manually |

## Machine-Readable Summary

    scope: "."
    mode: "report-only"
    filesScanned: 142
    dirsScanned: 28
    findings:
      total: 7
      bySeverity: { critical: 0, major: 3, minor: 2, suggestion: 2 }
      byCategory: { misplaced: 1, naming: 2, empty-dir: 1, dead-artifact: 2, duplicate: 1 }
    topActions:
      - { path: "src/utils.bak", action: "delete", impact: "high", effort: "small" }
```

---

## 限制 (Constraints)

### 硬边界 (Hard Boundaries)

- `report-only` 模式**绝不修改**任何文件或目录
- `apply-safe` 模式**绝不删除**有内容的目录；所有危险操作标记为"需人工处理"
- 不伪造或推测文件内容；仅基于路径、名称、修改时间、大小判断
- 不修改 git 历史
- 不执行任何网络操作

### 技能边界 (Skill Boundaries)

**不要做（其他技能处理）**：

- 代码质量、架构、依赖审查 → `review-codebase`
- 文档内容规范和准备情况 → `assess-docs`
- 需求/规划文档对齐 → `align-planning`
- 提交清理结果 → `commit-work`

**何时停止并交接**：

- 若发现大量文档规范违规 → 交给 `assess-docs`
- 若需要提交整理变更 → 交给 `commit-work`
- 若发现架构层面问题 → 交给 `review-codebase`

---

## 自检 (Self-Check)

### 核心成功标准（必须满足所有标准）

- [ ] 范围已明确；排除列表已应用
- [ ] 所有发现以标准格式输出（位置、类别、严重性、标题、描述、建议）
- [ ] 发现已按影响和代价排序
- [ ] 清理计划包含具体路径和操作类型
- [ ] apply-safe 模式仅执行可逆操作，并记录操作日志
- [ ] 报告已写入商定路径，包含合规前置事项

### 流程质量检查

- [ ] 没有误报高严重性的低影响问题
- [ ] 建议操作具体且可直接执行
- [ ] 交接技能名称有效且最新

### 验收测试

**团队是否可以仅凭报告前 5 项行动，让仓库结构显著改善？**

若否：减少歧义，强化优先级和具体性。若是：报告已完成。

---

## 示例 (Examples)

### 示例 1：发现废弃制品

- 文件：`src/auth.py.bak`，7 个月未修改
- 发现：位置 `src/auth.py.bak`，类别 `dead-artifact`，严重性 `major`，标题"源码目录中的备份文件"，描述"`.bak` 文件被提交至源码树中"，建议"删除或移至 `.archive/`"
- 清理计划：Quick Win；`apply-safe` 可自动执行

### 示例 2：空目录

- 目录：`tmp/cache/`（无任何文件）
- 发现：类别 `empty-dir`，严重性 `minor`，建议"删除空目录，或添加 `.gitkeep` 若有意保留"
- `apply-safe` 模式：自动删除

### 示例 3：命名不一致

- 发现：`src/` 下同时存在 `UserService.py`（PascalCase）和 `auth_service.py`（snake_case）
- 严重性：`major`，建议"统一命名约定；参考项目现有主导风格决定重命名方向"
- 标记为"需人工处理"（重命名涉及导入引用更新）

### 示例 4：apply-safe 执行日志

```
已执行：delete-empty-dir tmp/cache/        ✓
已执行：move docs/OLD-arch.md → .archive/ ✓
已跳过：src/legacy/（非空目录，需人工处理）
```
