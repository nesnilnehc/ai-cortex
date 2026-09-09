---
artifact_type: roadmap
created_by: define-roadmap
lifecycle: living
created_at: 2026-03-24
status: active
---

# Roadmap

**Last updated**: 2026-03-22

The path of evolution derived from the [strategic goals](../project-overview/strategic-goals.md). A roadmap is mostly about the **road** — the themes, the initiatives, the direction; a **milestone** is only a significant point along it. The concrete work is in the [backlog](backlog.md).

## The road at a glance

- **Now**: widen intent coverage and reach more channels in the ecosystem.
- **Next**: deeper reuse and richer orchestration. (Entry condition: intent coverage hits its target and the new channels are verified.)
- **Later**: standardisation across the ecosystem, and measuring usage.

---

## Now

**Strategic goals it serves**: [Goal 1, delivery-chain capabilities are discoverable](../project-overview/strategic-goals.md#goal-1-delivery-chain-capabilities-are-discoverable) and [Goal 2, governance-chain capabilities are discoverable](../project-overview/strategic-goals.md#goal-2-governance-chain-capabilities-are-discoverable)

**What success looks like**: once the Now milestones are met, core delivery and governance intents are 80% covered.

### Milestones

- **M5, core intent coverage**: full coverage of the core delivery and governance intents, enough for most everyday software engineering situations.
- **M6, multi-channel verification**: verify integration across platforms in the ecosystem, lowering adoption friction further.

### Key initiatives

- **Grow the core skill library**: design and build more finely divided delivery and governance skills on top of `intent-routing`, closing the capability gaps.
- **Verify cross-platform fit**: beyond Cursor, verify and adapt skill discovery, installation and invocation on more mainstream agent platforms and IDEs, Trae among them.

### Success metrics

- **Intent support**: coverage of the high-frequency delivery and governance intents reaches 80% or more. (Serves Goal 1 and Goal 2.)
- **Channel compatibility**: the existing skills verified and running smoothly on at least 2 new platforms. (Serves Goal 4.)

---

## Next

**Strategic goal it serves**: [Goal 3, capabilities can be reused and orchestrated across projects](../project-overview/strategic-goals.md#goal-3-capabilities-can-be-reused-and-orchestrated-across-projects)

### Entry conditions

- **The foundation is ready**: the Now stage's intent coverage and channel verification have hit their targets, meaning the M5 and M6 success metrics are met.
- **Pulled by demand**: a clear cross-project reuse pain, or a call for chained automated orchestration, has surfaced in the team.

### Milestones

- **M7, complex orchestration and a closed workflow loop**: semi-automated orchestration of complex governance and delivery chains, with the compositions verified.

### Key initiatives

- **Design meta-skills**: design and build higher-order orchestration workflows — running from requirement analysis through to task breakdown in one continuous pass — composing the atomic skills into end-to-end solutions.
- **Deepen the data-passing spec**: upgrade and promote the I/O contract spec to support more flexible input and output parameter mapping and shared context, so composition meets less resistance.

### Success metrics

- **Chained scenarios in production**: at least 3 high-value end-to-end orchestration scenarios built and verified. (Serves Goal 3.)
- **Reuse verified**: the correctness of composed skill reuse verified in no fewer than 2 different kinds of project.

---

## Later

Direction only, with no dates attached:

- **Build observability**: explore a standardised, privacy-respecting way to collect usage telemetry, so the North Star metric — monthly skill usage — can actually be measured.
- **A community-level standard**: take AI Cortex's skill spec system and contract mechanism to the wider open-source community, so it becomes the de facto standard.

---

## Milestone detail (appendix)

| Milestone | Scope | Metrics | Goals |
| :--- | :--- | :--- | :--- |
| M1-M4 (completed) | Discoverability, reuse, governance, establishing the channels | (archived) | (the stage goals were met) |
| M5, core intent coverage | Enriching and completing the delivery and governance skills | >80% of high-frequency everyday intents covered | Goal 1, Goal 2 |
| M6, multi-channel verification | Adapting to and verifying different IDE and agent platforms | Running smoothly on >2 new platforms | Goal 4 |
| M7, complex orchestration and a closed workflow loop | End-to-end chained execution, and an upgraded I/O spec | >3 chained workflows in production | Goal 3 |

---

## Constraints

- **Mapping**: a backlog item must map to the roadmap's Now or Next stage.
- **Out of scope**: a requirement that does not fit a roadmap direction is not worked on, until the roadmap changes.
