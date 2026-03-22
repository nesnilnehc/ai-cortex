# ASQM 审计 — AI Cortex 技能

**审计日期**：2026-03-10
**范围**：`skills/` 下全部 38 个技能（validate-doc-artifacts 已于 2026-03 并入 assess-docs）
**打分**：ASQM strict（基于证据；agent_native = 5 仅当 SKILL.md 含有显式 output contract 时）

---

## 1. 按状态的生命周期

| Status | 数量 | 技能 |
| :--- | :--- | :--- |
| **validated** | 38 | review-code, review-diff, review-codebase, review-dotnet, review-java, review-go, review-php, review-powershell, review-python, review-sql, review-vue, review-typescript, review-react, review-security, review-architecture, review-performance, review-testing, review-orm-usage, curate-skills, discover-skills, discover-docs-norms, decontextualize-text, generate-standard-readme, generate-agent-entry, refine-skill-design, generate-github-workflow, install-rules, bootstrap-docs, capture-work-items, run-automated-tests, run-repair-loop, commit-work, design-solution, analyze-requirements, align-planning, align-architecture, assess-docs, plan-next |
| **experimental** | 0 | — |
| **archive_candidate** | 0 | — |

所有技能均满足其生命周期门槛：**validated** ↔ Quality ≥ 17 + Gate A（agent_native ≥ 4）+ Gate B（stance ≥ 3）；**experimental** ↔ Quality ≥ 10。

---

## 2. 打分公式与门限

- **Quality（线性）**：`asqm_quality = agent_native + cognitive + composability + stance`（各 0–5，总分 0–20）。
- **Gate A**（agent readiness）：agent_native ≥ 4。
- **Gate B**（design integrity）：stance ≥ 3。
- **validated**：Quality ≥ **17** 且 Gate A 且 Gate B。
- **experimental**：Quality ≥ 10。
- **archive_candidate**：其他情况。

---

## 3. 维度检查清单（严格）

| 维度 | 含义 | 所用证据 |
| :--- | :--- | :--- |
| **agent_native** | Agent 消费；机器可读契约 | SKILL.md 中的 Appendix / Output contract；agent.yaml 结构 |
| **cognitive** | 从用户转移至 Agent 的推理 | Steps、checklists、Self-Check、Behavior |
| **composability** | 与其他技能组合的便利性 | related_skills、清晰 I/O、聚合格式 |
| **stance** | 设计完整性、spec 对齐 | Restrictions、Self-Check、spec/skill.md 对齐 |

**严格规则**：仅当 SKILL.md 包含**显式、机器可解析的 output contract**（如「Appendix: Output contract」或等效表/spec）时 agent_native = 5。仅 prose 的输出描述 → agent_native ≤ 4。

---

## 4. 汇总表（分数与生命周期）

| Skill | agent_native | cognitive | composability | stance | asqm_quality | status |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| review-code | 5 | 5 | 5 | 5 | 20 | validated |
| refine-skill-design | 5 | 5 | 5 | 5 | 20 | validated |
| analyze-requirements | 5 | 5 | 5 | 5 | 20 | validated |
| curate-skills | 5 | 4 | 5 | 5 | 19 | validated |
| review-diff | 5 | 4 | 5 | 5 | 19 | validated |
| review-dotnet | 5 | 4 | 5 | 5 | 19 | validated |
| review-java | 5 | 4 | 5 | 5 | 19 | validated |
| review-go | 5 | 4 | 5 | 5 | 19 | validated |
| review-php | 5 | 4 | 5 | 5 | 19 | validated |
| review-powershell | 5 | 4 | 5 | 5 | 19 | validated |
| review-python | 5 | 4 | 5 | 5 | 19 | validated |
| review-sql | 5 | 4 | 5 | 5 | 19 | validated |
| review-vue | 5 | 4 | 5 | 5 | 19 | validated |
| review-typescript | 5 | 4 | 5 | 5 | 19 | validated |
| review-react | 5 | 4 | 5 | 5 | 19 | validated |
| review-orm-usage | 5 | 4 | 5 | 5 | 19 | validated |
| review-security | 5 | 4 | 5 | 5 | 19 | validated |
| review-architecture | 5 | 4 | 5 | 5 | 19 | validated |
| review-performance | 5 | 4 | 5 | 5 | 19 | validated |
| review-testing | 5 | 4 | 5 | 5 | 19 | validated |
| install-rules | 5 | 4 | 5 | 5 | 19 | validated |
| review-codebase | 5 | 4 | 4 | 5 | 18 | validated |
| generate-agent-entry | 5 | 4 | 4 | 5 | 18 | validated |
| generate-github-workflow | 5 | 4 | 4 | 5 | 18 | validated |
| bootstrap-docs | 5 | 4 | 4 | 5 | 18 | validated |
| capture-work-items | 5 | 4 | 4 | 5 | 18 | validated |
| commit-work | 5 | 5 | 5 | 5 | 20 | validated |
| design-solution | 5 | 5 | 4 | 5 | 19 | validated |
| discover-skills | 5 | 3 | 5 | 4 | 17 | validated |
| decontextualize-text | 5 | 4 | 4 | 4 | 17 | validated |
| generate-standard-readme | 5 | 3 | 4 | 5 | 17 | validated |
| run-automated-tests | 5 | 4 | 4 | 4 | 17 | validated |
| run-repair-loop | 5 | 4 | 4 | 4 | 17 | validated |
| align-planning | 5 | 5 | 5 | 5 | 20 | validated |
| align-architecture | 5 | 5 | 5 | 5 | 20 | validated |
| assess-docs | 5 | 4 | 5 | 5 | 19 | validated |
| plan-next | 5 | 5 | 5 | 5 | 20 | validated |
| discover-docs-norms | 5 | 4 | 4 | 5 | 18 | validated |

