---
name: review-roadmap
description: "Review an existing roadmap document against roadmap-quality criteria: core model completeness, capacity baseline and allocation, metric triplets, outcome framing, dependency mapping, and change frequency. Evaluative atomic skill; output is a findings list."
description_zh: 按 roadmap-quality 判据评估既有路线图文档：核心模型完整性、容量基线与分配、指标三元组、结果导向、依赖已映射、变更频率。评估型原子技能，产出 findings 列表。
tags: [code-review, planning]
version: 1.0.0
license: MIT
recommended_scope: both
metadata:
  author: ai-cortex
triggers: [review roadmap, roadmap review, roadmap quality, check roadmap, roadmap health]
input_schema:
  type: document-artifact
  description: Existing roadmap document (path or content) to evaluate; secondary inputs are strategic-goals.md and the backlog items referenced by the Now tier
  artifact_type: roadmap
output_schema:
  type: findings-list
  description: Zero or more findings with location, category, severity, and suggestion, covering all five roadmap quality dimensions
---

# Skill: Review Roadmap

## Purpose

Evaluate an **existing roadmap document** against the established quality criteria. Neither generate nor rewrite the roadmap — that is the job of `define-roadmap` and `update-roadmap`. Produce a **findings list** the author can act on before anything downstream consumes it.

**The criteria do not live in this skill**: every item is defined in [rules/roadmap-quality.md](../../rules/roadmap-quality.md); this skill only runs the evaluation and organizes the output. Change the criteria in that rule, not in this file.

---

## Core Objective

**Primary goal**: Produce a roadmap findings list covering all five quality dimensions, so the author can close the gaps before a promotion decision depends on them.

**Success criteria** (all must be met):

1. ✅ All five dimensions scanned: completeness / executability / clarity / soundness / traceability
2. ✅ Every finding carries location / category / severity / title / description / suggestion
3. ✅ Every criterion is cited from `rules/roadmap-quality.md`; this skill invents none of its own
4. ✅ A dimension that cannot be evaluated is explicitly marked "cannot evaluate" with the reason, and is not skipped silently
5. ✅ The roadmap is not rewritten; only findings and suggestions are emitted

**Acceptance test**: From the findings list alone, can the author tell which parts to change and what to change them into?

**Handoff point**: The findings go to the author; structural gaps hand off to `define-roadmap`, and status or timing gaps hand off to `update-roadmap`.

---

## Scope Boundaries

**This skill handles**:

- Evaluating an existing roadmap dimension by dimension against `rules/roadmap-quality.md`
- Producing a findings list carrying location, severity, and suggestion
- Marking the dimensions that cannot be evaluated, with the reason

**This skill does NOT handle**:

- Generating or rewriting the roadmap (`define-roadmap` / `update-roadmap`)
- Deciding the orchestration mode — that is the orchestration layer's "detect the context" job; this skill only emits findings
- Promotion decisions (`promote-roadmap-items`)
- Dependency identification (`map-item-dependencies`)
- Maintaining the criteria themselves (`rules/roadmap-quality.md`)

---

## Use Cases

- **Gate before promotion**: when the capacity and dependency criteria do not hold, promotion cannot compute a correct result
- **Taking over someone else's roadmap**: see quickly what this roadmap is missing
- **Periodic checkup**: a roadmap is a living document and drifts over time
- **Entry point of the orchestration chain**: as step 0 of `orchestrate-roadmap-planning`, supplying the conditions the later steps are judged against

---

## Behavior

### Interaction Policy

- **Default**: read `docs/process-management/roadmap.md` or the path set by project norms; the user may name a path or paste the content directly
- **Read-only**: no file is modified at any point
- **No follow-up questions**: this is a one-shot evaluation; missing information becomes a finding or a "cannot evaluate" mark, with no clarification round-trip with the user

### Procedure

1. **Load the criteria**: read [rules/roadmap-quality.md](../../rules/roadmap-quality.md). **A missing file means halt** — without criteria there is no yardstick, and scoring from impressions yields conclusions that look authoritative and rest on nothing.
2. **Load the roadmap and its evidence sources**: read the target document. Three of the criteria draw on data that is not in roadmap.md; that data must be read as well, or those dimensions cannot be evaluated:

   | Criterion | Where the data lives |
   |---|---|
   | A Now-tier item traces to its strategic_goal | The item frontmatter's `strategic_goal_id`, cross-checked against `docs/project-overview/strategic-goals.md` |
   | A Now-tier item has no unresolved prerequisite | The item frontmatter's `depends_on` |
   | Priority was not set by a single source | The item frontmatter's `priority_decision` (including `strategic_override`) |

   **When it is missing**: if the backlog items cannot be read, or roadmap.md's Now tier references no concrete items, mark these three criteria "cannot evaluate — <reason>". **A criterion must not be recorded as passing because it could not be read** — that hollows the criterion out.
3. **Scan dimension by dimension**: work through the rule's five-dimension checklist item by item; each item that fails produces one finding.
4. **Tool adaptation for the change-frequency dimension**: this dimension needs git log to count structural changes to roadmap.md.
   - **Discover**: confirm the current directory is a git repository and that roadmap.md has commit history
   - **Run**: count the file's structural changes inside the configured window and compare against the threshold in the rule
   - **When it is missing**: for a non-git directory, a shallow clone with incomplete history, or a file with no commit history, mark this dimension "cannot evaluate — <the specific reason>". **It must not be skipped silently, and it must not be inferred to pass on that basis**
5. **Set severity**: map mechanically from the table below, with no subjective weighting.
6. **Emit the findings list**.

### Severity Mapping

