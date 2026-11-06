# AI Cortex promotional website

## Current publication

Sites version 18 went live on 2026-11-06 at
[AI Cortex](https://ai-cortex.nesnilnehc.top/). The catalogue contains 74 Skills,
including plan-milestones 0.2.1 and define-roadmap 7.13.5. The bilingual Skill
details explain milestone prerequisites and roadmap references. The 49 runtime
files come from repository commit `a5e18e40ea0532aa6147395ac069fabcedb7e143`.

All 77 website tests passed. HTTPS checks on the custom domain matched the
published source manifest, provenance, Skill metadata and both locale files to
the repository bytes. The pinned plan-milestones source matched version 0.2.1.
The [deployment receipt](.openai/deployment.json) records the published source
and verification scope.

## Prior publication

Sites version 17 went live on 2026-11-05 at [AI Cortex](https://ai-cortex.nesnilnehc.top/),
preserving the existing domain and public audience. The catalogue contains 73
Skills, including prepare-version-notes 0.1.1 with the reviewed net-difference
and completion clarifications. Source and provenance links pin
`5f4e10ecb00603eec8b724be0e4a1e9024492efb`; runtime references use
`version-notes-refinement-20261105`. The 49 runtime files and unchanged hosting
manifest were packaged from Sites source commit
`b604315d883f7732756ef9797cf9ee515372e94c`, matching repository runtime state
merged and pushed as `b556f427b2bc21d5fb55edad2aa257d87213c064`.

The unchanged local inputs retain passing 18 Python and 59 Node website tests.
Post-publication HTTPS checks found byte-identical source manifest, Skill metadata
and provenance JSON at the custom domain. The pinned public Skill source also
matches local bytes and declares 0.1.1. A live Chinese desktop browser check
confirmed the 73-Skill directory, delivery category and new Skill detail.
The [publication checks](.openai/publication-20261105-version-notes.json) retain
the provider result and verification scope.

## Prior publication: presales evidence update, 2026-11-02

Sites version 16 is public at [AI Cortex](https://ai-cortex.nesnilnehc.top/),
with the existing domain and public audience preserved. The catalogue and source
links now pin `cf6bdd396f87f81be72b9e0d7dfaea69aeaeddd7`, including the reviewed
prepare-presales-response 1.1.0 and its native provenance confirmation. Runtime
references use `presales-sync-20261102`; layout and displayed copy are unchanged.
Only the existing 49 runtime files and hosting manifest were packaged, from
Sites source commit `f1bff1e5c3d7919add053607074196314d6f9497`.

Validation passed 18 Python website tests and 59 Node tests. Public HTTPS checks
confirmed byte-identical source manifest, skill metadata and provenance JSON,
and the current source/cache identity in both homepage editions. No new browser
visual check is claimed. The [deployment receipt](.openai/deployment.json) and
[publication checks](.openai/publication-20261102-presales.json) record this update.

## Prior publication: asset synchronization, 2026-11-02

Sites version 15 is public at [AI Cortex](https://ai-cortex.nesnilnehc.top/),
preserving the existing domain and public audience. Both editions contain 68
Skills, 20 Specs, 34 Rules and one Protocol, including the build/release asset
retirement. Asset and provenance links pin `c22d8e5b30ad26a859b71cb39bddfdac1e8991d5`.
All versioned runtime references use `assets-sync-20261102`, including the legacy
entries, styles, icons and illustration. Static fallback source links use the
same asset revision as the interactive catalogue.

Validation passed 59 Node tests, 18 Python website tests, the generated index
check and the asset count check. Regression assertions first failed on the stale
cache and source references, then passed after repair. All 49 public runtime
files passed HTTPS, MIME and source checks: 45 matched byte for byte; four HTML
files differed only by the recognized provider security script. Browser checks
covered Chinese search and details, removal of `build-artifacts`, and the English
legacy entry's redirect into the working Relationships view. The isolated Sites
source commit is `dc1cbf8121bef8deb8e57e305c056bccdbbcc137`.

The [deployment receipt](.openai/deployment.json) and
[publication verification](.openai/publication-20261102.json) identify this release.
Only the 49 runtime files and hosting manifest were packaged. The sections below
retain prior publication and design evidence; they do not describe the current
catalogue unless explicitly stated.

## Prior publication: build-artifacts rename, 2026-11-01

Sites version 14 is public at [AI Cortex](https://ai-cortex.nesnilnehc.top/), with
its existing public audience preserved. Both languages use `build-artifacts` for
the independent build capability. Preparation and publication retain conditional
build calls; saved invocations must use the new name without an old-name alias.

Asset links pin `bb6b238c26e3a89ec4fabf5defe9893d34daafc1`. Website runtime files
come from public repository commit `ff5002aefc68a495f57e53fe744f4c2907b6e3af`;
the Sites source commit is `43ff245082b9f2f81c9bcd75ebb90bd7c5d6f73b`.
The [deployment receipt](.openai/deployment.json) records this publication. Version 13 and earlier records remain historical.

All 49 live runtime files were checked against the published source: 45 are
byte-identical and four HTML files differ only by Cloudflare's security script.
Both live language editions were inspected for the new name, conditional calls,
usage instructions and fixed source links. Pre-publication checks passed 58 Node
website tests, 18 Python website tests and the source/index checks. Other sessions'
28 pre-existing working files remained byte-identical and were excluded from the
website package. No other product build, upload or publication was performed.

A standalone static introduction to AI Cortex in English and Simplified Chinese. Serve this
directory directly; there is no package installation or build step.

## Preview

From the repository root:

```bash
python3 -m http.server 4173 --bind 127.0.0.1 --directory website
```

Open [the local preview](http://127.0.0.1:4173). Stop the server with Ctrl+C.
Native navigation and disclosures work without JavaScript. The optional module
adds command copying and a System/Light/Dark theme selector. Theme and language choices are saved locally as described below. With scripts disabled, theme follows the system.

## Content and design

The [README](../README.md), [asset terminology](../docs/architecture/terminology.md)
and asset indexes remain the content authority. Avoid copying catalogue counts
or inventing customer evidence. The install snippet is checked against the README.

- [Requirement AIC-REQ-02](../docs/requirements-planning/AIC-REQ-02.md)
- [Functional design](../docs/designs/2026-10-23-promotional-website-functional-design.md)
- [Technical design](../docs/designs/2026-10-23-promotional-website-technical-design.md)

The page uses local assets and system fonts, one orange accent and neutral
surfaces, responsive CSS, native disclosures and announced copy feedback.
There are no runtime services, analytics, cookies or visitor data submissions.

## Checks

```bash
node --test tests/website/*.test.mjs
python3 -m unittest discover -s tests/website -p 'test_*.py'
```

Run from the repository root. Node's built-in test runner verifies clipboard
success, rejection/retry, unavailable API, concurrent clicks and empty commands.
The five behavior tests were first observed failing against an empty controller,
then passed after implementation. Python's standard-library checks verify
installation parity, section anchors, source destinations, local assets and
search metadata. These checks do not establish remote resource availability.

The existing CI workflow runs both commands. Local validation on 2026-10-23 used
Node 20.20.2 and Python 3.11; no third-party test packages were installed.

### Browser acceptance evidence (2026-10-23)

| Check | Observed result |
| --- | --- |
| Desktop at 1280px and phone at 360px | Document width equaled viewport width; screenshots inspected for layout and legibility |
| Light and dark | Theme selector changed the full page; both themes inspected at both widths |
| Task discovery | Governance and research disclosures opened by Enter; relevant source links were present |
| Keyboard feedback | Focused summary had a visible solid outline; native FAQ disclosure also opened with Enter |
| Installation | Primary action reached `#start`; clicking Copy showed completed-success feedback |
| No JavaScript | A loopback test server blocked scripts with CSP; theme/copy actions stayed hidden, all commands remained readable, FAQ opened by keyboard |
| Error recovery | Rejection/retry and missing API passed controller tests; an attempted browser Permissions-Policy denial was not enforced by the preview browser, so native permission-denial behavior is not claimed as browser-verified |
| Source consistency | Five content/asset tests, link checks, document hygiene, CLI-documentation checks and changed-Markdown lint passed |

Reduced-motion behavior was source-inspected: there is no automatic animation,
and optional color transitions are gated by `prefers-reduced-motion: no-preference`.
An actual OS preference change was not tested. Lighthouse is not installed in
the local toolchain, so no Lighthouse score is claimed. Production Core Web
Vitals and real-device behavior need separate verification.

## Deployment

Public address: [AI Cortex](https://ai-cortex.nesnilnehc.top/). Configure a static host to
serve this directory with HTTPS and JavaScript MIME types for `.mjs`. The directory
has canonical metadata, `robots.txt` and a sitemap. Exclude this guide from the
published asset bundle if the host supports an explicit include list.

### Published deployment (2026-10-23)

Sites version 7 is public at [the custom domain](https://ai-cortex.nesnilnehc.top/)
and [the hosted origin](https://ai-cortex.mystic-loon-2462.chatgpt.site).
The [hosting identity](.openai/hosting.json) and
[deployment record](.openai/deployment.json) retain the exact project, version,
source commit and domain status. Only the ten runtime files listed in that
record were packaged; repository documentation and unrelated local changes were
not uploaded.

The deployment source checkout is separate from this repository. Prepare its
`dist/` from the runtime files in `website/`, copy `.openai/hosting.json` to its
root, and use the Sites source helper to push/package the matching source before
saving and publishing a new version. The manifest's `dist` is that deployment
checkout's output directory. Never deploy the entire AI Cortex repository.

Origin verification: anonymous HTTPS returned HTTP 200 with TLS verification
successful. All six non-HTML assets matched local bytes. HTML preserved the full
source with only an observed Cloudflare security script inserted before the
closing body tag. Python's own local certificate store could not validate the
chain; verification used system curl with certificate validation enabled.

The custom domain is registered with Sites. The following records were added
through the NameSilo DNS console on 2026-10-23 with TTL 3600 seconds; all three
were read back from the saved record list. Names are relative to `nesnilnehc.top`.
Existing unrelated records were preserved.

| Type | Name | Value |
| --- | --- | --- |
| CNAME | `ai-cortex` | `custom-domains.chatgpt.site.` |
| TXT | `_openai-site-verification.ai-cortex` | `openai-site-verification=3GJDbMTElqPCHX_8KPtDgVDph2wYkOFbYfUp8YjQfWQ` |
| TXT | `_cf-custom-hostname.ai-cortex` | `ea3e95ec-3348-420e-8a7a-99240aeb6c62` |

Custom-domain verification completed on 2026-10-23 at 13:48 Asia/Shanghai. Sites
reports domain, provider and certificate status as `active`. Anonymous requests
to the custom hostname returned HTTP 200 with successful TLS validation for the
homepage and all six static resources. The static resource bytes match local
source; HTML preserves local source with the observed Cloudflare security-script
insertion. JavaScript modules have the `text/javascript` MIME type.

The live browser rendered the page at the custom hostname, navigated to
installation, showed completed copy feedback, and expanded a FAQ using Enter.
The document width equaled the 1280px viewport. Detailed response types, hashes
and timestamps are retained in the [public verification record](.openai/public-verification.json).
Some recursive DNS caches returned earlier negative answers during propagation;
no DNSSEC or certificate verification protections were disabled.

## Language editions

English keeps the root URL; [Simplified Chinese](https://ai-cortex.nesnilnehc.top/zh.html)
uses `zh.html`. Header links work without JavaScript. Selection opens the other
edition at the top and saves an origin-local language preference.
Both editions share CSS and modules, while copy feedback comes from the page's
`data-*` messages. Each page has its own language, canonical URL and alternate
language metadata. Repository sources and commands remain unchanged.

When editing content, update both HTML editions and check their equivalent meaning.
Localization tests compare IDs, destinations, metadata and feedback fields. Add a
new edition only with reviewed copy, native language links, metadata and sitemap
coverage; do not introduce automatic translation. See the
[functional design](../docs/designs/2026-10-23-website-localization-functional-design.md)
and [technical design](../docs/designs/2026-10-23-website-localization-technical-design.md).

Localization verification on 2026-10-23: six clipboard tests and ten static
contracts passed, including equivalent commands, section IDs, links and all four
feedback messages. Localization and localized-feedback tests were observed failing
before implementation. Browser checks covered both languages at 360px and 1280px,
Chinese light/dark layouts, keyboard language navigation and Chinese copy success.
Public verification covered both HTML pages and all six resources over validated
HTTPS. Shared CSS/modules use a release query identifier to avoid stale edge or
browser resources after publication. The initial multilingual release used explicit selection only; the preference
behavior below extends that release.

Sites redirects `/zh.html` to its clean URL `/zh` (HTTP 307); following the
redirect returns HTTP 200 with validated TLS and the complete Chinese edition.
The source preview serves `zh.html` directly.

## Automatic language selection and preference

On either edition, selection follows this order: valid `lang=en|zh` URL choice,
saved manual preference, first supported entry in the browser language list,
English fallback. Regional Chinese tags select Simplified Chinese display copy.
Browser-inferred language is not saved. Native language links carry a choice
parameter so they can override a previous choice even if storage is unavailable.

The optional `ai-cortex.language` localStorage key contains only `en` or `zh`.
It persists across visits on the same origin until replaced or browser site data
is cleared; it is not synced across devices or sent to an application service.
Blocked storage falls back to browser detection on later visits. Without JavaScript,
complete static editions and native language links remain available.
Automatic navigation uses history replacement and retains query parameters and
section fragments; an already matching edition does not redirect. A shared edition
URL without an explicit choice follows the recipient's saved/browser preference.

The [functional design](../docs/designs/2026-10-23-language-preference-functional-design.md)
and [technical design](../docs/designs/2026-10-23-language-preference-technical-design.md)
record this extension. Six locale tests were observed failing before implementation
and now pass alongside the existing sixteen checks. Browser acceptance verified
English keyboard selection, reopening a Chinese URL while English was preferred,
retained `#start`, Chinese override and reload persistence.

Production version 4 passed the same preference navigation and reload checks on
the custom domain. Both HTML editions and all seven resources returned final
HTTP 200 over validated HTTPS; all seven non-HTML resources matched local bytes.

## Theme preference and capability atlas

System is the default theme. CSS `prefers-color-scheme` follows system appearance
changes while System is selected. Manual Light/Dark overrides remain fixed; the
`ai-cortex.theme` localStorage key saves the selected `system`, `light` or `dark`
value across visits and language changes. Storage denial leaves current-page
selection usable. Clearing browser site data resets the preference.

The capability section is now a native, responsive atlas: six task domains contain
all 70 registered Skills, while three foundation branches contain all 21 Specs,
33 Rules and one Protocol. These counts describe the 2026-10-23 registry state,
not a permanent product claim. Each asset has an on-site purpose summary and an
optional source reference. The grouping expresses membership, not dependencies
or a required execution order. Native disclosures work without JavaScript.

When registries change, update both editions' atlas entries and counts;
`tests/website/test_map.py` checks complete membership, uniqueness and branch counts.
The English registry descriptions and reviewed Chinese display summaries remain
subordinate to the defining assets. No external graph runtime is loaded.

- [Functional design](../docs/designs/2026-10-23-theme-and-capability-map-functional-design.md)
- [Technical design](../docs/designs/2026-10-23-theme-and-capability-map-technical-design.md)

Theme and atlas tests were observed failing before implementation. The full suite
now has 17 Node behavior tests and 12 Python content/registry tests. Native Chrome
inspection verified on-site branch content, keyboard disclosure operation, dark
theme restoration after reload, and dark appearance across language changes.
Rendered fixed-size iframe previews verified the Chinese atlas at 360px and the
English atlas at 1280px. Browser automation transport was unavailable, so these
were inspected through native Chrome rather than DOM viewport measurements.
System-following behavior is implemented by CSS media queries and source-reviewed;
an actual OS appearance change has not been exercised.

Production version 5 returned validated HTTPS HTTP 200 for both editions and all
eight resources, with source-preserving HTML and byte-identical non-HTML assets.
Native Chrome verified the custom-domain atlas and dark-theme restoration after
reload. The public verification record contains the response types and hashes.

The production selector also returned from Dark to System successfully. This mode
was retained as the final browser state; OS appearance itself was not changed.

## Shared brand asset

The header, footer and favicon reference the same [`favicon.svg`](favicon.svg).
The Cortex core mark uses an open C outline, a central node and a connecting
bridge, preserving the existing orange and warm-white palette. The repository
README uses a compact text heading. See the [brand usage guide](../docs/brand/README.md)
for sizing, clear space and the personal-site mirror contract.

Production version 7 replaces the former stacked-bar mark. Both HTML editions
use a new icon cache identifier. This changes the shared vector asset within the
existing layout; language, theme and navigation behavior remain unchanged.

## Current published version, 2026-10-28

Sites version 8 is public at [AI Cortex](https://ai-cortex.nesnilnehc.top/).
The owner accepted the integrated dual views and approved the clean-URL repair.
The [deployment](.openai/deployment.json), [public verification](.openai/public-verification.json)
and [accepted runtime manifest](.openai/runtime-manifest.json) identify the exact
published source and owner conclusion. All 47 public resources and eight real
public browser cases pass; both no-JS/blocked-entry fallback locales pass.
The public domain/audience are unchanged. Only the isolated Sites source checkout
was committed/pushed; the AI Cortex repository was not. Version 7 remains the
known-good recovery target; no rollback was performed.

The sections below describe implementation and dated local-stage evidence.
Their former authorization limits are historical; the current publication receipt
and verification are in [the release evidence](../tests/website/evidence/release/README.md).

## Same-page capability discovery: approved local integration

The homepage capability section (`/#capabilities` and `/zh.html#capabilities`)
provides Classification (default, original six cards) and Relationships (the
retained ten-topic graph). They share canonical skill IDs, localized names,
purposes, four-field usage guidance, lookup, one detail panel and one editable
request/copy controller. Switching preserves selection, the active explanation,
mode and edited/pending-copy identity, plus each view's disclosure/list/pan state.
Only evidence-backed calls create children; required calls are relative to the
applicable parent route. Scenario order is partial; layout never prescribes a
universal workflow. Other references remain explicitly typed.

Global navigation is Home / Capability overview / Asset directory, with Get
started as the adoption action and language/theme as utilities. Overview and the
compact four-type `#asset-directory` are sections of this same page. Old type,
category and installation anchors remain meaningful. `/explore/` and its HTML
editions are compatibility stubs linking/redirecting to the matching homepage
relationship view, not separate interactive pages. Native classification cards
and the complete directory remain usable with JavaScript disabled.

`site-navigation.json` and `site-navigation.mjs` own routes, section identity,
validated no-reload section navigation and same-language view/fragment mapping.
`explore/explorer-host.mjs` is the shared composition owner; `explorer-state.mjs`
owns semantic/view state. `classification-view.mjs` and `relationship-view.mjs`
render the two representations. `relationship-model.mjs`, `classification.json`
and the existing skill/topic/support records provide shared source-backed data.
The replaced `story.mjs` composition was removed. No framework or installation
step is required; serve only `website/` as the isolated static root.

`explore/locales/` owns reader copy; `skill-metadata.json` owns canonical identity
and source hashes. `source-manifest.json` pins asset links independently of the
runtime revision. Changed transitive modules/data share `aic04-host-1`. Changing
runtime bytes requires refreshing affected verification and the working
`.openai/runtime-manifest.json`; its owner conclusion stays null until actual
T9/T12 feedback. It is not an accepted release manifest.

[Dual-view evidence](../tests/website/evidence/dual/README.md) records repeatable
checks, visual review, source audit, candidate identity and limits. Existing
hosting/public-verification receipts describe the earlier public site. T13,
commit, push, upload and publication were not authorized or performed.

### Preserve-mode typography follow-up

The owner's `design-taste-frontend` invocation prompted a local audit and targeted
readability repair. Topic titles/counts now use separate rows and natural word
wrapping; classification IDs, purposes and call captions have distinct type sizes.
The tablet classification list is bounded above the detail sheet, so larger
captions remain reachable. Classification controls/content use the existing 4px
radius family; the mobile sheet retains its documented 8px overlay exception.
No new images, dependencies, navigation, data model or workflow were introduced.
See [current refinement evidence](../tests/website/evidence/taste/README.md) for
verification and preflight applicability/limits. This is the current local candidate;
owner acceptance and publication remain separate.

### Authorized publication preflight

The owner accepted T12 and authorized T13 on 2026-10-28. Before changing public
serving, the provider's `.html` to clean-URL redirects exposed a navigation-path
compatibility defect. Known `/zh`, `/index`, `/explore/zh` and `/explore/index`
aliases now resolve to the existing page families; arbitrary unknown paths do not.
This repair preserves content and interactions but changes runtime identity, so
targeted owner confirmation remains pending under the task record's changed-byte
gate. The isolated local archive is prepared; version 7 remains serving and no
new version/source push/deployment was performed. See the
[publication preflight record](../tests/website/evidence/release/README.md).
