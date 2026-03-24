---
artifact_type: adr
created_by: decision-record
lifecycle: snapshot
created_at: 2026-03-24
status: active
---

# Align 系列技能重规划与拆分

**状态**: 提案 (Proposed)  
**日期**: 2026-03-16  
**范围**: align-planning、align-architecture 及未来 align-* 技能的边界与拆分。

---

## 1. 背景与目标

- **现状**: 存在 `align-planning`（规划层追溯、漂移检测、再校准）与 `align-architecture`（设计/ADR 与代码一致性）。已移除 `align-backlog-to-strategy`，其能力由 `run-strategy-checkpoint` 在具备执行证据时覆盖。
- **目标**: 明确 align 家族的统一语义与边界；按「对齐层」拆分，避免重叠与脑裂；便于编排（如 `run-checkpoint`）和发现。

---

## 2. 命名与语义约定

- **align-* 语义**: 「将 A 层与 B 层对比，产出差距报告与建议；不直接修改被对比的文档或代码。」
- **产出**: 均为校准类报告（findings + 建议），写入 `docs/calibration/`（或项目规范约定路径）。
- **不负责**: 需求/设计/战略文档的撰写、代码实现、回溯执行；仅做对比与建议，具体修改由对应技能或人工完成。

---

## 3. 按「对齐层」的拆分方案

### 3.1 规划层对齐 — `align-planning`（保留并收紧）

| 项目 | 说明 |
| :--- | :--- |
| **A 层** | 规划类文档：目标、需求、里程碑、路线图（goals, requirements, milestones, roadmap） |
| **B 层** | 已完成任务/执行结果（completed task, backlog 状态等） |
| **产出** | Planning Alignment Report：追溯结果、漂移分类（goal/requirement/roadmap/priority）、再校准建议与下一任务推荐 |
| **边界** | 仅规划层；不包含设计文档与代码的对比 |

**可选细化（后续实施）**:

- **方案 A（保持单技能）**: 继续用 Lightweight / Full 两种模式区分「轻量追溯」与「全层追溯+再校准」，不拆技能。
- **方案 B（拆成两技能）**:  
  - `align-planning`：仅做追溯 + 漂移检测 + 报告（只读）；  
  - `recommend-recalibration` 或由编排器调用：基于报告产出再校准动作与下一任务建议。  
  若拆，需在 intent-routing 与 run-checkpoint 中明确谁调谁。

**建议**: 先采用方案 A，在 SKILL 内明确「Phase 1 追溯 / Phase 2 漂移 / Phase 3 再校准」的边界与 Handoff；若后续编排或复用需求增加再考虑方案 B。

---

### 3.2 设计/实现层对齐 — `align-architecture`（保留并收紧）

| 项目 | 说明 |
| **A 层** | 架构与设计文档：ADR、设计决策、架构说明 |
| **B 层** | 当前代码实现 |
| **产出** | Architecture Compliance Report：合规差距、影响、根因与修复建议 |
| **边界** | 仅设计/代码一致性；不包含「目标/需求/路线图」与执行的对比 |

与 `align-planning` 的协作顺序已在两技能中约定：规划层不确定时先 `align-planning`，再视需要运行 `align-architecture`。

---

### 3.3 战略层与执行层对齐（不再单独设 align-backlog-to-strategy）

| 需求 | 处理方式 |
| :--- | :--- |
| 战略文档 ↔ 执行/backlog 一致性 | 由 `align-backlog` 在 backlog↔strategy 映射与分类报告中体现；在需要治理视角时，由 `run-checkpoint` 的周期报告聚合包含 align 家族输出的 Strategy/Milestone 状态与建议。 |
| 战略链完整性（mission → vision → … → milestones） | 由战略撰写类技能（define-* / design-strategic-goals）与文档就绪类（如 assess-doc-readiness）保障；不新增 validate-strategy-chain 技能。 |

若未来需要「仅产出 backlog↔strategy 追溯矩阵」的原子能力，可再考虑新增单一职责的 align 技能（例如 `align-backlog-to-strategy` 仅做追溯与报告），当前由 align-planning、align-backlog 等报告 + run-checkpoint 的聚合视图共同覆盖。

---

## 4. 技能清单与编排关系（重规划后）

| 技能 | 对齐层 | 输入 A | 输入 B | 产出 |
| :--- | :--- | :--- | :--- | :--- |
| align-planning | 规划层 | 目标、需求、里程碑、路线图 | 已完成任务/执行 | Planning Alignment Report |
| align-architecture | 设计/实现层 | ADR、设计文档 | 代码 | Architecture Compliance Report |

**编排**:

- `run-checkpoint`: 先统一序列（如 align-planning → assess-doc-readiness），再按输出决定是否调用 align-architecture 等；在需要战略/里程碑视图时，基于 align-planning、align-backlog 等报告聚合出 Strategy/Milestone 状态与建议。

---

## 5. 后续动作建议

1. **align-planning**  
   - 在 SKILL 的 Scope Boundaries / Restrictions 中显式写出「仅规划层；设计 vs 代码归 align-architecture」。  
   - 在 Self-Check 中强调「未越界到设计/代码对比」。

2. **align-architecture**  
   - 在 SKILL 中再次强调「仅设计/代码；规划层追溯归 align-planning」。  
   - 保持与 run-checkpoint、align-planning 的 Orchestration Guidance 一致。

3. **run-checkpoint**  
   - 保持对 align-planning、align-architecture 的调用关系；不引用已删除的 align-backlog-to-strategy。  
   - 若在 Phase 1 或说明中曾引用「backlog-strategy 对齐」，改为「执行证据可由 run-strategy-checkpoint 消费」等表述。

4. **intent-routing**  
   - post_task_governance、architecture_compliance、iteration_orchestration 的 primary/optional 已只保留 align-planning、align-architecture，无需再引用已删除技能。

5. **可选**  
   - 若后续需要「仅追溯、不推荐」的原子能力，再评估将 align-planning 拆成「追溯报告」与「再校准建议」两个技能，并更新本决策与 intent-routing。

---

## 6. 决策总结

- **保留**: `align-planning`（规划层）、`align-architecture`（设计/代码层）；统一语义为「A 层 vs B 层 → 差距报告 + 建议，只读」。
- **移除**: `align-backlog-to-strategy`；其能力由 `run-strategy-checkpoint` 在提供执行证据时覆盖。
- **不新增**: `validate-strategy-chain`；战略链完整性由撰写技能与 doc-readiness 类能力保障。
- **重规划**: align 家族按「对齐层」清晰拆分；编排与场景映射按上表维护，避免重叠与脑裂。
