# Remote roadmap delivery

Use when publishing or maintaining a remote roadmap family, or retiring its local
predecessors. Apply the Spec's [remote authority](../../../specs/roadmap-modeling.md#remote-authority-and-delivery-evidence)
and [migration closeout](../../../specs/roadmap-modeling.md#migration-closeout).
This guide adds no destination, document count or approval gate.

## Read, change and verify

1. Discover document read, rich-content write, title, hierarchy and attachment
   capabilities. Read project norms and latest remote pages, affected details and
   history. Reuse the retained destination and authorization; do not recreate local
   plans or ask for the same permission again.
2. Inventory stable page IDs/URLs, heading and compatibility anchors, cards, source
   links, history and protected business facts. Identify the fact authority and
   affected projections. Separate unknown facts from undecided business options.
   Keep temporary snapshots outside published plans.
3. Prepare the smallest rich-content edit. Shorten display titles independently of
   URL slugs. Preserve unrelated markup and historical originals. Re-read immediately
   before writing; reconcile changes rather than overwriting them. Prefer conditional
   writes; a read/compare fallback leaves a residual race. Read unknown-outcome writes
   before retrying.
4. Read back each changed page and affected projection. Compare identities, anchors,
   cards, history and explicit source-derived scope/date/exclusion/state assertions.
   Partial multi-page delivery is not a consistency pass.
5. Inspect affected reader navigation, section jumps, images/cards, chart dates,
   colors/legend and table readability. Report stored and rendered checks separately.
   Missing access or rendering remains a gap; use an authorized supported fallback
   without inventing dates or dropping reproducible source access.

For Yuque, load [the Yuque adapter](platforms/yuque.md). Other services need their
own capability evidence; Yuque markup is not a portable assumption.

Match verification effort to the edit. A metadata-only title update needs body
equality plus title/directory verification; unchanged body/chart observations can
be reused. Content or asset changes require fresh affected checks. Reuse valid
platform probe results rather than writing test pages every time. Read-only review
never creates probes or publishes; a tool fallback does not expand authorization.
An unrelated prose correction does not invalidate an unchanged chart's valid load
receipt; a change to its source facts does require fresh chart consistency checks.
The host decides evidence applicability; the helper cannot certify freshness.

## Read-only evidence checker

For captured Lake/HTML updates, run `python3 <skill-dir>/scripts/check-platform-delivery.py evidence.json`.
This helper accompanies the Yuque adapter; it does not certify arbitrary platform
formats. The JSON root contains `baseline`, `readback` and `contract`; the concrete
encoding is documented in that adapter. `preflight(expected, current)` compares the initial and fresh pre-write
snapshots. The host owns conflict handling and publication. The checker performs
no network calls, writes, deletions, uploads or synchronization.

The helper compares the same selected set of existing pages. For newly created
pages, verify creation receipts, content and rendering through the host; do not
invent a pre-edit snapshot merely to satisfy the helper. The host reviews authorized
page additions/removals or card-type fallbacks outside this bounded check. This
tool limitation adds no confirmation gate when the operation is already authorized.

Collect `rendered_ids`, loaded image dimensions and named visual results from real
reader observations; retain screenshots or observation receipts in the existing
maintenance evidence location. Never populate them from expected answers. Inventory
published heading IDs and known compatibility/inbound fragments from rich source
and rendered HTML; exclude transient editor IDs. Build content assertions from source
decisions, including unallocated work, conditions and unknowns; check authoritative
detail and all affected projections. List only intended card replacements in
`changed_cards`; preserve unrelated cards and replacement identities/types. Declare
required source/navigation links so removing or retargeting one cannot pass as an
ordinary unverified external link.

Missing required observations fail the check. `passed` means only captured checks
passed; `unchecked_external_links` remain unverified. Text assertions supplement
semantic review, not source truth. The checker cannot authenticate observations,
certify business completeness or close concurrency races. Do not call an offline
fixture pass live integration evidence or continuous monitoring.

## Retire local predecessors

Account for unique decisions, unknowns, exclusions, source references, complete
history and diagram sources across the inventoried local files and remote current
content/history. Explain differences as preserved, linked, corrected or unresolved.
Unexplained omissions block affected-file removal. Inspect affected reader/chart
behavior and representative stable links before cleanup.

Check Git tracking/recovery, inbound links and file consumers. If normal history
cannot restore originals, create and verify a dated recovery archive outside the
editable plan. After explicit cleanup authorization, remove only inventoried files,
replace entry pointers and search for dangling paths. Preserve unrelated work,
historical originals and legitimate local-deployment statements. Do not infer
commit, push, installation or source-system mutation authorization.

The checker's `recovery_findings(root, inventory, archive)` can compare current
inventoried files with their tar members byte for byte, without extraction or
deletion. It rejects empty/duplicate inventories, escaped paths, symlinks and
missing/duplicate/nonregular or changed backup members. A recoverable backup does
not establish semantic migration completeness or authorize cleanup.

## Fictional regression example

The [two-turn offline session](../../../tests/fixtures/roadmap-platform/session.json)
first shortens titles without changing URLs, then shifts a milestone target in
detail and summary with an intended chart replacement. V2 and I2 contribute the
same batch; another batch remains unknown, Q9 conditional and MS1 planned. History
retains an earlier closure without claiming new delivery. This is adapter evidence,
not a new canonical roadmap example or a live Yuque receipt.

Run `python3 scripts/test-roadmap-platform.py` from the repository root. Positive
controls pass across turns; negative controls detect anchor/card/image loss, history
edits, stale summaries, unsupported completion, candidate inclusion, broken links
and concurrent edits. Existing structure/population conversation tests remain
separate; neither suite replaces semantic review or actual platform checks.
