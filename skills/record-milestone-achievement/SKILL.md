---
name: record-milestone-achievement
description: Verify evidence of a project milestone event and record its confirmed achievement with references to independently stored evidence. Use for planned or unplanned events, with an optional SVG calendar of actual occurrence dates.
version: 0.1.0
license: MIT
---

# Record Milestone Achievement

Apply the [achievement record contract](../../specs/roadmap-modeling.md#milestone-achievement-records-and-publication).
Use the project's existing achievement register, tracker or document. A plan can
supply the event identity and criterion. The achievement records what occurred.

## Verify and record

1. Resolve the event, scope and occurrence criterion from the request and project
   sources. Use the criterion applicable to the occurrence. Reuse the plan's
   milestone ID when it identifies the same event and scope. For an unplanned
   event, look for an existing ID before assigning one under project conventions.
2. Open the original evidence using available local or authorized project tools.
   Check whether it establishes every material part of the criterion for that
   event and scope. Record only the actual timing the evidence supports. If the
   occurrence is confirmed and its date is unknown, record the date as unknown.
   For inaccessible, insufficient or conflicting evidence, identify what is
   needed to resolve the observation and leave it pending verification.
3. Check the destination for the milestone ID before writing. Reuse an existing
   record for the same occurrence and use the destination's conditional write or
   uniqueness controls when available. Resolve
   conflicts in scope, criterion or actual timing through the project's correction
   process. Apply a supported correction only when authorized and retain its history.
4. Write the confirmed record to the authorized destination and read it back.
   Use the project's format or a Markdown record with the Spec's minimum fields.
   Store stable references to the exact evidence used, including a revision or
   locator where needed. Keep the evidence in its owning system or document.
   If the destination is unresolved or inaccessible, return a reviewable draft
   and report the missing destination or access. Verify the current record before
   retrying an uncertain write.

Report the confirmed records and their locations, and identify any observations
pending verification. Publication and plan comparison use the resulting records
in separate workflows.

## Optional SVG calendar

Derive the calendar from confirmed records using the
[achievement SVG contract](../../specs/roadmap-modeling.md#milestone-achievement-svg).
Create temporary UTF-8 JSON with `title`, optional `locale` (`en` by default or
`zh-CN`) and an `achievements` array in display order. For each row supply the
milestone `id`, event `name` and `date` as an ISO calendar day (`YYYY-MM-DD`) or
`null`. Use `null` for coarser or unknown timing so the row stays unplotted. For
coarser timing, use an optional `label` to preserve the known month or year.
The renderer accepts up to 200 rows and 1 MiB of JSON.

Use Python 3.10 or later with the [achievement renderer](scripts/render-achievements.py)
and the [roadmap renderer](../define-roadmap/scripts/render-roadmap.py) from the
same local AI Cortex checkout. Render to a temporary path in a POSIX shell:

```sh
python3 "$renderer" "$input" > "$preview"
```

After a successful exit, verify the preview against the readable records before
saving or replacing an SVG at the authorized destination. If the local dependency
or SVG support is unavailable, deliver the readable records and report the
limitation. Preserve any previously saved SVG on a failed render.

## Self-Check

- Confirmed records identify the event and scope, preserve the applicable
  criterion and actual timing precision, and contain resolving evidence references.
- Evidence remains in its owning source. Pending observations stay outside the
  confirmed records and their SVG view.
- Each event has one record for the same occurrence. Saved records and drafts are
  reported accurately.
- The optional SVG uses only evidence-supported days for plotted points and keeps
  unknown or coarser dates visible as text.
