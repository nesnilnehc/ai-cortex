# Example: Service Desk Roadmap

This fictional example demonstrates entry granularity, not approved project work.
IDs below stand for source links in an adopting project's roadmap; no source files
are created merely to complete the example.

Updated: 2026-10-08

Make request handling trustworthy first, then reduce repeated entry, and expand
external collaboration when real users and permissions are available.

## Roadmap

| Tier | Requirement / defect | Expected outcome | Priority | Status / key condition |
| --- | --- | --- | --- | --- |
| Now | BUG-17 · Duplicate submission after refresh | Refresh and retry preserve one external request | P0 | In progress; source acceptance verifies one external effect |
| Now | REQ-12 · Explain request outcomes | Users distinguish confirmed success, failure and unknown results | P1 | Approved; complete when source acceptance passes |
| Next | REQ-21 · Confirm related requests together | Users confirm several requests with isolated failure handling | P1 | Draft; needs approval and the existing audit contract |
| Later | REQ-30 · Collaborate through an external workspace | Authorized users handle requests in their existing workspace | P2 | Re-evaluate when a real adopter and write permissions exist |

## Why this order

Prevent duplicate external effects before making submission faster. Batch confirmation
reuses the audit contract. External collaboration waits for a demonstrated use case.

## Current boundaries

Mobile delivery is paused until the user explicitly resumes it. Batch confirmation
on desktop may proceed independently. Approval and release remain separate decisions.

Backlog requirements and defects must map to the roadmap; items outside it are not
done by default.

## Detail stays in sources

A real roadmap links the four source records and existing work-item and evidence
indexes. Database migrations, API handlers, browser tests and task completion counts
belong there. A missing prerequisite is shown as a blocker, not as a lower priority.
