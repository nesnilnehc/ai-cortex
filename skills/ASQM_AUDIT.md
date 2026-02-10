# ASQM Audit — AI Cortex Skills

**Audit date**: 2025-02-10  
**Scope**: All skills under `skills/`  
**Scoring**: ASQM strict (evidence-based; agent_native = 5 only with explicit output contract in SKILL.md).

---

## 1. Lifecycle by status

| Status | Count | Skills |
| :--- | :--- | :--- |
| **validated** | 17 | review-code, review-diff, review-codebase, review-dotnet, review-java, review-sql, review-vue, review-security, review-architecture, curate-skills, discover-skills, decontextualize-text, generate-standard-readme, write-agents-entry, refine-skill-design, generate-github-workflow, install-rules |
| **experimental** | 0 | — |
| **archive_candidate** | 0 | — |

All 17 skills meet **validated**: Quality ≥ 17 (or ≥ 10 for experimental), Gate A (agent_native ≥ 4), and Gate B (stance ≥ 3).

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
| review-sql | 5 | 4 | 5 | 5 | 19 | validated |
| review-vue | 5 | 4 | 5 | 5 | 19 | validated |
| review-security | 5 | 4 | 5 | 5 | 19 | validated |
| review-architecture | 5 | 4 | 5 | 5 | 19 | validated |
| write-agents-entry | 5 | 4 | 4 | 5 | 18 | validated |
| generate-github-workflow | 5 | 4 | 4 | 5 | 18 | validated |
| discover-skills | 5 | 3 | 5 | 4 | 17 | validated |
| decontextualize-text | 5 | 4 | 4 | 4 | 17 | validated |
| generate-standard-readme | 5 | 3 | 4 | 5 | 17 | validated |
| install-rules | 5 | 4 | 5 | 5 | 19 | validated |

---

## 5. Overlaps and ecosystem

- **review-code** (orchestrator): overlaps with review-diff, review-codebase, and external code-review skills; **market_position**: differentiated.
- **Atomic review skills** (review-diff, review-codebase, review-dotnet, review-java, review-sql, review-vue, review-security, review-architecture): overlap with each other and review-code; **market_position**: commodity.
- **curate-skills**: overlaps with refine-skill-design, generate-standard-readme; **market_position**: differentiated.
- **refine-skill-design**: overlaps with curate-skills, discover-skills; **market_position**: differentiated.
- **discover-skills**: overlaps with refine-skill-design; **market_position**: differentiated.
- **generate-standard-readme**: overlaps with decontextualize-text, write-agents-entry; **market_position**: commodity.
- **write-agents-entry**: overlaps with generate-standard-readme, refine-skill-design; **market_position**: differentiated.
- **decontextualize-text**: overlaps with generate-standard-readme; **market_position**: differentiated.
- **generate-github-workflow**: overlaps_with empty; **market_position**: differentiated.
- **install-rules**: overlaps with discover-skills (discover + install flow); **market_position**: differentiated.

All overlaps use **Git-repo form** `owner/repo:skill-name` (e.g. `nesnilnehc/ai-cortex:review-diff`).

---

## 6. Findings

1. **review-code**: Previously, agent.yaml and README described "diff-only" review; they have been updated to describe the **orchestrator** (scope → language → framework → library → cognitive, aggregate report). review-diff is the scope-only atomic skill.
2. **Seven skills** (review-diff, review-dotnet, review-java, review-sql, review-vue, review-security, review-architecture) had no agent.yaml or README; **agent.yaml** and **README** were created for each, with ASQM scores, overlaps_with, and market_position.
3. **refine-skill-design**: No explicit output contract in SKILL.md (no "Appendix: Output contract"); agent_native kept at 4 per strict scoring. All other skills with "Appendix: Output contract" (or equivalent) in SKILL.md received agent_native 5.
4. **INDEX.md** and **manifest.json** were not modified by this skill (per Restrictions); no capability changes were required.
5. **install-rules**: New skill had no agent.yaml or README; **agent.yaml** and **README** were created with ASQM scores (19, validated), overlaps_with (discover-skills), market_position (differentiated). SKILL.md contains Appendix: Output contract → agent_native 5.

---

## 7. Recommendations

1. **No structural changes recommended.** All 17 skills are validated; lifecycle and scoring are consistent with ASQM strict rules.
2. **Optional**: Consider adding an **Appendix: Output contract** (or equivalent machine-parseable spec) to **refine-skill-design** SKILL.md if you want to raise agent_native to 5 in a future audit; current score 4 is correct given the spec.
3. **Sync INDEX and SKILL versions**: `scripts/verify-registry.mjs` currently reports version mismatches for review-codebase (INDEX 1.1.0 vs SKILL 1.3.0) and review-diff (INDEX 1.2.0 vs SKILL 1.3.0). Align INDEX.md version column with each skill’s SKILL.md front matter, or bump SKILL versions to match INDEX, then re-run the verifier.
4. **Ongoing**: After adding or changing any skill, run **curate-skills** again (e.g. "curate" or "curate all skills") to refresh agent.yaml, README, and this ASQM_AUDIT.md.
5. **Commit**: Commit the new/updated `agent.yaml`, `README.md` per skill and this `ASQM_AUDIT.md` so the repo has a single source of truth for quality and ecosystem position.

---

*Generated by the curate-skills skill (ASQM strict scoring).*
