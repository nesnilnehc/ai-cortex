# AIC-REQ-04 accepted publication, 2026-10-28

Sites version 8 is published and publicly verified at
[AI Cortex](https://ai-cortex.nesnilnehc.top/).
The owner accepted T12, then explicitly approved the address compatibility repair
and T13 publication. T9/T12/T13 and all implementation tasks are Done;
AIC-REQ-04 is implemented on 2026-10-28.

## Exact identity

| Identity | Value |
| --- | --- |
| Accepted/published runtime | `sha256:1424a8bb40733a4a06ce41cbd4b63e9c411d4bb35ff941aad5b9eebb115d57ca` |
| Isolated Sites source commit | `f9762c952eb9c3847524dbdd2d52376c4224a19d` |
| Saved version | `appgprj_6adad0ee0f4881918acd4d3754f500af~appgver_84cf5ae9f2f08191b807714f228882e4` (version 8) |
| Deployment | `appgdep_6ae181e21bbc81919009450c9496f0af` (succeeded) |
| Preserved asset revision | `e5d862101d3110c5a3ee44c4e8cec042b058c061` |
| Public audience/domain | Unchanged public Site, `ai-cortex.nesnilnehc.top` |

[Provider receipt](provider-receipt.json), [published manifest](published-runtime-manifest.json)
and [publication record](publication.json) retain source, local archive, provider
archive, deployment and recovery identities. The local compressed upload and
provider stored-container digests are recorded separately; no equality of those
containers is asserted. Exact logical runtime source/delivery is independently
verified below. Only the isolated Site source was committed/pushed; the AI Cortex
repository and unrelated work were not committed or uploaded.

## Verification

- [Public runtime](public-runtime.json): 47 real HTTPS resources pass TLS, MIME and
  accepted-source checks; 43 non-HTML byte matches and four complete HTML sources
  with only the observed provider security-script insertion.
- [Public browser](public-browser.json): eight actual deployed-origin cases across
  English/Chinese, 360/1280 widths and light/dark. Both view entries, coordinator
  hierarchy, conditional call/scenario order, guidance, edited request continuity,
  keyboard focus, support scope, full directory/type/install/history, language/theme
  and legacy clean routes pass. Both locales pass no-JS and blocked-entry recovery;
  zero page errors. Only clipboard denial/module blocking are injected recovery
  cases; no local resource fulfillment is used in this public smoke.
- [Node](node-tests.txt): 46 pass. [Python](python-tests.txt): 18 pass.
- [Host-route simulation](host-route-browser.json): eight pre-release cases.
- [Canonical sources](public-sources.json): 137 public URLs pass, with pinned hashes.
- [Public verifier unit checks](public-verifier-tests.txt): exact HTML/non-HTML,
  provider insertion positions, unknown added HTML, MIME/TLS and identity negatives.
- [Known-good serving](known-good-serving.json): ten version-7 resources verified
  before the switch. [Prior public receipt](previous-public-verification.json)
  retains the earlier canonical verification record.

The initial [clean-route reproduction](host-route-preflight.json) and
[red-first route tests](host-route-red.txt) precede the compatibility repair.
[Initial HTML-verifier result](public-runtime-insertion-red.json) reflects a test
assumption about security-script placement, not changed public source: the
legacy stubs have no closing body tag and the provider appends its script after
exact original source. [Negative fixtures](public-verifier-legacy-red.txt)
precede support for this observed position; [extra-HTML negatives](public-verifier-red.txt)
reject arbitrary content carrying a provider marker. The browser waits for
asynchronous theme restoration after language navigation rather than checking its
uninitialized selector. Neither harness adjustment changed approved runtime bytes.

## Recovery and limits

Known-good version 7 is retained as
`appgprj_6adad0ee0f4881918acd4d3754f500af~appgver_ad106f4e8194819194699ca35f33e608`;
[baseline](known-good.json) records its source, serving and recovery path.
Version 8 passed public verification, so recovery was not needed or executed.
A later confirmed regression requires establishing actual serving state before
redeploying a non-conflicting retained version. No DNS/access policy changes,
announcement messages, Lighthouse/Core Web Vitals score, native-device or spoken
screen-reader pass are claimed. Old local guides/receipts retain historical scope.
