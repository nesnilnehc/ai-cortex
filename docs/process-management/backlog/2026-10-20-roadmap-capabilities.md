---
artifact_type: backlog-item
created_by: capture-work-items
lifecycle: living
type: requirement
date: 2026-10-20
status: done
priority: unset
strategic_goal_id: goal-2
source: user
---

# Make roadmap capabilities understandable and usable

## Problem / Need

Adopters need to understand which roadmap capabilities AI Cortex provides, what
they produce, and how requirement arrangement, version scope and scheduling fit
together. Planning must respect project priority policies and an explicitly chosen
delivery destination. Goal mapping is inferred from the governance capability
defined in [Goal 2](../../project-overview/strategic-goals.md#goal-2-governance-chain-capabilities-are-available).

## Acceptance Criteria

- [x] AC1: The public guide explains scenarios, skills, governing assets, deliverables,
  three presentation forms, formats, destinations and capability limits.
- [x] AC2: A shared roadmap contract supports optional version and schedule views,
  preserves approval/execution separation, and accepts existing single-view plans.
- [x] AC3: Priority policy application preserves settled priorities; full four-framework
  reassessment is explicit. Requirement priority vocabulary includes P3.
- [x] AC4: A standard-library local tool validates structured input and generates
  Markdown, SVG and, for dated schedules, Mermaid without automatic scheduling.
- [x] AC5: Skills agree on ownership, destination choice, source evidence and updating
  all selected views. No cross-platform synchronization or runtime downloads occur.
- [x] AC6: Behavioral tests, rendered SVG inspection and relevant repository checks
  pass, with unavailable platform checks reported explicitly.

## Delivery plan

User-authorized implementation; capture status and priority are not approval fields.
The existing project roadmap remains authoritative; this work serves its Now
governance-capability direction without rewriting unrelated milestones.

| Step | Work | Points | Progress |
| --- | --- | --- | --- |
| 1 | Publish the capability guide and navigation | 5 | Done |
| 2 | Define the shared multi-view and generator contracts | 5 | Done |
| 3 | Align priority and roadmap skills | 8 | Done |
| 4 | Build and test the local generator | 8 | Done |
| 5 | Inspect outputs and run repository checks | 5 | Done |

## Implementation boundaries

Recommend all three views at first creation and let the user choose. Confirm a new
destination; reuse an established selection during maintenance. Temporary JSON is
a generation interface, not a second planning authority. Use relative weeks when
the start date is unknown. Do not copy private reference content into examples.
No commit, push, installation update or remote publication is included.

Implementation detail: [technical design](../../designs/2026-10-20-roadmap-generation-technical-design.md).

## Verification evidence

- `python3 scripts/test-roadmap-renderer.py`: 19 tests passed. Red failures were
  observed before implementation, including XML control characters, the last
  supported date and missing direction/rationale output; targeted fixes went green.
- Browser inspection: relative-week example and dated Chinese long-label SVG opened
  successfully; spans, dependency arrows, labels and unscheduled work were inspected
  at the desktop viewport. No narrow-screen or assistive-technology audit is claimed.
- Public illustration is reproducible from the shipped JSON example.
- Markdown lint, relative links, document hygiene, asset counts, findings contract,
  cortex command documentation, skill index and whitespace checks passed.
- Modeled Rule validation, Rule scenarios and the existing mutation suite passed.
- Working-tree version comparison checked 12 changed/new versioned assets; the
  standard tag-range version check also passed, covering its declared committed range.
- Static contract walkthroughs checked policy application versus reassessment,
  single-view compatibility, tier/version separation, destination reuse and archive
  carryover. These are document reviews, not live-model behavioral evaluations.

### Capability version decisions

| Skill | Version | Changed responsibility / rationale |
| --- | --- | --- |
| `define-roadmap` | 7.1.0 | Inputs, procedure and delivery: select views/destination and render locally; additive capability. |
| `review-roadmap` | 3.2.0 | Procedure and Self-Check: evaluate selected views and destination evidence; additive checks. |
| `update-roadmap` | 3.1.0 | Scope, persistence and Self-Check: existing-version membership and cross-view refresh; additive maintenance. |
| `promote-roadmap-items` | 3.2.0 | Inputs and persistence: accept policy priorities and preserve version/time facts; additive clarification. |
| `prioritize-backlog` | 3.0.0 | Modes, procedure and references: policy application is the default and full reassessment is explicit; major behavior change. |
| `capture-work-items` | 2.2.0 | Priority handoff: suggest policy application or assessment without forcing batch scoring; additive interaction change. |
| `orchestrate-roadmap-planning` | 2.2.0 | Routing: preserve mode intent, selected views and archive target kinds; additive orchestration. |
| `archive-milestone` | 1.3.0 | Version/year route and conditional checks: preserve unfinished carryover without inventing directories; additive route. |
| `plan-next` | 15.3.0 | Diagnosis adapter: recognize version/schedule views without duplicating requirements; additive diagnosis. |

## Delivery limitations and exclusions

Yuque writes, image uploads and target-platform Mermaid rendering were not executed;
no compatible Mermaid renderer was present in this environment. Those remain
conditional destination checks, not claims of connected publication. No cross-platform
sync, resource scheduler, PNG/PDF exporter, commit, push or installation update was
performed. Existing unrelated working-tree changes were retained.

## Filled deliverable examples

- [x] Publish a single [Service Desk casebook](../../../skills/define-roadmap/references/service-desk/README.md)
  with four consistent IDs and source-backed initial, adjusted and after-delivery snapshots.
- [x] Provide filled priority, dependency, placement, review, change and archive outputs.
- [x] Separate the intentionally faulty candidate from valid generated roadmaps and
  show both correction and the independent sandbox-blocking event.
- [x] Point the input example to the casebook's canonical initial input through a
  relative compatibility symlink;
  link producing skills and the public guide to their finished outputs.
- [x] Verify regenerated Markdown/SVG, source anchors, policy/graph agreement,
  membership/timing/status, drift detection and unfinished-item destinations in CI.

Verification: 22 renderer tests and 7 casebook tests pass. Additional renderer
checks distinguish unscheduled items from unverified dependency edges and ensure
key conditions link to source evidence. Version window labels cover targets,
commitments and actual timing. These are local fictional examples; no remote
publication, live release or model-based end-to-end evaluation is claimed.

The producing skills receive minor version bumps for the worked examples and
entry links. The earlier delivery's recorded versions and test counts remain
its verification facts, rather than being rewritten as a new release record.

## Phase and milestone implementation

Design and research: [implementation design](../../designs/2026-10-20-roadmap-events-technical-design.md),
[primary-source evidence](../../references/roadmap-milestone-research.json).

| Step | Work | Points | Progress |
| --- | --- | --- | --- |
| 1 | Define roadmap, version, phase and event relations and compatibility | 5 | Done |
| 2 | Extend the offline generator with independent phase/event objects | 8 | Done |
| 3 | Align creation, maintenance, diagnosis and archive skills | 5 | Done |
| 4 | Migrate examples, inspect rendering and verify contracts | 5 | Done |

- [x] AC7: Definitions and relations are consistent; 1.0 inputs and existing single-view plans remain valid.
- [x] AC8: Version/phase spans coexist with independent approval and release events.
- [x] AC9: Event occurrence requires source evidence, with explicit unknown timing and actionable invalid-input errors.
- [x] AC10: Skills, templates, archive routes and examples share the model without directory migration or evidence loss.

### Phase/event verification

- Roadmap Spec 1.1.0 defines four concepts, optional relations, evidence and explicit
  JSON 1.0/1.1 compatibility; the quality Rule is 4.2.0.
- Extended generator tests were first run red against schema 1.0, then implemented
  and run green. Final checks cover 28 renderer tests and 8 casebook tests, including
  independent version/phase spans, multiple event points, dated Mermaid, global and
  unscheduled events, evidence/state validation, legacy compatibility and drift.
- Initial, adjusted and after-delivery examples reproduce their Markdown/SVG; the
  deliberately invalid example withholds SVG. Public illustration matches initial.
- Browser inspection of adjusted and after-delivery SVG confirms distinct lanes,
  same-time acceptance/release points and target/actual plus planned/reached labels.
  Inspection prompted moving event state out of wrapped names into timing labels.
- Definition, update, review, promotion, orchestration, diagnosis and archive skills
  follow the same model. Legacy archive maturity and cleanup stay on their existing
  work-package route; the general route preserves independent event evidence.
- No automatic input/directory migration, remote publication or source evidence
  deletion was performed. Destination-specific rendering remains unverified.

| Updated capability | Version |
| --- | --- |
| define-roadmap | 7.3.0 |
| update-roadmap | 3.3.0 |
| review-roadmap | 3.4.0 |
| promote-roadmap-items | 3.4.0 |
| orchestrate-roadmap-planning | 2.3.0 |
| plan-next | 15.4.0 |
| archive-milestone | 1.5.0 |

These are additive model/route clarifications with explicit legacy compatibility.
The earlier verification and version tables above retain their historical scope.
