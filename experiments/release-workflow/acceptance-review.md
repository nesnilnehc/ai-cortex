---
artifact_type: assessment
lifecycle: living
created_at: 2026-10-29
status: active
---

# AIC-REQ-06 acceptance coverage

The [approved requirement](../../docs/requirements-planning/AIC-REQ-06.md) remains
the acceptance authority. Its 14 bullets are referenced below by their order as
AC1–AC14; this assessment does not change the requirement or its approval status.
The [ADR](../../docs/adr/0016-staged-release-evidence.md) and
[workflow guide](../../docs/guides/release-workflow-usage.md) define the delivered
asset boundaries. No separate formal design/task chain was required by the
approved lightweight implementation plan.

## Conclusion and limits

All 14 criteria now have offline fixture evidence for at least their core scenario.
The new full-package reader and local execution fixtures close the previously
missing serialization, artifact, delivery and recovery test seams. They do not
establish independent Agent compliance, real project command discovery, provider
behavior or actual legacy-consumer rejection before mutation. Consequently this
is **offline scenario coverage, not full real-consumer/channel acceptance**; the
requirement's acceptance boxes remain unmarked. Unverified integrations must stay
disabled under the Spec and ADR.

There were no real product builds, uploads, announcements or publications in this
verification. Only the bundled harmless fixture builder executes. Website content
and runtime are unchanged; the previous website deployment is not acceptance
evidence for the release workflow.

## Traceability matrix

Test names below refer to the [contract suite](../../scripts/test-release-contract-v2.py),
[execution suite](../../scripts/test-release-execution-v2.py) and
[consumer suite](../../scripts/test-release-consumers-v2.py). The
[fixture guide](../../tests/fixtures/release-workflow/README.md) describes the real
local boundaries and substituted dependencies.

| AC | Rules | Offline evidence | Remaining real boundary |
| --- | --- | --- | --- |
| AC1 | R6 | Execution `build_records_actual_artifacts…`, `build_does_not_call_combined_tool…`, `build_failure_preserves_failure…`: actual subprocess, ZIP content, digest, failure exit and absence of release/provider writes | Skill-driven discovery and execution in a consumer project |
| AC2 | R1, R7 | Contract `package_round_trip_preserves_candidates…`: two candidates, explicit target selection, unchanged failed history and JSON round trip; execution combined path retains old candidates and creates a new one | Independent Agent candidate association |
| AC3 | R1, R7 | Same package test asserts explicit calendar-example release policy and independent build identities, without deriving one from the other | Consumer-specific version policy |
| AC4 | R1, R7 | Contract `delivery_identity_and_relation_are_required…`, execution `announcement_rejects_pending_target…`: association alone cannot complete or announce a target | Actual target receipt interpretation |
| AC5 | R7, R9 | Contract `package_round_trip_preserves_candidates…`: candidate A rejected, B admitted, both source/build identities and check results preserved | Agent verification of source and check evidence |
| AC6 | R9, R11 | Contract `exception_keeps_failed_result…`: explicit approver and fixture policy, scoped action only, original failed checks unchanged | Real approver authority and project policy provenance |
| AC7 | R11 | Contract `exception_is_denied…`, `observation_records_reject_missing_fields…`; execution `recovery_rejects_stale_receipt…`: missing policy, authority, identity and provider blockers fail closed | Real identity and authorization checks |
| AC8 | R10, QAS-02 | Contract `delivery_identity_and_relation_are_required…`; execution combined and Apple-style paths: actual bytes/digests, unchanged/transformed records, missing or modified output prevents completion/reuse | Real signing/transformation verification rules |
| AC9 | R2, R9, R10 | Execution `apple_style_upload_waits_for_server…`: upload receipt first, pending and failed server checks block, passed check permits target completion | Apple processing, signing and platform states |
| AC10 | R2, R8 | Contract `post_upload_gate_prevents_completion…`: preparation record retains required pending evidence, upload allowed, completion denied until both check and actual delivery evidence exist | Actual preparation Skill output and required artifact policy |
| AC11 | R8 | Contract `aggregate_keeps_optional_outcomes…`: both required complete, required pending/failed/unknown, optional pending/failed/unknown retained, empty and zero-success populations | Provider-specific meaning of complete |
| AC12 | R3 | Execution `combined_pipeline_reuses_project_tool…`: one bundled project build tool, authorization blocks all work when absent, resulting candidate/receipt round trip, no project-specific Skill trio | Discovery of real combined pipelines and their full effects |
| AC13 | R4, QAS-01 | Execution recovery tests: persisted intent, committed local write followed by reply loss, reload and reuse with exact write count; unknown/conflict/inaccessible and competing writer block; announcement retry adds no build/upload | Actual provider lookup, idempotency and crash durability |
| AC14 | R5 | Consumer suite: Spec field-list check, pinned historical reference readers, cross-version rejection before fixture mutation and explicit conservative import; existing 12 reference regressions retained | Actual deployed parsers/Agent hosts and an approved real migration |

