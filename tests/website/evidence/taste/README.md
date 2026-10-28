# Local capability typography refinement, 2026-10-28

The owner invoked `design-taste-frontend` on the delivered local capability page.
This is a preserve-mode readability repair, with dials 3/2/5, on the approved
AIC-REQ-04 scheme. Current candidate: `sha256:dff7c2c888c7970d9cd5e7b9691843d522f2161aae41c9bb7b023921bd3886db`. The previous
[dual-view evidence](../dual/README.md) remains historical evidence for its own
bytes. T9/T12 actual owner review is still pending; publication is unauthorized.

## Audit and chosen treatment

Preserve the green-gray neutral theme, rust action accent, semantic green support
lines, native system font, existing generated work illustration, same-page IA,
six functional categories, shared explanation and relationship graph. Retain
existing accessibility, language/theme and request-state behavior. No new design
system, package, decorative image or marketing section is introduced.

The prior selected English graph squeezed counts alongside names, splitting
words such as Research and Communication. Topic headings now take the full row,
counts sit beneath, and words wrap naturally. The open desktop inspector leaves
a readable minimum graph width, with local panning rather than compressed names.
Classification IDs use 11px mono, purposes 13px, call/reference captions 12px;
name, ID and explanation remain distinct. Skill buttons have a consistent 4px
content/control radius; the existing mobile sheet uses an 8px overlay radius.

The larger captions exposed an actual tablet click obstruction under the sheet
and sticky toolbar. Classification list height and native scroll/focus margins
now reserve those areas. [Initial typography failure](typography-red.txt) and
[caption layout failure](caption-layout-red.json) precede the repairs; final tests
use real clicks without forced pointer interaction.

## Reproduce and evidence

Use the existing server and local Playwright runtime; no installation is needed:

```bash
python3 -m http.server 4174 --bind 127.0.0.1 --directory website
node --test tests/website/*.test.mjs
python3 -m unittest discover -s tests/website -p 'test_*.py'
node tests/website/taste-browser.cjs
AIC_EVIDENCE_ROOT=taste node tests/website/dual-browser.cjs
AIC_EVIDENCE_ROOT=taste AIC_LOCALE=zh node tests/website/explorer-browser.cjs
AIC_EVIDENCE_ROOT=taste AIC_LOCALE=en node tests/website/explorer-browser.cjs
AIC_EVIDENCE_ROOT=taste node tests/website/explorer-controls.cjs
AIC_EVIDENCE_ROOT=taste node tests/website/explorer-recovery.cjs
```

Browser runs use the already installed Playwright found through
`NODE_PATH=/Users/nesnilnehc/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules`.
[Typography](typography-browser.json) covers both locales, four widths and both
themes, readable caption sizes, natural topic words, desktop navigation and
horizontal overflow. [Dual-view assembly](dual-browser.json) covers the five-width
matrix and 280 skill guidance paths. [Chinese](zh/local-branch-browser.json) and
[English](en/local-branch-browser.json) retain SVG/label/selected-node geometry
checks; [controls](controls-browser.json) and [recovery](recovery-browser.json)
retain keyboard, contrast, fallback and clipboard checks. [Node](node-tests.txt)
and [Python](python-tests.txt) results cover the unchanged semantic/assembly rules.
The [source audit](../dual/relationship-audit.json) still applies to unchanged
canonical definitions and relations. [Review](review.json), [preflight](preflight.json)
and [scope](scope.json) distinguish repair verification from owner acceptance.

Inspect [English selected graph](en/local-branch-1440.png),
[Chinese mobile classification](zh-390-dark-classification.png) and
[English classification](en-1440-light-classification.png). These are actual
rendered pages, rather than image mockups. Before comparison uses the unchanged
[previous English graph](../dual/en/local-branch-1440.png).

## Applicability and limits

This is a functional capability explorer within a marketing site. The owner's
explicit six-category and real relationship semantics take precedence over generic
marketing bento/card, decorative imagery and animation prescriptions. Existing
source-quoted asset descriptions retain canonical punctuation; complete skill
presentation-rule compliance for the whole site is not claimed. No new marketing
copy, logo, primary navigation, route, SEO or legal surface is changed.

Lighthouse is not available in the existing local runtime. No package was fetched
and no Lighthouse/Core Web Vitals score is claimed. Real-browser layout, contrast
and interaction checks are the evidence. Existing public hosting receipts remain
unchanged, and this candidate has no actual owner conclusion or release permission.

## T12 owner review

Open [local capability overview](http://127.0.0.1:4174/zh.html?lang=zh#capabilities).
Use the same [seven review questions](../dual/README.md#t12-owner-walkthrough),
but review the current candidate identified here. In particular, check whether
names, descriptions and relationship conditions read comfortably in both views,
and whether the same selected skill/explanation survives switching. Approval of
the previous documents or automation does not constitute acceptance of these bytes.

## Final local outcome

44 Node tests and 18 Python tests pass. The final browser checks pass 16 typography
cases, 20 dual-view cases with 280 usage paths, 20 relationship geometry cases with
140 graph usage paths, 20 controls cases and the contrast/recovery cases. Final
selected screenshots were visually inspected in English/Chinese and light/dark,
including the mobile classification and desktop selected relationship. Scoped
Markdown (five files), relative links, hygiene (415 documents) and diff whitespace
checks pass. The unchanged source audit and module structure remain valid.
Preflight limitations above remain explicit; no human experience or release pass
is inferred. The previously noted unrelated AIC-REQ-05 Markdown issues are outside
this repair and were not changed.
