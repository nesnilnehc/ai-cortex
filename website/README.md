# AI Cortex promotional website

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

Sites version 5 is public at [the custom domain](https://ai-cortex.nesnilnehc.top/)
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