---

## 5. 重叠与生态

- **review-code** (orchestrator): overlaps with review-diff, review-codebase, and external code-review skills; **market_position**: differentiated.
- **Atomic review skills** (review-diff, review-codebase, review-dotnet, review-java, review-go, review-php, review-powershell, review-python, review-sql, review-vue, review-typescript, review-react, review-orm-usage, review-security, review-architecture, review-performance, review-testing): overlap with each other and review-code; **market_position**: commodity.
- **analyze-requirements**: overlaps with design-solution, capture-work-items (upstream/downstream handoff); **market_position**: differentiated.
- **capture-work-items**: overlaps with analyze-requirements (validation handoff), design-solution (design handoff); **market_position**: differentiated.
- **design-solution**: overlaps with analyze-requirements, refine-skill-design, capture-work-items (design handoff); **market_position**: differentiated.
- **align-planning**: overlaps with assess-docs, plan-next, align-architecture (routing/handoff by design); **market_position**: differentiated.
- **align-architecture**: overlaps with align-planning, review-architecture, design-solution (design vs code compliance; distinct from planning alignment and code-only review); **market_position**: differentiated.
- **assess-docs**: overlaps with bootstrap-docs (structure vs readiness boundary); subsumes former validate-doc-artifacts (compliance + readiness in one report); **market_position**: differentiated.
- **plan-next** (orchestrator): overlaps with review-code orchestrator at control-plane level; input-source driven (mission/vision/backlogs); **market_position**: differentiated.
- **commit-work**: overlaps with review-diff (pre-commit review); **market_position**: differentiated.
- **curate-skills**: overlaps with refine-skill-design, generate-standard-readme; **market_position**: differentiated.
- **refine-skill-design**: overlaps with curate-skills, discover-skills; **market_position**: differentiated.
- **discover-skills**: overlaps with refine-skill-design; **market_position**: differentiated.
-- **generate-standard-readme**: overlaps with decontextualize-text, generate-agent-entry; **market_position**: commodity.
- **generate-agent-entry**: overlaps with generate-standard-readme, refine-skill-design; **market_position**: differentiated.
- **decontextualize-text**: overlaps with generate-standard-readme; **market_position**: differentiated.
- **generate-github-workflow**: overlaps_with empty; **market_position**: differentiated.
- **install-rules**: overlaps with discover-skills (discover + install flow); **market_position**: differentiated.
- **run-repair-loop**: overlaps with review-code and run-automated-tests; **market_position**: commodity.
- **run-automated-tests**: overlaps with run-repair-loop; **market_position**: commodity.
- **bootstrap-docs**: overlaps with generate-standard-readme, generate-agent-entry; **market_position**: differentiated.
- **discover-docs-norms**: overlaps with bootstrap-docs, assess-docs; **market_position**: differentiated.

所有重叠使用 **Git-repo 形式** `owner/repo:skill-name`（如 `nesnilnehc/ai-cortex:review-diff`）。

---

## 6. 发现

### 6.1 既往发现 (2026-02-27)

1. **review-testing** (new): Appendix: Output contract with standard findings format → agent_native 5. Quality 19, validated. market_position: commodity.
2. **review-code** (updated): Version 2.6.0 — review-testing added to cognitive chain. Quality 20, validated.
3. **refine-skill-design** (corrected): Explicit Appendix: Output contract found → agent_native corrected 4 → 5; quality 19 → 20.

### 6.2 新发现 (2026-03-02)

