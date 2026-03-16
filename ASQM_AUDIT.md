# ASQM Audit

**Generated**: 2026-03-16
**Skills audited**: 48
**Tool**: curate-skills

---

## Scoring Formula

**ASQM Quality** (linear): `asqm_quality = agent_native + cognitive + composability + stance` (0–20)

| Dimension | What it measures |
| :--- | :--- |
| `agent_native` | Agent consumption: explicit machine-parseable output contract, structured I/O schema |
| `cognitive` | Reasoning offloaded from user to Agent: phases, checklists, decision trees, Self-Check |
| `composability` | Ease of combining with other skills or pipelines: related_skills, artifact handoffs, orchestration |
| `stance` | Design integrity: spec alignment, all required sections, principles, evolution metadata |

**Strict scoring rules**:
- `agent_native = 5` only when the skill has an explicit `Appendix: Output contract` table in SKILL.md
- All scores are evidence-based from SKILL.md content; no inflation

**Lifecycle gates**:
- **validated**: Quality ≥ 17 AND agent_native ≥ 4 AND stance ≥ 3
- **experimental**: Quality ≥ 10
- **archive_candidate**: otherwise

---

## Lifecycle by Status

### validated (47 skills)

| Skill | Quality | agent_native | cognitive | composability | stance |
| :--- | :--- | :--- | :--- | :--- | :--- |
| align-architecture | 20 | 5 | 5 | 5 | 5 |
| align-backlog | 17 | 4 | 4 | 4 | 5 |
| align-planning | 20 | 5 | 5 | 5 | 5 |
| analyze-requirements | 20 | 5 | 5 | 5 | 5 |
| assess-docs | 19 | 5 | 4 | 5 | 5 |
| automate-repair | 17 | 5 | 4 | 4 | 4 |
| automate-tests | 17 | 5 | 4 | 4 | 4 |
| bootstrap-docs | 18 | 5 | 4 | 4 | 5 |
| breakdown-tasks | 18 | 5 | 4 | 5 | 4 |
| capture-work-items | 18 | 5 | 4 | 4 | 5 |
| commit-work | 20 | 5 | 5 | 5 | 5 |
| curate-skills | 19 | 5 | 4 | 5 | 5 |
| decontextualize-text | 17 | 5 | 4 | 4 | 4 |
| define-milestones | 20 | 5 | 5 | 5 | 5 |
| define-mission | 20 | 5 | 5 | 5 | 5 |
| define-north-star | 20 | 5 | 5 | 5 | 5 |
| define-roadmap | 20 | 5 | 5 | 5 | 5 |
| define-strategic-pillars | 20 | 5 | 5 | 5 | 5 |
| define-vision | 20 | 5 | 5 | 5 | 5 |
| design-solution | 19 | 5 | 5 | 4 | 5 |
| design-strategic-goals | 20 | 5 | 5 | 5 | 5 |
| discover-docs-norms | 18 | 5 | 4 | 4 | 5 |
| discover-skills | 17 | 5 | 3 | 5 | 4 |
| generate-agent-entry | 18 | 5 | 4 | 4 | 5 |
| generate-github-workflow | 18 | 5 | 4 | 4 | 5 |
| generate-standard-readme | 17 | 5 | 3 | 4 | 5 |
| plan-next | 20 | 5 | 5 | 5 | 5 |
| refine-skill-design | 20 | 5 | 5 | 5 | 5 |
| review-architecture | 19 | 5 | 4 | 5 | 5 |
| review-code | 20 | 5 | 5 | 5 | 5 |
| review-codebase | 18 | 5 | 4 | 4 | 5 |
| review-diff | 19 | 5 | 4 | 5 | 5 |
| review-dotnet | 19 | 5 | 4 | 5 | 5 |
| review-go | 19 | 5 | 4 | 5 | 5 |
| review-java | 19 | 5 | 4 | 5 | 5 |
| review-orm-usage | 19 | 5 | 4 | 5 | 5 |
| review-performance | 19 | 5 | 4 | 5 | 5 |
| review-php | 19 | 5 | 4 | 5 | 5 |
| review-powershell | 19 | 5 | 4 | 5 | 5 |
| review-python | 19 | 5 | 4 | 5 | 5 |
| review-react | 19 | 5 | 4 | 5 | 5 |
| review-requirements | 19 | 5 | 4 | 5 | 5 |
| review-security | 19 | 5 | 4 | 5 | 5 |
| review-sql | 19 | 5 | 4 | 5 | 5 |
| review-testing | 19 | 5 | 4 | 5 | 5 |
| review-typescript | 19 | 5 | 4 | 5 | 5 |
| review-vue | 19 | 5 | 4 | 5 | 5 |

### experimental (1 skill)

| Skill | Quality | agent_native | cognitive | composability | stance | Gate A fail |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| install-rules | 13 | 3 | 3 | 3 | 4 | agent_native 3 < 4 |

### archive_candidate (0 skills)

None.

---

## Overlaps and Market Position

### differentiated (25 skills)

