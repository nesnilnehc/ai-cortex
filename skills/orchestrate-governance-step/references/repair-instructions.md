# orchestrate-governance-step: repair instructions

## AI Repair Instructions

### Problem 1: several routing items were run

- **How to spot it**: the IterationStepReport has several `skill called` entries
- **How to correct it**:
  1. Identify the routing items that were run
  2. Keep only the 1 highest-priority item (`urgent` > `important` > `defer`)
  3. Re-emit the IterationStepReport, reporting only 1 action

---

### Problem 2: continuation_signal is missing

- **How to spot it**: the IterationStepReport lacks the internal continuation-signal field, or its value is outside the five-value enum
- **How to correct it**:
  1. Check the execution result and fill it in by this logic:
     - Sub-skill succeeded + routing remains → `advance`
     - Sub-skill succeeded + fresh plan-next says `complete` with acceptance evidence → `done`
     - Fresh plan-next says `needs_input` or `no_applicable_action` → `blocked`
     - Only human-owned/external candidates remain → `blocked`, preserving plan-next's state and naming the owner
     - The fingerprint repeated → `stalled`
     - The sub-skill failed → `error`
  2. Explain why in the `Next` field

---

### Problem 3: reporting advance while skipping the post-execution check

- **How to spot it**: the report says `advance` but plan-next was never re-run to verify the intended change
- **How to correct it**:
  1. Re-run `/plan-next` and check whether the intended evidence and decision state changed
  2. If the intended evidence is present and plan-next says `actionable` → `advance` is confirmed
  3. If the same eligible action remains unchanged → update the stall count; on the 2nd occurrence → `stalled`

---

### Problem 4: judging completion internally and skipping step 6

- **How to spot it**: the `Next` field carries self-assessment language such as "the whole governance layer is ready", "everything currently executable has been created", or "this belongs to the developer execution layer", with no record of a step 6 plan-next re-run
- **How to correct it**:
  1. Re-run `/plan-next`
  2. If plan-next explicitly says `complete` and provides acceptance evidence → `done` is valid
  3. If it says `needs_input` or `no_applicable_action` → `blocked`, preserving that state and the reason
  4. If it says `actionable` with an eligible route → `advance` only after the action and post-check

---
