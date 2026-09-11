---
artifact_type: adr
created_by: decision-record
lifecycle: snapshot
created_at: 2026-09-11
status: accepted
description: Adopt versioned engineering quality rules with risk profiles, project parameters and auditable waivers instead of an umbrella governance skill
---

# ADR 0012: Adopt profiled engineering quality rules

## Context

AI Cortex already separates Specs, Protocols, Skills and Rules, and states that review criteria live outside review Skills. The existing cognitive review Skills nevertheless embed architecture, security, performance and testing checklists. The repository also has no canonical rule model for stable rule identifiers, applicability, evidence, enforcement strength or waivers. This makes criteria difficult to reuse before coding, difficult to configure for different project types, and difficult to audit after a review.

An umbrella `engineering-governance` Protocol and `orchestrate-engineering-governance` Skill were considered as the way to connect the phases, and were not built. The Protocol would have had no two actively interacting roles, and the Skill would only have routed existing capabilities while depending on review capabilities that did not yet exist. Either would add a layer with no distinct contract and no independently testable outcome.

## Decision

Adopt a four-part policy stack:

1. `specs/rule-modeling.md` defines the data contract for modeled Rule documents, project profiles and waivers.
2. Canonical engineering criteria live in versioned `rules/*-quality.md` Rule sets with stable item identifiers, explicit applicability, evidence, pass conditions and remediation.
3. Atomic `review-*` Skills load and execute the applicable Rule sets and emit `findings-list`; they do not restate the criteria.
4. `orchestrate-code-review` aggregates the engineering gate, while `orchestrate-repair-loop` converges two sibling gates: engineering quality and functional correctness.

Rules are layered rather than copied:

- **Baseline rules** apply to every relevant project.
- **Profiles** activate conditionally mandatory rules for contexts such as a deployable service, public API, sensitive-data path, distributed workflow or high-volume workload.
- **Project parameters** declare topology, protected contracts, quality targets and change budgets without redefining canonical rules.
- **Waivers** are narrow, reasoned, owned, time-bounded and auditable. A project cannot silently turn a baseline rule off.

Quality attributes enter the delivery chain at three points: measurable scenarios in requirements, tactics and verification in technical design, and rule references plus evidence in tasks. Post-coding alignment review compares those artifacts with the implementation; repair consumes both engineering findings and functional failures.

## Alternatives

- **Keep quality principles only in `CLAUDE.md` or `AGENTS.md`**: rejected. The entry point should remain a constitution and router; a long checklist is hard to distribute, version, select and verify independently.
- **Embed every checklist in its review Skill**: rejected. Producers, reviewers and repair loops would maintain different copies, contradicting the repository's single-source-of-truth principle.
- **Create one umbrella governance Skill and Protocol**: rejected. Routing alone is not a unique capability, the proposed Protocol has no genuine multi-party interaction, and a global sequence would force heavyweight artifacts onto small changes.
- **Make every rule globally mandatory with fixed thresholds**: rejected. Some requirements are universal, but topology and thresholds depend on runtime shape and business risk. Treating context as an opt-out would either over-block small libraries or under-govern critical services.
- **Let each adopting project fork the Rule files**: rejected. Forks drift and make updates untraceable. Projects should select profiles and supply parameters while the canonical Rule IDs remain stable.

## Consequences

- Review criteria become reusable before coding, during implementation and after coding without duplication.
- A rule can move from judgment-based review to deterministic tooling without changing its identity.
- Adopting projects configure context and thresholds instead of rewriting policy, while exceptional departures remain visible and expire.
- Rule authors take on schema and compatibility obligations: identifiers are never reused, breaking semantic changes require a major version, and new blocking rules require validation against representative project shapes.
- The initial implementation adds more Rule documents and atomic review Skills, but declines the premature umbrella assets and keeps `AGENTS.md` and `CLAUDE.md` free of duplicated policy.
