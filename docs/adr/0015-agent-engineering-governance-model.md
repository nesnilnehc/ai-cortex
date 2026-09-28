---
artifact_type: adr
created_by: decision-record
lifecycle: snapshot
created_at: 2026-09-28
status: proposed
description: Position AI Cortex as the reusable governance owner for adaptive agent engineering without adding a parallel asset taxonomy.
---

# ADR 0015: Agent Engineering Governance Model

## Context

AI Cortex already defines an asset library for delivery and governance through Specs, Protocols, Skills, and Rules. Its [mission](../project-overview/mission.md), [core terminology](../architecture/terminology.md), and [engineering quality guide](../guides/engineering-quality-governance.md) give those assets distinct owners. Current [artifact norms](../ARTIFACT_NORMS.md) also give requirements, designs, tasks, and ADRs established paths and authority.

The [Agent-Native Engineering RFC](../rfcs/agent-native-engineering.draft.md) proposes a bounded Change Contract, adaptive execution, escalation, evidence, independent evaluation, and SDLC compatibility for adopting systems. AI Cortex needs a local ownership decision before adding any related assets. The RFC's integration interface and projection model remain proposals; this ADR does not enact them.

## Decision

Propose that AI Cortex own the **reusable governance semantics** for agent engineering through its existing four asset types. A future Change Contract or evidence structure belongs in a Spec; interaction among human, executor, and evaluator belongs in a Protocol; applicable constraints and escalation triggers belong in Rules; invocable analysis, review, or repair procedures belong in Skills. Local authority, thresholds, and protected boundaries remain with the adopting project.

Keep AI Cortex independent of a particular execution runtime and evaluator. Do not create a second `standards/` or `constraints/` taxonomy that duplicates `specs/` and `rules/`. Continue to treat current artifact norms and existing gates as authoritative until a separate, reviewed change updates them. This is a proposed repository decision, with no new runtime requirement or schema in force yet.

## Alternatives

### Make AI Cortex an SDLC workflow engine

**Why rejected:** A fixed requirement-to-task sequence would put runtime orchestration in the governance library and make replanning depend on rewriting a process graph. It would also duplicate an adopting execution system's responsibility.

### Add parallel standards and constraints directories now

**Why rejected:** The same concepts already have owners in Specs, Protocols, Skills, and Rules. Parallel directories would create competing canonical sources before the shared contract is specified or tested.

### Leave the RFC as the only record

**Why rejected:** The RFC frames hypotheses across governance, execution, and evaluation roles. It cannot by itself record why AI Cortex should place future governance assets within its existing taxonomy rather than become an execution platform.

## Consequences

**Positive:** The repository has a clear proposed owner for future contract, constraint, escalation, and evaluation definitions. Existing asset discovery and authority remain usable. Adopting execution and evaluation systems can make their own implementation decisions against the same proposed semantics.

**Negative / risks:** The conceptual contract is not yet machine-readable, so integrations remain speculative. AI Cortex's current SDLC-oriented assets will require careful compatibility analysis before any change; this ADR alone cannot establish projection authority or remove gates. Agreement with adopters and a bounded PoC are needed before accepting an interface.

**Neutral:** This ADR is `proposed`. It records a reviewable choice and does not change current AI Cortex norms or an adopter's implementation.
