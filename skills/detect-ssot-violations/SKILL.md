---
name: detect-ssot-violations
description: Detect semantic duplication across documents and enforce single source of truth (SSOT) principles. Atomic skill called by audit-docs or standalone.
description_zh: 检测跨文档语义重复，执行单一事实源（SSOT）原则。原子技能，由 audit-docs 调用或独立使用。
tags: [documentation, governance, data-integrity, ssot, deduplication]
version: 1.0.0
license: MIT
recommended_scope: project
metadata:
  author: ai-cortex
  artifact_type: detect-ssot-violations-report
  lifecycle: living
  role: atomic-skill  # 原子技能，可被 audit-docs 编排调用
triggers: [SSOT violation, semantic duplication, canonical source, document overlap, ssot audit]
input_schema:
  type: free-form
  description: Project path (default CWD), optional artifact types filter, overlap threshold
  defaults:
    mode: full
    artifact_types: null
    min_overlap_ratio: 0.3
output_schema:
  type: document-artifact
  description: SSOT violation report with conflict matrix, deduplication recommendations, and repair roadmap
  artifact_type: detect-ssot-violations-report
  path_pattern: docs/calibration/ssot-violations.md
  lifecycle: living
---

# 技能（Skill）：语义重复与单一事实源检测

**角色定位**：原子技能（Atomic Skill）。可单独使用，也被 `audit-docs` 在 `full` 模式下自动调用。

## 目的 (Purpose)

自动检测跨文档的语义重复与单一事实源（SSOT）违规。识别"复写"vs"引用"，生成可执行的冲突矩阵和修复路线图，确保文档生态中信息流清晰、权威来源明确。

## 核心目标 (Core Objective)

**首要目标**：在文档治理基础上，建立**语义完整性**，防止跨文档的权威冲突和信息重复，确保项目文档体系的单一事实源原则得以贯彻。

**成功标准**（必须满足所有要求）：

1. ✅ **检测与分类完成**：识别所有跨文档的语义重叠（章节级、表格级、段落级）
2. ✅ **冲突矩阵已生成**：清晰展示文档对、重叠内容、冲突类型、建议保留源
3. ✅ **SSOT 规则已定义**：对每类制品（roadmap/milestones/requirements/tasks）明确 canonical source
4. ✅ **修复路线图已生成**：P0/P1/P2 优先级的可直接执行的修复任务（>=10 条）
5. ✅ **修复建议可操作**：每条问题包含严重级别、证据片段、受影响文件、具体修复动作

**验收测试**：新团队成员仅通过报告即能理解每类信息的权威来源，并在 1 次迭代内解决所有 P0 问题。

## 范围边界 (Scope Boundaries)

**本技能负责**：
- 扫描 docs/ 下所有 .md 文档
- 检测跨文档的语义重叠（章节标题、表格、列表、代码示例）
- 分类重叠类型：完全复写、部分复写、摘要+链接（合规）、引用（合规）
- 按 artifact_type 进行边界校验（roadmap vs milestones vs requirements vs tasks）
- 针对每个重叠生成：冲突对、重叠率、建议保留源、修复动作
- 生成 SSOT 规则定义（canonical source for each artifact type）
- 生成修复路线图（P0/P1/P2）与实施顺序

**本技能不负责**：
- 实际执行文档修改 → 分配给团队或下游技能
- 详细代码审查 → 使用 `review-code`
- 策略制定 → 使用 `define-vision` 或 `design-solution`

**交接点**：当报告完成且优先级路线图明确时，交接给 `audit-docs` 进行集成，或交接给团队执行修复。

## 使用场景 (Use Cases)

| 场景 | 何时 | 输出焦点 |
| --- | --- | --- |
| **治理初建立** | 建立 SSOT 规则 | SSOT 定义、冲突矩阵、P0 修复列表 |
| **定期审查** | 月度/季度检查 | 新增重叠检测、规则合规性 |
| **合并相关文档时** | 多个主题文档重组 | 重叠分析、建议合并策略 |
| **跨项目规范建设** | 多项目统一文档治理 | SSOT 可迁移规则、通用冲突模式 |

