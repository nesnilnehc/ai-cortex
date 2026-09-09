---
artifact_type: rule
name: roadmap-quality
version: 1.0.0
scope: reviewing or self-checking a roadmap document
recommended_scope: user
status: active
---

# Rule: Roadmap Quality

> A review checklist for a roadmap artifact. Every item is independently verifiable.
>
> Applies to the roadmap document produced by [skills/define-roadmap](../skills/define-roadmap/SKILL.md) and stored at `docs/process-management/roadmap.md`, or at the project's conventional path.
>
> **This rule is the single authoritative source for roadmap criteria.** The producing side (`define-roadmap`), the diagnosing side (`plan-next`) and the reviewing side (`review-roadmap`) all cite this file rather than each maintaining its own wording.

---

## 5-dimension review

### 1. Completeness — is the structure all there?

- [ ] Every stage carries the four parts of the core model: milestone / strategic bets / metrics / promotion criteria
- [ ] A "capacity allocation" section is present and declares the **total capacity baseline** — person-weeks plus how it was derived
- [ ] Every strategic_goal has a percentage, and the percentages sum to 100%
- [ ] Each stage has 2–5 strategic bets, and none is empty

### 2. Executability — can the downstream consume it directly?

- [ ] The total capacity baseline exists. Without it, `promote-roadmap-items` has no denominator for "percentage × baseline" and the capacity guardrail cannot produce a result
- [ ] The engineering-health goal's capacity ≠ 0%
- [ ] Promotion criteria are decidable — they state which condition lets a stage enter the next one — rather than "it depends"
- [ ] The Now tier holds no more items than the WIP limit, 3–5 by default and overridable per project
- [ ] Every Now-tier item traces to the strategic_goal it belongs to

### 3. Clarity — is it unambiguous?

- [ ] **Metrics are triplets**: current value / target value / reference point. The reference is an industry benchmark, the project's own history, or an empirical threshold; where there is none, write 「项目自定（无外部基准）」
- [ ] Milestones use the outcome form (`让 [客群] 能够 [达成某事]，从而 [业务影响]`) rather than the name of a deliverable
- [ ] Strategic bets use the falsifiable hypothesis form (`我们相信 [做 X] 对 [人群] 会带来 [结果]，因为 [假设]`) rather than a noun phrase
- [ ] The Later tier states direction only, with no specific dates

### 4. Soundness — does this roadmap hold up?

- [ ] No feature list: items describe outcomes, not feature names. A bare feature name such as "dark mode" or "SSO" fails this item
- [ ] No TODOs mixed in: no execution-level tasks
- [ ] Dependencies are mapped: no Now-tier item has an unresolved prerequisite, and cross-item dependencies are recorded in each item's `depends_on`
- [ ] Priorities do not come from a single voice: each item's priority has a traceable score behind it, or an explicitly recorded strategic-override reason
- [ ] Change frequency is within the threshold: the roadmap has not been reordered repeatedly over a short period. The default threshold is at most 2 structural changes within one cycle, overridable per project

### 5. Traceability — can the impact of a change be located?

- [ ] Each stage goal maps to a goal in `docs/project-overview/strategic-goals.md`
- [ ] The constraint "the backlog must map onto the roadmap; anything not on the roadmap is not done by default" is stated explicitly
- [ ] The document records its last-updated date
- [ ] Stakeholder requests that were excluded, if any, are listed with their reasons in the "not doing this round" section

---

## Anti-patterns

Each corresponds to the failure mode of one dimension above, in the same order. On detecting one, go back to that dimension's checklist.

**§1 completeness failures**

- ❌ **Missing denominator**: percentages per goal with no total capacity baseline. The downstream "percentage × baseline" cannot be computed and the capacity guardrail becomes decorative

**§2 executability failures**

- ❌ **No capacity for governance**: the engineering-health goal allocated 0%. Technical debt and documentation have no capacity to draw on, so they always lose against competing value
- ❌ **Now tier piling up**: pulling in far more items than the WIP limit. It looks fully loaded while every item is waiting
- ❌ **Vague promotion criteria**: "it depends" instead of a decidable condition, which turns stage transitions into guesswork

**§3 clarity failures**

- ❌ **Metric with no reference point**: a target value alone, leaving the reader unable to tell whether it is ambitious or timid
- ❌ **A deliverable posing as an outcome**: a milestone written as "ship module X" rather than "let someone be able to do something"
- ❌ **A bet degraded into a noun**: a strategic bet with a name but no falsifiable hypothesis, so afterwards nobody can say whether the bet paid off

**§4 soundness failures**

- ❌ **A feature list posing as a roadmap**: feature names throughout, with no sense of why they are being built or what counts as success
- ❌ **Ordering without checking dependencies**: sorting by priority and capacity alone, so a blocked item enters Now and occupies capacity without producing anything
- ❌ **Priority with nothing behind it**: neither a score nor a recorded strategic-override reason, so nobody can reconstruct afterwards why the order was what it was
- ❌ **Reordering mistaken for responsiveness**: restructuring on every new piece of information, past the change-frequency threshold, without pausing to reflect

**§5 traceability failures**

- ❌ **Broken goal mapping**: a roadmap item that maps to no strategic goal, leaving "which goal does this serve?" unanswerable
- ❌ **Exclusions left unwritten**: relying on the implicit rule "anything not on the roadmap is not done", so every excluded stakeholder comes to ask individually

**Cross-cutting failure**

- ❌ **Capacity allocated to the last drop**: percentages taken against calendar capacity rather than effective capacity, so one urgent problem derails everything

---

## Basis for the criteria

The dimensions and failure modes above are derived from this rule's own five-dimension structure. Where a general product-management concept is involved, the primary source is a published work, listed here for traceability and further reading:

| Concept | Primary source |
| :--- | :--- |
| Now / Next / Later tiers; a roadmap is a plan, not a commitment | McCarthy, Lombardo, Ryan, Connors, *Product Roadmaps Relaunched* (2017) |
| The RICE scoring scale and confidence anchors | Intercom, "RICE: Simple prioritization for product managers" (2016) |
| The falsifiable hypothesis form | Gothelf & Seiden, *Lean UX* |
| Outcomes over feature lists — the cost of the feature factory | Melissa Perri, *Escaping the Build Trap* |
| Avoiding priority set by individual opinion (HiPPO) | Avinash Kaushik, *Web Analytics: An Hour a Day* |

---

## Related assets

- **Producing side**: [skills/define-roadmap](../skills/define-roadmap/SKILL.md) — constructs the roadmap against this checklist
- **Reviewing side**: [skills/review-roadmap](../skills/review-roadmap/SKILL.md) — produces findings against this checklist
- **Consuming side**: [skills/promote-roadmap-items](../skills/promote-roadmap-items/SKILL.md) — the consumer of the capacity and WIP criteria
- **Sibling review rules**: [requirement-quality](./requirement-quality.md) / [functional-design-quality](./functional-design-quality.md) / [technical-design-quality](./technical-design-quality.md) / [task-quality](./task-quality.md)
