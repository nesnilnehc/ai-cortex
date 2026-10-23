---
id: AIC-REQ-02
artifact_type: requirement
lifecycle: snapshot
created_at: 2026-10-23
status: implemented
implemented_at: 2026-10-23
parent: ../project-overview/strategic-goals.md
---

# Requirement: [Functional] AI Cortex promotional website

## Background & Value

Prospective adopters need to understand AI Cortex's value, find relevant
capabilities and reach installation guidance before deciding whether to use it.

## Objective

Visitors can evaluate AI Cortex and find a concrete starting point for adoption.

## Acceptance Criteria

- **A1**: The website can be served as a standalone static directory, with
  `https://ai-cortex.nesnilnehc.top` as its intended public address. Public
  availability is verified separately when deployment is authorized.
- **A2**: The introduction explains delivery and governance value and the four
  asset types consistently with the README and terminology source.
- **A3**: Visitors can follow real links to task-relevant Skills, the catalogue,
  project documentation and installation instructions.
- **A4**: The page shows the README's installation commands verbatim. Copying
  reports success only after completion; on failure the commands remain selectable.
- **A5**: Navigation, disclosures and installation guidance are usable with keyboard
  input and at 360px and 1280px widths, without page-level horizontal scrolling.
- **A6**: The page supports system light/dark preferences and reduced motion;
  the content and navigation remain available without JavaScript.

## Quality Attribute Scenarios

- **QA1**: When a visitor loads the page without JavaScript, or a clipboard write
  rejects during normal use, the installation panel retains all three commands
  for manual selection. After rejection the copy action permits another attempt.
  This supports A4 and A6.
- **QA2**: When a visitor reads or navigates the page at 360px or 1280px, in either
  light or dark mode, the document width does not exceed the viewport width and
  keyboard-operated navigation and disclosures show visible focus. Reduced motion
  has no automatic animation or transitions. This supports A5 and A6.

## Dependencies & Prerequisites

No dependent requirement IDs. The README, asset indexes and terminology document
are the content authority, verified by local inspection. DNS and a static host are
external prerequisites for public availability, to be verified at deployment.

## Risks, Constraints & Assumptions

- Content drift: medium probability × medium impact, medium priority. Link to
  canonical sources, omit changing catalogue counts, and verify installation copy.
- Constraints: repository prose is English; preserve existing unrelated work;
  no external runtime dependencies, accounts, analytics or credential collection.
- Assumption: the supplied domain is the desired public address. The user owns
  confirmation of hosting/DNS at deployment; it does not block local delivery.

## Source

Feature request: [captured intake](../process-management/backlog/2026-10-23-ai-cortex-promotional-website.md).
On 2026-10-23 the user explicitly requested design and implementation based on
that intake. This requirement refines its observable acceptance conditions; it
does not authorize remote publication. Requirement self-review found the scope
and dependencies sufficiently defined for local implementation. English follows
the existing [artifact norms](../ARTIFACT_NORMS.md).
