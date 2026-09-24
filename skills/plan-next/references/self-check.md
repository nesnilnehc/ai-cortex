# plan-next: self check

## Self-Check

**Scan**:

- [ ] Project governance sources were discovered in precedence order; unresolved conventions are reported rather than replaced with assumed directories
- [ ] The 2 asset fields are present (path + status)
- [ ] Whether the roadmap is tiered has been decided; where it is not, `promote-roadmap-items` has been routed
- [ ] The project-declared artifact conventions and evidence source for each path mapping were identified; no conventional directory was assumed mandatory

**Diagnose**:

- [ ] The strategic goals were read; with no goal, the L1 route fired
- [ ] **The L1 acceptance-criteria KPIs were parsed**; each goal's current KPI state was decided (met / not met / data missing)
- [ ] **L1 status=approved counts as in-progress**, and drilling down was not skipped
- [ ] **Where the KPI data source is missing**, the first route establishes the data source rather than routing downstream
- [ ] Every node's status was resolved by "explicit first > inference from children"
- [ ] Every level's sibling nodes were scanned in full and classified (done / in-progress / blocked / pending)
- [ ] The parallelism decision rules were applied; the suggestion (focus / parallel / converge / start) is stated
- [ ] The L3-L5 physical scan is complete (glob + optional parent: + optional manifest)
- [ ] The L3→L4 / L4→L5 G3 chain check was run; depth first (an upper-level G3 hit stops the lower-level report)
- [ ] The "finished" verdict rests on the status field alone, with no git signals introduced
- [ ] The drift sweep (step 2.2) was run; artifacts past the threshold are in the drift entry list
- [ ] The hygiene sweep (step 2.3) was run; finished-but-unarchived milestones, ADR status problems and repository structure problems were all scanned
- [ ] Prerequisites were scoped to the routes they actually govern; uncertain applicability was surfaced as `needs_input`, not inflated into a global blocker

**Recommend**:

- [ ] Every suggestion carries what to do, why, and an observable completion marker (prose or card alike)
- [ ] **The format choice is right**: prose for a single suggestion; structured cards for ≥2 parallel suggestions
- [ ] **A KPI or threshold carries the triplet on first appearance** (current value / target value / benchmark); with no benchmark, "project-defined (no external benchmark)" is noted
- [ ] Depth first (only the first gap in the tree is reported per goal)
- [ ] A parallel suggestion states the reason for parallelism in the text
- [ ] Drift and hygiene entries are all in the "Also worth noting" section and have not crowded out the first two slots of "Do now"
- [ ] **(When using structured cards)** The TL;DR quote block is ≤30 words and does not repeat the subject
- [ ] **(When using structured cards)** The governance context is a multi-line short chain (≤25 words per line) carrying the current L1 acceptance-KPI state
- [ ] **(When using structured cards)** The priority label is mapped correctly (urgent / important / defer / minor / awaiting execution)
- [ ] **(When using structured cards)** An all-pending L5 with several tasks (≥2 independently startable) renders as several side-by-side cards, not merged
- [ ] **(When using structured cards)** The cost-of-deferral / onboarding-threshold fields are omitted where information is short, not filled with placeholder text
- [ ] **(When a skip directive is present)** The selector was resolved against the conversation's displayed recommendation and its exact route key, or clarification was requested without excluding anything
- [ ] **(When duration is unspecified)** The user chose session or persistent scope before any exclusion was applied
- [ ] **(When persistent scope is chosen)** The preference file was validated and updated once, with unrelated entries preserved; a failed write was reported as a failure
- [ ] **(When a restore directive is present)** The selected active exclusion was identified exactly and cleared from every scope where it was active, or clarification was requested without a partial change
- [ ] **(When the project changed during a duration choice)** The displayed route was revalidated before any skip was saved; a stale suggestion was not persisted
- [ ] **(When a skip directive is present)** The complete eligible candidate sequence was considered before the display limit; every remaining route still passed its normal preconditions and dependencies
- [ ] **(When an exclusion is active)** The omitted action and its duration are reported, and a no-candidate result says so plainly rather than exposing a dependent route
- [ ] A `no_applicable_action` result is not called complete; `complete` requires all declared acceptance conditions met and no unfinished, excluded, or evidence-limited work

**Output**:

- [ ] **The header summary (situation/core tension) is within the word limits**: situation ≤25 words, core tension ≤30 words; no bare project code (the same rule as the "Do now" section)
- [ ] The "Do now" section carries no codes: L1-L5, G1-G4, P0-P3
- [ ] The "Do now" section carries no natural-language equivalents of the codes: asset missing, incomplete content, truth drift, completion drift, traceability drift, misplacement
- [ ] The "Do now" section carries no old priority labels: now/next time/later/ignorable; priorities are uniformly `urgent/important/defer/minor`
- [ ] The "Do now" section carries no English status codes: pending, in-progress, done, blocked
- [ ] **The "Do now" and "Also worth noting" sections carry no bare project code** (`T\d+` / `M\d+` / `Goal \d+` / `BL-\d+` / `ADR-\d+`) — every first appearance carries a natural-language subtitle
- [ ] **The "Do now" section carries no MoSCoW words** (Must Have / Should Have / Could Have / Won't Have)
- [ ] **The "Do now" section carries no governance process jargon** (precondition gate / short-circuit / soft-blocked / sibling scan / focus node / all-pending branch / inference from children)
- [ ] **A code missing from the dictionary is marked in the diagnostic-basis section**, not forced into a user-facing section
- [ ] **The diagnostic-basis decision logic uses a table** (4 columns: level / node / status / inference), not prose
- [ ] Ordinary diagnosis made no writes; an explicit persistent skip or restore touched only `.ai-cortex/plan-next.yaml`
- [ ] The diagnostic basis names each goal's traversal position and the blocked nodes
- [ ] No session skip was written to disk; no persistent skip was treated as completion

---
