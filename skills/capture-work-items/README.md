# Capture Work Items

Captures a requirement, bug, or issue from free-form input and turns it into a structured, persisted backlog artifact.

## Purpose

This skill gives you a fast structured record without the deep validation that `review-requirements` performs. It converts a user-supplied description into a work item (requirement, bug, or issue) carrying every required field, and persists it to the path the project has agreed on. The output stays aligned with the project documentation structure (project-docs-template, for instance) and includes status tracking for governance.

## When to use

- The user says "log this bug" or "add this requirement" - structure and persist it without a full analysis
- Pull work items out of meeting notes or email and save them as structured artifacts
- Capture items so they can be triaged and prioritized later in milestones or task breakdowns
- Fill the backlog gaps identified in an assessment document

## Inputs

- The user's raw description of a requirement, bug, or issue
- Optional: project context (an existing "docs/" structure used for path detection)

## Outputs

- Structured work item Markdown with YAML front-matter
- Path: one file each, under "docs/process-management/project-board/backlog/" (canonical) or "docs/backlog/" (fallback)
- Types: requirement, bug, issue
- Status: starts at "captured" (downstream updates: triaged, in-progress, done, blocked, cancelled)

## Related skills

- `review-requirements`: deep validation, once the item has been written up as a requirements document. Interactive clarification of a vague item is not an AI Cortex skill — it belongs to the runtime
- Design exploration, where a captured item leads to an architecture decision, is carried by the runtime; AI Cortex supplies the shape in [specs/functional-design-modeling.md](../../specs/functional-design-modeling.md) and [specs/technical-design-modeling.md](../../specs/technical-design-modeling.md)

## Install

Handled centrally by the canonical AI Cortex install; see the repository root [README](../../README.md#-install-and-use).

## License

MIT
