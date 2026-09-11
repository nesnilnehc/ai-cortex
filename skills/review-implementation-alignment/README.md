# Review Implementation Alignment

**Status**: Experimental

## Purpose

Executes the canonical [implementation alignment quality Rules](../../rules/implementation-alignment-quality.md) over an implemented change, comparing approved requirements, designs and tasks with the production code and the verification evidence. It is the post-coding functional gate, and it exists to catch what a file-by-file review and an implementation-shaped test suite both miss: an acceptance criterion never implemented, behaviour added outside the approved scope, a field dropped between layers, code built but never wired to a production call path, and a task marked done with nothing behind it.

## When to use

- Functional gate after coding: paired with test or acceptance execution, as the sibling of the engineering gate.
- Green-but-wrong suspicion: the tests pass and the change still does not do what was approved.
- Completion audit: tasks are marked done and the evidence for each claim needs checking.

## Inputs

- Approved artifact paths (requirement, functional design, technical design, task list).
- The implementation diff or code scope, plus whatever verification evidence exists.

## Outputs

- Findings list: location, category=`cognitive-alignment`, severity, title, description, optional suggestion; each finding cites the alignment Rule ID it failed.
- Rule coverage metadata separating passed, waived, not-applicable and evidence-limited IDs.

## Ecosystem

| Field | Value |
| :------------------------------------ | :------------------------------------------------------------------------------------------ |
| overlaps_with (owner/repo:skill-name) | nesnilnehc/ai-cortex:orchestrate-code-review, nesnilnehc/ai-cortex:review-testing, nesnilnehc/ai-cortex:automate-tests |
| market_position | differentiated |

## Full definition

See [SKILL.md](./SKILL.md) for execution and boundaries; the criteria live only in [implementation-alignment-quality.md](../../rules/implementation-alignment-quality.md).
