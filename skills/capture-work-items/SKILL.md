---
name: capture-work-items
description: Capture requirements, bugs, or issues from free-form input into structured, persistent artifacts. Use when user wants to record a work item quickly without deep validation.
description_zh: 将自由形式输入快速捕获为结构化、可持久的需求、缺陷或问题制品；无需深度验证。
tags: [writing, documentation, workflow]
version: 2.0.1
license: MIT
recommended_scope: both
metadata:
  author: ai-cortex
triggers: [capture, quick capture, record bug]
input_schema:
  type: free-form
  description: Raw description of requirement, bug, or issue from user; optional upstream_ref (parent roadmap/requirement path for colocation/parent-pointer modes); optional artifact_norms_path override
output_schema:
  type: document-artifact
  description: Structured work item(s) written per path detection
  artifact_type: backlog-item
  path_pattern: docs/process-management/project-board/backlog/YYYY-MM-DD-{slug}.md (canonical) or docs/backlog/YYYY-MM-DD-{slug}.md (fallback)
  lifecycle: living
---

# Skill: Capture Work Items

## Purpose

Capture a requirement, bug, or issue from free-form input and turn it into a structured, persistent artifact. It gives a fast structured record without the deep validation that "analyze-requirements" performs. It keeps the output path aligned with the project's documentation structure (a project documentation template, for instance) and covers governance status tracking.

---

## Core Objective

**Primary goal**: turn the requirement, bug, or issue description the user gives into a structured work item carrying every required field, and persist it to the path agreed for the project.

**Success criteria** (all must be met):

1. ✅ **Type identified**: the work item is classified as a requirement, a bug, or an issue
2. ✅ **Required fields complete**: every required field for that type is filled in (no inference; ask the user when one is missing)
3. ✅ **Status set**: the front-matter starts at `status: captured`
4. ✅ **strategic_goal_id tagged**: `strategic_goal_id` is required on every work item and maps to one of the goals in the project's strategic-goals. Promotion pools capacity by goal, and with nothing to attribute it to there is no way to compute the capacity already used
5. ✅ **priority marked unset**: a new work item's frontmatter carries `priority: unset`, waiting for `prioritize-backlog` to score the batch
6. ✅ **Path detected**: the output path is chosen from the project's documentation structure (see Path Detection)
7. ✅ **Artifact persisted**: the work item is written to the chosen path
8. ✅ **User confirmation**: the user explicitly confirms the write, or delegates it
9. ✅ **Priority scoring suggested after a bulk capture**: at the end of a bulk capture, count the unscored backlog entries and suggest running `prioritize-backlog` (**never automatically**)

**Acceptance test**: can a person or a downstream system read the artifact, understand the whole work item, and act on it without asking a clarifying question?

---

## Scope Boundaries

**This skill does**:

- Free-form input → a structured work item
- Single or bulk capture (bulk: confirmed per item or per batch)
- Output local Markdown under the path agreed for the project
- The status lifecycle: the initial "captured" only (downstream updates it to "triaged", "in progress", "done", "blocked", "cancelled")

**This skill does not do**:

- Deep requirement clarification or validation → use "analyze-requirements"
- Design or architecture → use "design-solution"
- Direct API calls to Zentao/GitHub to create issues (an extension point; not needed for v1)

**Handoff point**: once the artifact is persisted and the user has confirmed it, hand off to "analyze-requirements" where the item needs deeper validation, or to process management / milestones for planning.

---

## Use Cases

- **Quick backlog entry**: the user says "record this bug" or "add this requirement" — structure it and persist it, with no full analysis.
- **Meeting / email capture**: pull the work items out of meeting notes or email and save them as structured artifacts.
- **Triage intake**: capture items so they can be triaged and ranked later, during milestones or task breakdown.
- **Backlog evidence**: fill the backlog gap an assessment document identified (such as "backlog: weak — no explicit backlog document").

---

## Behavior

### Interaction Policy

- **Default**: the path from the project norms or from the spec / artifact contract; the type comes from the input
- **Choice options**: one question per missing field at a time; offer choices where they apply
- **Confirm**: the target path whenever it differs from the default; the user confirms before the write

1. Resolve the project norms in the §8.2 discovery order → determine the `path_pattern` for `backlog-item` (default: `docs/process-management/project-board/backlog/YYYY-MM-DD-{slug}.md`, or the fallback `docs/backlog/YYYY-MM-DD-{slug}.md`; a project can override it with an aggregated form)
2. Substitute using the §8.3 placeholder syntax; for a placeholder that does not resolve, follow §8.6 and ask the user
3. If the caller's frontmatter input carries `upstream_ref` (which points at an upstream roadmap entry or requirement): emit `parent: <upstream_ref>` in the produced artifact's frontmatter
4. Record resolved_path plus the frontmatter delta, for the write that follows

Note: by default the §3 path detection logic stands (whether `docs/process-management/` exists decides canonical vs fallback), but where a project declares an explicit `path_pattern` in `ARTIFACT_NORMS.md`, the project's declaration wins.

