# Per-skill usage: local verification

Date: 2026-10-27. Authority: AIC-REQ-04 A5/A7/A8 and the owner's explicit local
prototype instruction. Scope: the single relationship map and contextual skill
explanations. No publication or real skill execution.

This records the preceding nested-disclosure revision. For the current fixed
asset entry, use [fixed-entry verification](asset-entry-evidence.md).

## Delivered behavior

All 70 current skills have individually maintained Chinese explanations of when
they apply, what to provide, how to use them and what result to expect. Requests
are natural-language examples, not invented slash-command syntax. Related skill
names open native disclosures beside the existing map. Optional lookup reveals
the selected skill's same four fields at the panel's top. Source reading is
optional; access/setup guidance is provided in Chinese after the four fields.

The internal `assess-product-opportunity` capability routes through its public
`product-opportunity-analysis` coordinator. Review is distinguished from repair;
commit, integration, release preparation, publication and announcement retain their
separate outcomes and conditions. The page performs none of those operations.

`skill-guidance.json` owns display content; local Skill definitions retain
instructional authority. Stored source hashes detect subsequent definition drift.
Hash matching and field-presence tests do not themselves prove semantic fidelity:
source contracts and consequential boundaries were inspected while writing the
summaries, and owner whole-map review remains separate.

## Executed checks

- Registry synchronization: 70 current skills, in sync.
- [Model tests](skill-guidance-tests.txt): 45 passed, zero failed or skipped.
- [Browser report](skill-guidance-browser.json): all 70 skills opened through their
  actual map contexts; four displayed fields match their localized content; all
  defining links return the matching source bytes. Browser version, date and
  changed-file hashes are recorded in that report.
- Optional lookup opens the same panel; native skill disclosure and edited request
  survive perspective changes. No additional map is created.
- Pointer exploration plus keyboard disclosure/close/focus recovery pass at
  360/390/1024/1280/1440 CSS-pixel widths in light and dark themes. Close remains
  reachable and the document has no horizontal overflow in the checked states.
- Existing graph-perspective regression is rerun with the retained
  [browser harness](verify-lenses.cjs); its report is [recorded separately](lenses-browser.json).
- Desktop and mobile screenshots were inspected for hierarchy, wrapping, panel
  scrolling and fixed close/action controls: [1440px](skill-guidance-1440.png)
  and [390px](skill-guidance-390.png).

## TDD and repair evidence

The new model suite first failed because the guidance module did not exist; an
additional test then failed for the internal/public entry distinction. The new
browser path first failed because per-skill disclosures did not exist. Those
checks now pass without removing or weakening their assertions.

A responsive check exposed a transient 21px document overflow on widening the
viewport from 390px to 1024px: existing transform transitions animated the graph
nodes' positioning between mobile and desktop layouts. Disabling that positioning
transition repaired the failure while preserving native disclosure and reduced
motion behavior. The same resize path remains in the browser verification.

## Limits and acceptance

Checks use local Chromium and the existing installed runtime. No Safari, real
device, native zoom or spoken screen-reader verification is claimed. Existing
fallback behavior is retained; no new runtime recovery guarantee is introduced.
Owner whole-map acceptance under A9 remains pending. Tests and screenshots do not
prove every reader understands the content. No commit, push or public release was
performed.