---

## 行为 (Behavior)

### 交互策略 (Interaction Policy)

遵循规范 §4.3（默认优先，选择优先，上下文推理）：

| 参数 | 默认值 | 推理 | 用户覆盖 |
| --- | --- | --- | --- |
| **project-path** | CWD | Git 根目录自动检测 | `--project <path>` |
| **artifact-types** | 全部 | 检测所有制品类型 | `--types roadmap,milestones,requirements` |
| **min-overlap-ratio** | 0.3 | 30% 重叠即标记为问题 | `--min-overlap <0.1-1.0>` |
| **canonical-sources** | ARTIFACT_NORMS | 从规范读取定义 | `--canonical <type>:<file>` |
| **output-format** | markdown | 生成可读报告 | `--format json/markdown` |

### 执行流程 (Execution Flow)

**第 1 步：预飞行检查** (~30 秒)
- 验证 git 仓库（否则 ERROR）
- 检查 docs/ 存在（若缺失 WARN，继续）
- 验证 ARTIFACT_NORMS.md 存在，加载 canonical source 定义

**第 2 步：文档扫描与解析** (1-3 分钟，取决于项目大小)
- 递归扫描 docs/ 下所有 .md 文件
- 为每个文件提取：
  - 标题树（# ## ### 层级）
  - 表格（markdown 表格格式）
  - 列表（无序/有序）
  - 前 50 字符的段落摘要（用于语义相似度计算）
- 推断每个文件的 artifact_type（基于路径和 ARTIFACT_NORMS）

**第 3 步：语义重叠检测** (1-5 分钟)
- 对所有文件对 (A, B) 执行：
  - **标题匹配**：同一 artifact_type 中的相同标题 → 检测为完全重叠
  - **表格匹配**：相同列头和 >30% 行内容 → 部分重叠
  - **列表匹配**：相同列表项 >30% → 部分重叠
  - **段落语义相似度**：使用简单关键词匹配（>5 个关键词相同）→ 候选重叠
- 输出每个重叠的：
  - 文档 A、文档 B、重叠类型、重叠率（%）
  - 重叠的具体片段（前 100 字符）

**第 4 步：SSOT 规则校验** (~30 秒)
- 对每个 artifact_type 检查：
  - canonical source 是否已在 ARTIFACT_NORMS 中定义？
  - 若未定义，生成警告：该类型需要明确 SSOT 定义
  - 对每个检测到的重叠，判断：
    - 若 A 是 canonical source，B 是引用 → 检查 B 中是否包含"见 A"链接
    - 若 B 包含完整内容 + 链接 → 标记为"合规引用"
    - 若 B 是完全复写（无引用链接）→ 标记为"违规复写"
    - 若 A、B 都不是 canonical source → 标记为"多源冲突"

**第 5 步：冲突矩阵生成** (~1 分钟)
- 生成表格，每一行为一个冲突对：
  - 文档 A | 文档 B | 重叠类型 | 重叠率 | 建议保留源 | 修复动作
  - 按重叠率降序排列

**第 6 步：修复路线图生成** (~2 分钟)
- 对每个冲突生成修复建议：
  - **P0（严重）**：违规复写（不合规），影响 canonical source 权威性
    - 动作：删除 B 中的重复内容，保留摘要 + 链接
  - **P1（重要）**：多源冲突，信息可能冲突
    - 动作：确认 canonical source，合并为单一来源，其他文档引用
  - **P2（轻微）**：合规引用中缺少链接或摘要不准确
    - 动作：优化摘要、补充链接、改进格式

**第 7 步：生成报告** (~1 分钟)
- 输出 `docs/calibration/ssot-violations.md`
- 包含：
  - **SSOT 规则定义**：每个 artifact_type 的 canonical source
  - **冲突矩阵**：所有检测到的重叠
  - **修复路线图**：P0/P1/P2 按优先级排列，含执行顺序和风险提示
  - **样本修复步骤**：至少 3 个具体示例，展示"修复前"和"修复后"

