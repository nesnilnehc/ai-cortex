# ASQM Audit — AI Cortex Skills

**Audit date**: 2026-04-28  
**Auditor**: curate-skills v2  
**Scope**: `skills/` — 62 skills  

---

## Scoring Formula

```
asqm_quality = agent_native + cognitive + composability + stance  (0–20)

Lifecycle:
  validated        → quality ≥ 17 AND agent_native ≥ 4 AND stance ≥ 3
  experimental     → quality ≥ 10
  archive_candidate→ otherwise
```

### Dimension Checklist

| Dimension | 5 (max) | 4 | ≤3 |
|-----------|---------|---|-----|
| agent_native | Explicit machine-parsable output contract (Appendix / schema) in SKILL.md | Structured outputs described in prose | Vague or missing |
| cognitive | procedural: all branches deterministic; interpretive: 4 is the ceiling (correct design) | Most branches explicit or LLM judgment is core value | Minimal reasoning offload |
| composability | Clean handoff; consumed by ≥2 downstream skills | Feeds one downstream or partially composable | Standalone only |
| stance | MUST/MUST NOT hard rules + verification criteria + explicit output contract | Good spec alignment, scope boundaries | Weak or absent |

---

## Lifecycle by Status

### Validated (59 skills)

| Skill | Quality | agent_native | cognitive | composability | stance | Mode |
|-------|---------|-------------|-----------|---------------|--------|------|
| align-architecture | 19 | 5 | 4 | 5 | 5 | interpretive |
| align-backlog | 17 | 4 | 4 | 4 | 5 | interpretive |
| align-planning | 19 | 5 | 4 | 5 | 5 | interpretive |
| align-work-item-manifest | 17 | 4 | 4 | 4 | 5 | procedural |
| analyze-requirements | 19 | 5 | 4 | 5 | 5 | interpretive |
| assess-docs | 19 | 5 | 4 | 5 | 5 | interpretive |
| assess-docs-code-alignment | 19 | 5 | 4 | 5 | 5 | interpretive |
| assess-docs-links | 19 | 5 | 4 | 5 | 5 | interpretive |
| assess-docs-ssot | 19 | 5 | 4 | 5 | 5 | interpretive |
| audit-docs | 19 | 5 | 4 | 5 | 5 | interpretive |
| auto-iterate | 18 | 5 | 4 | 5 | 5 | procedural |
| automate-repair | 17 | 4 | 4 | 4 | 5 | procedural |
| automate-tests | 17 | 4 | 4 | 4 | 5 | procedural |
| bootstrap-docs | 18 | 5 | 4 | 4 | 5 | procedural |
| breakdown-tasks | 18 | 5 | 4 | 4 | 5 | interpretive |
| capture-work-items | 19 | 5 | 4 | 5 | 5 | procedural |
| commit-work | 18 | 5 | 4 | 4 | 5 | interpretive |
| curate-skills | 18 | 5 | 4 | 4 | 5 | interpretive |
| define-docs-norms | 18 | 5 | 4 | 4 | 5 | interpretive |
| define-mission | 18 | 5 | 4 | 4 | 5 | interpretive |
| define-north-star | 18 | 5 | 4 | 4 | 5 | interpretive |
| define-roadmap | 19 | 5 | 4 | 5 | 5 | interpretive |
| define-strategic-pillars | 18 | 5 | 4 | 4 | 5 | interpretive |
| define-vision | 18 | 5 | 4 | 4 | 5 | interpretive |
| design-solution | 18 | 5 | 4 | 4 | 5 | interpretive |
| design-strategic-goals | 18 | 5 | 4 | 4 | 5 | interpretive |
| discover-docs-norms | 19 | 5 | 4 | 5 | 5 | interpretive |
| generate-agent-entry | 18 | 5 | 4 | 4 | 5 | procedural |
| generate-github-workflow | 19 | 5 | 5 | 4 | 5 | procedural |
| generate-standard-readme | 18 | 5 | 4 | 4 | 5 | procedural |
| install-rules | 18 | 4 | 5 | 4 | 5 | procedural |
| merge-worktree | 19 | 5 | 5 | 4 | 5 | procedural |
| plan-next | 19 | 5 | 4 | 5 | 5 | interpretive |
| prioritize-backlog | 19 | 5 | 4 | 5 | 5 | interpretive |
| promote-roadmap-items | 19 | 5 | 4 | 5 | 5 | interpretive |
| refine-skill-design | 17 | 4 | 4 | 4 | 5 | interpretive |
| review-architecture | 17 | 4 | 4 | 4 | 5 | interpretive |
| review-code | 18 | 5 | 4 | 4 | 5 | interpretive |
| review-codebase | 17 | 4 | 4 | 4 | 5 | interpretive |
| review-diff | 17 | 4 | 4 | 4 | 5 | interpretive |
| review-dotnet | 17 | 4 | 4 | 4 | 5 | interpretive |
| review-go | 17 | 4 | 4 | 4 | 5 | interpretive |
| review-java | 17 | 4 | 4 | 4 | 5 | interpretive |
| review-orm-usage | 17 | 4 | 4 | 4 | 5 | interpretive |
| review-performance | 17 | 4 | 4 | 4 | 5 | interpretive |
| review-php | 17 | 4 | 4 | 4 | 5 | interpretive |
| review-powershell | 17 | 4 | 4 | 4 | 5 | interpretive |
| review-python | 17 | 4 | 4 | 4 | 5 | interpretive |
| review-react | 17 | 4 | 4 | 4 | 5 | interpretive |
| review-requirements | 17 | 4 | 4 | 4 | 5 | interpretive |
| review-security | 18 | 4 | 4 | 5 | 5 | interpretive |
| review-sql | 17 | 4 | 4 | 4 | 5 | interpretive |
| review-testing | 17 | 4 | 4 | 4 | 5 | interpretive |
| review-typescript | 17 | 4 | 4 | 4 | 5 | interpretive |
| review-vue | 17 | 4 | 4 | 4 | 5 | interpretive |
| sync-release-docs | 17 | 4 | 4 | 4 | 5 | interpretive |
| tidy-repo | 18 | 5 | 4 | 4 | 5 | interpretive |
| warn-destructive-commands | 18 | 4 | 5 | 4 | 5 | procedural |

