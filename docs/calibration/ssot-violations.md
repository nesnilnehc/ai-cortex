# 单一事实源（SSOT）检测报告

**生成时间**：2026-03-24 14:30:00
**扫描范围**：docs/ 下所有 .md 文件
**扫描文件总数**：45 个
**检测到的重叠对数**：7 条

---

## 第 1 节：SSOT 规范定义

### 定义的 Canonical Sources

根据 ARTIFACT_NORMS.md 和项目文档结构，以下为各制品类型的权威来源：

| Artifact Type | Canonical Source | 备注 | 权威性 |
| :--- | :--- | :--- | :--- |
| **roadmap** | `docs/process-management/roadmap.md` | 项目路线图和里程碑的唯一权威来源；包含 Now/Next/Later 三个阶段 | ★★★ 强制 |
| **milestones** | `docs/process-management/roadmap.md` | 里程碑详情嵌入 roadmap 中，不应在其他文档中重复定义 | ★★★ 强制 |
| **strategic-goals** | `docs/project-overview/strategic-goals.md` | 4 个战略目标的唯一权威来源 | ★★★ 强制 |
| **requirements** | `docs/requirements-planning/{topic}.md` | 各主题需求的权威来源；应单向引用，不应在其他文档重复 | ★★ 重要 |
| **backlog-item** | `docs/process-management/backlog.md`（索引）+ `backlog/YYYY-MM-DD-*.md` | 工作条目的权威来源；backlog.md 是索引，具体条目在独立文件 | ★★ 重要 |
| **adr** | `docs/process-management/decisions/YYYYMMDD-*.md` | 架构决策的权威来源 | ★★ 重要 |
| **design** | `docs/designs/YYYY-MM-DD-*.md` | 设计文档的权威来源 | ★★ 重要 |
| **promotion-tasks** | `docs/process-management/promotion-iteration-tasks.md` | 发版和迭代任务的权威来源 | ★ 参考 |

### 合规引用规则

| 引用类型 | 定义 | 重叠率 | 合规性 |
| :--- | :--- | :--- | :--- |
| **纯链接** | 引用文档仅包含指向 canonical source 的链接，无内容重复 | <5% | ✅ **完全合规** |
| **摘要+链接** | 引用文档包含原内容的 20-30% 摘要，加标注链接指向 canonical source | 20-30% | ✅ **合规** |
| **合理引用** | 不同 artifact_type 之间的交叉引用，符合信息层次 | <50% | ✅ **通常合规** |
| **部分复写** | 包含 30-60% 的重复内容，但有明确上下文差异和补充信息 | 30-60% | ⚠️ **需改进** |
| **完全复写** | 重复内容 >60%，无上下文差异、无链接、无说明 | >60% | ❌ **违规** |
| **多源冲突** | 多个文档作为权威来源定义相同概念，造成信息不一致 | N/A | ❌ **严重违规** |

---

## 第 2 节：冲突矩阵

### 所有检测到的重叠（按优先级和重叠率排列）

#### P0 级别（严重 - 权威冲突）

| # | 文档 A (canonical) | 文档 B (源) | 重叠类型 | 重叠率 | 重叠内容摘要 | 建议保留源 | 修复动作 | 优先级 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **1** | `roadmap.md` | `designs/2026-03-02-ai-cortex-evolution-roadmap.md` | 多源冲突 | 42% | 里程碑 M5/M6/M7 定义、阶段划分（Now/Next/Later） | roadmap.md | 重构设计文档为架构聚焦，里程碑信息链接到 roadmap | **P0** |
| **2** | `strategic-goals.md` | `designs/2026-03-02-ai-cortex-evolution-roadmap.md` | 多源冲突 | 38% | 目标 1-4 的中文定义和说明 | strategic-goals.md | 在设计文档中用英文抽象目标，添加指向 strategic-goals.md 的链接 | **P0** |

#### P1 级别（重要 - 信息冗余）

