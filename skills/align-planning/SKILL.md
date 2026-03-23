---
name: align-planning
description: Perform post-task traceback, drift detection, and top-down recalibration to keep planning (goals, requirements, milestones, roadmap) aligned with task execution.
description_zh: 执行任务后追溯、漂移检测与自上而下校准，使规划（目标、需求、里程碑、路线图）与执行对齐。
tags: [workflow, documentation]
version: 1.3.0
license: MIT
recommended_scope: both
metadata:
  author: ai-cortex
  evolution:
    sources:
      - name: "analyze-requirements"
        repo: "https://github.com/nesnilnehc/ai-cortex"
        version: "1.0.0"
        license: "MIT"
        type: "reference"
        borrowed: "State-based validation style, handoff boundaries, structured self-check"
      - name: "design-solution"
        repo: "https://github.com/nesnilnehc/ai-cortex"
        version: "1.0.0"
        license: "MIT"
        type: "reference"
        borrowed: "Phase-based process, alternatives framing, output artifact discipline"
    enhancements:
      - "Added deterministic mode selection (Lightweight vs Full)"
      - "Added four-type planning drift model (goal, requirement, roadmap, priority)"
      - "Added mapping-confirmation gate when traceability links are missing"
      - "v1.1.0: Slimmed to planning layer only; Architecture moved to align-architecture"
      - "Renamed to align-planning for semantic clarity (planning vs implementation)"
      - "v1.2.0: Document structure discovery phase; orchestration guidance with align-architecture"
triggers: [alignment, planning alignment, align planning, post task]
input_schema:
  type: free-form
  description: Completed task context, optional project docs root, optional mode and path mapping
  defaults:
    mode: lightweight
output_schema:
  type: document-artifact
  description: Planning Alignment Report written to docs/calibration/planning-alignment.md (default)
  artifact_type: planning-alignment
  path_pattern: docs/calibration/planning-alignment.md
  lifecycle: living
---

#技能（Skill）：协调规划

## 目的 (Purpose)

通过运行任务后调整循环，使项目执行与更高级别的规划保持一致：从已完成的工作回溯到策略、检测偏差并生成自上而下的重新校准建议。

---

## 核心目标（Core Objective）

**首要目标**：任务完成后生成一份可操作的规划调整报告，其中包含明确的偏差分类和优先的重新校准行动。

**成功标准**（必须满足所有要求）：

1. ✅ **追踪已完成**：通过所选模式的适用项目层追踪已完成的任务
2. ✅ **漂移分类**：所有检测到的偏差都使用规划漂移模型（目标、要求、路线图、优先级），每个项目都有影响范围和根本原因
3. ✅ **生成校准**：提供自上而下的重新校准建议列表，包括后续任务
4. ✅ **报告持久化**：规划对齐报告写入商定的路径
5. ✅ **评估证据准备情况**：对缺失或薄弱的文档进行明确评分并反映在置信度中
6. ✅ **避免不安全写入**：如果映射不确定或更新具有破坏性，则在提出文件级更改之前请求用户确认

**验收**测试：队友能否阅读报告并立即了解计划是否仍与执行保持一致、存在哪些偏差、下一步做什么以及为什么？

---

## 范围边界（范围边界）

**本技能负责**：

- 任务后调整评估
- 跨项目层的自下而上追溯
- 漂移检测、影响分析和根本原因标记
- 自上而下的重新校准建议
- 带有优先级提示的下一个任务建议
- 规划文档不完整时的证据准备评估和优雅降级

**本技能不负责**：

- 从头开始重写需求（使用“分析需求”）
- 重新设计架构（使用“设计解决方案”）
- 架构与代码合规性（使用“align-architecture”）
- 从头开始创建新的路线图或里程碑系统
- 实施代码更改
- 团队回顾促进（“哪些进展顺利/哪些进展不佳”）

**转交点**：报告制作和审核后，按问题类型（需求、架构设计、规划、架构合规性或修复循环）移交给相关技能。

---

## 使用场景（用例）

- **任务后检查点**：在完成任何任务后验证对齐情况
- **里程碑关闭审查**：在标记里程碑完成之前运行完全对齐
- **发布准备**：在发布削减之前检测计划偏差
- **范围转移诊断**：调查最近的工作是否仍然支持当前目标
- **待办事项重新排序输入**：生成有证据支持的下一个任务排序信号

---

## 编排指导

|场景|推荐顺序|
| ---| ---|
|日常任务完成 | `align-planning`（轻量级）|
|里程碑或释放门| `align-planning`（完整）→ 然后`align-architecture` |
|规划漂移疑似| `对齐规划` |
|需要设计与代码合规性| `align-architecture` （当规划也有问题时，在 `align-planning` 之后运行） |

当规划层对齐不确定时，先运行“align-planning”；在计划架构与代码验证的对齐之后运行“align-architecture”。

---

## 行为（行为）

### 代理即时合同

在执行开始时，遵循以下指令合同：


```text
You are responsible for planning alignment.

When a task is completed, perform traceback analysis to ensure planning
(goals, requirements, milestones, roadmap) is aligned with execution,
and produce a structured Planning Alignment Report.
```


