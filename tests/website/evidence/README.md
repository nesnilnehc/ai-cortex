# Local website integration evidence

Scope: approved AIC-REQ-04, retained single graph and in-topic skill disclosure.
The [current audit](../../../docs/calibration/audit-docs.md#aic-req-04-approved-local-website-integration-2026-10-27)
records authorization, fixes, remaining owner acceptance and publication limits.
The [working manifest](../../../website/.openai/runtime-manifest.json) binds 36
runtime files. It is local verification evidence, not an accepted release manifest.

## Reproduce

From the repository root, serve `website/` on loopback port 4174. Browser checks
require an existing local Playwright installation with Chromium; no installer is
run by these tests. Set `NODE_PATH` to that installation when necessary.

```bash
python3 -m http.server 4174 --bind 127.0.0.1 --directory website
```

In another terminal:

```bash
node --test tests/website/*.test.mjs
python3 -m unittest discover -s tests/website -p 'test_*.py'
AIC_LOCALE=zh node tests/website/explorer-browser.cjs
AIC_LOCALE=en node tests/website/explorer-browser.cjs
node tests/website/explorer-recovery.cjs
node tests/website/explorer-controls.cjs
node --test experiments/direction-planning/*.test.mjs
```

## Recorded results

- [Node](node-tests.txt): 33 passed; [Python](python-tests.txt): 18 passed.
- [Chinese matrix](zh/local-branch-browser.json) and [English matrix](en/local-branch-browser.json): 200 topic/size/theme selections and 140 full skill paths combined.
- [Recovery](recovery-browser.json): 16 contrast samples and eight clipboard cases, with blocked-module/no-JS and preference recovery.
- [Controls](controls-browser.json): 20 locale/size/theme scenarios, including long selected skills above the mobile sheet.
- [Original model tests](prototype-model-tests.txt): 63 passed; [reference control check](prototype-controls-browser.json): ten scenarios after the scoped short-panel repair.
- [Engineering review](engineering-review.json) and [implementation alignment](implementation-alignment.json): no code findings; owner acceptance is explicitly pending.

Red failure reports are retained beside the passing evidence. Chromium emulation
is not native-device or spoken-screen-reader testing. Source hashes were verified
locally at the pinned asset revision; public reachability/provider behavior and
publication are outside this run. Owner coverage/meaning/use conclusions remain
pending and must not be inferred from these checks.
