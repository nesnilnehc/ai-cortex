---
artifact_type: guide
created_by: ai-cortex
lifecycle: living
created_at: 2026-09-11
status: active
---

# Engineering quality governance

This guide explains how an adopting repository uses AI Cortex to constrain work before coding and converge it after coding. It is a usage map, not another source of quality criteria.

## 1. Asset responsibilities

| Asset | Owns | Must not own |
|---|---|---|
| `AGENTS.md` / `CLAUDE.md` | Project identity, non-negotiable invariants, workflow entry points and links to canonical assets | Detailed quality checklists, temporary lessons or copies of Rule text |
| Rules | Stable, independently verifiable obligations and default severity | Review steps, repair loops or project topology |
| `.ai-cortex/config.yaml` | Active profiles, module topology, protected contracts, targets, change budgets and waivers | Canonical Rule wording |
| Memory | Verified local facts, recent context and lessons that help future work | Normative policy, architecture truth or permanent waivers |
| Skills | Invocable procedures that gather evidence, evaluate Rules, aggregate findings or repair changes | A second copy of the criteria |
| Specs | The structure of requirements, designs, tasks, findings, Rules and waivers | The execution workflow |

Promote a repeated, verified memory lesson to its narrowest durable owner: project configuration for a local fact, an ADR for a decision, a Rule for a reusable constraint, a Spec for structure, or a Skill for procedure. Memory never overrides those owners.

## 2. Minimal project adoption

Keep the project entry file short. A project normally needs only:

```markdown
## Engineering governance

- Read `.ai-cortex/config.yaml` before design, review or repair.
- Before coding, review the applicable requirement, functional design, technical design and task list with the matching AI Cortex review Skills.
- After coding, run `orchestrate-code-review` for the engineering gate and `review-implementation-alignment` plus project acceptance tests for the functional gate.
- When either gate fails and repair is requested, use `orchestrate-repair-loop` until both pass or a stop condition is reached.
- Canonical quality criteria are the AI Cortex `rules/*-quality.md` Rule sets; cite Rule IDs rather than copying their text here.
```

Then add `.ai-cortex/config.yaml` with only profiles and parameters that are true for the project. A small library should not claim service, distributed-workflow or SLO profiles. A public service should not omit them merely to reduce findings. The installer leaves these project-scoped Rule sets in the canonical clone; the matched review Skill loads the applicable set in full instead of forcing every concern into every session.

## 3. Before coding

The artifact chain carries quality intent without duplicating policy:

| Layer | Quality content | Gate Skill |
|---|---|---|
| Requirement | Measurable Quality Attribute Scenarios when architecture or release can be affected | `review-requirements` |
| Functional design | Business workflows, states, permissions and exceptions; no engineering tactics | `review-functional-design` |
| Technical design | Scenario/Rule IDs mapped to system-specific tactics, trade-offs, verification and ownership | `review-technical-design` |
| Tasks | Affected scope, Rule IDs and concrete verification for quality-sensitive tasks | `review-tasks` |

Small changes may legitimately skip layers whose triggers are false. Record the reason and preserve the nearest valid parent; do not manufacture empty documents.

## 4. After coding

Engineering and functional correctness are sibling gates:

```text
                         ┌─ engineering gate ─ orchestrate-code-review ─┐
implemented change ─────┤                                               ├─ both pass ─ verified
                         └─ functional gate ─ alignment + acceptance ───┘
                                              │
                                              └─ failure ─ repair ─ rerun affected gates
```

- `orchestrate-code-review` aggregates language, framework, library, security, reliability, performance, architecture, observability and testing findings. It does not prove that the requested feature was implemented.
- `review-implementation-alignment` checks approved intent against production code and evidence. Test/acceptance execution proves observable behavior. Neither proves intrinsic engineering quality.
- `orchestrate-repair-loop` owns repetition and targeted edits. It consumes both gates; it does not replace or redefine them.

The runtime may execute gates in parallel or in the most efficient order. The semantic requirement is that both have current evidence after the final repair.

## 5. Rule selection and exceptions

Effective policy is canonical baseline + triggered profiles + project parameters. When a condition holds, its Rule is mandatory. A project-specific value is not a weaker alternative; it supplies the threshold or topology needed to evaluate the canonical item.

Use a waiver only for a narrow, temporary exception. Every waiver identifies the exact versioned Rule item, scope, reason, owner, approver, dates, compensating controls and evidence. Expired or invalid waivers produce findings normally.

## 6. Evidence and classic sources

Classic software books supply durable construction, design and reasoning principles. Current standards, platform documentation and project measurements supply normative or time-sensitive evidence. A book title or named pattern never substitutes for an applicable Rule ID and a concrete pass condition.

The curated [classic software engineering source map](../references/software-engineering-classics.md) records which books inform architecture, performance, reliability, testing, language-specific review and maintainer learning. It also records exclusions so language-specific or personal-development advice does not leak into universal engineering gates.

See [rule-modeling](../../specs/rule-modeling.md), [project configuration](./project-config.md) and [ADR 0012](../adr/0012-adopt-profiled-engineering-rules.md).
