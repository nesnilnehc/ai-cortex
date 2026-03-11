# Artifact Norms

**Source:** AI Cortex project override

These norms define the single authoritative location for generated artifacts. Unless the user explicitly requests a snapshot, skills should overwrite the canonical file at the paths below.

## Artifact Types

| artifact_type | path_pattern | naming | lifecycle |
| :--- | :--- | :--- | :--- |
| backlog-item | docs/process-management/backlog/YYYY-MM-DD-{slug}.md | YYYY-MM-DD-{slug}.md | living |
| adr | docs/process-management/decisions/YYYYMMDD-{slug}.md | YYYYMMDD-{slug}.md | living |
| design | docs/designs/YYYY-MM-DD-{topic}.md | YYYY-MM-DD-{topic}.md | snapshot |
| doc-readiness | docs/calibration/doc-readiness.md | doc-readiness.md | living |
| planning-alignment | docs/calibration/planning-alignment.md | planning-alignment.md | living |
| architecture-compliance | docs/calibration/architecture-compliance.md | architecture-compliance.md | living |
| cognitive-loop | docs/calibration/cognitive-loop.md | cognitive-loop.md | living |
| repair-loop | docs/calibration/repair-loop.md | repair-loop.md | living |

## Path Detection (backlog-item)

| Condition | Output path |
| :--- | :--- |
| docs/process-management/ exists | docs/process-management/backlog/YYYY-MM-DD-{slug}.md |
