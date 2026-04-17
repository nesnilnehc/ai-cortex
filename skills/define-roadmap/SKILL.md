---
name: define-roadmap
description: Derive a strategic roadmap from goals using milestone checkpoints, strategic bets, success metrics, and promotion criteria. Produces a decision-grade roadmap document.
description_zh: 从战略目标推导路线图，包含里程碑、关键举措、成功指标与推进条件，产出可用于决策的路线图文档。
tags: [documentation, strategy, workflow]
version: 3.0.0
license: MIT
recommended_scope: both
metadata:
  author: ai-cortex
triggers: [define roadmap, roadmap, milestones, strategic roadmap, phase planning]
input_schema:
  type: free-form
  description: Strategic goals (document or path); project context; optional vision/NSM; time horizon or phase preference
output_schema:
  type: document-artifact
  description: Decision-grade roadmap document with milestones, strategic bets, success metrics, and promotion criteria
  artifact_type: roadmap
  path_pattern: docs/process-management/roadmap.md
  path_alt: docs/process-management/milestones.md
  lifecycle: living
---

# 技能 (Skill)：定义路线图 (Production v3.0.0)

## 目的 (Purpose)

从战略目标推导"可驱动决策的路线图"，而非任务列表。路线图不是里程碑集合，而是**路径表达**。

---

## 核心目标（Core Objective）

**首要目标**：生成用户确认的可驱动决策的路线图文档，每个阶段明确包含里程碑、关键举措、成功指标与推进条件。

**成功标准**（必须满足所有要求）：

1. ✅ **核心模型完整**：每个阶段必须包含里程碑（Milestone）、关键举措（Strategic Bets）、成功指标（Metrics）和推进条件（Promotion Criteria）。
2. ✅ **有序结构与路径感**：采用 **Now / Next / Later** 划分阶段，体现演进路径。
3. ✅ **结果与指标导向**：成功指标优先量化，里程碑为成果导向，绝非功能列表或 TODO 的混入。
4. ✅ **避免虚假精确**：Later 阶段仅说明方向，**不写具体时间**。
5. ✅ **目标追溯与约束**：建立目标映射，且明确约束「Backlog 必须映射到路线图，不属于路线图的需求默认不做」。
6. ✅ **用户确认与持久化**：用户明确批准，并写入约定路径（默认 `docs/process-management/roadmap.md` 或依规范 `milestones.md`）。

**验收测试**：读者能否一眼看到演进路径（包含推进条件）？能否通过成功指标验证阶段成果，而非单纯检查任务列表？

**交接点**：路线图获批并持久化后，交接至待办规划、需求分析（`analyze-requirements`）或执行对齐（`align-planning` / `plan-next`）。

---

## 范围边界 (Scope Boundaries)

**本技能负责**：

- 从战略目标中推导并划分阶段（Now / Next / Later）。
- 为每个阶段定义里程碑、关键举措（2–5个）、成功指标和推进条件。
- 组织并生成结构化的路线图文档。
- 坚持项目约定路径。

**本技能不负责**：

- 定义使命、愿景、北极星或战略目标（使用 `define-mission`、`define-vision`、`define-north-star`、`design-strategic-goals`）。
- 编写具体需求或拆分任务（使用 `analyze-requirements`、`breakdown-tasks`）。
- 创建具体的 Backlog 项目（使用 `capture-work-items`）。

---

## 使用场景 (Use Cases)

- **战略目标确立后**：需要将高层的战略目标转化为具体阶段、关键举措与指标。
- **阶段流转评估**：通过"推进条件"（Next → Now）决定团队是否可以进入下一阶段。
- **规划与对齐会议**：为团队和利益相关者提供清晰的路径表达与决策依据，淘汰不符合当前路径的杂乱需求。

---

## 行为 (Behavior)

### 交互（互动）政策

- **默认**：输出至 `docs/process-management/roadmap.md` 或遵循项目既有规范。自动读取 `docs/project-overview/strategic-goals.md` 作为输入依据。
- **推断与确认**：基于现有的项目状态或上下文提炼关键举措与指标；涉及核心决策或覆盖既有文档前，向用户请求明确确认。

### 执行过程

1. **加载战略目标**：读取现有战略目标及项目背景。
2. **划分阶段**：结构化为 Now / Next / Later 视角。
3. **定义里程碑**：确保以成果为导向。
4. **提炼关键举措**：每个阶段提炼 2–5 个关键举措（Strategic Bets）。
5. **定义成功指标**：为阶段成果设定验证标准，优先量化。
6. **定义推进条件**：明确进入下一阶段的前提（如 Next → Now 的切换条件）。
7. **建立目标映射**：确保阶段目标和 Backlog 可以映射到战略。
8. **生成路线图文档**：按照输出结构模板生成文档草案。
9. **确认与持久化**：用户确认后持久化写入并标注最后更新日期。