## Reproduction and CI

From repository root, no installation, credentials, network or services:

```sh
python3 -B scripts/test-release-workflow-v2.py
python3 -B scripts/test-release-contract-v2.py
python3 -B scripts/test-release-execution-v2.py
python3 -B scripts/test-release-consumers-v2.py
python3 -B scripts/check-stable-consumers.py
python3 -B scripts/test-stable-consumers.py
```

The four staged suites run 37 methods (11 reduced projections, 10 full-package
contracts, 13 local execution/recovery cases and 3 consumer cases). The historical
suite retains its 12 methods and fixed descriptors. Counts include unrelated
Findings compatibility tests in that historical suite; they are not 12 new release
acceptance cases. The `registry` job in `.github/workflows/lint.yml` now runs all
four staged suites alongside the existing historical checks. Local results do not
claim a hosted CI run. Final command results are in
[verification.json](verification.json).

## TDD evidence

The contract suite first failed because the full-package reader was absent;
the execution suite first failed because its test harness was absent; the consumer
suite failed for the missing explicit import. A field-list oracle initially read
the descriptive table instead of the record table; that test defect was corrected
rather than weakening the field assertion.

Additional observed red-to-green assertions covered missing selected artifacts,
receipt reuse after delivered-byte changes and candidate replacement, the legacy
helper's incorrect relationship enum, and completion without identity/evidence.
The reduced helper remains explicitly a historical projection; full-package tests
use formal `candidate_id`, `target_id`, `check_id` and `unchanged`/`transformed`
values directly. No adapter silently translates these fields.

## Re-review

The previous missing fixture, persistence and write-count evidence findings are
addressed within the offline scope. The Spec field-list check and full-package
reader now detect field and enum divergence in the supported subset. Consumer
admission tests are structurally before local mutation, and unknown/unverified
consumer entry is disabled. No actual product integration has been enabled.

Rule coverage for the offline review: `implementation-alignment-quality@1.2.0`
has `passed: [ALN-002, ALN-007]`, `waived: []`,
`not_applicable: [ALN-003 (no assigned technical design), ALN-005 (no production migration), ALN-006 (no completed task list)]`,
`evidence_limited: [ALN-001 (independent Skill execution), ALN-004 (actual consumer boundary)]`.
`testing-quality@1.4.0` has `passed: [TST-001, TST-002, TST-003, TST-005, TST-006, TST-007]`
for the declared offline seams, `waived: []`,
`not_applicable: [TST-008 (no numeric coverage policy)]`,
`evidence_limited: [TST-004 (actual supported consumer/runtime compatibility)]`.
No waiver converts the remaining integration limits into a pass.

## Next step

Use an explicitly authorized consumer sandbox and an independent Agent host to
exercise the existing Skills against these same outcomes before enabling a real
2.x integration. Record exact Skill/source versions, actual command discovery,
package outputs and mutation counts. Real-channel acceptance remains a separate
authorization and verification step; do not substitute this fixture journal for it.
