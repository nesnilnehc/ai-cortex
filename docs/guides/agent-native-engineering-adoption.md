---
artifact_type: guide
created_by: ai-cortex
lifecycle: living
created_at: 2026-09-28
status: active
---

# Start using adaptive engineering

This is an optional starting path for a project that still uses requirements, designs, tasks, and existing review gates. The [Agent-Native Engineering RFC](../rfcs/agent-native-engineering.draft.md) proposes the architecture; [ADR 0015](../adr/0015-agent-engineering-governance-model.md) settles AI Cortex's asset ownership. Each adopting project decides whether and how to use the proposed model. This guide creates no approval requirement or universal schema.

## Start with L2 (adaptive SDLC) in ordinary work

Use a normal, bounded change in an adopting project. Keep its current canonical documents and applicable gates. There is no separate proof of concept to complete first.

To begin with an agent, use this request in the adopting project:

> For this change, follow our current canonical documents and applicable gates. Identify the goal, scope, acceptance conditions, constraints, and decision owner. Work in short verified steps, link material decisions and evidence to acceptance, and ask for a decision when intent is unclear or our local escalation rules require one. Do not change document authority without an explicit project decision.

1. **State the change.** In the project's existing canonical requirement or other declared source, identify the goal, scope, acceptance conditions, applicable constraints, and decision owner. Treat these linked facts as the local Change Contract; a new file is optional.
2. **Set local authority.** The project decides which implementation and document updates an agent may make directly, and which changes to intent, protected boundaries, or irreversible outcomes require a person. Record this in the project's existing entry point or governance, following its current approval rules.
3. **Work and verify in short cycles.** Let the agent inspect, choose a bounded action, act, verify, and revise its next step. Keep material decisions and evidence linked to the acceptance condition they affect. Amend the agreed goal or protected constraint through the project's decision owner.
4. **Keep SDLC handoffs usable.** Create or update a design or task when its existing trigger applies. Preserve links between those artifacts, the Change Contract, decisions, and evidence. Project-local formats and authority remain local.
5. **Use the existing quality gates.** Apply the relevant pre-coding reviews and the post-coding engineering and functional gates described in [Engineering quality governance](engineering-quality-governance.md). Have a reviewer or independent evaluation system judge the final evidence; the executor's claim alone is insufficient.

The first usable result is a completed change whose acceptance conditions, material decisions, and verification can be followed through the project's current handoff documents. Do not claim this result if an applicable gate or acceptance condition remains unverified.

## Prepare for L3 (agent-native engineering) only where needed

An adopting project can move its working core to the Change Contract, decisions, and evidence when it has decided:

- which record is authoritative for each kind of information;
- which generated SDLC documents are authoritative, for whom, and how their source and version are traced;
- how human edits, omissions, and conflicting versions are resolved; and
- what evidence an independent evaluator needs to judge completion.

These are project decisions. AI Cortex does not approve each local schema or projection. The RFC's L3 model remains proposed, and adopting it does not silently replace the project's current document authority.

## Add shared assets when a repeated need is clear

Use AI Cortex's existing [asset boundaries](../architecture/terminology.md) if adoption exposes a reusable gap:

| Repeated need | Asset to consider |
| --- | --- |
| A stable structure exchanged across projects | Spec |
| A verifiable constraint that applies beyond one project | Rule |
| A defined interaction among human, executor, and evaluator | Protocol |
| A repeatable agent task with clear inputs and outputs | Skill |

Keep project-specific fields, thresholds, authority, and projection mechanics in the adopting project. Publishing a shared asset is not a prerequisite for its routine engineering work.