### 输出结构模板 (内嵌契约)

```markdown
# 路线图

## 路线概览

Now / Next / Later（含推进条件简述）

---

## Now

### 里程碑
- ...

### 关键举措
- ...

### 成功指标
- ...

---

## Next

### 推进条件
- ...

### 里程碑
- ...

### 关键举措
- ...

---

## Later

仅方向，不写时间

---

## 里程碑详情（附录）

| Milestone | Scope | Metrics | Goals |
```

---

## 输入与输出 (Input & Output)

**输入**：
- **必填**：战略目标（文档或路径）；项目背景。
- **可选**：愿景/北极星指标；时间范围或阶段偏好。

**输出**：
- **工件**：决策级路线图文档。
- **位置**：`docs/process-management/roadmap.md` 或 `milestones.md`（依项目规范）。
- **内容**：含路线概览、Now/Next/Later 详情（里程碑、关键举措、指标、推进条件）。
- **生命周期**：living（随阶段推进持续更新）。

---

## 限制 (Restrictions)

### 硬边界 (Hard Boundaries)

- **路线图映射约束**：明确「Backlog 必须映射到路线图，不属于路线图的需求默认不做」。
- **结构强制**：每个阶段必须包含核心模型（里程碑、关键举措、成功指标、推进条件），缺一不可。
- **无覆盖**：未经用户明确确认，不覆盖既有路线图文件。

### 反模式（避免）

- **功能列表**：将路线图降级为功能特性堆砌。
- **TODO 混入**：掺杂具体执行级别的任务。
- **无指标**：无法验证里程碑是否达成。
- **无关键举措**：只有目标没有对应的战略动作。
- **虚假精确**：在 Later 阶段写明具体日期/时间。

### 技能边界 (Skill Boundaries)（避免重叠）

**不要做这些（其他技能负责）**：
- **定义战略目标**：使用 `design-strategic-goals`。
- **拆分具体需求/任务**：使用 `analyze-requirements` 或 `breakdown-tasks`。
- **编写待办**：使用 `capture-work-items`。

**何时停止并交接**：
- 用户回复「已批准/确认」等 → 路线图完成，持久化文档并交接给 `align-planning` 或待办规划。

---

## 自检 (Self-Check)

### 核心成功标准（必须满足所有标准）

- [ ] **核心模型完整**：文档包含里程碑、关键举措、成功指标、推进条件。
- [ ] **有序结构与路径感**：路线图基于 Now / Next / Later 展现演进路径。
- [ ] **结果与指标导向**：内容为成果导向，无功能或 TODO 列表。
- [ ] **避免虚假精确**：Later 阶段未包含具体时间，仅指明方向。
- [ ] **目标追溯与约束**：体现了路线图到战略目标的映射关系，约束了 Backlog。
- [ ] **用户确认与持久化**：用户已批准，并写入约定路径。

### 验收测试

读者能否一眼看到演进路径（包含推进条件）？能否通过成功指标验证阶段成果，而非单纯检查任务列表？

- 若否：需补充成功指标或推进条件，剔除功能性 TODO 列表。
- 若是：路线图符合生产级要求，继续转交。

---

## 示例 (Examples)

### 示例 1：根据战略目标生成生产级路线图

**背景**：已有包含 3 项指标的战略目标，需制定演进路径。
**流程**：
1. 读取目标并按 Now / Next / Later 视角划分。
2. 为 Now 定义明确的 3 项关键举措与量化成功指标。
3. 定义 Next 阶段的"推进条件"（如"当核心架构验证达到 10k QPS 时，启动 Next 阶段"）。
4. 在 Later 中列出长远探索主题（无日期）。
5. 呈现文档草案并获批后写入 `docs/process-management/roadmap.md`。
**结果**：路线图持久化，清晰驱动下一步的资源分配与决策。

### 示例 2：纠正任务列表反模式

**背景**：用户要求「帮我把这些 Backlog 任务排期做成路线图」。
**流程**：
1. 向用户说明本技能的原则：路线图是路径表达与决策模型，而非任务清单。
2. 将具体的 Backlog 抽象为对应的关键举措与阶段性里程碑。
3. 补充各阶段的成功指标与推进条件，去除细碎的 TODO。
4. 提供草案并与用户确认。
**结果**：将需求列表成功转换为符合生产级的决策路线图。