1. **commit-work** (v2.0.0, new audit): Output Contract section is prose-only (no structured Appendix table) → agent_native 4. Deep 10-step workflow with interaction policy, 12 Self-Check items, 3 examples → cognitive 5. Integrates review-diff, references commit-message-template, registry sync for AI Cortex ecosystem → composability 5. Hard Boundaries + Skill Boundaries + Scope Boundaries → stance 5. Quality 19 (4+5+5+5), Gate A (4 ≥ 4) and Gate B (5 ≥ 3) satisfied → **validated**. market_position: differentiated.
2. **design-solution** (v1.0.0, new audit): Markdown document template provided but no structured Appendix table → agent_native 4. 5-phase workflow with HARD-GATE, 13 Self-Check items, 4 examples → cognitive 5. 3 related_skills, I/O schema present → composability 4. Hard Boundaries (7 items) + Skill Boundaries → stance 5. Quality 18 (4+5+4+5) → **validated**. market_position: differentiated.
3. **review-typescript** (v1.0.0, new audit): Explicit Appendix: Output contract with findings format table → agent_native 5. 7-point review checklist, 9 Self-Check items → cognitive 4. Standard findings format for aggregation, 3 related_skills → composability 5. Hard Boundaries + Skill Boundaries → stance 5. Quality 19 (5+4+5+5) → **validated**. market_position: commodity.
4. **review-react** (v1.0.0, new audit): Explicit Appendix: Output contract → agent_native 5. Same review-skill pattern as review-typescript → cognitive 4, composability 5, stance 5. Quality 19 → **validated**. market_position: commodity.
5. **review-orm-usage** (v1.0.0, new audit): Explicit Appendix: Output contract with findings format → agent_native 5. 6-point review checklist → cognitive 4. 5 related_skills (widest among review skills) → composability 5. Hard Boundaries with "do not duplicate review-sql" → stance 5. Quality 19 (5+4+5+5) → **validated**. market_position: commodity.
6. **analyze-requirements** (v1.0.0, new audit): Structured output template + Appendix: Integration Map with 3 tables → agent_native 5. Deepest cognitive offload: triage scoring matrix, 6 diagnostic states (RA0-RA5) with entry/exit criteria, 5 anti-patterns, health check questions, 12 Self-Check items → cognitive 5. Explicit handoff contract + 3 related_skills + I/O schema → composability 5. Hard Boundaries (6 items) + 3-tier Self-Check → stance 5. Quality 20 (5+5+5+5) → **validated**. market_position: differentiated.

### 6.3 其他变更

1. **run-automated-tests** and **run-repair-loop**: Graduated from experimental (v0.1.0) to stable (v1.0.0) per INDEX.md §2 convention (validated at 0.x.x → upgrade when contract stabilizes). Scores unchanged (both 17).
2. **Existing 26 skills**: No score or lifecycle changes. All retain their validated status.

### 6.4 格式规范化 (2026-03-02)

1. **analyze-requirements** and **design-solution**: Migrated `agent.yaml` from legacy format (`version`/`description`/`lifecycle`/`asqm_score`/`related_skills`/`recommended_scope`) to the standard output-contract schema (`status`/`primary_use`/`inputs`/`outputs`/`scores`/`asqm_quality`/`overlaps_with`/`market_position`/`tags`). No score changes; format-only migration.
2. **execution-alignment** (v1.0.0): Introduced traceback + typed drift + calibration contract, deterministic mode selection, and mapping-confirmation gate. Quality 20.
3. **documentation-readiness** (v1.0.0): Introduced layer readiness scoring, gap prioritization, and minimal-fill plan output. Quality 19.
4. **project-cognitive-loop** (v1.0.0): Introduced governance-cycle orchestration contract and routed sequence reporting. Quality 20.
5. **Current baseline**: All 36 skills now use the unified agent.yaml/schema style expected by ASQM reporting.

### 6.5 Curation 运行 (2026-03-06)

1. **execution-alignment**, **documentation-readiness**, **project-cognitive-loop**: Created `agent.yaml` (scores, overlaps_with, market_position) and normalized `README.md` to standard sections (what it does, when to use, inputs, outputs, related skills). All three were previously scored in §4 but lacked agent.yaml and README.
2. **run-repair-loop**: Normalized README — updated status from experimental to validated, ASQM scores from 16 to 17 (agent_native 4 → 5, market_position experimental → commodity) to match agent.yaml and §4.

### 6.6 Curation 运行 (2026-03-06, refine-skill-design)

1. **refine-skill-design** (v1.2.0 → v1.3.0): Added Output Persistence policy — fixed temp `SKILL.refined.md` or new-per-run path; never overwrites original or prior outputs. Hard Boundary added. Scores unchanged (20); agent.yaml outputs updated.

### 6.7 project-cognitive-loop 精炼 (2026-03-06)

1. **project-cognitive-loop**: Single-artifact rule added — orchestrator produces only one output file; routed skills (documentation-readiness, execution-alignment) do not persist separate files. Recommended Next Tasks section required: prioritized, actionable, with owner, scope, rationale. agent.yaml and README updated; intent-routing output description updated. Scores unchanged (20).

