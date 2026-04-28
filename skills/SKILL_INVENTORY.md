# Skill Inventory — AI Cortex

**Generated**: 2026-04-28
**Source**: `skills/*/agent.yaml` via `scripts/generate-skill-inventory.mjs`
**Scope**: `skills/` — 61 skills

---

## Status Rule

Per [ADR 008](../docs/architecture/adrs/008-replace-asqm-with-acceptance-criteria.md):

```
validated         = has_output_contract AND len(acceptance_criteria) >= 1
experimental      = otherwise
archive_candidate = manual only
```

No scoring system. ASQM (`scores`, `asqm_quality`, `validation_gates`, `cognitive_mode`) was removed in full on 2026-04-28.

---

## Distribution

| Bucket | Count | % |
|---|---|---|
| validated | 61 | 100.0% |
| experimental | 0 | 0.0% |
| archive_candidate | 0 | 0.0% |

### Output contract coverage

- has_output_contract: true → **61 / 61** (100.0%)
- has_output_contract: false → **0 / 61**

### acceptance_criteria coverage

- skills with ≥1 acceptance_criterion → **61 / 61**
- skills with 0 acceptance_criteria  → **0 / 61**

---

## All Skills

| Skill | status | has_output_contract | acceptance_criteria | market_position |
|---|---|---|---|---|
| align-architecture | validated | true | 3 | differentiated |
| align-backlog | validated | true | 3 | differentiated |
| align-planning | validated | true | 3 | differentiated |
| align-work-item-manifest | validated | true | 3 | differentiated |
| analyze-requirements | validated | true | 3 | differentiated |
| assess-docs | validated | true | 2 | differentiated |
| assess-docs-code-alignment | validated | true | 2 | differentiated |
| assess-docs-links | validated | true | 2 | differentiated |
| assess-docs-ssot | validated | true | 2 | differentiated |
| audit-docs | validated | true | 3 | differentiated |
| auto-iterate | validated | true | 2 | differentiated |
| automate-repair | validated | true | 2 | commodity |
| automate-tests | validated | true | 2 | commodity |
| bootstrap-docs | validated | true | 2 | differentiated |
| breakdown-tasks | validated | true | 3 | differentiated |
| capture-work-items | validated | true | 3 | differentiated |
| commit-work | validated | true | 2 | differentiated |
| curate-skills | validated | true | 3 | differentiated |
| decontextualize-text | validated | true | 2 | differentiated |
| define-docs-norms | validated | true | 2 | differentiated |
| define-mission | validated | true | 2 | differentiated |
| define-north-star | validated | true | 2 | differentiated |
| define-roadmap | validated | true | 3 | differentiated |
| define-strategic-pillars | validated | true | 2 | differentiated |
| define-vision | validated | true | 2 | differentiated |
| design-solution | validated | true | 3 | differentiated |
| design-strategic-goals | validated | true | 2 | differentiated |
| discover-docs-norms | validated | true | 2 | differentiated |
| discover-skills | validated | true | 2 | differentiated |
| generate-agent-entry | validated | true | 2 | differentiated |
| generate-github-workflow | validated | true | 2 | differentiated |
| generate-standard-readme | validated | true | 2 | commodity |
| install-rules | validated | true | 2 | experimental |
| investigate-root-cause | validated | true | 2 | differentiated |
| merge-worktree | validated | true | 3 | differentiated |
| plan-next | validated | true | 3 | differentiated |
| prioritize-backlog | validated | true | 3 | differentiated |
| promote-roadmap-items | validated | true | 2 | differentiated |
| refine-skill-design | validated | true | 2 | differentiated |
| review-architecture | validated | true | 2 | differentiated |
| review-code | validated | true | 2 | differentiated |
| review-codebase | validated | true | 2 | commodity |
| review-diff | validated | true | 2 | commodity |
| review-dotnet | validated | true | 2 | differentiated |
| review-go | validated | true | 2 | differentiated |
| review-java | validated | true | 2 | differentiated |
| review-orm-usage | validated | true | 2 | differentiated |
| review-performance | validated | true | 2 | commodity |
| review-php | validated | true | 2 | differentiated |
| review-powershell | validated | true | 2 | differentiated |
| review-python | validated | true | 2 | differentiated |
| review-react | validated | true | 2 | commodity |
| review-requirements | validated | true | 2 | differentiated |
| review-security | validated | true | 2 | differentiated |
| review-sql | validated | true | 2 | commodity |
| review-testing | validated | true | 2 | commodity |
| review-typescript | validated | true | 2 | commodity |
| review-vue | validated | true | 2 | commodity |
| sync-release-docs | validated | true | 2 | differentiated |
| tidy-repo | validated | true | 2 | differentiated |
| warn-destructive-commands | validated | true | 2 | commodity |

---

## Skills missing output contract

_None._

---

## Skills missing acceptance_criteria

_None._

---

## Maintenance Protocol

- This file is **regenerated** by `node scripts/generate-skill-inventory.mjs`. Do not hand-edit.
- `curate-skills` re-runs the generator after batch updates to `agent.yaml`.
- A skill flips from `experimental` to `validated` only when its `SKILL.md` has an output-contract appendix **and** `agent.yaml` has at least one `acceptance_criteria` entry.
- `archive_candidate` is set manually by a maintainer; the rule never assigns it.

---

## Final Recommendations

1. **Phase 10 (review-* output contracts)** — 0 review-* skills still lack output contracts; batch-add YAML schema appendix.
2. **Phase 11 (governance skills)** — high-composability skills (plan-next, align-*, audit-docs) need output contracts to feed downstream consumers.
3. **Phase 12 (strategy + procedural)** — remaining 0 skills (define-*, design-*, generate-*, sync-*, tidy-*, etc.) follow.
4. **Acceptance criteria backfill** — all 0 skills need at least one observable input→output assertion to flip to `validated`.
