---
artifact_type: rule
name: agentic-artifact-paradigm
version: 1.0.0
scope: 输入到 spec 制品的智能体能力
recommended_scope: user
lifecycle: living
created_at: 2026-06-28
status: active
---

# Rule: Agentic Artifact Production Paradigm

> For any agent capability that turns messy input into an artifact conforming to a spec, **the quality framework is scaffolding, not an agenda**.
>
> **Position**: this rule governs the **paradigm** — how an agent treats structure against substance. It does not govern the shape of a particular artifact (that belongs to each `*-modeling.md` spec) nor its particular quality criteria (each `*-quality.md`). It is the **shared higher-order principle** above both.
>
> **When it applies**: whenever an "input → spec artifact" agent capability is designed or implemented, whether interactive (clarification, design) or one-shot (review, assessment).

---

## 1. Scope

Any agent capability that **turns messy input into an artifact conforming to a spec**:

- **Interactive**: requirement clarification (→ requirement spec), technical design (→ technical design spec), test case generation (→ test case spec).
- **One-shot**: code or requirement review (→ review dimension structure), coverage assessment (→ assessment report spec).

**Does not apply**: free generation with no target spec, such as open-ended conversation or plain code completion. There is no "framework" there, so the paradigm has nothing to act on.

---

## 2. Core proposition

> **An artifact's quality framework — a spec's sections, a review's dimensions — is scaffolding and a presentation form, not the agenda for the interaction or the generation. The agent leads with substance and structure follows; the framework fills in quietly through extraction and inference, and appears only in the product. It is never a checklist for interrogating field by field or scoring dimension by dimension. The quality rule is the convergence oracle — and the oracle itself must be substance-driven, never reduced to filling in a form.**

Two opposites, in one line each:

- **Scaffolding (right)**: the framework is the **target the artifact converges on, and its presentation structure**. It fills in the background.
- **Agenda (wrong)**: the framework is a checklist **driving what the agent does next** ("which field is empty?", "which dimension do I score next?") → inevitably hollow, and identical for every input.

---

## 3. Constraints

1. **Structure is scaffolding, not an agenda**: a spec's sections and a review's dimensions define the **target structure and its presentation**. They must not be used as the driving sequence for interaction or generation. **Never** advance the agent by asking "which spec section is empty?" or "which dimension do I score next?".

2. **Substance-led**: the agent's **foreground** is domain substance — how this requirement actually works, what this code actually does, what really matters in this review. Questions and findings must be **domain substance**, not "please supply field X" or "score dimension Y at N".

3. **Extract first, interrogate and score last (extract-first)**: fill the framework's fields and dimensions first by **extraction** (upstream artifacts, existing sources) and **inference** (from the substantive conversation itself). Only what is **genuinely missing, unrecoverable by inference, and critical** is escalated to a direct question. **Never** deduct points for, or ask about, anything extractable from upstream, provided by the platform, or inferable.

4. **The quality rule is the convergence oracle (quality-as-oracle)**: the corresponding `*-quality.md` is the **convergence target** — the agent converges the artifact until it meets those criteria (interactive: continue the substantive conversation; one-shot: dig until findings span the dimensions). **Never** build a parallel "completeness or coverage check" that duplicates the quality criteria.

5. **Guard the oracle against becoming a form (anti-form-filling oracle)**: quality verification must be **driven by substance** — real findings, real gaps — and fed back as a **convergence signal**. **Never** let it decay into a per-dimension scorecard that drives nothing. That merely swaps "filling in fields" for "filling in score dimensions"; same illness, different name.

---

## 4. Instantiation parameters — four per capability, paradigm unchanged

The paradigm is fixed; capabilities differ only in four parameters. This is what makes it "one paradigm, parameterised per scenario" rather than "one workflow per capability":

| Parameter | Meaning | Clarification (example) | Review (example) |
|---|---|---|---|
| **Target spec** | The structure to converge on | requirement-modeling | Review dimension schema |
| **Substance lens** | What "substance" means here | How the feature works | What really matters in this change |
| **Extraction sources** | Where the framework fills from | ZenTao + the repository | The diff + repository context |
| **Interaction model** | How convergence happens | Multiple interactive rounds | One-shot deep dig |

---

## 5. Bad Patterns

- ❌ Clarification asking one by one about the empty required fields — requirement source, risks, dependencies — turning schema gaps into an interrogation agenda
- ❌ A review scoring each dimension without surfacing what really matters in THIS change — form-filling dressed as scoring
- ❌ Deducting points for, or asking about, content already supplied upstream, provided by the platform, or inferable
- ❌ Building a parallel "completeness check" alongside the `*-quality` criteria — duplication that then drifts
- ❌ Quality verification producing only a final scorecard that is not fed back into substantive convergence
- ❌ Writing this paradigm in the shape of one interactive capability (a "five-phase interaction skeleton") and treating it as cross-scenario. An interaction skeleton belongs to an **interactive instance**, not to this paradigm

---

## 6. Remediation

1. **Framework turned into an agenda**: replace "fill the next empty field / score the next dimension" with "ask or find the most valuable piece of domain substance", and let the framework recede to a background convergence target.
2. **Interrogating what is extractable**: connect the extraction sources (upstream artifacts, the platform's capability list). Extract and infer first; ask directly only about what is genuinely missing and critical.
3. **Parallel completeness check**: delete it and use `*-quality.md` as the single convergence oracle.
4. **Form-filling oracle**: drive quality verification from substantive findings, and treat its output as a convergence signal rather than a final score.
5. **Paradigm written in an interaction shape**: push the interaction-specific phases down into the concrete instance design, and keep only the higher-order principles that are decoupled from the interaction model here.

---

## 7. Related assets

- **Convergence oracles (the quality criteria)**: the artifact's `rules/*-quality.md`. For example [requirement-quality](./requirement-quality.md) / [functional-design-quality](./functional-design-quality.md) / [technical-design-quality](./technical-design-quality.md) / [task-quality](./task-quality.md) / [test-case-quality](./test-case-quality.md) / [test-coverage-quality](./test-coverage-quality.md).
- **Target structures (the data contracts)**: `specs/*-modeling.md` — the "scaffolding" in this paradigm is the structure those specs define.
- **Instantiation by consumers**: each project instantiates this paradigm into concrete capabilities, interactive or one-shot, by filling in the four parameters from §4. That instantiation design stays local to the project and is not fed back into this rule.

---

## Change log

### 1.0.0 — 2026-06-28

**Initial Release**: defines four constraints — structure is scaffolding not an agenda, substance-led, extract-first, quality-as-oracle with the oracle itself guarded against form-filling — plus four instantiation parameters. It came out of a root-cause analysis of hollow form-filling questions in interactive clarification, and was cross-validated against one-shot review as a **higher-order principle decoupled from the interaction model**.