### Path Detection

Choose the output path from the resolved norms (or the contract default):

| Condition | Output path |
| :--- | :--- |
| `docs/process-management/` exists | `docs/process-management/project-board/backlog/YYYY-MM-DD-<slug>.md` |
| Otherwise | `docs/backlog/YYYY-MM-DD-<slug>.md` |

Create the subdirectories if they do not exist. Use today's date for "YYYY-MM-DD"; `<slug>` is the kebab-case form of the title.

### Phase 0: Classify — identify the type

**Announce at the start:** "I am using the capture-work-items skill to record this work item."

Classify the input as:

- **Requirement**: a new need, a feature request, or an enhancement
- **Bug**: a defect, incorrect behaviour, a failure to meet the spec
- **Issue**: a task, an improvement, or a question (the generic work item)

### Phase 1: Extract — identify the fields

Extract the available fields from the input. Required fields by type:

| Type | Required fields |
| :--- | :--- |
| Requirement | Title, problem/need, acceptance criteria, **strategic_goal_id** |
| Bug | Title, description, steps to reproduce, expected vs actual, severity, **strategic_goal_id** |
| Issue | Title, description, type (task\|improvement\|question), **strategic_goal_id** |

**Notes on strategic_goal_id**:
- Read `docs/project-overview/strategic-goals.md` and present the list of selectable goals to the user
- The user picks which strategic goal this work item mainly serves
- If strategic-goals.md does not exist → **halt**, and suggest running `design-strategic-goals` first
- A bug or tech-debt work item usually maps to the "engineering / governance health" goal — with no strategic sponsor, work of that kind never wins capacity in the competition for value

### Phase 2: Prompt — fill in the missing required fields

For any missing required field, ask the user **one question at a time**. Do not infer or guess.

### Phase 3: Persist — write the artifact

1. Run "resolve the project norms", then "path detection" (above)
2. If the target path differs from the default, confirm with the user
3. Write the Markdown with YAML front-matter from the appropriate template (see the output templates)
4. Set `status: captured` in the front-matter

### Phase 4: Confirm

Confirm with the user that the artifact is written and complete. Do not commit to version control unless the user explicitly asks.

### Phase 5: Suggest batch scoring (never automatic)

At the end of a capture (single or bulk), run the following **suggest action**:

1. Scan the backlog directory and count the entries at `priority: unset`
2. If that count is ≥ the threshold (default ≥ 3), or this bulk capture held ≥ 2 items, emit the suggestion:
   > "The backlog currently holds N entries with no priority set. Running `prioritize-backlog` for a batch scoring before the next planning session is recommended. This skill does not invoke it automatically — the timing is the user's call (batch scoring comes out better when there is a comparison group)."
3. **Never invoke** `prioritize-backlog` automatically (rationale in ADR 2, decision 3.7.1: the two skills run on different rhythms, and forcing them into a chain wrecks the scoring quality)

---

## Input & Output

### Input

- The user's raw description of a requirement, a bug, or an issue
- Optional: project context (the existing "docs/" structure used for path detection)

### Output

A structured work-item Markdown file with YAML front-matter. The templates follow.

#### Requirement template

```markdown
---
artifact_type: backlog-item
created_by: capture-work-items
lifecycle: living
type: requirement
date: YYYY-MM-DD
status: captured
priority: unset
strategic_goal_id: [goal-N]
source: [user|meeting|email]
trace_id: optional
---

# [Title]

## Problem / Need
[Who has what problem; no solution language]

## Acceptance Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]

## Notes
[Optional]
```

#### Bug template

```markdown
---
artifact_type: backlog-item
created_by: capture-work-items
lifecycle: living
type: bug
date: YYYY-MM-DD
status: captured
priority: unset
strategic_goal_id: [goal-N]
severity: [critical|major|minor]
---

# [Title]

## Description
[What goes wrong]

## Steps to Reproduce
1. ...
2. ...

## Expected vs Actual
- **Expected**: ...
- **Actual**: ...

## Environment
[Optional]
```

#### Issue template

```markdown
---
artifact_type: backlog-item
created_by: capture-work-items
lifecycle: living
type: issue
subtype: [task|improvement|question]
date: YYYY-MM-DD
status: captured
priority: unset
strategic_goal_id: [goal-N]
---

# [Title]

## Description
[Content]
```

### Status Lifecycle

This skill only sets "status: captured". Downstream processes (milestones, promotion into iteration tasks, run checkpoints) may update it to "triaged", "in progress", "done", "blocked", or "cancelled".

---

## Restrictions

### Hard Boundaries

