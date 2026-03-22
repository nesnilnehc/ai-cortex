---
name: align-architecture
description: Verify architecture and design documents against code implementation; produce an Architecture Compliance Report when implementation diverges from ADR or design decisions.
description_zh: 对照代码实现验证架构与设计文档；当实现偏离 ADR 或设计时，产出架构合规报告。
tags: [workflow, documentation]
version: 1.2.0
license: MIT
recommended_scope: project
metadata:
  author: ai-cortex
  evolution:
    sources:
      - name: "align-execution"
        repo: "nesnilnehc/ai-cortex"
        version: "1.0.0"
        license: "MIT"
        type: "reference"
        borrowed: "Drift model, traceback pattern, report template structure"
    enhancements:
      - "Split from align-execution (renamed align-planning) per planning vs implementation boundary; focuses on design vs code compliance"
      - "v1.1.0: Partial verification when only some modules have design docs; evidence readiness; orchestration guidance; remediation clarity for outdated design"
triggers: [align architecture, architecture compliance, design vs code, post implementation, post merge]
input_schema:
  type: free-form
  description: ADR or design doc scope, optional code scope (full repo, paths, or modules for incremental verification), optional project docs root
output_schema:
  type: document-artifact
  description: Architecture Compliance Report written to docs/calibration/architecture-compliance.md (default)
  artifact_type: architecture-compliance
  path_pattern: docs/calibration/architecture-compliance.md
  lifecycle: living
---

# 技能（Skill）：对齐架构

## 目的 (Purpose)

验证代码实现是否与 ADR、设计文档或架构规范中记录的架构和设计决策保持一致。当实施偏离记录的决策时，生成架构合规性报告。

---

## 核心目标（Core Objective）

**治理目标**：生成一份可操作的架构合规性报告，将文档化的架构/设计决策与当前实施进行比较，并列出合规性差距以及影响和补救建议。

**成功标准**（必须满足所有要求）：

1. ✅ **确定设计来源**：找到并解析 ADR、设计文档或架构规范
2. ✅ **实现比较**：根据记录的决策分析代码
3. ✅ **差距分类**：每个合规差距都经过分类（例如边界违规、缺少组件、不同模式）以及影响和根本原因
4. ✅ **Report persisted**：架构合规性报告写入约定路径
5. ✅ **参考证据**：每个差距都引用了特定的设计来源和代码位置；当使用部分验证时，覆盖/未覆盖的范围和置信度是明确的
6. ✅ **建议切换**：当设计过时或有冲突时，建议`设计-解决方案`；当需要结构审查时，建议“审查架构”

**验收**测试：队友能否阅读报告并立即了解哪些架构决策被违反、代码中的何处以及下一步该做什么？

---

## 范围边界（范围边界）

**本技能负责**：

- 设计文档与代码比较
- 合规差距检测和分类
- 每个差距的影响范围和根本原因
- 整治和转交建议

**本技能不负责**：

- 没有设计参考的代码结构审查（使用“review-architecture”）
- 需求分析（使用“analyze-需求”）
- 设计创作或设计替代方案（使用“设计解决方案”）
- 规划图层对齐（使用“align-planning”）

**转交点**：报告后，如果设计必须改变，则移交给“设计-解决方案”，或者如果没有设计比较，则移交给“审查-架构”以进行结构代码审查。

---

## 使用场景（用例）

- **实施后检查**：验证实施是否与 ADR 或设计文档匹配
- **里程碑或发布门**：确保架构决策反映在代码中
- **漂移调查**：当实施偏离文档设计时进行诊断
- **入职审核**：帮助新贡献者了解设计与实际状态

---

## 编排指导

|场景|推荐顺序|
| --- | --- |
|日常任务完成 | `align-planning`（轻量级）|
|里程碑或释放门| `align-planning`（完整）→ 然后`align-architecture` |
|实施后检查| `对齐架构` |
|规划和建筑都存在问题|首先进行“对齐规划”；如果报告表明设计代码漂移 → `align-architecture` |

当规划层对齐不确定时，在“align-architecture”之前运行“align-planning”；否则，独立运行“align-architecture”进行设计与代码验证。

---

## 行为（行为）

### 代理即时合同


