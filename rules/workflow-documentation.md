---
artifact_type: rule
name: workflow-documentation
version: 1.0.0
scope: 所有新建或维护 .md 文档
recommended_scope: user
status: active
---

# Rule: Documentation Management

## Scope

Every act of creating, naming or maintaining a Markdown document (`.md`), covering both product documentation (SKILL.md / agent.yaml / README / specs / body `*.md`) and temporary documents (design drafts, retrospectives, audit snapshots).

---

## Constraints

1. **Minimise**: do not create a document to record a thinking process. Product documentation carries neither discussion history nor traces of version evolution — see "Identifying a temporary document" below.
2. **DRY**: do not repeat the same content across documents. A topic must have exactly one authoritative document; everywhere else links to it.
3. **Reader-oriented**: write only usage documentation that solves a real problem. Do not write process-oriented records of your own thinking.
4. **A temporary document must be labelled as one**: any document meeting a condition below must carry a date prefix or a `.draft` suffix in its filename, and live in a dedicated directory such as `docs/designs/`, `experiments/` or `meetings/`.
5. **Change records go where they belong**: version changes into `CHANGELOG.md`, improvement notes into an issue or PR. Do not open a new document for them.

---

## Identifying a temporary document (any one of these)

### By filename

- Contains a purely summarising word such as `SUMMARY` / `COMPLETE` / `FINAL` / `REVIEW` / `NOTES` / `UPDATES` / `OPTIMIZATION`
- A process record that neither starts with `YYYY-MM-DD-` nor ends in `.draft.md`

### By body

These patterns match Chinese-language document bodies, the repository's historical corpus. English documents need the equivalent grep set — `since v1.3` / `removed in` / `deprecated` / `TBD` / `as mentioned above` / `we decided` / `I recommend` — which is not yet enumerated here.

- **Version-evolution narration**: `v\d+\.\d+ 起` / `v\d+\.\d+ 移除` / `v\d+\.\d+ 简化` / `v\d+\.\d+ 回撤` / `v\d+\.\d+ 引入`
- **Section-heading suffixes**: `（新增）` / `（已废弃）` / `（v\d.\d 简化）` / `（v\d.\d 重写）`
- **Process vocabulary**: `废弃` / `vaporware` / `待建` / `历史` / `原本` / `回撤` / `沿用历史` / `本次新增`

### By conversational residue (product documentation specifically)

Shorthand, references and first-person narration established between an author and a collaborator during a discussion. Once they leak into product documentation, a cold reader is left with nothing to go on. Three typical patterns:

- **Conversational shorthand** used as terminology without a canonical definition anywhere in the repository:
  - `\bL[0-9]+\b` — `L1` / `L2` / `L3`; a leak unless defined in this very document
  - `\b(方案|选项|Option)\s*[A-Z]\b` — `方案 A` / `Option B`, leftover option numbering from a discussion
  - Ad-hoc numbering `\b[TC]\d+\b` — `T1` / `C1`, unless it is a section heading in this document

- **Backward reference** to conversation history rather than document history:
  - `如上(所述|所说|提到|讨论)` / `刚才(提到|说过|讨论)` / `前面(说过|提到|讨论)`
  - `我们(之前|刚才|刚刚|前面)` / `基于(我们|刚才|之前的)讨论`

- **First-person narration** carrying the author's viewpoint into product documentation:
  - `我(建议|认为|觉得|推荐)` / `我们(决定|选择|采用|认为)`
  - `经(讨论|协商|沟通)后`

### Exceptions (not treated as temporary documents)

- The "change record" section at the top of a spec file — a local CHANGELOG, an accepted convention
- An ADR's own "context / decision / alternatives / consequences" narration — that is its genre
- The whole of `CHANGELOG.md`
- **The example fragments in this rule (`workflow-documentation.md`) that demonstrate the forbidden patterns** — a rule defining a no-go zone necessarily has to show those patterns as counter-examples, on the same reasoning as the blanket CHANGELOG exception

---

## Bad Patterns

- Creating `SUMMARY.md` / `COMPLETE_REFACTOR.md` / `REVIEW_2024.md`
- Copying the same install steps into several READMEs instead of linking
- Opening an "optimisation record" document for one refactor instead of writing it into the CHANGELOG or the commit
- A temporary document placed at the repository root or under the formal `docs/` path without a `.draft` suffix or a date prefix
- Version-evolution narration such as `v1.3 起 / 移除 / 简化` in the body of a SKILL.md or a spec

---

## Pre-commit self-check

Before staging any Markdown file, run these two steps:

### 1. The cold-reader test (mandatory)

Ask of each paragraph: **"could someone who joined the project today, and took part in no conversation, understand what I am saying from this text alone?"**

- Yes → it passes
- No → either define the term inside the document, or rewrite it into a self-explaining name (`L2 评审` → `用例集覆盖评审`)

The cold-reader test is not fully replaceable by grep — what it catches is the semantic gap where the author's context is not the reader's context.

### 2. Grep blacklist scan (the automated backstop)

Grep against the "Identifying a temporary document" list above — filename patterns, body patterns and conversational residue. On a hit, apply the "must be labelled" constraint:

- Filename or section heading hit → rename, or move to a dedicated directory
- Version-evolution narration → move it into an ADR or the CHANGELOG
- Conversational residue → replace with a self-explaining expression, or define the term in the document
- First-person narration → rewrite as a statement or an imperative

---

## Related guidance

- Deciding whether to create a document at all, and where to put it: [docs/guides/document-decision-tree.md](../docs/guides/document-decision-tree.md)
- Repository structure hygiene: [rules/repo-structure-hygiene.md](./repo-structure-hygiene.md)
- Document health criteria (link graph, SSOT, alignment): [rules/doc-health-criteria.md](./doc-health-criteria.md)