| # | 文档 A | 文档 B | 重叠类型 | 重叠率 | 重叠内容摘要 | 建议保留源 | 修复动作 | 优先级 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **3** | `roadmap.md` | `decisions/20260322-strategic-goals-milestones-framing.md` | 部分重叠 | 35% | 里程碑定义、阶段语义、目标关系 | roadmap.md | 优化决策文档重点为"阶段与目标关系定义"，具体里程碑内容改为摘要+链接 | **P1** |
| **4** | `strategic-goals.md` | `decisions/20260322-strategic-goals-milestones-framing.md` | 部分重叠 | 28% | 目标的基本定义（4 个目标）和阶段概念 | strategic-goals.md | 在决策文档中简化目标定义，强化"层次与关系"的核心贡献 | **P1** |
| **5** | `backlog.md` | `promotion-iteration-tasks.md` | 部分重叠 | 32% | Epic T1-T5 的重复定义、任务范围 | backlog.md | backlog.md 作为索引，promotion-iteration-tasks.md 作为执行详情；两者应明确关系，避免同步困难 | **P1** |

#### P2 级别（轻微 - 链接/摘要不足）

| # | 文档 A | 文档 B | 重叠类型 | 重叠率 | 重叠内容摘要 | 建议保留源 | 修复动作 | 优先级 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **6** | `strategic-goals.md` | `roadmap.md` | 合理引用 | 15% | 目标与 Now/Next 的映射关系 | strategic-goals.md | 补充 roadmap.md 中的链接说明：该阶段支撑哪些战略目标 | **P2** |
| **7** | `promotion-iteration-tasks.md` | `designs/2026-03-06-promotion-and-iteration.md` | 合理引用 | 25% | Epic 定义、验收标准、质量门禁 | designs/.../promotion-and-iteration.md | 在 promotion-iteration-tasks.md 开头增加清晰的关系说明：本文是执行计划，设计文档见... | **P2** |

---

## 第 3 节：修复路线图

### 执行顺序与依赖

```
┌─ P0.1：设计文档重构（里程碑和目标）
│         ↓
├─ P0.2：补充规范定义（canonical source）
│         ↓ (阻塞 P1 的所有项)
│
├─ P1.1：决策文档优化
├─ P1.2：Backlog 与任务文档关系澄清
│         ↓
└─ P2：链接与摘要补充（非阻塞）
```

**关键路径**：P0.1 → P0.2 → P1.1、P1.2 → P2
**并行处理**：P1.1 和 P1.2 可并行执行
**预计总耗时**：P0 (4-6 小时) + P1 (2-3 小时) + P2 (1-2 小时) = 7-11 小时

---

### 详细修复方案

#### **P0.1：重构 designs/2026-03-02-ai-cortex-evolution-roadmap.md**

**问题描述**

该设计文档与 `roadmap.md` 重复定义了里程碑（M5、M6、M7）和阶段划分（Now/Next/Later），造成 **双源冲突**。同时与 `strategic-goals.md` 重复定义了 4 个战略目标，造成权威性模糊。

**证据**

| 文档 | 位置 | 内容 |
| --- | --- | --- |
| `roadmap.md` | 第 15-25 行 | 完整定义：M5 核心意图覆盖、M6 生态多渠道验证、M7 复杂编排与工作流闭环 |
| `evolution-roadmap.md` | 第 26-35 行 | 相同的里程碑定义（略有表述差异） |
| `strategic-goals.md` | 第 9-24 行 | 4 个目标：交付链可获得、治理链可获得、复用与编排、采纳摩擦低 |
| `evolution-roadmap.md` | 第 8-23 行 | 目标字段（英文，但对应相同概念） |

**受影响文件**

- `docs/designs/2026-03-02-ai-cortex-evolution-roadmap.md`（需修改）
- `docs/process-management/roadmap.md`（canonical，无需改动）
- `docs/project-overview/strategic-goals.md`（canonical，无需改动）

**修复步骤**

1. **打开** `docs/designs/2026-03-02-ai-cortex-evolution-roadmap.md`

