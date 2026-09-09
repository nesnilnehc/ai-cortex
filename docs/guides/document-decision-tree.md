---
artifact_type: guide
created_by: ai-cortex
lifecycle: living
created_at: 2026-05-09
status: active
---

# Deciding whether to create a document

> Should you create a new markdown document at all, and where does it go? This guide answers with a decision tree.
>
> Companion: the list of constraints is in [rules/workflow-documentation.md](../../rules/workflow-documentation.md).

---

## The decision tree

Ask yourself these 4 questions before creating any new `.md`:

1. **Does it need ongoing maintenance?**
   - Yes → go to question 2
   - No → create nothing; use a commit message, a PR description, an issue comment or a scratch note

2. **Is there already an authoritative document on this topic?**
   - Yes → create nothing; update the existing document, or add a link to it
   - No → go to question 3

3. **Will ≥ 3 users or agents consume it?**
   - Yes → go to question 4
   - No → consider a wiki page, an internal note or a pinned Slack message instead

4. **What is its lifecycle?**
   - Long-lived (living) → create it in a formal directory such as `docs/architecture/` or `docs/guides/`, with complete frontmatter
   - Short-lived (snapshot) → it must be named `*.draft.md` or `YYYY-MM-DD-topic.md`, kept in a dedicated directory — `docs/design/`, `experiments/` or `meetings/` — with a date set for clearing it out

---

## Paths at a glance

| What it is | Where it goes |
|----|----|
| An architecture decision record | `docs/adr/NNNN-{topic}.md` |
| A functional design document | `docs/designs/YYYY-MM-DD-{slug}-functional-design.md` |
| A technical design document | `docs/designs/YYYY-MM-DD-{slug}-technical-design.md` |
| A long-lived usage guide | `docs/guides/{slug}.md` |
| Reference material | `docs/references/{slug}.md` |
| A draft, not yet settled | `<final location>.draft.md` |
| Notes from an ad hoc discussion | A dedicated directory such as `experiments/` or `meetings/` |

---

## Anti-patterns

- ❌ Creating a summary document with no defined lifecycle, such as `SUMMARY.md`, `COMPLETE_REFACTOR.md` or `REVIEW_2024.md`
- ❌ Copying the same installation steps into several READMEs; there is one authoritative copy, and everything else links to it
- ❌ Putting an ad hoc discussion at the top level of `docs/`, which pollutes the formal documentation
- ❌ Writing a version change record into a new document; it belongs in CHANGELOG.md

---

## Related

- The list of constraints: [rules/workflow-documentation.md](../../rules/workflow-documentation.md)
- Naming and paths for document artifacts: [docs/architecture/terminology.md](../architecture/terminology.md)