- **Do not skip a required field**: where a required field cannot be inferred, ask the user. Do not leave it blank.
- **Do not skip strategic_goal_id**: when `strategic-goals.md` does not exist, halt and suggest running `design-strategic-goals` first; it must not be left blank or inferred.
- **Do not invoke prioritize-backlog automatically**: at the end of a capture, only suggest it and let the user decide when to score the batch (the rhythms differ, and scoring one item at a time distorts the result).
- **No diagnostic flow**: Do not run diagnostic states (RA0–RA5). Where the input is very vague, the suggestion is to capture first, then go deeper on clarification once the intent is confirmed.
- **Confirm the path before writing**: avoid overwriting an existing file; confirm whenever the target path is unclear.
- **Paths follow the project structure**: use the path detection rules; do not hard-code a single path.

### Skill Boundaries (avoid overlap)

**Do not do these** (other skills handle them):

- **Deep requirement validation**: diagnostic states, problem articulation, scope boundaries → use "analyze-requirements"
- **Design and architecture**: solutions, alternatives, trade-offs → use "design-solution"
- **Task breakdown**: epic/task breakdown, refining acceptance criteria → use process management or the implementation plan

**When to stop and hand off**:

- The user says "this needs more analysis" → hand off to "analyze-requirements"
- The user says "design this" → hand off to "design-solution"
- The artifact is persisted and confirmed → the handoff is complete

---

## Self-Check

### Core Success Criteria (all must be met)

- [ ] **Type identified**: the work item is a requirement, a bug, or an issue
- [ ] **Required fields filled in**: every required field is filled in (no inference)
- [ ] **strategic_goal_id tagged**: mapped to a specific goal in strategic-goals
- [ ] **priority is unset**: the frontmatter carries `priority: unset`
- [ ] **Status set**: "status: captured" sits in the front-matter
- [ ] **Path detected**: the output path follows the path detection rules
- [ ] **Artifact persisted**: the file is written to the chosen path
- [ ] **User confirmation**: the user confirmed the write, or delegated it
- [ ] **Batch scoring suggested**: in a bulk scenario, running `prioritize-backlog` was put to the user (and not run automatically)

### Process Quality Checks

- [ ] **One question at a time**: the user was not swamped with questions about several missing fields at once
- [ ] **No solution language in the requirement**: the problem/need describes the problem, not the implementation
- [ ] **Path created**: the `backlog/` subdirectory was created where it was needed
- [ ] **Filename convention**: YYYY-MM-DD-{slug}.md is used

### Acceptance Test

**Can a person or a downstream system read the artifact, understand the whole work item, and act on it without asking a clarifying question?**

If no: the required fields are incomplete. Go back to the prompt phase.

If yes: the capture is done. Hand off as needed.

---

## Examples

### Example 1: Bug capture

**User**: "When I use special characters in the password field, the login page returns a 500."

**Agent announces**: "I am using the capture-work-items skill to record this work item."

**Classify**: classified as a bug.

**Extract**: the title and the description are there; steps to reproduce, expected vs actual, and severity are missing.

**Prompt** (one at a time):

Agent: "What are the exact steps to reproduce this?"

User: "1. Go to /login 2. Enter any username 3. Enter a password containing @ or # 4. Click "Log in""

Agent: "How does what you expected differ from what actually happened?"

User: "Expected: a normal login, or a validation error. Actual: a 500 internal server error."

Agent: "What severity would you assign: critical, major, or minor?"

User: "Major."

**Persist**: path detected — `docs/process-management/` exists. Write to "docs/process-management/project-board/backlog/2026-03-06-login-500-special-chars.md".

**Confirm**: "Written. Would you like to adjust anything, or hand it to triage?"

### Example 2: Requirement capture — vague input

**User**: "We need better error messages."

**Agent announces**: "I am using the capture-work-items skill to record this work item."

**Classify**: classified as a requirement (it could be an issue; the agent picks requirement as the default for a "need").

**Extract**: the title can be derived ("better error messages"); the problem/need and the acceptance criteria are missing.

**Prompt**:

Agent: "Who runs into this problem? What exactly is wrong with the current error messages?"

User: "Our API users get a generic 'something went wrong' with nothing actionable in it."

Agent: "What would 'done' look like — at least one concrete acceptance criterion?"

User: "An error response carries a code (ERR_001, for example) and a short human-readable message explaining what went wrong."

**Persist**: path detected — `docs/process-management/` does not exist. Write to "docs/backlog/2026-03-06-better-error-messages.md".

**Handoff suggestion**: "This could benefit from the deeper validation in analyze-requirements. Carry on with capture alone, or hand off for the full analysis?"

User: "Capture only, for now."

**Confirm**: "Written. Hand it to triage when you are ready."

### Example 3: Issue capture — edge case (several items in one message)

**User**: "Two things: 1) update the README install section. 2) add CONTRIBUTING.md."

**Agent announces**: "I am using the capture-work-items skill. I see two separate work items. I will capture them one at a time."

**Item 1** — type: issue (task). Title: "update the README install section". Description: from the context. Persisted as "2026-03-06-update-readme-install.md".

**Item 2** — type: issue (task). Title: "add CONTRIBUTING.md". Description: from the context. Persisted as "2026-03-06-add-contributing.md".

**Confirm**: "Both items are captured. Review and adjust them if you need to."
