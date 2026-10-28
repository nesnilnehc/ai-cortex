# Multiple point/line/plane interpretations

Date: 2026-10-27. The owner authorized local prototype refinement while retaining
one relationship map and contextual explanation. They explicitly required that
point/line/plane allow different perspectives, rather than a permanent taxonomy.
The [UI decision](../README.md#help-perspectives-2026-10-27) records the audience,
view states, alternatives, reuse and acceptance handoff.

## Implemented scope

- The page leads with Cortex's help, not an assessment of agent capability.
- A native selector offers two interpretations: work cooperation and evidence
  connections. These are examples, not stages, user levels or exhaustive categories.
- All ten work contexts have concrete point/line/plane descriptions in both views.
  The same node, skill membership, example, request and copy identity are retained.
- Ordinary conversation and Cortex assets are explained inside a collapsed,
  scenario-specific disclosure for each context. Adopted constraints still apply.
- Changing perspective brings its explanation into view without clearing edited
  requests. Without a selected work item, only the invitation changes.
- No second graph, planning engine, actual tool invocation or external publication
  was added. Approved requirement/design snapshots remain unchanged.

`help-lenses.mjs` owns view labels/definitions and contextual help. Pure model
snapshots isolate callers. `story.mjs` owns the current view and DOM updates;
`context-copy.mjs` owns localized scenario boundaries. The existing map topology
and canonical skill definitions retain their authority.

## Verification

- [Model red log](lenses-red.txt): the new view module was absent before implementation.
- [Scroll red report](lenses-scroll-red.json): the changed help remained 694px below
  the panel viewport. The repair resets the explanation body's scroll only.
- [Final tests](lenses-tests.txt): 40 executed and passed; none failed or skipped.
- [Perspective browser matrix](lenses-browser.json): five widths and both themes,
  both interpretations, selected work/request/skill-scope preservation, single map,
  visible copy controls, no horizontal overflow and focus restoration passed.
- Extra browser checks verified empty selection, persistent view on another work
  item, disclosed scenario boundaries/assets and in-flight copy continuity.
- The existing `verify-req03.cjs` regression matrix also passed for node selection,
  search, examples, keyboard/focus, clipboard success/failure/races and fallback.
  Its report is retained as [regression results](req03-browser.json).
- [Text contrast sampling](lenses-contrast.json) passed both themes using the same
  composed-background sampling method. It is not accessibility certification.
- In-app native keyboard inspection: click the view selector, Down, Return changed
  work cooperation to evidence connections. Its accessibility tree exposed the
  selected value and the corresponding empty-view text; selecting the design node
  then exposed the evidence-specific descriptions. This native check is separate
  from the headless popup-arrow limitation retained in the browser report.
- [Desktop capture](lenses-1440-light.png) and [390px dark capture](lenses-390-dark.png)
  were visually inspected. The current workspace preview points at this revision.
- [Source manifest](lenses-manifest.json) identifies this local candidate.

Safari, real mobile hardware and spoken screen-reader behavior remain unverified.
No fresh Lighthouse or field-performance score is claimed. T7 remains In Progress;
no human comprehension pass is inferred from these programmatic checks.

## Reproduce

Use the loopback static server and existing local Playwright installation described
in the experiment README. No runtime install or remote service is required.

```sh
node --test experiments/direction-planning/*.test.mjs
node experiments/direction-planning/audit/verify-lenses.cjs
node experiments/direction-planning/audit/verify-req03.cjs
node experiments/direction-planning/audit/verify-appearance.cjs
```

Set `NODE_PATH` to the already-installed local module directory before the browser
commands, as recorded in the preceding implementation evidence. The standalone
CJS files are test harnesses; browser delivery remains dependency-free ESM.
