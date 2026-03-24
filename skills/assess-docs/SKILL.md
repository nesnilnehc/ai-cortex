---
name: assess-docs
description: Assess documentation health in one pass — validate artifact norms compliance (paths, naming, front-matter) and evidence readiness by layer; report gaps and produce a minimum-fill plan.
description_zh: 一次性评估文档健康：验证制品规范合规（路径、命名、front-matter）与各层证据就绪；产出缺口与最小补齐计划。
tags: [documentation, workflow]
version: 3.2.0
license: MIT
recommended_scope: both
metadata:
  author: ai-cortex
triggers: [doc readiness, documentation readiness, doc gap, doc triage, validate docs, validate documents]
input_schema:
  type: free-form
  description: Project docs scope, optional layer mapping, optional target readiness level, optional docs root
output_schema:
  type: document-artifact
  description: Documentation Assessment Report (compliance findings + layer readiness + minimal fill plan)
  artifact_type: doc-assessment
  path_pattern: docs/calibration/doc-assessment.md
  lifecycle: living
---

# 技能 (Skill)：文档评估

## 目的 (Purpose)

在单次运行中，检查项目文档是否**符合产品规范**（路径、命名、前置事项），并且**足以进行可靠的人工智能辅助规划和调整**。生成一份报告，其中包含合规性调查结果、层准备分数以及最小化的优先填充计划，以缩小关键差距。

---

## 核心目标（Core Objective）

**治理目标**：生成一份文档评估报告，其中 (1) 列出了规范违规行为以及可行的建议，(2) 逐层量化证据质量，并规定了达到目标准备就绪所需的最小文档操作集。

**成功标准**（必须满足所有要求）：

1. ✅ **规范已解决**：来自 `docs/ARTIFACT_NORMS.md` 的项目规范；若不存在，回退到 project-documentation-template 默认值
2. ✅ **合规性检查**：扫描 `docs/` 下所有相关的 Markdown；路径、命名、front-matter 已验证；作为调查结果发出的每项违规行为（位置、类别、严重性、标题、描述、建议）
3. ✅ **层覆盖评估和准备度评分**：评估目标、需求、架构、里程碑、路线图和待办层，并对每个层进行“强”、“弱”或“缺失”评分；计算总体准备情况
4. ✅ **差距优先**：按照对交付和对齐的影响对缺失层和薄弱层进行排序
5. ✅ **制定最小填充计划**：可操作的步骤，包括首先创建/更新的内容以及原因； 转交技巧说明
6. ✅ **报告持久化**：单个输出文档写入商定的路径，其中包含合规性结果和准备情况部分

**验收**测试：队友是否可以仅使用此报告来修复规范违规行为并提高准备情况，而无需猜测首先要做什么？

---

## 范围边界 (Scope Boundaries)

**本技能负责**：

- 解决项目产品规范并扫描 Markdown 的“docs/”
- 合规性验证：路径、命名、前端事项是否符合规范；标准格式的调查结果列表
- 文档清单和图层映射；准备情况评分和差距优先级
- 最小填充计划和针对专业技能的转交建议

**本技能不负责**：

- 建立或更新规范（使用“discover-docs-norms”）
- 从模糊意图出发的完整需求创作（使用“分析需求”）
- 完整的设计合成（使用“设计解决方案”）
- 结构文档从头开始引导（使用“bootstrap-docs”）
- 任务后漂移校准（使用“align-planning”）
- 自动修复违规（用户或其他工具应用建议）

**转交点**：报告交付后，将规范创建交给“discover-docs-norms”，并将创建/更新操作交给相关文档或规划技能。

---

## 使用场景（用例）

- **预提交或审核**：确保文档符合规范并且在里程碑之前足够
- **对齐置信度低**：“对齐规划”报告证据质量较弱
- **带有部分文档的新存储库**：团队需要首先进行合规性检查和最少的文档添加
- **规范更改后**：更新 ARTIFACT_NORMS.md 后重新验证和重新评估
- **文件债务分类**：一份用于合规性和准备情况优先级的报告

---

## 行为（行为）

### 交互（互动）政策

- **默认输入**：文档根 = 存储库 `docs/`；使用项目规范（如果存在）
- **可选参数**：
  - `--code-diff [branch | pr | auto]`：若提供，分析代码变更对文档的影响（新增）
  - `--check-links [true | false]`：默认 true，检查文档链接有效性（新增）
  - `--target-readiness [medium | high]`：目标就绪度
