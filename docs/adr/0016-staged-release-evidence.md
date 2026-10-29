---
artifact_type: adr
created_by: decision-record
lifecycle: snapshot
created_at: 2026-10-29
status: proposed
description: Separate build capability and version staged release evidence while preserving legacy consumers.
---

# Staged release evidence and build boundaries

## Context

Builds can be requested independently and a release can select among several
candidates. Some required checks are only available after upload. The existing
1.x Release Package requires all required checks to pass before readiness, so
relabeling its status would mislead existing consumers.

## Decision

Provide an independently invocable build capability and a versioned staged
Release Package. Existing 1.x meanings remain intact. New workflows must validate
schema before mutation and cannot send incompatible inputs to an unverified
legacy consumer. The staged package is the authority for candidate selection,
per-target observations and actual results.

## Alternatives

A separate execution record could leave the existing contract untouched, but
would require binding two histories, defining authority for each fact and handling
crashes between writes. An optional sidecar on an executable 1.x package is unsafe:
an old reader may ignore the sidecar and bypass the later gates.

## Consequences

One record can represent candidate and target evidence without silently changing
1.x. New readers, tests and migration boundaries are still required. A reference
reader does not prove that independent deployed consumers fail closed; an
unverified integration remains disabled. Provider execution remains subject to
project-specific capability and authorization.