### 6.8 Curation 运行 (2026-03-06, capture-work-items)

1. **capture-work-items** (v1.0.0, new): Structured output templates in Input & Output section but no explicit Appendix: Output contract → agent_native 4. 4-phase behavior (Triage, Extract, Prompt, Persist), Path Detection table, required-fields-by-type, 6 Self-Check items → cognitive 4. 2 related_skills, I/O schema, handoff points → composability 4. Restrictions (4 hard boundaries) + Skill Boundaries + Self-Check → stance 5. Quality 17 (4+4+4+5), Gate A and Gate B satisfied → **validated**. overlaps_with: analyze-requirements, design-solution. market_position: differentiated. Created agent.yaml and README.

### 6.9 Curation 刷新 (2026-03-06, v2.1.0 发布准备)

1. **curate-skills ASQM refresh**: Full scan confirms 37 skills; all agent.yaml present; verify-registry.mjs and verify-skill-structure.mjs pass. No score or status changes; INDEX, manifest, marketplace.json consistent. Refresh executed as part of milestone-closed governance cycle.

### 6.10 Curation 运行 (2026-03-06, discover-docs-norms, validate-doc-artifacts)

1. **discover-docs-norms** (v1.0.0, new): Output schema describes docs/ARTIFACT_NORMS.md and .ai-cortex/artifact-norms.yaml; no explicit Appendix: Output contract table → agent_native 4. 4-phase workflow (Scan, Choose, Confirm, Write), dialogue-based, Self-Check → cognitive 4. 2 related_skills, I/O schema → composability 4. Hard Boundaries + Skill Boundaries + schema compliance → stance 5. Quality 17 (4+4+4+5), Gate A and Gate B satisfied → **validated**. overlaps_with: bootstrap-docs, documentation-readiness. market_position: differentiated.

2. **validate-doc-artifacts** (v1.0.0, new, **merged into assess-docs 2026-03**): Output schema described findings-list; 3-phase workflow (Resolve, Scan/Infer, Validate/Emit). Compliance validation is now Phase 1 of assess-docs; single report includes compliance findings and readiness.

3. **agent.yaml and README**: Created for both skills per governance artifact requirements. Full scan confirmed 39 skills; after merge, 38 skills.

### 6.12 Curation 运行 (2026-03-10, align-planning 拆分)

1. **align-architecture** (v1.0.0, new): output_schema with artifact_type, path_pattern, machine-readable compliance block in report template → agent_native 5. 4-phase workflow (Resolve, Extract, Compare, Report), gap classification, handoff logic → cognitive 5. 4 related_skills, clear boundary vs review-architecture (design vs code) and align-planning (planning) → composability 5. Hard Boundaries + Skill Boundaries + Self-Check → stance 5. Quality 20 (5+5+5+5) → **validated**. overlaps_with: align-planning, review-architecture, design-solution, assess-docs. market_position: differentiated.
2. **align-planning** (v1.1.0): Slimmed to planning layer; overlaps updated to include align-architecture. Scores unchanged (20).

### 6.11 Curation 运行 (2026-03-10)

1. **Appendix: Output contract added** to 5 skills; agent_native 4 → 5 per strict rule:
   - **commit-work**: Explicit Appendix with table (commit message, summary, commands, registry sync) → 19 → 20
   - **design-solution**: Explicit Appendix (path, artifact_type, sections, approval) → 18 → 19
   - **capture-work-items**: Explicit Appendix (path, artifact_type, required sections) → 17 → 18
   - **discover-docs-norms**: Explicit Appendix (primary/optional outputs, path mapping) → 17 → 18
   - **validate-doc-artifacts** (merged into assess-docs 2026-03): had Explicit Appendix (findings format table) → 17 → 18.
2. **Skill renaming** (2026-03-10): documentation-readiness → assess-docs, execution-alignment → align-planning, project-cognitive-loop → run-checkpoint; ASQM scores unchanged for renamed skills.
3. **Scope**: 40 skills; all validated; no archive candidates.

---

## 7. 建议

1. **已完成**：align-architecture 加入审计（v1.0.0，Quality 20，validated）；align-planning overlaps 已更新。
2. **无紧急变更**：40 个 validated；无 archive 候选。
3. **重叠为设计使然**：原子 review 技能与其编排器（review-code）重叠；analyze-requirements 与 design-solution 形成有意设计的上下游对。
4. **Curation 运行 (2026-03-10)**：已添加 align-architecture（Quality 20）；40 个 validated。prune-content 已移除 (2026-03-16)。无进一步变更建议。

---

*由 curate-skills 技能生成（ASQM strict 打分）。*
