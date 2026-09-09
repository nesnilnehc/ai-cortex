---
artifact_type: naming-convention
created_by: ai-cortex
lifecycle: living
created_at: 2026-05-09
status: active
---

# Asset naming convention

> Naming conventions for the 4 asset types: Spec / Protocol / Skill / Rule. Required reading before adding an asset.
>
> Type boundaries and how to tell them apart are in [terminology.md](terminology.md).

---

## I. General rules, shared by all 4 types

1. **kebab-case**: all lower case, words joined by a hyphen `-`
2. **The path matches the frontmatter `name`**: `skills/foo-bar/SKILL.md` carries `name: foo-bar`
3. **English; pinyin and Chinese are forbidden**: machine-consumed fields stay English so tools can work together
4. **No consecutive hyphens**: `foo--bar` is forbidden; `foo-bar` is fine
5. **Never starts or ends with `-`**

---

## II. Spec

What it is: it defines a thing's own structural and behavioural contract (see [terminology.md §I](terminology.md#i-the-four-concepts)).

**Formula**: **the head word is the noun being defined** (noun-first)

- `<thing-being-specified>`
- Examples: `universal-notification`, defining the notification object; `requirement-modeling`, defining the structure of a requirement document

**Counter-examples**:

- ❌ `define-notification` — a leading verb is Skill style
- ❌ `notification-protocol` — "protocol" names the Protocol type, which confuses the two

---

## III. Protocol

What it is: it defines how several entities interact — the steps, the states, the message sequence.

**Formula**: **subject + action**, saying who is doing what with whom

- `<actor-or-domain>-<action>`
- Example: `im-notification-delivery` — the IM channel, plus delivering a notification

**Counter-examples**:

- ❌ `notification` — a bare noun, which is Spec style
- ❌ `delivery-protocol` — adding "protocol" to a Protocol name is redundant

---

## IV. Skill

What it is: a capability a single agent can invoke — objective, execution, examples. It follows the [agentskills.io](https://agentskills.io) standard.

**Formula**: **verb-noun**

- `<verb>-<noun>`
- Examples: `commit-work`, `generate-readme`, `review-typescript`, `define-mission`

### 4.1 The review family

```text
review-<language>            e.g. review-python, review-typescript
review-<framework>           e.g. review-react, review-vue
review-<domain>-usage        e.g. review-orm-usage
review-<concern>             e.g. review-security, review-performance, review-architecture, review-testing
```

### 4.2 The define family

```text
define-<noun>                e.g. define-mission, define-roadmap, define-vision
```

### 4.3 Other common verb prefixes

```text
generate-<noun>              e.g. generate-standard-readme, generate-github-workflow
orchestrate-<noun>           an orchestrator skill must carry the orchestrate- prefix (see §IV orchestrator vs atomic vs meta)
archive-<noun>               e.g. archive-milestone
capture-<noun>               e.g. capture-work-items
prioritize-<noun>            e.g. prioritize-backlog
promote-<noun>               e.g. promote-roadmap-items
deliver-<noun>               e.g. deliver-feature
integrate-<noun>             e.g. integrate-branches
refine-<noun>                e.g. refine-skill-design
plan-<noun>                  e.g. plan-next
automate-<noun>              e.g. automate-tests
commit-<noun>                e.g. commit-work
decontextualize-<noun>       e.g. decontextualize-text
```

### 4.4 Counter-examples

- ❌ `code-review` — noun-verb, the wrong way round; it should be `orchestrate-code-review`
- ❌ `documentation` — a bare noun, with no action visible
- ❌ `ts-review` — an opaque abbreviation

---

## V. Rule

What it is: a single checkable constraint.

**Formula**: **prefix + the thing constrained**

```text
standards-<technology-or-domain>     technical standards: coding, shell, imports and the like
workflow-<concern>                   workflow constraints: documentation, document lifecycle and the like
documentation-<aspect>               constraints on documentation output, such as markdown formatting
tools-<tool-or-action>               constraints on tool use, such as list-dir behaviour
writing-<style-or-language>          writing-style constraints, such as Chinese technical writing
```

### Existing Rule names

```text
standards-coding              general coding principles
standards-shell               shell script standards
standards-import              import management
workflow-document-lifecycle   the governance document lifecycle
workflow-documentation        documentation management policy
documentation-markdown-format markdown formatting
tools-list-dir-dotfiles       directory listing tool behaviour
writing-chinese-technical     Chinese technical writing
requirement-quality           the requirement quality review checklist (no standard prefix, noun-led; use this only when no prefix fits)
```

### Counter-examples

- ❌ `coding` — no prefix, so the class of constraint is unclear
- ❌ `markdown-rule` — a "rule" suffix is redundant

---

## VI. Checklist before adding an asset

- [ ] The type is settled — Spec / Protocol / Skill / Rule — using the 4 cross-checks in [terminology.md](terminology.md)
- [ ] The name follows the general rules: kebab-case, English, matching the directory
- [ ] The name follows the formula for its type
- [ ] No name collision among assets of the same type
- [ ] The name is not that of a retired asset

---

## VII. Related documents

- [terminology.md](terminology.md) — the definitions of the 4 asset types and how to tell them apart
- [agentskills.io](https://agentskills.io) — the standard Skill format, the external authority
- [CONTRIBUTING.md](../../CONTRIBUTING.md) — the contribution process
