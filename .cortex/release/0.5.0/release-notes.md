# Release notes

## 0.5.0 — 2026-10-23

AI Cortex now supports source-backed roadmap planning from structure selection to delivery and archival. Teams can retain their existing plans, choose the views they need, and produce English or Simplified Chinese roadmap outputs. This release also strengthens requirement review and adds evidence-backed presales response preparation.

This is a stable release within the project's pre-1.0 series. It contains compatibility changes; review the upgrade notes before updating custom integrations.

### What you can do

- **Plan around requirements and defects.** Keep priority, approval, execution, readiness and timing distinct. Use optional version, iteration, phase, milestone-event and schedule views without turning each view into another task hierarchy.
- **Settle structure before filling a plan.** Request a blank structure for review, populate an already selected structure, or authorize both stages. Existing projects retain their decisions, paths and links during alignment.
- **Choose useful presentations.** Four worked scenarios cover iterative products, continuous service work, staged delivery and discovery. The bundled offline renderer produces Markdown, SVG and dated Mermaid; unknown dates remain unscheduled.
- **Keep language and history consistent.** Roadmap outputs follow project language evidence, support English and Simplified Chinese display catalogs, and retain material revision summaries and older history links. Legacy generator inputs retain their behavior.
- **Deliver to a knowledge base with explicit authority.** Remote delivery guidance separates source agreement, stored preservation and reader/chart checks. The Yuque adapter and offline regressions do not imply continuous monitoring.
- **Review requirements before design.** A new bounded repair loop coordinates review, targeted corrections and re-review. Blocking questions remain visible instead of being treated as approval.
- **Prepare grounded presales answers.** A new skill separates reusable product facts from customer-specific conditions, preserves source questions and evidence, and hands file production to the appropriate format tools. It does not authorize sending or contracting.
- **Explore the library on the website.** The bilingual site includes an on-page capability atlas, remembered language and theme choices, and the shared Cortex core identity.

### Upgrade notes

1. **Use a clean clone when crossing the history rewrite.** Main history was rewritten on 2026-10-23 solely to remove Claude and Cursor Agent coauthor trailers. Human authors, committers, dates and file contents were preserved; invalidated signatures on rewritten commits were removed. Existing release tags were retained. The old 0.4.0 tag and its mapped main-history commit have identical file trees. Back up local work and keep old clones for reference; do not merge their old branches directly into the rewritten main. Reapply intended file changes as new commits without the removed trailers.
2. **Update Skill discovery integrations.** Discover through each skill's English `description` and `skills/INDEX.md`. Removed metadata includes `tags`, `triggers`, Skill `recommended_scope`, `description_zh` and inactive fields. Do not restore substring-based trigger ranking. The consumed `findings-list` output schema remains supported.
3. **Adapt governance routing consumers.** Handle the four diagnosis states: `actionable`, `needs_input`, `no_applicable_action` and `complete`. Keep them separate from the executor's continuation signal. An empty or excluded recommendation list does not prove completion. Persistent skips use exact route/target pairs in the project's `.ai-cortex/plan-next.yaml`; malformed preferences must be reported.
4. **Re-read roadmap quality expectations.** Priority and dependency readiness replace mandatory percentage allocations per strategic goal. Preserve existing P0–P2 meanings; use P3 under the project's policy. Separate approval from execution, phase spans from milestone events, and planned dates from actual evidence. Adopt a new layout or schema only when authorized; legacy/custom plans do not require automatic migration.
5. **Reorder editable requirement drafts.** Requirement Modeling 6.1.0 defines the relative section order and review-readiness treatment of open questions. Preserve stable IDs, meanings, links and anchors. Approved, implemented and superseded snapshots stay frozen; use the project's successor process for authorized revisions.
6. **Record UI decisions when triggered.** Functional Design Modeling 2.0.0 makes tasks, states, selection rationale, reuse constraints, independent assets or an explicit skip reason, and acceptance handoff conditionally required for new interfaces and significant experience changes. Adopt the loading entry in the consuming project's own agent instructions. Small copy repairs and backend-only changes do not require empty UI documents.
7. **Keep release evidence honest.** A required check with zero executed cases, all cases skipped or unverified execution cannot satisfy readiness. Record actual scope and results, not only the command's exit code.

### Installation and rollback

A fresh installation follows the [repository quick start](https://github.com/nesnilnehc/ai-cortex#quick-start). Existing installations can use `cortex update` after protecting local work. It follows `origin/main`, not a release pin; it refuses a dirty checkout unless forced, and force is unnecessary for this upgrade.

To pin this release, check out `v0.5.0` in a clean canonical clone and run that clone's `bin/cortex install`. To roll back the installed assets, check out `v0.4.0` there and rerun the installer. An asset rollback does not reverse changes already made to consuming-project documents or remote pages; restore those from their own backups and authorities. Do not merge the old tag into main.

### Verification scope

The release gates cover registry and asset versions, documentation, modeled Rules, offline roadmap generation and regressions, website behavior and checker mutation tests. Synthetic UI scenarios check decision-contract structure; they do not establish visual acceptance in a consuming project. Remote platform tests use offline snapshots. No new live model evaluation or end-to-end external platform test was run for this release.
