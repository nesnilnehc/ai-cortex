# AI Cortex map with contextual details

A local exploratory prototype applying `eli5` and `design-taste-frontend`:
pictures and short labels explain the whole, with tools and instructions revealed
on demand. The Chinese interface is a scoped localization example. Maintenance
records, source identifiers and machine-consumed fields remain English.

Nothing has been published. Production website files, canonical assets, commits
and external systems remain unchanged. AIC-REQ-04 is the sole current requirement document; its endpoint and retained scheme are settled; formal document approval and whole-map acceptance remain pending. Duplicate predecessor documents
were removed at the owner's request. Existing implementation evidence is historical.

## Current retained baseline

Ten topics connect directly through 13 typed relations, with 53 curated concrete
skill edges and 70 registered skills. There is no current-work hub or angle switch.
One topic expands its owned skill list in place; names, Chinese purposes and four
usage fields remain directly available. The graph reflows, with local scrolling
and small-screen graph panning. The retained map scheme is unchanged. The follow-up T7/T8 changes are scoped
to loop text contrast and a script-independent source link.

Current chain: [requirement](../../docs/requirements-planning/AIC-REQ-04.md),
[functional design](../../docs/designs/2026-10-27-help-discovery-functional-design.md),
[technical design](../../docs/designs/2026-10-27-help-discovery-technical-design.md),
[task draft](../../docs/designs/help-discovery-tasks.md),
[consistency review](../../docs/calibration/audit-docs.md#aic-req-04-current-baseline-consistency-review-2026-10-27).

The [T7/T8 report](audit/t7-t8-browser.json) now passes: both loop labels exceed
11:1 in both themes, the static source link is available with a blocked entry or
without JavaScript, and keyboard navigation opens the catalogue. Controller/data
hashes are unchanged. [Repair evidence](audit/t7-t8-evidence.md) records the red and
green checks. T7/T8 are Done locally; formal approval and owner acceptance remain
pending. The sections below retain development history.

## Reading model

There is one main view: the relationship map. Users select a node and read its
explanation, relevant tools and editable/copyable request in the same contextual
panel. The repeated large illustration chapter, page-level scenarios, separate
request section and below-the-map skill inventory have been removed from the entry.

The panel includes only scenarios relevant to its selected node. Trying a scenario shows its contextual narrative without advancing project state
or changing to a second reading surface. It is not evidence that a real workflow
or every historical edge-highlight convention is active. Closing the panel restores focus to the original node.
Direction/goals and backlog/planning are distinct selectable nodes with distinct
explanations, requests and skill subsets.

A header search entry opens a native modal containing all 70 skills in nine groups.
Selecting a result closes search and locates its owning node and selected skill in
the same panel. There is no second skill-detail page within the prototype. Escape
explicitly closes search, including when its search field contains text, without
also closing the existing detail panel. Search closing restores its trigger focus.

## Nonlinear relationship contract

- Direction and goals provide judgment criteria, not a compulsory first stage.
- Backlog/planning, requirements/design, implementation and checking can be revisited.
  Double-headed edges express mutual checking and repair rather than a fixed order.
- Saving, integrating, publishing and announcing are distinct operations. A commit
  does not imply a release, and there is no commit-to-publication connector.
- Publication and announcements expose their own prerequisites in the panel.
- User feedback can return to goals or introduce new work directly to backlog.
- Research, foundations/knowledge and communication are available alongside work.
- Passing a preset checking example grants no operation authorization and performs
  no automatic navigation to commit or release.

`relations.mjs` owns the explanatory connector types and scenario data.
`panel-model.mjs` maps each selectable node to grounded skills, requests, examples
and operation prerequisites. `catalog.json` is the existing prototype snapshot;
source membership and descriptions are checked against `skills/INDEX.md` and
`website/zh.html`. It is not a new authoritative registry.

All 70 registered skills remain represented by actual rendered map nodes or the
anytime-support controls. The five strategy skills belong to the direction node;
the other eleven planning skills belong to the backlog/planning node. Language,
framework and quality specialists are conditional tools, not a compulsory checklist.

## Layout and behavior

- Existing brand: shared orange accent, mark, native type stack and semantic tokens.
  The only raster asset is the previously generated illustration sheet in `assets/`;
  its exact prompt and provenance are retained there.
- Dials: design variance 6, motion intensity 3, visual density 3. No new UI framework,
  external diagram runtime, generated fake screenshot or decorative feature grid.
- Desktop at 1200px and above: stable map plus sticky right-side panel. Map container
  queries preserve connector alignment and readable node labels as the map narrows.
- Narrower viewports: the map retains its nonlinear arrangement, while the contextual
  panel becomes a dismissible bottom sheet. It does not become a new chapter below
  the map. Panel header and copy action remain sticky during its internal scrolling.
- Search uses the browser's native modal top layer, focus behavior and an explicit
  close action. It is separate from task reading, not a second navigation hierarchy.
- Related tools expose a few relevant entries and a complete per-node disclosure.
  Tool source links open defining local SKILL.md files. Copy is the panel's primary
  action; editing the request is optional. Switching nodes restores that node's
  default request, with a notice inside the editor.
- Selection is exposed through pressed state and aria-controls. Panel labels change
  with selection, programmatic focus retains map scroll position, and Escape can
  dismiss the detail panel when no search modal is open.
- Empty search has reset; clipboard denial opens the editor, selects its text and
  explains manual copying. The page does not execute tools or collect credentials.
- Shared system/light/dark appearance covers map, panel and search. Transform-only
  tactile feedback respects reduced motion. No automatic animation is needed.

The old standalone planning case is retained in `detailed.html` as an experiment
reference but is no longer a competing route in the main entry. Earlier screenshots
and reports describe previous revisions, not the current reading model.

## Run

From the repository root:

```sh
python3 -m http.server 8765 --bind 127.0.0.1
node --test experiments/direction-planning/*.test.mjs
```

Open `http://127.0.0.1:8765/experiments/direction-planning/`.
`responsive-check.html` embeds this same entry at 390px. Serve from the repository
root to preserve shared assets and defining-skill links.

## Earlier candidate verification: 2026-10-27

- 30 tests pass. Four panel-model tests were observed failing before the module
  existed. They cover distinct direction/planning scope, every skill resolving to a
  selectable node, relevant-only examples and independent release prerequisites.
  Two additional layout contracts protect the sole map/panel, unique request/copy
  controls and all-70 coverage through nodes actually present in the entry.
- Browser checks verified node selection without leaving the map, local example
  highlighting, copying, all-70 search, returning a searched commit skill to the
  same panel, panel-close focus restoration and independent release conditions.
- Search-field Escape initially consumed the first key as native search clearing;
  its explicit handler was then verified closing the modal while retaining the
  selected panel and returning focus to the search trigger.
- Visually checked the desktop empty/selected panel in both themes, plus the 390px
  map and bottom sheet. The sticky mobile copy action was inspected in the rendered
  panel. Full screen-reader use and real-device checks are not claimed.
- Lighthouse desktop navigation: accessibility, best practices, SEO and agentic
  browsing all 100, with 53 passed and zero failed audits. See
  `audit/lighthouse-workspace-desktop.json`.
- Cold-cache local desktop navigation, unthrottled: LCP 522ms, CLS 0.00. These are
  local lab observations, not field performance; INP was not measured. See
  `audit/workspace-performance-summary.json`.
- `workspace-preview.png` is the current browser capture. Previous images remain
  historical experiment references.

Lighthouse does not prove complete accessibility. Comprehensive keyboard/screen-reader
coverage, clipboard-denial fallback and real mobile hardware remain unverified.
The 2.2 MB source illustration atlas needs delivery optimization before production
adoption. This remains a reviewable local prototype, not an approval or execution
receipt for any consuming project.

## Approved local implementation: 2026-10-27

Current implementation evidence and remaining acceptance (duplicate document removed at owner request)
supersedes the earlier candidate's current-state claims. It records 36 passing
unit/source tests and the ten-case browser viewport/theme matrix, with explicit
limits. Every skill remains reachable; planning definitions, priorities, promotion
and maintenance now have distinct contextual explanations.

Only the panel body scrolls; its title, close action and copy action remain visible.
A repeated node selection preserves the edited request. Changing context replaces
its default with feedback; pending copies are invalidated by selection, dismissal
or editing. Copy results cannot overwrite another request's context. Relationship
prose is owned by `context-copy.mjs`; `request-state.mjs` owns selection/copy identity,
while the textarea remains the single edited-text owner.

T1-T6 are complete. T7, the owner/reviewer comprehension walkthrough, awaits human
answers; no agent-generated comprehension result is claimed. Safari, real devices,
native browser zoom and spoken screen-reader behavior remain unverified. Historical
Lighthouse/performance scores above are not fresh audits of this revision.

## Owner walkthrough

[Four independent plain-language walkthroughs](walkthrough.html) list the actual
node selections, disclosures and feedback questions for T7. This is a separate
local review handout, not another prototype view or a recorded acceptance result.

## T7 feedback repair: 2026-10-27

The owner identified where to amend a requirement but found the page did not explain
why Cortex was needed when the agent could clarify and edit directly. The panel now
leads with ordinary agent help versus the additional value of reusable Cortex
methods, artifact contracts and quality constraints. Asset types and defining
examples are disclosed on demand; existing adopted constraints remain applicable.
The same map/panel/disclosure interaction is preserved, so this explanatory repair
does not create a new UI workflow under the UI design trigger/skip contract.

The added source/model test failed before the usage data existed and then passed.
[Repair tests](audit/t7-boundary-tests.txt) and the refreshed browser/contrast
reports record verification. Prior `req03-*` tests and manifests remain historical
candidate evidence; [the T7 source manifest](audit/t7-boundary-manifest.json)
identifies this revision. The walkthrough is In Progress, not accepted.

[Detailed T7 feedback, repair and verification](audit/t7-boundary-evidence.md).

## Help perspectives: 2026-10-27

The owner rejected agent-capability comparison as the primary reading model:
readers have different expectations of agents. They authorized point/line/plane
perspectives while preserving one map and contextual disclosure. These terms must
not become skill levels, stages or the sole taxonomy.

### UI decision and handoff

| Decision | Behavior / rationale |
| --- | --- |
| User task and entry | Visitors enter through their work problem, select a node and see concrete Cortex help first. No prior judgment of agent capability is required. |
| Alternative interpretations | Work perspective: a work item, its prerequisites/loops and shared goals/agreements. Evidence perspective: a concrete artifact, its references/checks and overall consistency/traceability. These are two useful interpretations, not an exhaustive or mandatory classification. |
| Selected approach | One native selector changes explanations for the same map and work selection. It does not filter skills, create another graph or turn relationships into a fixed workflow. |
| Rejected alternatives | Separate point/line/plane pages would repeat context. Assigning skill families or user seniority permanently to the three terms would misrepresent their relative meanings. |
| Default / empty | Work perspective is the default. Without a work selection, changing perspective updates the short invitation rather than inventing a first stage. |
| Selected / recovery | Change updates the three contextual descriptions and scrolls the explanation body to them. It preserves the selected work, edited request, current example and in-flight copy identity. Close returns to the work trigger. |
| Scene boundaries | Ordinary conversation versus Cortex support is now a collapsed, concrete explanation for each of the ten work contexts. Existing adopted constraints still apply; asset types remain available inside that disclosure. |
| Reuse and accessibility | Native select, existing panel and disclosures, shared typography/appearance and orange accent are retained. Added help data is local, synchronously resolved and announced through the existing explanatory surface. No loading service or extra animation was introduced. |
| Independent assets | Current local entry and the linked captures below identify the revision. No new illustration was needed; the existing generated atlas remains the visual source. |
| Acceptance method / roles | Maintainer verifies both perspectives at the five established widths in both themes, map count, request preservation, focus and copy behavior. Owner continues the human T7 walkthrough separately; no comprehension pass is inferred. |

`help-lenses.mjs` owns view identifiers, labels and point/line/plane content for
all ten contexts. `panel-model.mjs` resolves a copied view of those values;
`story.mjs` owns only the current perspective and DOM composition. Perspective
changes neither invoke skills nor mutate business state. `context-copy.mjs` owns
scenario-specific ordinary/Cortex boundary prose. These are localized prototype
content sources; the canonical defining assets retain authority.

The new model tests were red before the perspective module existed. A browser
assertion then caught that changed explanations could remain scrolled out of view;
the repair resets only the explanation body, retaining request text and identity.
[40 passing tests](audit/lenses-tests.txt),
[perspective browser report](audit/lenses-browser.json) and
[verification/limitations](audit/lenses-evidence.md) record this candidate.

The native in-app selector was also exercised with click, Down and Return; the
accessibility tree showed the selected perspective and empty-view explanation
change. The headless runtime could not exercise native popup arrow selection;
its separate limit is retained rather than presented as a headless keyboard pass.

T7 remains In Progress. Approved snapshots and the public website remain unchanged;
this records the owner's authorized local prototype refinement.

## Graph-level perspectives: 2026-10-27

The owner found that changing only contextual prose did not make the perspective
visible in the map, and questioned whether point/line/plane was useful reader
terminology. This authorized refinement supersedes the earlier explanation-only
view contract above. Those terms now remain internal modeling keys rather than
user-facing concepts to learn.

| UI decision | Current behavior / rationale |
| --- | --- |
| Reader task | Choose Work and cooperation or Artifacts and evidence, then inspect the same subject in one primary map. |
| Work view | Action-oriented node names, bidirectional work/recheck arrows and the shared work area explain cooperation. |
| Evidence view | Artifact-oriented node names/subtitles, reference endpoints and labeled evidence associations, and a dashed shared-delivery region show what supports what. Operation prerequisites remain distinct. |
| Orientation | Positions and logical node IDs stay stable so the visitor can compare corresponding subjects. Shape, labels, connector meaning, legend and group emphasis change together; color alone is not the view signal. |
| Rejected alternative | Relocating every subject would make comparison harder. A second graph would compete with the single main view. Renaming the sidebar alone hid the change. |
| State and recovery | Selection, edited request, copy identity and skill membership remain unchanged; the contextual heading follows the projected subject. Empty view does not invent a selected first step. |
| Small screens and access | Mobile text connectors receive the corresponding meanings; map text alternatives and accessible node names follow the view. The existing native selector, keyboard/focus patterns, theme tokens and reduced-motion policy are reused. |
| Acceptance handoff | Maintainer inspects both themes at the established five widths and checks actual node names, connector labels/endpoints, group boundary style, request preservation and one-map structure. The owner separately judges comprehension in T7. |

`getMapProjection()` in `help-lenses.mjs` owns the two sets of node labels, relation
meanings and shared-area descriptions. `story.mjs` renders them into the same DOM;
`workspace.css` provides complementary shape/connector/group cues. Semantic
references retain their local defining-asset authority. The native in-app view
selector was exercised again, and its accessibility tree exposed the changed
artifact node names and map description.

[Graph-level evidence and current screenshots](audit/graph-perspectives-evidence.md)
record 41 passing tests, both-view browser and appearance checks, limitations and
source identity. Publication remains excluded and T7 remains In Progress.

## Current decision boundary: 2026-10-27

D1-D3 are settled: find applicable assets and know how to use them, through one
primary global relationship map. The agent first checks complete coverage,
relationship accuracy and findable purpose/use guidance; the owner then reviews
the map as a whole. Search, views and request helpers are optional aids.

[Current three-criterion self-check](audit/aic04-three-criteria-review.md) records
fresh model checks, reused evidence and remaining gaps. Owner acceptance remains
pending. Historical T1-T7 narratives describe the removed task chain and do not
close AIC-REQ-04. No prototype change or publication accompanies this consolidation.

## Current local revision: direct per-skill usage

The owner's 2026-10-27 instruction is implemented for all 70 registered skills:
open a skill beside the single map to read Chinese applicability, required input,
usage and expected outcome. Optional lookup opens the same explanation directly;
English definitions remain optional sources. Internal assessment routes through
its public coordinator. Guidance is localized display content authorized by the
owner, not a translation or replacement of canonical Skill instructions.

[Per-skill content](skill-guidance.json), [lookup model](skill-guidance.mjs) and
[tests](skill-guidance.test.mjs) have one content owner and source-drift checks.
[Local verification and screenshots](audit/skill-guidance-evidence.md) record the
checks and limits. This supersedes the earlier source-only usage gap; owner
whole-map acceptance and publication remain separate and unperformed.

## Current local revision: asset access without explanatory scrolling

Selecting a graph node immediately shows its related-skill selector above the
scrolling body. The default skill guidance and work explanation are separate
content choices; the selector remains fixed for either. All 70 skills remain
available through their node contexts and optional lookup. Changing skill does not
replace an edited work request. Long instructions may scroll; reaching the asset
control does not require page or explanation scrolling. Native popup menus retain
the browser's own selection/scroll behavior.

[Current fixed-entry verification](audit/asset-entry-evidence.md) supersedes the
prior nested-disclosure browser path. Earlier per-skill reports and harnesses are
historical and must be interpreted against their recorded source hashes, not run
as current-layout acceptance. Canonical definitions and localized guide content
remain unchanged. One primary graph, local-only scope and pending owner acceptance
are preserved.

## Current local revision: one fixed work map

At the owner's request on 2026-10-27, angle switching is removed. Only the work
relationship map remains. Its node/connection meanings, all 70 skills, fixed asset
selector, Chinese usage fields and skill/work explanation choices are retained.
`work-map.mjs` owns the single map; the old lens module and alternate display data
are removed. Earlier multi-perspective notes and reports describe preceding studies.

[Single-map verification](audit/single-map-evidence.md) is the current reproducible
entry. No publication or owner acceptance is inferred.

## Current local revision: skills are the visible graph nodes

All 70 skills are now expanded in the one primary graph, grouped by the work they
help with. No asset dropdown or collapsed list hides the primary inventory. The
whole graph uses normal page scrolling to keep labels readable. Selecting a skill
highlights its direct neighbors and draws evidenced connections; the panel explains
usage, exact relationships/conditions/sources and work context. It is not another
main map. Angle switching remains removed.

[Graph model](skill-graph.mjs), [curated relationships](skill-edges.json) and
[model tests](skill-graph.test.mjs) own the new display contract. The 53 relationships
cover conditional coordination, method reuse, artifact input and optional
recommendation. Shared topic alone creates no edge; the curation is not an
exhaustive claim about every possible interaction. Five overview edges appear
initially, and selection shows the complete recorded direct neighborhood.

[Current expanded-graph verification](audit/expanded-skills-evidence.md) supersedes
picker and macro-node browser paths. Prior reports retain their recorded-source
scope. Local-only authorization and pending owner whole-map acceptance continue.

## Current visual repair: compact labels and clear routing lanes

Asset nodes now use compact Chinese labels, with IDs in tooltips/usage instead of
an extra line per node. Related nodes show relationship labels inline. Dedicated
column gutters and orthogonal routes keep strokes out of asset contents; separate
relation kinds use separate lanes and cross-column links take nearby safe gaps.
All 70 skills remain expanded; the 53 source-backed relationships are unchanged.

[Current compact-routing verification](audit/compact-skills-evidence.md) replaces
the prior curved-routing checks. It includes actual SVG/node collision checks,
node-size bounds, dense-hub cases and context-only redraw after resizing. Local-only
scope, no angle switch and pending owner acceptance are retained.

## Current label contract: show both name and description

Every primary node shows the formal skill name (for example `define-mission`) on
its first row and the Chinese purpose description on its second. Neither is
replaced by the other or confined to hover/details. Relation badges have a separate
cell. Names wrap completely, and the existing routing gutters are retained.

[Current name-and-description verification](audit/named-skills-evidence.md) covers
all 70 visible pairs, their bounds, routing and responsive behavior. The preceding
single-line/hidden-name layout is superseded; earlier reports remain historical.

## Topic-spine branch redesign

The local graph now uses topic anchors and relationship-based skill branches, with
shared methods and independent skills kept visible. Topic order is navigation only.
Names, Chinese purposes and all four usage fields remain available. Verification:
[audit report](audit/branch-layout-evidence.md),
[model checks](audit/branch-layout-tests.txt),
[browser checks](audit/branch-layout-browser.json).

## Current revision: topic relations and folding

The continuous topic spine is removed. One map shows sourced input relationships,
repair/recheck loops, conditional calls and an independent on-demand support region.
Topics start folded, with counts and explicit controls; search and peer navigation
reveal their destinations. See [current evidence](audit/topic-map-evidence.md),
[model tests](audit/topic-map-tests.txt), and [browser checks](audit/topic-map-browser.json).
This supersedes the always-expanded branch presentation; prior reports retain their
historical scope. Owner acceptance and publication remain pending.

## Current presentation: one connected global graph

All topics now share one persistent work-context graph, with distinct contribution
associations and evidenced directional relationships. Folding changes only the
skill branches below it in the same canvas. Topic nodes, lines and labels remain.
See [current evidence](audit/global-map-evidence.md),
[model log](audit/global-map-tests.txt), [browser report](audit/global-map-browser.json)
and [overview](audit/global-map-overview.png). Earlier separate-region evidence
retains its historical scope. This remains local and unaccepted by the owner.

## Current presentation: direct relationships between topics

The work-context hub is removed. Ten topics connect directly through 13 curated
artifact inputs, conditional calls, feedback and specific support relationships.
Every line exposes its condition and source. Topic paths and labels remain visible
when skill branches fold. See [current evidence](audit/direct-map-evidence.md),
[model log](audit/direct-map-tests.txt), [browser report](audit/direct-map-browser.json)
and [complete desktop view](audit/direct-map-1280-overview.png). Earlier hub and
pair-layout reports describe their historical revisions. No publication or owner
acceptance is implied.

## Current presentation: skills expand inside their topic

The lower-page skill dock is removed. One topic expands locally at a time, with
its heading and bounded skill list together. The active desktop column widens,
peer cards remain compact and topic links reflow around them. Skill connectors
scroll/clip inside their own list. Small screens support graph-local horizontal
panning and keep the selected topic/skill above the explanation sheet.

See [current evidence](audit/local-branch-evidence.md),
[model checks](audit/local-branch-tests.txt),
[browser report](audit/local-branch-browser.json), and
[local desktop expansion](audit/local-branch-1440.png).
Prior lower-dock evidence records its historical scope. This is local only.