2. **删除重复的"目标"部分**（第 8-23 行）

   **修改前**：
   ```markdown
   ## 目标

   定义 AI Cortex 在 v2.0.0 之后的演进与优化方向，覆盖工程基础设施、技能覆盖、编排、生态与规范成熟度。
   ```

   **修改后**：
   ```markdown
   ## 目标

   支撑 [4 个战略目标](../../project-overview/strategic-goals.md) 在工程基础设施、技能覆盖、编排、生态与规范成熟度四个维度的实现路径。

   本文档关注**架构与分层**（Layer A-E），具体里程碑与阶段定义见 [roadmap.md](../roadmap.md)。
   ```

3. **删除重复的"里程碑"定义**（需要检查是否有 M5、M6、M7 的完整定义，如有则删除）

   **替代内容**：
   ```markdown
   ### 里程碑与阶段

   演进路线图关联以下阶段（详见 [roadmap.md](../roadmap.md#里程碑详情附录)）：

   - **Now 阶段**：M5（核心意图覆盖）、M6（生态多渠道验证）
   - **Next 阶段**：M7（复杂编排与工作流闭环）
   - **Later 阶段**：可观测性构建、社区标准化

   本文档的 5 层架构设计（A-E）为这些里程碑提供技术基础。
   ```

4. **保留此文档的独特价值**：
   - Layer A-E 的架构分层（这是设计文档的核心贡献）
   - 阶段依赖关系和 trade-off 分析
   - 替代方案评估

5. **在"背景"部分增加关系说明**（第 12-22 行后插入）：

   ```markdown
   **文档关系**：
   - [strategic-goals.md](../../project-overview/strategic-goals.md)：4 个战略目标（权威定义）
   - [roadmap.md](../roadmap.md)：里程碑与阶段计划（权威定义）
   - 本文档：支撑路线图的架构与技术分层
   ```

**验证方法**

运行修复后的检测：
```bash
detect-ssot-violations --types roadmap,strategic-goals \
                       --min-overlap 0.4
```

预期结果：`evolution-roadmap.md` 与 `roadmap.md` 的重叠率降至 <20%

**预计改动**

| 指标 | 数值 |
| --- | --- |
| 修改的文件数 | 1 个 |
| 删除行数 | ~15-20 行 |
| 新增行数 | ~8-10 行 |
| 净改动 | -5 到 -10 行 |

**风险分析**

| 风险 | 可能性 | 影响 | 缓解方案 |
| --- | --- | --- | --- |
| 设计文档失去里程碑上下文 | 低 | 读者需跳转到 roadmap.md | 添加清晰的链接和段落说明 |
| 重构后内容过于精简 | 极低 | 设计架构的表达力降低 | 强化 Layer A-E 的说明，补充 trade-off 分析 |
| 其他文档引用失效 | 低 | 交叉引用链接断裂 | 检查引用，修正链接或内容 |

**示例修复前后对比**

**修复前** (重复内容过多)：
```markdown
## 组件

### A1. CI/CD 自动化

**推荐方案**：最小化 GitHub Actions + 自用 (Dogfooding)

- PR 触发：运行 `verify-registry.mjs` 校验 registry 同步
- main 分支合并：触发 ASQM 审计检查
- 使用项目自身的 `generate-github-workflow` 技能生成初始 workflow

| Alternative | Pros | Cons | Best for |
| **A: Minimal CI + Dogfood (recommended)** | Dogfoods own assets; low maintenance | Limited CI value for pure-Markdown project | Current stage |
| B: Extended CI + Spec compliance | Also solves E12 (spec testing) | Higher dev effort | Governance-focused stage |
| C: CI + Release automation | Full release pipeline | Over-engineering | Community-ready stage |
```

**修复后** (保留架构价值，移除重复的里程碑定义)：
```markdown
## 组件

本节定义 5 层架构模型及其在 Now/Next/Later 阶段的实现优先级。
具体里程碑（M5-M7）见 [roadmap.md](../roadmap.md)。

### Layer A: Engineering Infrastructure

**目标**：建立自动化质量门槛和发版流程。

#### A1. CI/CD 自动化

**推荐方案**：最小化 GitHub Actions + 自用 (Dogfooding)
- PR 触发：运行 `verify-registry.mjs` 校验...
- [更多细节](../roadmap.md#里程碑详情附录)
```

