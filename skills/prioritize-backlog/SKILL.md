---
name: prioritize-backlog
description: Force a clean re-score of every backlog item with four frameworks (RICE, WSJF, MoSCoW, ICE) in parallel — ignores any existing priority, auto-detects multi-file or single-file backlog layouts, surfaces framework disagreements, and captures the user's final decision with rationale.
description_zh: 对全部 backlog 条目强制重评（忽略原 priority），并行跑 RICE / WSJF / MoSCoW / ICE 四框架；自动适配多文件目录或单文件 backlog 形态，呈现分歧并捕获用户决策依据。
tags: [workflow, automation, meta-skill]
version: 2.2.0
license: MIT
recommended_scope: project
cognitive_mode: interpretive
metadata:
  author: ai-cortex
triggers: [prioritize backlog, score backlog, backlog ranking, planning prep, re-score backlog]
input_schema:
  type: free-form
  description: Backlog items in any priority state, located either as one-file-per-item under a backlog directory or as a single backlog.md (yaml-list / H2+yaml / table); plus strategic-goals.md and optional project-specific thresholds
output_schema:
  type: chat
  description: Per-item scoring table across 4 frameworks + disagreement call-outs + detected backlog mode + user's priority_decision (with previous-value field) written back to each item in its native format
---

# Skill: Prioritize Backlog

## Purpose

Assess a batch of backlog items with several value frameworks in parallel, surface where those frameworks disagree, and let the user make the priority decision with its rationale recorded.

---

## Core Objective

**Primary goal**: run a **forced, complete re-score** over a batch of backlog items (disregarding their current priority state), produce the user-confirmed new `priority` and `priority_decision`, and write them back into whichever backlog layout each one lives in (a multi-file directory, or a single file).

**Success criteria** (all of them must hold):

1. ✅ Every item carries a score from each of the 4 frameworks (RICE / WSJF / MoSCoW / ICE)
2. ✅ Disagreement between frameworks is surfaced explicitly (a gap of ≥ 2 levels triggers a human decision)
3. ✅ Each item's final `priority` is confirmed by the user, not emitted by an algorithm
4. ✅ Each item gets a `priority_decision` field written back (carrying the `previous` snapshot of the old value, so what this round overwrote can be looked up)
5. ✅ A batch result table is emitted, so the user can compare across items
6. ✅ The report header declares the detected backlog layout (`multi-file` / `yaml-list` / `h2-yaml` / `table`), and the write-back follows that layout

**Acceptance test**: can a reader see the new priority, the decision rationale, and the overwritten old value straight from a backlog item's frontmatter / yaml block / table row, without going back through the conversation?

---

## Scope Boundaries

**This skill owns**:

- Detecting the backlog layout automatically (multi-file directory / single-file yaml-list / h2-yaml / table) and reading **every** item
- Force-rerunning the RICE / WSJF / MoSCoW / ICE scoring on each one (ignoring the existing priority and priority_decision)
- Surfacing disagreement between frameworks
- Capturing the user's decision and writing it back in the detected layout (frontmatter for multi-file; the matching yaml block or table cell for a single file)

**This skill does not own**:

- Creating new backlog items (use `capture-work-items`)
- Promoting items into the roadmap (use `promote-roadmap-items`)
- Scoring a single item (this skill is a **batch** workflow; scoring one item alone loses the comparison)
- Archiving old assessment history (only the single `previous` field is kept; a caller that needs history owns it)

**Handoff point**: once scoring is done, hand off to `promote-roadmap-items` for the backlog → roadmap promotion.

---

## Use Cases

- Suggested as the trigger after a batch capture by `capture-work-items`
- A clean, complete re-score of the pile before a planning ceremony
- A direct rerun at any point after a strategy refresh (no extra switch needed — an overwriting re-score is the default)
- A large gap reported by `plan-next` enters scoring once it has been captured
- A single-file backlog (a lightweight project keeping one `backlog.md`, say) is handled directly too

---

## Behavior

### Stage 0: read the input and detect the layout

