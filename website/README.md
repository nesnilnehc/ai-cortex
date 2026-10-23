# AI Cortex promotional website

A standalone, English-language static introduction to AI Cortex. Serve this
directory directly; there is no package installation or build step.

## Preview

From the repository root:

```bash
python3 -m http.server 4173 --bind 127.0.0.1 --directory website
```

Open [the local preview](http://127.0.0.1:4173). Stop the server with Ctrl+C.
Native navigation and disclosures work without JavaScript. The optional module
adds command copying and a System/Light/Dark theme selector. Preferences are
session-only and are not stored. With scripts disabled, theme follows the system.

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
node --test tests/website/copy.test.mjs
python3 tests/website/test_site.py
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

Sites version 1 is public at [the custom domain](https://ai-cortex.nesnilnehc.top/)
and [the hosted origin](https://ai-cortex.mystic-loon-2462.chatgpt.site).
The [hosting identity](.openai/hosting.json) and
[deployment record](.openai/deployment.json) retain the exact project, version,
source commit and domain status. Only the seven runtime files listed in that
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
