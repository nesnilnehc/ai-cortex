# capture-work-items

Capture requirements, bugs, or issues from free-form input into structured, persistent backlog artifacts.

## What it does

This skill provides quick structured recording without the deep validation that `analyze-requirements` performs. It transforms user-provided descriptions into work items (requirement, bug, or issue) with all required fields and persists them to the project-convention path. Output aligns with project documentation structure (e.g. project-documentation-template) and includes status tracking for governance.

## When to use

- User says "record this bug" or "add this requirement" — structure and persist without full analysis
- Extract work items from meeting notes or email and save as structured artifacts
- Capture items for later triage and prioritization in milestones or task breakdown
- Fill the Backlog gap identified in assess-documentation-readiness

## Inputs

- Raw description of requirement, bug, or issue from user
- Optional: project context (existing `docs/` structure for path detection)

## Outputs

- Structured work item Markdown with YAML front-matter
- Path: `docs/process-management/project-board/backlog/` (canonical) or `docs/backlog/` (fallback) per spec/artifact-contract.md
- Types: requirement, bug, issue
- Status: initial `captured` (downstream updates: triaged, in-progress, done, blocked, cancelled)

## Related skills

- `analyze-requirements`: Deep validation when item is vague and needs clarification
- `brainstorm-design`: Design exploration when captured item leads to architecture decisions

## Installation

```bash
npx skills add nesnilnehc/ai-cortex --skill capture-work-items
```

## License

MIT