- **确认**：输出路径（若与规范不同）；写之前

### 第 0 阶段：解决范围和映射

1. 解析文档根目录和可选的自定义路径映射
2. **解决项目规范**：检查 `docs/ARTIFACT_NORMS.md`。如果找到，则用于路径模式、命名和层级映射；否则使用 project-documentation-template 默认值。
3. 检测预期层路径：目标`docs/project-overview/`、需求`docs/requirements-planning/`、架构`docs/architecture/`、里程碑/路线图/待办事项`docs/process-management/`（和待办路径）。接受向后兼容的别名（例如“docs/需求/”）。

### 第 1 阶段：合规性验证

1.枚举`docs/`（或用户指定的根目录）下的Markdown
2. 对于每个文件：读取“artifact_type”的前文；如果不存在，则从路径推断（例如`待办/`→待办-item，`设计-decisions/`→设计）。映射到预期的 path_pattern 并根据规范命名。
3. 根据规范验证路径、文件名和前置事项（如适用的“artifact_type”、“created_by”等必填字段）。
4. 针对每个违规行为发出一项调查结果：位置（路径）、类别（”产品规范”|”路径”|”命名”|”前事项”|”root-categorization”）、严重性（”严重”|”主要”|”次要”|”建议”）、标题、描述、建议。摘要：扫描的文件总数、按严重程度划分的违规计数。

5. **Root-Categorization 合规性检查**（在步骤 3 中进行）：
   - 如果文件路径为 `docs/*.md`（根目录）：
   - 检查其是否在允许的根目录文件列表中（README.md、INDEX.md、ARTIFACT_NORMS.md 等）
   - 如果否，标记为 root-categorization 违规，建议移至按 artifact_type 分类的子目录
   - 严重性：`建议`（信息级别，不阻止合规性）

6. **Timestamp 命名合规性检查**（在步骤 3 中进行）：
   - 对每个制品文件：
     - 检查文件名是否有 `YYYY-MM-DD` 前缀
     - 从 ARTIFACT_NORMS.md 查询该 artifact_type 的时间戳策略
     - 如果文件**有**时间戳但类型**不允许** → 标记为 `naming/timestamp-misuse`，建议移除前缀
     - 如果文件**没有**时间戳但类型**需要** → 标记为 `naming/timestamp-missing`（可选）
     - 如果有时间戳但格式错误 → 建议正确格式 `YYYY-MM-DD-title.md`
   - 严重性：`次要`（命名违规，不阻止合规性）

**调查结果格式**（每个调查结果必须遵循）：

|领域|内容 |
| :--- | :--- |
|地点 | `path/to/file.md` |
|类别 | `产品规范` \| `路径` \| `命名` \| `前面的事情` \| `root-categorization` \| `naming/timestamp-misuse` |
|严重性 | `关键` \| `主要` \| `次要` \| `建议` |
|标题 |简短的违规摘要 |
|描述 |怎么了|
|建议 |如何修复（例如移动到 X，添加前面的 Y）|

### 第 2 阶段：清单和证据收集

1. 枚举每层相关文档
2. 检查新鲜度信号（最后更新日期、过时的参考、明显的损坏链接）
3. 标记证据来源：“规范”（项目规划文档）、“次要”（问题/PR/提交上下文）、“无”

### 第 3 阶段：准备情况评分

每层分配一个就绪级别：

- **强**：规范文档存在并且看起来足够最新以提供决策支持
- **弱**：文档存在但不完整、陈旧或依赖于次要证据
- **缺少**：该层没有可用的文档

总体准备情况：

- `high`：没有缺失层且最多有一个薄弱层
- `medium`：一个或多个薄弱层，无关键缺失层
- “低”：至少缺少一个关键层（需求、架构或路线图/待办）

### 第 4 阶段：差距优先排序

对于每个差距，评价影响（高|中|低）、努力（小|中|大）、所有者、到期窗口（本次冲刺|下一个冲刺|待办）。首先以最小的努力降低最高的交付风险为优先顺序。

### 第 5 阶段：最小填充计划

制定最小的行动集，以将准备程度提高到目标水平：首先修复的层、要创建/更新的确切文档路径、建议的转交技能（“引导文档”、“分析需求”、“设计解决方案”）以及此周期的停止条件。

