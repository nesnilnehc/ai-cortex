---
artifact_type: functional-design
lifecycle: snapshot
created_at: 2026-10-28
parent: ../requirements-planning/AIC-REQ-08.md
status: approved
---

# Functional design: Skill provenance presentation

## Goal

Users see badges for third-party Skills and can inspect recorded provenance evidence for every Skill; maintainers receive actionable review recommendations before confirming classifications.

## Functional modules and boundaries

| Module | Responsibility | Boundary |
| --- | --- | --- |
| Provenance investigation | Assemble creation records, actual external sources, comparisons and a classification recommendation for the current Skill version | Prepares evidence; does not confirm on the maintainer's behalf |
| Maintainer review | Present the review packet, capture confirmation or correction and identify unresolved facts | Human decision in the existing repository/chat contribution workflow; no new administration website or automated approval |
| Catalogue readiness | Identify missing, inconsistent or outdated decisions across the full catalogue before delivery | Reports actionable failures; does not remove Skills to make coverage pass |
| Reader presentation | Present the same classification and evidence in the index and website | Explains provenance; does not score quality or change Skill execution |

## Business workflow

The agent or contributor starts with the current catalogue and the version under review. The maintainer decides the proposed classification; the contributor checks catalogue readiness and prepares presentation for delivery. Covers R1, R2, R4, R5, R6, R7.

```text
Catalogue or Skill change
  -> Contributor investigates records and sources
  -> Prepare recommendation and evidence packet
  -> Evidence complete?
       no -> Report missing facts -> Investigation blocked (end of this attempt)
       yes -> Maintainer reviews
                no response / withdrawal -> Review pending or withdrawn (end)
                correction -> Record corrected decision and supporting evidence
                confirmation -> Record confirmed decision and supporting evidence
  -> Decision still describes current Skill version?
       no -> Review required again (end of this attempt)
       yes -> Check complete catalogue
                failure -> Catalogue not ready; report affected Skills (end)
                pass -> Prepare matching index and website labels
                     -> Reader opens evidence -> Reader returns to discovery (end)
```

A blocked attempt resumes at investigation when new evidence arrives. Catalogue readiness is distinct from this design's approval and from permission to publish remotely.

### Maintainer review packet

Present one clearly identified Skill/version per decision, allowing a batch summary without hiding individual decisions. The packet has the following fields; their purpose is to make R7 actionable rather than ask for an unsupported yes/no answer.

| Review point | Information and recommended action |
| --- | --- |
| Identity and creation | Skill name/version, creation commit or related requirement; inspect whether the record describes the current content |
| External influence | Actual source references and which method, workflow or expression they informed; distinguish creative input from tool-use lookup |
| Upstream comparison | Where applicable, the pinned source and complete distributed-file comparison; recommend the R2 category when it matches |
| Local work | Summarize modifications or independent rewriting; explain the R6 recommendation, including article-based sources without upstream Skill files |
| Original recommendation | Cite creation evidence and explicitly ask whether external creative reference was used; do not infer absence from Git history |
| Missing facts | List the exact fact to verify and suggest the next investigation step; do not invite confirmation while essential evidence is missing |
| Decision | Recommended category and reason, then ask the maintainer to confirm or correct it; retain the final identity, date, decision, rationale and evidence references |

The agent assembles the packet; the maintainer supplies the attestation and may correct factual omissions. A correction is evaluated against the cited evidence, not treated as permission to bypass R1–R6.

## Exception and edge scenarios

| Trigger | Expected business behavior |
| --- | --- |
| Creation or source evidence missing | Name the missing evidence and next investigation step; keep delivery blocked for the affected catalogue, without a fourth public label. Covers R1, R5, R7. |
| Maintainer declines, withdraws or does not answer | Preserve the packet and review outcome; no confirmation is inferred and no timeout approves it. Covers R7. |
| Duplicate confirmation for the same unchanged version | Retain one effective decision with its supporting record; do not request the same confirmation again. Covers R7. |
| Competing decisions or content changed during review | Show the disagreement or version mismatch and seek a decision for the current content; an old confirmation cannot resolve it. Covers R1, R7. |
| Previously unchanged distribution gains, loses or changes a file | Return the affected version to investigation and compare again before catalogue readiness. Covers R2. |
| Evidence cannot be opened by a reader | Show an actionable evidence-access error and allow retry or return to the Skill; retain the supported label rather than invent a replacement classification. Broken required evidence links fail delivery acceptance. Covers R3, R4. |

