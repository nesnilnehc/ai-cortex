# Select and retain deliverable language

The [Roadmap Spec](../../../specs/roadmap-modeling.md#57-deliverable-language-schema-15)
owns the contract. This workflow applies it without another mandatory interview.

## Read first and ask only gaps

Read explicit artifact-language instructions, applicable project policy, the target
roadmap and comparable documents. Select in that order, then use consistent reader
and document evidence for new artifacts. For example, an English project policy
still applies during a Chinese conversation; an existing Chinese roadmap retains
Chinese when no higher-priority instruction changes it. English template headings
do not establish a consumer policy. A bilingual audience without a clear preference
needs a focused choice, such as “Which language should the roadmap use: English or
Simplified Chinese?” Offer the evidence-backed recommendation first when available.

Record locale, basis, rationale and source in the existing planning decision or
norms. Carry this into definition, capture, priority/dependency reports, promotion,
updates, review and archive summaries. Routine runs reuse it. Do not translate
historical originals or unrelated source documents. A new explicit instruction can
change it within the requested scope without repeated permission. Preserve one
revision identity for a material planning decision; a prose-only translation can
remain in version control unless project policy requires a revision.

## Optional offline helper

The helper accepts evidence already discovered by the skill, not a project path:

```json
{
  "language_context": {
    "project": [{"locale": "en", "source": "AGENTS.md#language"}],
    "documents": [{"locale": "zh-CN", "source": "docs/overview.md"}]
  }
}
```

```bash
python3 <skill-dir>/scripts/render-roadmap.py evidence.json --resolve-language
```

Here project policy wins. Same-level conflicts or no evidence return `needs-input`
and questions. A saved 1.5 choice without new evidence returns `retained`; a
higher-priority different choice returns `change-proposed`. The command prints
JSON and changes no files. It does not ask the user itself. Update the source
choice before rendering; generation blocks unresolved or differing context.
`--recommend` can return language advice alongside view advice, but language
questions do not reset an established scenario or layout.

## Prepare and verify an edition

For localized generation, use schema 1.5 with a saved `language` record, prepare
free-text fields in that language, validate with `--check`, and generate to the
established destination. Preserve source links relative to that destination.
The renderer supports `en` and `zh-CN`; other locales fail rather than falling back.
Its bundled catalog is read once per process from the script directory. A missing or
damaged catalog stops localized generation before writes and names the file to restore
from the same skill version; no runtime download or English fallback occurs.
Old schemas still render English. Without Python, follow the same contract manually
and disclose that generator checks did not run; install no dependency at runtime.

Check headings, table headers, status displays, summaries, chart labels, legends and
accessible descriptions across main and detail outputs. Review names, goals, reasons,
conditions and approval labels separately: the renderer intentionally does not
translate arbitrary project prose. Keep IDs, paths, URLs, machine fields, canonical
states and Mermaid syntax unchanged. Inspect source evidence before judging semantic
agreement; a successful render proves neither translation quality nor publication.

[Paired complete examples](languages/README.md) show the same fictional plan in both
languages, with sources, input, main/detail/history documents, SVG and dated Mermaid.
