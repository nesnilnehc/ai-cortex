# plan-next: output guidance

## 3.3 Output format selection

The output format adapts to the situation:

| Situation | Recommended format |
| --- | --- |
| One suggestion, the situation is clear | **Prose**: 1-3 sentences saying what to do, why, and what counts as done |
| ≥2 parallel suggestions, or a parallel / converge judgment is needed | **Structured cards** (format below) |

**Prose format (simple situations)**: state it directly in natural language, covering what to do → why now → what counts as done. No fields, labels or card headers needed.

**Structured card format (complex situations, ≥2 parallel suggestions)**:

```text
**N. [action name]** · `priority label`

> [TL;DR card header: one sentence answering "what to do → the immediately visible benefit", ≤30 words]

- Governance context: [multi-line short chain, ≤25 words per line; see "Writing the governance context" below]
- Recommended skill: `/skill-name [focus ≤40 words]`
- Evidence: [file path or observable signal ≤20 words]
- Completion marker: [observable result, 1 sentence]
- [optional] Cost of deferral: [the impact of not doing it ≤30 words]
- [optional] Onboarding threshold: [prior knowledge / doc path ≤30 words]
```

**Shared constraints (prose and cards alike)**: whichever format is used, every suggestion must carry what to do, why, and an observable completion marker. A project code must carry a natural-language subtitle on first appearance (see §3.3.1 + §3.7).

**Writing the TL;DR card header**:

A quote block (`> ...`), placed under the priority label and above the field list. It answers "what to do → the immediately visible benefit" in ≤30 words. It is the strongest visual anchor, so the reader sees the core action on the first screen.

- ✅ Good: `> Let the PM see coverage progress live, filling the visibility gap in Goal 1's acceptance.`
- ❌ Bad: `> Start parallel tasks to advance the milestone (repeats the subject field below, no new information).`

**Writing the governance context**:

Show the trace chain from the strategic goal down to the current gap, **and it must carry the current state of the L1 acceptance KPI**. Use a multi-line short-chain format (≤25 words per line):

```text
- Governance context:
  - Strategic goal: [the goal's natural-language name + its core KPI in one sentence]
  - Current KPI: [current value / target value / benchmark; write "data missing" when there is none]
  - Roadmap: [the milestone's natural-language name + its current stage]
  - Current position: [the layer the blockage sits in + why, ≤15 words]
```

The ≤25-word limit per line is hard. Wrap onto the next line when it overflows; nest parentheses no more than 1 level deep.

**Mandatory constraint**: every route must answer explicitly, "how does this action lead back to the strategic goal's acceptance?" If it cannot, route to the task of establishing the KPI data source instead; it must not route straight to downstream execution.

**Three ways to express KPI state** (following the triplet; see the threshold annotation in §3.3):

- Met: `citation visibility 85% / target ≥80% / industry 75-85% (met)`
- Not met: `citation visibility 62% / target ≥80% / industry 75-85% (not met)` or `citation visibility not yet measured / target ≥80% (pending measurement)`
- Data missing: `citation visibility data source missing / target ≥80% / no benchmark (data source to be built)`

**The threshold annotation triplet**:

Any KPI or threshold must carry the triplet on first appearance:

> Format: `[metric name (plain-language gloss)]: current X / target Y / benchmark Z`
>
> Example: `Adoption rate (share of recommendations users accept): current 42% / target ≥70% / 50-65% counts as good in the industry`

**The benchmark** is one of: an industry baseline, the project's own historical value, or an empirical threshold. With no benchmark available, write "project-defined (no external benchmark)" to put the reader on guard. On a metric's second appearance within the same card, the benchmark may be omitted.

> The authoritative definition of the triplet format is [rules/roadmap-quality.md](../../../rules/roadmap-quality.md) §3; the roadmap's success metrics are produced by `define-roadmap` in the same format, and the wording at both ends must stay consistent.

**Writing the recommended skill**: a slash command + a completion prompt, in the format:

> `/skill-name [focus: what to do this time, the scope, the key asset path or task ID]`

Prompt requirements: state the specific focus of this call, include the key asset path or task ID, ≤40 words, and make it directly copy-pasteable. When the all-pending L5 "awaiting execution" branch has no governance skill available, write "(no governance skill; hand to the development team to implement per `[path]`)".

**Priority labels** (mapped from the internal priorities in §3.2; the "Do now" section uses only labels, never the codes):

