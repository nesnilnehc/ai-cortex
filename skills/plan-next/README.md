# Plan Next

Recommend the next useful action from the user's current problem, settled decisions and project evidence. Compare choices and prepare a focused skill handoff.

## How it works

1. Establish the current question and intended result from the request and conversation. A bare invocation continues identifiable current work. An explicit project-wide request, or no usable context, selects whole-project diagnosis.
2. Check relevant records, decisions, dependencies and acceptance evidence, following the project's conventions. Broaden inspection only where the evidence affects the choice.
3. Recommend eligible actions that resolve current blockers, then continue selected or active work, then follow recorded project priorities. Explain genuine ties and meaningful alternatives.
4. When the user selects an action, prepare its skill or project-workflow handoff with the objective, target, evidence, retained decisions, authorization and completion marker.

A missing document or metric is a first action only when it affects the current decision or safe progress. Continuing strategic directions follow the project's own meaning and need no invented completion KPI. The response distinguishes current user decisions, verified project state and unresolved evidence, and states its inspected scope.

## What the user gets

One recommendation is enough when the next step is clear. Up to two alternatives may help a real choice or identify independent work. Each entry explains what to do, why now, its relevant trade-off, and what result and skill/workflow complete the step. Project-wide diagnosis remains available by asking for the whole project's next actions.

A focused result does not establish whole-project completion. An exhausted scope reports waiting conditions or exclusions and offers broader inspection. Relevant document drift and hygiene findings remain secondary unless they block the current choice.

## Adjust recommendations across replies

- “Next” skips the first displayed recommendation for this conversation and returns the revised result.
- “Put 2 first” changes the conversation's display order among eligible actions; underlying priorities and dependencies retain their meaning.
- “Show the queue” shows additional eligible entries beyond the usual one-to-three display limit.
- “Refresh” rechecks evidence. A reported completion is verified before advancing dependencies.
- “That is not the main problem” revisits the question and ranking rationale before rebuilding the recommendations.
- “Reset recommendation order” clears conversation moves while keeping skip choices.

An ordinary skip without an explicit duration asks whether to omit it for this conversation or until restored in this project. Session choices stay in the conversation. An explicit persistent choice writes only the exact `(route, target)` exclusion to `.ai-cortex/plan-next.yaml` under the [preference Spec](../../specs/plan-next-preferences.md).

“Recommend this again” removes the exact route from every active exclusion scope. Restoration does not make a blocked or paused action eligible. Invalid preference files, failed writes, stale selectors and dropped moves are reported. A new conversation starts with default display order and no session skips; persistent exclusions remain effective.

## Boundaries and automation

Ordinary diagnosis is read-only. Persistent skip/restore may change only the preference file. Pausing a task, changing roadmap placement or revising project priorities follows the workflow owning that record. A conversation decision can guide recommendations before its source is synchronized; conflicts are made explicit.

Plan Next prepares the selected handoff. The downstream skill or outer executor performs authorized work. Calling this skill grants no additional implementation or external-write permission.

- `/plan-next` diagnoses current work or the requested project scope.
- `/loop /plan-next 30m` schedules repeated diagnosis where the host supports `/loop`.
- `/loop /orchestrate-governance-step 30m` combines scheduling with the existing single-action executor. An internal invocation without current-work context uses project-wide diagnosis.

For a known single action, invoke its dedicated skill directly. Document-health checks remain with runtime/linter/CI tooling under `rules/doc-health-criteria.md`.

## Version 16 compatibility

Version 16 changes the default from an unconditional project scan to context-led recommendations, and replaces mandatory strategic-KPI-first routing with evidence relevant to the current choice. Explicit project-wide diagnosis, exact preference keys and existing decision-state values remain supported. A focused result uses `no_applicable_action` when locally exhausted; only verified project-wide closure can produce `complete`.
