# Approved local site-structure revision

Scope: AIC-REQ-04 T16-T19, approved on 2026-10-28. This evidence concerns the local
website candidate, not public deployment or an owner's acceptance result.
The [current audit](../../../../docs/calibration/audit-docs.md#aic-req-04-approved-site-structure-implementation-2026-10-28)
records scope and limits; the [working manifest](../../../../website/.openai/runtime-manifest.json)
identifies runtime bytes. `ownerConclusion:null` is deliberately unfinished.

## Reproduce

Serve `website/` on loopback port 4174. Use an existing Playwright/Chromium
installation; set `NODE_PATH` if necessary. No installation is performed.

```bash
node --test tests/website/*.test.mjs
python3 -m unittest discover -s tests/website -p 'test_*.py'
AIC_EVIDENCE_ROOT=revision AIC_LOCALE=zh node tests/website/explorer-browser.cjs
AIC_EVIDENCE_ROOT=revision AIC_LOCALE=en node tests/website/explorer-browser.cjs
AIC_EVIDENCE_ROOT=revision node tests/website/explorer-controls.cjs
AIC_EVIDENCE_ROOT=revision node tests/website/explorer-recovery.cjs
node tests/website/revision-browser.cjs
```

## Evidence

- [Node tests](node-tests.txt) and [Python tests](python-tests.txt) include source, locale, safe routes, complete directory, native navigation mirrors and name/identity contracts.
- [Chinese map](zh/local-branch-browser.json) and [English map](en/local-branch-browser.json) exercise 200 topic/size/theme selections and 140 full skill paths together, with geometry, search/peer reveal and focus checks.
- [Control paths](controls-browser.json) cover 20 locale/size/theme scenarios, including a minimum usable work-panel body and selected long skills above the sheet.
- [Recovery](recovery-browser.json) covers contrast, clipboard failures/stale completions, script-free/blocked-entry source recovery and preferences.
- [Site revision paths](site-revision-browser.json) cover 20 locale/size/theme combinations: directory bookmarks, language/type anchors, history/active state, support navigation, Chinese names, keyboard close and native no-JS directory access.
- [Engineering and alignment review](review.json) records revised-scope results and pending human criteria.

Intent-derived red reports are retained here. Old evidence outside this directory
remains tied to the old revision. Final captures show the same revised candidate.
Chromium emulation is not native-device, browser zoom or spoken-screen-reader
validation. Canonical quotes are checked locally at the pinned revision; public
source reachability, provider/TLS/recovery operations and publication are not tested.
No copied request or real skill execution is required for T12.