1. **Layout detection (tried in order, stopping at the first hit)**

   | Order | Layout | Detection condition |
   |---|---|---|
   | 1 | `multi-file` | `docs/process-management/backlog/` or `docs/backlog/` exists, and at least one `*.md` file carries the `artifact_type: backlog-item` or `priority:` frontmatter field |
   | 2 | `yaml-list` | The single file `docs/process-management/backlog.md` or `docs/backlog.md` exists, and its frontmatter or top-level YAML carries an `items:` array |
   | 3 | `h2-yaml` | The same single file, whose body has a `## <title>` heading immediately followed by a ```yaml … ``` code block |
   | 4 | `table` | The same single file, whose body has a Markdown table carrying `Title` and `Priority` (or equivalent columns) |

   Prefer the project's own custom path (where `backlog-item.path_pattern` exists in `.ai-cortex/artifact-norms.yaml` or `docs/ARTIFACT_NORMS.md`).

   **Nothing hits at all** → halt, report "no recognizable backlog layout found", and point the user at `capture-work-items` first.

   **A mixed layout is detected** (both a directory and a single file) → default to multi-file and tell the user in the report that the single file was ignored; nothing is written twice, to avoid inconsistency.

2. Read `docs/project-overview/strategic-goals.md` (used for the WSJF Cost of Delay judgement and the MoSCoW Must judgement).

3. **Enumerate every item** (no longer filtering on `priority: unset`): show any existing `priority` / `priority_decision` as an audit log only, **kept out of the new scoring**, to avoid anchoring bias.

4. If the total item count = 1 → **halt with a warning**: "scoring one item alone loses the comparison. Scoring at least 2 together is suggested. Continue?"

### Stage 1: score against all four frameworks in parallel

Compute all of these for every item at once:

#### RICE

```text
RICE = (Reach × Impact × Confidence) / Effort
```

- **Reach**: how many people or instances are affected, as a number
- **Impact**: 3 (massive) / 2 (high) / 1 (medium) / 0.5 (low) / 0.25 (minimal)
  - The floor must be able to go below 1. If the lowest band is 1, a trivial item cannot be pushed down and only Reach and Effort can separate it from the rest, which leaves low-value items scoring too high
- **Confidence**: 0-100%, anchored at three points — `100% = backed by data` / `80% = partial evidence` / `50% = a guess`
  - Without anchors, scoring the same batch twice drifts; the anchors are what make a score reproducible
- **Effort**: person-weeks

Mapped to a priority level:
| RICE score | Level |
|---|---|
| ≥ 1000 | P0 |
| 200-1000 | P1 |
| 50-200 | P2 |
| < 50 | P3 |

(These thresholds are a default example; a project may set its own.)

#### WSJF

```text
WSJF = Cost of Delay / Job Size
```

- **Cost of Delay** = Business Value + Time Criticality + Risk Reduction / Opportunity Enablement
- **Job Size** = relative effort, on the Fibonacci scale 1, 2, 3, 5, 8, 13, 20

Mapped to a priority level, by the item's WSJF percentile within the current backlog:
| WSJF percentile | Level |
|---|---|
| Top 10% | P0 |
| 10-30% | P1 |
| 30-70% | P2 |
| Bottom 30% | P3 |

#### MoSCoW

Classified by level of commitment:

- **Must**: not doing it this cycle blocks something badly or breaches compliance → P0
- **Should**: doing it this cycle raises value markedly → P1
- **Could**: do it if there is time → P2
- **Won't**: explicitly not this cycle → P3. Where it is **never** to be done, as opposed to deferred past this cycle, take the `status: declined` terminal state instead; see stage 4

#### ICE

```text
ICE = Impact × Confidence × Ease
```

- Each dimension scored qualitatively from 1-10
- Impact: the effect on a strategic goal
- Confidence: how much the estimate is trusted
- Ease: how easy it is to build — higher means easier

Mapped:
| ICE score | Level |
|---|---|
| ≥ 500 | P0 |
| 200-500 | P1 |
| 50-200 | P2 |
| < 50 | P3 |

### Stage 2: surface the disagreements

For each item, compute the **widest gap between frameworks**:

| Gap in levels | What happens |
|---|---|
| ≤ 1 level (P1 vs P2, say) | Take the **RICE** result by default; no human decision needed |
| ≥ 2 levels (P0 vs P3, say) | Surface it explicitly; a human decision is required |

A project may set its own disagreement threshold; the default is 2 levels.

### Stage 3: present the batch result

Output format:

