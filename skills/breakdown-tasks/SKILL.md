---
name: breakdown-tasks
description: Break a design document into an executable task list with dependencies, acceptance criteria, and assignee or AI execution hints. Use when design is approved and you need an implementation plan.
description_zh: 将设计文档拆解为可执行任务列表：依赖、验收标准、负责人或 AI 执行提示。
tags: [writing, documentation, workflow]
version: 1.1.0
license: MIT
recommended_scope: both
metadata:
  author: ai-cortex
triggers: [breakdown tasks, task breakdown, implementation plan, tasks from design]
input_schema:
  type: document-artifact + optional free-form
  description: Design document (e.g. design.md or docs/design-decisions/YYYY-MM-DD-<topic>.md); optional scope or priority hints
output_schema:
  type: document-artifact
  description: Task list document with ordered tasks, dependencies, acceptance criteria, and assignee/execution hints
  path_pattern: docs/process-management/tasks/YYYY-MM-DD-{topic}.md (or project-convention tasks.md)
  lifecycle: living
---

# 技能（Skill）：分解任务

## 目的 (Purpose)

将已验证设计文档变成有序的、可跟踪的任务列表。每个任务都有依赖性、验收标准和受让人（或人工智能执行提示），以便可以毫无歧义地进行实施。

---

## 核心目标（Core Objective）

**任务目标**：根据设计文档生成任务文档（例如tasks.md），以便每个可实施的单元都是一个具有明确依赖性、验收标准和所有权的任务。

**成功标准**（必须满足所有要求）：

1. ✅ **任务文档存在**：写入商定的路径（例如 `docs/process-management/tasks/YYYY-MM-DD-<topic>.md` 或项目 `tasks.md`）并提交
2. ✅ **设计可追溯性**：每项任务至少映射到设计的一部分（部分或验收标准）
3. ✅ **依赖关系明确**：任务顺序或依赖关系列表清晰（无循环依赖关系）
4. ✅ **每个任务的接受标准**：每个任务都有具体的“完成”标准
5. ✅ **受让人或执行提示**：每个任务都有所有者（人/角色）或AI执行提示（例如要运行哪个技能或步骤）
6. ✅ **用户确认**：用户明确批准或调整任务列表

**验收**测试：执行者（人或代理）可以仅使用此文档和设计来选择下一个任务，实施它并验证完成情况吗？

---

## 范围边界（范围边界）

**本技能负责**：

- 设计文档 → 有序任务列表（tasks.md 或同等文件）
- 任务之间的依赖关系；每项任务的验收标准；受让人或AI执行提示
- 将任务列表作为活的产品进行持久化，以进行实施跟踪

**本技能不负责**：

- 创建或验证设计（使用“设计解决方案”或“头脑风暴设计”）
- 验证需求（使用“分析需求”）
- 执行任务（实施技巧、运行修复循环等）
- 日程安排或容量规划（使用项目/里程碑工具）

**转交点**：当任务列表被批准并保留后，移交给执行（例如按顺序运行任务，或输入待办/板）。

---

## 使用场景（用例）

- **设计后规划**：设计获得批准；在编码之前你需要一个清晰的实施计划。
- **可追溯性**：您希望每个设计决策都映射到一个或多个具体任务。
- **人工智能辅助执行**：您希望每个任务都包含提示（例如“使用技能 X”或“编辑文件 Y”），以便代理可以执行计划。

---

## 行为（行为）

### 交互（互动）政策

- **默认**：需要设计文档（路径或内容）；使用项目规范作为输出路径（如果存在）
- **选择选项**：当设计不明确时，一次提出一个澄清问题
- **确认**：用户必须批准或调整任务列表才能转交

### 第 1 阶段：摄取设计

