# Topic-spine branch verification

Date: 2026-10-27. Scope: local prototype only; no publication or owner acceptance.

- 58 model tests passed, including exact skill partition, evidence-backed forest
  placement, shared-method roots, cycle prevention and near-side route geometry.
- Browser checks passed all 70 selection paths and ten viewport/theme combinations
  (360, 390, 1024, 1280 and 1440px; light and dark).
- Formal names and Chinese purposes remain visible and fit without overlap. The
  browser sampled actual SVG segments against every node interior; no collisions
  were found for all selections or the dense review hub matrix.
- Keyboard selection, focus return, peer navigation, usage guidance, work-request
  retention, narrow-screen selected/related-node visibility and context-only resize
  passed. No page errors or horizontal overflow were observed.
- Desktop overview and mobile/desktop release details were visually inspected.

Evidence: [unit log](branch-layout-tests.txt), [browser report](branch-layout-browser.json),
[reproducible browser checks](verify-branch-layout.cjs),
[overview](branch-layout-overview.png), [desktop detail](branch-layout-1440.png),
[mobile detail](branch-layout-390.png).