```markdown
## Batch Scoring Summary

| # | Title | RICE | WSJF | MoSCoW | ICE | Gap | Suggestion |
|---|---|---|---|---|---|---|---|
| 1 | ... | P1 | P1 | Should | P2 | 1 level | take P1 automatically |
| 2 | ... | P3 | P1 | Could | P3 | 2 levels | **human needed** |
| ... |

## Items needing a human decision (gap ≥ 2 levels)

### Item #2: <title>

- RICE=P3 because Reach is only 10 people and Effort is 8 weeks
- WSJF=P1 because the Q3 milestone depends on it, so Cost of Delay is high
- MoSCoW=Could
- ICE=P3

**Where they disagree**: time criticality (WSJF) against reach (RICE)

**Your decision**: which P, and why?
```

### Stage 4: capture the decision and write it back, per layout

For each item:

1. Settle the final `priority`, whether taken automatically or given by the user.
2. Build the `priority_decision` field, which **must contain** `previous`:

   ```yaml
   priority_decision:
     final: P<N>
     previous: P<N> | unset
     frameworks:
       rice: P<N>
       wsjf: P<N>
       moscow: Must | Should | Could | Won't
       ice: P<N>
     rationale: <one-sentence reason if disagreement was ≥ 2 levels>
     strategic_override: <the reason; required only when the final priority is above what the frameworks concluded>
     decided_by: auto | user
     decided_at: <ISO date>
   ```

   `strategic_override` covers the case where all four frameworks score an item low but strategy requires it anyway. That judgement is legitimate, but it must leave a trace — otherwise "the user confirms each item" becomes an evidence-free bypass through which anyone can lift any item. The field is required whenever the final `priority` sits above what the frameworks concluded.

3. **Decide whether it is terminal**: where an item is judged never to be done — low value against high effort, or the need has lapsed — do not leave it in the backlog to sink under P3. P3 goes to Later by default, so the item would take part in every full re-scoring from then on. Write the terminal state instead:

   ```yaml
   status: declined
   declined_reason: <one sentence on why it will never be done>
   declined_at: <ISO date>
   ```

   A terminal item is skipped outright in later re-scorings. The user decides on the terminal state; this skill must not decide it alone.

4. **Write back per layout**:

   | Layout | How to write back |
   |---|---|
   | `multi-file` | Update `priority` + `priority_decision` in each `*.md` file's frontmatter |
   | `yaml-list` | Change `items[i].priority` + `items[i].priority_decision` in the single file, keeping the YAML indentation and key order |
   | `h2-yaml` | Inside that item's ```yaml``` block, replace `priority` + `priority_decision`, leaving the block where it is |
   | `table` | Update the table's `Priority` cell; put `priority_decision` in a `## Priority Decisions` section below the table, listed by item anchor |

   Before writing back, confirm the old value is recorded in `priority_decision.previous`, so nothing is swallowed silently.

5. **The boundary on skipping terminal and settled items**: an item with `status: declined` takes no part in re-scoring.

### Stage 5: emit the final report

The report header must carry:

- `Backlog mode: multi-file | yaml-list | h2-yaml | table`
- How many items entered the `declined` terminal state this round, if any
- `Re-scored items: N (X overwrote an existing priority; Y were unset)`

The report body:

- How many were processed, decided automatically, and decided by a human
- The distribution across priorities
- What to do next, such as a batch promotion with `promote-roadmap-items`

---

## Input & Output

**Input**: see the frontmatter `input_schema` — the backlog directory, strategic-goals.md, and optional threshold overrides.

**Output**: the batch scoring table in conversation, plus updated frontmatter in every backlog file — the `priority` and `priority_decision` fields.

---

## Restrictions

### Hard boundaries

- **A full re-score is forced**: by default every item's `priority` and `priority_decision` is overwritten, the old value surviving only in the single `previous` field. No history is archived — the skill keeps one responsibility, and archiving belongs to the caller
- **Layouts are never mixed**: once multi-file is detected, no single file is scanned, and the reverse likewise, so the two are never written inconsistently
- The frameworks are never aggregated into one score; keeping the disagreement signal is the point of this skill
- Where the gap is ≥ the threshold, a human must decide; there is no default fallback
- No new backlog item is created; that is `capture-work-items`' job

### Skill boundaries

**Not done here; another skill owns it**:

| Action | Owner |
|---|---|
| Creating a new backlog item | `capture-work-items` |
| Promoting a backlog item into the roadmap | `promote-roadmap-items` |
| Task breakdown | The AgentFabric runtime, outside AI Cortex |
| Recording a requirement in detail | `capture-work-items` |

