---
artifact_type: audit-docs
created_by: ai-cortex
lifecycle: living
created_at: 2026-10-27
status: active
---

# Documentation audit

The owner requested removal of the duplicate AIC-REQ-03 document chain on
2026-10-27. Its obsolete document-level review and execution summary were removed;
relevant product feedback and raw prototype evidence are retained below. Current status is governed by the
[published and publicly verified outcome](#aic-req-04-published-and-publicly-verified-2026-10-28).
Earlier sections retain their original review date and scope.

## T7 feedback: ordinary agent work versus Cortex assets, 2026-10-27

The owner correctly identified the requirement document as the place to clarify
search scope. They then noted that an agent can both ask the question and update
the document directly, without invoking a repository skill. The existing page did
not clearly explain when ordinary conversation is sufficient and when AI Cortex's
reusable methods, artifact contracts or constraints are useful. This is a confirmed
interface/content gap, not a failed answer by the owner.

The local repair places that distinction before related skills in the existing
contextual panel, uses a disclosed Skill/Spec/Rule/Protocol explanation with local
sources, and makes the default design request permit direct clarification/editing.
Already-adopted project constraints continue to apply; skills are not presented as
a mandatory extra step for every conversation. The scenario now explicitly refers
to an existing requirement document. Approved snapshots remain unchanged; this is
an owner-requested explanatory repair within the current prototype scope.

T7 is In Progress. The owner has not yet supplied all remaining scenario answers.
Continue with one question at a time after they inspect the repaired explanation.

## T7 feedback: multiple help perspectives, 2026-10-27

The owner noted that comparing what an agent can do first depends on the reader's
experience and should not organize the page. They explicitly authorized a local
point/line/plane refinement, retaining one map and click-to-explain, with ordinary
conversation boundaries inside specific scenarios. They also emphasized that the
three terms can carry different perspectives.

The prototype now offers two interpretations of the same selected work: work
cooperation and evidence/artifact connections. Neither is a stage or user level;
all ten contexts have concrete help in both. The ordinary/Cortex comparison is
contextual disclosure, not the primary entry. The [experiment decision and evidence](../../experiments/direction-planning/README.md#help-perspectives-2026-10-27)
record the view contract, preserved state and verification limits. T7 remains In
Progress; no owner comprehension result or public delivery is inferred.

## T7 feedback: the map must change with the view, 2026-10-27

The owner requested visible graph-level changes and questioned teaching readers
point/line/plane terminology. The latest local refinement changes node subjects,
connector meaning and endpoint form, shared-region emphasis, legends and text
alternatives within the single existing graph. Reader labels now use concrete
work/artifact language. Positions and work IDs remain stable for comparison;
request text and skill membership are preserved.

The [current graph UI decision and evidence](../../experiments/direction-planning/README.md#graph-level-perspectives-2026-10-27)
supersede the earlier prose-only perspective design. No approved canonical snapshot
or production website was rewritten. T7 remains an ongoing human walkthrough.

## AIC-REQ-04 rewrite and review, 2026-10-27

### Scope, authority and lifecycle

The owner explicitly selected rewriting and re-reviewing AIC-REQ-03 and its designs,
not modifying review skills. The approved requirement/design snapshots were
preserved. [AIC-REQ-04](../requirements-planning/AIC-REQ-04.md), its
[new functional proposal](../designs/2026-10-27-help-discovery-functional-design.md)
and [new technical proposal](../designs/2026-10-27-help-discovery-technical-design.md)
are co-drafted successors for review, not approved replacements. Neither predecessor
supersession nor publication follows automatically from this rewrite request.
The underlying backlog topic remains one item, with priority unset.

Review used review-requirements, review-functional-design and
review-technical-design in order, keeping evaluation separate from authoring.
Sources: the originating chat's explicit decisions, current asset terminology and
registries, artifact norms, the frozen predecessor chain, the experiment's feedback
and source/evidence records. No external browsing or publication was required.

Canonical contracts reviewed: requirement-modeling 6.1.0 / requirement-quality 2.4.0;
functional-design-modeling 2.0.0 / functional-design-quality 2.0.0;
technical-design-modeling 2.2.0 / technical-design-quality 2.5.0; UI design decisions
guide and findings-list 2.0.1. Referenced engineering constraints resolve to
architecture-quality 1.4.0, testing-quality 1.4.0 and error-surfacing-quality 1.2.0.
No project config, declared budget or waiver exists for this scope.

### Baseline findings motivating the rewrite

These are grounded revision gaps against the clarified owner intent. Their
resolution is in the proposed successor, not a retrospective rewrite of frozen
sources. All finding maturities are `ready`.

| Location | Category | Severity | Title | Description | Successor resolution |
| --- | --- | --- | --- | --- | --- |
| AIC-REQ-03 / A1, A11 | requirement-quality | major | Work discovery does not establish Cortex-specific value | Locating work and recognizing relationships can succeed without identifying what Cortex contributes, needed context or expected outcomes. The owner repeatedly distinguished ordinary agent work from reusable Cortex help. | AIC-REQ-04 A1/A2/R2/R5 and FD F1/F2 require the contribution and applicability directly. |
| AIC-REQ-03 / A6 and functional design / human answer keys | requirement-quality | major | Copy capability is not evidence of usable request preparation | The UI can copy a default string while the human walkthrough only tests reading. This does not establish the objective of preparing a usable request for the reader's problem. | A7/A9 and FD F6/F9 require actual prepared requests with context/output, separately recorded from copy tests. |
| Prior functional design / UI hierarchy and selected approach | functional-design-quality | major | Later perspective and entry decisions are absent from the formal target | The approved snapshot does not specify graph-level alternative subjects/relations or keep agent-ability comparison out of the primary entry. Implementing only that snapshot would miss later owner decisions. | New UI entry, perspective table and state contract define the graph behavior and contextual applicability disclosure. |
| Prior technical design / Components and detailed design | technical-design-quality | major | Complete help and graph-meaning contracts are missing from the revision target | technical-design-quality@2.5.0/TDES-011: the predecessor contracts cannot decide complete contribution/input/outcome content or typed per-view relationship meaning for the clarified design. Tasks would have to invent these requirements at implementation time. | New NodeDetail/MapProjection definitions, source ownership and TD1/TD3/TD5 make the target explicit. |

### Draft review, repair and re-review

After the initial rewrite, review identified two connected draft defects. One
repair batch resolved both, followed by a full content re-review:

| Location | Category | Severity | Title | Description | Confirmed repair |
| --- | --- | --- | --- | --- | --- |
| AIC-REQ-04 / A7 | requirement-quality | major | Source-guidance wording accidentally forced an asset into direct help | Mandatory source guidance on every request conflicted with A2/R5's legitimate ordinary-dialogue outcome. | Guidance is explicitly conditional; a direct request need not name an additional asset when none is applicable. |
| New functional design / Business workflow | functional-design-quality | major | Direct-help branch bypassed observable request preparation | The direct branch could exit while still claiming the human use outcome, without reaching the shared editor/copy/handoff path. | Direct clarification now edits a request and joins the shared copy/recovery/handoff path. |

These repairs preserve the owner's boundary decision; no new product metric,
user segmentation, deadline, execution permission or performance budget was invented.
The requirement background is 246 characters and both design goals are below the
modeled 200-character limit. The relative section order, conditional quality/UI
sections, Rule references and downstream traceability were rechecked.

### Final content results and remaining stage-gate findings

Requirement content review: no remaining finding identified against the active
Spec/Rule and cited owner decisions. It is a reviewable draft for the owner's
replacement/approval decision, not an automatically approved requirement.

Functional and technical content is specified for the requested co-draft. Their
normal handoff gates remain unmet and are not waived:

| Location | Category | Severity | Title | Description | Maturity / disposition |
| --- | --- | --- | --- | --- | --- |
| New functional design / parent frontmatter | functional-design-quality | major | Rewritten requirement remains draft | The parent resolves to AIC-REQ-04, but normal functional-design handoff requires an approved requirement. Requested co-drafting does not establish that approval. | ready; approval pending, no normal downstream-readiness pass claimed |
| New technical design / parent frontmatter | technical-design-quality | major | Rewritten functional parent remains draft | technical-design-quality@2.5.0/TDES-022 remains unmet because the functional proposal has not been approved. | ready; approval pending, no implementation/task handoff claimed |

No other functional or technical content finding was identified in this re-review.
No owner comprehension, implementation alignment or completed requirement is
inferred from a document-content review.

### Technical review Rule coverage

- `rule_set`: technical-design-quality
- `version`: 2.5.0
- `passed`: TDES-001, TDES-002, TDES-003, TDES-004, TDES-005, TDES-006,
  TDES-007, TDES-008, TDES-009, TDES-011, TDES-013, TDES-014, TDES-015,
  TDES-016, TDES-017, TDES-018, TDES-019, TDES-020, TDES-021, TDES-023,
  TDES-024, TDES-025, TDES-028
- `waived`: []
- `not_applicable`: TDES-010 (no cited item depends on an unresolved project
  parameter), TDES-012/TDES-027 (no persisted-data/migration change), TDES-026
  (no decision constrains a future public-site architecture)
- `evidence_limited`: []
- Failed item: TDES-022, reported explicitly above, not counted as a pass.

The profiles are quality-attribute, shared-value and interface-change for private
module consumers. The private interface scope does not introduce a public API.
Coverage evaluates design obligations and planned checks, not executed engineering
Rule passes against code. Requirement/functional quality use checklist criteria;
their content and stage results are reported above without invented Rule IDs.

### Acceptance-to-design and candidate impact

| Revised acceptance | Functional | Technical | Candidate / remaining reconciliation |
| --- | --- | --- | --- |
| A1 contribution, inputs and result | F1 | TD1 | Audit every context for complete purpose/input/outcome presentation; current descriptive triples are not sufficient proof. |
| A2 contextual applicability | F2 | TD1/TD2 | Reuse scene boundaries; verify each defining example and legitimate direct-help path. |
| A3 truthful relationships | F3 | TD3 | Reuse source-reviewed meanings; reconcile typed edge-kind contract and all scenario distinctions. |
| A4 visible alternative views | F4 | TD3/TD4 | Existing graph projections and preservation checks are useful baseline evidence; compare with the full revised contract. |
| A5 full skill/source coverage | F2/F5 | TD2 | Reconcile current canonical inventory and meaningful context/source associations, not a permanent 70 count. |
| A6 lookup and recovery | F5/F7 | TD4/TD6 | Reuse tested search/focus behavior on an identified revised candidate. |
| A7 actual request preparation | F6 | TD5 | Audit templates for desired work/context/output/applicable guidance; gather prepared human requests, not just copy success. |
| A8 local operation | F7 | TD6 | Keep recorded Chromium matrix and explicit limits; native select/assistive environments need evidence appropriate to the claim. |
| A9 human understanding and use | F9 | TD8 | Re-run the requirement-owned observations one question at a time on the reconciled revision; current T7 feedback is partial. |
| A10 truthful local evidence/fallback | F8 | TD6/TD7 | Reconcile source fallback for absent/failed scripts, manifests and criterion mapping. No fresh execution is claimed here. |

The old task list's Done rows apply to AIC-REQ-03 only. This rewrite does not create
or assign a new task list, change its historical statuses, approve the new chain
or automatically supersede predecessors. Once the rewritten chain is approved,
reconcile tasks from TD1-TD8 and decide which existing evidence can be reused.
The existing prototype remains a candidate and was not changed by this rewrite.

### Rewrite verification

- Relative-link checker: zero broken links and zero forbidden governance links.
- Document hygiene: 400 documents checked; no orphan/temporary-label findings.
- Repository Markdown lint: 408 files checked, zero errors.
- Direct acceptance-ID checks: A1-A10, F1-F9 and TD1-TD8 are complete/unique;
  the referenced upstream acceptance IDs resolve.
- Background/goal bounds and required metadata/sections were checked.
- `git diff --check` passed. Original approved snapshots and prototype code were
  not edited; only new proposals and living navigation/review/impact notes changed.
- No prototype, browser or human test was rerun for this documentation-only rewrite;
  historical results retain their original candidate scope.

## AIC-REQ-04 consolidation and reopened decisions, 2026-10-27

At explicit owner instruction, the duplicate AIC-REQ-03 requirement, functional
and technical designs, old task list and old requirement-specific acceptance
summary were deleted. AIC-REQ-04 is the sole current requirement; the backlog entry
and indexes point there. Raw prototype images, logs and prior product feedback are
retained as observations, not competing authority or transferred acceptance.

The owner confirmed objective and content scope only. D1 (use endpoint), D2
(experience) and D3 (acceptance evidence) are now explicit blocking decisions in
AIC-REQ-04. Earlier copy-only use, mandatory map/two-view layout and guided four-case
acceptance remain candidate choices. Both design drafts are labeled accordingly.
The earlier content review does not establish current readiness: unresolved
product decisions prevent execution handoff. No approval or new answer is inferred.

Only D1 has been presented to the owner so far. Recommendations about experience
and acceptance must follow that outcome decision; no implementation change or
publication was performed in this consolidation.

## D1 resolved: discovery and knowledge of use, 2026-10-27

The owner selected finding applicable assets and knowing how to use them. Actual
execution in an agent, installation, real task completion and compulsory request
preparation are not the endpoint. A request example/copy aid may support usage
understanding, but cannot become a required outcome by implication.

AIC-REQ-04's objective/scope and A7 now reflect that decision. D2 and D3 remain
blocking; candidate designs are labeled accordingly, with their old mandatory
request-walkthrough wording adjusted. The next discussion is the primary visitor
entry; no experience or acceptance-method choice is inferred from D1. No prototype
or publication change was made.

## D2 resolved: global map as the primary experience, 2026-10-27

The owner clarified that only the global relationship map is currently needed.
The proposed problem-first entry is not selected. Asset discovery and knowing how
to use assets remain supported through that map and contextual explanation.
Multiple views, search or request-copy controls are optional aids, not mandatory
extra journeys or settled acceptance outputs. D3 alone remains the blocking
product decision; no prototype or publication change was made.

## D1-D3 consolidation, 2026-10-27

All three product decisions are settled: asset discovery and knowledge of use;
one primary global map; agent self-check followed by owner whole-map review of
coverage, relationship accuracy and findable purpose/use. The requirement and two
design drafts were reconciled, removing mandatory four-scenario questioning and
request preparation from acceptance. Draft approval and prototype acceptance are
separate and remain pending; prior T7 results do not transfer.

[Three-criterion self-check](../../experiments/direction-planning/audit/aic04-three-criteria-review.md)
records 70 registered skills, 41 fresh passing model tests, inspected relationships
and the limitation that per-skill instructions currently rely largely on raw
English source Markdown. No fresh browser audit, exhaustive source reread or human
comprehension pass is claimed. No prototype code or publication changed.

## Direct per-skill guidance, 2026-10-27

The owner explicitly authorized repairing the local prototype's source-only usage
gap. All 70 skills now disclose Chinese applicability, needed input, usage and
expected result in the existing contextual panel. The English original is optional.
Internal assessment is explained through its public coordinator. Formal document
status is unchanged; this authorization is for a local prototype, not publication.

[Verification](../../experiments/direction-planning/audit/skill-guidance-evidence.md)
records TDD, all-skill browser paths, responsive/keyboard checks and remaining
limits. Earlier statements that detailed usage relies on raw English sources are
historical observations of the preceding revision. Owner acceptance is pending.

## Fixed asset access, 2026-10-27

The owner reported that finding corresponding assets should not require scrolling.
The local panel now starts with a fixed context-skill selector and skill/work
content choices. It replaces the nested lists behind long explanations; all 70
skills retain their four Chinese usage fields. Long detail text may scroll below
the entry, while selecting an asset requires no explanatory/page scroll.

[Fresh verification](../../experiments/direction-planning/audit/asset-entry-evidence.md)
records model tests, all-skill paths, the ten-node responsive matrix and actual
IAB native selection. Earlier disclosure-based evidence is historical. Owner
acceptance, formal draft approval and publication are not inferred.

## Single work map, 2026-10-27

The owner removed angle switching. The local prototype now retains only the work
relationship map; its asset selector, 70 Chinese skill guides and skill/work
content choices remain. Alternate markup, state, data and CSS were removed.
[Fresh verification](../../experiments/direction-planning/audit/single-map-evidence.md)
replaces prior multi-view acceptance evidence. No publication is authorized.

## Visible skill nodes and evidenced relationships, 2026-10-27

The owner requested directly visualized skills and meaningful inter-skill relations.
All 70 skills are now expanded primary nodes; the hidden selector is removed.
Fifty-three curated relationships distinguish conditional calls, method reuse,
artifact input and recommendation with sources and conditions. Selection highlights
neighbors in the same graph; the panel explains usage and relationships. Normal
page scrolling retains readable labels. No relationship is inferred from topic alone.

[Current verification](../../experiments/direction-planning/audit/expanded-skills-evidence.md)
records 53 model tests, 70 direct skill paths, ten layout/theme combinations and
limits. Earlier picker/macro-node acceptance records describe older revisions.
Owner review, formal draft approval and publication remain separate.

## Compact nodes and clear relationship routes, 2026-10-27

The owner found asset components oversized and some relationships obscured.
The local repair uses compact labels, reserved routing gutters, orthogonal paths,
separate lanes by relationship meaning and inline peer labels. A resize-state bug
that redrew default-skill edges without a matching selection was also repaired.
Inventory and all 53 relationship meanings are preserved.

[Current verification](../../experiments/direction-planning/audit/compact-skills-evidence.md)
records size/collision regressions, all-skill paths, dense-hub checks and limits.
Earlier large-card/curve evidence is historical. Owner acceptance and publication
remain separate.

## Visible names and descriptions, 2026-10-27

The owner clarified that skill name and description must both be visible. The
local prototype restores the canonical name above the Chinese description in
all 70 primary nodes, with relation badges in a separate cell. Names wrap in full;
tooltips/details are no longer the only way to identify them. Nearby release
labels retain visibility above the responsive sheet.

[Current verification](../../experiments/direction-planning/audit/named-skills-evidence.md)
records visible-field assertions, retained routing checks and layout evidence.
Canonical instructions, relationship meanings and publication authorization are
unchanged. Owner acceptance remains pending.

## 2026-10-27: Local topic-spine branch redesign

AIC-REQ-04's local prototype now lays out skills by evidenced coordinator branches,
artifact handoffs and shared methods beside a topic spine. All 70 names/purposes
remain visible. The spine is navigation, not a required sequence. Model and browser
checks passed; current evidence is in the experiment README. Formal approval,
owner whole-map acceptance and publication remain pending.

## 2026-10-27: Independent topic relationships and folding

The owner found that the topic spine still implied sequence and requested truthful
topic dependencies, loops, on-demand support and optional folding in one map.
The current revision removes the spine, summarizes the four curated cross-topic
edges in three isolated relation corridors, adds source-backed repair loops and
places on-demand support in an independent region. Topic folding supersedes A5/A6's
always-expanded constraint for this authorized local revision. All 70 skills remain
present with full names, Chinese purposes and four usage fields after expansion.
Search/peer navigation reveals folded destinations. Current evidence is linked
from the experiment README; 60 model tests and the responsive browser matrix pass.
No formal draft approval, owner comprehension acceptance or publication is inferred.

## 2026-10-27: One persistent connected topic graph

The owner requested a complete visible topic graph rather than isolated relation
pairs, with folding limited to skill detail. The current local revision connects
ten topics to one work context through non-directional contribution associations;
three directional relationships and local repair loops remain explicit. Support
is connected within the graph. No new skill dependency is inferred. Skill branches
expand below the persistent topology in the same canvas; topic nodes and all 13
connections retain their geometry when folding. The experiment README links the
current model/browser evidence. Owner acceptance, document approval and publication
remain separate and have not been inferred.

## 2026-10-27: Direct topic relationships replace the work hub

The owner found the hub obscured substantive topic relationships. The current
local prototype removes that hub and draws 13 direct, typed topic relationships
with exact source excerpts and Chinese conditions. These are topic-level artifact
handoffs, feedback and scoped support, not 13 mandatory skill calls. The concrete
53-edge skill registry is unchanged. Existing artifacts and research recommendations
do not imply rerunning producers, automatic roadmap approval or broader authority.

A regression check found stale label geometry immediately after the inspector
reduced map width. Opening and closing now redraws topic geometry synchronously.
The final browser matrix checks label clearance with the inspector open and closed,
all 13 relation explanations, persistent folded topology and all 70 skill paths.
The current requirement/design drafts were reconciled to this presentation and
superseded implementation descriptions consolidated. Evidence is linked from the
experiment README. Formal approval, owner comprehension and publication remain
pending.

## 2026-10-27: Skill details expand in their owning topic

The owner requested local expansion without travelling to a lower-page skill dock.
That dock is removed: each of the 70 skill nodes is rendered once inside its owning
topic. Zero or one topic is open, the active desktop column widens, peer cards stay
compact and later rows reflow. Bounded lists keep the title visible; their own SVG
connectors scroll and clip with their skill nodes. Search and peer navigation reveal
and align the owning topic and skill. Small screens pan within the graph and use
coordinated list/sheet heights.

A red test reproduced a topic edge crossing a newly tall peer; routing now uses
actual ports and reserved row gaps. A further red disclosure test established the
single-topic transition. Current requirement/design drafts were reconciled without
inferring formal approval. The experiment README links current model/browser
verification, including source ownership, all 70 usage paths and ten-topic expansion
in each responsive/theme combination. Publication and owner acceptance remain pending.

## AIC-REQ-04 current baseline consistency review, 2026-10-27

### Scope and decision

The owner retained the current prototype after reconsidering a work-context hub.
The baseline is one direct-topic map with local skill expansion: ten topics,
13 topic relations, two loop annotations, 70 skills and 53 concrete skill relations.
There is no hub, angle switch, mandatory sequence or lower-page skill dock.
One topic is open at a time; nearby ownership, internal list scrolling, reflow and
small-screen graph panning are intentional. No runtime prototype file changed in
this documentation synchronization, and nothing was published.

Authority chain: [requirement](../requirements-planning/AIC-REQ-04.md),
[functional design](../designs/2026-10-27-help-discovery-functional-design.md),
[technical design](../designs/2026-10-27-help-discovery-technical-design.md),
[task draft](../designs/help-discovery-tasks.md). All remain drafts.

### Review method and repaired documentary findings

Authoring repairs were separate from the evaluative review passes. The atomic
`review-requirements`, `review-functional-design`, `review-technical-design`,
`review-tasks` and `review-implementation-alignment` boundaries were used. Canonical
modeling versions: requirement 6.1.0, functional design 2.0.0, technical design
2.2.0, tasks 2.2.0; findings format 2.0.1 defines the fields below.

| Repaired issue | Repair and re-review outcome |
| --- | --- |
| Requirement/index still described decisions as reconsidered or request preparation as the endpoint | Retained scheme, D1-D3, direct relations and local disclosure now agree; endpoint remains find asset/know use |
| Functional design mixed current behavior with old layout/assets | Consolidated current interaction/state contract, actual captures, local scrolling and ordinary-agent boundaries |
| Technical design promised target/obsolete contracts, selectors, invariant geometry and module recovery already present | Replaced with actual exports/state/value ownership, per-topic SVGs, geometry reflow and explicit intended-versus-observed failure behavior |
| No AIC-REQ-04 task list existed in docs or the experiment, including ignored-file search | Added a ten-row draft reconciliation plan with design traces, Fibonacci points, DAG, governance checks and evidence; no inherited completion claims |
| Three-criterion self-check cited 41 tests and largely English-source usage | Replaced with current 63-test/source-bound all-skill evidence and directly available Chinese guidance |
| README and design index exposed earlier versions as current | Added one current-baseline entry and corrected active design/task labels; historical evidence remains scoped to its revision |

Requirement content review: completeness, determinacy, ordering, scope, measurable
quality criteria, risks, source and traceability pass. No product-choice question
remains unresolved. Functional content/UI traceability passes; role/object lifecycle
sections are inapplicable to this read-only single-visitor prototype. Technical
contracts, alternatives, failures, value ownership and task mapping are now explicit.
Task fields, IDs, DAG, dependencies, bounded scope and engineering annotations pass.
These content conclusions do not remove the approval gates below.

### Prototype observations before T7/T8 repair

Both observations below were reproduced during synchronization and subsequently
resolved by the [scoped T7/T8 follow-up](#aic-req-04-t7-and-t8-local-repair-2026-10-27).
The original measurements are retained as red evidence.

| ID | Location / expected item | Observed result | Consequence / task |
| --- | --- | --- | --- |
| P1 | `workspace.css` loop text; A8/QAS-01, F7, TD6 | Both light-theme loop labels measure 4.3776:1; the target is at least 4.5:1. Four light-theme samples (two sizes × two states) contain the same two failing labels; dark samples pass. | Acceptance gap; T7. The target is retained and not waived. |
| P2 | `index.html` source fallback; A10, F8, TD6 | JavaScript disabled exposes the catalogue link with zero interactive topics. JavaScript enabled with `story.mjs` blocked leaves zero topics and no visible catalogue recovery. | Intended failure recovery is not implemented; T8. No-JS success cannot stand in for module-failure recovery. |

The checker completed successfully as an observation run; it did not report an
all-acceptance pass. Prototype code remains unchanged at the owner's instruction.
These are consistency discrepancies against intended completion, not a production
incident or permission to silently alter the retained scheme.

### Approval-gate findings and readiness

| Location | Category | Severity | Title | Description / suggestion | Maturity |
| --- | --- | --- | --- | --- | --- |
| `docs/designs/2026-10-27-help-discovery-functional-design.md` frontmatter | functional-design-quality | major | Parent requirement remains draft | The requirement is not approved under functional-design-modeling §4.1 and functional-design-quality traceability. This synchronized draft can be reviewed but cannot be declared a passed formal pre-coding gate; record actual approval before handoff. | ready |
| `docs/designs/2026-10-27-help-discovery-technical-design.md` frontmatter | technical-design-quality | major | Parent functional design remains draft | `technical-design-quality@2.5.0/TDES-022` requires an approved upstream. Retaining the prototype is not that approval; keep the draft and gate limitation explicit. | ready |

At synchronization, task content had no remaining TASK-rule finding and no task
was Done. The follow-up explicitly assigned T7/T8 and records their local Done
states. The parent remains draft under task-modeling §8, so this is still not an
approved-parent formal handoff.
The formal alignment gate cannot certify completion against an approved chain
because none exists. Its comparison here is an observational consistency audit,
with missing approval authority recorded as evidence limitations rather than
invented approved intent. No intrinsic engineering/security/performance review is
claimed. No blocking decision for this documentation-only reconciliation is inferred.

### Requirement-to-prototype traceability

| Requirement | FD / TD | Current code/data | Evidence and result | Task |
| --- | --- | --- | --- | --- |
| A1/A2 | F1/F2, TD1 | `context-copy.mjs`, `panel-model.mjs`, `work-map.mjs` | Context/model tests and actual explanation paths; ordinary/Cortex boundary retained | T4 |
| A3 | F3, TD3 | `topic-edges.json`, `global-topic-graph.mjs`, `skill-edges.json`, `skill-graph.mjs` | Quotes/endpoints, typed neighborhoods, relation explanations and inspected conditional scope | T2 |
| A4 | F4, TD3/TD4 | `index.html`, `story.mjs`, `request-state.mjs` | One-map DOM; content/request continuity; no hub/perspective switch | T3/T5/T6 |
| A5 | F5, TD2 | `catalog.json`, `workflow.mjs`, `panel-model.mjs`, `story.mjs` | Exact 70-node partition and source parity; local ownership/search/peer paths | T1/T3 |
| A6 | F4/F5/F7, TD4 | `topic-map.mjs`, `story.mjs`, `workspace.css`, local SVGs | All ten topics in ten size/theme combinations; source heading/selection/local viewport preserved | T3/T5 |
| A7 | F6, TD5 | `skill-guidance.json`, `skill-guidance.mjs`, `story.mjs`, request identity | Four Chinese fields for every skill; absent/rejected/late edit/close copy recovery passes | T4/T6 |
| A8 | F7, TD6 | Native controls, local lists, responsive sheet and prototype styles | Pointer/keyboard/geometry matrix passes; contrast P1 remains unmet | T5/T7 |
| A9 | F9, TD8 | Three-criterion review and recorded owner conclusion | Current agent self-check updated; explicit owner acceptance pending | T9 |
| A10 | F8, TD7 | Static source route, canonical links and evidence hashes | Runtime identity bound and local-only scope confirmed; module failure P2 remains unmet | T8/T10 |

All experiment paths above are under `experiments/direction-planning/`. T1-T6 have
substantial implemented/verified baseline evidence, not a request to rebuild them.
All new task statuses remain Todo as an unassigned draft. T7/T8 are independent
pending corrections; T9/T10 record actual acceptance and approval when supplied.

### Evidence and limits

- [Current 63 model checks](../../experiments/direction-planning/audit/doc-alignment-tests.txt).
- [All-skill, local-ownership and 100 topic/viewport/theme cases](../../experiments/direction-planning/audit/local-branch-browser.json).
- [Fresh runtime hashes, title comparison, eight contrast samples, two fallback cases and four clipboard cases](../../experiments/direction-planning/audit/doc-alignment-browser.json).
- [Current three-criterion self-check](../../experiments/direction-planning/audit/aic04-three-criteria-review.md).
- [Modeled review coverage](../../experiments/direction-planning/audit/doc-review-coverage.json).

The new report verifies every recorded core-runtime hash against the retained
browser baseline; current model checks were rerun. The full 100-case local-branch
browser matrix was not rerun in this documentation-only turn, and its source-bound
record is reused with that scope explicitly retained. It does not
reuse old Lighthouse or earlier contrast claims for this revision. Native Safari,
real devices, native browser zoom and spoken screen-reader operation remain
unverified. Scheme retention, formal approval, machine verification, owner
comprehension and publication remain separate.

## AIC-REQ-04 T7 and T8 local repair, 2026-10-27

The owner explicitly authorized T7/T8 after retaining the current scheme. The
contrast and blocked-entry checks were first run red, then both passed after
prototype-only HTML/CSS changes. No graph topology, skill records, controller or
request-state logic changed; nothing was published.

| Task / original observation | Current result | Evidence |
| --- | --- | --- |
| T7 / P1 | Done locally: loop labels use theme ink; about 11.47:1 light and 11.12:1 dark, exceeding 4.5:1 | [Eight current samples and loop ratios](../../experiments/direction-planning/audit/t7-t8-browser.json) |
| T8 / P2 | Done locally: static footer source route works without JavaScript and with the entry blocked; keyboard focus and catalogue HTTP 200 verified | [Blocked-entry capture](../../experiments/direction-planning/audit/t7-t8-module-fallback.png) and the same browser report |

[Red/green repair record](../../experiments/direction-planning/audit/t7-t8-evidence.md)
retains the original failures and current measurements. After final edits,
[63 model tests](../../experiments/direction-planning/audit/t7-t8-tests.txt) and the
[fresh all-skill/local-branch browser matrix](../../experiments/direction-planning/audit/local-branch-browser.json)
pass. This includes all 70 skill paths and 100 topic/size/theme selection cases.
The scheme and one-map/local-disclosure behavior remain unchanged.

The task file is now an active local progress record after scoped assignment;
only T7/T8 moved to Done. Other tasks remain Todo. The existing formal-parent
approval findings and owner whole-map review are not resolved by these repairs.
The [modeled review coverage](../../experiments/direction-planning/audit/doc-review-coverage.json)
records concrete completion evidence for these two tasks without certifying the
unapproved artifact chain. Current functional/technical text, three-criterion
self-check and the prototype entry now reference the repaired behavior. No task,
approval or acceptance from AIC-REQ-03 is restored or transferred.

## AIC-REQ-04 website delivery planning, 2026-10-27

The owner identified that no task covered formal website integration or publication,
then authorized adding both to the planning chain only. The previous local-only
scope omitted future delivery rather than representing an intentional product
exclusion. Requirement scope and R7/R8 now distinguish planned delivery from
execution permission. No website or prototype modification, remote request,
packaging, publication or task completion is authorized by this update.

| Planning concern | Requirement | Functional / technical design | Tasks / entry gates |
| --- | --- | --- | --- |
| Formal website integration | A11, QAS-05 | F10 / TD9: dedicated bilingual explorer, retained map/atlas, shared theme/language, site-root runtime closure, revision-bound sources and static fallback | T11 after T10, approved document chain and separate website-change authorization; T12 local integration tests and owner scheme-retention confirmation |
| Public delivery and recovery | A12, QAS-06 | F11 / TD10: runtime allowlist/hashes, existing host, actual known-good version, public verification and failure recovery | T13 after T12 plus separate publication authorization and verified access/domain/certificate state |

Inspected local sources: [website guide](../../website/README.md),
[recorded deployment](../../website/.openai/deployment.json), existing website files
and `.github/workflows/lint.yml`. The website is a standalone static root with two
language editions and a complete passive-asset atlas. Its recorded publication
uses a separate Sites deployment checkout and explicit runtime payload. Existing
workflow steps run website tests; no website publication job was identified in
that workflow. These are repository observations, not a fresh live-host check.
Version 7 is historical evidence; T13 must identify the actual current known-good
version before changing public delivery.

Consistency self-check: A11/A12 trace through F10/F11 and TD9/TD10 to T11-T13.
T1-T10 retain their IDs and states, including only T7/T8 Done. New estimates are
bounded Fibonacci values (8, 5, 3); dependencies are acyclic. Website implementation,
integrated acceptance and public release have distinct entry/exit evidence.
Formal approval and A9 owner acceptance remain pending; this planning check does
not certify the draft chain as ready for implementation. No new prototype result
or production-health claim is inferred from documentation validation.

Planning validation passed: changed-Markdown lint (eight files), relative-link
checks (zero broken links), document hygiene (409 documents), task ID/estimate/DAG
and status checks, and whitespace validation. A before/after SHA-256 manifest
confirmed all 224 files under `website/`, `experiments/direction-planning/` and
`.github/workflows/` were byte-identical, with no additions or deletions. Runtime
and browser suites were not rerun for this documentation-only change; existing
prototype evidence retains its original revision scope.

## AIC-REQ-04 website delivery re-review, 2026-10-27

The owner requested re-review and repair of the requirement, functional design,
technical design and tasks, focusing on website integration, acceptance and
publication. Atomic reviews used their canonical assets; the subsequent authoring
repairs were performed separately under this explicit instruction. The scope is
document planning only. The earlier planning entry and prototype review coverage
remain historical; neither is current approval of the extended delivery chain.

### Applied review sources

| Review | Modeling Spec | Quality Rule | Scope / applicability |
| --- | --- | --- | --- |
| review-requirements | requirement-modeling 6.1.0 | requirement-quality 2.4.0 | All required/conditional sections, all acceptance including A11/A12, decisions, scenario trace and external prerequisites |
| review-functional-design | functional-design-modeling 2.0.0 | functional-design-quality 2.0.0 | Visitor UI plus owner/maintainer delivery roles, candidate lifecycle, workflow branches, exceptions and upstream approval |
| review-technical-design | technical-design-modeling 2.2.0 | technical-design-quality 2.5.0 | Quality-attribute, shared-value and interface-change; planned static routes and existing route compatibility; no visitor database/migration |
| review-tasks | task-modeling 2.2.0 | task-quality 2.4.0 | Active local progress record with unassigned future tasks, not a formal handoff; engineering annotations apply to runtime/integration/release tasks |

Findings follow findings-list 2.0.1 and applicability follows rule-modeling 1.1.1.
Referenced engineering Rules were loaded: architecture-quality 1.4.0,
testing-quality 1.4.0 and error-surfacing-quality 1.2.0. No project configuration,
waiver, session-duration target or coverage percentage was invented. Source review
included `website/language.mjs`: its existing redirect targets are homepage-only,
so explorer-family routing requires an explicit compatible extension rather than
blind reuse. Existing website tests and recorded deployment contracts were read;
no current provider availability, authorization or recovery capability is claimed.
The roadmap.sh inspiration URL resolved; it was not used to establish licensing,
external interaction behavior or runtime dependencies.

### Repair summary

This is a change summary, not a replacement for the remaining findings below.
Each repair was checked against its defining layer before downstream reconciliation.

| Observed gap | Repair and deciding evidence |
| --- | --- |
| R8 was separated from the rule table; QAS-05/QAS-06 were not cited by their acceptance items; Product decisions interrupted standard section order | R1-R8 are one table, A11/A12 cite their scenarios, and decisions remain within the risk/constraint section; structural/trace checks pass |
| A5 always required Chinese purposes despite the new English edition | Localized purpose/use obligations now explicitly distinguish prototype/Chinese and reviewed English editions without dropping formal names |
| Integration acceptance could be reused after runtime or registry changes | A11 and all downstream gates bind acceptance to runtime hashes, pinned asset sources and the actual owner conclusion; affected changes reopen checks and semantic/owner review |
| All release failures implied rollback, even before switching; uncertain outcomes and intervening deployments were not closed | A12/QAS-06, functional workflow/states and technical outcome table distinguish unchanged delivery, candidate verification, safe recovery and unresolved/conflicting state |
| Public interactions were only called representative, and mandatory checks could be skipped as unverified | FD defines the two-edition, two-width, two-theme public smoke set and recovery checks; unexecuted required checks leave A12 incomplete |
| New delivery roles/states had no conditional models or closed flowchart | FD now includes delivery candidate states, role-by-menu/operation/data permissions, and explicit authorization/failure/withdrawal/change branches; these introduce no application accounts or approval screen |
| Locale ownership and source/routing interfaces were left for implementation to invent | TD names locale/metadata/source/route paths, adapter signatures and invalid outcomes. It separates canonical asset SHA, accepted runtime identity and deployment-checkout commit, and removes duplicate display owners in the final candidate |
| Shared language reuse could redirect explorer readers to a homepage; entry-only cache versioning did not cover changed nested files | TD preserves the old caller contract while adding explicit explorer route maps; language/storage-denial, nested-cache and cold/warm assembly checks cover both editions |
| T11 combined runtime migration, full bilingual content and site wiring into one deliverable | T11 is a functioning Chinese-only local runtime port; new T14 extracts/reviews final bilingual copy and T15 connects site navigation/preferences; neither T11 nor T14 requires a later task to produce its own intermediate deliverable |
| Integrated acceptance did not explicitly separate engineering/alignment gates from browser and owner evidence; release lacked final evidence closeout | T12 now records all four separately; T13 closes actual deployment/public/task/requirement evidence only after success, preserving prior successful receipts and failed candidate outcomes |

### Re-review result and remaining findings

The requirement's content and Spec checks pass: completeness, executability,
clarity, soundness and traceability, including the new QAS-05/QAS-06. It is ready
for owner approval, not automatically approved. Functional content checks pass
except the existing parent-approval obligation. Technical content and task
coverage/dependency/governance checks pass with the approval findings below.
No new unresolved product/architecture decision was found within the planned
static-site scope. Runtime, browser and public execution remain future evidence.

- **Location**: `docs/designs/2026-10-27-help-discovery-functional-design.md:5`
  **Category**: functional-design-quality. **Severity**: major. **Maturity**: ready.
  **Title**: Parent requirement has not been formally approved.
  **Description**: Functional-design-quality's approved-parent criterion and
  functional-design-modeling 2.0.0 §4.1 are unmet because AIC-REQ-04 remains draft.
  Scheme retention and a successful content re-review do not supply owner approval.
  **Suggestion**: Record actual requirement approval before formal downstream handoff.
- **Location**: `docs/designs/2026-10-27-help-discovery-technical-design.md:5`
  **Category**: technical-design-quality. **Severity**: major. **Maturity**: ready.
  **Title**: Functional-design parent remains draft.
  **Description**: technical-design-quality@2.5.0/TDES-022 is unmet because the
  functional-design parent has not reached approved status. The document remains
  a reviewed planning draft, not an approved implementation authority.
  **Suggestion**: Record actual functional-design approval before formal implementation handoff.
- **Location**: `docs/designs/help-discovery-tasks.md:5`
  **Category**: task-quality. **Severity**: major. **Maturity**: ready.
  **Title**: Technical-design approval is still missing for formal task execution.
  **Description**: task-modeling 2.2.0 §1/§8 requires an approved technical-design
  source; this parent remains draft. TASK-011 itself passes because the source
  exists, but that does not satisfy the separate approved-parent Spec obligation.
  **Suggestion**: Keep the active historical progress states and new Todo rows;
  obtain actual upstream approval and stage authorization before starting website tasks.

These findings were not waived or repaired by changing status fields. They are
approval limits, not remaining defects in the integration/release behavior plan.
A9 whole-map acceptance also remains pending; T7/T8 scoped completion does not
substitute for it. No user approval is fabricated and no permission question is
needed to complete this authorized document review.

### Rule coverage metadata

The three findings above are separate from coverage metadata. The technical
review's non-passed applicable item is represented by its TDES-022 finding; every
other item has a disposition below. Legacy requirement/functional Rules use their
five-dimension checklist rather than invented Rule IDs. Functional conditional
sections and UI handoff were checked, with its traceability exception reported above.

```json
[
  {
    "skill": "review-technical-design",
    "rule_set": "technical-design-quality",
    "version": "2.5.0",
    "passed": [
      "TDES-001",
      "TDES-002",
      "TDES-003",
      "TDES-004",
      "TDES-005",
      "TDES-006",
      "TDES-007",
      "TDES-008",
      "TDES-009",
      "TDES-010",
      "TDES-011",
      "TDES-013",
      "TDES-014",
      "TDES-015",
      "TDES-016",
      "TDES-017",
      "TDES-018",
      "TDES-019",
      "TDES-020",
      "TDES-021",
      "TDES-023",
      "TDES-024",
      "TDES-028"
    ],
    "waived": [],
    "not_applicable": [
      {
        "rule_id": "TDES-012",
        "reason": "No visitor/business persisted schema or database change; static locale/source records have explicit component contracts."
      },
      {
        "rule_id": "TDES-025",
        "reason": "No external technical specification is adopted; repository references resolve, and the separate functional inspiration URL check is recorded."
      },
      {
        "rule_id": "TDES-026",
        "reason": "Existing static stack/host reused; no structural decision beyond this scoped integration."
      },
      {
        "rule_id": "TDES-027",
        "reason": "No breaking schema, backfill or irreversible data operation."
      }
    ],
    "evidence_limited": []
  },
  {
    "skill": "review-tasks",
    "rule_set": "task-quality",
    "version": "2.4.0",
    "passed": [
      "TASK-001",
      "TASK-003",
      "TASK-004",
      "TASK-005",
      "TASK-006",
      "TASK-007",
      "TASK-008",
      "TASK-009",
      "TASK-010",
      "TASK-011",
      "TASK-012",
      "TASK-013",
      "TASK-014",
      "TASK-015",
      "TASK-016",
      "TASK-017",
      "TASK-019"
    ],
    "waived": [],
    "not_applicable": [
      {
        "rule_id": "TASK-002",
        "reason": "Historical active progress record, not a formal initial execution handoff; only T7/T8 were previously completed."
      },
      {
        "rule_id": "TASK-018",
        "reason": "No waiver is cited."
      }
    ],
    "evidence_limited": []
  }
]
```

### Validation and revision binding

Executed document checks: Markdown lint on six changed documents, relative-link
resolution (zero broken links), document hygiene (409 documents) and whitespace
validation. Additional assertions verified A1-A12 → F1-F11 → TD1-TD10 references,
R1-R8 table integrity, scenario citations and requirement section order; all 15
task IDs/fields/statuses, Fibonacci estimates, governance annotations and dependency
DAG; canonical engineering references; and dispositions for all 28 TDES and 19 TASK
items. The three approval findings remain explicitly open.

A before/after SHA-256 manifest verified all 224 files under `website/`,
`experiments/direction-planning/` and `.github/workflows/` were byte-identical,
with no additions or deletions. Only T7/T8 retain Done status; all website tasks
remain Todo and upstream documents remain draft. No runtime/browser tests, provider
operations, packaging, deployment or publication were performed for this document
review. Earlier prototype results retain their original revision and scope.

Reviewed document identities (audit record itself excluded to avoid self-reference):

| Document | SHA-256 |
| --- | --- |
| [AIC-REQ-04.md](../requirements-planning/AIC-REQ-04.md) | `4faeac9448a540271cb682f527432f4125383a31f4918b967f79bd2f1e40671d` |
| [2026-10-27-help-discovery-functional-design.md](../designs/2026-10-27-help-discovery-functional-design.md) | `63d8d17fdc4b806ec902dae009398bf381441910512a9b6499f9fc728c124e70` |
| [2026-10-27-help-discovery-technical-design.md](../designs/2026-10-27-help-discovery-technical-design.md) | `a68f94dcbb91f4c0d855a6fedf07fddc32adf110a8dd27bb5dba38a07f230f78` |
| [help-discovery-tasks.md](../designs/help-discovery-tasks.md) | `31b644c086152600bb889151d2b0a8edc6ab03687c2db161e8faf978c4582a4c` |

## AIC-REQ-04 approved local website integration, 2026-10-27

The owner explicitly approved the revised requirement, functional design, technical
design and task plan, retained the current scheme and authorized formal website
integration with local verification. The three parent-approval findings are now
resolved by actual instruction, not inferred from tests. No publication, remote
write, commit or push was requested.

The same instruction directly authorizes integration now. T9's separate owner
whole-map comprehension conclusion is not fabricated; T10's dependency is adjusted
to source/verification tasks T1-T8 so that the newly authorized implementation can
proceed independently of that human conclusion. T12 machine/engineering checks
will be completed, with owner acceptance recorded separately and left pending
until actually provided. T13 remains Todo and unauthorized.

### Implemented scope and verification

T1-T8/T10 are reconciled; T11/T14/T15 are complete locally. The formal site now
serves `/explore/` and `/explore/zh.html`, reached from both matching homepages.
The retained single map has 10 topics, 13 direct topic relations, two loops,
70 uniquely owned skills and 53 concrete skill relations. Skills expand within
their topic; the panel retains applicability, inputs, usage, expected result and
ordinary-agent boundaries. Source links are pinned to the canonical asset revision;
local hashes were checked against that revision, without claiming public availability.

Both locales have reviewed copy and strict key/type/identity/placeholder parity.
Navigation, theme, language precedence, cache identity, isolated runtime closure,
static source recovery, focus and clipboard failure/stale-result behavior pass.
The 36-file [working runtime manifest](../../website/.openai/runtime-manifest.json)
records exact hashes and the pending owner conclusion. It is not an accepted
release manifest and cannot authorize T13.

Evidence: [local verification guide](../../tests/website/evidence/README.md),
[engineering review](../../tests/website/evidence/engineering-review.json),
[implementation alignment](../../tests/website/evidence/implementation-alignment.json).
Node: 33 passed; Python: 18 passed; original model tests: 63 passed. Integrated
browser checks cover 200 topic/size/theme selections, 140 actual skill paths,
20 control scenarios, 16 contrast samples and eight clipboard recovery cases.
Final English overview, Chinese dark overview and both mobile editions were visually inspected.

Verification found overflow in translated headings/skill children and mobile
navigation, and a short-screen work panel squeezed to four pixels. Targeted
red/green corrections preserve the graph/router and scheme. The last issue also
existed in the reference prototype: only its `story.mjs` and `workspace.css` were
patched to preserve a usable 123px panel body. Original browser and T7/T8 regressions,
plus ten original control scenarios, pass again. No registry or skill definition
was changed.

### Remaining gates and limits

T9 remains Todo: the actual three-criterion owner conclusion is pending. T12 is
In Progress: machine and engineering checks pass, but integrated owner acceptance
is not supplied. A9/A11 therefore remain unverified overall; no implemented or
release-ready requirement status is inferred. A12/T13 remain Todo, unauthorized.
Native-device, browser zoom and spoken-screen-reader testing remain unverified;
recorded browser results are Chromium emulation. No public source availability,
TLS/provider behavior, deployment or recovery operation was tested. Existing
hosting receipts and workflows are untouched. No commit, push, upload or publish
operation occurred.

## AIC-REQ-04 site information-architecture revision, 2026-10-28

### Decision and authorization

The owner identified broad support shown too narrowly, missing Chinese skill
names, confusing navigation and overlapping Capability overview / Work relations
entries. After comparing AIC-REQ-02's introduction/discovery/adoption purpose with
the integrated site, the owner requested a site-wide information-architecture plan
and synchronized AIC-REQ-04 chain. This authorizes documentation only. No website,
prototype, tests/evidence or publication artifact is changed in this revision.

The functional design's site-information-architecture section is the placement
and navigation authority: Home introduces and guides adoption; Capability overview
is the single discovery destination; the relationship graph is its primary
representation, not a separate global menu; Asset directory retains complete
four-type indexed lookup; Get started retains installation guidance. Existing
explorer paths and directory/type/install anchors remain. The directory stays in
the homepage document, avoiding an unrelated migration. Native navigation, local
graph controls and language/theme utilities have separate responsibilities.

### Trace and corrections

R9/A13 → F12 → TD11 → T16 establishes the site structure and compatibility contract.
R10/A14 → F13 → TD12 → T17 addresses source-backed cross-cutting support without
claiming universal invocation. R10/A15 → F14 → TD13 → T18 distinguishes localized
names, canonical IDs and purposes. T19 verifies the revised assembly; T12 then
records actual owner acceptance. T13 remains separately gated and unauthorized.
All prior acceptance and publication/recovery obligations remain in force.

The requirement and two designs now have draft status for the changed revision.
The prior approval is preserved in the dated local integration record, not silently
applied to new decisions. T11/T14/T15 remain Done only for their previous runtime.
T12 remains In Progress: owner feedback requires corrections, so prior machine
results cannot establish acceptance. T9's actual comprehension conclusion is still
pending. No implementation, owner acceptance or public release is claimed.

### Documentation self-check and limits

The author checked module boundaries, navigation closure, two-language direct and
alternate routes, compatibility/fallback, scoped support and name ownership,
A13-A15/F12-F14/TD11-TD13 task trace, estimates and task DAG. Native route data and
locale/scope records are explicitly planned, not claimed to exist. The design uses
local website patterns; no external reference, service or skill installation was
needed. T16-T19 remain Todo. Exact supported subjects and translations require the
source/content audit in T17/T18; there is no invented complete support matrix.

This is a synchronized revision proposal, not a passed formal pre-coding review:
upstream approval conditions are unsatisfied while the chain is draft. Those gates
remain explicit rather than waived. Future implementation must obtain revision
approval and authorization, then run affected interface/model/browser checks. This
change runs documentation checks only; prior source-bound browser evidence is
untouched and is not reused as proof of these new requirements.

Validation results: markdownlint passed for all eight revised documents; repository
link checks found zero broken relative links or forbidden downward references;
document hygiene passed across 410 documents; the 19-task DAG and status/parent
checks passed; `git diff --check` passed. Before/after SHA-256 inventories confirm
all website, prototype, website test/evidence and workflow files are unchanged.
No runtime/browser tests were rerun because this revision changes documentation only.

## AIC-REQ-04 information-architecture re-review, 2026-10-28

### Scope and method

The owner requested review and targeted repair of the revised requirement,
functional design, technical design and task list, focusing on whole-site structure,
navigation and acceptance. The four atomic review Skills were applied as separate
evaluations; targeted edits followed outside their evaluative scope, then the
changed sections were re-reviewed. No code, prototype, tests/evidence, deployment
record or publication operation is included.

Canonical versions: requirement-modeling 6.1.0 / requirement-quality 2.4.0;
functional-design-modeling 2.0.0 / functional-design-quality 2.0.0;
technical-design-modeling 2.2.0 / technical-design-quality 2.5.0;
task-modeling 2.2.0 / task-quality 2.4.0; findings-list 2.0.1.
Referenced engineering constraints were read at architecture-quality 1.4.0,
testing-quality 1.4.0 and error-surfacing-quality 1.2.0. Quality-attribute,
interface-change and shared-value apply. No persisted-data/migration change,
new platform, declared quality/session budget, project configuration or waiver is
present. Baseline evidence is not new runtime acceptance. The list is a living
progress/revision record, not a fresh handoff of started tasks.

### Findings repaired and re-reviewed

All following findings have maturity `ready`. Locations are document section
anchors; each row retains the emitting category and actual bounded impact.

| ID / severity / category | Location | Finding and repair | Re-review |
| --- | --- | --- | --- |
| IA-01 / major / requirement-quality | AIC-REQ-04, Dependencies & Prerequisites | The old T9/T10-before-integration gate contradicted the revision task order and recorded owner exception. The requirement now separates revision approval/implementation authority from final T9/T12 owner acceptance and distinguishes repository-root prototype checks from website-root verification. | Resolved |
| IA-02 / major / functional-design-quality | Functional design, Site information architecture | Active state was promised without scripts while the technical design offered only heading fallback; Get started and history/fragment transitions lacked a defined state. Product behavior now distinguishes script-driven active destination from native-link/heading orientation and defines recognized sections, unknown fragments and back/forward behavior. | Resolved |
| IA-03 / major / functional-design-quality | Functional design, modules and exceptions | New IA/support/name responsibilities and their exception paths were absent from the original module/edge tables. Added bounded responsibilities and legacy bookmark, language, script-failure and scope-navigation outcomes, retaining one graph and complete directory coverage. | Resolved |
| IA-04 / major / technical-design-quality | Technical design, Planned site information architecture integration | TDES-011/TDES-028: new global route/label ownership conflicted with old explorer-locale ownership and a homepage-to-explorer adapter dependency. A shared navigation record/module now owns routes, labels and section mapping; native mirrors are checked, explorer delegates compatibly and obsolete copies are removed in T16. | Resolved |
| IA-05 / major / technical-design-quality | Technical design, scope and locale contracts | TDES-011/TDES-013: group-wide sources did not substantiate each supported subject, and translated names could conflict with identity guards. Per-target conditions/provenance and a scope-model interface are specified; localized name fields and true identity checks are distinct, with negative fixtures. | Resolved |
| IA-06 / major / requirement-quality | AIC-REQ-04, A12/QAS-05 | Revised A13-A15 could be omitted from release/integration gates. A12 and QAS-05 now include the revised candidate; the functional public smoke set, technical implemented-status gate and accepted manifest carry new navigation/support/name criteria. | Resolved |
| IA-07 / major / task-quality | Tasks, T9/T12 dependencies | TASK-010/TASK-013: T12 could finish without T9 and T9 could review an obsolete baseline. T9 now depends on T19, T12 on T19 and T9; one actual review can supply separately recorded criteria for the same revision. | Resolved |
| IA-08 / major / task-quality | Tasks, T16-T19 governance and acceptance | TASK-015/TASK-017: affected modules and verification did not fully locate shared routing, scope/model/name changes or maintenance-guide refresh. Exact planned/existing paths and tests are recorded, including language/history/native mirrors, translation/identity negatives and final assembly evidence. | Resolved |
| IA-09 / minor / technical-design-quality | Technical design, integrated contracts and Source | TDES-015: already implemented adapters were labeled nonexistent/planned, and old acceptance boundaries stopped at A12. Baseline contracts are now explicitly historical implemented contracts with revision extensions; current A1-A15 scope and source request/date are recorded. | Resolved |

The requirement's A13-A15 criteria were moved before its Review evidence subsection
so all acceptance items share the same section scope. No source meaning, owner
acceptance or remote availability was invented to close a finding.

### Remaining approval findings

These are known unmet conditions, not unknown evidence and not waived. They are
retained because a review/repair instruction is not approval of the revised plan.
All have maturity `ready` and severity `major`.

| ID / category | Location | Description / next action |
| --- | --- | --- |
| G-01 / functional-design-quality | Functional design, parent frontmatter | The requirement parent is a revision draft. Functional-design-modeling 4.1 and functional-design-quality Traceability require an approved parent for formal downstream readiness. Record actual requirement approval before formal handoff. |
| G-02 / technical-design-quality | Technical design, parent frontmatter | technical-design-quality@2.5.0/TDES-022: the functional parent is draft. Record actual functional approval before technical-design handoff; this review does not approve it. |
| G-03 / task-quality | Tasks, parent frontmatter and Execution gates | Task-modeling upstream approval condition is not met because the technical parent is draft. Keep the revision as planning input until actual technical approval; T16-T19 remain Todo, not assigned or started. |

Requirement content re-review has no remaining content finding and is ready for
owner approval. Functional, technical and task content defects above are repaired,
but their formal downstream gates remain blocked by G-01/G-02/G-03. No claim of
zero overall findings or readiness to code is made. T12 remains In Progress,
T9/T13/T16-T19 remain Todo. No approval or owner comprehension is inferred.

### Rule coverage metadata

`review-requirements` and `review-functional-design` use non-ID checklist Rules:
all required fields/sections, conditional business/UI/delivery-state/permission
sections, source/trace/quality-scenario obligations and five review dimensions
were checked. G-01 is the remaining functional approval condition. No deferred
support translation is used as permission to change product scope: T17/T18 author
bounded source-backed content under the defined acceptance rules.

Technical-design coverage (`rule_set: technical-design-quality`, `version: 2.5.0`):

- `passed`: TDES-001–009, TDES-011, TDES-013–021, TDES-023–024, TDES-028.
- `waived`: [].
- `not_applicable`: TDES-010 (no required declared parameter), TDES-012/027 (no persisted schema/backfill/breaking migration), TDES-025 (technical design cites local contracts, no new external specification), TDES-026 (no platform or structural decision beyond this bounded change).
- `evidence_limited`: [].
- Known failed item: TDES-022, represented by G-02 above rather than mislabeled as missing evidence.

Task coverage (`rule_set: task-quality`, `version: 2.4.0`):

- `passed`: TASK-001, TASK-003–017, TASK-019.
- `waived`: [].
- `not_applicable`: TASK-002 (living progress record, not new handoff), TASK-018 (no waiver).
- `evidence_limited`: [].

TASK-011 checks that the parent resolves; that passes while the separate modeled
approved-parent prerequisite G-03 remains unmet. TASK-007 is evaluated against
bounded deliverables, not an invented session-duration budget. Engineering tactics
and verification for every cited ARC/TST/ERR item are reviewed as planning
obligations; no post-coding Rule pass is asserted by this documentation review.

### Verification and limits

The corrected chain is A13 → F12 → TD11 → T16, A14 → F13 → TD12 → T17,
A15 → F14 → TD13 → T18, followed by T19 → T9 → T12 → T13. Existing A1-A12 and
release/recovery obligations remain. The same actual owner feedback may satisfy
T9 and T12 without duplicate walkthroughs, provided all named criteria and exact
runtime identity are recorded. T13 requires all local criteria plus separate
publication authorization. The working null-owner manifest is explicitly not an
accepted manifest.

Document lint, link graph, hygiene, task DAG/trace/Rule-reference checks and protected
file hashes are checked for this review. No runtime/browser tests were run because
no runtime bytes changed. Previous machine reports remain bound to their old
revision and cannot prove the revised information architecture.

Validation result: all five reviewed Markdown files pass markdownlint; link checks
report zero broken relative links/forbidden downward references; hygiene passes
410 documents; all 19 task IDs/dependencies, Fibonacci estimates, A/F/TD trace IDs
and cited engineering Rule IDs pass. Protected before/after inventories are
byte-identical. `git diff --check` passes.

Reviewed document identities (audit excluded to avoid self-reference):

| Document | SHA-256 |
| --- | --- |
| [AIC-REQ-04.md](../requirements-planning/AIC-REQ-04.md) | `86fc69ddd7639e1244b27f085c811e53ac41c0b6dc673b031215dbfbcfc8cf27` |
| [2026-10-27-help-discovery-functional-design.md](../designs/2026-10-27-help-discovery-functional-design.md) | `3c22903eae3ddd2a0cf9161dd902a3f95abb8fce8479fa0a6a666ad5b8e0e693` |
| [2026-10-27-help-discovery-technical-design.md](../designs/2026-10-27-help-discovery-technical-design.md) | `72ffe1d88e56d947938c877b7754470101ea58e3200598a073f54ae27a5f95a7` |
| [help-discovery-tasks.md](../designs/help-discovery-tasks.md) | `32e155f78f8114aad709c9d1a8ec86d31c0891b95f281fecdcd1051e1d5de8d1` |

## AIC-REQ-04 approved site-structure implementation, 2026-10-28

### Authority and delivered scope

The owner explicitly approved the revised requirement, functional design,
technical design and tasks, and authorized T16-T19 local website implementation,
verification and record synchronization before another T12 review. G-01/G-02/G-03
from the previous review are resolved by that actual approval. No publication,
commit, push or other remote mutation is authorized or performed.

T16 delivers shared Home / Capability overview / Asset directory navigation and
Get started action in both editions, separate language/theme utilities and local
skill lookup. The graph stays the overview's single main view at existing routes;
the complete four-type directory stays at original homepage/type anchors. Native
headers and four-type context mirrors have explicit data owners and tests.
Language/type bookmarks, back/forward, active destination and no-JS directory access
pass. Plain scrolling does not change the selected destination.

T17 delivers visible cross-cutting support labels for foundations and communication
inside the graph, with per-target conditions/sources and same-map subject links.
The first uses adopted project-entry conventions for seven work subjects; the
second offers context-independent handoff for eight. Conditions are optional
applicability, not an execution fan or universal prerequisite. Quotes match the
pinned canonical source revision locally; no public availability is inferred.
Existing 13 topic edges, two loops and 53 skill relations retain their meanings.

T18 delivers reviewed Chinese names for all 70 current skills, separately visible
from canonical IDs and purposes; panel headings and name/ID/purpose lookup use the
same locale records. English retains formal names with separate purposes. True
identity/placeholder/shape guards remain, while translated display names are allowed.
No canonical asset ID, skill definition or source registry changed.

T19 completes the local machine/engineering portion. The
[revision evidence guide](../../tests/website/evidence/revision/README.md) records
38 Node tests, 18 Python tests, 200 topic/size/theme selections, 140 skill paths,
20 control scenarios, 20 navigation/support/name scenarios and 16 contrast samples
including new names/support/navigation labels. Eight clipboard recovery cases,
script-free/blocked-entry fallback, root closure, locale/source/cache checks and
acyclic module wiring pass. Pointer and keyboard navigation, focus and visual
captures were inspected in both languages/themes and mobile/desktop sizes.

The [engineering/alignment review](../../tests/website/evidence/revision/review.json)
has no in-scope code finding. Human A9/final A11 evidence remains explicitly limited.
The [working manifest](../../website/.openai/runtime-manifest.json) records 40 runtime
files with exact hashes, canonical asset revision and `ownerConclusion:null`; it
is not an accepted release manifest. Old evidence stays bound to the old candidate.

### Repairs and remaining acceptance

Intent-derived failing tests preceded new route/name/scope behavior. Additional
red/green repairs cover missing scope providers, native-copy ownership, the mobile
Get started link hidden by old styles, desktop overview height and a work-panel
body compressed by long names. The minimum usable body assertion was retained;
layout was corrected instead of weakening it. Final overview remains visible at
1280x800, and selected skill/topic context remains above the mobile sheet.

T16-T19 are Done for this local candidate. T9 remains Todo; T12 remains In Progress
pending the owner's actual whole-map/site conclusion on this exact revision.
One review may supply both records: coverage, relationships, purpose/use,
site structure, support scope and localized-name distinction. Approval of documents
and tests do not provide that conclusion. T13 remains Todo and unauthorized.

Native devices, browser zoom and spoken-screen-reader behavior remain unverified;
recorded browser checks use local Chromium emulation. Public source reachability,
TLS/provider behavior, real deployment/recovery and publication were not tested.
No hosting receipt, workflow, DNS/host/audience or original prototype was changed.

Final candidate identity: `sha256:3e757275765c789bab7a213d26e9c42e0827973a571bbfde6832d31e32037a67`. All 40 runtime hashes,
approved parent statuses, 19-task dependency/Done states and preserved prototype/
workflow/hosting receipts were rechecked. Markdownlint passed for ten changed
documents; link checks report zero broken relative links or forbidden downward
references; hygiene passes 411 documents; `git diff --check` passes. Browser
reports match current explorer source hashes. T9/T12 remain pending actual owner
feedback, not additional document approval.

## AIC-REQ-04 single-page dual-view revision, 2026-10-28

### Authority and changed decisions

The owner reconsidered the original homepage cards and identified unclear skill
order and parent/child relationships as the gap. They requested Classification
and Relationships as two switchable views on one webpage, then authorized revision
of AIC-REQ-04 and its functional/technical designs and tasks only. No website,
prototype, test/evidence, hosting record or publication is changed by this instruction.

This explicitly replaces the earlier graph-only/no-switch and dedicated explorer
decisions. The stable document chain is revised at the owner's request; its
status is draft. Earlier approval, T16-T19 completion and source-bound evidence
remain historical, not approval or acceptance of this changed scheme.

### Product and engineering handoff

The homepage capability section defaults to original six-theme rectangular
Classification; Relationships reuses the connected graph. One active renderer
shares one selected skill/work/relation, detail surface, lookup and request owner.
A compact complete four-type directory remains on the same page without repeating
a second six-theme overview. Old explorer URLs become same-page compatibility
entries with native links, not another interactive application. Existing useful
category/type/install links are mapped; the former directory meaning of
`#capabilities` is explicitly replaced by the unified host.

A16/R11 defines only source-backed partial order and coordinator parent/child
calls, labeled required or conditional. Category membership, method reuse, artifact
inputs and recommendations do not create children or mandatory numbered steps.
Multiple callers reference one primary skill entry per view; cycles use finite
return links. Existing curated edges and original card output arrows require
source review before serving as sequence/child evidence.

A17/R12 and the functional state table preserve selected identity/work/relation,
detail mode/open state, query, edited request and pending-copy token across both
switch directions. Each view separately remembers disclosure/scroll/pan. Reveal
may override only incompatible collapse/off-screen position. Focus stays on the
switch; hidden nodes leave the tab order; later close resolves an active-view
opener. Work-only/relation-only/no-selection states do not fabricate a skill.
Reload/language persistence of ephemeral content is not promised.

A4/A6/A13 revise experience/site structure; A16 → F15 → TD15 → T20/T22/T23 covers
order/hierarchy; A17 → F4/F16 → TD14 → T21/T22/T23 covers state. TD11/T24 covers
same-page assembly, compact directory and compatibility. TD16/T25 covers final
verification. QAS-02/QAS-04/QAS-05 and the release smoke/manifest requirements
include both views; existing bilingual guidance/support and release recovery remain.

### Tasks, status and verification boundary

New T20-T25 are Todo: semantic/partition audit, shared host/state, classification,
relationship adapter, same-page assembly and final verification. Their order is
T20 → T21 → (T22 and T23) → T24 → T25 → T9 → T12 → T13. T9/T12 require actual
review of identified new bytes; T12 stays In Progress as the ongoing acceptance
record. One actual walkthrough can supply distinct conclusions without two quizzes.
T13 remains Todo and unauthorized. No prior task/evidence proves the new scheme.

The author self-check covers module/data ownership, navigation and native/legacy
closure, source-backed hierarchy/partial-order counterexamples, state/error/focus
branches, stable trace IDs and task dependencies. The changed UI triggers a full
functional UI record; original cards and verified graph captures are cited as
reuse baselines, not dual-view implementation. No external reference or new package
is needed. Exact edge content is bounded source authoring in T20, not authority to
invent missing relationships. Parent approvals remain unmet for formal handoff;
this synchronized planning draft neither waives them nor authorizes coding.

Validation: all eight revised Markdown documents pass markdownlint; repository
links report zero broken relative paths or forbidden downward references; hygiene
passes 413 documents. The 25-task DAG, required fields/Fibonacci estimates,
A1-A17/F1-F16/TD1-TD16 identity sets, active engineering Rule references and draft/
acceptance states pass checks. Before/after SHA-256 inventories confirm website,
prototype, website tests/evidence and workflows are byte-identical. `git diff --check`
passes. No runtime/browser tests were rerun for this documentation-only change.

## AIC-REQ-04 dual-view re-review, 2026-10-28

### Scope and method

The owner requested review/repair of the dual-view requirement, functional design,
technical design and tasks, focusing on skill order, parent/child meaning, state
retention and acceptance consistency. `review-requirements`,
`review-functional-design`, `review-technical-design` and `review-tasks` were applied
as separate evaluations; document repairs followed outside their evaluative scope,
then affected clauses and their traces were re-reviewed. No website, prototype,
website test/evidence, hosting record or publication is part of this change.

Canonical versions: requirement-modeling 6.1.0 / requirement-quality 2.4.0;
functional-design-modeling 2.0.0 / functional-design-quality 2.0.0;
technical-design-modeling 2.2.0 / technical-design-quality 2.5.0;
task-modeling 2.2.0 / task-quality 2.4.0; findings-list 2.0.1. Referenced ARC/TST/ERR
versions remain 1.4.0/1.4.0/1.2.0. Quality-attribute, interface-change and shared-value
apply; no persisted-data migration, declared performance/session budget, new
runtime service or waiver is introduced. Draft status is not a content exemption.

### Findings repaired and re-reviewed

All findings below have maturity `ready`; each location names its document section.
The same defect's task changes are remediation trace, not a separate duplicate.

| ID / severity / category | Location | Finding and repair | Re-review |
| --- | --- | --- | --- |
| DV-01 / major / requirement-quality | AIC-REQ-04 R11/A16 | Required calls had no explicit parent-path scope, and unordered peers could be read as parallel work. Required is now relative to the applicable route/scenario; missing ordering evidence is unspecified order, never proof of parallelism. Both designs and T20 fixtures carry the distinction. | Resolved |
| DV-02 / major / technical-design-quality | Technical design, relationship projections | TDES-011/014: cyclic calls and contradictory ordering could both be converted into feedback references, masking invalid sequence evidence. Deterministic acyclic call presentation retains source call references; per-scenario before-graph contradictions reject acceptance. Real feedback remains separately evidenced. | Resolved |
| DV-03 / major / technical-design-quality | Technical design, relationship-model signatures | TDES-011: category-only hierarchy/order signatures could not serve ten work-topic groups in Relationships. Shared projection APIs now accept validated view/group identity and use the correct category or metadata ownership map, preserving semantic equality without demanding identical layout. T20/T23 cover both. | Resolved |
| DV-04 / major / technical-design-quality | Technical design, shared state and renderer contracts | TDES-011/014: selected skill/relation IDs did not identify the active explanation; switching could replace a relation/support detail with a stale skill. Added authoritative typed detail target, selectSupport/selectWork callbacks, target/mode normalization, reveal priority and same-work request-preservation rules. R12/A17, FD and T21/T25 trace them. | Resolved |
| DV-05 / major / functional-design-quality | Functional design, switching focus state | Unconditional focus-to-switch conflicted with a preserved open modal lookup during history navigation. User switches focus their button; history switches retain the modal trap/query, and modal close returns to a visible shared trigger. Requirement, technical callbacks and keyboard acceptance agree. | Resolved |
| DV-06 / major / functional-design-quality | Functional design, collapse versus switching | Closing a selected branch could leave a selected ID that switching immediately reopened. Explicit collapse now clears its owned active selection/detail, invalidates pending copy and focuses disclosure; hiding a view never performs that action. Inactive layouts remain saved. T21/T25 verify the distinction. | Resolved |
| DV-07 / major / technical-design-quality | Technical design, native section/view route contract | TDES-013/014: same-page hrefs could reload the host and erase state; explicit Relations plus old category anchor had no deterministic outcome. Valid same-document navigation updates the live host without reload; cold/no-JS links remain native. Explicit view wins with a category-context hint rather than invented selection; absent explicit view opens the requested classification card. T24/T25 cover history and controller identity. | Resolved |
| DV-08 / minor / requirement-quality | AIC-REQ-04 A1/A3/A11/A12 and task acceptance | Old global-map/home-to-explorer wording and incomplete edge-state traces contradicted the dual-view revision. Both-view discovery/acceptance and same-page/legacy navigation now agree; T20-T25 and review matrix name the corrected semantic/state/URL counterexamples. | Resolved |

No new product goal, real skill execution, persistent user state or publication
permission was added. Repairs specify outcomes already required by correct
relationships, retained state, accessible interaction and the same-page scheme.

### Remaining approval findings

Three known unmet approval conditions remain, each `major`, maturity `ready`:

| ID / category | Location | Description and next condition |
| --- | --- | --- |
| DVG-01 / functional-design-quality | Functional-design parent frontmatter | Requirement is draft. Functional-design-modeling 4.1 and the functional quality traceability gate require actual requirement approval before formal downstream readiness. |
| DVG-02 / technical-design-quality | Technical-design parent frontmatter | technical-design-quality@2.5.0/TDES-022: functional parent is draft; actual approval is required for formal technical-design handoff. |
| DVG-03 / task-quality | Tasks parent and execution gates | Task-modeling approved technical-parent prerequisite is unmet. Keep new tasks Todo; this review/repair request is not revised-plan approval or implementation authorization. |

These are known failed prerequisites, not missing runtime evidence or waivers.
Requirement content is ready for owner approval. Other content findings are repaired,
but no zero-overall-findings or ready-to-code result is claimed. T20-T25 remain Todo,
T9 remains Todo, T12 remains In Progress awaiting the new scheme, T13 remains Todo
and unauthorized. Earlier Done rows remain historical and cannot verify this plan.

### Rule coverage metadata

Requirement/functional non-ID checklist coverage: required identity/section order,
conditional rules/quality scenarios, UI decisions, delivery states/roles, source
and five dimensions were checked; only DVG-01 remains in functional gate status.

Technical design (`rule_set: technical-design-quality`, `version: 2.5.0`):

- `passed`: TDES-001–009, TDES-011, TDES-013–021, TDES-023–024, TDES-028.
- `waived`: [].
- `not_applicable`: TDES-010 (no needed declared parameter), TDES-012/027 (no persisted schema or irreversible migration), TDES-025 (local contracts, no new external specification citation), TDES-026 (no structural platform decision beyond this bounded revision).
- `evidence_limited`: [].
- Known failed item: TDES-022, represented by DVG-02 above.

Tasks (`rule_set: task-quality`, `version: 2.4.0`):

- `passed`: TASK-001, TASK-003–017, TASK-019.
- `waived`: [].
- `not_applicable`: TASK-002 (living progress/revision record, not fresh execution handoff), TASK-018 (no waiver).
- `evidence_limited`: [].

TASK-011 resolves the parent path; that passes while the separate modeled approval
prerequisite DVG-03 remains unmet. Session bounds are judged against deliverables,
not an invented duration. Engineering tactics and named verification were reviewed
as design obligations only, not claimed as post-coding/runtime passes.

Validation: all five reviewed Markdown documents pass markdownlint. Relative-link
checks report zero broken paths/forbidden downward references; hygiene passes
413 documents. A/F/TD/R identity sets, active engineering Rule citations, all 25
task fields/Fibonacci estimates, dependency DAG and unchanged task/draft gates pass.
Before/after SHA-256 inventories confirm website, prototype, website tests/evidence
and workflows are byte-identical. `git diff --check` passes. No browser/runtime
tests were rerun because only documents changed.

Reviewed identities (audit excluded to avoid self-reference):

| Document | SHA-256 |
| --- | --- |
| [AIC-REQ-04.md](../requirements-planning/AIC-REQ-04.md) | `ba7be3e66f9e8f2d329a7cdc3423b606c21dac735de872181edf97f8cf94a477` |
| [2026-10-27-help-discovery-functional-design.md](../designs/2026-10-27-help-discovery-functional-design.md) | `28e67c03b60ad440260e10aae4d91b050bfe4c5c765e49233885d0824ab78536` |
| [2026-10-27-help-discovery-technical-design.md](../designs/2026-10-27-help-discovery-technical-design.md) | `47bb63b1fca9d3fe5f8c885c35e390355e2ece6acf20ffbbd85c0d92117e42f9` |
| [help-discovery-tasks.md](../designs/help-discovery-tasks.md) | `1a4a0147be4c2804f8a0ae93ed065559bf21cb0655e3e43ec9484b78f4f4112d` |

## AIC-REQ-04 approved dual-view implementation, 2026-10-28

The owner explicitly approved the revised requirement, functional design, technical
design and tasks, and authorized T20-T25 local implementation, verification and
record synchronization. This resolves the prior document-approval gates; it does
not supply T9/T12 experience acceptance or permission to commit, push or publish.

T20-T25 are locally complete. Both homepage editions now contain one capability
section: original six-card Classification by default and the retained Relationships
graph as a switch. One shared detail, lookup and editable request controller uses
canonical skill identity and localized usage. Required/conditional call hierarchy,
scenario-scoped partial order, other references and support retain their sources.
The complete four-type directory is compact and separate; old explorer URLs are
compatibility entries to the homepage. The superseded graph composition is removed.

The source audit verifies 59 skill relationship quotes (36 calls and six scenario
order edges) at the pinned asset revision. Exact category/registry partition,
missing/foreign/duplicate identities, invalid layouts and contradictory sequences
have negative fixtures. Captured red tests preceded the pure model/state repairs.
Browser regression exposed and repaired a covered lookup control, delayed modal
focus, a local route crossing another child, and long selected labels behind the
responsive sheet. Local routes now use the reserved outside gutter; the list
height accounts for available space above the sheet.

Final checks: 44 Node tests and 18 Python tests pass; 20 bilingual/two-theme/five-width
dual-view cases and 280 skill usage paths pass. Both relationship matrices pass
20 geometry cases and 140 graph skill paths; 20 controls cases plus contrast,
no-JS/blocked module and absent/rejected/late clipboard recovery pass. Both-way
switching checks edited and pending requests, active relation/support explanation,
modal-history focus, explicit collapse, per-view local scroll and no-reload section
navigation. Actual selected desktop/mobile screenshots were inspected. The local
ESM graph is acyclic; all 47 runtime/static files are hashed. Engineering review
and the separate implementation-alignment review have no unresolved local finding.

Candidate: `sha256:a5abad1224f5f466b1655ccca9cc32de4a01da99639857bdd540c8e274282027`. Detailed results, repaired red evidence, Rule coverage and
traceability are in [the dual-view evidence guide](../../tests/website/evidence/dual/README.md).
The working runtime manifest has a null owner conclusion and publication disabled.
297 previously captured prototype/workflow/hosting/evidence files are unchanged.
Public source reachability, deployed serving/TLS/hash and release/recovery evidence
are not claimed. T9 remains Todo, T12 In Progress awaiting actual owner review,
and T13 Todo and unauthorized. No remote mutation or publication occurred.

In-scope Markdown, relative links and document hygiene pass. A full-repository
Markdown check reports three existing MD032 blank-line issues in the unrelated,
uncommitted AIC-REQ-05 (lines 70, 74, 79); those files were preserved. No full-repo
Markdown pass is claimed. See the dual evidence document-check record.

## AIC-REQ-04 local readability follow-up, 2026-10-28

The owner explicitly invoked `design-taste-frontend` after local dual-view delivery.
The design read is preserve-mode capability discovery for developers, with
variance/motion/density 3/2/5. The audit retains the neutral green-gray theme,
rust action accent and semantic green support notation, native system type,
existing illustration, original six functional categories and single-page IA.
Marketing-page bento/hero/image-generation prescriptions do not apply to this
bounded capability-reading repair. No branding/navigation/data/workflow overhaul
is inferred from the skill invocation.

The audit identified arbitrarily broken English topic words, competing topic
count/title widths, and overly small identifiers/call captions. Local CSS now
places counts beneath names, wraps names naturally, and raises classification
IDs to 11px, purposes to 13px and call/reference captions to 12px. Local graph
call captions are 10px; the selected detail retains full-size explanations.
Content/control radii use 4px with the existing 8px mobile-sheet exception.
A captured failed dual-view regression exposed tablet references under the sheet
after the larger captions; the classification list's available height was then
bounded above it. Tests exercise the real click path rather than forced clicks.

Current candidate: `sha256:dff7c2c888c7970d9cd5e7b9691843d522f2161aae41c9bb7b023921bd3886db`. See [refinement evidence](../../tests/website/evidence/taste/README.md)
for visual inspection, final checks and preflight applicability. The local
Lighthouse package is unavailable; no Lighthouse/Core Web Vitals pass is claimed.
Canonical quoted catalog descriptions are preserved even where source punctuation
differs from the skill's presentation preferences. Existing source audit remains
valid because definitions, relationships and guidance are unchanged.

T9/T12 owner acceptance remains pending for this changed candidate. T13 and
commit/push/publication remain unauthorized; hosting receipts are unchanged.

Refinement verification: 44 Node and 18 Python tests pass; 16 typography cases,
20 dual-view cases/280 usage paths, 20 graph geometry cases/140 graph usage paths,
20 controls cases and contrast/recovery checks pass. Actual selected screenshots
were inspected in both locales/themes. Scoped Markdown, relative links, hygiene
and whitespace checks pass. All 47 current runtime hashes match the working
manifest; the actual owner conclusion remains null.

## AIC-REQ-04 authorized publication preflight, 2026-10-28

The owner explicitly stated that T12 passed and authorized publication under T13.
The actual accepted identity `sha256:dff7c2c888c7970d9cd5e7b9691843d522f2161aae41c9bb7b023921bd3886db` and seven integrated owner conclusions are
preserved in [the accepted manifest](../../tests/website/evidence/release/accepted-runtime-manifest.json).
T9 is Done. T12 was accepted for those bytes; the new targeted compatibility repair
below reopens its affected candidate gate, not the unchanged content decision.

Sites confirms the existing public Site, custom domain, version 7 and successful
deployment; verified HTTPS serves all ten known-good files, with expected HTML
security-script insertion and exact non-HTML content. The source checkout opens
at its recorded commit. The helper initially failed under the folder's Node 20;
using the existing bundled Node runtime succeeded without installation. The
existing saved version and a local source backup provide the recovery baseline.
137 canonical public source URLs pass reachability/content checks, including
pinned skill-definition hashes.

Pre-switch HTTPS confirmed `/zh.html?lang=zh` normalizes to `/zh?lang=zh`.
Serving accepted bytes locally under that observed path reproduces `Unknown site
path`. The repair accepts only explicit normalized home/legacy aliases and keeps
unknown paths rejected; the full cache identity changes to `aic04-host-1`.
No visual/content/workflow changes were made. Red-first alias tests then pass;
46 Node, 18 Python and eight provider-route simulation cases verify section,
state/request, language/view and legacy-entry behavior. Simulation is explicitly
not deployed public smoke.

Repaired identity: `sha256:1424a8bb40733a4a06ce41cbd4b63e9c411d4bb35ff941aad5b9eebb115d57ca`. The isolated local archive contains only 47 runtime
files plus hosting metadata; no repository docs, credentials or Git metadata are
packaged. No source push, version save, deployment, DNS or audience mutation has
occurred. Version 7 remains verified serving. T13 is In Progress, awaiting targeted
owner confirmation under the task record's existing changed-byte gate. Final
public TLS/MIME/hash/smoke checks remain unexecuted until actual publication.
The [release record](../../tests/website/evidence/release/README.md) carries evidence,
archive identity, baseline and exact continuation/recovery steps.

## AIC-REQ-04 published and publicly verified, 2026-10-28

The owner explicitly approved the clean-URL compatibility repair and continuation
of T13. Accepted identity: `sha256:1424a8bb40733a4a06ce41cbd4b63e9c411d4bb35ff941aad5b9eebb115d57ca`. The runtime did not change during
publication; the accepted manifest records the actual integrated and supplemental
owner conclusions. Source commit `f9762c952eb9c3847524dbdd2d52376c4224a19d` was saved/pushed only
in the isolated Sites source checkout, saved as version 8 and successfully deployed
as `appgdep_6ae181e21bbc81919009450c9496f0af`. The AI Cortex repository was not committed or pushed.

The public domain and audience are unchanged. All 47 runtime resources pass
verified HTTPS, expected MIME and accepted-source checks: 43 non-HTML files match
bytes exactly; all four HTML sources are preserved with only the provider security
script inserted. The two legacy HTML stubs omit a closing body tag, so the observed
provider script follows their exact source rather than appearing before a closing
body. The verifier initially assumed the latter position; new failing fixtures
and targeted repair verify both placements while rejecting changed source or
unrecognized/multiple inserted HTML. This verification-oracle repair changed no
published runtime bytes.

Eight actual public browser cases cover both locales, 360/1280 widths and both
themes: direct views, real coordinator children, conditional call and scenario
order, full guidance, edited request/view continuity, clipboard denial recovery,
keyboard close/focus, cross-topic support, full directory/type/install/history,
language/theme and legacy routes. Both locales pass actual no-JS and blocked-entry
recovery. There are zero public page errors. The smoke harness waits for theme
restoration after language navigation before checking it; no startup default is
mistaken for the settled state. The known-good version 7 remains available;
recovery was not needed or executed. No DNS/audience change occurred.

T9/T12/T13 and all associated implementation tasks are Done; AIC-REQ-04 is
implemented on 2026-10-28. [Release evidence](../../tests/website/evidence/release/README.md)
and the canonical deployment/public/runtime manifests record exact identities,
checks, limits and continuation/recovery. Local upload and provider archive hashes
are retained separately; runtime/source identity is verified independently rather
than claiming byte equality of differently stored containers. No Lighthouse score,
native-device or spoken screen-reader result is claimed.
