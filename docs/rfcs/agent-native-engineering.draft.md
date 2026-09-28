---
artifact_type: rfc
created_by: ai-cortex
lifecycle: snapshot
created_at: 2026-09-28
status: proposed
description: A cross-project architecture proposal for adaptive agent execution with an SDLC compatibility layer.
---

# Agent-Native Engineering: From SDLC Workflow to Adaptive Engineering

This RFC proposes an engineering model that AI Cortex can define and adopting execution and evaluation systems can use. It defines architectural direction without changing existing asset contracts or requiring an adopter's implementation. [ADR 0015](../adr/0015-agent-engineering-governance-model.md) records AI Cortex's accepted governance boundary; the cross-system model here remains proposed.

## Context

Many teams organize the software development life cycle (SDLC) around requirements, designs, tasks, implementation, review, and release. Those artifacts support accountability, coordination, acceptance, and audit. AI Cortex currently models several of them as canonical sources in [Artifact norms](../ARTIFACT_NORMS.md), and its [engineering quality guide](../guides/engineering-quality-governance.md) already allows small changes to omit design layers when their triggers are absent. Both facts must survive a transition.

Coding agents also learn material facts while exploring code, changing it, and running checks. A common Plan Mode pattern asks for a complete plan to be approved before that exploration, so the plan can become stale. Yet a purely local act-and-adjust loop can drift across architecture, data, security, or compatibility boundaries. Large or risky changes still need explicit design and human decisions.

The problem is how to let execution replan as evidence arrives while keeping stable intent, applicable constraints, reviewable decisions, and the organizational SDLC interfaces that people still use.

## Core Thesis

Planning is an ongoing activity; a plan document is one possible artifact. Plan Mode remains useful when advance design reduces material risk, but a complete static plan need not be the default for every change. Execution may revise its next steps when new information invalidates an assumption. Intent, acceptance conditions, architecture constraints, and consequential decisions require more stability than the step list.

Governance should increasingly state the permitted outcome and operating boundaries, then check what happened. This is a proposed shift in emphasis from prescribing every process step to governing constraints, escalation, and evidence. It does not remove required approvals, designs, or audit records. Their need depends on risk and organizational obligations.

| Classification | Statement | Status in this repository |
| --- | --- | --- |
| Existing authority | AI Cortex owns reusable Spec, Protocol, Skill, and Rule assets; its current artifact paths and canonical sources remain governed by [Artifact norms](../ARTIFACT_NORMS.md) and [core terminology](../architecture/terminology.md). | In force |
| Proposed architectural decision | Use a Change Contract as the stable reference for a bounded change, with linked constraints, decisions, execution state, evidence, and evaluation. | Proposed here; schemas are not defined |
| Proposed architectural decision | Keep an SDLC Compatibility Layer so current organizational artifacts and agent execution can coexist. | Proposed here; current SDLC sources remain authoritative |
| Proposed architectural decision | Separate governance definitions, execution, and independent evaluation across participating systems. | Proposed integration boundary, subject to each adopter's own decision process |
| Hypothesis | For suitable changes, adaptive execution with risk-triggered design will reduce rework or review burden without lowering acceptance or quality. | Assess through adoption experience; not an established outcome |
| Hypothesis | Some SDLC artifacts can eventually be generated as projections of a shared change model. | Requires mapping, ownership, and audit validation; not current policy |

## Durable Artifacts

The following are conceptual information categories, not new schemas or directories. Existing AI Cortex [asset types](../architecture/terminology.md) remain the owners of any normative definitions adopted later.

| Category | Minimum durable meaning | Why it persists |
| --- | --- | --- |
| Change Contract | Intent, scope, exclusions, acceptance conditions, owner, and links to applicable constraints | Anchors the requested outcome when execution steps change |
| Constraints | Applicable project and organization rules, protected interfaces, architecture boundaries, and approval limits, with source references | Defines what execution may not violate |
| Decisions | A material question, alternatives, rationale, authority, outcome, and effect on the contract | Makes consequential choices reviewable and recoverable |
| Evidence | A trace from each acceptance or constraint claim to a change, test, inspection, runtime observation, or acknowledged gap, including result and provenance | Lets a reviewer distinguish verified outcomes from agent assertions |
| Evaluation | Findings and disposition against the contract and constraints, referencing the evidence inspected | Supports an independent completion judgment |

Execution state holds current hypotheses, discovered context, next actions, completed actions, and blockers. It can be revised frequently; a task list is not automatically a permanent artifact. A durable decision or evidence link must survive those revisions. The exact fields, storage locations, identifiers, and lifecycle rules remain open design work.

The Change Contract is stable **within an approved scope**, not immutable. A change to intent, acceptance, or a protected constraint requires an explicit amendment and, where applicable, renewed human authorization. This prevents replanning from silently changing the requested outcome.

## Adaptive Execution Model

Verification feeds both replanning and the evidence used for evaluation.

```mermaid
flowchart LR
    contract["Change Contract and applicable constraints"] --> understand["Understand"]
    understand --> decide["Decide"]
    decide --> act["Act"]
    act --> verify["Verify"]
    verify -->|"More work"| adjust["Adjust"]
    adjust -->|"Replan"| understand
    verify --> evidence["Evidence"]
    evidence --> evaluation["Evaluation"]
```

1. **Understand:** inspect the request, repository, constraints, and uncertainty. Record assumptions that could alter the approach.
2. **Decide:** choose the next bounded action. Persist material design choices and escalate those outside delegated authority.
3. **Act:** execute within the contract and applicable controls.
4. **Verify:** gather direct evidence against acceptance conditions and relevant constraints; record failures and gaps.
5. **Adjust:** revise the next actions from the evidence. Amend the contract only through the appropriate authority.

