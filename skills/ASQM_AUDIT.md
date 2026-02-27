# ASQM Audit — AI Cortex Skills

**Audit date**: 2026-02-27
**Scope**: All skills under `skills/`  
**Scoring**: ASQM strict (evidence-based; agent_native = 5 only with explicit output contract in SKILL.md).

---

## 1. Lifecycle by status

| Status | Count | Skills |
| :--- | :--- | :--- |
| **validated** | 26 | review-code, review-diff, review-codebase, review-dotnet, review-java, review-go, review-php, review-powershell, review-python, review-sql, review-vue, review-security, review-architecture, review-performance, review-testing, curate-skills, discover-skills, decontextualize-text, generate-standard-readme, write-agents-entry, refine-skill-design, generate-github-workflow, install-rules, bootstrap-project-documentation, run-automated-tests, run-repair-loop |
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
| curate-skills | 5 | 4 | 5 | 5 | 19 | validated |
| refine-skill-design | 5 | 5 | 5 | 5 | 20 | validated |
| review-diff | 5 | 4 | 5 | 5 | 19 | validated |
| review-dotnet | 5 | 4 | 5 | 5 | 19 | validated |
| review-java | 5 | 4 | 5 | 5 | 19 | validated |
| review-go | 5 | 4 | 5 | 5 | 19 | validated |
| review-php | 5 | 4 | 5 | 5 | 19 | validated |
| review-powershell | 5 | 4 | 5 | 5 | 19 | validated |
| review-python | 5 | 4 | 5 | 5 | 19 | validated |
| review-sql | 5 | 4 | 5 | 5 | 19 | validated |
| review-vue | 5 | 4 | 5 | 5 | 19 | validated |
| review-security | 5 | 4 | 5 | 5 | 19 | validated |
| review-architecture | 5 | 4 | 5 | 5 | 19 | validated |
| review-performance | 5 | 4 | 5 | 5 | 19 | validated |
| review-testing | 5 | 4 | 5 | 5 | 19 | validated |
| install-rules | 5 | 4 | 5 | 5 | 19 | validated |
| review-codebase | 5 | 4 | 4 | 5 | 18 | validated |
| write-agents-entry | 5 | 4 | 4 | 5 | 18 | validated |
| generate-github-workflow | 5 | 4 | 4 | 5 | 18 | validated |
| bootstrap-project-documentation | 5 | 4 | 4 | 5 | 18 | validated |
| discover-skills | 5 | 3 | 5 | 4 | 17 | validated |
| decontextualize-text | 5 | 4 | 4 | 4 | 17 | validated |
| generate-standard-readme | 5 | 3 | 4 | 5 | 17 | validated |
| run-automated-tests | 5 | 4 | 4 | 4 | 17 | validated |
| run-repair-loop | 5 | 4 | 4 | 4 | 17 | validated |

---

## 5. Overlaps and ecosystem

- **review-code** (orchestrator): overlaps with review-diff, review-codebase, and external code-review skills; **market_position**: differentiated.
- **Atomic review skills** (review-diff, review-codebase, review-dotnet, review-java, review-go, review-php, review-powershell, review-python, review-sql, review-vue, review-security, review-architecture, review-performance, review-testing): overlap with each other and review-code; **market_position**: commodity.
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

1. **review-testing** (new): Created `agent.yaml` and `README.md`. SKILL.md contains an explicit Appendix: Output contract with standard findings format (Location, Category=cognitive-testing, Severity, Title, Description, Suggestion) → agent_native 5. Quality 19 (5+4+5+5), Gate A and B satisfied → **validated**. Same structural pattern as review-security and review-architecture; 6-item review checklist (existence, coverage, quality, types, edge cases, maintainability); 3 examples including well-tested edge case. market_position: commodity.
2. **review-code** (updated): Version bumped from 2.5.0 to 2.6.0 — review-testing added to cognitive execution order (security → performance → architecture → testing). related_skills updated. No score change; remains Quality 20, validated.
3. **skillgraph.md** (updated): Added review-testing to cognitive section. Also corrected prior omissions: review-performance, review-go, review-php, review-python were missing from the composition graph and quick reference table.
4. **Existing skills**: No score or lifecycle changes. All 25 previously instrumented skills retain their scores and validated status.

---

## 7. Recommendations

1. **Done**: **refine-skill-design** SKILL.md already contains an explicit Appendix: Output contract (structured table: Optimized SKILL, Diff summary with Section/Change/Reason, Version suggestion). agent_native corrected from 4 → 5; asqm_quality 19 → 20.
2. **Commit**: Commit the new review-testing skill (SKILL.md, agent.yaml, README.md) and updated governance artifacts (review-code SKILL.md, INDEX.md, manifest.json, skillgraph.md, ASQM_AUDIT.md).
3. **No other changes recommended**: All skills are validated; no archive candidates; overlaps are expected and by design (atomic skills naturally overlap with their orchestrator).

---

*Generated by the curate-skills skill (ASQM strict scoring).*