**总预计时间**：5-15 分钟（取决于项目大小和重叠数量）

---

## 输入与输出 (Input & Output)

### 输入 (Input)

```bash
detect-ssot-violations [--project <path>]
                       [--types <type1,type2,...>]
                       [--min-overlap <ratio>]
                       [--canonical <type>:<file>]
                       [--output-format markdown|json]
```

**参数**：

| 参数 | 默认值 | 类型 | 说明 |
| --- | --- | --- | --- |
| `--project` | CWD | path | Git 根目录自动检测；用于覆盖 |
| `--types` | 全部 | enum | 要检查的 artifact_type（逗号分隔）；留空检查全部 |
| `--min-overlap` | 0.3 | float | 重叠率阈值（0.0-1.0）；低于此阈值的重叠忽略 |
| `--canonical` | ARTIFACT_NORMS | path | canonical source 定义来源（ARTIFACT_NORMS.md 路径或自定义） |
| `--output-format` | markdown | enum | markdown（可读）或 json（机器可读） |

### 输出 (Output)

**总是生成**：
- `docs/calibration/ssot-violations.md`：完整 SSOT 违规报告（artifact_type: detect-ssot-violations-report, lifecycle: living）

**条件生成**：
- 若 `--output-format json`：同时输出 `docs/calibration/ssot-violations.json`，机器可读格式

---

## 输出结构 (Output Structure)

### `docs/calibration/ssot-violations.md`