```text
You are responsible for architecture compliance verification.

Compare documented architecture and design decisions (ADRs, design docs) against
the codebase and produce an Architecture Compliance Report when divergence exists.
```


### 交互（互动）政策

- **默认**：来自项目规范或“docs/architecture/”、“docs/design-decisions/”、“docs/process-management/decisions/”的 ADR/设计路径；工作区中的代码范围
- **选择选项**：非默认时显式设计文档路径；部分作用域时的显式代码路径
- **确认**：在对设计文档提出编辑建议之前；在大代码范围之前

### 第 0 阶段：解决设计源和代码范围

1、解决设计源码路径（项目规范或默认：`docs/architecture/`、`docs/design-decisions/`、`docs/process-management/decisions/`）
2.解析代码范围：
   - **完整**：整个存储库（默认）
   - **增量**：用户指定的路径、包或模块（对于大型代码库；仅验证受影响的设计决策）
3. 如果没有设计文档，则输出所需最少输入的阻塞报告；建议“设计解决方案”或“引导文档”

### 阶段 0.5：证据准备情况评估

在比较之前评估设计覆盖范围：

- **强**：范围内所有相关组件/模块都存在设计文档
- **弱**：部分设计文档；一些组件有 ADR，另一些则没有——以较低的置信度执行部分验证
- **缺失**：没有设计文档；报告被阻止，建议设计工作流程

规则：

1. 当准备度“弱”时，仅验证有设计来源的决策；将未发现的代码标记为“未知”并在报告中列出。
2. 当准备“弱”时，不要声称有很高的信心。
3. 明确报告：覆盖范围、未覆盖范围和置信度。

### 第 1 阶段：提取设计决策

1. 解析 ADR、设计文档和架构规范
2. 提取关键决策：边界、组件、模式、约束
3. 建立决策指标进行比较

### 第 2 阶段：比较实施

1. 根据每个记录的决策分析代码
2. 对于每个决定，评估：“合规” | `部分` | ‘违反’ | `未知`
3. 捕获证据：文件路径、模块或片段
4. 差距分类：
   - **边界违规**：代码跨越了文档化的模块/层边界
   - **缺少组件**：记录的组件或接口未实现
   - **发散模式**：实现使用与文档中不同的模式
   - **过时的设计**：设计文档可能已过时；实现可能反映当前意图 - 分配“recommended_action”：
     - `update_设计`：执行权威； 应更新设计以匹配（建议“设计-解决方案”）
     - `update_code`：设计保持权威；代码应该重构以匹配
     - “两者”：不明确；需要利益相关者做出决定；建议“设计解决方案”来协调

### 第三阶段：生成报告

1. 汇总调查结果，包括影响范围、根本原因和每个差距的“推荐行动”
2. 对于每个差距，明确说明：更新代码、更新设计或两者兼而有之（请参阅上面的差距类型）
3. 当设计必须改变时，推荐转交到`设计-解决方案`；当需要仅结构审查时，进行“审查架构”
4. 使用部分验证时包括证据准备和置信度

### 第 4 阶段：坚持报告

将报告写至：

- 从项目规范解析的路径（`docs/ARTIFACT_NORMS.md` 或 `.ai-cortex/artifact-norms.yaml`）
- 默认：`docs/calibration/architecture-compliance.md`（除非明确请求快照，否则覆盖）
- 或者用户指定的路径

报告必须包含机器可读的合规性块（YAML 或 JSON）。

---

## 输入与输出 (Input & Output)

### 输入（输入）

- 可选的 ADR/设计文档路径
- 可选的代码范围（路径或模块）
- 可选的项目文档根目录

### 输出（输出）

#### 架构合规性报告模板


