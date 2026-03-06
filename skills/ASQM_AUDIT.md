# ASQM Audit — AI Cortex Skills

**Audit date**: 2026-03-06
**Scope**: All 37 skills under `skills/`
**Scoring**: ASQM strict (evidence-based; agent_native = 5 only with explicit output contract in SKILL.md).

---

## 1. Lifecycle by status

| Status | Count | Skills |
| :--- | :--- | :--- |
| **validated** | 37 | review-code, review-diff, review-codebase, review-dotnet, review-java, review-go, review-php, review-powershell, review-python, review-sql, review-vue, review-typescript, review-react, review-security, review-architecture, review-performance, review-testing, review-orm-usage, curate-skills, discover-skills, decontextualize-text, generate-standard-readme, write-agents-entry, refine-skill-design, generate-github-workflow, install-rules, bootstrap-project-documentation, capture-work-items, run-automated-tests, run-repair-loop, commit-work, brainstorm-design, onboard-repo, analyze-requirements, execution-alignment, documentation-readiness, project-cognitive-loop |
| **experimental** | 0 | — |
| **archive_candidate** | 0 | — |

All skills meet their lifecycle thresholds: **validated** ↔ Quality ≥ 17 + Gate A (agent_native ≥ 4) + Gate B (stance ≥ 3); **experimental** ↔ Quality ≥ 10.

---

## 2. Scoring formula and gates

- **Quality (linear)**: `asqm_quality = agent_native + cognitive + composability + stance` (each 0–5, total 0–20).
- **Gate A** (agent readiness): agent_native ≥ 4.
- **Gate B** (design integrity): stance ≥ 3.
- **validated**: Quality ≥ **17** AND Gate A AND Gate B.
- **experimental**: Quality ≥ 10.
- **archive_candidate**: otherwise.

---

## 3. Dimension checklist (strict)

| Dimension | Meaning | Evidence used |
| :--- | :--- | :--- |
| **agent_native** | Agent consumption; machine-readable contracts | Appendix / Output contract in SKILL.md; agent.yaml structure |
| **cognitive** | Reasoning offloaded from user to Agent | Steps, checklists, Self-Check, Behavior |
| **composability** | Ease of combining with other skills | related_skills, clear I/O, aggregation format |
| **stance** | Design integrity, spec alignment | Restrictions, Self-Check, spec/skill.md alignment |

**Strict rule**: agent_native = 5 only when SKILL.md contains an **explicit, machine-parseable output contract** (e.g. "Appendix: Output contract" or equivalent table/spec). Prose-only output description → agent_native ≤ 4.

---

## 4. Summary table (scores and lifecycle)

| Skill | agent_native | cognitive | composability | stance | asqm_quality | status |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| review-code | 5 | 5 | 5 | 5 | 20 | validated |
| refine-skill-design | 5 | 5 | 5 | 5 | 20 | validated |
| onboard-repo | 5 | 5 | 5 | 5 | 20 | validated |
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
| write-agents-entry | 5 | 4 | 4 | 5 | 18 | validated |
| generate-github-workflow | 5 | 4 | 4 | 5 | 18 | validated |
| bootstrap-project-documentation | 5 | 4 | 4 | 5 | 18 | validated |
| capture-work-items | 4 | 4 | 4 | 5 | 17 | validated |
| commit-work | 4 | 5 | 5 | 5 | 19 | validated |
| brainstorm-design | 4 | 5 | 4 | 5 | 18 | validated |
| discover-skills | 5 | 3 | 5 | 4 | 17 | validated |
| decontextualize-text | 5 | 4 | 4 | 4 | 17 | validated |
| generate-standard-readme | 5 | 3 | 4 | 5 | 17 | validated |
| run-automated-tests | 5 | 4 | 4 | 4 | 17 | validated |
| run-repair-loop | 5 | 4 | 4 | 4 | 17 | validated |
| execution-alignment | 5 | 5 | 5 | 5 | 20 | validated |
| documentation-readiness | 5 | 4 | 5 | 5 | 19 | validated |
| project-cognitive-loop | 5 | 5 | 5 | 5 | 20 | validated |

---

## 5. Overlaps and ecosystem

