# plan-next: output guidance

## 3.3 Help the user choose

Use two short sections with headings by default in project-wide conversations. Give each distinct workstream or readiness group its own short bullet. Keep text under each heading easy to scan.

- **Project and pending work.** Open with a sentence or two connecting recent progress to the current goal or decision. Use bullets to show how the main pending work fits and which waits shape the choice. Roll up related paused or deferred work in plain language. Keep the full inventory available on request.
- **Do now.** Show the first one to three eligible actions in the current recommendation order. When at least two are visible, number them, explain why the first comes first, and say the user can reply with a number or action name. For genuine ties, explain the trade-off and state that the order is for display. Give each action a brief reason grounded in evidence and a completion marker. Name the skill or workflow when it helps the user start.

For a focused request, keep the summary within the inspected scope and lead with the recommendation or remaining condition. Use the same numbered format if multiple actions are eligible within that scope. A sole action can be a prose recommendation and counts as position 1. When no action is eligible, explain the remaining condition and who or what can resolve it. If more eligible actions exist beyond the display limit, tell the user they can ask to see the queue. When the user asks what to do in the next conversation, make the recommendation ready to copy with its target, source, completion marker and any stop point.

Explain only the upstream context needed to judge the action. Follow the project's declared goal and acceptance model. When a numeric criterion matters, use the threshold and evidence source under [roadmap quality](../../../rules/roadmap-quality.md); distinguish unknown from zero and identify a project-defined benchmark when no external one exists. A continuing strategic direction needs no invented completion KPI. An unrelated missing measurement does not displace an independently supported action.

Use the user's language and describe the work in terms the reader can understand without a glossary. Include a project ID only when it helps locate or distinguish an item, and place it after the descriptive name. Keep internal traversal codes and status values in the diagnostic basis. If urgency labels help, retain `urgent`, `important`, `defer`, `minor` and `awaiting execution`; these annotations alone do not determine recommendation order. Ready implementation work uses its existing project workflow or an awaiting-execution marker, without inventing a governance skill.

## 3.4 Continuation and handoff

Explain queue controls when the user asks how to change the recommendations or is reviewing the queue. “Next” skips the first displayed entry for this conversation. Ordinary skips with unspecified duration still require the user's duration choice. Resolve selectors against the latest displayed result before rescanning.

Report adjustments and their scope, then return the revised **Do now** list with fresh positions. Put active exclusions in **Skipped recommendations** before that list, including exact action names and durations. Explain reordered display as the user's conversation preference while retaining the actions' underlying rationale. Report stale moves that were dropped. An exhausted implicit focus triggers the read-only project scan in SKILL.md in the same reply. Name the original wait, blocker or exclusions separately from the resulting project recommendation, and state expanded coverage and limitations. An explicit scope limit instead retains local exhaustion and offers broader inspection. Neither path manufactures work.

A correction such as “that is not the main problem” revisits the question and ranking rationale before rebuilding candidates. A reported completion is revalidated against source closure criteria before it advances dependencies. Previously settled decisions and authorization remain effective unless superseded or conflicting evidence requires a specific clarification.

When the user selects an action, resolve it against the latest visible options before rescanning. Provide a ready-to-use handoff for the exact route if it remains eligible. Name the selected skill or project workflow, objective, concrete target, relevant source references, retained decisions, existing authorization and completion marker. If the route is stale, report the change and return the refreshed result without selecting a substitute. Keep unresolved business choices explicit. Selection alone adds no permission. The selected workflow or outer executor handles subsequent execution.

For a roadmap handoff, retain the established artifact language under the [Roadmap Spec](../../../specs/roadmap-modeling.md#57-deliverable-language-schema-15). Use the consuming project's evidence to identify any unresolved language choice that affects the handoff. Report actual language drift when it affects the decision and apply the user's language to the conversational reply.

## 3.5 Result and diagnostic basis

Compute `decision_state` as defined in [diagnosis](diagnosis.md#201-decision-state). For callers such as `orchestrate-governance-step`, retain the exact top-level state and the usual first one to three eligible candidates, with exact route keys, source evidence, prerequisites, blockers and authorization boundaries. Use plain language for the state in ordinary conversation. A focused result never establishes project-wide `complete`.

Keep the inspected evidence and decision basis available even when the reply is short. Give a detailed diagnostic basis when requested, when a material conflict needs it or when the caller consumes it. Include relevant paths, inspected scope and limits, prerequisites, exact candidate keys and applicable preferences. Use level, node, status and inference rows when a detailed project-wide report needs them. Project-wide inspection still covers all applicable goals and siblings. Include drift and hygiene in the short reply only if they affect the decision.

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
| A project code helps locate or distinguish the item and the dictionary has it | Use `full_name (code)`, for example `Coverage dashboard (T51)` |
| Later appearances within the same card | Reuse the descriptive name |
| The dictionary has no matching entry | Fall back to the source artifact's frontmatter `title:`, injecting the first ≤12 words |
| Both the dictionary and the fallback are missing | Mark it in the diagnostic-basis section as "dictionary miss: suggest adding `<code>` to `docs/glossary.md`", and **do not show that code in the user-facing sections**; use a generic description instead ("the task awaiting execution", say) |

**Constraints**:

- A missing dictionary is not an error and blocks nothing — the degraded output is still usable
- Use expanded names in user-facing recommendations and secondary findings; the diagnostic basis allows bare codes
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
- Stopping at an exhausted implicit focus to ask permission for read-only project diagnosis, overriding an explicit scope limit, or claiming whole-project exhaustion/completion from local evidence.
- Omitting a candidate's reason, evidence, completion marker or usable skill/workflow handoff.
- Hiding genuine ties or uncertainty behind invented scores, costs or priority labels.
- Showing unexplained project IDs, traversal jargon or empty template fields in the user-facing recommendation.
- Duplicating requirements for linked roadmap views, treating history as unfinished work, or requiring optional artifacts to fill a template.
