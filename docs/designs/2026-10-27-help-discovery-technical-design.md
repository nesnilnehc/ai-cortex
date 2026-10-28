---
artifact_type: technical-design
lifecycle: snapshot
created_at: 2026-10-27
parent: 2026-10-27-help-discovery-functional-design.md
status: approved
---

# Technical design: direct work relations and locally owned skill branches

Final delivery (2026-10-28): the owner approved the dual-view documents,
accepted T12, approved the address compatibility repair and authorized T13.
Sites version 8 is published and public verification passes on the unchanged
accepted runtime. T9/T12/T13 are Done. Earlier dated planning/local records retain
their historical scope; current outcome is the [published audit](../calibration/audit-docs.md#aic-req-04-published-and-publicly-verified-2026-10-28).

## Goal

Compose two same-page capability renderers over shared source-backed skill, relationship and UI-state owners, preserving compatible navigation and verifiable switching continuity.

## Architecture and service decomposition

| Boundary | Owner / planned location | Dependencies |
| --- | --- | --- |
| Canonical definitions | Existing registry and defining Skill/Spec/Protocol/Rule files | No runtime network fetch; pinned source identity |
| Skill identity/guidance/work context | Existing `website/explore/skill-metadata.json`, `locales/`, `workflow.mjs`, `panel-model.mjs` | Canonical IDs and 70-skill baseline; current set verified at implementation |
| Classification ownership | Planned `website/explore/classification.json` | Extract original six homepage skill groups once, validate exact registry partition; labels in locales |
| Concrete relationships | Existing `website/explore/skill-edges.json`, extended after source audit | One edge owner for both projections; quote/hash, call/sequence evidence |
| Shared state / host | Planned `website/explore/explorer-state.mjs`, `explorer-host.mjs` | Pure models, existing request token owner and shared explanation |
| Classification renderer | Planned `website/explore/classification-view.mjs` | Classification partition, call forest/partial order, shared state callbacks |
| Relationship renderer | Planned `website/explore/relationship-view.mjs` | Existing topic/skill graph/router/support models behind host callbacks |
| Same-page entry / navigation | Existing homepage HTML, `main.mjs`, `site-navigation.json`, `site-navigation.mjs` | Section routes, native fallback and legacy explorer compatibility |
| Verification | `tests/website/`, current audit and working runtime manifest | Root-isolated local preview; never a runtime import |

Home composition wires host, shared details and renderer adapters explicitly.
Pure data/models never import renderers or the host. The old graph `story.mjs`
composition is split rather than importing an entire second application into the
homepage. Exactly one shared dialog/detail/request/copy owner is registered.
Existing graph modules/assets can remain under `website/explore/`; module location
does not create a separate user page. No new package/framework/service is required.

## Components and detailed design

### Single-source records and projections

| Value | Single owner | Consumers / reconciliation |
| --- | --- | --- |
| Skill ID, defining paths/hashes, logical work-topic owner | `skill-metadata.json` under `website/explore/` | Both renderers and shared details; registry/source tests |
| Six category IDs and skill membership | Planned `website/explore/classification.json`: `{groups:[{id,skillIds:string[]}]}` | Native cards and classification model; exact partition and original-group migration fixtures |
| Display names/purpose/guidance, category/view/relationship labels | Existing `website/explore/locales/en.json`, `zh.json` | Both renderers and native mirrors; exact locale/key/static parity |
| Edge identity/type/conditions/provenance | Existing `website/explore/skill-edges.json`, extended schema below | Both projections and same shared relation details; one editable record, not independent forests/graphs |
| Work-topic graph and support applicability | Existing `global-topic-graph.mjs`, `topic-edges.json`, `support-scopes.json` under explorer | Relationship renderer and shared support detail; classification references the same scope rather than inferring category-based calls |
| Global routes/labels/section ownership | Existing `website/site-navigation.json` | Shared adapter and all native header/alternate mirrors; same-page/legacy route tests |
| Ephemeral selected state and view-local layout | Planned `website/explore/explorer-state.mjs` | Host and renderers; no persistent project data |
| Request text/version/copy token | Existing textarea and `request-state.mjs` | Shared host; view change does not call select/edit/clear/begin |

Six category IDs retain `map-research`, `map-planning`, `map-quality`,
`map-delivery`, `map-collaboration`, `map-library`. Their names/membership come from
the original homepage cards, not the ten graph topic IDs. A skill's logical work
context continues to resolve from metadata regardless of representation/category.
No second editable skill purpose list remains in homepage markup: native mirrors
must reconcile to the locale/identity owners. The compact four-type directory may
contain lookup references to the same skills; it is not a third execution forest.

Extend the canonical concrete-edge record with types `sequence` and `feedback`
alongside existing `call`, `method`, `input`, `suggest`. A call adds
`callMode:'required'|'conditional'`; conditional calls require a localized condition.
A call also names its applicable parent path/scenario in its condition; required
means required inside that applicable route only. A sequence adds
`scenarioId:string`, a nonempty condition and defining evidence
for the ordering within that compatible scenario; it is not a total rank.
All edges retain stable ID/from/to/source quote(s), locale label/condition keys and
pinned definition identity. Validate endpoints, source inclusion, required fields
and locale parity. Existing 53 curated edges are the migration baseline, not the
required total or a license to turn method/input/suggest edges into children.

Planned pure `relationship-model.mjs` exports
`getCallHierarchy({view,groupId}): {roots,children,references}` and
`getSkillOrder({view,groupId,scenarioId?}): {before,peers,feedback}`. `groupId` resolves
through classification membership for Classification and metadata work-topic
ownership for Relationships; unknown/foreign group IDs reject. Projections may
use different nesting/reference placement while preserving the same edge meaning. Call hierarchy uses
only audited call edges. A shared child has one primary presentation per view;
use a deterministic source-order/ID tie-break for its presentation parent and label
other parent links as references, never as absence of that real call. Cross-category
calls remain labeled navigable references. Cyclic calls do not recurse: emit a
finite reference/feedback explanation. Artifact-input/method/recommendation edges
remain related references. Unsupported peers use stable non-execution browse order.
Every original edge remains inspectable in shared details even when not a tree arc.
Validate call projection per category with cycle detection: choose a deterministic
acyclic presentation parent using source order then ID, demoting any cycle-forming
arc to an explicit call reference without deleting the source relationship.
Sequence constraints are checked independently per scenario; a cycle in their
before relation is rejected rather than topologically sorted or relabeled feedback.
Do not merge incompatible scenario branches into one linear order. Unordered peers
mean unspecified execution order unless the source explicitly establishes parallelism.

### State ownership and switching contract

Planned `createExplorerState(initial)` exposes `snapshot()`,
`selectSkill(skillId)`, `selectWork(workId)`, `selectRelation(relationId)`, `selectSupport(scopeId)`, `setView(view)`,
`setDetailMode(mode)`, `closeDetail()` and `updateViewState(view,patch)`.
IDs and enums are validated before mutation; unknown selections fail rather than
silently picking a different skill. Records are copied snapshots.

State shape:

```text
view: classification | relations
selectedSkillId: string | null
selectedWorkId: string | null
selectedRelationId: string | null
detail: {open:boolean, target:null|{kind:skill|work|relation|support,id:string}, mode:usage|relations|work}
lookup: {open:boolean, query:string}
viewState:
  classification: {expandedCategoryIds:string[], scrollByRegion:record, focusedSkillId:string|null}
  relations: {expandedTopicId:string|null, scrollByRegion:record, pan:{x:number,y:number}, focusedSkillId:string|null}
```

Selection normalization is explicit: `selectSkill` opens skill/usage and sets its
logical work; `selectWork` opens work/work without inventing a skill;
`selectRelation` opens relation/relations, and `selectSupport` opens support/work,
retaining an independent prior selected skill/work as context. Mode changes are
valid for skill targets (usage/relations/work); work/support targets use work,
relation targets use relations. Invalid target/mode combinations fail before
mutation. Switching never re-applies these selection defaults. Only a real logical
work change announces request replacement; changing relation/support detail within
the same work cannot reset edited text. `closeDetail` clears active target/open
state and invalidates a pending copy, but may retain selected-skill highlight;
explicit branch collapse additionally clears that branch's selection.

Request text/version/pending token stays with the existing request controller and
DOM owner; it is not copied into a second renderer state. Both projections resolve
the same `selectedSkillId` to their own category/topic. `setView` changes only view
and its local layout restoration; it never reselects work, resets mode/query/text,
closes detail or starts/invalidates copying. Actual skill/context change, edit and
close retain the existing request identity rules. `detail.target` is the authoritative reveal/detail target; remembered selected
skill/work IDs are not fallback instructions to overwrite it. Relation/support
targets keep their condition/source and mode even after a prior skill selection.
For relation reveal use its source endpoint, retaining a compatible currently
selected endpoint if present; for support reveal use its provider. No skill is
invented. Work/skill targets reveal their actual owner. Closed detail uses an
existing selected skill for highlight/reveal without opening it. A
work-only selection retains selectedWorkId and shared work detail; Classification
reveals the category or categories intersecting that work topic's skills, while
Relations reveals that topic. No skill is invented. A category disclosure alone
updates only classification viewState.

Renderer contract: `mount(container,{snapshot,onSelectSkill,onSelectWork,onSelectRelation,onSelectSupport,
onViewStateChange}) -> {render(snapshot),reveal({kind:skill|work|relation|support,id}),capture(),dispose()}`.
Only the host owns shared detail/copy/lookup listeners. On switch, capture outgoing
local scroll/pan/disclosure, hide/inert that renderer, activate destination, restore
its layout and reveal selected owner/asset (overriding only incompatible collapse
or off-screen position). For user-activated switches, focus the switch control. For history-driven view
changes while lookup is modal, keep its query/open state and focus trap; close
lookup returns to the visible shared lookup trigger. Closing details later
resolves the active view's visible skill/disclosure or falls back to that switch.
Use a render-generation guard for rapid switch/resize/deferred reveal callbacks;
it must not change request-generation tokens. On viewport changes clamp saved
positions to real bounds rather than hide the selected asset. Hidden renderers
have no tab stops or duplicate DOM IDs; IDs are view-prefixed, canonical skill ID
remains the model key. Classification can remember several expanded cards;
Relations keeps its zero/one topic rule. Explicit active-card/topic collapse atomically clears its selected skill/target
and closes detail if owned by the collapsed branch, invalidates the old request
token through the declared close action and focuses disclosure; it does not change
inactive layouts. Mere view hiding never invokes that collapse action.
The host registers neither graph listeners
nor copy actions twice after repeated switching.

## Database design

No database change, visitor account, project storage or business-data migration.
Selected/detail/request/local-layout state is in memory. The initial URL may select
a view; no new localStorage preference for view, skill or request is introduced.
Existing theme/language preferences remain unchanged.

## Interface contracts

No public API or service interface is added. Native anonymous GET/fragment routes
and the private model/renderer contracts above are affected.

| Destination | English | Chinese | Compatibility |
| --- | --- | --- | --- |
| Home | `/?lang=en` | `/zh.html?lang=zh` | Existing aliases `/index.html` remain valid |
| Capability overview | `/?lang=en#capabilities` | `/zh.html?lang=zh#capabilities` | One same-page host, default Classification |
| Explicit relationship view | `/?lang=en&view=relations#capabilities` | `/zh.html?lang=zh&view=relations#capabilities` | Local representation, not another webpage |
| Asset directory | `/?lang=en#asset-directory` | `/zh.html?lang=zh#asset-directory` | Compact complete index; original type anchors remain targets |
| Get started | `/?lang=en#start` | `/zh.html?lang=zh#start` | Installation contract unchanged |
| Legacy explorer | `/explore/`, `/explore/index.html` | `/explore/zh.html` | Thin native fallback/compatibility redirect to same-language capability host requesting Relations; no independent renderer |

`site-navigation.json` owns these routes and the active-section map. All native
headers, CTA, alternate/canonical metadata and sitemap are reconciled in T24.
`getSiteDestination`, `getActiveDestination` and `getAlternateDestination` retain
names but adapt to same-page routes. Overview is current at `#capabilities` or its
six category anchors, directory at `#asset-directory`/type anchors, start at
`#start`, otherwise Home. `#skills` now targets the compact skill index;
`#map-*` work bookmarks open the corresponding classification card (explicit view
takes precedence as Relations overview with a category-context hint, no fabricated selection, and a native fallback).
`#specs`, `#rules`, `#protocols` and their existing subcategory IDs remain valid
index targets. Unrecognized fragments preserve the document and use a visible
section fallback; they never select a different skill silently.

Initial `view` accepts `classification|relations`; absent/unknown value uses
Classification, with an accessible notice for an invalid supplied value. Same-document global/header/directory links intercept only validated same-origin
homepage-family paths and supported section/view destinations; update fragment
and active state without replacing the host, textarea or request controller.
Unmodified native hrefs remain for no-JS/cold entry. Do not intercept external,
modified/new-tab or language-edition links. Category anchors without explicit view
select Classification and open that card; explicit supported view wins.
Switching
uses `history.replaceState` to update only the view query, preserving lang,
other query data and destination fragment, without navigation/scroll reset.
`popstate`/`hashchange` or direct URL restoration uses the same validated navigation/view transition, not a second
state store. Language links preserve supported view and recognized section/category
fragment in the other edition; skill/request/layout persistence across reloads or
languages is not promised. Legacy route handling is same-origin only and preserves
appropriate campaign/lang data while forcing the capability target; no open redirect.
A script-free legacy stub has a visible direct link to the homepage host.

Accepted manifest remains `website/.openai/runtime-manifest.json`, outside its own
runtime allowlist. Contract: `{runtimeRevision:string,assetsRevision:string,
files:[{path:string,sha256:string}],checks:Record<criterionId,{result:pass|fail|
unverified,evidence:string[]}>,ownerConclusion:null|{reviewer:string,at:string,
result:accepted|changes-requested,revision:string,criteria:{coverage:string,
relationships:string,purposeAndUse:string,siteStructure:string,supportScope:string,
localizedNames:string,switchContinuity:string}}}`. Sorted website-root-relative
paths/hashes identify the complete accepted runtime, including both renderers and
native compatibility stubs, excluding tests/audits/hosting records. Use a full
canonical asset commit SHA separately from the deployment checkout identity;
`runtimeRevision` may be the allowlist digest for uncommitted local work.
All changed transitive imports/data use a coherent updated cache key. A working
null-owner manifest is never accepted; T12 acceptance includes A1-A11/A13-A17 and
all actual owner fields for the same bytes. T13 compares every accepted hash,
verifies public canonical source availability, captures current known-good payload
and recovery capability, and checks serving identity before mutation/retry/restore.
An intervening unrelated release blocks conflicting switching/recovery. Record
unchanged, verified recovered or unresolved delivery distinctly; failed candidates
never become complete merely because upload or rollback succeeded.

Static HTML/ESM/JSON remain within `website/`, with normal static 404 and correct
MIME verification. Canonical sources use existing pinned `sourceUrl` logic, not
repository-root runtime dependencies. Clipboard remains the sole optional manual
write boundary and is never executed by view switching.

## Data flow and error handling

Source records → audited classification/call/order projections → shared state →
one active renderer → shared explanation. Search/peer/index references resolve a
canonical ID before revealing its active-view owner. No renderer invents guidance.

| Failure / boundary | Detection | Recovery / outcome |
| --- | --- | --- |
| Missing/duplicate skill or unsupported edge/call mode/quote | Model/source fixture rejects offending ID | Reconcile before complete-coverage claim |
| Invalid view query | Enum parse at host boundary | Classification with honest notice; no missing page |
| Render or module failure | Entry/renderer initialization fails | Native classification/directory/source route remains readable; no loaded/success claim |
| Rapid switch/resize reveal finishes late | Render-generation mismatch | Ignore stale layout operation; preserve current selection/request identity |
| Edited/different-work/closed copy resolves late | Existing request token guard | No stale success; selectable/manual text on rejected/absent clipboard |
| Call projection would recurse | Cycle detection identifies back edge | Keep finite call reference with true source semantics, not fabricated feedback |
| Scenario sequence is contradictory | Per-scenario before-graph cycle/source check | Reject invalid order before acceptance; do not confuse genuine feedback with impossible sequence |
| Saved position no longer fits viewport | Bounds/reveal check after activation | Clamp and reveal selected asset/owner, leave switch/close reachable |
| Legacy route script unavailable | Native fallback markup | Same-language homepage capability link remains usable |

## Technology choices and trade-offs

| Approach | Benefit | Cost / decision |
| --- | --- | --- |
| Shared pure state and two native renderers in homepage | Reuses original cards/current graph, no navigation loss or package migration | Explicit adapters and state/DOM lifecycle tests required; selected |
| Separate pages/applications per representation | Each renderer could keep its old composition | Duplicates detail/request state and navigational context; violates same-page decision; rejected |
| New graph/UI framework | Could automate layout and lifecycle | Dependency/stack migration without solving source semantics; rejected |

The old homepage card and graph implementations are local baselines. No external
runtime dependency, external reference-site implementation, new host or enduring
platform boundary is introduced; no new ADR is required for this bounded revision.
Risks are fabricated hierarchy/order, duplicate content owners, mixed cached
modules, stale async view restoration and hidden/unreachable focused nodes.
Source/partition guards, shared state ownership and assembly tests address them.

## Test strategy

| Layer | Method and observable outcome | Role |
| --- | --- | --- |
| Source / semantics | Audit each shown parent and partial-order edge against definition/condition; intent-derived fixtures reject method/input-as-child, unsupported rank, cyclic recursion, missing/duplicate/foreign IDs and unsourced order | Maintainer, T20 |
| Pure state | Red/green snapshots for both switch directions, selected/none/relation-only/closed modes, independent disclosures, edited and pending copy identity, rapid switches and invalid view | Maintainer, T21 |
| Classification | Exact six-group/current-registry migration, one primary skill per view, real call indentation and reference cases, native mirrors and compact index completeness | UI/content maintainer, T22 |
| Relationship adapter | Reuse real graph/router, equivalent edge/detail meanings, support scope and canonical ID reveal without duplicate listener/detail roots | UI maintainer, T23 |
| Navigation / assembly | Same homepage sections, explicit view URL, old explorer fallback, valid type/category/install aliases, language/view mapping, history/denied storage, no-JS/blocked module, complete root closure | Website maintainer, T24 |
| Full functional and visual | Both locales, five A8 widths and both themes; all skills in both views, no overflow/occlusion, switch/search/peer/close and focus; same-view-local scroll/pan return, long labels, relation/support detail after skill selection, modal history focus, collapse-then-switch, same-page section navigation without controller recreation, copy absent/rejected/late results, new/old caches and resize | Maintainer, T25 |
| Engineering / alignment | Actual diff including untracked modules; rule coverage and acceptance-to-code/evidence; human conclusion separate | Maintainer, T25 then T9/T12 |
| Public delivery | Exact accepted runtime allowlist and source revision, canonical targets already public, actual serving identity, all-file TLS/MIME/hash and full FD dual-view smoke/recovery outcomes | Release maintainer, T13 only after separate authorization |

No revised runtime/browser results are produced by this document-only change.
Historical 70-skill/graph matrices establish only their own old scheme. Native
devices, zoom and spoken-screen-reader behavior remain unverified unless actually
exercised. No declared performance, session-duration or coverage budget is invented.

## Quality attribute design

Profiles: quality-attribute, interface-change, shared-value. No persisted-data
migration profile, new service, telemetry contract or project config is introduced.
Active canonical references: architecture-quality 1.4.0, testing-quality 1.4.0,
error-surfacing-quality 1.2.0. Other applicable code concerns are reviewed at T25.

| Source | Rule refs | Tactic | Trade-off | Verification | Owner |
| --- | --- | --- | --- | --- | --- |
| A3/A16 / F3/F15 | ARC-001, TST-001, TST-006 | One relation owner; call-only finite forest and source-conditioned partial order | Curated semantic audit remains necessary | Counterexample and quote/endpoint fixtures, shared-child/cycle review | Relationship model |
| QAS-02 / F5/F14 | ARC-001, TST-001, TST-006 | Shared identity/locales plus exact category/topic partitions | Native mirror reconciliation cost | Registry/name/source/locale and compact-index tests | Data/content owner |
| QAS-04 / F4/F16 | ARC-001, ARC-003, TST-001, TST-003 | One state/detail/request owner, view-local layout, separate render/request generations | Explicit renderer lifecycle logic | Both-direction state/async-copy/focus/resize and module-DAG tests | Explorer host |
| QAS-01 / F7 | TST-001, TST-003 | Native switch buttons and hidden inert renderer; bounded lists/detail | Local scroll/pan | Full pointer/keyboard/geometry/contrast matrix and captures | UI maintainer |
| QAS-03 / F6 | ERR-004, TST-002, TST-003 | Preserve existing request token and manual copy fallback | No automatic operation | Absent/rejected/late/edited/closed copy checks during switching | Shared details |
| QAS-05 / F10/F12 | ARC-001, ARC-005, TST-001, TST-002, TST-003 | Same-page route contract, native aliases, versioned complete closure | Compatibility stubs retained as public URL adapters | Exact old/new routes, no-JS, cold/cached assembly and manifest fixtures | Website maintainer |
| QAS-06 / F11 | ARC-005, ERR-004, TST-001, TST-002, TST-003 | Accepted hash gate, actual known-good baseline, serving check and branch-specific recovery | Provider/source access may block release | Public smoke and recorded unchanged/recovered/unresolved outcome | Release maintainer |

## Acceptance criteria

- **TD1**: Shared context contribution/input/result match definitions in both views. Covers F1/F2.
- **TD2**: Current registry, unique per-view ownership, names/guidance and sources agree. Covers F2/F5/F14.
- **TD3**: All typed relations and finite feedback retain the same source-backed semantics. Covers F3/F15.
- **TD4**: Disclosure, active-view lookup/reveal and close/focus retain context. Covers F4/F5/F7.
- **TD5**: Shared four-field guidance and request identity/manual recovery are truthful across switching. Covers F6/F16.
- **TD6**: Both views and switch meet A8 operations/contrast/fallback with recorded outcomes. Covers F7/F8.
- **TD7**: Source/cache/runtime/evidence identities distinguish current verification from history/external execution. Covers F8.
- **TD8**: Actual owner three-criterion review identifies both views and the candidate. Covers F9.
- **TD9**: Website-root bilingual assembly, shared preferences, complete directory and adoption contracts pass with actual owner conclusion. Covers F10.
- **TD10**: Accepted candidate/public-source/serving/hash gates and distinct release/recovery outcomes are recorded; failed candidate is incomplete. Covers F11.
- **TD11**: Homepage sections, view URLs, old explorer/type/category/install links and native fallbacks satisfy F12. Covers F12.
- **TD12**: Shared per-target source-backed support scope remains discoverable in both views. Covers F13.
- **TD13**: Locale-owned name/ID/purpose remain consistent across both renderers, lookup and details. Covers F14.
- **TD14**: Shared host and adapters preserve every F16 state through both-way/repeated/rapid switching, async copy, focus and responsive restoration. Covers F4/F16.
- **TD15**: Call-only hierarchy and conditional partial-order projections pass all F15 source/counterexample/multiple-parent/cycle fixtures. Covers F3/F15.
- **TD16**: Complete changed assembly has passing semantics/unit/integration/browser and engineering/alignment evidence for both views, fresh hashes and explicit actual-owner limits. Covers F7-F12/F15/F16.

## Downstream reconciliation

T1-T8/T10/T11/T14-T19 retain their old local completion evidence; none proves this
new scheme. The approved T20-T25 revision is implemented and locally verified as recorded in the current audit and task evidence. T9/T12 review that identified candidate; T13 still requires separate authorization after acceptance. Existing hosting receipts and publication workflows remain unchanged.
