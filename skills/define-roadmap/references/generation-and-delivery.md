# Roadmap generation and delivery

## Local generation

Use `python3 <skill-dir>/scripts/render-roadmap.py INPUT.json --check` to validate
temporary facts under the Spec, then pass `--output-dir DIR` and optionally
`--layout split` (legacy default `single`; schema 1.4 reuses its saved layout) for the selected local
destination. Use `--overwrite` only for confirmed replacement of reserved generated
filenames. Never overwrite authoritative evidence or treat the temporary JSON as
a second project plan. The generator emits Markdown and, when selected, SVG and
dated Mermaid; inspect the SVG in a local browser or image-capable viewer. If Python
is unavailable, prepare the same views manually and state that tool validation did
not run. No runtime dependency installation is permitted.

Read the [generator example](service-desk/initial/input.json). Preserve the user's
source links relative to the chosen output path; the generator does not relocate
project records. Copying a roadmap to a new directory requires rebasing relative links.

## Knowledge-base delivery

For a knowledge-base destination, discover available document read/write and image
upload tools, map them to the selected operation, read the latest target before
editing and preserve unrelated content. Verify Mermaid support with a small preview
before relying on it. Check disclosure-element support as well; if unavailable,
expand folded content or use authorized linked detail pages without hiding facts.
If native rendering is unavailable, use supported image upload
and retain source access. If upload/write is unavailable, report undelivered views
and the local output location; do not silently switch destination or claim publication.
External writes require the user's explicit destination/publication authorization.
This capability performs one delivery, never continuous or bidirectional sync.
