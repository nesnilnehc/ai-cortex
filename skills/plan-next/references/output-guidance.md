# plan-next: output guidance

## 3.3 Help the user choose

Begin with the current question, the inspected scope and the decisions being carried forward. Distinguish user decisions, verified source state and unresolved evidence. Name any conflict that changes which action is safe or worthwhile.

Use prose for one clear recommendation. For several meaningful alternatives or independently startable actions, use separate numbered entries. Usually recommend one action with up to two alternatives. Explain a focus, parallel or convergence choice when applicable. Explicit queue inspection can show more eligible entries after the usual **Do now** list.

Every recommendation answers four questions:

1. What action should the user take?
2. Why is it worth doing now, based on current evidence?
3. What benefit, cost or waiting condition distinguishes it from the other choices, when a comparison is relevant?
4. What observable result completes this step, and which skill or existing project workflow produces it?

Give each entry its own reason, evidence and completion marker. Separate actual parallel work from alternatives between which the user should choose. Do not manufacture alternatives, costs, rankings or empty fields. Genuine ties can be displayed in source order and then exact route-key order for stable browsing; describe the trade-off without implying a settled business priority.

Explain only the upstream context needed to judge the action. Follow the project's declared goal and acceptance model. When a numeric criterion matters, use the threshold and evidence source under [roadmap quality](../../../rules/roadmap-quality.md); distinguish unknown from zero and identify a project-defined benchmark when no external one exists. A continuing strategic direction needs no invented completion KPI. An unrelated missing measurement does not displace an independently supported action.

Use the user's language and plain action names. Introduce a project ID with its descriptive name. Keep internal traversal codes and status values in the diagnostic basis. If urgency labels help, retain `urgent`, `important`, `defer`, `minor` and `awaiting execution`; these annotations alone do not determine recommendation order. Ready implementation work uses its existing project workflow or an awaiting-execution marker, without inventing a governance skill.

## 3.4 Continuation and handoff

In an initial recommendation result, explain briefly that “next” skips its first entry for this conversation. With multiple entries, “put 2 first” may illustrate reordering. Ordinary skips with unspecified duration still require the user's duration choice. Resolve selectors against the latest displayed result before rescanning.

Report adjustments and their scope, then return the revised **Do now** list with fresh positions. Put active exclusions in **Skipped recommendations** before that list, including exact action names and durations. Explain reordered display as the user's conversation preference while retaining the actions' underlying rationale. Report stale moves that were dropped. An exhausted scope names the remaining blockers or exclusions and offers broader inspection; it does not silently manufacture more work.

A correction such as “that is not the main problem” revisits the question and ranking rationale before rebuilding candidates. A reported completion is revalidated against source closure criteria before it advances dependencies. Previously settled decisions and authorization remain effective unless superseded or conflicting evidence requires a specific clarification.

When the user selects an action, provide a ready-to-use handoff naming the selected skill or project workflow, objective, concrete target, relevant source references, retained decisions, existing authorization and completion marker. Keep unresolved business choices explicit. Selection alone adds no permission. The selected workflow or outer executor handles subsequent execution.

## 3.5 Result and diagnostic basis

