---
artifact_type: audit-report
created_by: curate-skills
created_at: 2026-04-09
status: final
lifecycle: governance
---

# ASQM Skill Curation Audit — 2026-04-09 (Final)

**Audit Date**: 2026-04-09
**Scope**: 58 skills (`skills/*/SKILL.md`)
**Method**: ASQM strict + `cognitive_mode` guardrails + lifecycle dual-gate

---

## Part I: Lifecycle Distribution

| Status | Count | % | Rule |
| :--- | :---: | :---: | :--- |
| validated | 54 | 93% | `asqm_quality >= 17` and `agent_native >= 4` and `stance >= 3` |
| experimental | 4 | 7% | `asqm_quality >= 10` but not validated |
| archive_candidate | 0 | 0% | `asqm_quality < 10` |

**Result**: lifecycle mapping is consistent (0 status mismatches against formula).

---

## Part II: Scoring Formula & Dimension Checklist

### Formula

```text
asqm_quality = agent_native + cognitive + composability + stance
# each dimension in [0,5], total in [0,20]
```

### Gates

- Gate A (agent-ready): `agent_native >= 4`
- Gate B (design integrity): `stance >= 3`

### Dimension checklist

- `agent_native`: machine-consumable contract completeness
- `cognitive`: reasoning offload quality
- `composability`: handoff and pipeline friendliness
- `stance`: boundary clarity and spec/rule alignment

### cognitive_mode guardrail

- `interpretive`: `cognitive <= 4` (4 is correct ceiling)
- `procedural`: `cognitive <= 5`

**Validation result**:

- all 58 skills have `cognitive_mode`
- all interpretive skills satisfy `cognitive <= 4`
- all 58 skills satisfy `asqm_quality == score sum`

---

## Part III: Mode Distribution

| cognitive_mode | Count | % |
| :--- | :---: | :---: |
| interpretive | 47 | 81% |
| procedural | 11 | 19% |

---

## Part IV: Overlap & Ecosystem Findings

### A. Documentation governance cluster (post-refactor)

- `discover-docs-norms` (discover/propose only)
- `define-docs-norms` (apply/write norms)
- `assess-docs` (core assessment)
- `assess-docs-code-alignment` (code-doc gap)
- `assess-docs-links` (graph/link health)
- `assess-docs-ssot` (SSOT audit)
- `audit-docs` (read-only orchestration)
- `plan-next` (planning-first routing)

### B. Boundary quality

- `discover` vs `define` split is now explicit and enforceable
- `assess-docs` has been decomposed from monolith to composable specialist skills
- `audit-docs` now aligns with audit semantics (read-only orchestration)
- `plan-next` defaults to planning-only (`execute=false`)

### C. Market position

- The above governance cluster remains **differentiated** and internally composable
- Overlap now reflects intentional workflow composition, not semantic ambiguity

---

## Part V: Key Findings

1. **Major semantic alignment improvement**: skill names now better match behavior boundaries.
2. **Hard consistency defects fixed**: score-sum mismatch and interpretive cognitive ceiling violations were corrected.
3. **Lifecycle remains healthy**: 54 validated / 4 experimental / 0 archive-candidate.
4. **Registry integrity preserved**: manifest + INDEX + skill files remain consistent.
5. **merge-worktree v0.2.0**: CWD safety fix — `cd <main-repo-path>` before `git worktree remove` to prevent shell CWD breakage. README/INDEX synced to validated/18 (was stale at experimental/16). Scores unchanged (AN=4, COG=5, COMP=4, ST=5).

---

## Part VI: Experimental Skills

| Skill | ASQM | Primary blocker | Suggested next action |
| :--- | :---: | :--- | :--- |
| discover-skills | 15 | composability/stance depth | add stricter machine-readable recommendation schema |
| conduct-retro | 16 | output contract depth | add explicit output contract appendix |
| decontextualize-text | 16 | composability clarity | add stronger structured IO contract |
| investigate-root-cause | 16 | stance/composability depth | expand deterministic checkpoints in output contract |

---

## Part VII: Summary Table (Refactor-Impacted Skills)

| Skill | Mode | AN | COG | COMP | ST | ASQM | Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| discover-docs-norms | interpretive | 5 | 4 | 5 | 5 | 19 | validated |
| define-docs-norms | interpretive | 5 | 4 | 4 | 5 | 18 | validated |
| assess-docs | interpretive | 5 | 4 | 5 | 5 | 19 | validated |
| assess-docs-code-alignment | interpretive | 5 | 4 | 5 | 5 | 19 | validated |
| assess-docs-links | interpretive | 5 | 4 | 5 | 5 | 19 | validated |
| assess-docs-ssot | interpretive | 5 | 4 | 5 | 5 | 19 | validated |
| audit-docs | interpretive | 5 | 4 | 5 | 5 | 19 | validated |
| plan-next | interpretive | 5 | 4 | 4 | 5 | 18 | validated |

---

## Part VIII: Recommendations (Final)

### Immediate

1. Keep the new docs-governance split as the canonical architecture (discover/define + assess-specialists + read-only audit orchestrator).
2. Continue enforcing `interpretive => cognitive<=4` and `asqm_quality==sum` in future curation runs.

### Next Sprint

1. Run targeted `refine-skill-design` on the 4 experimental skills listed above.
2. Add a lightweight reusable schema snippet for recommendation-style outputs to improve composability consistency.

### No-Change Decisions

1. No rollback recommended for the recent governance-skill refactor.
2. No lifecycle downgrade required for refactor-impacted skills.

---

**Audit conclusion**: skill inventory remains stable and improved after aggressive boundary refactor.
**Next review window**: 2026-07.

---

## Part IX: Delta Update — 2026-04-16

### Scope

- `define-strategic-pillars`
- `design-strategic-goals`

### Re-scoring result

- No ASQM score changes required.
- Both skills remain `validated` with `asqm_quality = 18`.
- Gate A (`agent_native >= 4`) and Gate B (`stance >= 3`) both pass.

### Normalization changes

- Standardized Chinese README wording and section consistency.
- Corrected related-skill references to canonical skill IDs (`design-strategic-goals`, `define-roadmap`, `define-milestones`).
- Refined overlap mapping in `agent.yaml` to reflect upstream/downstream adjacency.

### Recommendations (Final)

1. Keep current scores unchanged for both skills.
2. When strategic chain skills change, run focused curation on adjacent nodes (`define-vision`, `define-north-star`, `define-roadmap`) to keep overlap graph fresh.
3. No lifecycle downgrade or archive action recommended.