- **review-code** (orchestrator): overlaps with review-diff, review-codebase, and external code-review skills; **market_position**: differentiated.
- **Atomic review skills** (review-diff, review-codebase, review-dotnet, review-java, review-go, review-php, review-powershell, review-python, review-sql, review-vue, review-typescript, review-react, review-orm-usage, review-security, review-architecture, review-performance, review-testing): overlap with each other and review-code; **market_position**: commodity.
- **onboard-repo** (orchestrator): overlaps with review-codebase, review-architecture, generate-standard-readme, write-agents-entry, discover-skills; **market_position**: differentiated.
- **analyze-requirements**: overlaps with brainstorm-design, capture-work-items (upstream/downstream handoff); **market_position**: differentiated.
- **capture-work-items**: overlaps with analyze-requirements (validation handoff), brainstorm-design (design handoff); **market_position**: differentiated.
- **brainstorm-design**: overlaps with analyze-requirements, refine-skill-design, capture-work-items (design handoff); **market_position**: differentiated.
- **execution-alignment**: overlaps with documentation-readiness and project-cognitive-loop (routing/handoff by design); **market_position**: differentiated.
- **documentation-readiness**: overlaps with bootstrap-project-documentation (structure vs readiness boundary); **market_position**: differentiated.
- **project-cognitive-loop** (orchestrator): overlaps with onboard-repo and review-code orchestrators at control-plane level; **market_position**: differentiated.
- **commit-work**: overlaps with review-diff (pre-commit review); **market_position**: differentiated.
- **curate-skills**: overlaps with refine-skill-design, generate-standard-readme; **market_position**: differentiated.
- **refine-skill-design**: overlaps with curate-skills, discover-skills; **market_position**: differentiated.
- **discover-skills**: overlaps with refine-skill-design; **market_position**: differentiated.
- **generate-standard-readme**: overlaps with decontextualize-text, write-agents-entry; **market_position**: commodity.
- **write-agents-entry**: overlaps with generate-standard-readme, refine-skill-design; **market_position**: differentiated.
- **decontextualize-text**: overlaps with generate-standard-readme; **market_position**: differentiated.
- **generate-github-workflow**: overlaps_with empty; **market_position**: differentiated.
- **install-rules**: overlaps with discover-skills (discover + install flow); **market_position**: differentiated.
- **run-repair-loop**: overlaps with review-code and run-automated-tests; **market_position**: commodity.
- **run-automated-tests**: overlaps with run-repair-loop; **market_position**: commodity.
- **bootstrap-project-documentation**: overlaps with generate-standard-readme, write-agents-entry; **market_position**: differentiated.

All overlaps use **Git-repo form** `owner/repo:skill-name` (e.g. `nesnilnehc/ai-cortex:review-diff`).

---

## 6. Findings

### 6.1 Prior findings (2026-02-27)

1. **review-testing** (new): Appendix: Output contract with standard findings format → agent_native 5. Quality 19, validated. market_position: commodity.
2. **review-code** (updated): Version 2.6.0 — review-testing added to cognitive chain. Quality 20, validated.
3. **refine-skill-design** (corrected): Explicit Appendix: Output contract found → agent_native corrected 4 → 5; quality 19 → 20.

### 6.2 New findings (2026-03-02)

1. **commit-work** (v2.0.0, new audit): Output Contract section is prose-only (no structured Appendix table) → agent_native 4. Deep 10-step workflow with interaction policy, 12 Self-Check items, 3 examples → cognitive 5. Integrates review-diff, references commit-message-template, registry sync for AI Cortex ecosystem → composability 5. Hard Boundaries + Skill Boundaries + Scope Boundaries → stance 5. Quality 19 (4+5+5+5), Gate A (4 ≥ 4) and Gate B (5 ≥ 3) satisfied → **validated**. market_position: differentiated.
2. **brainstorm-design** (v1.0.0, new audit): Markdown document template provided but no structured Appendix table → agent_native 4. 5-phase workflow with HARD-GATE, 13 Self-Check items, 4 examples → cognitive 5. 3 related_skills, I/O schema present → composability 4. Hard Boundaries (7 items) + Skill Boundaries → stance 5. Quality 18 (4+5+4+5) → **validated**. market_position: differentiated.
3. **review-typescript** (v1.0.0, new audit): Explicit Appendix: Output contract with findings format table → agent_native 5. 7-point review checklist, 9 Self-Check items → cognitive 4. Standard findings format for aggregation, 3 related_skills → composability 5. Hard Boundaries + Skill Boundaries → stance 5. Quality 19 (5+4+5+5) → **validated**. market_position: commodity.
4. **review-react** (v1.0.0, new audit): Explicit Appendix: Output contract → agent_native 5. Same review-skill pattern as review-typescript → cognitive 4, composability 5, stance 5. Quality 19 → **validated**. market_position: commodity.
5. **onboard-repo** (v1.0.0, new audit): Richest output contract of all skills (6-section diagnostic-report table + finding format + report template) → agent_native 5. 6-step fixed execution order, pre-flight confirmation, defaults table, condensed Agent instruction block, 10 Self-Check items → cognitive 5. Orchestrates 5 atomic skills with defined data flow → composability 5. Hard Boundaries (4 items, including "no analysis of its own") → stance 5. Quality 20 (5+5+5+5) → **validated**. market_position: differentiated.
6. **review-orm-usage** (v1.0.0, new audit): Explicit Appendix: Output contract with findings format → agent_native 5. 6-point review checklist → cognitive 4. 5 related_skills (widest among review skills) → composability 5. Hard Boundaries with "do not duplicate review-sql" → stance 5. Quality 19 (5+4+5+5) → **validated**. market_position: commodity.
7. **analyze-requirements** (v1.0.0, new audit): Structured output template + Appendix: Integration Map with 3 tables → agent_native 5. Deepest cognitive offload: triage scoring matrix, 6 diagnostic states (RA0-RA5) with entry/exit criteria, 5 anti-patterns, health check questions, 12 Self-Check items → cognitive 5. Explicit handoff contract + 3 related_skills + I/O schema → composability 5. Hard Boundaries (6 items) + 3-tier Self-Check → stance 5. Quality 20 (5+5+5+5) → **validated**. market_position: differentiated.