```markdown
# Architecture Compliance Report

**Date:** YYYY-MM-DD
**Design Sources:**
**Code Scope:**
**Status:** compliant | partial | violated
**Evidence Readiness:** strong | weak | missing (when partial verification used)
**Confidence:** high | medium | low

## Summary
- Total decisions checked:
- Compliant:
- Partial:
- Violated:

## Compliance Gaps

### Gap 1
- **Type:** boundary violation | missing component | divergent pattern | outdated design
- **Design Source:**
- **Code Location:**
- **Impact Scope:**
- **Root Cause:**
- **Recommended Action:** update_code | update_design | both
- **Remediation:**

## Covered / Uncovered Scope (when partial verification)
- Covered:
- Uncovered:
- Reason:

## Recommended Next Actions
1.
2.

## Machine-Readable Compliance

    evidence:
      readiness: "strong"  # strong | weak | missing
      confidence: "high"   # high | medium | low
    gaps:
      - type: "boundary violation"
        designSource: "docs/architecture/adr-001.md"
        codeLocation: "pkg/infra/db.go"
        impactScope: "Domain layer imports infrastructure"
        rootCause: "Repository interface not used; direct DB import"
        recommendedAction: "update_code"  # update_code | update_design | both
        remediation: "Implement repository pattern per ADR-001"
```


---

## 限制（限制）

### 硬边界（Hard Boundaries）

- 当文档丢失时，不要发明设计决策；报告被阻止并建议设计工作流程
- 当证据准备度“弱”时，请勿声称高度可信（部分验证）
- 当设计来源不完整或不明确时，请勿声称合规
- 未经用户明确批准，请勿悄悄修改设计文档
- 不要在没有设计参考的情况下执行结构性代码审查（即“审查架构”）

### 技能边界 (Skill Boundaries)（避免重叠）

**不要做这些（其他技能可以处理它们）**：

- 仅代码结构审查 → `审查架构`
- 设计创作或替代方案 → `设计解决方案`
- 规划层回溯→`align-planning`

**何时停止并交接**：

- 不存在设计文档→建议“设计解决方案”或“引导文档”
- 设计存在冲突或过时 → 交给“设计解决方案”
- 无需设计比较即可进行结构性代码审查 → 交给“审查架构”

---

## 自检（Self-Check）

### 核心成功标准（必须满足所有标准）

- [ ] 设计源的识别和解析
- [ ] 代码与记录决策进行比较（或在准备情况较弱时进行部分验证）
- [ ] 每个差距都包含影响范围、根本原因以及类型过时时的“推荐操作” 设计
- [ ] 报告坚持约定的路径
- [ ] 为每个差距提供证据参考（包括使用部分验证时覆盖/未覆盖的范围和置信度）
- [ ] 适用时提供移交建议

### 验收测试

**团队成员是否可以在没有额外说明的情况下针对前 1-3 个合规差距采取行动？**

如果否：完善证据并明确补救措施。

如果是：报告完成；进行转交或补救。

---

## 示例（示例）

### 示例 1：边界违规

**上下文**：ADR-001 规定域不得导入基础设施。代码显示域包导入数据库驱动程序。

**输出**：

- 类型：边界违规
- 设计来源：`docs/process-management/decisions/20240101-adr-001-layered-architecture.md`
- 代码位置：`pkg/domain/order.go`（导入`pkg/infra/db`）
- 影响：领域与基础设施耦合；违反了干净的架构
- 修复：在域中定义存储库接口；在基础设施中实施；通过构造函数注入

### 示例 2：无设计文档

**背景**：项目没有 ADR 或设计文档。

**输出**：

- 状态：被阻止
- 消息：未找到架构或设计文档。运行“设计解决方案”来创建设计文档，或运行“bootstrap-docs”来建立结构。
- 置信度：不适用

### 示例 3：部分验证（弱就绪）

**上下文**：只有 `pkg/auth` 有 ADR； `pkg/orders` 和 `pkg/inventory` 没有设计文档。

**输出**：

- 证据准备情况：弱
- 置信度：中等
- 涵盖范围：`pkg/auth`（根据 ADR-002 进行验证）
- 未发现的范围：`pkg/orders`、`pkg/inventory`（无设计来源；标记为未知）
- 报告继续包含“pkg/auth”的调查结果；如果需要合规性，建议为未覆盖的包创建设计文档

### 示例 4：过时的设计和建议的操作

**上下文**：ADR-003 指定同步 API；实现使用异步事件驱动流程，利益相关者更喜欢它。

**输出**：

- 类型：过时的设计
- 建议操作：update_设计
- 修复：将 ADR-003 更新为文档异步事件驱动方法；执行力具有权威性。移交给“设计解决方案”来修改设计文档。