### 第 6 阶段：坚持报告

根据已解决的项目规范或默认的”docs/calibration/doc-assessment.md”写入路径。除非用户明确请求过时的快照，否则覆盖规范文件。包括前面的内容：”产品类型：文档评估”、”创建者：评估文档”、”生命周期：生活”、”创建时间：YYYY-MM-DD”。如果输出目录不存在，则创建它。报告必须包括以下合规调查结果和准备情况部分。

### 第 7 阶段：Code-to-Docs Alignment（可选，若 --code-diff 提供）

**前置条件**：用户指定了 `--code-diff` 参数

**处理流程**：

1. **获取代码 diff**

   ```bash
   git diff <base>...HEAD --name-status --diff-filter=MAD
   ```

   解析结果，分类为：已修改(M)、新增(A)、删除(D) 的文件

2. **推断代码区域**
   - `src/api/*` → area: “api”
   - `src/utils/*` → area: “utils”
   - `src/core/*` → area: “core”
   - `src/auth/*` → area: “auth”
   - 等等

3. **查询 doc update map**，找出每个代码区域应该更新的文档路径

4. **检查相关文档是否更新**
   - 在本 branch 中修改的文档
   - vs 推断应修改的文档
   - 输出缺口

5. **发出 alignment findings**

   ```
   格式同”第 1 阶段”的 violations：
   位置、类别（code-alignment）、严重性、标题、描述、建议
   ```

**输出示例**：

```
| Location | Category | Severity | Title | Description |
| --- | --- | --- | --- | --- |
| src/api/auth.py | code-alignment | high | API changed but docs not updated | auth.py modified but docs/architecture/api.md not touched |
```

### 第 8 阶段：Documentation Graph Analysis（新增）

**前置条件**：`--check-links` 参数为 true（默认）

**处理流程**：

1. **构建文档依赖图**
   - 扫描所有 .md 文件中的链接
   - 识别 Markdown links: `[title](../path/file.md)`
   - 识别 Wiki links: `[[file]]`
   - 识别 URL links（仅标记，不检查外部有效性）

2. **检测图问题**
   - **孤立文档**：无入度且无出度

     ```python
     orphaned = [node for node in graph.nodes
                 if in_degree(node) == 0 and out_degree(node) == 0]
     ```

   - **损坏链接**：目标文件不存在

     ```python
     broken = [edge for edge in graph.edges
               if not file_exists(edge.target)]
     ```

   - **循环引用**：存在环
   - **嵌套过深**：引用链过长（4+ 跳）

3. **计算 Health Score**

   ```
   health_score = 100 - (broken_count * 10 + orphan_count * 5 + cycle_count * 15)
   最终范围：0-100
   ```

4. **发出 graph findings**

   ```
   - Broken links: 2
     - docs/architecture/api.md → ../design/auth (expected ../design-decisions/)

   - Orphaned docs: 3
     - docs/archive/2024-decisions.md
     - docs/calibration/temp-notes.md

   - Cross-doc consistency issues: 1
     - Version: README says v1.2 but CHANGELOG latest is v1.1
   ```

**输出示例**：

```markdown
## Documentation Graph Health

- Total docs: 42
- Broken links: 2
- Orphaned docs: 3
- Health score: 92%

**Issues requiring attention:**
1. Fix broken links (2 occurrences)
2. Archive or link orphaned docs (3 files)
3. Update version reference in README
```

---

## 输入与输出（输入&输出）

### 输入（输入）

- 文档根路径（默认存储库文档根）
- 非模板项目的可选路径映射
- 可选的目标准备情况（“中”或“高”）

### 输出（输出）

具有以下结构的单个文档产品：


