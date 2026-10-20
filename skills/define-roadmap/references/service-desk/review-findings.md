# Service Desk roadmap review

Finished review output for the [deliberately faulty candidate](problematic/roadmap.md),
using the [W0 source state](sources.md#execution-by-stage), not later delivery facts.
This fictional review reports two defects; it is not an acceptance or release receipt.
Finding structure follows [findings-list](../../../../specs/findings-list.md).

## Findings

### Unsupported completion

- **Location**: [problematic roadmap, Requirements](problematic/roadmap.md#requirements), BUG1 execution cell.
- **Category**: roadmap-quality.
- **Severity**: critical.
- **Maturity**: ready.
- **Description**: BUG1 is labeled Completed, but its W0 source says In progress,
  with required acceptance and production release pending. The label could wrongly
  permit dependent work to proceed; it violates roadmap-quality §4 source-backed
  closure and §1 execution-status boundaries.
- **Suggestion**: Restore In progress from the source, retain the acceptance/release
  condition and verify closure before a later completion transition.

### Dependency timing conflict

- **Location**: [problematic roadmap, Schedule](problematic/roadmap.md#schedule), V2 span.
- **Category**: roadmap-quality.
- **Severity**: major.
- **Maturity**: ready.
- **Description**: V2 depends on V1 finishing at boundary W3, but starts at W2.
  Its schedule also disagrees with its W3–W4 version target. This violates
  roadmap-quality §6 dependency timing and cross-view agreement.
- **Suggestion**: Restore V2's start to W3 and keep the requirement/version/schedule
  references aligned. Do not silently remove the dependency to make dates fit.

## Evaluation coverage and limits

Completeness, executability, clarity, soundness and traceability were examined
against the finite source records, together with selected-view agreement. A reader
can identify BUG1 as the current priority, R1/R2 as subsequent work and the pending
acceptance chain as the key condition. All four items have stable source links.
Version groups are valid; the absence of detailed task rows is not a defect.

Change-frequency compliance: **cannot evaluate**; the fictional project defines
no threshold/window or history. External publication: not applicable; delivery is
local. No production environment was inspected, and no real release is certified.
The review has findings and an unevaluated frequency criterion, so it is not a pass.

## Handoff and corrected result

Status and dates route to `update-roadmap`. The [corrected W0 candidate](initial/roadmap.md)
and its [Gantt chart](initial/roadmap.svg) show both fixes. Its inputs validate and
reproduce those outputs. The subsequent W1 sandbox failure is a different event,
handled by the [change record](change-record.md); it is not hidden in this correction.
