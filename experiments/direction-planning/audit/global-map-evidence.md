# Persistent global topic graph verification

Date: 2026-10-27. Scope: local prototype only. Publication and owner acceptance
are not implied by these machine checks.

## Model checks

62 tests pass. The new global-graph tests failed before implementation. They verify
ten unique topic placements, one connected work-context graph, ten explicitly
non-directional help associations, three anytime support associations, canonical
source quotes, unchanged directional summaries, isolated snapshots and corridor
geometry. The associations do not enter the 53-edge skill-dependency registry.

## Browser checks

The default graph contains ten topics, one work context and 13 persistent topic
paths. Expanding each topic leaves all topic paths and their geometry unchanged.
Only the skill-branch dock changes; it is inside the same primary canvas and does
not contain a second topic map. Closing all branches restores the same topology.

All 70 skill selection paths retain formal names, Chinese descriptions, four usage
fields, source-backed direct relation counts and peer navigation. Search and peer
navigation reveal folded target branches. Keyboard dismissal/focus, request
retention and context-only resize pass. Every source hash and browser version is
recorded in the browser report.

Five widths (360, 390, 1024, 1280 and 1440px), each in light and dark, pass. Checks
include label bounds, node size, selected-node visibility, no page overflow and the
dense review hub. Actual skill SVG segments are sampled against skill interiors;
topic SVG segments are independently sampled against topic interiors. Proper
orthogonal segment crossings are checked in each layer. No intrusion or proper
crossing was found. Shared trunks/endpoints are intentional drawing corridors,
not additional semantic dependencies.

A separate compact-desktop capture verifies the complete topic board fits in a
1280×800 viewport. Desktop overview and mobile detail captures were visually
inspected. Smaller screens retain readable labels through normal vertical page
scrolling; no claim is made that all mobile topics fit simultaneously on screen.
Owner understanding and formal approval remain unverified.

## Reproduction and captures

- [Model log](global-map-tests.txt)
- [Browser harness](verify-global-map.cjs)
- [Browser report and source hashes](global-map-browser.json)
- [Desktop overview](global-map-overview.png)
- [1280×800 complete overview](global-map-1280-overview.png)
- [Desktop skill detail](global-map-1440.png)
- [Mobile skill detail](global-map-390.png)