| Internal code | User-facing label |
| --- | --- |
| P0 | `urgent` |
| P1 | `important` |
| P2 | `defer` |
| P3 | `minor` |
| — | `awaiting execution` (special: governance is ready, waiting on execution; used only for the all-pending L5 branch) |

**Completion marker**: an observable result, 1 sentence; where execution can be blocked (a strategic conflict, a dependency cycle), append "return to plan-next for re-evaluation if blocked". With several tasks, **each card owns its own completion marker**; they are not stacked at the outer level.

**Cost of deferral (optional)**:

Answers "what happens if this is not done", so the reader can judge "this one first vs something else first". ≤30 words.

- ✅ Good: `Goal 1's acceptance has no visible route, so the PM cannot judge when to wrap up the deliverables`
- ❌ Placeholder filler (forbidden): `to be added` / `see the task` / `affects the schedule` (the same as the vague-wording anti-pattern)

When there is not enough information, **omit this field**; inventing one is not allowed.

**Onboarding threshold (optional)**:

Answers "who does this next, and do they need to read up first". ≤30 words. Attach the path when pointing at a specific document.

- ✅ Good: `Requires knowing how to configure a Grafana data source; if unfamiliar, see docs/runbooks/grafana-setup.md`
- ❌ Placeholder filler (forbidden): `needs relevant knowledge` / `see the docs`

When there is not enough information, **omit this field**; inventing one is not allowed.

### 3.3.1 Words banned from the "Do now" section

In the "Do now" section the following are **banned outright** — the codes themselves and their natural-language equivalents alike:

| Banned | Allowed instead |
| --- | --- |
| L1, L2, L3, L4, L5; goal layer, roadmap layer, requirement layer, design layer, task layer | Say "strategic goal", "roadmap", "requirement document", "design document", "task" directly |
| G1, asset missing | Describe what is actually missing: "`xxx.md` does not exist" |
| G2, incomplete content | Describe what content is missing: "missing field X / section X" |
| G3, truth drift, completion drift, traceability drift | Describe the actual inconsistency: "the task status does not reflect the code progress" |
| G4, misplacement | Describe the actual problem: "the file name does not follow the norms" |
| P0, P1, P2, P3; now/next time/later/ignorable (as a priority annotation) | Use `urgent` / `important` / `defer` / `minor` |
| pending, in-progress, done, blocked (verbatim in user-facing output) | Say "not started", "in progress", "finished", "blocked" |
| Rules layer, Why layer, What layer, How layer, Is layer | Say "norms files", "strategy documents", "planning documents", "design documents", "code implementation" |
| **A bare project code**: `T\d+` / `M\d+` / `Goal \d+` / `BL-\d+` / `ADR-\d+` / a commit hash and other internal IDs | In the header summary and the "Do now" and "Also worth noting" sections, the first appearance must carry a natural-language subtitle: `T51 (coverage dashboard)` / `M5 (hybrid-retrieval maturity milestone)`; later appearances within the same card may use the bare code; for a missing dictionary entry see the §3.7 fallback |
| **MoSCoW framework words**: Must Have / Should Have / Could Have / Won't Have | Use "must-deliver / expected-deliver / optional / not for now" instead |
| **Governance process jargon**: precondition gate / short-circuit / soft-blocked / sibling scan / focus node / all-pending branch / inference from children | Use a plain description: "the norms file is missing, establish it first" / "waiting on the developers" / "the scan result for the other nodes at this level" |
| **A bare threshold with no benchmark**: `≥70%` / `P95 ≤30s` / `a 14-day continuous window` (a number with no benchmark) | Use the triplet: `[metric name (plain-language gloss)]: current X / target Y / benchmark Z` (see the threshold annotation in §3.3) |

Violating this table = the "Do now" output is unacceptable; the offending fields must be rewritten and must not be kept.

### 3.4 User output structure

> **Format choice**: a single suggestion may use prose instead of the cards below. The structured template below applies where there are ≥2 parallel suggestions. When any route is excluded, render `Skipped recommendations` before `Do now`, even when the remaining recommendation uses prose.

````markdown
# Next-step suggestions

> **Decision state**: `actionable` | `needs_input` | `no_applicable_action` | `complete`

> **Situation**: [objective status summary, ≤25 words. Example: the M5 must-deliver items are clear, three expected-deliver items not started]
> **Core tension**: [the sticking point this cycle, ≤30 words. Example: the adoption-rate pipeline is live but the sample has not reached 100, so acceptance cannot be judged yet]

---

## Skipped recommendations