| Severity | Trigger |
|---|---|
| `critical` | No total capacity baseline or no capacity allocation; a missing piece of the four-part core model; a Now-tier item with an unresolved prerequisite |
| `major` | A success metric that is not a triplet; a milestone or strategic bet not written in the prescribed form; capacity percentages that do not sum to 100%; an engineering-health goal at 0% |
| `minor` | No "explicitly not doing this round" section; no last-updated date; change frequency close to the threshold but not over it |

### Findings Format

```yaml
- location: <section or line in the document>
  category: completeness | executability | clarity | soundness | traceability
  severity: critical | major | minor
  title: <one-line conclusion>
  description: <what fails, and which criterion it is measured against>
  suggestion: <what to change it to, ready to apply>
```

---

## Input & Output

**Input**: the existing roadmap document (path or content); `rules/roadmap-quality.md`; the evidence sources `strategic-goals.md` and the backlog items referenced by the Now tier.

**Output**: a findings list (zero or more) plus a note on any dimension that could not be evaluated. With zero findings, state plainly that the roadmap passes every criterion.

---

## Restrictions

### Hard Boundaries

- **No rewriting**: do not generate new roadmap text, milestones, or metrics. Emit findings and suggestions only; the writing is left to the author or to `define-roadmap`
- **No embedded criteria**: every criterion is cited from `rules/roadmap-quality.md`; a new criterion goes into that rule, not into this skill
- **A missing rule means halt**: with no yardstick, evaluation from impressions must not happen
- **No mode output**: the orchestration layer does its own context detection; this skill emits findings only
- **"Cannot evaluate" must be marked explicitly**: a dimension must not be recorded as passing because a tool was unavailable or an evidence source could not be read

### Anti-Patterns (Avoid)

- ❌ **Copying the criteria into the skill**: criteria maintained in two places inevitably drift, which is exactly what this skill is built to sidestep
- ❌ **Silently skipping the git-dependent dimension**: if the history cannot be read, say so; do not leave the reader thinking it was evaluated
- ❌ **Weighting severity subjectively**: severity comes mechanically from the mapping table, not from "this one feels more important"
- ❌ **Fixing the problem along the way**: evaluation mixed with rewriting leaves the author unable to see what the original problem was

### Skill Boundaries (Avoid Overlap)

| Action | Owner |
|---|---|
| Generate / rewrite the roadmap | `define-roadmap` |
| Change status / shift dates | `update-roadmap` |
| Promote / demote | `promote-roadmap-items` |
| Dependency identification | `map-item-dependencies` |
| Criteria maintenance | `rules/roadmap-quality.md` |
| Cross-layer governance diagnosis | `plan-next` |

---

## Self-Check

- [ ] `rules/roadmap-quality.md` loaded; halted when it was missing
- [ ] All five dimensions scanned
- [ ] Every finding carries all six fields
- [ ] Severity taken mechanically from the mapping table
- [ ] The change-frequency dimension went through "discover → run → handle the gap"; where it cannot be evaluated, the reason is written out
- [ ] The three criteria that depend on backlog item frontmatter had their evidence sources read; where they could not be read, they are marked "cannot evaluate" rather than recorded as passing
- [ ] The roadmap document was not rewritten
- [ ] No mode or other orchestration-layer field was emitted
- [ ] With zero findings, the pass was stated plainly

---

## Examples

### Example 1: Missing capacity baseline (mainstream case)

**Input**: a roadmap with a complete Now / Next / Later structure and a capacity allocation percentage table, but no total capacity baseline in the table header.

**Output** (excerpt):

```yaml
- location: "## Capacity allocation (current cycle)"
  category: executability
  severity: critical
  title: No total capacity baseline, so the downstream capacity guardrail cannot compute
  description: The capacity allocation gives only percentages and declares no total capacity baseline. The promote-roadmap-items formula is "percentage × total capacity baseline"; with no baseline there is no denominator, and the allocated capacity per goal cannot be computed. Measured against rules/roadmap-quality.md §2.
  suggestion: Add a total capacity baseline line to the capacity allocation header, in the form "<N> person-weeks (<headcount> people × <cycle length> − overhead, discounted to <60–70>% effective hours)". Step 8 of define-roadmap can be re-run to collect it.
```

**Result**: the author learns that the roadmap looks complete but will jam at the promotion step.

### Example 2: Not a git repository (edge case)

**Input**: the roadmap content is pasted directly by the user and lives in no git repository.

**Process**:

1. The first four dimensions scan normally.
2. Change-frequency dimension: the discover step establishes there is no git repository → the history cannot be read.
3. Mark the dimension "cannot evaluate — the input is pasted content, with no git commit history to count change frequency from".
4. **Do not infer from this that the dimension passes**, and do not invent a change-frequency finding either.

**Output** (excerpt):

```text
Dimensions that could not be evaluated:
- Soundness / change frequency: the input is pasted content, with no git commit history.
  To evaluate this dimension, supply the path to a roadmap.md inside a repository.
```

**Result**: the reader knows exactly which part went unchecked and will not assume every dimension passed.

### Example 3: Criteria file missing (edge case)

**Input**: a roadmap, in a project where `rules/roadmap-quality.md` is not installed.

**Process**:

1. Step 1, loading the criteria, fails.
2. **halt**; the scan is not entered.
3. State the reason: evaluating with no yardstick produces a list that looks authoritative and rests on nothing — more harmful than not evaluating at all.
4. Give the way out: install `rules/roadmap-quality.md` from AI Cortex, or name another criteria file explicitly.

**Result**: the skill refuses to produce conclusions with no yardstick, rather than assembling one from impressions.
