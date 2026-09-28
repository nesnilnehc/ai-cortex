---
artifact_type: adr
created_by: decision-record
lifecycle: snapshot
created_at: 2026-09-28
status: accepted
description: Assign reusable agent engineering governance to AI Cortex's existing asset types without owning execution or evaluation runtimes.
---

# ADR 0015: Agent Engineering Governance Model

## Context

AI Cortex already defines an asset library for delivery and governance through Specs, Protocols, Skills, and Rules. Its [mission](../project-overview/mission.md), [core terminology](../architecture/terminology.md), and [engineering quality guide](../guides/engineering-quality-governance.md) give those assets distinct owners. Current [artifact norms](../ARTIFACT_NORMS.md) also give requirements, designs, tasks, and ADRs established paths and authority.

The [Agent-Native Engineering RFC](../rfcs/agent-native-engineering.draft.md) proposes a bounded Change Contract, adaptive execution, escalation, evidence, independent evaluation, and SDLC compatibility for adopting systems. AI Cortex needs a local ownership boundary for any reusable governance definitions that emerge. The repository's existing four asset types already provide a place for those definitions; the RFC's integration interface and projection model remain proposals.

## Decision

AI Cortex owns **reusable governance semantics** for agent engineering through its existing four asset types. When a shared Change Contract or evidence structure is defined, its data contract belongs in a Spec; interaction among human, executor, and evaluator belongs in a Protocol; reusable constraints and escalation criteria belong in Rules; invocable analysis, review, or repair procedures belong in Skills. Local authority, thresholds, and protected boundaries remain with the adopting project.

AI Cortex does not own an adopter's execution state, evaluation runs, or instance evidence. It does not add a parallel `standards/` or `constraints/` taxonomy that duplicates `specs/` and `rules/`. Current artifact norms and existing gates remain authoritative until a separate decision changes them. This decision uses the repository's existing asset architecture; it creates no shared runtime schema or cross-system obligation.

## Alternatives

### Make AI Cortex an SDLC workflow engine

**Why rejected:** A fixed requirement-to-task sequence would put runtime orchestration in the governance library and make replanning depend on rewriting a process graph. It would also duplicate an adopting execution system's responsibility.

### Add parallel standards and constraints directories now

**Why rejected:** The same concepts already have owners in Specs, Protocols, Skills, and Rules. Parallel directories would create competing canonical sources before the shared contract is specified or tested.

### Leave the RFC as the only record

**Why rejected:** The RFC frames hypotheses across governance, execution, and evaluation roles. It cannot by itself record why AI Cortex should place future governance assets within its existing taxonomy rather than become an execution platform.

## Consequences

**Positive:** Future reusable contract, constraint, escalation, and evaluation definitions have a clear owner and path within the current asset architecture. Existing discovery and authority remain usable. Adopting systems can make their own implementation decisions.

**Negative / risks:** Mapping concrete agent engineering concepts into the four asset types may expose gaps that require a later decision. Existing SDLC-oriented assets need compatibility analysis before change; this ADR does not establish projection authority or remove gates.

**Neutral:** The cross-system model in the RFC remains a proposal. Each adopting system decides its own implementation; this ADR does not define a shared schema or require an implementation sequence.