Retain the existing top-level `decision_state` values for consumers. Use `actionable`, `needs_input`, `no_applicable_action` or `complete` as defined in [diagnosis](diagnosis.md#201-decision-state). A focused result states local completion separately and never emits project-wide `complete` from uninspected evidence.

For a simple recommendation, keep the explanation and evidence compact. For a complex result, the following outline is available; include only applicable sections. The technical basis can be brief but must identify the inspected scope, material evidence and limitations. A project-wide result records every applicable goal and its current position.

```text
Current question and inspected scope
Decisions carried forward, source conflicts and evidence limits
Decision state

Skipped recommendations, when active

Do now
1. Action, why now, relevant comparison, evidence, skill/workflow and completion marker
2. A meaningful alternative or independent action, when available

Also worth noting, when relevant
Findings outside the immediate choice and their evidenced effects

Diagnostic basis
Inspected source paths and status (present / placeholder / missing)
Scope not inspected
Exact candidate keys, exclusions and any user-directed order adjustments
Route blockers, their scope and independent candidates
Open decision and how its answer changes the recommendation, when needed

Level | Node | Status | Inference
Relevant decision rows only; project-wide scope covers every applicable goal

Drift and hygiene findings, or not inspected when outside scope
```

Use a four-column decision table for a complex diagnosis. Do not fill uninspected rows as passed or treat known historical records as current work. Drift and hygiene remain secondary unless their evidenced effect blocks the current choice. If no action remains, explain the waiting, evidence or preference condition and the available next decision.

### 3.7 Terminology dictionary lookup

**Purpose**: inject a natural-language subtitle for project codes automatically, so the user-facing output can be read on its own and no one has to consult an internal ID dictionary to understand it.

**Dictionary sources (in discovery order)**:

1. The `glossary_path` input parameter (when the caller supplies it)
2. `.ai-cortex/glossary.yaml`
3. `docs/glossary.md`
4. **Fallback**: read the source artifact's frontmatter `title:` field (the `title:` of `docs/tasks/T51.md`, say); with no frontmatter, take the first H1 heading

**Dictionary schema** (in YAML):

```yaml
T51:
  full_name: coverage dashboard task
  one_liner: lets the PM see coverage progress live
M5:
  full_name: milestone 5, "hybrid retrieval matures"
Goal 1:
  full_name: requirement clarification depends on the knowledge base running reliably
  kpi: adoption rate ≥70% for 14 consecutive days
```

**Field notes**:

- `full_name` (required): the natural-language name, used to inject the subtitle
- `one_liner` (optional): the core value in one sentence, usable to help generate the TL;DR card header
- `kpi` (optional, strategic goals only): a short statement of the core KPI

**Lookup rules at the output layer**:

| Situation | Rendering |
| --- | --- |
| A project code appears for the first time and the dictionary has it | Inject `code (full_name)`, for example `T51 (coverage dashboard task)` |
| Later appearances within the same card | The bare code only |
| The dictionary has no matching entry | Fall back to the source artifact's frontmatter `title:`, injecting the first ≤12 words |
| Both the dictionary and the fallback are missing | Mark it in the diagnostic-basis section as "dictionary miss: suggest adding `<code>` to `docs/glossary.md`", and **do not show that code in the user-facing sections**; use a generic description instead ("the task awaiting execution", say) |

**Constraints**:

- A missing dictionary is not an error and blocks nothing — the degraded output is still usable
- The dictionary lookup injects only into the "Do now" and "Also worth noting" sections; the diagnostic-basis section allows bare codes
- A malformed dictionary source YAML → HALT and ask the user to fix it (the same behavior as the norms resolution in §0)

---

## Anti-Patterns

- Calling downstream skills, repairing governance records or adding authorization while preparing a recommendation.
- Discarding a current decision because it is absent from disk, or treating a user's completion report as verified closure.
- Inventing a central problem without evidence linking it to the user's intended result.
- Promoting a missing document or metric merely because it is higher in the goal tree.
- Turning a route-specific uncertainty into a global blocker or bypassing a verified dependency, focus constraint or pause.
- Inferring parent completion solely from Git activity or child counts when the project requires independent closure evidence.
- Treating approval as execution completion, waiting as done, or a continuing direction as a finite goal.
- Substituting a dependent route for a skipped prerequisite or filling an empty list with invented work.
- Persisting a skip without explicit duration, guessing an ambiguous selector, or reporting a failed preference write as successful. “Next” explicitly selects conversation scope.
- Carrying session skips or moves into a new conversation, or silently dropping persistent preferences.
- Treating a user-directed display order as a changed project priority.
- Silently broadening an exhausted focused scope or claiming whole-project completion from local evidence.
- Omitting a candidate's reason, evidence, completion marker or usable skill/workflow handoff.
- Hiding genuine ties or uncertainty behind invented scores, costs or priority labels.
- Showing unexplained project IDs, traversal jargon or empty template fields in the user-facing recommendation.
- Duplicating requirements for linked roadmap views, treating history as unfinished work, or requiring optional artifacts to fill a template.
