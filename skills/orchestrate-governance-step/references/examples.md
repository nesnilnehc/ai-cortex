# orchestrate-governance-step: examples

## Examples

### Example 1: happy path — a requirement is registered

**Scenario**: plan-next routes to registering new backlog entries; first invocation; the sub-skill succeeds.

**Execution**:

1. Call plan-next internally → subject: "register the 3 backlog entries added in stage M5", recommended skill: `/capture-work-items`, priority: defer
2. Stall detection: first invocation, no fingerprint history → continue
3. Human gate: `capture-work-items` is not a creative skill → pass
4. The action creates three files, so prepare and review an explicit plan:
   - Goal: register the 3 M5-stage backlog entries (quoting the card subject)
   - Sub-skill command: `/capture-work-items register the 3 requirements newly found in M5 into the backlog`
   - Focus traceability: the card says "the M5 sweep found 3 requirements scattered through discussions"
   - Expected output: 3 new markdown files under `backlog/`, with frontmatter
   - Scope red lines: MUST NOT modify existing backlog entries; MUST NOT touch `roadmap/` or `requirements/`
   - Rollback points: the new files can be removed with `git clean -f backlog/<new-files>`
5. One review finds no scope or dependency defect → `plan_reviewed_rounds = 1`
6. Run `/capture-work-items register the 3 requirements newly found in M5 into the backlog`
7. Post-execution check: re-run plan-next → verify the three entries exist and the route is resolved; another eligible route remains → advance

**IterationStepReport**:

```markdown
## What this automatic step did

- **What was done**: registered the 3 requirements newly found in M5 into the backlog
- **Why it needed fixing**: the M5 sweep found 3 requirements scattered through discussions, never registered in structured form
- **What changed**:
  - Before: no matching entries under backlog/
  - After: 3 new backlog entry files, with frontmatter and a summary
- **Result**: Success ✅
- **Next**: keep going automatically (1 item still pending)
- **Decision state**: actionable
- **Evidence and blockers**: three registered entries verified; another eligible route remains
- _(internal) continuation signal: advance; plan_reviewed_rounds: 1_
```

---

### Example 2: the human gate skips a card → the next non-creative card is taken

**Scenario**: plan-next reports `actionable` with two cards: `design-strategic-goals` (important, strategic/creative) + `capture-work-items` (defer, registration).

**Execution**:

1. Call plan-next internally → two routing cards
2. Stall detection: first invocation → continue
3. Step 2 takes the highest priority: `design-strategic-goals`
4. The strategy decision is reported as human-owned; continue only because plan-next independently surfaced the capture route
5. Verify the capture route's target, prerequisites, and scope; the work is routine and reversible
6. Run `/capture-work-items …` with that bounded focus
7. Step 6 re-run plan-next; verify the intended artifacts/evidence changed, then emit `advance`

**IterationStepReport**:

```markdown
## What this automatic step did

- **What was done**: registered the 3 backlog entries added in stage M5
- **Why it needed fixing**: the strategic-goal card needs human judgment and was skipped; the same batch held another card that could run automatically
- **Result**: Success ✅
- **Next**: keep going automatically (skipped, awaiting a human: 1 — `design-strategic-goals`)
- **Decision state**: actionable
- **Evidence and blockers**: strategy decision awaits the user; capture route is independent and eligible
- _(internal) continuation signal: advance; plan_reviewed_rounds: 0; per-invocation deferral: [design-strategic-goals]_
```

---

### Example 2b: no candidate is eligible for automatic execution → blocked

**Scenario**: plan-next routes two cards, both either strategic/creative or "awaiting execution".

**Execution**:

1. plan-next → `define-mission` (important) + one `awaiting execution` card
2. Both are identified as human-owned or externally owned; no governance action is run
3. Emit `blocked` while preserving `decision_state: actionable`, listing the owner and next handoff for each

**IterationStepReport**:

```markdown
## What this automatic step did

- **What was done**: scanned 2 routing cards, all of which need a human
- **Why it needed fixing**: everything in "Do now" is either creative or waiting on outside execution, so nothing can be automated
- **Result**: Your call needed ⚠️
- **Next**: your decision needed:
  1. `define-mission`: a strategic skill that needs human judgment; running it by hand is recommended
  2. The "awaiting execution" card: governance is ready, waiting on outside development
- _(internal) continuation signal: blocked_
- **Decision state**: actionable
- **Evidence and blockers**: plan-next surfaced two candidates; both require a human decision or outside execution, so the executor ran neither
```

---

### Example 2c: a persistent exclusion leaves no visible action

**Scenario**: plan-next finds an unfinished route, but the user has excluded its exact route key in `.ai-cortex/plan-next.yaml`. Fresh diagnosis finds no independent eligible route, so `decision_state` is `no_applicable_action` and "Skipped recommendations" names the route.

**Result**: emit `continuation_signal: blocked` and report the excluded route. Do not emit `done`; the executor does not add, remove, or convert the persistent preference.

---

### Example 3 (edge case): stall detection — the sub-skill made no progress

**Scenario**: after the last `/capture-work-items` run, the requirement document was never written; this time plan-next routes the same card.

**Execution**:

1. Call plan-next internally → fingerprint = "analyze the requirements of roadmap node N1||strategic goal 'Goal A' → roadmap 'N1' current: requirements layer"
2. Stall detection: identical to the previous fingerprint → **stalled fires**

**IterationStepReport**:

```markdown
## What this automatic step did

- **What was done**: tried to analyze the requirements of roadmap N1, but detected 2 consecutive rounds with no progress
- **Why it needed fixing**: requirements/N1-requirements.md was never written after the last `/capture-work-items`
- **Result**: Error ❌
- **Next**: stuck: the same task made no progress twice in a row. Possible causes: the requirement file was not written, the path configuration is wrong, or the skill ran incorrectly. Suggested: run `/capture-work-items` by hand, check whether the output file exists, and re-run /orchestrate-governance-step once it is resolved
- _(internal) continuation signal: stalled_
```

---
