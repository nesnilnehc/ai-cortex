---
artifact_type: rule
name: requirement-intake-triage
version: 1.0.0
created_by: ai-cortex
lifecycle: living
created_at: 2026-06-18
recommended_scope: user
status: active
---

# Rule: Requirement Intake Triage

> A shared vocabulary, decision criteria and soundness lenses for triaging raw intake — a pile of ZenTao requirement fields, for instance — by what it actually is.
>
> **Position**: intake is the raw input that arrives **before** a requirement exists, and is not assumed to conform to [specs/requirement-modeling.md](../specs/requirement-modeling.md). This rule classifies what a lump of input fundamentally is; only intake classified as a requirement goes on to be judged against requirement-modeling.
>
> **Consumers**: upstream clarification (which routes to a different clarification workflow per kind) and downstream review (which picks a different soundness lens per kind) share this vocabulary as the single diagnostic SSOT. Cite it across repositories with the anchored version `requirement-intake-triage@1.0.0`.

---

## 1. The kind axis — one decision question, MECE

The decision question is: **"which single thing is this item mainly expressing?"** One question fixes one kind.

| Kind | What it expresses | Category |
|---|---|---|
| **Functional requirement** | A user-facing capability need waiting to be met | Is a requirement |
| **Non-functional requirement** | A quality attribute target waiting to be reached (performance / security / maintainability / scalability) | Is a requirement |
| **Design proposal** | "How to build it" — an implementation approach or a technology choice | Not a requirement |
| **Task** | "Which unit of work to carry out" — an action waiting to be executed | Not a requirement |
| **Defect** | "The existing behaviour is broken" — a defect | Not a requirement |
| **Insufficient information** | None of the above cores can be identified | Fallback |

- **Mutual exclusivity** comes from the singleness of the decision question; boundary ambiguity is cut by the tie-breaks in §2.
- **Exhaustiveness** comes from "insufficient information" as the fallback — any intake whose core cannot be identified lands there.
- The two "is a requirement" kinds are defined by the types in [specs/requirement-modeling.md](../specs/requirement-modeling.md); this rule does not redefine them.

---

## 2. Decision questions and tie-breaks

Apply the single questions in order and classify on the first hit. Where several kinds look plausible, cut with the tie-breaks:

- **Can you not even tell whether this is a feature change, a bug fix, or technical work?** Yes → **insufficient information** (the fallback has the highest precedence, on a deliberately narrow trigger: only when the kind is entirely undecidable).
- **Has existing behaviour departed from an established expectation (a fault, a regression, falling below a known baseline)?** Yes → **defect**.
- **Does it set a new target for a quality attribute (a metric, a baseline)?** Yes → **non-functional requirement**.
- **Does it add or change a user-facing capability?** Yes → **functional requirement**.
- **Is it saying "how to do it" (an implementation structure, a technology choice), or is it pointing at a deliverable unit of work?** The former → **design proposal**; the latter → **task**.

Tie-breaks:

- **Design proposal vs task**: when both look plausible, check whether it points at a deliverable unit of work — if it does → task; if it is only a technical leaning → design proposal.
- **Defect vs non-functional**: departing from an established baseline → defect; setting a new target → non-functional requirement.
- **Defect vs functional**: it once worked, or was once specified → defect; it did not exist before → functional requirement.
- **Design proposal serving business vs serving technology**: if the goal you work back to lands on a user or business outcome → work it back into a functional requirement; if it lands on a system or technical metric and is self-consistent → it is genuinely reasonable technical work, so classify it as a task.

---

## 3. An orthogonal attribute: completeness

Completeness is independent of kind and **does not belong on the kind axis**. A functional requirement can be either "complete" or "partially missing".

| Completeness | Criterion |
|---|---|
| Complete | The core that kind requires is fully present |
| Partially missing | The core is identifiable but a key element is absent |

---

## 4. Soundness lenses per kind

Review runs on soundness as its spine — judging whether the logic and the business case hold — not on format. Each lens splits into two columns:

- **Assertable**: a conclusion can be drawn from the text alone (level confusion / a gap between means and ends / not acceptance-testable / internal contradiction).
- **Ask, do not assert**: it depends on business context, so only probe and flag the risk. **Do not pass judgement** (whether the business value is real / priority / market judgement).

| Kind | Assertable lens | Ask-only lens |
|---|---|---|
| Functional requirement | Internally coherent, solution matches problem, the acceptance implies the goal | Whether the value is real, priority |
| Non-functional requirement | The metric is concrete, has a baseline, is measurable | Whether that target level is worth it |
| Design proposal | **Work back to the implied requirement**; judge whether it holds, whether the approach fits the problem, whether it is over-engineered; not acceptance-testable | The business value of the requirement worked back to |
| Task | Work back to the requirement it serves; technical necessity, blast radius | Priority, ROI |
| Defect | Clarity of root cause, blast radius, reliability of reproduction | Fix priority |
| Insufficient information | Note what is missing; do not force it into a kind | — |

**The key discipline for design proposals and tasks**: work back to the implied requirement and judge whether that holds. **Do not judge the technical merit of the design or the task** — scoring their technical detail rewards filing the wrong kind of item.

---

## 5. How consumers differ in what they do next

Diagnosis (§1–§4) is shared; what happens next varies by the consumer's interaction model and is **not** shared.

| Consumer | Interaction model | What it does |
|---|---|---|
| Upstream clarification | Multiple rounds | Route to a different clarification workflow by kind: design or task → work back to the requirement; defect → the bug clarification flow; insufficient information → start from scratch; is a requirement → fill the gaps as normal |
| Downstream review | One-shot | Pick the soundness lens by kind, then diagnose and score without fixing. Non-requirement kinds get a low score plus the requirement worked back to, and are not sent back |

---

## Anti-patterns

- ❌ Forcing a completeness grade onto the kind axis — kind measures "what it is", completeness measures "how much of it there is", and the two axes are orthogonal
- ❌ Judging the technical merit of a misfiled design proposal or task, instead of working back to the requirement and judging its soundness
- ❌ Forcing anything unidentifiable into some kind rather than classifying it as insufficient information
- ❌ Running review on format — which section is missing — as its spine, rather than on soundness
- ❌ Passing business judgement through an ask-only lens; with no business context the model can only probe

---

## Change log

### 1.0.0 — 2026-06-18

**Initial Release**: defines the 6-kind triage vocabulary for requirement intake (functional requirement / non-functional requirement / design proposal / task / defect / insufficient information), the decision questions, the tie-breaks, completeness as an orthogonal attribute, the soundness lens per kind split into assertable and ask-only, and how consumers differ in what they do next. Pairs with the type narrowing in [specs/requirement-modeling.md](../specs/requirement-modeling.md), where defect and technical task are demoted to triage labels.
