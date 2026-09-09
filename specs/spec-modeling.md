---
id: SPEC_MODELING_SPEC_V2
name: Spec Modeling Schema (Meta-Spec)
description: Meta-spec defining the structural contract that any spec document must follow — frontmatter contract, body section skeleton, and required/conditional/optional section taxonomy.
version: 2.0.1
status: active
lifecycle: living
created_at: 2026-05-21
scope: |
  Defines the structural contract for any spec document.
  Applies recursively to this file itself. Establishes the required / conditional /
  optional section taxonomy and frontmatter requirements that downstream specs inherit.
related:
  - ./adr-modeling.md
  - ./claude-md-modeling.md
  - ./functional-design-modeling.md
  - ./technical-design-modeling.md
  - ./requirement-modeling.md
  - ./task-modeling.md
  - ./universal-notification.md
---

# Spec Modeling Schema (Meta-Spec)

> **Data contract**: defines the structural skeleton and field constraints of any spec document

---

## 1. Position and scope

This is the spec of specs: every spec document, this file included, must follow the section skeleton and frontmatter contract defined here.

Each spec defines the data contract of one kind of artifact — its fields, sections, states and validation; this meta-spec defines how those specs themselves are organised.

In scope:

- Any spec document that describes an artifact's data contract

Out of scope:

- The companion rule (behavioural constraints)
- Protocols (process descriptions)
- The artifact itself (the object a spec describes, defined by that concrete spec)

The storage path is decided by each project's governance (this repository's `specs/` directory, another project's `docs/specs/`, and so on) and is outside this spec's constraints.

---

## 2. Mental model

> The core questions a sound artifact has to answer.

The artifact a spec describes usually has a handful of "core questions" — a sound artifact must hold up on each of them. Putting those questions up front in §2 lets both the spec author and the reader grasp the essentials and avoid drifting away from what matters.

| Artifact | Example core questions |
|---|---|
| ADR | What / Why / Alternatives / Consequences (4 questions) |
| CLAUDE.md | What / With / How / Don't (4 questions) |
| A spec itself | Its sections classified into three states by when each is to be written (required / conditionally required / optional) |

### 2.1 The mental model of a spec itself: the three states of a section

The defining dimension of a sound spec is "how each of its sections is classified by when it is to be written". The three states are the answer along that dimension, and every later section depends on this classification.

| Type | When the trigger holds | When the trigger does not hold |
|---|---|---|
| **Required** | Must be written (always, unconditionally) | — |
| **Conditionally required** | Must be written | **Must not be written** (writing it is redundant) |
| **Optional** | May be written | May be left out |

#### The distinctions that matter

- **Required vs conditionally required**: a required section has no trigger; a conditionally required one appears only when some characteristic holds
- **Conditionally required vs optional**: conditionally required is a binary switch — meet the condition and it must be written, miss it and it must not be; optional is the author's free judgement

### 2.2 Section classification and triggers at a glance

| Section | Type | Trigger (if any) |
|---|---|---|
| §1 Position and scope | Required | — |
| §2 Mental model | Conditionally required | The artifact has a distinct thinking framework (N core questions) |
| §3 Naming | Conditionally required | The artifact is written to disk and its filename follows a customary pattern |
| §4 Frontmatter contract | Conditionally required | The artifact is markdown and carries frontmatter |
| §5 Body structure contract | Required | — |
| §6 Anti-patterns | Required | — |
| §7 Examples | Required | — |
| §8 Relationship to other assets | Optional | — |

---

## 3. Naming

Each spec describes the **file naming rule** of the artifact it models, where one exists. It does not prescribe a storage path; the path is decided by each project's governance.

### 3.1 How a spec itself is named

- A document-modelling spec: `<artifact-name>-modeling.md` (for example `adr-modeling.md`)
- A runtime-object spec: `<concept>.md`, without the `-modeling` suffix (for example `universal-notification.md`)
- The meta-spec itself: `spec-modeling.md`

### 3.2 Deciding whether it applies