## Business object states

These are internal review states, never additional provenance categories.

| State | Entry | Event and next state |
| --- | --- | --- |
| Investigating | New Skill/version or invalidated decision | Complete packet -> awaiting confirmation; missing facts -> blocked |
| Blocked | Essential fact missing or conflicting | New evidence -> investigating; withdrawn -> withdrawn |
| Awaiting confirmation | Complete packet presented | Confirm/correct with sufficient evidence -> confirmed; missing evidence -> blocked; withdrawal -> withdrawn; no response -> unchanged |
| Confirmed | Recorded decision matches reviewed version | Relevant content/source change -> investigating; catalogue checks pass -> ready |
| Ready | All catalogue decisions and presentation checks pass | Relevant change -> investigating; otherwise terminal for this delivery |
| Withdrawn | Review attempt explicitly withdrawn | Terminal for this attempt; a new review starts investigating |

## Roles and permission matrix

These are existing workflow responsibilities, not a new account or access-control system.

| Role | Menu/access | Operations | Data |
| --- | --- | --- | --- |
| Reader | Existing public discovery and evidence entries | Browse, open evidence, return | Public classification and supporting evidence only |
| Contributor/agent | Existing repository and authorized chat workflow | Investigate, recommend, record explicit decisions, validate | Authorized local evidence and public delivery material; no credentials or private chat contents in public evidence |
| Maintainer | Existing review workflow | Confirm/correct own review decision and rationale | Review packet and decision record; remote publication requires separate authorization |

## UI and interaction flow

### Reader task and coverage

The reader enters through classification, relationship discovery, search or a direct Skill detail. Each third-party Skill presentation has a short text badge at its upper right; confirmed originals omit the badge but retain evidence access. Relationship references that identify an individual Skill also show its third-party badge when applicable; relationship edges and topic-only headings do not represent Skills and have no provenance badge. The generated index places evidence with every Skill entry and a provenance badge with each third-party entry. Covers R1, R3, R4.

A badge is descriptive text. An adjacent, separately focusable evidence action opens the supporting evidence, with an accessible name identifying the Skill. Existing selection controls continue opening the detail panel. The evidence action must not be placed inside another interactive control. Return navigation preserves the selected Skill, view, search query and scroll position.

### States and recovery

- Default/success: third-party Skills have their supported labels and confirmed originals omit badges; evidence can be opened without selecting another Skill.
- Loading: retain the existing page-loading treatment; do not render an unclassified Skill as an interim result.
- Empty search: preserve the existing no-results message; no Skill exists to label.
- Invalid catalogue: fail delivery validation before replacement of the last validated reader-facing catalogue; report affected Skills to maintainers. Do not show partial classification as a successful catalogue.
- Evidence navigation failure: use the existing navigation error/retry path and allow return; no automatic relabeling.
- Maintainer pending/blocked/withdrawn states appear in the review packet only. There is no new public confirmation form or disabled public approval action.

### Layout, reuse and rationale

Reuse the existing website's classification rows, relationship nodes, search entries and detail panel, along with its typography, light/dark tokens, focus treatment, selection and responsive sheet behavior. Give the badge its own top-right region; let long text wrap and move the Skill name below that region when width is limited. Do not overlap text, shrink names to illegibility or rely on color to convey classification. Use the existing locale selection for equivalent label wording.

Evidence access is a sibling action so the existing Skill selection path remains usable. Showing provenance only in details was rejected because it hides the distinction until after selection. Making the entire badge a replacement selection action was rejected because it changes the discovery task.

Independent pixel mockups are unnecessary for this additive reuse of existing row and panel patterns. Local reference baseline: [classification view](../../website/explore/classification-view.mjs) and [dual-view styling](../../website/explore/dual.css), as inspected on 2026-10-28; these are implementation references, not proof of a completed UI. No external visual reference is needed.

### Acceptance handoff

The implementing contributor verifies FD-01–FD-08 using catalogue fixtures, interaction checks and recorded manual visual/keyboard inspection. The maintainer checks decision packets and confirms the final classification records. UI evidence must come from the eventual implementation; this document does not claim the UI has been run or visually accepted.

