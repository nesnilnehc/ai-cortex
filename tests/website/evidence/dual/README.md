# AIC-REQ-04 dual-view local evidence, 2026-10-28

T20-T25 implement the owner-approved same-page Classification / Relationships
scheme. Local candidate: `sha256:a5abad1224f5f466b1655ccca9cc32de4a01da99639857bdd540c8e274282027` (47 files, pinned assets revision remains
`e5d862101d3110c5a3ee44c4e8cec042b058c061`). This is a working verification identity, not an accepted
release. T9/T12 owner feedback remains pending; T13/publication is unauthorized.

## Reproduce

Serve only the website root:

```bash
python3 -m http.server 4174 --bind 127.0.0.1 --directory website
node --test tests/website/*.test.mjs
python3 -m unittest discover -s tests/website -p 'test_*.py'
node tests/website/dual-browser.cjs
AIC_EVIDENCE_ROOT=dual AIC_LOCALE=zh node tests/website/explorer-browser.cjs
AIC_EVIDENCE_ROOT=dual AIC_LOCALE=en node tests/website/explorer-browser.cjs
AIC_EVIDENCE_ROOT=dual node tests/website/explorer-controls.cjs
AIC_EVIDENCE_ROOT=dual node tests/website/explorer-recovery.cjs
```

Browser runners require the existing local Playwright runtime. This run used
`NODE_PATH=/Users/nesnilnehc/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules`;
no dependency was installed or downloaded.

## Results and scope

- [Node results](node-tests.txt): 44 passed. [Python results](python-tests.txt): 18 passed.
- [Dual-view browser](dual-browser.json): 20 locale/width/theme cases, 280 skill paths;
  exact edited/pending requests, mode/active target, modal focus, collapse, section
  navigation and independent view scroll restoration.
- [Chinese graph](zh/local-branch-browser.json) and [English graph](en/local-branch-browser.json):
  20 geometry cases, 140 skill paths; sampled actual SVG paths clear nodes, topic
  routes do not cross, labels fit, selected skills stay visible above the sheet.
- [Controls](controls-browser.json): 20 cases. [Recovery](recovery-browser.json):
  measured text contrast, no-JS/module-blocked fallback, clipboard failure/stale
  completion and theme/language continuity. Public source availability is excluded.
- [Source audit](relationship-audit.json): 59 exact quotes, 36 calls, six scoped
  sequence edges at the pinned revision; unchanged canonical asset definitions.
- [Module DAG](module-dag.json): 25 ESM modules, no missing import or cycle.
- [Engineering/alignment review](review.json): separate Rule coverage and approved
  acceptance/design/task-to-production trace. Actual owner criteria remain limited.
- [Protected files](protected-files.json): 297 existing prototype/workflow/hosting
  and earlier-evidence files unchanged.

Captured red artifacts (`*-red.txt`, `browser-red.json`) document the initial
missing models and later validator, partition, layout, route, label, toolbar and
modal-focus failures. They are failure history, not current verification.

Visual review inspected the final selected classification at desktop/light and
mobile/dark, and selected relationship layouts in both locales at desktop/mobile.
See [classification desktop](classification-1440-light.png),
[classification mobile](classification-390-dark.png),
[Chinese relationship mobile](zh/local-branch-390.png) and
[English relationship desktop](en/local-branch-1440.png). All current matrix images
are adjacent to their reports. No public/provider verification is claimed.

## T12 owner walkthrough

Open [local capability overview](http://127.0.0.1:4174/zh.html?lang=zh#capabilities).
A single walkthrough can supply T9's three content conclusions and T12's distinct
integration conclusions for this exact candidate. No copied request or actual
Agent execution is required.

| Action | Question for the owner |
| --- | --- |
| Read the six Classification cards, expand a relevant category, then switch to Relationships | Is asset coverage sufficiently complete, with both representations in one coherent capability overview? |
| Inspect an orchestration skill, its children and related references; click a relationship | Are parent calls, their conditions, evidenced order and feedback/support understandable without assuming one mandatory sequence? |
| Select a skill and read its Chinese name, ID, purpose and usage | Can you tell when to use it, what to provide, how to use it and what to expect without reading English source? |
| Use Home / Capability overview / Asset directory / Get started | Are introduction, capability discovery, complete index and installation distinct and easy to reach? |
| Inspect the cross-topic document/convention and communication support entries | Is their help clearly broader than backlog/planning, without implying a required step everywhere? |
| Compare Chinese skill names, canonical identifiers and descriptions | Are names actual names and descriptions useful explanations? Flag any awkward translation. |
| Select a skill, optionally edit its request, switch both ways and use lookup | Does selection, explanation and edited content stay intact, with a clear visible location and no need to search again? |

For feedback, mark each question accepted or describe the operation, expected
result and observed problem. Silence and passing automation do not count as owner
acceptance. Publication still requires separate authorization after T12.

## Documentation checks

[Document checks](document-checks.json): all ten in-scope Markdown files pass,
relative links have zero failures and hygiene passes across 414 documents.
The complete 422-file Markdown run reports three existing MD032 blank-line
issues in the unrelated uncommitted `docs/requirements-planning/AIC-REQ-05.md`
(lines 70, 74 and 79). That content was preserved; a repository-wide Markdown
pass is not claimed. `git diff --check` passes and all 47 runtime hashes match.