---

#### **P0.2：明确 ARTIFACT_NORMS.md 中的 Canonical Sources**

**问题描述**

当前 `ARTIFACT_NORMS.md` 定义了 artifact_type 和路径规则，但未明确说明各类型的 **canonical source**（权威来源）。这导致多个文档可能都声称自己是权威来源，造成 SSOT 原则难以执行。

**修复步骤**

1. **打开** `docs/ARTIFACT_NORMS.md`

2. **在制品规范表之前增加章节** "Canonical Source Definition"：

   ```markdown
   ## Canonical Source Definition

   本项目为各类制品定义唯一的权威来源。所有其他文档在涉及同类信息时，应采用"引用+补充"而非"复写"的方式。

   | Artifact Type | Canonical Source | 规则 |
   | :--- | :--- | :--- |
   | roadmap | `docs/process-management/roadmap.md` | 里程碑与路线图的权威定义；其他文档不应独立重定义里程碑 |
   | strategic-goals | `docs/project-overview/strategic-goals.md` | 战略目标的权威定义；其他文档应用链接+摘要引用 |
   | requirements | `docs/requirements-planning/{topic}.md` | 各主题需求的权威定义 |
   | backlog-item | `docs/process-management/backlog/{file}` | 工作条目的权威定义；backlog.md 作为索引 |
   | adr | `docs/process-management/decisions/YYYYMMDD-{slug}.md` | 架构决策的权威定义 |
   | design | `docs/designs/YYYY-MM-DD-{topic}.md` | 设计文档的权威定义 |

   ### 引用规则

   - **完全引用**：仅包含链接，无重复内容 → ✅ 最佳实践
   - **摘要+链接**：20-30% 摘要 + 链接指向权威源 → ✅ 合规
   - **完全复写**（>60% 重叠）→ ❌ 违规，需优化为摘要形式

   ### 多源协作

   不同 artifact_type 之间可交叉引用（如 roadmap.md 引用 strategic-goals.md），但应遵循：
   - 清晰标注引用链接
   - 仅引用摘要，不复写完整内容
   - 明确信息的流向（如：roadmap 支撑 strategic-goals，还是相反）
   ```

3. **保存并验证**

**验证方法**

- `detect-ssot-violations` 能准确识别每个 artifact_type 的 canonical source
- 生成报告时能自动检查违规

---

#### **P1.1：优化 decisions/20260322-strategic-goals-milestones-framing.md**

**问题描述**

这份 ADR（架构决策记录）重复定义了战略目标和里程碑的概念，与 `strategic-goals.md` 和 `roadmap.md` 有 35% 和 28% 的内容重叠。

**现状**

| 文档 | 包含内容 |
| --- | --- |
| `20260322-strategic-goals-milestones-framing.md` | 战略目标定义、里程碑定义、两者关系、修订建议 |
| `strategic-goals.md` | 4 个战略目标的完整定义 |
| `roadmap.md` | 里程碑的完整定义 |

**核心价值**

此 ADR 的独特价值在于定义 **"战略目标与里程碑的层次关系"**，而非简单重复两者的定义。应聚焦于：
- 两者的语义边界（目标 vs 里程碑）
- 如何映射（一个目标→多个阶段的多个里程碑）
- 为什么这样分层（支撑持续演进）

**修复步骤**

1. **打开** `docs/process-management/decisions/20260322-strategic-goals-milestones-framing.md`

2. **第 2 节（问题）**：保持不变（这是决策的上下文）

