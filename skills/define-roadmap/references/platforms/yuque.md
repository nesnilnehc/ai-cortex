# Yuque adapter

Load only for Yuque. Apply the [remote delivery guide](../platform-delivery.md).
These mechanics belong in the adapter, not reader-facing plans or other platforms.

## Capabilities and preservation

- Discover the active connector by service and operation, not a fixed account/tool
  name. Inspect supported formats and full rich source. Lake-capable APIs may expose
  `body_lake` and `body_html` beside Markdown. Use rich source for card/anchor-sensitive
  pages; Markdown replacement may rebuild headings or lose cards. If rich writes
  are unavailable, use an authorized editor fallback or report the blocked part.
- Prefer metadata-only title changes. Preserve document IDs/slugs; read back titles
  and inspect the book directory. Titles live in metadata, without a duplicate
  body H1. Preserve the project's headings, fields and table column widths.
- Parse Lake metadata by attributes, not literal attribute order. Where project
  style requests adaptive width, preserve/set viewport meta `content=adapt` and
  inspect actual readability; metadata alone is not visual acceptance.
- Preserve structured card payloads, including image/diagram/embed identity and
  unrelated properties. Compare decoded payloads rather than percent-encoding or
  HTML attribute order. SVG image cards can reference an uploaded asset URL with
  original dimensions and a display ratio; inspect the resulting display.

## Anchors and references

Collect IDs from Lake and rendered HTML: legacy headings may expose IDs only in
the latter. Inventory published headings, known inbound fragments and explicit
compatibility aliases; internal generated block/text IDs are not public anchors
merely because they appear in HTML. Keep aliases at meaningful section positions.
An empty span stored by the API is not proof of a rendered anchor. One observed
Lake-compatible form is a paragraph-contained span with matching `id`/`data-lake-id`
and a zero-width character:
`<p><span id="legacy" data-lake-id="legacy">&#8203;</span></p>`.
Revalidate against the current editor, inspect reader DOM and follow the old fragment.
Do not strip compatibility nodes as clutter or promise every renderer retains them.

Ordinary stable links provide navigation. Treat embeds as live projections only
after isolated source-update/target-refresh tests. Observe target content and
update metadata separately; refresh-based visibility is not realtime push. Preserve
embed cards rather than copying text. Target Lake alone does not verify embedded
content; inspect the reader after refresh.

## Charts and fallback

Use existing valid probe evidence, or test Mermaid on authorized isolated pages
before relying on it, including a second rich-content
update retaining diagram and aliases. Inspect shapes, labels, dates, colors and
legend. An observed renderer accepted Mermaid while ignoring theme CSS; recheck
current behavior instead of turning that observation into a permanent prohibition.

If native output fails approved presentation, upload a generated SVG with an
available authorized attachment tool/editor, reuse a supported image card and retain
reproducible source in existing history/source records. Inline base64 SVG is not an
assumed fallback. If MCP lacks upload, state the limitation and use authorized UI
when available. Generation alone is not upload evidence. Verify loaded dimensions
and actual chart appearance. A source-only Mermaid card in history is not another
editable schedule. Unknown milestone dates remain unscheduled.

## Update acceptance

Compare read-back stable identities, URLs, anchors, card payloads and history.
Inspect section navigation, affected references, charts and tables in the reader.
Use conditional writes where available; otherwise compare a fresh read, reconcile
differences and disclose the residual race. Inspect partial/unknown outcomes before
retry. Store receipts outside reader prose. Every later update repeats these checks;
one passing receipt does not guarantee future preservation. A metadata-only change
may reuse unchanged rich-body/chart evidence after exact body equality and new
title/directory checks. Content/asset changes still require fresh affected checks.

## Captured Lake/HTML evidence encoding

The optional read-only checker uses this concrete encoding. It is not a project
plan, a universal platform schema or a live-service client.

| Record | Fields |
| --- | --- |
| Root | `baseline`, `readback`: nonempty arrays for the same existing page set; `contract`: acceptance assertions |
| Page snapshot | `id`, absolute stable `url`, display `title`, raw `lake`, `updated_at`; optional raw `html` for legacy heading anchors |
| Reader observation | `rendered_ids` for protected headings/fragments/aliases, `images` with observed `src` and positive integer `natural_width`, named boolean `visual_checks` |
| Per-page contract | `documents` entries with `id`, expected `title`, optional `protected_anchors`, `required_links`, `required_text`, `forbidden_text`, required named `visual_checks`; `inspection` defaults to `content`, or explicitly `metadata` for exact unchanged rich body |
| Preservation scope | `immutable_docs` names whole historical originals; `changed_cards` maps page IDs to only intended payload replacements, retaining card identity/type/attributes |

The checker protects heading IDs, explicit Lake aliases, declared anchors and
in-scope inbound fragments. It does not require every editor node ID to survive.
Metadata mode skips unaffected anchor/image observation requirements and requires
named title/directory visual checks. Unknown modes, duplicate IDs and missing
required links fail. `preflight` remains a read/compare guard, not an atomic lock.
