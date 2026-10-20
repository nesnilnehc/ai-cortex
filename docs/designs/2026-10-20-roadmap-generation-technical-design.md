---
artifact_type: technical-design
lifecycle: snapshot
created_at: 2026-10-20
parent: ../process-management/backlog/2026-10-20-roadmap-capabilities.md
status: approved
---

# Local roadmap generation

## 1. Goal

Generate consistent roadmap views from verified planning facts without a new
planning authority, external renderer or synchronization service.

## 2. Architecture and service decomposition

| Component | Responsibility | Dependency |
| --- | --- | --- |
| Roadmap skills | Gather evidence, choose views and destination, inspect results | Project records; canonical Spec and Rule |
| Local generator | Validate once, render all requested views | Python standard library only |
| Destination adapter | Save local files or use authorized connector operations | Existing runtime capabilities; no bundled network code |

Functional design is skipped for the local document-generation utility: no app
interface or new interactive screen is introduced. Output SVG uses the existing
document/diagram presentation pattern.

## 3. Components and detailed design

The skill bundles `scripts/render-roadmap.py`. Its callable functions are
`validate(data: dict) -> dict`, `markdown(data: dict) -> str`,
`mermaid(data: dict) -> str`, and `svg(data: dict) -> str`.
Validation precedes rendering or filesystem mutation. Renderers consume the same
validated facts and never compute priorities or infer dates. The exact input
contract is defined in [roadmap modeling](../../specs/roadmap-modeling.md).

## 4. Database design

No database change. Input JSON is a temporary build input. Existing adopting
project records remain authoritative; generated views are presentation outputs.

## 5. Interface contracts

CLI: `python3 <skill-dir>/scripts/render-roadmap.py INPUT.json --output-dir DIR`.
`--check` validates without writing and does not require an output directory.
`--overwrite` permits replacement of the fixed generated filenames only.
Exit 0 means success; exit 1 reports invalid input or an I/O failure to stderr.
No authentication or network endpoint is introduced. The calling skill confirms
destination and scope before invoking a write.

## 6. Data flow and error handling

Verified project facts → temporary input → validation → render strings → chosen
output directory → visual inspection → delivery receipt.

- Invalid JSON, references, cycles or time ranges: report the offending field or ID,
  exit nonzero and write nothing; the caller corrects the facts before retrying.
- Existing generated file without overwrite permission: report the collision before
  writing. An I/O failure is explicit; never claim complete delivery. Report any
  partially written files for recovery.
- Missing platform rendering/upload support: deliver verified local outputs and
  state the platform limitation; do not install or silently change destination.

## 7. Technology choices and trade-offs

| Choice | Benefit | Cost | Decision |
| --- | --- | --- | --- |
| Python XML/SVG and JSON | Offline, reviewable, no extra packages | Maintain a small renderer | Selected |
| Mermaid CLI | Mature renderer | Requires an extra installed runtime | Not a mandatory dependency |
| Manual spreadsheet | Familiar editing | Harder to reproduce and compare | Remains a user-selected presentation, not generator authority |

## 8. Test strategy

TDD with unittest: JSON validation, references/cycles, time modes, escaping,
deterministic output and CLI collision behavior. Integration checks parse SVG XML
and inspect cross-view references. Inspect rendered short/long label examples in a
browser; check narrow viewing and text layout. No live Yuque write is required.

## 9. Acceptance criteria

- Contract and existing single-view compatibility are documented. Covers AC2.
- Dated and relative-week examples produce consistent readable outputs. Covers AC4.
- Invalid inputs and collisions fail explicitly without false delivery claims. Covers AC4–AC6.
- Skills and guide distinguish formats, destinations and authority. Covers AC1, AC3, AC5.

## Quality attribute design

| Source | Rule concern | Tactic | Trade-off | Verification | Owner |
| --- | --- | --- | --- | --- | --- |
| AC4 | Untrusted input and output safety | Validate IDs/links; XML-escape labels; fixed output names | Restricted link schemes and identifiers | Malformed input and escaping tests | Generator |
| AC6 | Bounded work | Limit input size and item count | Large plans must be split | Boundary tests | Generator |
| AC5 | External-action boundaries | Keep connectors outside generator | Manual runtime handoff | Skill review | Calling agent |
