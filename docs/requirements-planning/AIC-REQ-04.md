---
id: AIC-REQ-04
artifact_type: requirement
lifecycle: snapshot
created_at: 2026-10-27
status: implemented
implemented_at: 2026-10-28
parent: ../project-overview/strategic-goals.md#goal-4-adoption-friction-is-low
---

# Requirement: [Functional] Contextual discovery and use of AI Cortex

Final delivery (2026-10-28): the owner approved the dual-view documents,
accepted T12, approved the address compatibility repair and authorized T13.
Sites version 8 is published and public verification passes on the unchanged
accepted runtime. T9/T12/T13 are Done. Earlier dated planning/local records retain
their historical scope; current outcome is the [published audit](../calibration/audit-docs.md#aic-req-04-published-and-publicly-verified-2026-10-28).

## Background & Value

Readers cannot tell what AI Cortex contributes to their own work from asset names
alone. Different expectations of agents make capability comparisons unreliable.
They need to identify useful help, its connections and how to use the relevant assets.

## Objective

Readers can find applicable AI Cortex assets for a work problem and understand when and how to use them without first learning the catalogue.

## Scope

In scope: a read-only discovery experience spanning all currently registered
skills, with contextual explanations of supporting asset types, work/artifact
relationships, applicable boundaries, source discovery and usage guidance. Optional
request examples may support that guidance; preparing a request is not the endpoint.
Readers include people unfamiliar with the catalogue and people seeking a known
capability; neither must assess their agent's ability before entering.

The owner retained D1: find applicable assets and know how to use them, without
requiring installation, copied requests or real task execution. D3 retains agent
self-check followed by actual owner review. D2 is revised: Capability overview is
one homepage section with two complementary views, Classification (default, the
original rectangular subject cards) and Relationships. The view switch is local,
not navigation to another page. Both views share identities, guidance, evidenced
relationships and selected-state ownership. The currently explained target (skill,
work, relation or support scope) is explicit, so a stale selected ID cannot replace
its explanation or request when switching. One is visible at a time.

The homepage retains introduction and adoption guidance. Its capability section
contains the dual-view explorer; a compact complete Asset directory indexes Skill,
Spec, Protocol and Rule without repeating the six work-theme cards. Keep existing
valid type/category/install bookmarks through compatible target handling; old
explorer URLs resolve into the same homepage capability section, not another
interactive page. English and Chinese are editions of this same site structure,
not competing experiences. Independent modules are permitted; no runtime service,
account, analytics or real project execution is added.

Chinese names, canonical IDs, distinct purposes and four-field guidance remain.
The current graph can be reused as one renderer, not the primary site architecture.
The original six subject cards are the classification baseline. Do not infer
execution order from their numbering, card position or membership. Passive assets
remain fully findable in the compact directory and explained contextually; no
complete passive-asset graph is promised. Cross-cutting support remains explicit.
All later implementation and publication require their applicable authorization.

AIC-REQ-04 is the sole current requirement document for this topic. At the owner's
explicit request, the duplicate AIC-REQ-03 requirement/design/task files were
removed rather than archived. Earlier prototype evidence remains revision-scoped, not a
second approved requirement or proof that AIC-REQ-04 is complete.
[AIC-REQ-02](AIC-REQ-02.md) is unaffected.

## Business Rules

| ID | Condition | Required behavior or meaning |
| --- | --- | --- |
| R1 | Help and sources are explained | Defining local assets and the generated skill registry retain authority. Summaries may simplify language but cannot expand capability scope or create another invocation contract. |
| R2 | A visitor explores help | Lead with the problem addressed, needed context and resulting work/artifact. Skill names, geometric terminology, user seniority and an assessment of agent capability are not entry prerequisites. |
| R3 | Relationships or views are represented | Distinguish guidance, prerequisites, iteration, feedback and anytime support. Provide Classification and Relationships as two views of the same capability section; neither changes relationship meaning or starts work. Classification membership is not a parent-skill call, and visual position does not establish order. |
| R4 | A visitor selects, searches, changes view or tries an example | Only explanatory interface state changes. No real approval, check completion, commit, message or publication is performed or inferred. |
| R5 | A scene explains applicability | Ordinary clarification, writing and editing can be performed directly by an agent. Cortex provides reusable task methods, artifact contracts, constraints and interaction agreements when applicable. Already-adopted project constraints remain applicable without manually invoking a skill on every turn. |
| R6 | A request is prepared | Preserve the reader's known context and unresolved business decisions. Changing the selected skill or content mode cannot replace edited text; different-work defaults must be announced. Copy completion must refer to the initiating request, with honest manual recovery on failure. |
| R7 | Evidence or delivery status is reported | Distinguish model tests, browser checks, human comprehension and actual external execution. A local demonstration authorizes neither website integration nor publication. Report the three delivery stages separately; publication requires its own explicit authorization. |
| R8 | Delivery advances beyond planning | Require approval of the applicable document revision and explicit authorization before website changes; any baseline exception must cite the actual owner instruction. Integrated owner acceptance precedes separately authorized publication. An earlier approval, Todo task or passing test is not new implementation or remote-write permission. |
| R9 | Website entry points are presented | Home introduces and guides adoption; its Capability overview section offers the two local views; a compact complete four-type Asset directory supports lookup without repeating work-theme cards. Both navigation destinations are sections of the same homepage. |
| R10 | Broad support or localized skill names are shown | Explain applicable support across work subjects without inferring universal calls or exclusive edges. Chinese display names, canonical skill IDs and purpose descriptions remain distinguishable; translations never change invocation identity. |
| R11 | A skill hierarchy or sequence is displayed | Only defining-source-backed coordinator calls create parent/child relations; label required versus conditional invocation and conditions within the stated parent/scenario. A required child is required only after that parent path applies; it is never mandatory for all users or work. Method reuse, recommendations, artifact inputs and classification membership are distinct. Order is partial and conditional, never a fabricated total sequence; feedback cycles remain explicit rather than recursive child trees. |
| R12 | A reader switches view | Retain selected skill/work, explanation mode, edited request and pending-copy identity. Keep each view's local disclosure/scroll/pan state; the same skill is revealed in the destination view without treating representation changes as different work. |

## Acceptance Criteria

D1-D3 are settled for this revision. Both views support discovery and knowledge of use; optional aids do not become mandatory outcomes.

- **A1 — Find relevant help**: From either capability view, a reader can locate a relevant
  asset or contextual entry and identify its purpose, needed context and expected result. Each selected
  context explains Cortex's contribution before catalogue detail. Covers R1/R2.
- **A2 — Judge applicability**: Within the selected scene, explain what ordinary
  agent work can handle directly and what reusable method, contract or constraint
  Cortex contributes. Neither writing a document nor every conversation implies a
  skill invocation. Defining asset types are discoverable on demand. Covers R1/R5.
- **A3 — Understand connections**: Explain the relationships and distinctions in
  both representations, grounded in defining sources, including existing decisions that can be reused.
  Distinguish a prerequisite from a useful reference, and a real outcome from an illustrative result. Skill-to-skill connections identify conditional calls, method reuse, artifact inputs or recommendations, with defining-source evidence and conditions. A shared topic alone never creates an execution edge. Covers R1/R3/R4.
- **A4 — Explore two representations in one place**: The homepage Capability overview provides Classification and Relationships controls, with Classification the initial default unless an explicit valid view link requests Relationships. Only one view is exposed at a time. No page reload, independent explorer navigation or duplicated explanation is required to switch. Both languages use the same asset/relationship meanings. Covers R2-R4/R9/R12/QAS-04.
- **A5 — Reach all skills and sources**: Every current registry skill has exactly one primary entry in each view. Classification cards and relationship topics show skill counts and explicit disclosure. Secondary relationship references are identified as links, not extra owned entries. Expanded skill nodes display both the formal name and localized purpose (Chinese in the prototype and Chinese edition, reviewed English in the English edition); neither requires hover or opening usage details. Search and peer navigation reveal the destination in the current view without forcing a view change. No missing/unknown/duplicate primary entries remain; cross-references link to defining sources.
- **A6 — Explore without losing context**: Classification expands skills inside the original work-theme cards; Relationships retains one connected work graph with direct, source-backed dependencies, loops and support. Each view can keep its own disclosure/layout, while selected topic/work and skill remain identifiable with their shared explanation. Parent/child skills and ordering follow A16, not card position. No lower-page skill dock requires a return trip. Long local lists may scroll; narrow relationship canvases may pan without document-wide overflow. Following cross-category/topic links reveals the real selected asset. Closing the shared explanation restores a valid visible opener in the active view. Collapsing its selected branch closes details and focuses that disclosure. Covers R3/R4/R11/R12/A16/A17.
- **A7 — Know how to use the selected asset**: Readers can identify when the asset
  applies, necessary inputs/prerequisites, how to access and use it in the relevant
  agent/project context, and the expected output or constraint. Explain an
  invocable Skill differently from applying a Spec/Rule or following a Protocol.
  The selected skill explanation directly provides this guidance in the selected UI language; reading a defining source is optional. A suitable example may support this understanding. Actual
  invocation, installation, task completion or production of a copied request is
  not required. If a request-copy aid is retained, its truthful recovery
  and edit-preservation obligations still apply. Covers R1/R5/R6; optional copying
  uses QAS-03/QAS-04.
- **A8 — Operate the local interface**: Selection and dismissal, plus any retained skill/content/search/example/request controls,
  work with pointer and keyboard in the
  recorded local Chromium environment at 360/390/1024/1280/1440 CSS-pixel widths,
  both themes. Skill nodes use compact readable labels; relationship strokes stay outside primary-node content, with visible direction and meaning. No document horizontal overflow; focus, labels and feedback identify
  context. Close and any retained copy control stay reachable. Covers QAS-01 and R4.
- **A9 — Review the capability overview**: The agent first records a self-check of (1) complete current skill coverage, (2) accurate relationships and (3) findable purpose and usage guidance when selecting an asset. The owner then reviews both views of the same identified revision against those three criteria. Record findings and the owner's actual conclusion separately from machine results. No prescribed four-scenario quiz, copied request or real execution is required. Covers R1-R3/R5/R7.
- **A10 — Deliver honest local evidence**: Keep local source/provenance links,
  inventory identity and reproducible evidence. No third-party runtime fetch is
  needed. Without scripts, readable work labels, an explanatory limitation and
  canonical catalogue fallback remain. Unexecuted browser/assistive-technology
  conditions remain unverified. No real execution or public delivery is implied.
  Covers R1/R4/R7.

- **A11 — Integrate the formal website locally**: Both existing website editions
  provide same-page capability navigation and native language links. The integrated
  dual-view section preserves A1-A8 and A10 behavior,
  source meanings and exact current skill coverage. Chinese guidance remains
  directly available; English guidance is reviewed for equivalent meaning. Theme
  preference, installation links and the existing full Skill/Spec/Rule/Protocol
  atlas do not regress. Serve the final runtime bundle with `website/` as its root:
  all required modules/data/styles resolve without repository-root or experiment
  paths; defining-source and script-failure fallback links resolve outside the
  packaged repository. Repeat the A8 matrix, both-language content/link checks,
  registry checks and existing website tests on the identified integrated revision.
  Record owner confirmation that both integrated views meet the revised scheme.
  Acceptance identifies the complete runtime file hashes, canonical asset revision,
  locale content and owner conclusion. Any subsequent runtime, guidance or registry
  change invalidates the affected checks and acceptance; reverify the changed scope
  and obtain renewed owner review when coverage, meaning or the retained scheme
  changes. Local integration acceptance is not publication. Covers R1-R8/QAS-05.
- **A12 — Publish and verify the accepted website**: Only after A1-A11 and A13-A17 pass for the same integrated candidate and
  separate explicit publication authorization is recorded, package the identified
  runtime allowlist and hashes for the existing Sites project. Retain its domain,
  audience and previous known-good version; exclude experiment audits, repository
  documents and unrelated files. Verify anonymous HTTPS/TLS, status, module/JSON
  content types, cache consistency, both-language same-page section/view and legacy-route navigation,
  sources/fallback, theme and the explicit public smoke checks defined in the designs
  at the public custom domain. Record version, source identity, manifest, timestamps
  and actual results, bound to the A11-accepted runtime hashes. Canonical defining
  sources must already be anonymously reachable at their recorded revision and match
  the definitions used for acceptance before public switching; site publication does not implicitly authorize publishing other
  repository work. A pre-switch failure leaves the known-good site unchanged. A
  post-switch failure restores and verifies the known-good version under the same
  scoped release authorization, without overwriting an intervening unrelated release.
  An uncertain switch outcome requires checking the
  actual public version before further mutation. A failed candidate remains
  incomplete even if recovery succeeds; unresolved recovery is explicitly blocked.
  No completion follows solely from upload success. Covers R7/R8/QAS-06.

- **A13 — Understand single-page site structure**: Home introduction, Capability overview, compact Asset directory and Get started are sections of the same page in each language. Capability overview contains the Classification / Relationships switch, not a separate work-relations destination. Replace the duplicate six-theme directory presentation with the classification renderer; retain complete four-type lookup separately. Native navigation, directory/type/install/category bookmarks, language mapping and legacy explorer URLs resolve to the corresponding same-page destination or explicit fallback. Script-free navigation and readable classification/directory fallback remain. View controls, local lookup and theme/language utilities have distinct roles. Covers R9/A11/QAS-01/QAS-05.
- **A14 — Read support scope accurately**: Both views visibly identify project foundations and communication as cross-cutting support with source-backed applicable subjects and conditions available on selection. Folding skills never hides this scope in the current view. No fan of speculative calls, forced execution order or claim that an omitted line excludes support is introduced. Specific evidenced dependencies/feedback remain explicit. Covers R3/R10/A3/A6.
- **A15 — Distinguish localized names from purposes**: In the Chinese edition every current skill visibly presents a reviewed Chinese name, its unchanged formal ID and a separate purpose when expanded; any retained lookup accepts all three. Its detail heading uses the same name/ID. English keeps its reviewed name/ID/purpose convention. Invocation examples retain canonical IDs. No hover or source reading is needed to distinguish identity from explanation, and the three fields remain readable at A8 widths/themes. Covers R1/R10/A5/A7.

- **A16 — Read skill order and parent/child meaning**: Classification disclosure and the relationship renderer distinguish coordinator parent/child calls, required/conditional invocation, existing-artifact inputs, method reuse, recommendations, parallel alternatives and feedback. Each displayed sequence/parent edge exposes defining evidence and conditions, including its applicable parent/scenario. Absence of sequence evidence means order is unknown/unspecified, not proof of parallel execution. Contradictory order within one scenario blocks acceptance; real iteration is shown as feedback, not a cyclic sequence. No unsupported ordered step or child is introduced by card position, topic membership or a shared method. Multiple callers may reference one canonical skill; cycles are finite explicit links, not recursive children. Items with no evidenced order are peers in a stable browse order identified as non-execution order. Covers R3/R11/A3.
- **A17 — Preserve state on view switching**: After selecting a skill, opening explanation modes, editing a request and changing local disclosure/scroll/pan, switching each way retains selected ID/work, shared detail/mode and exact edited text; both views resolve the same guidance and relation conditions. The active explanation target and any independent selected skill are both retained; destination reveal follows that target rather than a stale selection. The destination reveals the selection and remembers its prior local state where compatible. A pending copy is not restarted or invalidated merely by switching; late results still use the initiating request token and never claim success for changed/closed requests. For a user-activated switch, focus stays on that view control; a history-driven switch while lookup is modal keeps focus inside the open dialog. Hidden-view controls leave the tab order. No selection means no invented selection. Switching back restores local position except movement needed to keep the selected asset visible. Covers R6/R12/QAS-03/QAS-04.

### Review evidence

| Criterion | Agent self-check | Owner review |
| --- | --- | --- |
| Complete coverage | Compare current registry IDs with both view/context entries and defining links. | Check whether both views expose the intended breadth of help. |
| Accurate relationships | Compare connectors, conditions, loops and anytime support with defining assets. | Assess whether the two representations communicate the relationships clearly without implying a mandatory sequence. |
| Findable purpose and use | Inspect selection details and source routes for applicability, prerequisites, access/application and expected outcome. | Assess whether selecting relevant help explains what it provides and how to use it. |

Owner review is bounded local acceptance, not a representative adoption study.
Its result remains pending until the owner actually reviews the identified revision.

## Quality Attribute Scenarios

| ID | Quality | Source / stimulus | Environment | Artifact | Response | Measure | Rule refs |
| --- | --- | --- | --- | --- | --- | --- | --- |
| QAS-01 | Accessible interaction | Visitor uses the named A8 operations | Recorded Chromium, A8 widths/themes, pointer/keyboard | Both views, shared details, switch and search | Retain operable context and recovery | All named operations complete; zero document overflow; visible focus; enabled text labels contrast at least 4.5:1 | TST-001, TST-003 |
| QAS-02 | Content integrity | Registered skill set changes | Local registry differs from display snapshot | Both view partitions and source/context associations | Detect drift before claiming full coverage | Exact registry ID parity in each view; unknown, missing and duplicate-primary fixtures fail; labeled secondary references are not counted as primary entries | ARC-001, TST-001, TST-006 |
| QAS-03 | Truthful recovery | Copy is absent, rejected or delayed | An editable request exists; reader may edit, change context or dismiss | Request preparation | Preserve text and associate feedback with the initiating request | Zero false success; no stale result overwrites or relabels another request; manual selection remains available after failure | ERR-004, TST-002, TST-003 |
| QAS-04 | Context continuity | Visitor changes skill/content mode or Classification / Relationships view | Same selected work, with edited text or pending copy | Dual-view host and shared details | Retain work/request identity while revealing selected content | No reload; unchanged selected ID/work/detail mode/edited text across both switch directions; separate view-local disclosure/scroll/pan; visible selected asset and focus; pending copy stays bound to its initiating token | ARC-001, TST-001, TST-003 |
| QAS-05 | Static-site portability | Visitor opens either homepage edition and switches capability views | Preview serves only the website runtime root | Modules, data, source routes and fallback | Resolve the complete candidate runtime closure and correct defining sources | Zero missing runtime files, repository-root dependencies or invalid source mappings; both editions pass A11 and A13-A17 checks, including native navigation/direct bookmarks, four-type directory links and complete localized skill names | ARC-001, TST-001, TST-003 |
| QAS-06 | Recoverable publication | Candidate upload or post-publication verification fails | Existing explicitly authorized Sites release | Identified candidate and known-good version | Stop candidate completion; leave the old version intact before switching, restore it after switching, and determine actual state after an uncertain outcome | Candidate never marked complete on failed checks; observed serving version and manifest prove unchanged or recovered delivery, or the result explicitly remains unresolved | ERR-004, TST-001, TST-003 |

## Dependencies & Prerequisites

Dependent requirement IDs: none. AIC-REQ-02 is adjacent website work, not an
execution prerequisite; AIC-REQ-03 is not revived or reused.

- Source dependency: local [skill registry](../../skills/INDEX.md),
  [protocol registry](../../protocols/INDEX.md) and
  [terminology](../architecture/terminology.md). Verify defining source links,
  descriptions and exact skill parity before acceptance.
- Candidate baseline, not an execution prerequisite: the
  [local experiment](../../experiments/direction-planning/README.md). Existing code
  and reports supply feasibility and reusable evidence only; reconcile against
  this acceptance set. No circular dependency on prior task completion is created.
- Historical prototype checks use a repository-root loopback server. Current integrated checks serve only `website/`; use the already-installed browser/runtime and record its version. No revised runtime checks are claimed by this document review.
- Human acceptance requires the owner/reviewer to complete A9 on an identified
  revision. Prior T7 discussion is partial feedback, not completion evidence.
- Local prototype and integrated-preview validation need no hosting credentials.
- Revised integration depends on approval of this requirement/design/task revision, T10 baseline evidence and explicit website-change authorization. T9 owner comprehension and T12 integrated acceptance occur on the final revised candidate before publication; the historical integration exception is recorded in the 2026-10-27 audit. Existing
  [site contracts](../../website/README.md) govern bilingual navigation, native
  atlas, theme, runtime packaging and baseline tests; AIC-REQ-02 remains adjacent
  established behavior, not an unfinished prerequisite.
- Publication depends on accepted integration whose runtime hashes still match, anonymously reachable revision-bound canonical sources, an identified runtime manifest and
  known-good rollback version, explicit release authorization, and access to the
  existing Sites project/custom domain. Its [deployment record](../../website/.openai/deployment.json)
  is historical evidence, not proof of current access or hosting health. Recheck
  project/domain/certificate state at execution; do not create a new host or alter
  DNS/audience implicitly. Missing access or failed verification blocks publication,
  not local integration.

## Risks, Constraints & Assumptions

| Risk | Probability | Impact | Priority | Mitigation |
| --- | --- | --- | --- | --- |
| Diagram familiarity is mistaken for understanding Cortex's contribution | Medium | High | High | A1/A2/A7/A9 require contribution, applicability and knowledge of asset use, not recognition of labels or obligatory request preparation. |
| A simplified connection teaches an automatic or mandatory workflow | Medium | High | High | Source audit plus A3/A4 counterexamples and changed connector semantics. |
| Prototype tests are presented as new-requirement acceptance | Medium | High | High | Reconcile every item, identify revision/environment, keep human outcomes separate. |
| Repository-root source paths or a mixed cached bundle break the public explorer | Medium | High | High | Root-isolated integration checks, runtime allowlist/hashes, versioned imports and post-publication verification with rollback. |
| A representation switch loses selected context, edited text or in-flight copy identity | Medium | High | High | A17/QAS-04 define shared versus local state, bidirectional and async/focus tests, followed by actual owner review. |
| A browse tree or card order is mistaken for mandatory orchestration | Medium | High | High | A16 source audit, required/conditional call labels, independent peers and finite feedback references. |
| Skill/source drift or a small-screen detail obscures useful context | Medium | Medium | Medium | Exact parity fixtures, source links and A8 matrix with dismissal/recovery. |

Confirmed direction/content: full current skill coverage and contextual explanation
of Cortex help, with one same-page capability section and two complementary views. Separate
publication authorization remains required. Search, request-copy and
walkthrough details remain optional aids, not required user journeys. English repository prose and the scoped
Chinese UI example follow the existing language scheme.

Assumption: work/artifact entry and contextual boundaries help readers with varied
agent expectations. The owner/reviewer assesses this through the whole-map review in A9. No claim about a fixed novice/expert classification or conversion target.
Native Safari, real devices, native browser zoom and spoken screen-reader behavior
are outside this local Chromium evidence claim and must be identified as unverified
unless actually exercised; this is not production accessibility certification.

### Product decisions

| ID | Decision | Current state and consequence | Owner / resolution |
| --- | --- | --- | --- |
| D1 | What counts as using Cortex in this delivery? | Resolved: the owner selected finding applicable assets and knowing how to use them. Real execution, environment installation, task completion and mandatory request preparation are not acceptance prerequisites. | Owner response in this chat, 2026-10-27. |
| D2 | Which experience serves discovery? | Revised: the original rectangular Classification view is default; Relationships is a complementary switch in the same homepage section. No separate interactive page. | Owner instruction in this chat, 2026-10-28; replaces the earlier graph-only/no-switch decision. |
| D3 | What evidence demonstrates the chosen outcome? | Resolved: agent self-check followed by owner whole-map review of complete asset coverage, accurate relationships and findable purpose/use guidance. No mandatory quiz, copied request or execution. | Owner response in this chat, 2026-10-27. |

The previous direct-topic implementation (ten work topics, 13 typed topic edges,
53 curated skill relations and 70 skills) is reusable baseline evidence, not a
permanent topology/count or dual-view acceptance claim. The classification
baseline is the existing six-card homepage grouping. Their groupings may differ;
asset identity, use guidance and relationship meaning must not. The revised
requirement/design chain was approved with explicit T20-T25 local implementation authorization on 2026-10-28. T9/T12 remain unaccepted, and publication is unauthorized.

## Source

- Feature revision request in the same identified chat, 2026-10-28: keep rectangular classification and relationships as switchable views on one webpage; clarify skill order, parent/child semantics and state retention; revise documents only, with no website change or publication.

- Feature revision and review requests in the same identified chat, 2026-10-28: clarify whole-site information architecture, navigation, cross-cutting support and localized names; synchronize and review the four documents, repairing findings without website changes or publication.

- Review correction in the same chat, 2026-10-27: re-review all four planning
  artifacts, repair cross-layer gaps, and retain the planning-only execution boundary.

- Owner instruction in the same chat, 2026-10-27: add formal website integration
  and publication to the requirement/design/task plan, including acceptance and
  dependencies; change no website code and perform no publication now.

- Explicit feature request and revision instruction in chat
  `01a17b19-6aa4-7de0-80e9-5a560aa6bbae`, 2026-10-27: rewrite and re-review
  AIC-REQ-03 and its designs; do not modify review skills or publish the website.
- Decision history: full skill coverage, truthful nonlinear relationships and contextual ordinary-agent boundaries remain. The earlier fixed graph/no-switch decision is replaced by D2 on 2026-10-28: two same-page representations with state retention; no geometric metaphor or prior agent-capability assessment is required.
- [Recorded owner feedback and prototype revisions](../calibration/audit-docs.md)
  and [captured topic](../process-management/backlog/2026-10-27-work-relationship-explorer.md).
- [Goal 4: adoption friction is low](../project-overview/strategic-goals.md#goal-4-adoption-friction-is-low).

## Related proposals and review

- [Functional design](../designs/2026-10-27-help-discovery-functional-design.md)
- [Technical design](../designs/2026-10-27-help-discovery-technical-design.md)
- [Local execution and reconciliation tasks](../designs/help-discovery-tasks.md)
- [Current approved local implementation audit](../calibration/audit-docs.md#aic-req-04-approved-dual-view-implementation-2026-10-28)

The approved dual-view revision replaces the prior graph-only integration plan. The owner explicitly authorized T20-T25 local implementation on 2026-10-28; final owner acceptance is not inferred from this approval or machine results. Verification results and remaining approval/owner-review limits are recorded in the task record and current review. Scoped T7/T8 repairs are locally verified, not global completion or publication approval. Old duplicate documents were removed at explicit owner instruction; no old task completion or implementation acceptance transfers to this requirement.