align-architecture, align-backlog, align-planning, analyze-requirements, assess-docs, bootstrap-docs, breakdown-tasks, capture-work-items, commit-work, curate-skills, decontextualize-text, define-milestones, define-mission, define-north-star, define-roadmap, define-strategic-pillars, define-vision, design-solution, design-strategic-goals, discover-docs-norms, discover-skills, generate-agent-entry, generate-github-workflow, plan-next, refine-skill-design, review-orm-usage, review-requirements

### commodity (22 skills)

generate-standard-readme, review-architecture, review-code, review-codebase, review-diff, review-dotnet, review-go, review-java, review-performance, review-php, review-powershell, review-python, review-react, review-security, review-sql, review-testing, review-typescript, review-vue

### experimental (1 skill)

install-rules

### Notable overlap clusters

| Cluster | Skills |
| :--- | :--- |
| Code review orchestration | review-code ← review-diff, review-codebase, all language/framework/cognitive review skills |
| Requirements → design chain | analyze-requirements → review-requirements → design-solution → breakdown-tasks |
| Strategy foundation | define-mission, define-vision, define-north-star, define-strategic-pillars, design-strategic-goals, define-milestones, define-roadmap |
| Planning alignment | align-planning, align-architecture, align-backlog, plan-next, assess-docs |

---

## Ecosystem

**Internal overlaps** (nesnilnehc/ai-cortex): expected and intentional — skills are composable atomic units designed to chain, not compete.

**External overlaps** detected:
- `review-code`, `review-codebase`, `review-diff` overlap with: wshobson/agents:code-review-excellence, secondsky/claude-skills:code-review, trailofbits/skills:differential-review, cxuu/golang-skills:go-code-review, obra/superpowers:requesting-code-review, skillcreatorai/Ai-Agent-Skills:code-review
- `commit-work` overlaps with: anthropics/skills:commit-work, softaworks/agent-toolkit:commit-work

**Differentiation**: AI Cortex review skills are differentiated by: (a) atomic skill composition architecture (one dimension per skill, orchestrated by review-code), (b) governance integration (registry sync, artifact-contract compliance), (c) requirements/design chain unique to this repo.

---

## Findings

### F-01 · install-rules — Promote to validated

**Current**: experimental (quality 13, agent_native 3 — Gate A fails)

**Gap**: No formal `Appendix: Output contract` table in SKILL.md. Output is described in prose. Output type is `side-effect` which reduces composability.

**Path to validated**: Add explicit output contract table documenting post-install summary fields (rule name, action, target path, status). This raises agent_native from 3 → 4, enabling Gate A. With that improvement quality would be 14, still below 17 — also needs cognitive or composability improvement (e.g. structured plan output format or richer orchestration hooks) to reach 17.

### F-02 · analyze-requirements / design-solution — agent.yaml output paths were stale

**Resolved in this run**: Updated `analyze-requirements` output path from `docs/requirements/<topic>.md` → `docs/requirements-planning/<topic>.md`; updated `design-solution` output description to reflect `docs/designs/` and requirements-first input model.

### F-03 · align-backlog — agent_native ceiling

**Current**: agent_native 4 (just meets Gate A). The embedded output template in SKILL.md counts as a contract, but no formal `Appendix: Output contract` table. Adding a formal table would raise to 5 and increase quality to 18 (validated with margin).

### F-04 · review family cognitive score

**Observation**: All language/framework atomic review skills score cognitive 4 (not 5). This is correct and intentional — they offload structured review checklists but do not perform multi-phase reasoning or decision trees of the same depth as orchestrators (review-code, align-planning). No change recommended.

---

## Recommendations

1. **Promote install-rules to experimental → validated** (P2): Add `Appendix: Output contract` table to SKILL.md documenting post-install summary format. Then improve cognitive or composability by one point (structured plan output, or pipe to discover-skills). Target: quality ≥ 17, agent_native ≥ 4.

2. **Improve align-backlog agent_native** (P3): Add a formal `Appendix: Output contract` table alongside the existing embedded template. This is a low-effort change that raises quality 17 → 18 and improves discoverability.

3. **No further action on existing validated skills**: All 47 validated skills meet lifecycle criteria. Scores are evidence-based and consistent. The review family's cognitive 4 is accurate and should not be inflated.

4. **Monitor review-requirements adoption** (P3): Newly added; watch for trigger coverage (scenario-map `requirements_review` and `project_start` optional) and correct any missing README.md governance warnings after next CI run.

---

## Summary

| Status | Count | % |
| :--- | :--- | :--- |
| validated | 47 | 97.9% |
| experimental | 1 | 2.1% |
| archive_candidate | 0 | 0% |
| **Total** | **48** | |

| Market position | Count |
| :--- | :--- |
| differentiated | 27 |
| commodity | 20 |
| experimental | 1 |

Inventory health is high. The single experimental skill (install-rules) has a clear promotion path. No archive candidates. The new `review-requirements` skill fills the requirements quality review gap identified in the delivery standard audit.