Completion requires a current evaluation of the final change and its evidence. A long upfront plan remains useful when it reduces risk: for example, changes to service boundaries, authorization, shared data models, migration paths, or external contracts. Risk-triggered design is compatible with continuous replanning.

## Human Escalation

The agent may choose local, reversible implementation steps when they fit the approved contract and constraints. It must stop the affected action and present a decision when authority, intent, or consequences exceed that scope. The table describes candidate policy triggers; precise thresholds and approvers must be defined by the adopting project or organization.

| Trigger | Proposed response |
| --- | --- |
| Ambiguous intent or conflicting acceptance conditions | Clarify with the request owner before choosing an interpretation |
| Material change to architecture, service boundary, shared data model, or permission model | Present options, impact, and recommendation to the designated decision owner |
| Breaking external interface, destructive data action, or hard-to-reverse operation | Obtain explicit authorization before the affected action |
| Security or compliance boundary without a clear applicable rule | Stop the affected action and escalate to the accountable owner |
| Evidence cannot establish an acceptance condition or a required quality gate | Report the gap; do not claim verified completion |

An escalation should identify the exact question, feasible options, recommendation, affected contract terms, expected impact, reversibility, and evidence available. Review the consequential choice rather than every small execution step. Existing repository and organization approval rules take precedence over this proposed default.

## Dual-Mode Engineering Architecture

The proposed compatibility layer keeps organizational SDLC artifacts connected to an adaptive execution core:

```mermaid
flowchart TB
    subgraph sdlc [SDLC mode]
        organization["People and organizational artifacts"]
    end
    compatibility["SDLC compatibility layer: mapping and provenance"]
    subgraph native [Agent-native mode]
        contract["Change Contract and constraints"]
        execution["Decisions and adaptive execution"]
        evidence["Evidence"]
        evaluation["Independent evaluation"]
    end
    organization --> compatibility
    compatibility --> contract
    contract --> execution
    execution --> evidence
    evidence --> evaluation
```

**SDLC Mode** preserves the artifacts, approvals, and handoffs an organization needs today. **Agent-native Mode** works from intent and constraints, replans execution, and supplies evidence for evaluation. The compatibility layer translates between them while preserving source provenance and the authority of the originating artifact.

At first, a one-way mapping from an existing requirement, design, or task to the corresponding change information is sufficient. Automatic reverse generation and two-way synchronization are hypotheses, not prerequisites. A generated view must identify its source, version, omissions, and any human-authored additions. It must not quietly overwrite an authoritative SDLC document. Promoting a view to a canonical source would require a separate change to [Artifact norms](../ARTIFACT_NORMS.md) and the affected asset contracts.

## Project Boundaries

| Role | Proposed responsibility | Boundary |
| --- | --- | --- |
| AI Cortex | Define reusable governance semantics through its existing Specs, Protocols, Rules, and Skills: contract structures, constraint and escalation rules, evaluation vocabulary, and capability guidance | Does not own another project's execution state, review runs, or every instance of evidence |
| Adopting execution system | Execute a bounded change, maintain adaptive runtime state, collect evidence, invoke escalation and evaluation, and assemble release output | Consumes governance definitions; does not make itself the sole judge of its own success |
| Independent evaluation system | Evaluate a change against intent, constraints, decisions, and evidence, returning findings and an evaluation result | Does not own the execution loop or redefine the governing contract |

These boundaries are recommendations for future adoption, not claims that any implementation already exposes these interfaces. A shared semantic contract should avoid dependencies on one system's runtime representation.

## Migration Strategy

The levels describe modes of adoption, not mandated versions or dates. A team can retain a lower level where risk, regulation, or coordination calls for it.

| Level | Operating model | Admission to the next level |
| --- | --- | --- |
| **L1 — SDLC Assisted** | Requirements, designs, tasks, review, and release remain the working structure; agents assist within existing gates. | Select a bounded change and establish an explicit contract, escalation owner, and acceptance evidence. |
| **L2 — Adaptive SDLC** | The organization keeps SDLC artifacts; the agent executes from a Change Contract and creates or updates design and tasks when their triggers arise. Evidence and material decisions are linked to acceptance. | Demonstrate reliable provenance, risk-triggered escalation, independent evaluation, and usable SDLC handoffs. |
| **L3 — Agent-native Engineering** | Intent, constraints, decisions, execution, evidence, and evaluation form the working core; SDLC artifacts are produced when organizational consumers need them. | No automatic promotion. Adopt only after the organization accepts the authority, audit, and synchronization model. |

L2 is the near-term adoption path. L3 remains a hypothesis. No level removes an approval or artifact that a project currently requires.

## Adoption and Revision

Adopting systems may apply this proposal through their own architecture and delivery decisions. They can retain existing SDLC interfaces while introducing the Change Contract, adaptive execution, and evidence links incrementally.

When adoption reveals a material mismatch, update this RFC with the observed constraint, the revised proposal, and its compatibility impact. Project-specific implementation choices remain local. Shared Specs, Protocols, or Rules should be added only when a reusable contract or constraint becomes clear.

This RFC does not yet define shared schema fields, escalation thresholds, evidence identifiers, projection authority, or contract versioning. These details are settled when an adopting system encounters a concrete need; a change to AI Cortex's canonical artifacts still follows the relevant repository rules.