---

## Anti-Patterns

- ❌ **Never take a weighted average of the four scores** — aggregating throws away the disagreement signal, which is what this skill exists for
- ❌ **Never score a single item on its own** — with no comparison group, the relative nature of RICE and WSJF stops working
- ❌ **Never hide a disagreement** — even where RICE is taken automatically, show every framework's score in the report table
- ❌ **Never ignore `strategic_goal_id`** — the strategic goal is what decides MoSCoW's Must
- ❌ **Never write `priority_decision.rationale` in vague words** ("roughly", "possibly") — it must cite a framework or a figure concretely
- ❌ **Never re-score by "checking whether the old priority looks reasonable, then deciding whether to overwrite"** — that anchors the framework scores, defeating the clean forced re-score this skill is designed around
- ❌ **Never discard the old value** — `priority_decision.previous` must be written, so the user can see what this round changed in one place
- ❌ **Never try to write to both layouts** — pick multi-file or single-file, so the data cannot drift apart

---

## Self-Check

- [ ] The backlog layout is declared (`multi-file` / `yaml-list` / `h2-yaml` / `table`) and written back accordingly
- [ ] Where layout detection failed, it halted and pointed at `capture-work-items`
- [ ] Every item was scanned, with the old priority shown but kept out of the scoring, so nothing was anchored
- [ ] All 4 frameworks ran on every item
- [ ] Items whose gap is ≥ the threshold were surfaced and a human decision was asked for
- [ ] Items whose gap is ≤ the threshold took RICE automatically, with every framework's score still visible
- [ ] `priority_decision` was written back for every item, carrying the framework results, the rationale where there was a disagreement, and the `previous` snapshot of the old value
- [ ] The batch summary carries `Backlog mode`, the overwrite counts, the priority distribution, and what to do next
- [ ] `promote-roadmap-items` was not called automatically

---

## Examples

### Example 1: a full re-score of a multi-file backlog, the common case

**Input**: 5 items under `docs/process-management/backlog/`, in mixed states — 3 at `priority: unset`, 1 at an existing `priority: P2`, 1 at an existing `priority: P3`.

**Layout detection**: `multi-file` matches.

**Output summary**:

```markdown
Backlog mode: multi-file
Re-scored items: 5 (2 overwrote an existing priority; 3 were unset)

## Batch Scoring Summary

| # | Title | Old | RICE | WSJF | MoSCoW | ICE | Gap | Suggestion |
|---|---|---|---|---|---|---|---|---|
| 1 | Payment API response time | unset | P1 | P1 | Should | P1 | 0 levels | **P1 automatically** |
| 2 | ARTIFACT_NORMS format upgrade | P3 | P3 | P3 | Could | P3 | 0 levels | **P3 automatically, matching the old value** |
| 3 | Multi-currency support for Q3 | unset | P2 | P0 | Must | P2 | 2 levels | **human needed** |
| 4 | Fix the 500 on login | P2 | P1 | P2 | Should | P1 | 1 level | **P1 automatically, overwriting P2** |
| 5 | New technical debt: refactor the auth module | unset | P3 | P2 | Could | P2 | 1 level | P3 automatically |

## Human decision needed: Item #3
(as above, abridged)
```

**A fragment of what was written back** (Item #4, the overwritten one):

```yaml
priority: P1
priority_decision:
  final: P1
  previous: P2
  frameworks:
    rice: P1
    wsjf: P2
    moscow: Should
    ice: P1
  decided_by: auto
  decided_at: 2026-04-17
```

### Example 2: a single-file backlog in the h2-yaml layout

**Input**: `docs/backlog.md` holds a "lightweight backlog", each item an H2 heading plus an inline yaml block:

```markdown
## Payment API response time
```yaml

strategic_goal_id: goal-1
priority: P2

```markdown
Reason: ...

## Fix the 500 on login
```yaml

strategic_goal_id: goal-1
priority: unset

```text
…
```

**Layout detection**: the multi-file path does not exist -> yaml-list does not match -> **`h2-yaml` matches**.

**How it is written back**: replace `priority` and `priority_decision` inside each item's yaml block, leaving the descriptive prose outside the block untouched; `priority_decision.previous` records the old value — P2 for one item, unset for the other.

The report header: `Backlog mode: h2-yaml`, `Re-scored items: 2 (1 overwrote an existing priority; 1 was unset)`.

---
