# plan-next: output guidance

## 3.3 Help the user choose

Write for someone returning to the project after a long absence. Give them the first two layers in the default reply, with the key evidence beside the conclusion it supports. Expand the third layer when the reader asks or when evidence conflicts in a way that could change the choice. Use as much explanation as the reader needs to follow the reasoning.

1. **Where things stand.** In plain language, say what the project helps people do, which outcome the current work serves, and what has been verified or is still open. If the reader's last known checkpoint is established, explain the changes from that checkpoint that matter now. Otherwise give the latest verified state and dates that help locate it. Distinguish work merely recorded or implemented from work tested or released when that affects the choice. Close the overview with the first recommendation, the reason work must wait and who or what can unblock it, or the verified conclusion that work is complete.
2. **Do now.** Explain how the current state leads to the recommended action. Show the first one to three eligible actions in order. For each, say how to start and what result would show it worked. When showing multiple actions, use selectable numbers for the actions and tell the reader they can reply with a number or action name. Explain why the first comes first, including what changes if the reader chooses another realistic path. For genuine ties, explain the trade-off and state that the order is for display. Name the skill or workflow when it helps the user start.
3. **Evidence.** In the default reply, attach the few sources that establish the current state or explain the choice. State what they verified and disclose any gap or disagreement that could change the next step. On expansion, use [the diagnostic basis](#35-result-and-diagnostic-basis) to show what was checked, what the evidence establishes, and how it led to the recommendation.

For a focused request, use the same reading order and give only the project context needed to understand the inspected work. A sole action can be a prose recommendation and counts as position 1. When no action is eligible, use the overview to explain the remaining condition. During a follow-up where the reader already has the overview, bring forward the context that changed or affects the choice. If more eligible actions exist beyond the display limit, tell the user they can ask to see the queue. When the user asks what to do in the next conversation, make the recommendation ready to copy with its target, source, completion marker and any stop point.

Make the explanation understandable before the reader opens a source. Describe what someone is trying to do, what usually happens, and what changed or is in doubt. Connect that situation to the recommended step by saying what question it answers or what problem it resolves. Use a concrete example or a simple sequence when it helps the reader see that connection.

Say what to do first and what the reader would see if it works. If a detail changes the action, the outcome, or how certain the recommendation is, explain it in place. If another step needs evidence, access or a decision, say what it is waiting for outside **Do now** and explain why the first step can still proceed. Distinguish finding a fix or a test in the repository from verifying its result. Link directly to the evidence after explaining what it shows.

For example, when a fix and test inputs are available but older records still need access:

> **Where things stand.** The app lets teams agree on work in a conversation and turn it into a tracked task. The team is working on making the result of an approval visible. A fix for missing activity records is now in the main branch. The next step is to verify how the current version behaves when you approve again.
>
> **Do now.** When you click “Create task,” the system creates the task and records what it did in the conversation. If the record is blank, you cannot tell whether the task already exists. Clicking again might create a duplicate. In the test environment, create a task while making the record save fail, then retry the same approval. The check passes when the conversation shows the record and the task list still contains exactly one new task.
>
> The test answers how the current version behaves. To find out what happened in earlier cases, someone with access needs to provide redacted copies of the old records.

Include the project background needed to locate the current decision and judge the action. Explain any earlier decision that still shapes the choice. Follow the project's declared goal and acceptance model. When a numeric criterion matters, use the threshold and evidence source under [roadmap quality](../../../rules/roadmap-quality.md); distinguish unknown from zero and identify a project-defined benchmark when no external one exists. A continuing strategic direction needs no invented completion KPI. An unrelated missing measurement does not displace an independently supported action.

Use the user's language and the words people see when doing the work, such as the name of a button or the result they expect. Explain any necessary technical term through what it means in this situation when it first appears. Include a project ID only when it helps locate or distinguish an item, and place it after the descriptive name. Keep internal traversal codes and status values in the diagnostic basis. If urgency labels help, retain `urgent`, `important`, `defer`, `minor` and `awaiting execution`; these annotations alone do not determine recommendation order. Ready implementation work uses its existing project workflow or an awaiting-execution marker, without inventing a governance skill.

## 3.4 Continuation and handoff

Explain queue controls when the user asks how to change the recommendations or is reviewing the queue. “Next” skips the first displayed entry for this conversation. Ordinary skips with unspecified duration still require the user's duration choice. Resolve selectors against the latest displayed result before rescanning.

Report adjustments and their scope, then return the revised **Do now** list with fresh positions. Put active exclusions in **Skipped recommendations** before that list, including exact action names and durations. Explain reordered display as the user's conversation preference while retaining the actions' underlying rationale. Report stale moves that were dropped. An exhausted implicit focus triggers the read-only project scan in SKILL.md in the same reply. Name the original wait, blocker or exclusions separately from the resulting project recommendation, and state expanded coverage and limitations. An explicit scope limit instead retains local exhaustion and offers broader inspection. Neither path manufactures work.

A correction such as “that is not the main problem” revisits the question and ranking rationale before rebuilding candidates. A reported completion is revalidated against source closure criteria before it advances dependencies. Previously settled decisions and authorization remain effective unless superseded or conflicting evidence requires a specific clarification.

When the user selects an action, resolve it against the latest visible options before rescanning. Provide a ready-to-use handoff for the exact route if it remains eligible. Name the selected skill or project workflow, objective, concrete target, relevant source references, retained decisions, existing authorization and completion marker. If the route is stale, report the change and return the refreshed result without selecting a substitute. Keep unresolved business choices explicit. Selection alone adds no permission. The selected workflow or outer executor handles subsequent execution.

For a roadmap handoff, retain the established artifact language under the [Roadmap Spec](../../../specs/roadmap-modeling.md#57-deliverable-language-schema-15). Use the consuming project's evidence to identify any unresolved language choice that affects the handoff. Report actual language drift when it affects the decision and apply the user's language to the conversational reply.

## 3.5 Result and diagnostic basis

Compute `decision_state` as defined in [diagnosis](diagnosis.md#201-decision-state). For callers such as `orchestrate-governance-step`, retain the exact top-level state and the usual first one to three eligible candidates, with exact route keys, source evidence, prerequisites, blockers and authorization boundaries. Use plain language for the state in ordinary conversation. A focused result never establishes project-wide `complete`.

Keep the inspected evidence and decision basis available. “Show the evidence” requests the basis for the last displayed result. For “Why option 2?”, use the latest displayed **Do now** positions. For a request by name, use the matching displayed action. If the action is unclear, ask which one to explain. If there is no prior result, say that a fresh diagnosis would supply one. Keep the options and their order while explaining what the sources say, which conclusion follows, and which checks are still open. A request to refresh rechecks current evidence under the usual continuation rules.

Give the detailed basis when requested, when a material conflict needs it or when the caller consumes it. Include relevant paths, inspected scope and limits, prerequisites, exact candidate keys and applicable preferences. Use level, node, status and inference rows when a detailed project-wide report needs them. Project-wide inspection still covers all applicable goals and siblings. Include drift and hygiene in the default reply only if they affect the decision.

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
