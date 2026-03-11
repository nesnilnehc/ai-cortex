---
artifact_type: adr
path_pattern: docs/process-management/decisions/YYYYMMDD-{slug}.md
created_at: "2026-03-10"
lifecycle: living
---

# 实施计划：run-checkpoint Phase 0.5 Planning Readiness Gate

**日期**: 2026-03-10  
**状态**: 已实施  
**类型**: 实施计划  
**相关**: [skills/run-checkpoint](../../../skills/run-checkpoint/SKILL.md)

> 注：原 `orchestrate-governance-loop` 已重命名为 `run-checkpoint`（2026-03-10 命名审计）。

---

## 1. 目标与范围

### 1.1 目标

扩展 `run-checkpoint`，在 Phase 1（Unified Sequence）之前增加 **Phase 0.5: Planning Readiness Gate**，在项目文档缺失或不足时自动执行准备步骤，使 align-planning 具备可执行前提。

### 1.2 范围

- **在范围内**：修改 run-checkpoint 的 SKILL.md、agent.yaml、README；更新 skillgraph、INDEX、manifest、scenario-map 等引用；ensure discover-document-norms、bootstrap-docs 为 related_skills 并参与 Phase 0.5 编排
- **不在范围内**：修改 align-planning、assess-doc-readiness、discover-document-norms、bootstrap-docs 的技能逻辑

---

## 2. 设计摘要

### 2.1 流程变更

```text
原流程:
  Phase 0 (Trigger) → Phase 1 (align-planning → assess) → Phase 2–4

新流程:
  Phase 0 (Trigger)
  → Phase 0.5 (Planning Readiness Gate)  [新增]
      ├─ 诊断 (assess 或轻量检测)
      ├─ norms_missing → discover-document-norms
      ├─ structure_missing → bootstrap-docs
      ├─ readiness=missing → 短路，输出 Minimal Fill Plan
      └─ readiness∈[weak,strong] → 继续 Phase 1
  → Phase 1 (align-planning → assess)
  → Phase 2–4
```

### 2.2 诊断逻辑

| 状态 | 检测条件 | 动作 |
| --- | --- | --- |
| norms_missing | 无 `docs/ARTIFACT_NORMS.md` 且无 `.ai-cortex/artifact-norms.yaml`，且 `docs/` 存在但路径不符合 contract 默认 | 调用 `discover-document-norms` |
| structure_missing | 无 `docs/` 或缺少 planning 相关目录（project-overview、requirements-planning、process-management 等） | 调用 `bootstrap-docs` |
| readiness=missing | assess 返回 low 且主要为内容缺失（结构已有但 goals/requirements/roadmap 空） | 短路，将 Minimal Fill Plan 纳入 cycle report |
| readiness=weak/strong | assess 返回 medium 或 high | 继续 Phase 1 |

### 2.3 输出规则

- **Phase 0.5 准备类 skill**：discover、bootstrap 产出为项目状态（norms、docs 结构），**需要持久化**
- **Phase 1 分析类 skill**：align-planning、assess 产出为分析结论，**不单独持久化**，汇总进 cycle report
- **短路时**：cycle report 包含 Phase 0.5 的 assess 的 Minimal Fill Plan，以及 Recommended Next Tasks

---

## 3. 实施阶段

### 阶段 1：SKILL.md 修改

**文件**: `skills/run-checkpoint/SKILL.md`

| 任务 | 内容 |
| --- | --- |
| 1.1 | 确认 frontmatter 的 `related_skills` 包含 `discover-document-norms`、`bootstrap-docs`（已包含） |
| 1.2 | 在 `## Behavior` 中插入 **Phase 0.5: Planning Readiness Gate**，描述：诊断逻辑、状态分支、调用条件、短路条件 |
| 1.3 | 在 Phase 1 描述前增加「仅在 Phase 0.5 通过后执行」的说明 |
| 1.4 | 在 `## Scope Boundaries` 的「This skill handles」中增加：Planning Readiness 诊断与准备编排 |
| 1.5 | 在 `## Restrictions` 的 Skill Boundaries 中注明：norms 建立 → discover-document-norms；结构建立 → bootstrap-docs |
| 1.6 | 新增 Example 4：readiness=missing 短路；Example 5： Phase 0.5 执行 bootstrap 后继续 Phase 1 |
| 1.7 | 更新 Self-Check：Phase 0.5 执行正确性、短路时 Recommended Next Tasks 包含 Minimal Fill Plan |
| 1.8 | 更新 version 为 `1.2.0`（minor：新增 Phase 0.5 子流程） |

**验收**：SKILL.md 自洽，Phase 0.5 逻辑可被 Agent 理解并执行。

---

### 阶段 2：agent.yaml 与 README

**文件**: `skills/run-checkpoint/agent.yaml`

| 任务 | 内容 |
| --- | --- |
| 2.1 | 在 `overlaps_with` 中增加 `nesnilnehc/ai-cortex:discover-document-norms`、`nesnilnehc/ai-cortex:bootstrap-docs` |
| 2.2 | 在 `primary_use` 或 `outputs` 中补充 Phase 0.5 的职责与短路输出说明（如有字段） |

**文件**: `skills/run-checkpoint/README.md`

| 任务 | 内容 |
| --- | --- |
| 2.3 | 在 When to use / 流程描述中补充 Phase 0.5 简要说明 |
| 2.4 | 在 Related skills 中列出 discover-document-norms、bootstrap-docs |

