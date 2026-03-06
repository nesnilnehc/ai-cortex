# Artifact Norms Schema

Status: Informational  
Version: 1.0.0  
Scope: Project-level artifact path and naming configuration.

---

## 1. Purpose

Projects may define their own artifact norms to override the default [spec/artifact-contract.md](artifact-contract.md). Skills that produce document artifacts read project norms first; if none exist, they fall back to the contract.

---

## 2. Resolve Order

Skills check in order:

1. `.ai-cortex/artifact-norms.yaml` (machine-readable, preferred for automation)
2. `docs/ARTIFACT_NORMS.md` (human-readable)
3. If neither exists: use [spec/artifact-contract.md](artifact-contract.md) as default

---

## 3. docs/ARTIFACT_NORMS.md Format

Minimum structure (Markdown):

```markdown
# Artifact Norms

**Source**: Custom | AI Cortex default | project-documentation-template

## Artifact Types

| artifact_type | path_pattern | naming | lifecycle |
| :--- | :--- | :--- | :--- |
| backlog-item | docs/... | YYYY-MM-DD-{slug}.md | living |
| design | docs/... | YYYY-MM-DD-{topic}.md | snapshot |
| adr | docs/... | YYYYMMDD-{slug}.md | living |
| doc-readiness | docs/calibration/ | YYYY-MM-DD-doc-readiness.md | snapshot |

## Path Detection (backlog-item, optional)

| Condition | Output path |
| :--- | :--- |
| docs/process-management/ exists | docs/process-management/project-board/backlog/YYYY-MM-DD-{slug}.md |
| Otherwise | docs/backlog/YYYY-MM-DD-{slug}.md |
```

---

## 4. .ai-cortex/artifact-norms.yaml Format

YAML structure compatible with [artifact-contract Appendix A](artifact-contract.md#appendix-a-machine-readable-schema-for-verify-artifact-contract):

```yaml
artifact_types:
  backlog-item:
    path_patterns:
      - "docs/process-management/project-board/backlog/YYYY-MM-DD-{slug}.md"
      - "docs/backlog/YYYY-MM-DD-{slug}.md"
    naming: "YYYY-MM-DD-{slug}.md"
    lifecycle: living
  design:
    path_patterns:
      - "docs/design-decisions/YYYY-MM-DD-{topic}.md"
    naming: "YYYY-MM-DD-{topic}.md"
    lifecycle: snapshot
  adr:
    path_patterns:
      - "docs/process-management/decisions/YYYYMMDD-{slug}.md"
    naming: "YYYYMMDD-{slug}.md"
    lifecycle: living
  doc-readiness:
    path_patterns:
      - "docs/calibration/YYYY-MM-DD-doc-readiness.md"
    naming: "YYYY-MM-DD-doc-readiness.md"
    lifecycle: snapshot
```

---

## 5. Skill Behavior

When a skill needs to write a document artifact:

1. **Resolve project norms**: Check for `.ai-cortex/artifact-norms.yaml` or `docs/ARTIFACT_NORMS.md`.
2. **Parse**: Extract path_pattern and naming for the relevant artifact_type.
3. **Apply**: Use project norms if found; otherwise use [spec/artifact-contract.md](artifact-contract.md) defaults.
4. **Write**: Persist to the resolved path with the correct naming.