### 6.3 Additional changes

1. **run-automated-tests** and **run-repair-loop**: Graduated from experimental (v0.1.0) to stable (v1.0.0) per INDEX.md §2 convention (validated at 0.x.x → upgrade when contract stabilizes). Scores unchanged (both 17).
2. **Existing 26 skills**: No score or lifecycle changes. All retain their validated status.

### 6.4 Format normalization (2026-03-02)

1. **analyze-requirements** and **brainstorm-design**: Migrated `agent.yaml` from legacy format (`version`/`description`/`lifecycle`/`asqm_score`/`related_skills`/`recommended_scope`) to the standard output-contract schema (`status`/`primary_use`/`inputs`/`outputs`/`scores`/`asqm_quality`/`overlaps_with`/`market_position`/`tags`). No score changes; format-only migration.
2. **execution-alignment** (v1.0.0): Introduced traceback + typed drift + calibration contract, deterministic mode selection, and mapping-confirmation gate. Quality 20.
3. **documentation-readiness** (v1.0.0): Introduced layer readiness scoring, gap prioritization, and minimal-fill plan output. Quality 19.
4. **project-cognitive-loop** (v1.0.0): Introduced governance-cycle orchestration contract and routed sequence reporting. Quality 20.
5. **Current baseline**: All 36 skills now use the unified agent.yaml/schema style expected by ASQM reporting.

### 6.5 Curation run (2026-03-06)

1. **execution-alignment**, **documentation-readiness**, **project-cognitive-loop**: Created `agent.yaml` (scores, overlaps_with, market_position) and normalized `README.md` to standard sections (what it does, when to use, inputs, outputs, related skills). All three were previously scored in §4 but lacked agent.yaml and README.
2. **run-repair-loop**: Normalized README — updated status from experimental to validated, ASQM scores from 16 to 17 (agent_native 4 → 5, market_position experimental → commodity) to match agent.yaml and §4.

### 6.6 Curation run (2026-03-06, refine-skill-design)

1. **refine-skill-design** (v1.2.0 → v1.3.0): Added Output Persistence policy — fixed temp `SKILL.refined.md` or new-per-run path; never overwrites original or prior outputs. Hard Boundary added. Scores unchanged (20); agent.yaml outputs updated.

### 6.7 project-cognitive-loop refinement (2026-03-06)

1. **project-cognitive-loop**: Single-artifact rule added — orchestrator produces only one output file; routed skills (documentation-readiness, execution-alignment) do not persist separate files. Recommended Next Tasks section required: prioritized, actionable, with owner, scope, rationale. agent.yaml and README updated; scenario-map output description updated. Scores unchanged (20).

### 6.8 Curation run (2026-03-06, capture-work-items)

1. **capture-work-items** (v1.0.0, new): Structured output templates in Input & Output section but no explicit Appendix: Output contract → agent_native 4. 4-phase behavior (Triage, Extract, Prompt, Persist), Path Detection table, required-fields-by-type, 6 Self-Check items → cognitive 4. 2 related_skills, I/O schema, handoff points → composability 4. Restrictions (4 hard boundaries) + Skill Boundaries + Self-Check → stance 5. Quality 17 (4+4+4+5), Gate A and Gate B satisfied → **validated**. overlaps_with: analyze-requirements, brainstorm-design. market_position: differentiated. Created agent.yaml and README.

### 6.9 Curation refresh (2026-03-06, v2.1.0 release prep)

1. **curate-skills ASQM refresh**: Full scan confirms 37 skills; all agent.yaml present; verify-registry.mjs and verify-skill-structure.mjs pass. No score or status changes; INDEX, manifest, marketplace.json consistent. Refresh executed as part of milestone-closed governance cycle.

---

## 7. Recommendations

1. **Improvement opportunity**: Add structured "Appendix: Output contract" tables to **commit-work** and **brainstorm-design** to raise agent_native from 4 → 5 (potential quality 18 → 19).
2. **No urgent changes**: All 37 skills are validated; no archive candidates; no experimental skills remain.
3. **Overlaps by design**: Atomic review skills overlap with their orchestrator (review-code); analyze-requirements and brainstorm-design form an intentional upstream/downstream pair.
4. **Curation run (2026-03-06)**: capture-work-items added; agent.yaml and README created. All 37 skills have agent.yaml and normalized README; ASQM_AUDIT.md is current. No further changes recommended.

---

*Generated by the curate-skills skill (ASQM strict scoring).*
