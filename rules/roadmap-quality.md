---
artifact_type: rule
name: roadmap-quality
version: 4.10.1
scope: reviewing or self-checking a roadmap document
recommended_scope: user
status: active
---

# Rule: Roadmap Quality

The single source of quality criteria for roadmap generation, diagnosis and review.
A roadmap arranges requirements and defects in Now / Next / Later, optionally
adding iteration/version and schedule views under [roadmap modeling](../specs/roadmap-modeling.md).
Tasks belong in source task lists, not in requirement rows. Version groups and
schedule milestones are valid presentation units. Existing project decisions take precedence.

## Review scope and structure drafts

- [ ] Identify the requested stage entry and review scope under the [stage contract](../specs/roadmap-modeling.md#stage-entries-authorization-and-acceptance); artifact population alone does not select scope. Structure and content results are distinct, including in a continuous request.
- [ ] Verify authorization at the stage boundary: structure confirmation or available source facts alone never authorizes population; already authorized continuous work does not require another confirmation. Planning does not replace settled business decisions or authorize implementation/publication.
- [ ] A structure-only review or repair of a populated plan preserves its business facts. Content planning reuses settled structure; unknown facts and unresolved business choices remain explicit, with no full pass for unevaluated applicable criteria.
- [ ] Identify whether the artifact is an intentionally blank structure or a populated plan, using the request and artifact rather than guessing from empty cells.
- [ ] For a structure draft, check the selected document roles, required columns/fields, main-to-detail navigation, one clear entry, consistent headings/field-label style/placeholders and empty tables. Do not demand business rows, dates, owners, versions or evidence the user explicitly deferred.
- [ ] Check the [reader-facing content boundary](workflow-documentation.md#structure-and-reader-facing-content): no field-filling instructions, enum tutorials, agent work orders or discussion residue in blank templates or completed reader deliverables. Necessary business rationale and actual constraints are not author guidance.
- [ ] A structure-scoped review reports structural findings and business criteria as not evaluated; it MUST NOT claim full roadmap approval. For content-scoped or combined review apply all applicable criteria below, reporting unavailable evidence separately.
- [ ] If content review is requested on an empty draft, preserve the requested scope and report its missing business basis/cannot-evaluate criteria; do not populate, substitute a structure-only review or certify content.
- [ ] Compare against the retained layout, not an arbitrary document count. Distinguish Spec conformance, template organization and exact named-example replication; disclose actual differences. Re-review with no new finding or evidence does not demand a rewrite.

## 1. Completeness

- [ ] Every requirement-view row identifies a requirement or defect by stable ID, meaningful name and source link; no task, task group or implementation step is an independent requirement row. Version groups reference those IDs rather than duplicating their records.
- [ ] Rows carry an expected outcome, priority, tier, separate approval and execution status columns, and a separate key conditions column.
- [ ] Now / Next / Later are visible; an empty tier may say that no items are planned.
- [ ] The opening states the evolution direction in one sentence; ordering rationale is recoverable without reading task lists.

### Execution status vocabulary

Each execution status cell contains exactly one of the following canonical labels
or its one-to-one display translation under the selected deliverable language,
with no badges, qualifiers, evidence or combined states. This is a presentation
vocabulary; map project source fields explicitly rather than replacing their schema.

| Execution status | Definition and boundary |
| --- | --- |
| Not started | Execution has not begun; approval or tier placement alone does not mean work started. |
| In progress | Work is actively underway, including rework after failed acceptance. A risk alone does not mean progress is blocked. |
| Awaiting acceptance | Development or repair is complete according to the source, but required acceptance is pending or not yet verified. |
| Awaiting release | Required acceptance has passed, but a release required for project closure is outstanding. This label grants no release authorization. |
| Paused | An explicit project decision intentionally suspends work; record the reason and resume condition separately. |
| Blocked | A necessary prerequisite prevents the next required step; record the blocker and unblock condition separately. Ordinary planned acceptance or release waiting uses the corresponding waiting label. |
| Completed | Source evidence meets the project's declared closure criterion, including acceptance and production release where required. Development completion alone is insufficient. |

- [ ] Every execution status cell uses exactly one label above. If source evidence is missing or conflicting, report the mapping as unverified outside the cell; do not invent a status or certify a complete roadmap.
- [ ] Approval is shown separately using the project's own labels (or explicitly unverified / not applicable). Now / Next / Later, priority and approval never substitute for execution status.
- [ ] Key conditions contain only a short next-step prerequisite, blocker or completion condition with a source link; use `—` when none applies. Put mitigation detail, test counts, commit records, history and detailed evidence in linked sources, never in execution status cells.
- [ ] The roadmap states or links the project's closure criterion: whether closure requires acceptance, production release, or another existing project-defined delivery condition. Do not invent a release gate for non-release work. If closure is undefined, report it as unresolved and do not mark the item Completed.

## 2. Executability

- [ ] Eligible items follow documented priority; departures carry a reason. Priority and readiness remain separate.
- [ ] Now items have checked prerequisites for the next intended step and a verifiable completion condition, stated briefly or linked to source acceptance criteria. Later-needed dependencies permit grounded parallel work with a visible need-by condition; an entire prerequisite requirement need not be complete. Unknown evidence is not a readiness pass.
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

- [ ] Each status transition is backed by the authoritative source record and its applicable acceptance/release evidence. Development complete, acceptance passed and production released are distinct facts; none substitutes for another. A failed acceptance returns to In progress only when rework has actually started. Paused or Blocked overrides the underlying stage only while its recorded decision or impediment applies. If both apply, show Paused for an explicit suspension decision and retain the blocker in key conditions; resume from current evidence, not automatically from the previous label.
- [ ] Roadmap summaries agree with source requirement and defect records; placement does not grant approval, execution or release authorization.
- [ ] Dependency and priority decisions have traceable evidence or an explicit strategic rationale; no scoring framework is mandatory merely to display an item.
- [ ] Priority policy is the reusable rule; arrangement rationale explains its current application and verified conditions, not a second scoring scheme. Existing decision links are valid. Stable presentation order is not falsely claimed as business precedence.
- [ ] An independent policy is linked with only a useful summary, not copied as another editable authority. Current policy results link to item/roadmap decisions; historical application snapshots are identified as such.
- [ ] Detailed progress and acceptance evidence have one source of truth; task counts are not used as proof that a requirement or defect is complete.
- [ ] Reordering follows a material change in priority, readiness or strategy. If the project declares a change-frequency window and threshold, evaluate them from history; without a defined window, do not invent a frequency verdict.

## 5. Traceability

- [ ] Requirements and defects trace to project goals in their sources or a concise mapping; links supply detail without repeating it.
- [ ] The roadmap states that backlog requirements and defects map to the roadmap and that items outside it are not done by default.
- [ ] The last-updated date is recorded.
- [ ] Paused or excluded items affecting current decisions have a brief reason and restart or re-evaluation condition; exhaustive coverage may link to a source index.

## 6. Selected views and delivery

- [ ] View selection is explicit; discuss cadence and appropriate delivery/schedule views at first creation and retain the user's choice. An existing single-view roadmap is valid without mandatory expansion.
- [ ] A new or changed destination is confirmed by the user; established destination choices are reused during maintenance. No synchronization or competing editable source is introduced.
- [ ] Selected version views show member references, core outcome, owner and target window; unknowns and unassigned entries are explicit. Version membership does not imply approval or a complete release.
- [ ] Selected schedules distinguish target, committed and actual timing, state their calendar/origin, show unknown timing as unscheduled, and agree with member/version scope. Relative weeks do not masquerade as real dates.
- [ ] Dependencies and known timing agree; cycles, finish-to-start overlaps, unresolved timing and missing scope are reported rather than silently repaired. Resource availability is not inferred from date arithmetic.
- [ ] Every status, scope or time change checks all selected views in the chosen destination. Detailed tasks and evidence retain one authoritative source.
- [ ] Platform delivery claims have receipts or read-back evidence. A generated SVG is not proof of a successful remote upload; unavailable rendering or connector operations are explicit limitations.

## Related assets

Consumers, resolved through the Skills registry: `define-roadmap`, `review-roadmap`,
`promote-roadmap-items`, `update-roadmap`, `plan-next` and `archive-milestone`.
The presentation template is bundled with `define-roadmap`; this rule judges
substance rather than requiring a fixed number of sections or rows.

## Phase and event integrity

- A version groups delivery scope; a phase is work over time; a milestone is an event.
  Relationships need not form a strict tree. Use the [Roadmap Spec](../specs/roadmap-modeling.md).
- Phase scope and exit conditions MUST be source-backed. Milestones MUST identify
  an owner and occurrence criterion; non-planned states MUST link evidence.
- Time passage or member completion MUST NOT automatically reach an event or grant
  approval. An actual event time MUST correspond to a reached event.
- Multiple events for one version MUST NOT overwrite its span or each other's IDs.
  Unknown timing MUST remain unknown. Legacy 1.0 and single-view plans remain valid.

## Revision traceability

- [ ] Material priority/tier, scope, phase, timing/commitment, exclusion and milestone
  state changes have a dated before/after summary, reason, impact and source link
  under [the revision contract](../specs/roadmap-modeling.md#54-revision-records).
- [ ] The main roadmap shows the latest five summaries; older records remain in a
  resolving history source. Regeneration, correction and archiving preserve history.
- [ ] Repeated generation does not create duplicate decisions. Revision IDs and dates
  agree across selected views and source records; history is not current scope.
- [ ] Legacy adoption discloses the baseline and any unknown earlier history. Missing
  reconstructed history is not a defect; a known material change after adoption
  without a record is. Formatting-only changes need no planning revision.

## Reading structure and iteration integrity

- [ ] The main roadmap alone explains direction, ordering, active priorities, blockers,
  near-term delivery and key events where known. Split output is not a link-only index.
- [ ] The overview emphasizes the plan and material unknowns; unverified execution is visible before rows. Policy/closure definitions and view/layout/language evidence remain recoverable but do not displace the plan. Detailed dependencies do not overload one arrangement paragraph.
- [ ] Document names distinguish policy, plan, basis and history under the Spec's naming advice. Existing project paths/URLs are respected; missing optional child documents or nondefault titles alone are not defects.
- [ ] Delivery objects are grouped under selected delivery views; completed work is
  folded or linked separately without rewriting tiers/statuses. Empty optional
  chapters and repeated priority inventories do not obscure the current plan.
- [ ] Splitting follows reader, owner, update cadence or volume needs. Detail pages
  link back; each scope/date/status fact has one editable source. Every affected
  projection is refreshed for the same decision and revision ID.
- [ ] Selected iteration views show cadence, goals, source-backed scope, owner,
  timeboxes or explicit unknowns, version mapping and execution-detail links when
  available. Unallocated work remains visible; far-future timeboxes are not invented.
- [ ] Iteration carry-over is distinct from version scope change, tier movement and
  completion. Iteration end does not prove phase exit, event occurrence or release.
- [ ] Iteration goal/scope/cadence/timebox changes retain material revision evidence.
  Generated detail/history files do not replace their authoritative source records.

## Scenario choice and intake

- [ ] New planning reads existing choices and source facts before asking questions;
  questions target only missing cadence, delivery, audience or constraint evidence.
- [ ] The recommendation names a primary perspective, supporting/omitted views,
  layout, rationale and source basis; recipe advice is not a mandatory framework.
- [ ] The chosen combination has one retained source. Maintenance reuses views,
  layout, primary perspective and destination without repeating settled questions.
- [ ] Conflicting or changed context is surfaced for reconsideration while existing
  choices remain intact; a default recommendation never replaces a team decision.
- [ ] Selected flow policies, service expectations and metrics have project evidence
  or explicit unknowns. No default WIP number, invented cycle or fake iteration appears.
- [ ] Schema 1.4 explicitly controls phase/event/flow registers and retained layout;
  custom choices are evaluated for consistency, not conformity to a recipe.

## 7. Deliverable language

- [ ] Language follows the [resolution order](../specs/roadmap-modeling.md#57-deliverable-language-schema-15): user instruction, consuming-project policy, retained artifact, then supported audience/document context. Only unresolved or conflicting winning evidence requires a question; conversation language alone is insufficient.
- [ ] The choice and its basis are recoverable from existing norms or planning decisions and survive handoffs and ordinary maintenance. New options do not reset it; higher-priority explicit changes are applied within authorization.
- [ ] Main/detail documents and diagrams use consistent headings, headers, statuses, summaries, legends and accessible descriptions. Free text is checked separately from generated labels; generator success alone proves no prose-language consistency.
- [ ] Localized execution labels preserve the canonical state meanings and source mapping. IDs, references, machine fields and enums are unchanged; translated approval labels do not create new approval states.
- [ ] Historical originals and source evidence remain intact. Parallel language editions, when requested, agree on scope, dates, priorities, states, membership and commitments. Unknown language or inaccessible evidence is reported as a limitation, not an inferred pass. Legacy metadata absence alone is not a defect.

## Existing-project alignment

- [ ] First alignment follows the Spec's preservation boundary: review distinguishes structural repairs, evidence gaps and business changes; before/after known facts and stable IDs/URLs/anchors agree unless a separate authorized decision changed them.
- [ ] A missing conventional filename is not mistaken for no roadmap. Existing views, source-label meanings, language and destination are retained; generator limitations do not force migration or invented fields.
- [ ] Alignment alone does not trigger scoring, promotion, strategy creation, new delivery commitments or archive deletion. Missing sources remain explicit and are routed without silently executing those actions.
- [ ] Adoption records the actual baseline and unknown prior history. Re-review reports remaining limitations, and repeated no-op alignment adds no duplicate document or revision.