**验收**：agent.yaml 与 README 与 SKILL.md 一致。

---

### 阶段 3：skillgraph 与索引

**文件**: `scripts/generate-skillgraph.mjs`

| 任务 | 内容 |
| --- | --- |
| 3.1 | 在 `ORCHESTRATOR_CHAINS['run-checkpoint']` 中，将 `discover-document-norms`、`bootstrap-docs` 加入（作为 Phase 0.5 可能调用的 skill） |
| 3.2 | 确认 `PROJECT_LOOP_CHAIN` 或相关流程图中体现 Phase 0.5 分支（如有） |

**文件**: `skills/skillgraph.md`

| 任务 | 内容 |
| --- | --- |
| 3.3 | 运行 `node scripts/generate-skillgraph.mjs`  regenerate，或手动补充 Phase 0.5 相关说明（若脚本未覆盖） |

**文件**: `skills/INDEX.md`、`manifest.json`

| 任务 | 内容 |
| --- | --- |
| 3.4 | 确认 run-checkpoint 的 related_skills、version 变更已反映（manifest 自动或人工同步） |

**验收**：skillgraph 与 INDEX 正确反映编排关系。

---

### 阶段 4：scenario-map

**文件**: `skills/scenario-map.json`、`skills/scenario-map.md`

| 任务 | 内容 |
| --- | --- |
| 4.1 | 在「项目无文档体系，想用 align-planning / checkpoint」相关 scenario 中，将 run-checkpoint 标为推荐入口，并注明会执行 Phase 0.5 准备 |
| 4.2 | 在 optional skills 中保留 discover-document-norms、bootstrap-docs（若尚未列入） |

**验收**：用户通过 scenario 可正确理解 run-checkpoint 作为入口时会执行准备步骤。

---

### 阶段 5：CHANGELOG 与元数据

**文件**: `CHANGELOG.md`

| 任务 | 内容 |
| --- | --- |
| 5.1 | 新增条目：run-checkpoint v1.2.0 — Phase 0.5 Planning Readiness Gate；discover-document-norms、bootstrap-docs 纳入编排 |

**文件**: `skills/run-checkpoint/SKILL.md`（metadata）

| 任务 | 内容 |
| --- | --- |
| 5.2 | 在 `metadata.evolution.enhancements` 中增加：v1.1.0 Phase 0.5 Planning Readiness Gate |

**验收**：变更可追溯。

---

### 阶段 6：自检与回归

| 任务 | 内容 |
| --- | --- |
| 6.1 | 运行 run-checkpoint Self-Check（人工或按 SKILL 自检清单逐项检查） |
| 6.2 | 验证与 align-planning、assess-doc-readiness、discover-document-norms、bootstrap-docs 的 handoff 与边界描述一致 |
| 6.3 | 若存在 `scripts/verify-*.mjs` 等校验脚本，确保通过 |

**验收**：自检通过，无技能边界冲突。

---

## 4. 依赖与前置

| 依赖 | 说明 |
| --- | --- |
| discover-document-norms | 已存在，可被编排调用 |
| bootstrap-docs | 已存在，可被编排调用 |
| assess-doc-readiness | 已存在，可作 Phase 0.5 诊断或与轻量检测配合 |
| spec/artifact-contract.md | 路径与 layer 定义不变 |
| spec/artifact-norms-schema.md | discover 输出格式不变 |

---

## 5. 风险与缓解

| 风险 | 缓解 |
| --- | --- |
| discover、bootstrap 需用户确认 | 编排中注明：调用时若 skill 请求确认，Agent 应暂停并引导用户；短路时 Recommended Next Tasks 可建议用户单独执行 |
| 诊断逻辑过于复杂 | v1 采用「先运行 assess 作诊断」的简化方案；复杂分支可后续迭代 |
| Phase 0.5 与 Phase 1 的 assess 重复 | 若 Phase 0.5 已运行 assess 且未短路，可将 Phase 1 的 assess 视为 refresh，或复用 Phase 0.5 结果（需在 SKILL 中明确） |

---

## 6. 里程碑

| 里程碑 | 完成标准 |
| --- | --- |
| M1: 设计冻结 | Phase 0.5 逻辑、状态定义、输出规则在 SKILL 中确定 |
| M2: SKILL 修改完成 | 阶段 1–2 完成，SKILL/agent/README 一致 |
| M3: 生态同步完成 | 阶段 3–5 完成，skillgraph/INDEX/scenario-map/CHANGELOG 更新 |
| M4: 发布就绪 | 阶段 6 完成，自检通过，version 更新为 1.2.0 |

---

## 7. 附录：Phase 0.5 伪代码

```text
function phase05_planning_readiness_gate():
  # Step 1: 轻量诊断
  if not has_norms() and has_non_standard_docs():
    run discover-document-norms
    # discover 可能需要用户确认；完成后重新诊断
    return phase05_planning_readiness_gate()  # 或进入下一轮 cycle

  if not has_structure():
    run bootstrap-docs
    return phase05_planning_readiness_gate()

  # Step 2: 运行 assess 获取 readiness
  result = run assess-doc-readiness (in-process, aggregate output)

  if result.readiness == "low" and result.gaps_are_content_only():
    # 短路：结构在，内容缺
    short_circuit()
    cycle_report.include(result.minimal_fill_plan)
    cycle_report.recommended_next_tasks = result.minimal_fill_plan.actions
    persist(cycle_report)
    return

  if result.readiness in ["medium", "high"]:
    proceed_to_phase1()
```