### 交互（互动）政策

- **默认**：来自上下文的模式（`轻量级`，除非发布/里程碑/史诗）；工作区中的文档根目录
- **选择选项**：当用户喜欢时模式覆盖“[轻量级][完整]”
- **确认**：在文件级更改建议之前；当映射不确定时继续之前 (NeedsMappingConfirmation)

### 第 0 阶段：模式和上下文解析

1. 具有确定性策略的解决模式：
   - 如果用户明确设置模式，则使用它
   - 否则，如果上下文包含“release”、“里程碑关闭”或“epic-done”，则使用 **完全对齐模式**
   - 否则使用**轻量级模式**
2.解析文档路径：
   - 默认映射采用项目-文档-模板布局
   - 如果提供，应用用户路径映射覆盖
   - **可选发现**：如果用户未提供路径映射且默认布局不匹配，请运行文档结构发现（例如在存储库根目录扫描`docs/`、`docs/需求/`、`docs/路线图*`、`*.md`）或建议`discover-docs-norms`来建立路径；报告假定的映射，如果不明确则要求确认
3. 确认最低限度的上下文：
   - 已完成任务总结
   - 至少一个追踪锚点（需求 ID、路线图项、里程碑参考或同等内容）

### 阶段 0.5：证据准备情况评估

在回溯之前评估证据质量：

- **强**：所选模式下所有必需的图层都存在规范文档
- **弱**：存在部分文档，但至少一个必需的层依赖于辅助证据（问题/PR/提交说明）
- **缺失**：关键层不可用；回溯无法产生可靠的漂移类型

规则：

1. 丢失的文档不得默默地通过对齐。
2. 仅当规范文档缺失时才使用辅助证据，并明确标记。
3.结论的置信度必须根据准备程度进行调整：
   - `强` -> 高置信度
   - `弱` -> 中等置信度
   - `失踪` -> 低信心或被阻止

### 模式定义

- **轻量级模式**：任务积压→路线图→要求
- **完全对齐模式**：任务积压→路线图→里程碑→要求→项目目标

该技能仅涵盖**规划层**。架构与代码合规性由“align-architecture”处理。

### 第 1 阶段：回溯（自下而上）

1. 确定已完成的任务意图、输出和目标结果
2. 向上遍历选定的层并记录每层的对齐状态：
   - `对齐` | `部分` | `错位` | `未知`
3. 获取每种状态的支持证据
4. 如果缺少关键映射，请输入“NeedsMappingConfirmation”：
   - 列出缺失的链接
   - 提供 1-3 个候选映射并说明理由
   - 在继续之前请求用户确认
   - 如果未解决，则输出具有所需最少输入的阻止报告
5. 如果准备情况为“弱”或“缺失”，请注释每层证据来源：
   - `canonical`（项目文档）
   - `次要`（问题/PR/提交上下文）
   - `无`

### 第 2 阶段：漂移检测

将每个漂移项分类为（仅限规划层）：

- **目标漂移**：工作不再支持当前的项目目标
- **需求漂移**：需求已更改、已弃用或已被取代
- **路线图漂移**：排序或路线图假设发生变化
- **优先级漂移**：相对于当前业务方向，优先级已经过时

对于实现与设计的偏差，请交给“align-architecture”。

对于每个项目，输出：

- `类型`
- `影响范围`
-“根本原因”
-“严重性”（“低”|“中”|“高”）

### 第 3 阶段：校准（自上而下）

1.从顶层向下重新推导优先级（目标→要求→里程碑→路线图→待办事项）
2. 产生重新校准动作：
   - 优先级调整
   - 顺序变化
   - 依赖性修正
   - 转交后续分析
3. 推荐接下来的任务，并给出理由和紧急程度
4. 如果建议对规范规划文档进行编辑，请在生成文件级变更建议之前请求明确确认

### 第 4 阶段：坚持报告

将报告写至：

- 从项目规范解析的路径（`docs/ARTIFACT_NORMS.md` 或 `.ai-cortex/artifact-norms.yaml`）
- 默认：`docs/calibration/planning-alignment.md`（除非明确请求快照，否则覆盖）
- 或者用户指定的路径

除了人类可读的部分之外，报告还必须包含机器可读的漂移块（YAML 或 JSON）。
报告还必须包括证据准备块和明确的置信度。

---

## 输入与输出 (Input & Output)

### 输入（输入）

- 完成的任务描述和结果
- 可选模式覆盖（“轻量级”|“完整”）
- 可选的文档根/路径映射
- 可选上下文：发布/里程碑/史诗标记

### 输出（输出）

#### 规划调整报告模板