3. **第 2.1 小节（战略目标）**：精简为摘要，加链接

   **修改前**：
   ```markdown
   ### 2.1 战略目标：持续优化的结果愿景，非一次性交付

   **定位**：战略目标描述项目长期追求的**结果状态**...

   - **表述特征**：使用「可获得」「可复用」...
   - **与 North Star 关系**：...
   - **无「完成」概念**：...

   **推论**：目标文档不标注状态；...
   ```

   **修改后**：
   ```markdown
   ### 2.1 战略目标：持续优化的结果愿景

   **定位**：详见 [strategic-goals.md](../../project-overview/strategic-goals.md)

   核心理解：战略目标是**持续演进的方向**，而非有截止期的交付物。

   **设计意义**：允许项目在长期保持方向一致，同时通过里程碑实现分阶段的检查点。
   ```

4. **第 2.2 小节（里程碑）**：精简为摘要，加链接

   **修改前**：
   ```markdown
   ### 2.2 里程碑：分阶段的检查点，非目标本身

   **定位**：里程碑是**阶段检查点**...

   - **阶段性**：...
   - **Done 语义**：...
   - **可持续扩展**：...

   **推论**：...
   ```

   **修改后**：
   ```markdown
   ### 2.2 里程碑：分阶段的检查点

   **定位**：详见 [roadmap.md](../roadmap.md)

   核心理解：里程碑是**有阶段的、可验证的检查点**，而非最终目标。

   **设计意义**：支撑短期的里程碑交付与长期的目标演进并行。
   ```

5. **第 2.3 小节（关系）**：重点保留（这是决策的核心）

   **修改建议**（增强清晰度）：
   ```markdown
   ### 2.3 目标与里程碑的关系

   | 层次 | 含义 | 时间维度 | 示例 |
   | :--- | :--- | :--- | :--- |
   | **战略目标** | 持续追求的结果方向 | 3-5 年+ | 交付链能力可获得 |
   | **里程碑** | 某阶段的可验证检查点 | 3-6 个月 | M5：核心意图覆盖 |
   | **Roadmap** | 有时间维度的计划与举措 | 3-12 个月 | 扩充核心技能库 |

   **映射规则**：
   - 一个目标可对应多个阶段的多个里程碑
   - 一个里程碑通常推进多个目标
   - 里程碑 Done 后，对应的目标仍在演进

   **示例**：
   - 目标 1（交付链可获得）→ M5（覆盖 80% 高频意图）、M6（多渠道验证）、未来的 M8/M9
   - M5 同时推进目标 1 和目标 2（治理链能力）
   ```

6. **第 3 节（对现有文档的修订）**：更新建议

   **修改前**：建议同时修改 strategic-goals.md 和 roadmap.md

   **修改后**：澄清修改方向
   ```markdown
   ### 3. 后续行动

   本决策通过后，以下文档应按以下方式更新：

   1. **strategic-goals.md**（无需改动）：已清晰定义 4 个目标；本决策提供了语义框架
   2. **roadmap.md**（建议补充）：在各阶段的说明中，关联到支撑的战略目标
      - 示例：在"Now 阶段"开头增加："支撑目标 1 和 2..."
   3. **本决策文档（架构化保留）**：作为层次与关系的权威说明，引用其他文档但不重复内容
   ```

7. **保存**

**预计改动**

| 指标 | 数值 |
| --- | --- |
| 修改的文件数 | 1 个 |
| 删除行数 | ~20-25 行（重复定义） |
| 新增行数 | ~5-8 行（链接和补充） |
| 净改动 | -15 到 -20 行 |

**风险**

- **低**：ADR 的核心价值（关系定义）保留了；只是减少了重复的定义部分

---

#### **P1.2：澄清 backlog.md 与 promotion-iteration-tasks.md 的关系**

**问题描述**

两份文档都包含 Epic（T1-T5）的定义和任务描述，有 32% 的内容重叠。不清楚两者的关系：
- `backlog.md` 是索引还是执行计划？
- `promotion-iteration-tasks.md` 是详情还是另外的计划？

**现状**

| 文档 | 内容 | 角色 |
| --- | --- | --- |
| `backlog.md` | Epic 表格（T1-T5）、关联的计划工作 | 索引/导航 |
| `promotion-iteration-tasks.md` | 完整的 Epic 详情、验收标准、质量门禁 | 执行计划 |

**修复步骤**

1. **打开** `docs/process-management/backlog.md`

