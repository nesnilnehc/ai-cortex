---
artifact_type: technical-design
lifecycle: snapshot
created_at: 2026-10-20
parent: ../process-management/backlog/2026-10-20-roadmap-capabilities.md
status: approved
---

# Roadmap phases and milestone events

## 1. Goal

Separate roadmap, release grouping, duration-bearing phase and significant event,
with independent milestone identity, evidence and backwards-compatible rendering.

## 2. Architecture and service decomposition

| Component | Responsibility | Dependencies |
| --- | --- | --- |
| Roadmap Spec and quality Rule | Own meanings, relationships and evaluation | Research evidence; source records |
| Existing roadmap skills | Define, maintain, review and archive the appropriate object | Canonical Spec and Rule |
| Offline renderer | Validate and display explicit phase/event facts | Python standard library |
| Service Desk casebook | Demonstrate the same objects across retained snapshots | Sources and reproducible JSON inputs |

This extends a document-generation utility without a new application interface;
functional/UI design is skipped. The SVG retains its existing labeled lanes and
milestone diamonds. Existing adoption paths and destination authorization apply.

## 3. Components and detailed design

Keep the public `validate`, `markdown`, `mermaid` and `svg` functions. Extend
validation with phase and milestone helpers; collect names through one shared
record lookup. Render phase/event registers in Markdown, phase bars and distinct
milestone lanes in SVG/Mermaid. No timestamps or event occurrence are inferred.
The [roadmap Spec](../../specs/roadmap-modeling.md) owns exact fields.

## 4. Database design

No database change. Input remains transient rendering data. Source records are
canonical; examples retain explicit teaching snapshots, not multiple active plans.
No directory rename, deletion or automatic consumer migration is performed.

## 5. Interface contracts

CLI arguments and reserved output names stay unchanged. Accept JSON schema 1.0
unchanged. Schema 1.1 adds optional `phases` and `milestones` arrays with globally
unique IDs. Phase scopes reference entries/versions; milestone relations reference
entries/versions/phases, or an explicit empty relation list for a global event.
1.1 schedule spans reference entries/versions/phases; milestone points reference
milestone objects. 1.0's reused-record milestone presentation stays a legacy route.
A declared reached milestone needs evidence; only reached events may use actual
point timing. Missing dates remain unscheduled. All invalid references and temporal
constraints fail before writing outputs, as in the existing CLI.

## 6. Data flow and error handling

Verified facts → version-aware validation → relation and timing checks → one set
of generated views → SVG inspection and source-backed review.

- Missing relation, duplicate ID or wrong point/span kind: name the offending object,
  reject input and write nothing; correct facts rather than synthesizing records.
- Reached/actual event with no occurrence evidence: reject the claim; a target date
  is not evidence that approval or release happened.
- Legacy milestone directories: diagnose them as work-package containers. Preserve
  their existing archive route, maturity checks and apply gate; do not delete or
  migrate directories merely because terminology is clarified.

## 7. Technology choices and trade-offs

| Approach | Benefit | Cost | Decision |
| --- | --- | --- | --- |
| Optional 1.1 phase/event records | Explicit identity and relations; old inputs remain valid | Additional validation and registers | Selected |
| Reuse the version ID for every point | Minimal schema | Cannot represent a span and several independent events | Retain only for legacy 1.0 compatibility |
| Import a project-management platform | Rich scheduling and editing | New dependency and data authority | Not selected |

Research basis: [primary-source evidence](../references/roadmap-milestone-research.json).
PMI's inspected edition is from 2011, not a claim of current certification.
Microsoft's duration-bearing milestone flag is a tool-specific compatibility fact;
AI Cortex uses event points and keeps the preceding work as duration-bearing phases.

## 8. Test strategy

TDD: 1.1 independent points alongside a version span, relation/kind validation,
required occurrence evidence, unknown dates, date and week rendering; preserve
all 1.0 regression tests. Extend casebook tests to cross-check phase scope, event
relations/state/time against source tables, and perturb those facts. Inspect the
updated SVG lanes in a local browser. Run repository links, hygiene, versions,
index, findings and existing relevant checks; report remote-rendering limitations.

## 9. Acceptance criteria

- AC7: Public definitions distinguish the four concepts and separate optional
  associations from containment; preserve prior single-view and 1.0 inputs.
- AC8: A version span, phase span and several distinct evidence-backed milestone
  points coexist in Markdown, SVG and dated Mermaid without duplicated requirements.
- AC9: Planned dates never certify occurrence; null event dates remain explicit;
  invalid references/kinds/evidence fail with actionable errors.
- AC10: Skills, templates and Service Desk examples use the same relationships;
  archival preserves event evidence and unfinished work, including the legacy route.

## Quality attribute design

| Concern | Tactic | Trade-off | Verification | Owner |
| --- | --- | --- | --- | --- |
| Input/output safety | Reuse source-link and XML validation for every object | Restricted link syntax | Malformed-record tests | Renderer |
| Compatibility | Explicit 1.0/1.1 dispatch; no silent conversion | Two accepted input versions | Legacy regression tests | Renderer |
| Source-backed reporting | Require evidence for terminal milestone claims; never infer from dates | Upstream facts required | State/timing tests and casebook review | Skills and renderer |
