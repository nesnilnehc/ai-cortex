---
artifact_type: rule
name: roadmap-quality
version: 3.0.0
scope: reviewing or self-checking a roadmap document
recommended_scope: user
status: active
---

# Rule: Roadmap Quality

The single source of quality criteria for roadmap generation, diagnosis and review.
A roadmap arranges requirements and defects in Now / Next / Later. Tasks belong
in source task lists, not in roadmap rows. Existing project decisions take precedence.

## 1. Completeness

- [ ] Every row identifies a requirement or defect by stable ID, meaningful name and source link; no task, task group or implementation step is an independent row.
- [ ] Rows carry an expected outcome, priority, tier and a concise current status or key blocker.
- [ ] Now / Next / Later are visible; an empty tier may say that no items are planned.
- [ ] The opening states the evolution direction in one sentence; ordering rationale is recoverable without reading task lists.

## 2. Executability

- [ ] Eligible items follow documented priority; departures carry a reason. Priority and readiness remain separate.
- [ ] Now items have checked prerequisites and a verifiable completion condition, stated briefly or linked to source acceptance criteria.
- [ ] Next items identify material start conditions; Later items identify a re-evaluation trigger without invented dates or detailed commitments.
- [ ] Missing approval, a pause or an unresolved prerequisite is visible; a blocked high-priority item retains its priority and is not automatically treated as a distant direction.
- [ ] No effort, staffing, quota or item-count gate is invented. Explicit project capacity decisions are preserved and summarized only where they affect the plan.

## 3. Clarity

- [ ] A reader can identify current priorities, subsequent work and key blockers from the main view in about one minute; check by summarizing those three things using the main view alone.
- [ ] Requirement outcomes describe the capability or result; defect outcomes describe the expected behavior to restore. Useful feature and defect names are allowed.
- [ ] No task IDs, implementation steps, test counts, detailed acceptance procedures or historical reconciliation are copied into rows. Link to sources instead.
- [ ] Metrics, strategic hypotheses and evidence appear only where they change a planning decision; they may be linked and are not mandatory sections per tier.
- [ ] When a numeric success threshold is used, its current value, target and reference point are recoverable in the text or linked source. Unknown values are labeled, not invented.

## 4. Soundness

- [ ] Roadmap summaries agree with source requirement and defect records; placement does not grant approval, execution or release authorization.
- [ ] Dependency and priority decisions have traceable evidence or an explicit strategic rationale; no scoring framework is mandatory merely to display an item.
- [ ] Detailed progress and acceptance evidence have one source of truth; task counts are not used as proof that a requirement or defect is complete.
- [ ] Reordering follows a material change in priority, readiness or strategy. If the project declares a change-frequency window and threshold, evaluate them from history; without a defined window, do not invent a frequency verdict.

## 5. Traceability

- [ ] Requirements and defects trace to project goals in their sources or a concise mapping; links supply detail without repeating it.
- [ ] The roadmap states that backlog requirements and defects map to the roadmap and that items outside it are not done by default.
- [ ] The last-updated date is recorded.
- [ ] Paused or excluded items affecting current decisions have a brief reason and restart or re-evaluation condition; exhaustive coverage may link to a source index.

## Related assets

Consumers, resolved through the Skills registry: `define-roadmap`, `review-roadmap`,
`promote-roadmap-items`, `update-roadmap` and `plan-next`.
The presentation template is bundled with `define-roadmap`; this rule judges
substance rather than requiring a fixed number of sections or rows.
