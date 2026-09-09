---
artifact_type: guide
created_by: ai-cortex
lifecycle: living
created_at: 2026-09-09
status: active
---

# Using the roadmap planning chain

For users: nine skills sit on the chain from strategic goals to items entering Now. This page says when to reach for each, and what you will run into the first time.

Each skill is defined authoritatively in its own `SKILL.md`, and the execution order and tiering in [orchestrate-roadmap-planning](../../skills/orchestrate-roadmap-planning/SKILL.md). This page restates neither; it only tells you how to get in the door.

---

## 1. Almost always: one line

```text
/orchestrate-roadmap-planning
```

It checks the roadmap's health first, works out which link in the chain you are stuck on, then runs only the steps that need running; whatever it skips, the report says why. **You do not have to work out which skill to call** — that is exactly why it exists.

You can skip the slash command and just say "run a round of roadmap planning".

---

## 2. Finding the entry point from where you are

When you know exactly what you want, naming a single skill is faster.

| Where you are | What to use |
| :--- | :--- |
| You want to know what is wrong with this roadmap | [`review-roadmap`](../../skills/review-roadmap/SKILL.md) |
| There are no strategic goals yet | [`design-strategic-goals`](../../skills/design-strategic-goals/SKILL.md) |
| You want to build a roadmap from the strategic goals | [`define-roadmap`](../../skills/define-roadmap/SKILL.md) |
| You have a requirement or a defect to write down | [`capture-work-items`](../../skills/capture-work-items/SKILL.md) |
| The backlog needs re-prioritising | [`prioritize-backlog`](../../skills/prioritize-backlog/SKILL.md) |
| You want to see which items block which | [`map-item-dependencies`](../../skills/map-item-dependencies/SKILL.md) |
| You want to pull items into Now | [`promote-roadmap-items`](../../skills/promote-roadmap-items/SKILL.md) |
| Something is stuck, or the dates have to move | [`update-roadmap`](../../skills/update-roadmap/SKILL.md) |
| A milestone is finished and needs archiving | [`archive-milestone`](../../skills/archive-milestone/SKILL.md) |

Plain description matches too — the matching rules are in [AGENTS.md](../../AGENTS.md) §4, and each skill's `triggers` field exists for exactly this.

---

## 3. Two places that will stop you

Both are by design, not a fault.

### 3.1 Promotion says the capacity allocation is missing

`promote-roadmap-items` computes capacity as "that goal's percentage × the total capacity baseline". With neither number present, it stops and sends you to `define-roadmap` first.

**Why it does not fill them in for you**: a capacity allocation is a commitment of resources, and a skill is not allowed to infer one on your behalf. `define-roadmap` asks you two things:

1. **The total capacity baseline**: engineer count × cycle length − known overhead (meetings, oncall, holidays), discounted to 60–70% effective hours. The buffer for unplanned work is given up at this step, so the percentages that follow are relative to effective capacity, not calendar capacity.
2. **The percentage per strategic goal**: they must sum to 100%, and an engineering-health goal must not be 0% — that kind of work has no advocate in the strategy, and never wins capacity in a contest of value.

### 3.2 With the governance documents empty, it does not interrogate you from scratch

Run `design-strategic-goals` on a new project with no vision and no North Star, and it does not ask you for answers one field at a time. It works candidate goals back out of the evidence in the repository: README and AGENTS.md for intent, CHANGELOG and git log for where effort actually went, the code structure for the boundaries of what exists, the backlog for needs not yet met.

**The output is marked as such**: every candidate goal carries the evidence it was inferred from, pointing at a specific file, and one with no evidence is not written at all; nothing lands on disk until you confirm it item by item; and the document's header carries a note that it lacks upstream backing and is a temporary anchor. Once the vision and North Star exist, it should be run again.

The reason is blunt: a goal reasoned back out of evidence reads smoothly and hangs together, and that is precisely what makes it most likely to be invention filling a gap. Attaching the evidence and asking you to confirm is what lets you falsify it on the spot.

---

## 4. Why dependencies are mapped before promotion

Putting `map-item-dependencies` ahead of `promote-roadmap-items` is the most important ordering decision on the whole chain.

High priority does not mean it can be pulled now. Promote a P0 item whose prerequisite is still sitting in the backlog and it occupies capacity in Now while producing nothing — and the capacity report shows full. So entry to Now has two conditions: it ranks near the top, **and** it has no unresolved prerequisite.

Where an item has no dependencies recorded, `promote-roadmap-items` does not wave it through silently: it tells you to record dependencies first, and if you press on regardless, the candidate table marks it "dependencies not checked".

---

## 5. Where the criteria live

What a roadmap has to look like, and what counts as a problem, is settled in one place: [rules/roadmap-quality.md](../../rules/roadmap-quality.md). The producing side (`define-roadmap`), the diagnosing side (`plan-next`) and the reviewing side (`review-roadmap`) all cite that same file. To change a criterion, change it there — not in a skill.

---

## 6. How this differs from plan-next

Both tell you what to do next, but they cover different ground:

- [`plan-next`](../../skills/plan-next/SKILL.md) answers "what does the whole project do next", across every layer from mission to task. It reads; it does not execute.
- `orchestrate-roadmap-planning` answers "take the roadmap line from strategy through to promotion in one pass". It covers only that vertical slice, and it does execute.

When you are unsure where governance goes next, run `plan-next` first; when you have decided to move the roadmap forward, use `orchestrate-roadmap-planning`.