1. **加载设计**：阅读设计文档（例如设计.md或docs/design-decisions/*.md）。
2. **提取结构**：识别暗示工作的部分（架构、组件、数据流、错误处理、测试等）。
3. **确认范围**：如果用户指定了一个子集（例如“仅后端”），则将任务限制为该子集。

### 第 2 阶段：派生任务

1. **每个可实施单元一项任务**：每项任务都应在一次焦点会议中完成；当 X 很大时，避免模糊的“实施 X”。
2. **按依赖关系排序**：列出任务，使依赖关系排在第一位； 明确的文档依赖性（例如“取决于：T1，T2”）。
3. **验收标准**：对于每项任务，说明“完成”是什么样的（可测试或可验证）。
4. **受让人或提示**：对于每个任务，设置受让人（人员/角色）或 AI 执行提示（例如“为模块 Y 运行设计解决方案”、“根据设计§3 编辑 src/foo.ts”）。

### 第三阶段：坚持并移交

1. **解析路径**：优先选择项目规范（例如docs/ARTIFACT_NORMS.md）；否则 `docs/process-management/tasks/YYYY-MM-DD-<topic>.md` 或项目约定 `tasks.md`。
2. **编写任务文档**：使用一致的格式（见下文）；如果项目使用它，则包含 front-matter（`created_by:分解任务`、`lifecycle:living`、设计源路径）。
3. **用户批准**：呈现摘要并请求批准或编辑。
4. **Handoff**：建议从第一个未阻塞的任务开始执行。

---

## 输入与输出 (Input & Output)

|角色 |内容 |
| :--- | :--- |
| **输入** |设计文档（路径或内容）；用户的可选范围/优先级 |
| **输出** |任务文档位于 `docs/process-management/tasks/YYYY-MM-DD-<topic>.md` 或项目 `tasks.md`；每个任务都有 ID、标题、依赖项、接受标准、受让人/提示 |

---

## 推荐的任务列表格式


```markdown
# Implementation tasks: [Topic]

**Source design:** [path or title]
**Created:** YYYY-MM-DD

| Id | Task | Depends on | Acceptance criteria | Owner / Hint | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| T1 | ...  | —          | ...                  | ...         | Todo   |
| T2 | ...  | T1         | ...                  | ...         | Todo   |
```

### 状态生命周期 (Status Lifecycle)

本技能仅负责将所有派生任务的初始状态设置为 `Todo`。
下游实施与执行技能（如具体的开发执行 agent）、任务看板同步工具或开发人员，负责在实施期间维护并更新该状态（例如流转为 `In Progress`、`Blocked`、`Done` 或 `Cancelled`）。本技能不负责在此后持续变更任务状态。


可选：在顶部添加简短的“摘要”和“设计可追溯性”（任务 → 设计部分）。

---

## 限制（限制）

### 硬边界（Hard Boundaries）

- **设计优先**：设计缺失或未经批准时请勿运行；交给“设计解决方案”或“头脑风暴设计”。
- **无实施**：不编写代码或运行实施技巧；只产生任务列表。
- **无循环依赖**：任务顺序必须是非循环的。

### 技能边界 (Skill Boundaries)（避免重叠）

**不要做这些（其他技能可以处理它们）**：

- 需求分析或验证→“分析需求”
- 设计探索或批准→`设计解决方案`
- 执行任务或修复循环→实施技能或“运行修复循环”

---

## 自检（Self-Check）

- [ ] 任务文档存在并已提交
- [ ] 设计可追溯性：每项任务至少映射到设计的一部分
- [ ] 依赖关系明确：任务顺序或依赖列表清晰，无循环依赖
- [ ] 每个任务都有接受标准（可测试或可验证）
- [ ] 每个任务都有受让人或 AI 执行提示
- [ ] 每一项任务都配置了初始状态（如 `Todo`）并包含在表格状态列中
- [ ] 用户批准或明确接受的任务列表

---

## 示例（示例）

### 示例 1：标准设计到任务流程

**调用**：“我们在 docs/design-decisions/2026-03-16-core-v1.md 中有设计。将其分解为任务。”

**代理**：使用分解任务；读设计；导出具有部门和验收标准的有序任务；写入 docs/process-management/tasks/2026-03-16-core-v1.md；获得用户认可；建议从第一个任务开始。

### 示例 2：边缘情况 — 超大设计

**调用**：“我们的平台设计文档非常庞大（多个子系统）。我们现在只需要‘身份验证+用户入门’的任务。”

**代理**：

- 要求用户确认预期的范围子集（例如设计的第 3 节和第 4 节）。
- 将任务派生限制为该子集，并清楚地注明任务文档中的范围源部分。
- 确保范围之外的依赖项要么作为外部先决条件存根，要么作为显式阻止程序捕获。
- 生成一个任务文件，其第一列将每个任务链接回所使用的特定设计部分，因此将来的运行可以扩展覆盖范围而无需重复。