```markdown
# 单一事实源（SSOT）检测报告

**生成时间**：YYYY-MM-DD HH:MM:SS
**扫描范围**：docs/ 下所有 .md 文件
**检测到的重叠**：N 条

---

## 第 1 节：SSOT 规范定义

### 定义的 Canonical Sources

| Artifact Type | Canonical Source | 备注 |
| --- | --- | --- |
| roadmap | docs/process-management/roadmap.md | 路线图唯一权威来源 |
| milestones | docs/process-management/roadmap.md（嵌入） | 里程碑详情在 roadmap 中定义 |
| requirements | docs/requirements-planning/ | 各主题需求的权威来源 |
| backlog-item | docs/process-management/backlog.md（索引）+backlog/YYYY-MM-DD-* | 工作条目的权威来源 |
| adr | docs/process-management/decisions/YYYYMMDD-*.md | 架构决策的权威来源 |
| design | docs/designs/YYYY-MM-DD-*.md | 设计文档的权威来源 |

### 合规引用规则

- **完整复写**：两个文档包含相同内容（>80% 重叠）→ **违规**（除非一方是另一方的快照）
- **摘要+链接**：引用文档包含摘要（20-30% 原内容）+ 指向 canonical source 的链接 → **合规**
- **纯引用**：引用文档仅包含链接，无重复内容 → **合规**
- **跨类型复写**：不同 artifact_type 的文档各有独立权威源，相同信息应有清晰的主仆关系 → **需校验**

---

## 第 2 节：冲突矩阵

### 所有检测到的重叠（按重叠率降序）

| # | 文档 A | 文档 B | 重叠类型 | 重叠率 | 重叠内容摘要 | 建议保留源 | 修复动作 | 优先级 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | roadmap.md | designs/2026-03-02-ai-cortex-evolution-roadmap.md | 完全重叠 | 85% | 里程碑 M5/M6/M7 定义 | roadmap.md | 删除设计文档中重复的里程碑，保留摘要+链接 | P0 |
| 2 | roadmap.md | decisions/20260322-strategic-goals-milestones-framing.md | 部分重叠 | 45% | 里程碑语义和阶段分层 | roadmap.md | 优化决策文档，重点改为"阶段与目标关系定义"，里程碑详情链接到 roadmap | P1 |
| ... | ... | ... | ... | ... | ... | ... | ... | ... |

---

## 第 3 节：修复路线图

### P0（严重 - 立即修复）

#### P0.1：删除 designs/2026-03-02-ai-cortex-evolution-roadmap.md 中的冗余里程碑定义

**问题**：该设计文档与 roadmap.md 重复定义了 M5、M6、M7，造成权威冲突。

**证据**：
- roadmap.md 第 17-20 行：完整的里程碑定义
- evolution-roadmap.md 第 26-30 行：相同的里程碑定义
- 重叠率：88%

**受影响文件**：
- `docs/designs/2026-03-02-ai-cortex-evolution-roadmap.md`（需修改）
- `docs/process-management/roadmap.md`（canonical，无需改动）

**修复步骤**：
1. 打开 `docs/designs/2026-03-02-ai-cortex-evolution-roadmap.md`
2. 删除"## 里程碑详情"章节（原第 66-74 行）
3. 在原位置插入：`详见 [roadmap.md 里程碑详情](../process-management/roadmap.md#里程碑详情附录)`
4. 在"背景"部分增加说明：本演进路线图关注技术架构与分层（A-E），具体里程碑见 roadmap.md

**验证**：
- 修改后，该文档不再包含 M5、M6、M7 的完整定义
- 使用 `detect-ssot-violations --min-overlap 0.8` 重新扫描，该冲突对应消失

**预计改动**：1 个文件，删除 ~10 行，新增 ~2 行链接说明
**风险**：低（增加链接，未删除关键信息）

---

#### P0.2：明确 strategic-goals.md 的 canonical 地位

**问题**：backlog.md 中重复了战略目标的完整列表，与 strategic-goals.md 重复率 76%。

**证据**：
- strategic-goals.md：4 个目标的完整定义
- backlog.md 的"相关"部分：引用了相同的 4 个目标

**受影响文件**：
- `docs/process-management/backlog.md`（需修改）
- `docs/project-overview/strategic-goals.md`（canonical）

**修复步骤**：
1. 打开 `docs/process-management/backlog.md`
2. 在"相关"部分，将目标列表删除
3. 改为：`战略目标见 [strategic-goals.md](../project-overview/strategic-goals.md)`

**验证**：
- backlog.md 与 strategic-goals.md 的重叠率降至 <20%（仅保留链接）

**预计改动**：1 个文件，删除 ~8 行
**风险**：低（保留链接，指向权威源）

---

### P1（重要 - 本周内修复）

#### P1.1：优化 decisions/20260322-strategic-goals-milestones-framing.md

**问题**：该决策文档与 roadmap.md 的"里程碑详情"章节有 52% 的内容重叠。

**受影响文件**：
- `docs/process-management/decisions/20260322-strategic-goals-milestones-framing.md`（需修改）
- `docs/process-management/roadmap.md`（canonical）

**修复步骤**：
1. 打开 ADR 文档
2. 在第 3 节"对现有文档的修订"中，删除重复的表格内容
3. 改为摘要形式，加链接：`详见 roadmap.md 的里程碑定义`

**预计改动**：1 个文件，修改 ~5 行
**风险**：低

#### P1.2：补充 promotion-iteration-tasks.md 的 canonical 源链接

**问题**：该文档中的"计划工作"表格与 designs/2026-03-06-promotion-and-iteration.md 中的内容 68% 重叠，但未标注来源。

**修复步骤**：
1. 在表格上方增加说明：`基于设计文档 [promotion-and-iteration.md](../designs/2026-03-06-promotion-and-iteration.md)，供任务追溯`

**预计改动**：1 个文件，新增 1 行说明
**风险**：极低

### P2（轻微 - 优化，下月处理）

#### P2.1：改进 backlog.md 的交叉引用清晰度

**问题**：多个链接使用相对路径且未标注链接类型（design/adr/skill），新贡献者需要逐一点击判断。

**修复步骤**：
1. 为 backlog.md 中的所有链接增加 Markdown 链接文本，指明类型：
   - `[promotion-and-iteration (design)](../designs/2026-03-06-promotion-and-iteration.md)`
   - `[strategic-goals-milestones-framing (adr)](../process-management/decisions/20260322-strategic-goals-milestones-framing.md)`

**预计改动**：1 个文件，修改 ~6 个链接
**风险**：极低

---

## 第 4 节：执行顺序与依赖

### 推荐修复顺序

```
P0.1（演进路线图） → P0.2（战略目标）
                    ↓
                  P1.1（ADR 优化）
                    ↓
                  P1.2（任务链接）
                    ↓
                  P2（下月优化）
```

**关键路径**：P0 必须先执行，以消除权威冲突。P1、P2 可并行。

---

## 第 5 节：统计与趋势

### 检测统计

| 指标 | 数值 |
| --- | --- |
| 扫描的文档总数 | N |
| 检测到的重叠对数 | M |
| 平均重叠率 | X% |
| P0 级别问题 | 2 |
| P1 级别问题 | 2 |
| P2 级别问题 | 1 |

### 问题分布

- **完全重叠**（>80%）：2 处（P0）
- **高度重叠**（50-80%）：2 处（P1）
- **部分重叠**（30-50%）：1 处（P2）

### 后续建议

1. **自动化检测**：在 CI/CD 中集成 SSOT 检查，每次 PR 对新增文档自动扫描
2. **规则强化**：确定每个 artifact_type 的 canonical source，写入 ARTIFACT_NORMS.md
3. **审查政策**：PR 审查时，检查是否存在跨文档重叠；if yes, request 修复

---

## 参考与关联

- [ARTIFACT_NORMS.md](../ARTIFACT_NORMS.md) - 制品规范和 canonical source 定义
- [audit-docs.md](audit-docs.md) - 整体文档治理报告
- [roadmap.md](../process-management/roadmap.md) - 项目路线图（canonical）
- [strategic-goals.md](../project-overview/strategic-goals.md) - 战略目标（canonical）

```

---

## 质量指标 (Quality Metrics)

- **准确度**：检测到的重叠通过人工抽查验证，误差率 <5%
- **覆盖率**：扫描 100% 的 .md 文件，检测所有 >30% 重叠
- **可操作性**：每条修复建议明确涉及的文件、改动行数、执行步骤
- **执行效率**：所有 P0 级修复可在 <2 小时内完成；P1 在 <1 day 内完成

---

## 实现笔记 (Implementation Notes)

### 语义相似度检测算法

1. **标题匹配**：完全相同的标题 → 100% 重叠
2. **表格匹配**：相同列头 + 行内容 >N% 相同 → 重叠率 N%
3. **列表匹配**：列表项完全相同的比例 → 重叠率
4. **段落关键词**：提取名词、动词、关键数字；相同关键词 >5 个 → 候选重叠（需人工验证或增强）

### 可扩展性

- 可支持不同语言的文档（通过 front-matter 或配置）
- 可支持自定义的 artifact_type 和 canonical source 定义
- 可集成到 CI/CD 管道中，作为 PR 合并前的自动检查

### 与其他技能的集成

- **discover-docs-norms**：从规范读取 canonical source 定义
- **audit-docs**：在统一报告中嵌入 SSOT 审计结果
- **tidy-repo**：可扩展以支持跨文档重叠检测
- **commit-work**：将修复建议转为可提交的 git commit

---

## 限制 (Limitations)

- **语言限制**：目前支持中文和英文文档；其他语言需配置
- **格式限制**：仅检测 Markdown 格式的文档（.md）；其他格式（.txt, .rst）不支持
- **语义限制**：基于关键词匹配和结构相似度；无法感知自然语言的深层语义（如"里程碑"与"checkpoint"的等价性）
- **性能限制**：大型项目（>1000 个 .md 文件）的全量扫描可能耗时 >1 小时

---

## 反馈与改进

如发现以下情况，请反馈：
- 误报（报告了不存在的重叠）
- 漏报（未检测到的实际重叠）
- 修复建议不可操作（步骤不清晰或有遗漏）
- 性能问题（扫描耗时过长）
