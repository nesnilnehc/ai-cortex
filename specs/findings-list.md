---
id: FINDINGS_LIST_SPEC_V1
name: Findings List Schema
description: Spec defining the structure of a findings list — the artifact every evaluative skill emits, and the one an orchestrator aggregates. Covers the six elements of a finding, the severity enum, and the category convention.
version: 1.0.0
status: active
lifecycle: living
created_at: 2026-09-10
scope: |
  Applies to any skill declaring `output_schema.type: findings-list`, and to any
  orchestrator aggregating findings from several such skills. Defines the shape of a
  finding, not the criteria for raising one — those belong to each skill or to the
  rules/*-quality.md it cites.
related:
  - ./spec-modeling.md
  - ../rules/roadmap-quality.md
  - ../docs/adr/0001-io-contract-protocol.md
---

# Findings List

> **Data contract**: defines the elements, severity enum and category convention of a finding

---

## 1. Position and scope

A findings list is what an evaluative skill emits instead of a rewrite. [ADR 0001](../docs/adr/0001-io-contract-protocol.md) made `findings-list` one of the artifact types a skill may declare in `output_schema`, so an orchestrator can match an upstream output to a downstream input without reading either skill's body. This spec defines what that type *is*.

It exists because 16 review skills share one output format. Holding a copy of it in each skill guarantees the copies drift, and the drift is invisible until an orchestrator tries to aggregate two of them.

In scope:

- Any skill whose frontmatter declares `output_schema.type: findings-list`
- Any orchestrator aggregating findings across several skills

Out of scope:

- **The criteria for raising a finding.** What counts as a defect is each skill's own subject, or is cited from the `rules/*-quality.md` that owns it. This spec governs the shape a finding takes, never whether it should exist.
- **Severity assignment.** The enum is fixed here; which severity a given defect earns is a judgement the emitting skill makes.
- **How findings are rendered to a user.** A skill may present them as a table, a list or prose, as long as every element below is recoverable.

---

## 5. Body structure contract

### 5.1 The six elements

Every finding carries these. Location, category, severity, title and description are required; suggestion is optional.

| Element | Required | Content |
|---|---|---|
| **Location** | yes | `path/to/file.ext`, optionally with a line or range — `path/to/file.ext:42`, `path/to/file.ext:42-58`. For a document artifact, a section anchor is acceptable in place of a line. |
| **Category** | yes | The dimension this finding belongs to, per §5.3. One value, matching the emitting skill's declared category. |
| **Severity** | yes | `critical` / `major` / `minor` / `suggestion`, per §5.2. |
| **Title** | yes | A single line naming the defect. Not a restatement of the category. |
| **Description** | yes | 1-3 sentences: what is wrong, and what follows from it. |
| **Suggestion** | no | A concrete fix. Where the fix is not obvious, omitting this is better than padding it. |

### 5.2 Severity

| Value | Meaning |
|---|---|
| `critical` | Correctness, security or data loss. It must be fixed before the change ships. |
| `major` | A real defect that will cost something later — a broken contract, a missing error path, a regression risk. |
| `minor` | A defect with bounded cost — naming, a narrow edge case, a local inconsistency. |
| `suggestion` | An improvement, not a defect. Declining it leaves nothing broken. |

An orchestrator aggregating several skills sorts by severity first, so the values must mean the same thing in every skill that emits them.

### 5.3 Category

A category names the dimension a skill reviews, so an aggregated list stays readable when findings from a dozen skills sit together. It takes the form `<class>` or `<class>-<subject>`:

| Class | Subject | Example |
|---|---|---|
| `scope` | — | `scope`, for a skill bounded by a diff or a path set |
| `language` | the language | `language-python`, `language-go`, `language-sql` |
| `framework` | the framework | `framework-react`, `framework-vue` |
| `library` | the library or usage area | `library-orm` |
| `cognitive` | the concern | `cognitive-security`, `cognitive-performance`, `cognitive-architecture`, `cognitive-testing` |
| `<artifact>-quality` | — | `requirements-quality`, `roadmap-quality`, for a skill evaluating a governance document against a quality rule |

A skill declares its own category once, in its body, and every finding it emits carries that value. A skill must not invent a category outside this form.

### 5.4 Aggregation

Where an orchestrator merges lists from several skills, it:

- Keeps every finding's original category, so the emitting skill stays identifiable
- Sorts by severity, then by location
- Never rewrites a title or description, and never merges two findings into one

---

## 6. Anti-patterns

- ❌ A finding with no location, or a location naming only a file where a line is known
- ❌ A severity outside the four-value enum — `blocker`, `nit`, `info` and `warning` are not values here
- ❌ A category invented ad hoc, or a finding carrying several categories
- ❌ A title that restates the category (`Security issue`, `Performance problem`) rather than naming the defect
- ❌ A description that states the rule rather than what is wrong at this location
- ❌ A padded suggestion, offered because the field exists rather than because the fix is known
- ❌ A skill embedding its own copy of this contract instead of citing it — the copies drift, and the drift surfaces only when an orchestrator aggregates them
- ❌ Rewriting the artifact under review. A findings list reports; it does not fix

---

## 7. Examples

### 7.1 A single finding

```markdown
- **Location**: `utils/helpers.py:42`
- **Category**: language-python
- **Severity**: major
- **Title**: Mutable default argument
- **Description**: A list as a default argument is created once at definition, so state leaks between calls.
- **Suggestion**: Take `items=None` and initialise with `if items is None: items = []`.
```

### 7.2 A finding with no obvious fix

The suggestion is omitted rather than padded.

```markdown
- **Location**: `docs/process-management/roadmap.md#now`
- **Category**: roadmap-quality
- **Severity**: critical
- **Title**: Capacity allocation has no total baseline
- **Description**: The percentages per strategic goal are present, but the total capacity baseline they multiply is absent, so `promote-roadmap-items` cannot compute a capacity for any goal.
```

---

## 8. Relationship to other assets

- **The decision that created the type**: [ADR 0001](../docs/adr/0001-io-contract-protocol.md) — `findings-list` as a declarable `output_schema` type, so an orchestrator can route by type
- **The criteria side**: `rules/*-quality.md` — a skill evaluating a governance document cites the rule for *what* to raise; this spec fixes *how* to state it
- **Recursive basis**: this spec follows the [spec-modeling.md](./spec-modeling.md) skeleton, skipping §2, §3 and §4 — a findings list is a runtime object with no filename, no frontmatter and no state machine
