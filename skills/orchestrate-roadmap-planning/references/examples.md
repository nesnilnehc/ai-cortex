# Roadmap planning examples

## Example 1: pulling in newly prioritized items (mainstream case)

- **Context**: `review-roadmap` findings show a complete structure, but 3 scored items are unpromoted → mode = `intake`
- **Schedule**: step 0 → skip 1 and 2 (governance documents complete) → skip 3 (no unregistered input) → skip 4 (no unset items) → step 5 (dependency evidence needs checking) → step 6 → skip 7 and 8
- **Step 5 output**: 1 candidate has an unresolved prerequisite and is marked as not admissible to Now
- **Step 6**: the other 2 are promoted to Now; the blocked one goes to Next
- **Aggregation**: priority-ordered tier report + change list + a suggestion to run `capture-work-items` on the newly promoted Now items

## Example 2: cold start on a new project (edge case)

- **Context**: `docs/` holds nothing but README → findings show roadmap.md and strategic-goals.md are both missing → mode = `bootstrap`
- **Schedule**: step 0 → step 1 (`design-strategic-goals` detects missing upstream context and derives fallback goals from repository evidence) → step 2 → step 3 → step 4 → step 5 if dependency evidence is missing or stale, otherwise reuse it → step 6
- **Key point**: the orchestration layer does **not** call `define-vision` just because the vision is missing. Whether the upstream is complete, and whether to run in normal or fallback mode, is `design-strategic-goals`'s own call
- **If the user rejects the fallback candidates**: halt, prompt to run `plan-next` first to establish the strategy layer, and emit the completed step 0 health-check report

## Example 3: downgrade after the dependency step fails (edge case)

- **Context**: mode = `intake`, 5 promotion candidates
- **Step 5 fails**: `map-item-dependencies` detects a dependency cycle and halts
- **Handling**: step 5 sits at the **default** tier, so the orchestration is not terminated; record the failure and carry on
- **Step 6 downgraded**: report the missing verified dependency result before any recommended comparison. Known cyclic candidates remain unresolved; downgrading never authorizes them into Now. Independently verified candidates may still be compared under the atomic skill's rules.
- **Aggregated report**: retain the cycle `#12 → #19 → #25 → #12`, affected candidates and the limitation. Suggest resolving the cycle before reconsidering those candidates; do not describe them as unchecked but executable.
