# ASQM Audit — AI Cortex Skills

**Audit date**: 2026-02-25
**Scope**: All skills under `skills/`  
**Scoring**: ASQM strict (evidence-based; agent_native = 5 only with explicit output contract in SKILL.md).

---

## 1. Lifecycle by status

| Status | Count | Skills |
| :--- | :--- | :--- |
| **validated** | 21 | review-code, review-diff, review-codebase, review-dotnet, review-java, review-go, review-powershell, review-sql, review-vue, review-security, review-architecture, review-performance, curate-skills, discover-skills, decontextualize-text, generate-standard-readme, write-agents-entry, refine-skill-design, generate-github-workflow, install-rules, bootstrap-project-documentation |
| **experimental** | 2 | run-automated-tests, run-repair-loop |
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
| curate-skills | 5 | 4 | 5 | 5 | 19 | validated |
| refine-skill-design | 4 | 5 | 5 | 5 | 19 | validated |
| review-diff | 5 | 4 | 5 | 5 | 19 | validated |
| review-codebase | 5 | 4 | 4 | 5 | 18 | validated |
| review-dotnet | 5 | 4 | 5 | 5 | 19 | validated |
| review-java | 5 | 4 | 5 | 5 | 19 | validated |
| review-go | 5 | 4 | 5 | 5 | 19 | validated |
| review-powershell | 5 | 4 | 5 | 5 | 19 | validated |
| review-sql | 5 | 4 | 5 | 5 | 19 | validated |
| review-vue | 5 | 4 | 5 | 5 | 19 | validated |
| review-security | 5 | 4 | 5 | 5 | 19 | validated |
| review-architecture | 5 | 4 | 5 | 5 | 19 | validated |
| review-performance | 5 | 4 | 5 | 5 | 19 | validated |
| write-agents-entry | 5 | 4 | 4 | 5 | 18 | validated |
| generate-github-workflow | 5 | 4 | 4 | 5 | 18 | validated |
| discover-skills | 5 | 3 | 5 | 4 | 17 | validated |
| decontextualize-text | 5 | 4 | 4 | 4 | 17 | validated |
| generate-standard-readme | 5 | 3 | 4 | 5 | 17 | validated |
| install-rules | 5 | 4 | 5 | 5 | 19 | validated |
| run-automated-tests | 4 | 4 | 4 | 4 | 16 | experimental |
| run-repair-loop | 4 | 4 | 4 | 4 | 16 | experimental |
| bootstrap-project-documentation | 5 | 4 | 4 | 5 | 18 | validated |

---

## 5. Overlaps and ecosystem

- **review-code** (orchestrator): overlaps with review-diff, review-codebase, and external code-review skills; **market_position**: differentiated.
- **Atomic review skills** (review-diff, review-codebase, review-dotnet, review-java, review-go, review-powershell, review-sql, review-vue, review-security, review-architecture, review-performance): overlap with each other and review-code; **market_position**: commodity.
- **curate-skills**: overlaps with refine-skill-design, generate-standard-readme; **market_position**: differentiated.
- **refine-skill-design**: overlaps with curate-skills, discover-skills; **market_position**: differentiated.
- **discover-skills**: overlaps with refine-skill-design; **market_position**: differentiated.
- **generate-standard-readme**: overlaps with decontextualize-text, write-agents-entry; **market_position**: commodity.
- **write-agents-entry**: overlaps with generate-standard-readme, refine-skill-design; **market_position**: differentiated.
- **decontextualize-text**: overlaps with generate-standard-readme; **market_position**: differentiated.
- **generate-github-workflow**: overlaps_with empty; **market_position**: differentiated.
- **install-rules**: overlaps with discover-skills (discover + install flow); **market_position**: differentiated.
- **run-repair-loop**: overlaps with review-code and run-automated-tests; **market_position**: experimental.
- **bootstrap-project-documentation**: overlaps with generate-standard-readme, write-agents-entry; **market_position**: differentiated.

All overlaps use **Git-repo form** `owner/repo:skill-name` (e.g. `nesnilnehc/ai-cortex:review-diff`).

---

## 6. Findings

1. **review-performance**: `agent.yaml` and `README.md` were added so the skill is fully instrumented for ASQM governance. SKILL.md contains an explicit output contract (Appendix) → agent_native 5.
2. **run-automated-tests**: New skill added; `agent.yaml` and `README.md` were created. It is **experimental** (Quality 16) primarily because SKILL.md currently describes outputs in prose (no explicit machine-parseable output contract) → agent_native 4 under strict scoring.
3. **run-repair-loop**: New skill added; it is **experimental** (Quality 16) under strict scoring because SKILL.md does not yet define a machine-parseable output contract → agent_native 4.
4. **Existing skills**: agent.yaml and README were already aligned with the standardized structure; no score or lifecycle changes were required in this run.
5. **bootstrap-project-documentation**: New skill added; `agent.yaml` and `README.md` were created. SKILL.md contains an explicit Appendix: Output Contract with tables for Initialize/Adjust modes and template source → agent_native 5. Quality 18, Gate A and B satisfied → **validated**. v1.1.1: Adjust mode uses template as target; no empty dirs unless requested; repeatable; strict kebab-case naming; TEMPLATE_BASE_URL canonical; VERSION creation optional on user request; fetch-failure handling.

---

## 7. Recommendations

1. **Optional**: Add an explicit, machine-parseable **Output contract appendix** to `run-automated-tests` SKILL.md (e.g. a fixed "Test Plan Summary" schema). This would raise agent_native under strict scoring and may move it to **validated** if the overall quality reaches ≥ 17.
2. **Optional**: Add an explicit, machine-parseable **Output contract appendix** to `run-repair-loop` SKILL.md (e.g. a fixed "Repair Loop Report" schema). This would raise agent_native under strict scoring and may move it to **validated** if the overall quality reaches ≥ 17.
3. **Optional**: Consider adding an **Appendix: Output contract** (or equivalent machine-parseable spec) to **refine-skill-design** SKILL.md if you want to raise agent_native to 5 in a future audit; current score 4 is consistent with strict scoring.
4. **Ongoing**: After adding or changing any skill, run **curate-skills** again to refresh per-skill governance artifacts (`agent.yaml`, `README.md`) and this audit.
5. **Commit**: Commit the newly instrumented governance artifacts for `bootstrap-project-documentation` plus this updated `ASQM_AUDIT.md`.

---

*Generated by the curate-skills skill (ASQM strict scoring).*
