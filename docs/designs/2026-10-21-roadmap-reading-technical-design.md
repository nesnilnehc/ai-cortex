---
artifact_type: technical-design
lifecycle: snapshot
created_at: 2026-10-21
parent: ../process-management/backlog/2026-10-20-roadmap-capabilities.md
status: approved
---

# Roadmap reading hierarchy and policy references

## 1. Goal

Make the existing roadmap model easier to read without creating a second priority
policy, changing settled placement, or migrating adopting projects. User approval
covers this refinement of the existing roadmap capability, not external publication.

## 2. Architecture and service decomposition

The Roadmap Spec owns concept and reading contracts; its quality Rule owns review
criteria. Planning skills apply them. The offline renderer presents supplied facts;
source records remain authoritative. No new service, configuration or schema is needed.

## 3. Components and detailed design

Modern main documents open with direction, the current arrangement explanation and
unverified execution mappings before the requirement table. Policy, closure,
selection and language evidence appear after delivery and revisions in a planning
basis section. Selection remains inspectable, rather than occupying the first screen.
Legacy 1.0–1.2 single output retains its layout; explicit split output uses the modern
hierarchy. Source-only policy references become safe links in modern output; prose
policies remain escaped text. No narrative facts are inferred from tiers or dates.

Dependency mapping identifies the deliverable needed for the next intended step,
its owner and need-by point in existing item evidence. Promotion checks that step,
not completion of the entire prerequisite item. A later dependency permits parallel
work only with source evidence and a visible later condition. Unknowns do not pass.
The orchestrator checks missing/stale dependency evidence even for a single candidate.

This is document presentation using established Markdown patterns, not a new app
interface or interaction; separate UI assets and application UI acceptance are inapplicable.

## 4. Database design

No database or new persistent fields. Reuse the existing priority decision, item
dependency evidence, roadmap selection and source/history records.

## 5. Interface contracts

Keep schemas 1.0–1.5, required fields, filenames, enums and authorization unchanged.
The existing priority_policy string accepts prose or a source-only reference. Modern
rendering recognizes HTTP(S), fragments, explicit relative paths and bare .md paths;
recognized references use the common validation and escaping contract. Legacy output
continues escaping the field as prose. No automatic sorting or placement is added.

Recommended document-family names describe roles; existing project titles/URLs win.
Generated sibling names remain reserved. Current policy results are linked from
policy rather than maintained as a second current inventory.

## 6. Data flow and error handling

Read source decisions → prepare concise arrangement text → validate facts → render
plan before its basis → review source agreement. Missing execution evidence is
visible before the table, not guessed. Malformed policy references fail validation.
Unchecked dependencies return to mapping; known cycles never become executable work
because a mapping step was skipped. Remote projects remain outside implementation.

## 7. Technology choices and trade-offs

Retain standard-library Python, current schemas and shared template modules. Moving
evidence later improves scanning but requires preserving links and all source facts.
Reject removing default tier advice, automatic dependency-priority inheritance and
a new mandatory rank field: none is needed to explain policy versus its application.

## 8. Test strategy

TDD covers modern single/split reading order, early unknown warnings, safe clickable
policy references, unchanged facts and legacy output. Reproduce complete examples
against independent source tables. Dependency decisions use contrasting grounded
scenarios in the skills; renderer tests cannot certify live-agent planning behavior.
Run links, hygiene, asset versions/index, findings contract and Markdown lint locally.
Inspect generated Markdown in a local preview; no hosted-layout claim is made.

## 9. Acceptance criteria

- RC1: Policy is the rule, priority/order are decisions, and arrangement rationale
  explains their application without becoming another policy.
- RC2: Modern main documents show the plan before maintenance metadata, preserve
  policy/closure/selection/language evidence and expose unknown execution early.
- RC3: Policy references are clickable and safe; legacy inputs and facts survive.
- RC4: Dependency mapping and promotion agree on next-step readiness, including
  parallel work, unknown evidence and a single externally dependent candidate.
- RC5: Templates, complete examples, naming guidance and meaningful checks agree;
  no adopting project, installation or publication is changed.
