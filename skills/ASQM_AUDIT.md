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
5. **merge-worktree v0.3.0**: CWD safety hardened with two-layer guard — Step 1 `cd <main-repo-path>` immediately after detection (whole flow runs from main repo), plus Step 6 explicit `pwd` check + halt before `git worktree remove`. Addresses recurring "shell CWD points to deleted directory" friction observed in usage insights (April 2026). Scores unchanged at 18/20 (AN=4, COG=5, COMP=4, ST=5); stance reinforced by redundant guards. Status: validated.
6. **plan-next v4.0.0** (breaking): output contract changed from `document-artifact` to `chat`; cognitive-loop.md artifact deprecated (see ADR-20260417). Behavior fully restructured around MECE 5×4 routing matrix (5 themes Why/What-When/How/Is/Rules × 4 gap types G1-G4 Absent/Incomplete/Inconsistent/Disorganized). Added stop condition formalism (DONE/DEFERRED/ESCALATED), Anti-Patterns section (6 rules), matrix-aware Self-Check (7 items), real conversation examples. Score lift: composability 4 → 5 (Skill Boundaries table covers all action verbs × executors with explicit ESCALATED return path). Final 19/20 (AN=5, COG=4 interpretive ceiling, COMP=5, ST=5). overlaps_with reduced from 3 to 2 (align-planning removed — now an explicit handoff target, not overlap). Status: validated.
7. **Value-driven prioritization model implementation (2026-04-17)**: ADR 1 (unified value-driven prioritization) + ADR 2 (work lifecycle & skill responsibilities) landed, driving a coordinated 7-skill change batch:
   - **design-strategic-goals v1.1.0**: mandatory engineering-health goal for long-term projects. Scores unchanged at 18/20 (AN=5, COG=4, COMP=4, ST=5).
   - **capture-work-items v1.1.0**: `strategic_goal_id` required; Phase 5 suggests (not auto-invokes) `prioritize-backlog`. Score lift: COMP 4 → 5 (bidirectional handoff with design-strategic-goals upstream and prioritize-backlog downstream). 18 → 19/20.
   - **prioritize-backlog v1.0.0** (new): multi-framework scoring (RICE + WSJF + MoSCoW + ICE) with explicit disagreement surfacing; user-decided final priority; writes `priority_decision` with framework breakdown. 19/20 (AN=5, COG=4, COMP=5, ST=5). `overlaps_with: []` — differentiated.
   - **promote-roadmap-items v1.0.0** (new): event-driven roadmap planning ceremony support; capacity controlled per strategic_goal; updates roadmap.md and item status. Named per verb-noun rule (prior `plan-roadmap-pull` rejected as modifier-form violation). 19/20. `overlaps_with: []` — differentiated.
   - **define-roadmap v3.1.0**: mandatory capacity allocation per strategic_goal (sum=100%, engineering-health non-zero). Score lift: COMP 4 → 5 (provides capacity contract for promote-roadmap-items). 18 → 19/20.
   - **plan-next v5.0.0**: added Phase 0.6 state machine (S1-S7, interpreter over matrix — not replacement) and Phase 1.5 two-layer output (Primary state-focused + Secondary full-matrix compressed preserving MECE). Low-confidence fallback to full-matrix. Anti-Pattern added against using state machine as filter. Scores unchanged at 19/20. Positioning explicitly called out: state machine is matrix's interpreter, two-layer output is presentation layer above data+interpretation.
   - **align-planning**: README updated to spell out backward-looking role complementary to plan-next's forward role. No behavior change; no rescoring.

   Full workflow now: design-strategic-goals → define-roadmap → capture-work-items → prioritize-backlog → promote-roadmap-items → execute → align-planning. plan-next v5 monitors governance health at any point. All steps event-driven, no Sprint cadence assumption. overlaps_with cleanup for new skills: handoff chains are NOT overlaps; only genuine user-confusion-potential counts.

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

---

## Part X: Delta Update — 2026-04-17 (prioritize-backlog v2.0.0)

### Scope

- `prioritize-backlog` (v1.0.0 → v2.0.0): breaking behavior change — forced blanket re-score (ignores existing `priority`/`priority_decision`); backlog-shape auto-detection extended to four modes (`multi-file`, `yaml-list`, `h2-yaml`, `table`); `priority_decision.previous` added to output contract.

### Re-scoring result

- **No ASQM score changes**: AN=5, COG=4 (interpretive ceiling), COMP=5, ST=5 → `asqm_quality = 19`. Gates A+B both pass. Status remains **validated**.
- The mode-dispatch table and the `previous` field sharpen an already-explicit output contract (AN already at ceiling).
- Stance is reinforced — new anti-patterns (no pre-overwrite comparison, no dual-write across modes, no silent drop of old values) encode stronger design discipline, but stance was already at 5.
- Composability marginally improved (skill now plugs into single-file-backlog projects too) but already at 5.

### Overlap & market position

- `overlaps_with: []` unchanged; job remains uniquely "parallel multi-framework scoring with surfaced disagreement".
- `market_position: differentiated` unchanged.

### Normalization changes

- `agent.yaml.primary_use` updated to reflect blanket re-score + multi/single-file coverage.
- `SKILL.md` description + input/output schemas rewritten; examples refreshed (added h2-yaml single-file example; removed obsolete `single-item=true` escape-hatch example).
- `README.md` aligned.
- `skills/INDEX.md` version bumped `1.0.0 → 2.0.0` with matching description (INDEX is hand-maintained per `verify-registry.mjs`).

### Recommendations (Final)

1. Keep scores unchanged; no lifecycle change.
2. When `promote-roadmap-items` is next touched, confirm it tolerates the new `priority_decision.previous` field (currently reads only `priority`, so backward-compatible).
3. If usage surfaces a 5th single-file backlog shape in practice, revisit mode detection; do not pre-emptively add modes.