### Experimental (3 skills)

| Skill | Quality | agent_native | cognitive | composability | stance | Mode | Gap to Validated |
|-------|---------|-------------|-----------|---------------|--------|------|-----------------|
| decontextualize-text | 16 | 4 | 4 | 4 | 4 | interpretive | quality gap=1; add hard rules → stance 4→5 |
| discover-skills | 15 | 4 | 4 | 3 | 4 | interpretive | quality gap=2; composability=3 and stance=4 both below ceiling |
| investigate-root-cause | 16 | 4 | 4 | 4 | 4 | interpretive | quality gap=1; add output contract → stance 4→5 |

### Archive Candidate (0 skills)

None.

---

## Overlap Map

### High-Overlap Clusters

**docs-assess cluster** (audit-docs orchestrates):
- `audit-docs` → `assess-docs`, `assess-docs-links`, `assess-docs-ssot`, `assess-docs-code-alignment`
- Each atomic assess-* has differentiated focus; audit-docs is the read-only orchestrator

**governance loop** (plan-next ↔ auto-iterate):
- `plan-next`: read-only diagnosis + routing
- `auto-iterate`: single-step execution consuming plan-next output
- `automate-repair`: code-fix loop (orthogonal, not substitutable)

**review cluster** (review-code orchestrates):
- `review-code` → `review-architecture`, `review-diff`, `review-codebase`, `review-security`, `review-testing`, `review-performance`
- → language atomics: `review-go`, `review-typescript`, `review-python`, `review-java`, `review-dotnet`, `review-php`, `review-powershell`
- → framework atomics: `review-react`, `review-vue`
- → library atomics: `review-orm-usage`, `review-sql`

**strategy chain** (linear, sequential):
- `define-mission` → `define-vision` → `design-strategic-goals` → `define-strategic-pillars` → `define-north-star` → `define-roadmap` → `promote-roadmap-items` → `prioritize-backlog` → `align-backlog`

**artifacts chain** (waterfall):
- `analyze-requirements` → `design-solution` → `breakdown-tasks` → (execution layer)

**docs lifecycle**:
- `discover-docs-norms` → `define-docs-norms` → `bootstrap-docs` / `assess-docs`

### Market Position Summary

| Market Position | Count | Skills (notable) |
|----------------|-------|-----------------|
| differentiated | 49 | Most governance, strategy, and meta-skills |
| commodity | 12 | automate-repair, automate-tests, generate-standard-readme, review-codebase, review-diff, review-performance, review-react, review-sql, review-testing, review-typescript, review-vue, warn-destructive-commands |
| experimental | 1 | install-rules |