## Acceptance criteria

References to upstream acceptance items below use their current list order in [AIC-REQ-08](../requirements-planning/AIC-REQ-08.md#acceptance-criteria).

1. **FD-01 — coverage:** compare the complete catalogue with index and all website Skill locations; every Skill has exactly one matching classification and reachable evidence. Missing/conflicting records prevent readiness without dropping Skills. Upstream AC1, AC7; Covers R1, R4.
2. **FD-02 — original evidence:** review a packet supported by a creation record and explicit maintainer confirmation; reject Git history alone. A tool-use-only reference does not change the recommendation. Upstream AC2; Covers R5.
3. **FD-03 — classification boundary:** compare unchanged upstream, copied/modified and article-informed rewrite packets; decisions follow the respective upstream rules, including no upstream-file requirement for article-based adaptation. Upstream AC3, AC5; Covers R2, R6.
4. **FD-04 — confirmation:** inspect confirm, correct, unanswered and withdrawn cases; every effective decision retains all R7 review fields and a human decision. Missing facts yield a concrete next investigation step. Upstream AC4; Covers R7.
5. **FD-05 — change and concurrency:** change/add/remove a distributed upstream file or change content during review; the old decision no longer establishes readiness. Conflicting decisions require resolution for the current version. Upstream AC1, AC4, AC5; Covers R1, R2, R7.
6. **FD-06 — responsive presentation:** inspect both third-party badges and unbadged confirmed originals in each Skill location at 360px and 1280px in light/dark themes; text remains readable, badges stay upper right and names/purposes do not overlap. Upstream AC6, QAS-01; Covers R3.
7. **FD-07 — navigation:** by keyboard, select a Skill, open evidence, return, switch views and search; labels are readable without color, focus is visible, evidence is operable and discovery state is retained. Exercise evidence failure and empty search recovery. Upstream AC6, QAS-01; Covers R3.
8. **FD-08 — execution boundary:** presentation and catalogue validation do not retrieve upstream data or alter Skill execution. Upstream AC7; Covers R4.

## Trade-offs and open questions

- Full classification before delivery increases initial maintenance work and may block delivery on one unresolved Skill. Silent omissions or an unknown public label were rejected because they violate the approved coverage decision.
- Maintainer attestation makes original classification practical but depends on informed human judgment. Git-only inference was rejected because it cannot establish external influence; absolute proof would make the workflow unusable.
- Use the existing maintainer contribution workflow rather than a new administration interface: the latter adds review navigation and account-management work without improving the required decision packet.
- No unresolved functional decision. Public evidence must use publishable records rather than expose private conversations. Reconciliation of the source contract, version binding, data format and generation boundaries belongs to technical design after this functional design is approved.

## Approved display amendment — 2026-10-28

Per the user amendment in [REQ 08](../requirements-planning/AIC-REQ-08.md#display-amendment--2026-10-28), only confirmed originals omit badges. Evidence actions remain separately focusable for all categories. Unknown or missing classifications still block delivery; they do not share the original display path. This amendment supersedes earlier references to three visible labels in this snapshot.

## Website display amendment — 2026-10-29

The approved requirement now omits audit-material links from every website surface, including generated static fallbacks and the asset directory. This supersedes earlier website evidence-navigation sections. Preserve third-party text badges, unbadged originals, Skill source navigation and repository evidence validation.

## Original-source navigation — 2026-10-29

Covers R3 and AC6 as amended. Readers open a third-party badge to inspect its actual original source, then return to the unchanged catalogue. A single source uses the existing external-link pattern and opens a new tab. Multiple sources use native details/summary to expand a titled list; Enter/Space toggles it and Tab reaches each link. Closed is the initial state; reopening preserves Skill selection. Originals have neither badge nor source control. Missing/unsafe source data fails the existing catalogue gate and retains the static fallback; an unavailable external page leaves the catalogue intact. No new loading state or role is introduced.

Reuse current badge placement, text, color tokens, selection controls and responsive layout. Reject separate arrow buttons because they duplicate the entry. No independent mockup is needed for this localized change to existing controls. Acceptance: the frontend owner verifies single-source destinations, multiple-source keyboard behavior, preserved selection, no audit links and no overlap at 360px/1280px in both locales. No unresolved business decisions.