```markdown
---
artifact_type: doc-assessment
created_by: assess-docs
lifecycle: living
created_at: YYYY-MM-DD
---

# Documentation Assessment Report

**Date:** YYYY-MM-DD
**Overall Readiness:** high | medium | low
**Target Readiness:** medium | high

## Compliance Findings

Summary: N files scanned; M violations (by severity: critical, major, minor, suggestion).

| Location | Category | Severity | Title | Description | Suggestion |
| :--- | :--- | :--- | :--- | :--- | :--- |
| path/to/file.md | artifact-norms | major | ... | ... | ... |

(If no violations: "No norm violations found.")

## Layer Readiness

- Goal: strong | weak | missing
- Requirements: strong | weak | missing
- Architecture: strong | weak | missing
- Milestones: strong | weak | missing
- Roadmap: strong | weak | missing
- Backlog: strong | weak | missing

## Gap Priority List

1. Gap: ...
   Impact: high | medium | low
   Effort: small | medium | large
   Owner: ...
   DueWindow: this-sprint | next-sprint | backlog

## Minimal Fill Plan

1. Path: ...
   Why now: ...
   Handoff skill: ...
   Done condition: ...

## Machine-Readable Summary

    overallReadiness: "medium"
    complianceSummary: { filesScanned: N, violations: M }
    layers:
      requirements: "missing"
      architecture: "weak"
    gaps:
      - id: "gap-req-core"
        impact: "high"
        effort: "small"
        owner: "product-owner"
        dueWindow: "this-sprint"
```


---

## 限制（限制）

### 硬边界（Hard Boundaries）

- 请勿伪造不存在的文档
- 请勿重写本技能中的产品策略、需求或架构决策
- 当最小计划就足够时，不要规定全面的文档修改
- 当关键层丢失时，请勿将就绪状态标记为高
- **合规阶段**：不要修改文件；仅报告调查结果。结果必须遵循上述标准格式。

### 技能边界 (Skill Boundaries)（避免重叠）

**不要做这些（其他技能可以处理它们）**：

- 创建或更新产品规范 → `discover-docs-norms`
- 模板引导和结构初始化 → `bootstrap-docs`
- 需求内容开发→`分析需求`
- 建筑/设计决策工作流程 → `设计解决方案`
- 任务后漂移和重新校准→“对齐规划”
- 自动修复违规→用户应用建议

**何时停止并交接**：

- 如果规范缺失或需要更新 → 移交给“discover-docs-norms”
- 如果主要差距是需求质量 → 移交给“分析需求”
- 如果主要差距是架构清晰度→移交给“设计解决方案”
- 如果文档框架广泛缺失 → 移交给“bootstrap-docs”

---

## 自检（Self-Check）

### 核心成功标准（必须满足所有标准）

- [ ] 已解决规范；文档扫描
- [ ] 以标准格式发布合规调查结果（位置、类别、严重性、标题、描述、建议）
- [ ] 评估所有规划层；每层的准备情况按基本原理进行评分
- [ ] 按影响和努力优先排序的差距
- [ ] 最小填充计划包括混凝土路径和转交
- [ ] 输出持续遵循合规调查结果和准备情况部分商定的路径

### 流程质量检查

- [ ] 规范证据与次要证据明显分开
- [ ] 未隐藏在总分中的关键缺失层
- [ ] 建议最少且具有排序意识
- [ ] 切换技能名称有效并且是最新的

### 验收测试

**团队能否利用报告中的前 3 项行动来纠正违规行为并提高准备情况？**

如果否：减少歧义并加强优先顺序或调查结果。
如果是：报告已完成。

---

## 示例（示例）

### 示例 1：合规性 + 准备度

- 合规性：非标准路径中的`docs/designs/2026-03-06-auth.md`→使用建议“移至docs/design-decisions/2026-03-06-auth.md”查找
- 准备情况：缺少需求层 → 计划：首先使用“analyze-requirements”创建“docs/requirements-planning/core-v1.md”

### 示例 2：缺少需求层

- 调查结果：目标和路线图存在，需求文档缺失
- 准备情况：“低”
- 计划：首先使用“analyze-Customer”创建“docs/demand-planning/core-v1.md”

### 示例 3：弱架构层

- 调查结果：架构文档存在，但陈旧且与最近的 ADR 相矛盾
- 准备情况：“中”
- 计划：刷新架构决策文档，然后重新运行“align-planning”

### 示例 4：路径不匹配（合规性）

- 文件：`docs/designs/2026-03-06-auth.md`（项目规范：`docs/design-decisions/`）
- 查找：位置`docs/designs/2026-03-06-auth.md`，类别`产品规范`，严重性`major`，标题“非标准路径中的设计文档”，描述“文件位于 docs/designs/ 但规范指定docs/design-decisions/”，建议“移至docs/design-decisions/2026-03-06-auth.md”