```markdown
# Planning Alignment Report: <task title>

**Date:** YYYY-MM-DD
**Mode:** Lightweight | Full
**Status:** aligned | partial | misaligned | blocked
**Confidence:** high | medium | low

## Completed Task
- Summary:
- Outcome:

## Traceback Path
Task Backlog -> Roadmap -> Milestones -> Requirements -> Project Goals

## Evidence Readiness
- Readiness: strong | weak | missing
- Missing Layers:
- Secondary Sources Used:

## Alignment Status
- Goal Alignment:
- Requirement Alignment:
- Milestone Alignment:
- Roadmap Alignment:

## Drift Detected
- Type:
  Impact Scope:
  Root Cause:
  Severity:

## Impact Analysis
- Delivery impact:
- Technical impact:
- Planning impact:

## Calibration Suggestions
1.
2.
3.

## Recommended Next Tasks
1.
2.
3.

## Machine-Readable Drift

    drifts:
      - driftType: "Requirement Drift"
        severity: "medium"
        owner: "product-team"
        dueWindow: "next-sprint"
        impactScope: "Search filter acceptance criteria"
        rootCause: "Requirement updated to include keyboard navigation; task covered only click interactions"
    evidence:
      readiness: "weak"
      confidence: "medium"
      missingLayers:
        - "docs/requirements-planning/search-improvements.md"
      secondarySources:
        - "PR#142"
        - "commit:abc1234"

```


---

## 限制（限制）

### 硬边界（Hard Boundaries）

- 当证据缺失时，不要发明可追溯性链接
- 当准备状态“薄弱”或“缺失”时，请勿声称高度自信
- 未经用户明确批准，请勿悄悄修改规划真实来源（目标、需求、里程碑、路线图）
- 不要将漂移类别折叠到通用的“错位”桶中；保留输入的漂移输出（目标、要求、路线图、优先级）
- 不要在完整模式下跳过图层检查，除非该图层确实不可用（标记为“未知”并解释）
- 如果没有与追溯证据相关的理由，请勿提出建议

### 技能边界 (Skill Boundaries)（避免重叠）

**不要做这些（其他技能可以处理它们）**：

- 需求重新定义工作流程→`分析需求`
- 架构选项设计工作流程→`设计解决方案`
- 存储库级入门 → `review-codebase`、`generate-standard-readme`、`generate-agent-entry` （根据需要按顺序运行）
- 自动测试和修复循环执行 → `run-repair-loop`

**何时停止并交接**：

- 要求无效或矛盾 → 移交给“分析需求”
- 架构设计冲突是主要障碍→移交给“设计解决方案”
- 需要进行架构与代码合规性检查 → 移交给“align-architecture”
- 报告表明需要修复的主动实施缺陷 → 建议“运行修复循环”

---

## 自检（Self-Check）

### 核心成功标准（必须满足所有标准）

- [ ] 所选模式的回溯已完成
- [ ] 使用四类规划模型键入的漂移项目
- [ ] 每个漂移都有影响范围和根本原因
- [ ] 提供自上而下的校准操作
- [ ] 报告坚持约定的路径
- [ ] 明确报告证据准备水平和置信度
- [ ] 在映射或写入安全不确定的情况下请求确认

### 流程质量检查

- [ ] 模式选择遵循确定性策略
- [ ] 映射不确定性触发了“NeedsMappingConfirmation”
- [ ] 规范证据与次要证据明显分开
- [ ] 每个对齐状态都有证据参考
- [ ] 建议具有优先顺序且有时限
- [ ] 需要时可以明确地移交相邻技能

### 验收测试

**团队成员是否可以在不进行额外说明的情况下执行最重要的 1-3 个建议，并解释为什么它们具有最高优先级？**

如果否：报告不完整；完善追溯证据和重新校准细节。

如果是：报告完成；继续进行转交或执行计划。

---

## 示例（示例）

### 示例1：轻量级模式（常规任务）

**上下文**：已完成的任务更新搜索过滤器 UI 行为。

**模式分辨率**：没有显式覆盖，没有发布/里程碑/史诗标记 → 轻量级。

**回溯**：

- 任务与路线图项目“search-improvements-q2”一致
- 要求仍然有效，但接受标准上周发生了变化
- 证据准备度“强”，因为要求和路线图文档都是规范且最新的

**漂移**：

-“需求漂移”（中）：需求措辞更改为包括键盘导航；已完成的任务仅涵盖点击交互

**校准**：

1.添加键盘导航后续任务
2. 在合并相关 UI 任务之前移动可访问性验收检查
3. 重新排序待办项目以解锁回归测试

### 示例 2：完整模式（里程碑关闭）

**上下文**：API 网关身份验证推出后标记为“里程碑关闭”的里程碑。

**模式分辨率**：标记命中 → 完全。

**回溯**：

- 路线图和里程碑映射有效
- 目标和需求仍然有效
- 证据准备度“强”；所有规划层都存在规范文档

**漂移**：

- `优先级漂移`（高）：待办中未促进迁移工作

**校准**：

1. 将迁移史诗插入当前的冲刺计划中
2. 推迟非关键网关增强功能
3. 建议运行 `align-architecture` 进行架构与代码合规性检查

### 示例 3：边缘情况（阻塞映射）

**上下文**：已完成的任务没有要求 ID 或路线图链接。

**行为**：

1. 输入“NeedsMappingConfirmation”
2. 提供带有置信度注释的候选映射
3. 在漂移分类之前要求用户确认映射

**结果**：

- 如果用户确认：继续正常流程
- 如果未确认：输出带有缺失字段清单的“阻止”报告
- 在建立规范映射之前，置信度保持“低”