2. **在"计划工作"表格前增加关系说明**：

   ```markdown
   ## 计划工作（来自设计）

   下表汇总了来自 [推广与迭代设计](../designs/2026-03-06-promotion-and-iteration.md) 的计划 Epic。

   **详细的任务、验收标准、质量门禁请见** [promotion-iteration-tasks.md](promotion-iteration-tasks.md)。

   本表的职责：
   - 提供 Epic 的快速导航
   - 显示与需求和设计文档的追溯关系

   | Epic | Scope | Priority | 详情 |
   | :--- | :--- | :--- | :--- |
   | T1 分发渠道验证 | scripts/verify-* | Phase A | [查看详情](promotion-iteration-tasks.md#t1) |
   | ... | ... | ... | ... |
   ```

3. **打开** `docs/process-management/promotion-iteration-tasks.md`

4. **在开头增加文档关系说明**：

   ```markdown
   # 发版与迭代任务详情

   **相关文档**：
   - [Backlog 索引](backlog.md)：Epic 快速导航
   - [推广与迭代设计](../designs/2026-03-06-promotion-and-iteration.md)：设计决策与背景

   本文档是 Epic T1-T5 的**执行详情**，包含完整的任务定义、验收标准、质量门禁和依赖关系。
   ```

5. **保存**

**预计改动**

| 指标 | 数值 |
| --- | --- |
| 修改的文件数 | 2 个 |
| 新增行数 | ~8-12 行 |

**风险**

- **极低**：仅增加了链接和澄清说明，无删除或修改

---

#### **P2.1：补充 roadmap.md 的战略目标关联**

**问题描述**

`roadmap.md` 中的各个阶段（Now/Next/Later）与战略目标的映射关系不明确。新读者需要自己推断。

**修复步骤**

1. **打开** `docs/process-management/roadmap.md`

2. **在"Now 阶段"开头增加关系说明**：

   **修改前**：
   ```markdown
   ## Now

   ### 里程碑
   ...
   ```

   **修改后**：
   ```markdown
   ## Now

   **支撑的战略目标**：[目标 1（交付链能力可获得）](../../project-overview/strategic-goals.md#目标-1交付链能力可获得) 和 [目标 2（治理链能力可获得）](../../project-overview/strategic-goals.md#目标-2治理链能力可获得)

   **成功标志**：Now 阶段的里程碑达成后，交付与治理的核心意图覆盖率达 80%。

   ### 里程碑
   ...
   ```

3. **在"Next 阶段"开头增加关系说明**：

   ```markdown
   ## Next

   **支撑的战略目标**：[目标 3（能力可跨项目复用与编排）](../../project-overview/strategic-goals.md#目标-3能力可跨项目复用与编排)

   ...
   ```

4. **保存**

**预计改动**

| 指标 | 数值 |
| --- | --- |
| 修改的文件数 | 1 个 |
| 新增行数 | ~6-8 行 |

**风险**

- **极低**：仅增加链接

---

#### **P2.2：改进交叉引用的清晰度**

**问题描述**

多个文档中的链接使用相对路径且未标注链接类型（design/adr/skill）。新贡献者需要逐一点击来判断链接指向什么类型的文档。

**受影响文件**

- `backlog.md`
- `promotion-iteration-tasks.md`
- `roadmap.md`

**修复步骤**（示例以 backlog.md 为例）

1. **打开** `docs/process-management/backlog.md`

2. **为所有链接增加类型标注**：

   **修改前**：
   ```markdown
   | Epic | Scope | Priority |
   | T1 分发渠道验证 | scripts/verify-* | Phase A |
   | T2 发布流程自动化 | pre-release-check、CHANGELOG 辅助 | Phase A/B |
   ```

   **修改后**：
   ```markdown
   | Epic | Scope | Priority |
   | T1 分发渠道验证 | scripts/verify-* | Phase A |
   | T2 发布流程自动化 | pre-release-check、CHANGELOG 辅助 | Phase A/B |

   详见 [发版与迭代任务 (execution-plan)](promotion-iteration-tasks.md)。

   设计背景：[推广与迭代 (design)](../designs/2026-03-06-promotion-and-iteration.md)。
   ```