---

## Ecosystem Analysis

### External Overlaps

| Skill | External Repositories |
|-------|-----------------------|
| review-code | wshobson/agents, secondsky/claude-skills, trailofbits/skills, cxuu/golang-skills, obra/superpowers, skillcreatorai/Ai-Agent-Skills |
| review-codebase | same as review-code |
| review-diff | wshobson/agents, trailofbits/skills |
| review-go | cxuu/golang-skills:go-code-review |
| commit-work | anthropics/skills, softaworks/agent-toolkit |

### Commodity Positioning Notes

Commodity-positioned skills are correctly labelled — they implement standard patterns with significant external competition. Their inventory value is composability within orchestration chains (especially review-code), not standalone differentiation.

---

## Findings

### F1 — Version history purged from `primary_use` (24 changes, this run)

**Pattern**: `v\d+.\d+ adds/refactors/adopts/retracts/simplifies` embedded in `primary_use` fields. Violates global CLAUDE.md no-version-history-in-product-docs policy.

**Affected skills**: align-architecture, align-backlog, align-planning, align-work-item-manifest, analyze-requirements, assess-docs, assess-docs-code-alignment, assess-docs-links, assess-docs-ssot, audit-docs, bootstrap-docs, breakdown-tasks, capture-work-items, define-mission, define-north-star, define-roadmap, define-strategic-pillars, define-vision, design-solution, design-strategic-goals, discover-docs-norms (primary_use + output field), plan-next (verbose block literal simplified), tidy-repo.

**Fix applied**: Stripped version narration; retained behavioral purpose.

### F2 — auto-iterate stance corrected: 4 → 5 (this run)

**Evidence**: SKILL.md Appendix contains formal YAML schema + JSON schema output contract, 6 MUST/MUST NOT hard boundary rules each with explicit verification criteria and rejection consequences, plus an AI Reconstruction Instructions section. This matches the stance=5 standard held by other validated skills with equivalent spec rigor.

**Impact**: asqm_quality 17 → 18. Status remains validated.

### F3 — discover-skills composability=3 is the floor of the inventory

**Observation**: No downstream skill explicitly consumes `discover-skills` output; composability=3 is evidence-based. The skill recommends installs but does not hand off to `install-rules` in a machine-readable contract.

**Not fixed here** (requires SKILL.md redesign): Route to `refine-skill-design`.

### F4 — Experimental cluster: 3 skills below validated threshold

- **decontextualize-text** (16/20): Add MUST/MUST NOT hard rules and output contract → stance 4→5.
- **investigate-root-cause** (16/20): Add output contract Appendix → stance 4→5.
- **discover-skills** (15/20): Both composability (3→4) and stance (4→5) gaps; needs handoff contract and hard rules.

**Not fixed here** (requires SKILL.md redesign): Route to `refine-skill-design`.

---

## Summary Table

| Status | Count | % |
|--------|-------|---|
| validated | 59 | 95% |
| experimental | 3 | 5% |
| archive_candidate | 0 | 0% |

| Metric | Value |
|--------|-------|
| Total skills | 62 |
| Quality min | 15 (discover-skills) |
| Quality max | 19 (16 skills at 19/20) |
| Quality median | 18 |
| Quality mean | ~17.9 |

---

## Recommendations

### No action required

1. **Inventory is production-ready.** 95% validated, all gate checks passing. No skills require archive or demotion.
2. **Scoring is consistent.** Interpretive cognitive ceiling (4) applied uniformly; agent_native=5 restricted to skills with explicit output contracts.

### Route to `refine-skill-design`

3. **Promote `decontextualize-text`** (16→17): Add hard-boundary section with MUST/MUST NOT rules and an output contract appendix. One point needed.
4. **Promote `investigate-root-cause`** (16→17): Same prescription. One point needed.
5. **Promote `discover-skills`** (15→17): Requires both adding composability handoff to `install-rules` (composability 3→4) and adding hard rules + output contract (stance 4→5). Two points needed.

### No change

6. **Commodity skills**: `review-codebase` and `review-diff` overlap significantly and face external competition. Current positioning (commodity/validated) is accurate — consolidation not recommended without usage data.
7. **install-rules market_position `experimental`**: Reflects early ecosystem traction. Reassess after adoption data is available; scores already validated (18/20).
