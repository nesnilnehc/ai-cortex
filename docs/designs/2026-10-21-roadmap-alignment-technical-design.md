---
artifact_type: technical-design
lifecycle: snapshot
created_at: 2026-10-21
parent: ../process-management/backlog/2026-10-20-roadmap-capabilities.md
status: approved
---

# Existing-project roadmap alignment

## 1. Goal

Add the user-authorized first-alignment scenario without treating compliance work
as permission to replan. Existing business decisions and stable links are protected.

## 2. Architecture and service decomposition

The Roadmap Spec owns preservation, its quality Rule judges it, review classifies
gaps, define repairs structure and update handles separately authorized maintenance.
The orchestrator routes intent before applying normal planning conditions.

## 3. Components and detailed design

`align-existing` takes precedence over bootstrap/refresh/intake. Its path is review,
needed definition/authorized maintenance, then re-review. It skips strategy, intake,
scoring, dependency registration, promotion and archiving unless separately requested.
No generator or automatic migration is introduced. Existing paths are discovered;
unavailable source facts remain limitations. No application UI changes are involved.

## 4. Database design

No new persistent configuration, data field or document family. Use existing records
and transient before/after observations to verify preservation.

## 5. Interface contracts

All renderer schemas and output names remain unchanged. The optional generator is
not required when it cannot preserve established names/anchors or unknown fields.
Manual repair retains protected URLs, identities, facts, scope and commitments.
Alignment is an intent branch, not another team/delivery scenario recipe.

## 6. Data flow and error handling

User alignment intent → source discovery → read-only review → structural repair or
separately authorized correction → before/after comparison → re-review. Missing
plan location stops for evidence; missing goals do not bootstrap a new strategy.
Conflicting facts are reported, not resolved through defaults. No-op retries write
nothing and unknown history is not reconstructed.

## 7. Technology choices and trade-offs

Keep the skill-driven workflow rather than adding a routing service for testability.
Use a manual before/after example to demonstrate nonstandard paths and anchors;
forcing generator input would hide this compatibility case. Route choices therefore
have explicit examples and review criteria, not a claimed live-agent test result.

## 8. Test strategy

Extend example checks to compare protected source-row facts/order, delivery/closure
statements and links/anchors. Mutation controls must detect changed tier/status,
commitment, source identity and removed anchor. Existing generator suites guard
unaffected behavior. Checks validate artifact consistency, not live-agent compliance.

## 9. Acceptance criteria

- EA1: Intent selects bounded alignment before normal planning routes.
- EA2: Structural repair preserves known business facts and stable links; unavailable
  facts and earlier history remain unknown.
- EA3: Definition and maintenance retain distinct authorization boundaries, followed
  by re-review; no repeated no-op changes occur.
- EA4: A complete nonstandard-path example and mutation-backed checks pass, with
  limitations explicit and no consuming project modified.