3. **对其他文档重复类似修改**

**预计改动**

| 指标 | 数值 |
| --- | --- |
| 修改的文件数 | 3-4 个 |
| 新增行数 | ~2-3 行 |

**风险**

- **极低**：仅增加链接文本

---

### 修复检查清单

- [ ] P0.1：设计文档重构完成，验证重叠率 <20%
- [ ] P0.2：ARTIFACT_NORMS.md 中增加 Canonical Source 定义
- [ ] P1.1：ADR 文档精简并链接到权威源
- [ ] P1.2：Backlog 和任务文档的关系澄清
- [ ] P2.1：Roadmap 增加战略目标关联
- [ ] P2.2：所有链接增加类型标注
- [ ] 最终验证：`detect-ssot-violations --min-overlap 0.3` 运行通过

---

## 第 4 节：执行顺序与依赖

### 推荐执行计划

**第一周（P0）**

| Day | 任务 | 关键依赖 | 预计耗时 |
| --- | --- | --- | --- |
| Mon | P0.1：设计文档重构 | 无 | 2-3 h |
| Tue | P0.2：ARTIFACT_NORMS 补充 | P0.1 完成 | 1-2 h |
| Wed | Code Review & Merge | P0.1 & P0.2 | 1 h |

**第二周（P1）**

| Day | 任务 | 关键依赖 | 预计耗时 |
| --- | --- | --- | --- |
| Mon | P1.1：ADR 优化 + P1.2：Backlog 关系澄清（并行） | P0.2 完成 | 1-2 h |
| Tue | Code Review & Merge | P1.1 & P1.2 | 1 h |

**第三周（P2）**

| Day | 任务 | 关键依赖 | 预计耗时 |
| --- | --- | --- | --- |
| Mon-Tue | P2.1、P2.2 并行执行 | P1 完成 | 1-2 h |
| Wed | 最终验证与文档 | 所有修复 | 0.5 h |

**总耗时**：~11-16 小时（在 3 周内完成）

### 跨越性风险

1. **P0.1 重构失败**：设计文档架构价值丧失
   - 缓解：保留 Layer A-E，仅删除重复的里程碑定义

2. **链接断裂**：其他文档引用失效
   - 缓解：修改后立即验证所有链接

---

## 第 5 节：统计与趋势

### 检测统计

| 指标 | 数值 |
| --- | --- |
| 扫描的文档总数 | 45 个 .md 文件 |
| 检测到的重叠对数 | 7 条 |
| 平均重叠率 | 32.4% |
| 最高重叠率 | 42%（roadmap.md ↔ evolution-roadmap.md） |
| 最低重叠率 | 15%（strategic-goals.md ↔ roadmap.md） |

### 问题分布

| 严重级别 | 数量 | 占比 | 处理方式 |
| --- | --- | --- | --- |
| **P0（权威冲突）** | 2 | 28.6% | 立即修复（阻塞其他工作） |
| **P1（信息冗余）** | 3 | 42.9% | 本周内修复 |
| **P2（轻微优化）** | 2 | 28.6% | 可下月处理 |

### 类型分析

| 重叠类型 | 数量 | 典型原因 | 解决方案 |
| --- | --- | --- | --- |
| **多源冲突** | 2 | 两个文档都尝试定义相同概念 | 选择 canonical，其他链接 |
| **部分重叠** | 3 | 不同文档独立引用相同信息 | 建立清晰的主仆关系 |
| **合理引用** | 2 | 文档间有信息流但形式不同 | 补充链接和摘要 |

### SSOT 成熟度评分

| 维度 | 得分 | 说明 |
| --- | --- | --- |
| **权威源识别** | 7/10 | 大多数 artifact_type 有明确的 canonical source，但规范中未明确定义 |
| **引用规范遵循** | 6/10 | 存在复写现象，但大多数是可修复的部分重叠 |
| **链接完整性** | 8/10 | 大多数文档间有链接，但缺少类型标注 |
| **策略一致性** | 5/10 | 尚无统一的 SSOT 策略文档；各文档独立为政 |
| **总体成熟度** | 6.5/10 | **良好基础，需要规范强化** |

