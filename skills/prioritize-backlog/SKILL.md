---
name: prioritize-backlog
description: Apply a project's priority policy to unresolved backlog items, or explicitly reassess a batch using RICE, WSJF, MoSCoW and ICE; preserve settled decisions unless replacement is requested.
version: 3.1.0
license: MIT
---

# Skill: Prioritize Backlog

## Purpose and modes

Set source-backed priorities without confusing normal planning with a complete
reassessment. Load [roadmap modeling](../../specs/roadmap-modeling.md#52-priority-vocabulary)
and the project's policy. This skill owns priority decisions, not roadmap placement,
dependency registration, requirement creation or task decomposition.

| Intent and evidence | Mode | Scope |
| --- | --- | --- |
| Project policy exists; normal planning requested | Policy application | Unset or explicitly selected unresolved items; preserve settled decisions |
| No policy exists | Framework assessment | Offer four-framework comparison for unresolved items |
| User explicitly asks to reassess the whole backlog | Full reassessment | All non-declined items; old values excluded from scoring, retained for audit |

An explicit policy-change request may select affected settled items for replacement.
Policy/framework conflicts are visible; full assessment does not silently waive
business policy. Do not run full reassessment merely because promotion needs priorities.

## Procedure

1. Read project norms, strategic goals, policy, item sources and current priority
   decisions. Choose the mode from the request and evidence. Extract facts before
   asking; ask only for unresolved policy mappings, required comparison inputs or
   a business decision. If no policy exists, offer framework assessment; do not
   manufacture project policy from the scoring defaults.
2. Detect the project's declared backlog path and layout. Supported layouts, in
   fallback order, are a directory of item frontmatter (`multi-file`), a single
   file with an `items` YAML array (`yaml-list`), H2 entries followed by YAML blocks
   (`h2-yaml`), and a Title/Priority table (`table`). Conventional paths are
   `docs/process-management/backlog/` or `docs/backlog/`, then their `.md` equivalents.
   If mixed, report the ambiguity; preserve declared authority, otherwise use
   multi-file and report the ignored single file. Never write both. If none is
   recognizable, report the limitation and hand off to `capture-work-items`.
3. Inventory every item and retain current priority and decision as audit evidence.
   Exclude `status: declined`. Report the selected scope and preserved items.
   In policy mode, map the stated business conditions to project labels; record the
   policy reference and exceptions. Unknown conditions remain unresolved. A single
   item may receive a policy priority without a comparison batch.
4. In framework modes, load [four-framework assessment](references/four-frameworks.md)
   and compare the selected batch using all four methods. For a single item,
   explain the comparison limitation and ask whether to continue; do not block
   valid policy application. Show every result and evidence gap, never a weighted
   average. With missing numeric inputs, report cannot score and obtain evidence
   rather than calculating invented scores. A gap of two or more levels needs a
   user decision; a smaller gap yields a provisional RICE suggestion.
5. Present a result table with item, old priority, policy or framework basis,
   proposed priority, conflict/unknown and rationale. The user settles material
   trade-offs. Existing authorization or an explicit deterministic project policy
   can authorize application; do not repeatedly ask to approve settled rules.
6. Write only settled decisions in the detected layout. Preserve source approval
   and execution. Record `priority_decision` with `final`, `previous`, `rationale`,
   `decided_by` (user/auto), `decided_at`, and `mode`. Policy mode adds `policy_ref`;
   framework modes add `frameworks` (rice/wsjf/moscow/ice results). An upward
   override of the framework consensus also carries `strategic_override`.
   Auto denotes deterministic authorized application, not invented business judgment.
   Multi-file uses frontmatter; yaml-list uses the matching array entry; h2-yaml
   uses its block; table uses the Priority cell and a linked Priority Decisions
   section keyed by stable item anchor. Preserve surrounding content.
7. An explicit user decision never to do an item writes `status: declined`,
   `declined_reason` and `declined_at`; P3 alone does not mean rejection. Never
   decline automatically. Only the last `previous` priority is retained; callers
   needing longer history use project records, not a new archive created here.
8. Report mode, layout, scanned/changed/preserved/unresolved counts, distribution,
   policy exceptions, framework conflicts and declined count. Suggest
   `promote-roadmap-items`; do not invoke it automatically.

## Output

A comparison/decision table and updated source priority records. No tier, version
membership or date changes are made. Missing source facts are explicit limitations.

## Self-Check

- [ ] Mode, scope and authoritative layout were resolved before writing.
- [ ] Normal policy application preserved settled priorities and terminal exclusions.
- [ ] Full reassessment occurred only on explicit intent, retaining previous values.
- [ ] Selected framework assessments used all four methods and disclosed gaps/conflicts.
- [ ] Decisions cite policy or assessment evidence; business overrides are traceable.
- [ ] Source approval, execution, tier and version scope were preserved.
- [ ] Output reports changed, preserved and unresolved items without automatically promoting.

## Examples

- A project ranks active-customer blockers P0 and sales requests P2. One new
  customer blocker receives P0 under that policy; settled items are unchanged.
- A user requests complete reassessment after a strategy change. Compare all
  non-declined items afresh, expose policy conflicts and retain overwritten values.
- A project has no policy and sparse intake. Offer framework comparison, identify
  missing Reach/Effort evidence and leave unsupported results unresolved.

## Filled deliverable example

[Filled policy decisions](../define-roadmap/references/service-desk/priority-decisions.md). This is a fictional completed output, not a template
or authorization to change the adopting project.