- The artifact is a single fixed file (such as `CLAUDE.md`) → §3 may be omitted, since the name is a constant
- The artifact is many files sharing a naming pattern (such as an ADR's `NNNN-{slug}.md`) → §3 is required
- The artifact is a runtime object with no file → §3 must not be written

---

## 4. Frontmatter contract

```yaml
---
id: <UPPER_SNAKE>_MODELING_SPEC_V<n>
name: <English Name>
description: <one-line summary in English>
version: <SemVer>
status: active | draft | superseded | archived
lifecycle: living
created_at: YYYY-MM-DD
scope: |
  <a multi-line statement of what the spec constrains and what it does not>
related:
  - <relative path to a related rule, spec or document>
# conditional fields (required by status)
superseded_by: <new-spec-id>      # required when status: superseded
archived_at: YYYY-MM-DD            # required when status: archived
---
```

### 4.1 Field table

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | string | Yes | Format `<UPPER_SNAKE>_MODELING_SPEC_V<n>` (for example `ADR_MODELING_SPEC_V1`); a runtime-object spec may drop `_MODELING_` (for example `UNIVERSAL_NOTIFICATION_SPEC_V2`) |
| `name` | string | Yes | The spec's English name |
| `description` | string | Yes | A one-line summary in English (≤ 200 characters) |
| `version` | string | Yes | The SemVer version |
| `status` | enum | Yes | `active` / `draft` / `superseded` / `archived` (semantics in §4.2) |
| `lifecycle` | enum | Yes | Fixed as `living`, since a spec keeps evolving |
| `created_at` | date | Yes | The date the spec was first published (`YYYY-MM-DD`) |
| `scope` | string | Yes | A multi-line statement of applicability; use `\|` rather than `>`, so line breaks survive |
| `related` | list[path] | Optional | A list of relative paths to related assets |
| `superseded_by` | string | Conditional | Required when `status: superseded`; points at the id of the replacing spec |
| `archived_at` | date | Conditional | Required when `status: archived` |

### 4.2 State machine semantics

The meaning of the 4 `status` values and the condition for entering each:

| Status | Meaning | Entry condition |
|---|---|---|
| `draft` | A first draft, not yet stable | The spec has just been written and nothing in production references it |
| `active` | Currently in force | The spec has stabilised and downstream assets reference it |
| `superseded` | Replaced by a newer spec | A newer spec has been published and taken over the responsibility |
| `archived` | Archived and no longer maintained | The artifact it describes has been retired, or the concept has been merged elsewhere |

**When to write this subsection**: it must be written when the artifact's state machine carries non-trivial meaning (≥3 states plus conditional fields). When status is just a simple marker — a binary `draft` / `published` with no further semantics — this subsection may be omitted, because the §4.1 field table already suffices.

---

## 5. Body structure contract

### 5.1 Section order

```markdown
# {Artifact} Modeling Schema

> **Data contract**: <one-line statement of position>

## 1. Position and scope            [required]
## 2. Mental model                  [conditionally required]
## 3. Naming                  [conditionally required]
## 4. Frontmatter contract          [conditionally required]
## 5. Body structure contract              [required]
## 6. Anti-patterns                    [required]
## 7. Examples                      [required]
## 8. Relationship to other assets            [optional]
```

### 5.2 Numbering rules

- **Uniform numeric headings**: every spec uses `## N. <name>`, never a topic-word heading
- **Skipping a number is allowed**: when a section does not apply, because a conditionally required section's trigger does not hold, skip that number and **do not renumber** — the numbering must stay aligned across specs
- **A uniform opening**: the H1 is followed immediately by a single-line blockquote, `> **Data contract**: <one-line statement of position>`; anything further belongs in §1, not in the blockquote

### 5.3 Validation kept in one place

Every validation rule for a **body structure** field or section is listed once, together, inside §5; scattering them after individual field definitions or into the §6 anti-patterns is not allowed.

Validation of §4 frontmatter fields — whether required, the type, the enum — naturally belongs to §4 and does not count as scattering.

§6 anti-patterns enumerate the concrete shapes of "violating a §4 or §5 validation rule"; they do not redefine the rule itself.

### 5.4 Examples kept in one place

Every example lives in §7; do not append an example after each field definition, so that §5 stays compact.

---

## 6. Anti-patterns

- ❌ Sections headed by a topic word instead of a number (`## Scope` rather than `## 1. Position and scope`)
- ❌ Forcing in a conditionally required section that does not apply (a runtime-object spec that adds §3 Naming or §4 Frontmatter contract)
- ❌ Validation rules scattered through individual field definitions (they belong together in §5)
- ❌ Examples scattered after individual field definitions (they belong together in §7)
- ❌ The anti-patterns section redefining validation rules (it lists violation shapes only; the rules live in §4 and §5)
- ❌ Frontmatter missing a required field such as `id` / `name` / `description` / `version`
- ❌ A `scope` field folded with `>` instead of preserved with `|` (the former swallows line breaks)
- ❌ Renumbering because one section does not apply (skip the number and keep the alignment)
- ❌ An opening blockquote with several paragraphs or extra explanation (it carries one line of positioning; everything else goes to §1)
- ❌ State machine semantics given a section of their own (they belong as a §4.x subsection of the Frontmatter contract)
- ❌ Writing the storage path into §3 (§3 governs naming only; the path is decided by project governance)
- ❌ A "change log" section in the body — a spec's version history is carried by git history plus the frontmatter `version`, and must not be repeated in the body
- ❌ A standalone "glossary" section — terminology is not a dimension of the artifact itself, so route each term by its nature:
  - A foundational concept or thinking framework that later sections depend on → write it into §2 Mental model
  - A term that serves only one field → embed it in that field's definition in §5, keeping it close to where it is used
  - Common industry terminology (Gherkin, the C4 model, IEEE 830 and the like) → link to an external glossary or reference

---

## 7. Examples

### 7.1 The minimal compliant skeleton (required sections only)

For a spec describing a runtime object, where the artifact itself has no frontmatter, no state machine, no naming pattern and no thinking framework — the spec document, of course, still has frontmatter of its own:

````markdown
---
id: WIDGET_SPEC_V1
name: Widget Schema
description: Spec defining the widget runtime object contract.
version: 1.0.0
status: active
lifecycle: living
created_at: 2026-05-21
scope: |
  Defines the structural contract for widget runtime objects passed between services.
---

# Widget Schema

> **Data contract**: defines the fields and validation of the widget runtime object

## 1. Position and scope
Applies to ...; does not apply to ...

## 5. Body structure contract
| Field | Type | Required | Description |
|---|---|---|---|
| ... | ... | ... | ... |

## 6. Anti-patterns
- ❌ ...

## 7. Examples
```json

{ "id": "...", "type": "..." }

```text
````

Note: §2, §3, §4 and §8 are skipped because they do not apply.

### 7.2 The full skeleton, with every conditionally required section

For a document spec — a markdown artifact with frontmatter, a state machine, a naming pattern and a thinking framework — such as an ADR:

```markdown
# ADR Modeling Schema

> **Data contract**: ...

## 1. Position and scope
## 2. Mental model               ← What/Why/Alternatives/Consequences
## 3. Naming               ← NNNN-{slug}.md
## 4. Frontmatter contract       ← artifact_type / status / superseded_by / ...
   ### 4.2 State machine semantics        ← proposed/accepted/superseded/archived/rejected
## 5. Body structure contract           ← 4 body sections: context / decision / alternatives / consequences
## 6. Anti-patterns
## 7. Examples
## 8. Relationship to other assets         ← the companion rule, the decay policy
```

---

## 8. Relationship to other assets

- **Applies recursively**: this file follows the skeleton this meta-spec defines, demonstrating it on itself
- **Downstream specs**: every spec inherits this one
- **Writing discipline**: general markdown writing discipline lives in each project's own documentation-management rule; this meta-spec has no separate rule of its own yet