- **[action name; displayed position when known]** — [this conversation / persistently until restored from `.ai-cortex/plan-next.yaml` / both, when both scopes contain the key]; no governance artifact or status changed.

---

## Do now

**1. [action name (project code with a natural-language subtitle)]** · `urgent / important / defer / awaiting execution`

> [TL;DR card header: what to do → the immediately visible benefit, ≤30 words]

- Governance context:
  - Strategic goal: [the goal's natural-language name + its core KPI in one sentence]
  - Current KPI: [current value / target value / benchmark; write "data missing" when there is none]
  - Roadmap: [the milestone's natural-language name + its current stage]
  - Current position: [the layer the blockage sits in + why, ≤15 words]
- Recommended skill: `/skill-name [focus ≤40 words]`
- Evidence: [file path or observable signal ≤20 words]
- Completion marker: [observable result, 1 sentence]
- [optional] Cost of deferral: [the impact of not doing it ≤30 words; omit when information is short, inventing one is not allowed]
- [optional] Onboarding threshold: [prior knowledge / doc path ≤30 words; omit when information is short]

---

**2. [action name]** · `priority label`

...(same format as above, at most 3; several tasks starting in parallel render as several side-by-side cards, see the multi-task multi-card rendering rule in §3.1)

When no candidate remains, use the appropriate state-specific behavior from §2.0.1. State the blocker or completion evidence plainly; an empty list alone is never a completion claim.

---

## Also worth noting

<!-- The drift sweep (step 2.2) and hygiene sweep (step 2.3) entries collect here, at most 5, truncated by priority -->

**[drift/hygiene name]** · `defer / minor`

[one sentence: what problem was found]

- Evidence: [file path or observable signal]
- Recommended skill: `/skill-name [focus]`

---

## Diagnostic basis (technical traceability)

<!-- This section is the internal traceability zone: L1-L5, G1-G4, P0-P3 and the status codes (pending/in-progress/done/blocked) are allowed here -->

- **Project situation**: [one-sentence summary]
- **Asset inventory**: [list only the assets whose status changed]
- **Excluded routes**: [action name, exact route key, evidence path, and session/persistent duration; write "none" when empty]
- **Route blockers**: [candidate/action, blocker evidence, scope, and whether independent candidates remain; write "none" when empty]
- **Open decision** (when `needs_input`): [the one fact needed and how its answer changes routing]

**Decision logic**:

| Level | Node | Status | Inference |
|---|---|---|---|
| Strategic goal | [goal name] | [KPI state] | [keep drilling down / skip / route] |
| Roadmap | [node name] | [pending/in-progress/done/blocked] | [sibling scan conclusion + focus node / the rule that fired] |
| Requirement | [requirement name] | [status] | [verdict] |
| Design | [design name] | [status] | [verdict] |
| Task | [task name / set] | [status] | ["awaiting execution" branch / route downstream / completion verdict] |

- **Drift sweep result**: [list of drift entries; write "none" when empty]
- **Hygiene sweep result**: [list of hygiene issues; write "none" when empty]
- **Missing dictionary notice** (if any): [the project codes not found in the dictionary, with a suggestion to add them to `docs/glossary.md`]
````

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

**On responsibility boundaries**:

- ❌ Calling any downstream skill or editing a governance artifact
- ❌ Hiding the reason for a skip or treating a route-level blocker as global
- ❌ Mixing in downstream execution detail (no writing ADRs, no fixing code, no tidying structure)
- ❌ Treating a skipped recommendation as `done`, `blocked`, `cancelled`, a date change, or any other persisted governance state
- ❌ Choosing session or persistent scope when the user did not specify one
- ❌ Carrying a session skip into another conversation, or silently dropping a persistent preference on a later run
- ❌ Reporting a saved preference when `.ai-cortex/plan-next.yaml` was not written successfully
- ❌ Guessing which recommendation an ambiguous ordinal or title means

**On the routing itself**:

- ❌ Vague wording ("possibly / perhaps / could consider")
- ❌ Omitting the completion marker
- ❌ Mixing several gap types into one route
- ❌ Assigning priority by the number of gaps
- ❌ Skipping a level in the tree-traversal report (reporting an L3 route while L2 is missing) — it violates "first gap first"
- ❌ Judging "finished" from git signals — completion at L2-L5 is judged by the `status` field; **L1 completion must additionally pass the acceptance-KPI check**
- ❌ Ignoring an explicit `status:` field and relying only on inference from children — explicit wins
- ❌ **Treating `status = approved` as the criterion for L1 done** — approved = the decision was approved ≠ acceptance met; confusing them skips the whole L1 subtree
- ❌ **Bypassing L1 and reporting a middle layer (M5/tasks) directly** — answer "is the L1 acceptance KPI met" first, then drill down
- ❌ A governance-context field with no current L1 acceptance-KPI value — it violates the "a route must lead back to the strategic goal's acceptance" constraint
- ❌ Routing straight to downstream execution while the L1 acceptance-KPI data source is missing — the first route should establish the KPI data source
- ❌ Forcing a downstream skill in when L5 is all pending — with the tasks already there, no governance skill applies, and the output should be an "awaiting execution" card
- ❌ Not considering a parallel start when a blocked node is present — blocked is a parallelism signal
- ❌ Recommending yet more parallel expansion when several nodes are in-progress and none blocked — the suggestion is to converge
- ❌ Merging routes for several goals without naming each goal's source in the evidence
- ❌ Evaluating downstream while the roadmap is untiered, skipping `promote-roadmap-items`
- ❌ Ignoring the `depends_on:` field and suggesting parallelism anyway — a dependency forces sequence
- ❌ Using a skipped precondition or unfinished ancestor as permission to route to its children
- ❌ Replacing an excluded recommendation with a dependent route merely to ensure that "Do now" is non-empty

**On tree traversal and scanning**:

- ❌ Reporting a gap on a done node in the main "Do now" routing (the hygiene sweep's checks on done nodes are the exception, and go to "Also worth noting")
- ❌ Reporting gaps at several levels of the same node at once (it violates depth-first)
- ❌ Introducing a mode enum or configuration override for the governance scan (read the physical signals directly)
- ❌ Taking on manifest maintenance (a difference is emitted as a G3 diagnostic entry, not repaired)

**On internal terminology leaking**:

- ❌ A code appearing in the "Do now" section: any form of L1-L5, G1-G4, P0-P3
- ❌ The natural-language equivalents of those codes appearing in "Do now": asset missing, incomplete content, truth drift, completion drift, traceability drift, misplacement, goal layer, roadmap layer, requirement layer, design layer, task layer, Rules layer, Why layer, What layer, How layer, Is layer
- ❌ Priorities using the old labels "now/next time/later/ignorable" or the P0-P3 numbering (use `urgent/important/defer/minor`)
- ❌ Verbatim status values in the "Do now" section: pending/in-progress/done/blocked (use: not started/in progress/finished/blocked)
- ❌ Using a level number as the subject in the diagnostic basis (a parenthetical trace is allowed, a subject is not)
- ❌ An example titled "L2→L3 advance" (use a natural-language description of the situation)

**On jargon and judgment scaffolding**:

- ❌ A bare project code (`T51` / `M5` / `Goal 1` / `BL-001` / `ADR-033`, and so on) with no natural-language subtitle on first appearance
- ❌ MoSCoW framework words in a user-facing section (Must Have / Should Have / Could Have / Won't Have)
- ❌ Governance process jargon in a user-facing section (precondition gate, short-circuit, soft-blocked, sibling scan, focus node, all-pending branch, inference from children)
- ❌ A threshold with no benchmark (a bare `≥70%` / `P95 ≤30s` / `14-day continuous window`) — the triplet is mandatory: current value / target value / benchmark
- ❌ Merging several tasks into one card subject with a comma, a plus sign, or "start in parallel" (`T51 + T-SG5-002` / `T51, T52 in parallel`) — several tasks render as several cards
- ❌ Stacking several tasks' KPIs into one card's completion marker (`A reachable + B queryable + C usable`) — each card owns its own completion marker
- ❌ A governance context nesting parentheses more than 1 level deep (`Goal X (acceptance: KPI A current 80% (met) / target ≥70% (stretch))`) — split it into a multi-line short chain
- ❌ A governance context written as a single chain over 60 words — it must become a multi-line short chain of ≤25 words per line
- ❌ Filling the cost-of-deferral / onboarding-threshold fields with placeholder text ("to be added" / "see the task" / "affects the schedule" / "needs relevant knowledge") — omit when information is short
- ❌ A TL;DR card header that repeats the subject field ("start parallel tasks to advance the milestone" restates the subject) — it must answer "the immediately visible benefit"
- ❌ Forcing a code missing from the dictionary into a user-facing section (mark it in the diagnostic basis, and use a generic description in the user-facing section)

---