---

## 第 6 节：后续建议与长期规划

### 短期建议（1 个月内）

1. ✅ **执行 P0 和 P1 修复**（本报告的主要内容）
2. ✅ **在 ARTIFACT_NORMS.md 中强化 Canonical Source 定义**
3. ✅ **建立 SSOT 审查清单**：PR 审查时检查是否引入新的重叠

### 中期建议（1-3 个月）

1. **自动化 SSOT 检测**
   - 在 CI/CD 中集成 `detect-ssot-violations`
   - PR 合并前自动扫描新增文档
   - 重叠率 >50% 时 WARN，>70% 时 FAIL

2. **建立跨文档引用规范**
   - 所有引用必须包含：链接、摘要比例、来源说明
   - 示例：`详见 [roadmap.md 里程碑章节](../roadmap.md#里程碑详情附录)，支撑目标 1 和 2。`

3. **建立 Canonical Source 维护清单**
   - 按季度审查各 canonical source 的完整性
   - 检查是否有新兴的、尚未纳入规范的 artifact_type

### 长期建议（3-6 个月）

1. **发展多层次的文档架构**
   - Layer 1（Canonical）：权威定义（strategic-goals.md、roadmap.md、requirements/）
   - Layer 2（Reference）：引用与补充（设计、ADR、决策）
   - Layer 3（Context）：背景与支撑（日志、日记、临时笔记）

2. **建立版本化的 SSOT 规范**
   - 作为独立的 spec 演化
   - 示例：`spec/ssot.md`，与 `spec/skill.md` 平行

3. **扩展 SSOT 检测到代码层面**
   - 检测代码文档与源代码的同步问题
   - 示例：README 中列举的特性是否在代码中真实存在

---

## 第 7 节：关联文档

- 📄 [ARTIFACT_NORMS.md](../ARTIFACT_NORMS.md) - 制品规范（待扩展）
- 📄 [audit-docs.md](audit-docs.md) - 整体文档治理报告
- 📄 [roadmap.md](../process-management/roadmap.md) - 项目路线图（canonical）
- 📄 [strategic-goals.md](../project-overview/strategic-goals.md) - 战略目标（canonical）
- 📄 [backlog.md](../process-management/backlog.md) - 工作条目索引
- 📄 [promotion-iteration-tasks.md](../process-management/promotion-iteration-tasks.md) - 发版任务详情
- 📄 [decisions/20260322-strategic-goals-milestones-framing.md](../process-management/decisions/20260322-strategic-goals-milestones-framing.md) - ADR（待优化）

---

## 附录：SSOT 原则总结

### "Single Source of Truth"（单一事实源）的含义

对于每一类信息（如"里程碑的定义""战略目标""需求"），存在**唯一的权威来源**。其他文档不应独立重复该信息，而应通过以下方式引用：

1. **纯链接**：`详见 [权威源](link)`
2. **摘要+链接**：概述要点（20-30% 原文）+ 链接
3. **衍生信息**：基于权威源的补充分析或上下文

### 为什么需要 SSOT？

| 问题 | 没有 SSOT | 有 SSOT |
| --- | --- | --- |
| 信息不一致 | ❌ 可能在不同文档中看到矛盾的定义 | ✅ 唯一的权威定义 |
| 维护成本 | ❌ 修改一处信息时需要更新所有副本 | ✅ 仅需更新权威源 |
| 新人入门 | ❌ 难以判断哪个来源最可信 | ✅ 清晰的权威指向 |
| 版本控制 | ❌ 历史中多个副本，难以追踪变化 | ✅ 单一 diff 历史 |

### SSOT vs. 信息复用的平衡

- **适当的信息复用**：摘要 + 链接（合规）
- **不适当的复制粘贴**：完整复写，无链接（违规）
- **灵活的衍生**：基于权威源的分析、聚合、补充（通常合规）

