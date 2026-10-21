# Paired English and Simplified Chinese outputs

These fictional complete outputs exercise the same source facts, IDs, dates,
canonical states, memberships, revision and split layout in two languages. The
[source records](sources.md) are authoritative; input JSON is a rendering projection.

| Edition | Input | Main | Delivery | History | Timeline |
| --- | --- | --- | --- | --- | --- |
| English | [JSON](en/input.json) | [Roadmap](en/roadmap.md) | [Detail](en/roadmap-delivery.md) | [History](en/roadmap-history.md) | [SVG](en/roadmap.svg), [Mermaid](en/roadmap.mmd) |
| Simplified Chinese | [JSON](zh-CN/input.json) | [Roadmap](zh-CN/roadmap.md) | [Detail](zh-CN/roadmap-delivery.md) | [History](zh-CN/roadmap-history.md) | [SVG](zh-CN/roadmap.svg), [Mermaid](zh-CN/roadmap.mmd) |

Generate either input with the bundled renderer and `--output-dir` pointing to its
edition directory; use `--overwrite` only for the existing generated files. Both
inputs are schema 1.5. The Chinese free text was prepared explicitly; the renderer
only localizes its own headings, table headers, enums, legends and descriptions.
This example does not require consumers to maintain two editions.

Read the [language workflow](../deliverable-language.md) for automatic selection,
focused questions and retention. Tests reproduce every generated file and compare
machine facts across the two editions; prose equivalence also requires review.
