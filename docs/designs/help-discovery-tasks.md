---
artifact_type: tasks
lifecycle: living
created_at: 2026-10-27
parent: ./2026-10-27-help-discovery-technical-design.md
status: active
---

# Tasks: reconcile, integrate and publish AI Cortex discovery

Current outcome (2026-10-28): the owner accepted T12, explicitly approved the
clean-URL compatibility repair and authorized T13. Sites version 8 is published
and public verification passes. T1-T25 are Done. Only the isolated Sites source
repository was committed/pushed; this AI Cortex repository remains uncommitted.
The final runtime, owner conclusion and provider/public receipts are linked below.

Authority: [technical design](2026-10-27-help-discovery-technical-design.md),
[functional design](2026-10-27-help-discovery-functional-design.md),
[AIC-REQ-04](../requirements-planning/AIC-REQ-04.md).

This is a living progress record. The table states current completion; original
local evidence remains historical for its identified bytes. Actual owner acceptance
and release are recorded in the [publication evidence](../../tests/website/evidence/release/README.md).
Fibonacci estimates are bounded deliverables, not dates.

| Id | Task | Points | Depends on | Acceptance / design trace | Owner / Hint | Status | Observed local baseline |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T1 | Reconcile registry, skill ownership and guidance sources | 2 | — | TD2: exact current IDs, one primary node each, defining-source quotes/hashes and invalid fixtures pass | Maintainer: inspect `catalog.json`, `workflow.mjs`, `panel-model.mjs`, `skill-guidance.json` and model tests | Done | 70 canonical skill IDs, unique owners and pinned definition hashes pass; [integrated evidence](../../tests/website/evidence/README.md). |
| T2 | Verify direct topic and concrete skill relationship meanings | 3 | T1 | TD3: 13 topic connections, two local loops and 53 skill edges retain their endpoint/type/condition/source distinctions and text alternative | Maintainer: semantic source audit of `topic-edges.json`, `skill-edges.json`, `global-topic-graph.mjs`, `topic-map.mjs` | Done | 13 topic edges, two loops and 53 concrete skill edges pass source/model checks; human clarity remains T9/T12. |
| T3 | Verify skills expand inside their owning topic | 3 | T2 | TD4: zero/one local branch, no lower dock, compact peers, reflow, internal scroll/clipping and correct peer/search reveal; heading and full selected label remain visible | UI maintainer: `story.mjs`, `workspace.css`, `topic-map.mjs`; local-branch browser harness | Done | Original 100-case matrix and integrated 200 topic/size/theme selections pass, with owned local expansion and geometry checks. |
| T4 | Verify Chinese use guidance and ordinary-agent boundaries | 2 | T1 | TD1/TD5: actual panel shows applicability, needed context, usage and result; internal assessment routes through public entry; sources remain optional | Content maintainer: guidance, context and panel records plus all-skill browser paths | Done | All 70 skills have source-grounded four-field guidance; 140 English/Chinese panel paths pass. |
| T5 | Verify retained controls, appearance and focus recovery | 3 | T3, T4 | TD4/TD6: selection, relation tabs, work explanation, examples, lookup/reset, keyboard, close/focus and local viewport alignment work at all A8 widths/themes | UI maintainer: run current local browser harness; compare captures and record environment limits | Done | Original and integrated controls pass. A red/green short-screen work-panel repair keeps the body and selected asset visible; native devices and spoken screen readers remain unverified. |
| T6 | Verify edited requests and clipboard failure identity | 2 | T5 | TD5: same-work edits persist; absent/rejected copy offers manual recovery; late edit/close results never claim current success | UI maintainer: `request-state.mjs`, `story.mjs`; targeted clipboard checks | Done | Original targeted recovery and integrated eight clipboard failure/stale-result cases pass. |
| T7 | Correct light-theme loop-label contrast | 1 | — | TD6/F7/A8/QAS-01: both loop labels meet at least 4.5:1 in light/dark overview and selection states without changing relationship meaning | UI maintainer: scoped prototype style correction, intent-derived failing contrast check, repeat measurements | Done | [Green browser evidence](../../experiments/direction-planning/audit/t7-t8-browser.json): both loop labels exceed 11:1 in both themes; red failure retained |
| T8 | Add a visible source route for entry-module failure | 2 | — | TD6/F8/A10: with JavaScript enabled and the entry module blocked, a visible canonical catalogue link remains; no false loaded/complete claim | UI maintainer: scoped static fallback, blocked-module regression and no-JS comparison | Done | [Green browser evidence](../../experiments/direction-planning/audit/t7-t8-browser.json): static source link remains visible for blocked entry and no-JS; keyboard navigation returns HTTP 200 |
| T9 | Record owner review of both capability views | 2 | T25 | TD8: actual owner concludes coverage, accurate order/hierarchy/relationships and findable purpose/use across both views of one identified candidate; no quiz/copy/execution | Owner: one dual-view walkthrough may also supply the distinct T12 conclusions | Done | Actual owner T12 acceptance on 2026-10-28 covers the integrated content criteria; unchanged content is retained in the release acceptance snapshot. |
| T10 | Reconcile local baseline evidence and document approval state | 1 | T1, T2, T3, T4, T5, T6, T7, T8 | TD7: final requirement/design/task/evidence links, unresolved findings and actual approvals agree; status changes only follow supplied approval/acceptance | Maintainer: current calibration review and document indexes; no publication action | Done | Parent approvals recorded from the owner instruction; current source/evidence/task states reconciled in the [integration audit](../calibration/audit-docs.md#aic-req-04-approved-local-website-integration-2026-10-27). T9 owner acceptance is now recorded in the publication evidence. |
| T11 | Migrate the accepted explorer runtime into the website root | 5 | T10 | TD9/F10/A11/QAS-05: runtime dependency closure under `website/explore/` loads from an isolated website root; existing map semantics, owned branches and static recovery retained; source revision resolver and candidate manifest checks reject invalid paths/drift | Website maintainer: migrate Chinese-only runtime/models/data port with source metadata; final locale extraction follows in T14; root-isolated assembly tests and source/manifest fixtures | Done | Website-root runtime closure, safe pinned sources, local source hashes and 36-file working manifest verified. No dependency on experiments at runtime. |
| T12 | Verify and accept the integrated website revision | 5 | T25, T9 | TD9/TD11/TD14-TD16/A1-A11/A13-A17: final same-page bilingual candidate passes model, full two-view A8, switching/copy/recovery/navigation/cache/source checks and engineering/alignment gates; actual owner site/support/naming/switch continuity and T9 results recorded in accepted manifest | Maintainer verifies in the isolated website root; owner records integrated coverage/meaning/use and scheme retention for the same revision | Done | Actual owner accepted the integrated candidate and separately approved the address compatibility repair; accepted manifest, 46 Node/18 Python checks and targeted/public browser evidence identify the released bytes. |
| T13 | Publish the accepted website and verify public delivery | 3 | T12 | TD10/F11/A12-A17/QAS-06: release authorization, accepted runtime hashes, public canonical sources, actual serving/known-good version and usable recovery path verified before switching; all runtime TLS/MIME/hash checks and FD public smoke operations pass; pre-switch/unknown/post-switch failures follow distinct outcomes; failed candidate never Done | Release maintainer: existing Sites checkout/host; preserve known-good receipts, record deployment/public evidence and reconcile actual task/requirement status only after acceptance | Done | Sites version 8 deployed successfully; 47 public resources pass HTTPS/MIME/source checks, eight bilingual/size/theme browser cases and both fallback locales pass. Domain/audience preserved; version 7 retained for recovery. [Release evidence](../../tests/website/evidence/release/README.md). |
| T14 | Prepare reviewed English and Chinese explorer copy | 8 | T11 | TD9/F10/A11: planned locale dictionaries own all UI/use/condition/context/example/feedback text; both languages have exact current ID/key parity, nonempty four-field guidance and source-grounded equivalent meaning; no silent language fallback or duplicate editable copy | Content/UI maintainer: locale dictionaries/adapter and model/composition consumers; remove transitional Chinese display copies; review both editions against defining scopes | Done | Both locale dictionaries reviewed; 70-skill guidance, exact key/type/placeholder/identity parity and static mirrors pass. Display copy has one owner. |
| T15 | Connect explorer navigation, language, theme and metadata | 3 | T14 | TD9/F10/A11: both homepage headers/capability entries reach the corresponding explorer; home/alternate routes, metadata/sitemap, theme and language precedence work without regressing existing atlas/installation; changed transitive resources use coherent cache identity | Website maintainer: `website/index.html`, `zh.html`, `language.mjs`, `explore/site-contract.mjs`, explorer HTML and `sitemap.xml`; old callers and explorer-route tests pass | Done | Both native homepages link matching explorer locales; home/alternate routes, language precedence, theme, sitemap and cache identity pass. |
| T16 | Unify website destinations and navigation | 5 | T15 | TD11/F12/A13: common Home / Capability overview / Asset directory navigation, Get started action, graph-local controls and separate utilities; preserve route/type/install bookmarks, native fallback, active state and destination-family language behavior in both editions | Website maintainer: both homepage/explorer HTML, planned `website/site-navigation.json`, `website/explore/site-contract.mjs`, `language.mjs`, shared styles and route/browser tests | Done | Done: shared four-destination navigation, directory/install bookmarks, destination-preserving language/history, native fallback and separated utilities pass the 20-case site matrix and static mirrors. [Evidence](../../tests/website/evidence/revision/README.md). |
| T17 | Explain source-backed cross-cutting support in the same map | 3 | T16 | TD12/F13/A14: foundations/communication expose applicable subjects and conditions with folded labels and panel navigation; no exclusive-edge interpretation, speculative all-to-all calls or hidden direct relations | Graph/content maintainer: audit canonical sources; `website/explore/support-scopes.json`, locale/model/renderer/routing checks | Done | Done: two visible support labels and per-target source/condition records audited at the pinned revision; same-map subject navigation and geometry pass. [Evidence](../../tests/website/evidence/revision/README.md). |
| T18 | Add reviewed localized skill names distinct from IDs and purposes | 5 | T16 | TD13/F14/A15: exact current registry names in both locales, Chinese name plus unchanged ID plus separate purpose in nodes/panels; search all three; canonical invocation preserved and full labels readable at A8 sizes/themes | Content/UI maintainer: `website/explore/locales/`, guidance/search adapters, `story.mjs`, node styles and model/browser tests | Done | Done: all 70 reviewed Chinese names plus canonical IDs/purposes are visible and searchable; 140 bilingual skill paths and true-identity/translation negatives pass. [Evidence](../../tests/website/evidence/revision/README.md). |
| T19 | Verify the revised site assembly and reconcile evidence | 3 | T17, T18 | TD11-TD13/F12-F14/A13-A15: source/content review, site guide/locale ownership and metadata consistency, red/green fixtures, old suite and full bilingual A8 regressions pass; engineering/alignment review, cache and working manifest updated for actual bytes; record any limits without inferring owner acceptance | Maintainer: `tests/website/`, working runtime manifest, audit/task records; prepare exact candidate for T9/T12 owner review; update `website/README.md` maintenance guidance only when implementation is authorized | Done | Done: 38 Node and 18 Python tests, full bilingual map/control/recovery/site matrices, source hashes, import DAG, engineering/alignment review and 40-file working manifest verified. Owner acceptance is now recorded for the published candidate. [Evidence](../../tests/website/evidence/revision/README.md). |
| T20 | Audit classification ownership, skill hierarchy and partial order | 3 | T19 | TD2/TD3/TD15: exact original six-card/current-registry partition; every required/conditional parent has its applicable parent/scenario and defining evidence; scenario order is contradiction-free; unspecified order is not presumed parallel; both category and work-topic projections resolve valid ownership; input/method/recommendation are not children; shared callers/cycles have finite references | Content/model maintainer: `website/explore/classification.json`, `relationship-model.mjs`; existing skill-edge/locale/source records and negative fixtures | Done | Exact six-category/70-skill partition audited; all 59 relationship quotes verified at the pinned asset revision, including 36 scoped calls and six scenario-order edges. [Evidence](../../tests/website/evidence/dual/README.md). |
| T21 | Extract the shared explorer host and view-state owner | 5 | T20 | TD4/TD5/TD14: single selection/detail/lookup/request owner with explicit active detail target, separate view-local state and render generations; both switch directions retain exact selected work/skill/relation, mode, edited text and pending-copy identity; active-target reveal, modal-history focus, target/mode normalization and collapse-versus-switch contracts pass red/green tests | UI maintainer: `explorer-state.mjs`, `explorer-host.mjs`; former `story.mjs` composition, retained request controller and detail composition | Done | Shared host/state delivered; red/green state fixtures and pending-copy, active-target, modal-history focus and manual-collapse browser checks pass. [Evidence](../../tests/website/evidence/dual/README.md). |
| T22 | Render classification cards with evidenced skill order and children | 5 | T21 | TD2/TD13/TD15: original six-card presentation uses shared names/IDs/purposes; one primary skill per view, call-only required/conditional indentation, partial sequences and peer/reference/cycle distinctions; native fallback and current-view lookup/reveal work | UI maintainer: `classification-view.mjs`, category/relationship models, locale/native mirrors and card styles | Done | Original six cards hydrate the shared call-only hierarchy and typed references; all 70 localized usage paths pass in both editions. [Evidence](../../tests/website/evidence/dual/README.md). |
| T23 | Adapt the relationship renderer to the shared host | 3 | T21 | TD3/TD4/TD12/TD14/TD15: existing graph/router/support runs as one adapter using the shared audited call/partial-order model, shares every relation condition and detail; zero/one topic, local pan/list and visible selected owner retained; no duplicate detail/copy listeners or inactive tab stops | UI maintainer: `relationship-view.mjs`; current graph/skill/router/support modules, host adapter and layout checks | Done | Existing topic graph runs inside its adapter; 13 topic edges/two loops retained. Both locales pass all-skill and full A8 route/label/focus regressions. [Evidence](../../tests/website/evidence/dual/README.md). |
| T24 | Assemble same-page navigation and compact complete directory | 5 | T22, T23 | TD9/TD11: both homepages host one dual-view capability area plus compact four-type index; no-reload section links preserving the live shared controller, explicit view URL/category precedence, language mapping, valid old type/category/install and legacy explorer routes work; no second interactive page; native fallback, metadata and cache closure reconciled | Website maintainer: homepage HTML/main/styles, shared navigation records/modules, existing explorer HTML compatibility stubs, sitemap and native mirror tests | Done | Both homepages now host one capability section and compact four-type directory; old explorer entries are compatibility stubs. Native fallback, route/cache/locale/static and no-reload navigation checks pass. [Evidence](../../tests/website/evidence/dual/README.md). |
| T25 | Verify the final dual-view candidate and reconcile records | 5 | T24 | TD6/TD7/TD14-TD16: source/registry/locale/semantic negatives, full bilingual two-view A8 and every-skill paths, both-way rapid switching, active relation/support after skill selection, modal-history focus, explicit collapse and no-reload section navigation, state/copy/scroll/pan, complete-directory/legacy/cache/fallback checks and engineering/alignment gates pass; refresh working hashes, guide and audit without owner-pass inference | Maintainer: `tests/website/`, `website/.openai/runtime-manifest.json`, site maintenance guide and canonical audit/tasks; prepare exact bytes for T9/T12 | Done | 44 Node and 18 Python tests, 20 dual-view cases/280 skill paths, 20 graph geometry cases/140 graph paths, 20 controls cases and recovery/contrast checks pass. Engineering/alignment review has no unresolved local finding; actual T9/T12 acceptance is recorded in the publication evidence. [Evidence](../../tests/website/evidence/dual/README.md). |

## Execution gates and stage evidence

Dependencies describe delivery order, not authorization. The owner has now supplied actual approval and the explicit implementation
instruction for T20-T25. Earlier T16-T19 approval alone would not authorize them.

Order: T20 → T21 → (T22 and T23) → T24 → T25 → T9 → T12 → T13.
T20 audits the concrete source projection; it does not manufacture a mandatory
workflow. T21 owns shared state; the two renderer tasks use its contracts. T24
assembles one homepage capability section and compact full lookup, including
legacy routes. T25 verifies identified bytes, not human comprehension.

T9/T12 may use one actual owner walkthrough but record distinct required criteria:
coverage, relationship/order/hierarchy accuracy, findable use, site structure,
support scope, localized naming and view-switch continuity. T12 accepted manifest
requires exact runtime hashes, canonical asset revision, locale/content identity,
A1-A11/A13-A17 evidence and actual owner conclusion. Working null-owner manifests
cannot authorize release. Changed bytes reopen affected checks and owner review.

T13 requires accepted T12 and separate publication authorization, actual known-good
serving/recovery identity, canonical sources already public and full dual-view
public smoke. Pre-switch failures leave old delivery unchanged; uncertain outcomes
are investigated before another mutation; failed switched candidates require
verified non-conflicting recovery and remain incomplete. Missing release access
blocks T13, not local planning. No DNS/host/audience or repository-publication
change is included.

## Engineering governance

These annotations retain baseline obligations and add planned revision checks.
Done states follow recorded evidence. No waiver is claimed. Model rules are cited,
not restated.

| Task | Affected scope | Rule refs | Verification | Waiver |
| --- | --- | --- | --- | --- |
| T1 | `experiments/direction-planning/catalog.json`, `workflow.mjs`, `panel-model.mjs`, `skill-guidance.json` | ARC-001, TST-001, TST-006 | Source-owner inspection, canonical-set/invalid-fixture tests and isolated snapshots in `node --test experiments/direction-planning/*.test.mjs` | — |
| T2 | `topic-edges.json`, `skill-edges.json`, `global-topic-graph.mjs`, `skill-graph.mjs` under the experiment | ARC-001, TST-001 | Source semantic audit plus exact quotes/endpoints, graph/forest/neighborhood tests | — |
| T3 | Experiment `story.mjs`, `workspace.css`, `topic-map.mjs` and local SVGs | ARC-001, TST-003 | `audit/verify-local-branch.cjs`: actual ownership, local viewport, geometry and internal-scroll behavior | — |
| T4 | Experiment `skill-guidance.json`, `context-copy.mjs`, `panel-model.mjs`, `skill-guidance.mjs` | TST-001, TST-003 | Definition audit and all 70 actual panel paths; omit a required usage field and the model/browser assertions fail | — |
| T5 | Experiment `index.html`, `story.mjs`, `workspace.css` and shared appearance consumer | TST-003 | Recorded Chromium five-size/two-theme controls, focus, sheet, name bounds and visual captures | — |
| T6 | Experiment `request-state.mjs`, `story.mjs`, native clipboard boundary | ERR-004, TST-002, TST-003 | Promise-preserving absent/rejected/late-edit/late-close browser checks and token tests, with actionable manual recovery inspected | — |
| T7 | Experiment `workspace.css` loop text and its contrast verifier | TST-001, TST-003 | Retained red computed-color report reproduces failure; green regression measures both themes/states against 4.5:1 | — |
| T8 | Experiment `index.html` static source fallback and blocked-entry verifier | ERR-004, TST-002, TST-003 | Abort `story.mjs` with JavaScript enabled; visible catalogue recovery must pass, alongside no-JS fallback | — |
| T11 | `website/explore/` runtime/data, `source-links.mjs`, `source-manifest.json`, `skill-metadata.json`; `website/.openai/runtime-manifest.json`; migrated model/source tests in `tests/website/` | ARC-001, ARC-003, TST-001, TST-002, TST-003, ERR-004 | Red/green source-path/manifest fixtures and actual root-isolated model/composition tests; inspect import DAG and single ownership; no-JS/blocked-entry recovery and missing-file failure | — |
| T14 | `website/explore/locales/en.json`, `locales/zh.json`, `locale.mjs`, migrated model/composition consumers, mirrored explorer static copy and `tests/website/` locale checks | ARC-001, TST-001, TST-002, TST-006 | Exact key/current-ID parity and nonempty-field negative fixtures; full per-skill semantic review; isolated language storage and deterministic locale tests; static mirrors reconciled to dictionaries | — |
| T15 | `website/index.html`, `zh.html`, `language.mjs`, `sitemap.xml`; `website/explore/index.html`, `zh.html`, `site-contract.mjs` and route/theme tests | ARC-001, ARC-005, TST-001, TST-002, TST-003 | Existing website Node/Python suites plus red/green route-map, language precedence, storage-denial and cached-leaf fixtures; preserve old routes/anchors/atlas; real home-to-explorer assembly and theme inspection | — |
| T12 | Website-root runtime and `tests/website/`; `website/.openai/runtime-manifest.json`; `docs/calibration/audit-docs.md` integrated evidence | ARC-001, ARC-003, ARC-005, TST-001, TST-002, TST-003, TST-006 | Full TD acceptance strategy, real owner acceptance, exact accepted/deployed hashes, clean-route negatives and actual public smoke; engineering/alignment evidence remains scoped separately | — |
| T13 | Separate Sites checkout `dist/`; `website/.openai/deployment.json`, `public-verification.json`, `runtime-manifest.json`; `website/README.md`, canonical audit/tasks and AIC-REQ-04 status evidence | ARC-001, TST-001, TST-002, TST-003, ERR-004 | Compare accepted/deployed manifests, pinned source reachability, actual provider/recovery baseline and branch-specific outcomes; execute every FD public smoke operation and all-file TLS/MIME/byte checks; record failure/location/next action and verified unchanged/recovered delivery | — |
| T16 | `website/site-navigation.json`, `site-navigation.mjs`; existing `website/index.html`, `zh.html`, `language.mjs`, `styles.css`, `explore/site-contract.mjs`, `explore/index.html`, `explore/zh.html` and local header styles | ARC-001, ARC-005, TST-001, TST-002, TST-003 | Intent-derived red/green destination/active-state and native-mirror tests; exact old directory/type/install inputs, back/forward and hash active-state tests; direct/return/alternate/no-JS/type-anchor paths and mobile keyboard/visual checks in both languages | — |
| T17 | `website/explore/support-scopes.json`, `support-scopes.mjs`; existing `explore/locales/`, `story.mjs`, `workspace.css` and topic selection contracts | ARC-001, TST-001, TST-003, TST-006 | Source quote/target audit, invalid/missing fixtures, folded visibility and non-occluding geometry in all A8 combinations | — |
| T18 | `website/explore/locales/en.json`, `locales/zh.json`, `locale.mjs`, `skill-guidance.mjs`, `panel-model.mjs`, `story-model.mjs`, `story.mjs`, `workspace.css` | ARC-001, TST-001, TST-002, TST-003 | Per-skill name/purpose semantic review, registry/key/required-field negatives, name/ID/purpose search, accept translated names while rejecting true identity drift, full-node bounds and canonical example IDs | — |
| T19 | `website/` revised runtime closure, `explore/source-manifest.json`, `.openai/runtime-manifest.json`, `tests/website/` and canonical audit/task records | ARC-001, ARC-003, ARC-005, TST-001, TST-003, TST-006 | Existing suites plus full bilingual A8 matrix and all-skill paths, native/no-JS recovery, import closure/hash checks, engineering and implementation-alignment gates; no owner pass inferred | — |
| T20 | `website/explore/classification.json`, `relationship-model.mjs`; existing `skill-edges.json`, locales and canonical source fixtures | ARC-001, TST-001, TST-002, TST-006 | Exact partition/source quote/condition audit; call-only hierarchy, required/conditional order, unsourced/missing/duplicate/shared/cyclic-call and contradictory-scenario sequence counterexamples; prove peers do not assert parallel execution | — |
| T21 | `website/explore/explorer-state.mjs`, `explorer-host.mjs`; existing request-state/controller, lookup/detail DOM and `story.mjs` extraction | ARC-001, ARC-003, TST-001, TST-002, TST-003 | Red/green shared-state and renderer-contract tests, pending-copy token and explicit active-target/mode assertions, generation/modal-focus/collapse-versus-switch/DOM listener assembly checks and import DAG | — |
| T22 | `website/explore/classification-view.mjs`; category/relationship projections, locale records, native card markup and relevant styles | ARC-001, TST-001, TST-003, TST-006 | Every-skill tree/peer/reference/source tests, card disclosure and active-view selection, keyboard/native-fallback/geometry checks | — |
| T23 | `website/explore/relationship-view.mjs`; existing graph/skill/router/support modules and shared host composition | ARC-001, ARC-003, TST-001, TST-003 | Actual host-adapter assembly; shared edge/guidance equivalence, finite cycles, no duplicated listeners/IDs and graph route/selection regressions | — |
| T24 | `website/index.html`, `zh.html`, `main.mjs`, `styles.css`, `site-navigation.json`, `site-navigation.mjs`, explorer route stubs and `sitemap.xml` | ARC-001, ARC-005, TST-001, TST-002, TST-003 | New/legacy section/type/category/view URL/precedence and language/history fixtures; prove same-page navigation retains controller/edited text/copy token, exact full index/locale mirrors, no-JS/blocked module, root closure/cache and metadata checks | — |
| T25 | Complete `website/` dual-view closure; `tests/website/`, runtime/source manifests, site guide, canonical audit/tasks | ARC-001, ARC-003, ARC-005, ERR-004, TST-001, TST-002, TST-003, TST-006 | Full TD strategy, every-skill/both-view A8 matrix, manual visual and keyboard checks, source-bound reports, engineer/alignment review and no-human-pass status audit | — |

## Coverage and dependency closure

T1-T8/T10/T11/T14-T19 remain completed historical work for their own scheme/bytes.
T20 covers dual-view source/order/parent semantics (TD2/TD3/TD15); T21 state and
shared details (TD4/TD5/TD14); T22 classification and T23 relationships; T24 homepage,
compact index and compatible routes (TD9/TD11); T25 all changed verification and
closure (TD6/TD7/TD16). T9/T12 require the actual revised owner conclusion, and T13
alone changes public delivery under separate authorization. The 25-task DAG is
acyclic. No task is marked complete based on the previous graph-only tests.

The [approved local dual-view audit](../calibration/audit-docs.md#aic-req-04-approved-dual-view-implementation-2026-10-28) records the actual approval,
implementation, verification and remaining owner gate. Earlier planning records
retain their historical scope. No public delivery is authorized by local completion.

## Local readability follow-up, 2026-10-28

The owner invoked `design-taste-frontend` on the local capability page. The scoped
preserve-mode repair improves title/count wrapping, skill caption hierarchy and
control shape consistency; it preserves the approved dual-view interaction and
navigation contracts. T20-T25 remain completed local delivery; refreshed T25
verification and candidate identity are in the
[current visual evidence](../../tests/website/evidence/taste/README.md).
T9/T12 require owner review of these new bytes; no previous machine/owner result
is transferred as acceptance. T13 remains unauthorized.

## Authorized publication preflight and compatibility repair, 2026-10-28

The owner accepted T12 and authorized T13. Preserve that real acceptance separately
from the later repaired bytes: [release record](../../tests/website/evidence/release/README.md).
The provider's observed `/zh.html` to `/zh` normalization exposed an actual
`Unknown site path` error before switching delivery. Only known home/legacy clean
aliases were normalized; unknown paths still reject. Both public URL styles,
section navigation, alternate language/view and selected request continuity pass
46 Node tests, 18 Python checks and eight simulated provider-route browser cases.
The 47-file isolated archive is ready locally; source save/push and deployment
remain unexecuted. This is a pre-switch stop, with verified unchanged version 7,
not a failed switched deployment or an owner rejection of the original candidate.
The existing changed-byte rule requires targeted owner confirmation before the
remaining T13 steps; it does not require repeating unchanged content review.

## Final accepted publication, 2026-10-28

The owner explicitly approved the compatibility repair and continuation of T13.
The actual accepted bytes were committed/pushed only to the isolated Site source,
saved as version 8 and deployed successfully. All 47 runtime files pass public
HTTPS/MIME/source checks (43 non-HTML byte matches, four source-preserved HTML
files with only the provider security-script insertion). Eight actual public
locale/viewport/theme cases and both no-JS/blocked-entry fallback locales pass.
T9/T12/T13 are Done; all associated implementation tasks are Done. Earlier
preflight/readability sections retain their dated historical scope.
[Final release record](../../tests/website/evidence/release/README.md) carries
accepted/runtime/source/provider/archive identity, public proof and retained
known-good version 7. Recovery was not needed or executed.
