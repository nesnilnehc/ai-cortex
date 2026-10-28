# Graph-level perspective refinement

Date: 2026-10-27. The owner requested that the map itself change focus with the
selected view, and questioned exposing point/line/plane terminology to readers.
This authorized local refinement preserves the single primary graph and
contextual details. It supersedes the prior prose-only view behavior.

## User-facing behavior

- Work and cooperation shows actions, bidirectional work/recheck relationships
  and a shared-work region.
- Artifacts and evidence shows documents, records and receipts; reference
  endpoints and explicit correspondence labels; and a dashed shared-delivery
  region emphasizing consistency. Actual operation prerequisites remain separate.
- Positions and logical IDs stay stable so corresponding subjects are easy to
  compare. Node form/subtitle, relation meaning/endpoints, group treatment, legend,
  accessible names and the textual alternative change together.
- Reader labels use concrete phrases such as This work, How it connects,
  Resulting artifact and Overall checks. The internal geometric terms no longer
  appear as reader-facing headings, instructions or a prerequisite explanation.
- Skill membership, selected logical context, edited requests, examples and copy
  identity remain stable when changing the view. No stage is advanced.
- Ordinary dialogue versus Cortex assets remains inside scenario disclosure.

The [UI decision](../README.md#graph-level-perspectives-2026-10-27) explains why
stable positions were retained instead of a disorienting complete relayout.
`getMapProjection()` owns the alternate subjects and relation descriptions;
composition updates one existing DOM graph. No second graph or external graph
package was added. Canonical definitions retain their source authority.

## Evidence

- [Observed red test](graph-perspectives-red.txt): the graph projection contract
  was missing before implementation.
- [Final model/source tests](graph-perspectives-tests.txt): 41 executed and passed,
  zero failures or skips. The new test verifies distinct projected subjects,
  relation meanings and group description, matching logical node IDs, isolated
  snapshots and removal of the internal terms from public headings.
- [Both-view browser checks](graph-perspectives-browser.json): ten viewport/theme
  combinations, each checking both views, actual node titles, connector text and
  endpoint markers, shared-region border form, preserved selection/request/skill
  scope, one graph, visible copy controls and no horizontal document overflow.
- Additional checks retain copy continuity, empty-view behavior, scene disclosure
  and focus restoration. The baseline search/copy/keyboard/fallback regression
  harness also passed; see [regression report](req03-browser.json).
- [Contrast sampling](graph-perspectives-contrast.json) passed all four theme/view
  combinations: minimum 4.95:1 light and 6.29:1 dark. This samples computed text
  against composed backgrounds; it does not certify complete accessibility.
- Native in-app click/Down/Return selection changed the map to the evidence view;
  the accessibility tree showed changed artifact names, shared context and map
  description. Headless native-popup keyboard limitations remain separately
  identified in the browser report.
- [Work view](graph-work-desktop.png) and [evidence view](graph-evidence-desktop.png)
  show corresponding subjects at stable locations. [Mobile work](graph-work-mobile.png)
  and [mobile evidence](graph-evidence-mobile.png) keep one readable map without
  the detail sheet obscuring its contents. Desktop evidence and mobile evidence
  captures were visually inspected.
- [Source manifest](graph-perspectives-manifest.json) identifies this working-tree
  candidate. Older perspective reports and images are historical revisions.

No public website or approved canonical requirement/design snapshot was modified.
No commit, push or publication occurred. The prototype neither executed skills nor
mutated project state.
T7 remains In Progress and requires the continued human walkthrough. Safari, real
mobile hardware and spoken screen-reader behavior are not claimed verified. No
fresh Lighthouse or field-performance score is claimed.

## Reproduce

With the repository-root loopback server running and `NODE_PATH` set to the existing
local Playwright modules as documented in the experiment README:

```sh
node --test experiments/direction-planning/*.test.mjs
node experiments/direction-planning/audit/verify-lenses.cjs
node experiments/direction-planning/audit/verify-req03.cjs
node experiments/direction-planning/audit/verify-appearance.cjs
```
