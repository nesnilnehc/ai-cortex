---
id: PROJECT_TERMINOLOGY_MODELING_SPEC_V1
name: Project Terminology Modeling Schema
description: Concept entries, source authority, and validation for reusable project terminology records.
version: 0.1.0
status: draft
lifecycle: living
created_at: 2026-11-09
scope: |
  Defines the minimum information a project terminology record carries, whether
  stored in Markdown, YAML, or an existing glossary. Does not prescribe a file
  location, translation process, or an organization's approval workflow.
related:
  - ../docs/architecture/terminology.md
  - ../rules/project-terminology.md
---

# Project Terminology Modeling Schema

> **Data contract**: defines one project-owned record per concept and the evidence needed to use its terms consistently.

## 1. Position and scope

Projects may have their own concepts and may also use terms defined by vendors,
standards, or other projects. A project glossary records how those concepts are
used in that project. It does not replace the source that defines an external
concept or duplicate a contract that already defines a project concept.

Adopting projects choose the authoritative glossary and storage format. Reuse an
existing glossary or concept-defining Spec before creating a new file. A glossary
may point to a concept's authoritative Spec instead of copying its full contract.
Existing documents are not required to migrate solely to adopt this model.
The project's agent entry or equivalent configuration identifies that glossary
and loads the companion project-scoped Rule when terminology is written or reviewed.
An ID-to-display-name dictionary, such as `plan-next`'s optional
`.ai-cortex/glossary.yaml`, can be used for output labels without becoming the
authority for domain concepts. Keep its established lookup contract intact.

## 2. Mental model

| Element | Meaning |
| --- | --- |
| Concept | A meaning within a stated context; the unit of one record. |
| Term | A name for a concept in a language or audience. Several terms may name one concept. |
| Preferred term | The name the project uses by default in that language and context. |
| Alternative term | A valid synonym, abbreviation, or search term that is not the default name. |
| Discouraged term | A name that readers may encounter but should not introduce into new project writing. |
| Source | The exact document, standard, product page, or project decision that supports a definition or local usage. |

One spelling may name distinct concepts in different contexts. A concept may
have several language-specific preferred terms. A project-specific interpretation
of an external concept must be marked as such; it must not be presented as the
external publisher's definition.

## 5. Body structure contract

### 5.1 Concept record

Projects may use headings, tables, YAML, or another existing representation.
The following logical fields must remain recoverable for each accepted concept.

| Field | Required | Meaning |
| --- | --- | --- |
| `concept_key` | Yes | Stable key or linkable heading unique within the glossary; do not recycle it for another meaning. |
| `scope` | Yes | Product, domain, bounded context, team, version, or other boundary in which the definition applies. |
| `definition` | Yes | Concise statement of what the concept means here, or a precise link to its authoritative definition. |
| `preferred_terms` | Yes | At least one term paired with its language; specify audience when audiences use different names. |
| `origin` | Yes | `project` or `external`; identify the defining organization or standard for an external concept. |
| `authority` | Yes | Source locator for the definition and, if different, the project's usage decision. Include a version or access date when the target can change. |
| `alternatives` | Conditional | Valid synonyms, abbreviations, and search names when they exist, with language and any ambiguity noted. |
| `discouraged` | Conditional | Names to avoid in new writing when a known competing name causes confusion; give the preferred replacement. |
| `local_usage` | Conditional | A project's narrower, extended, or translated usage when it differs from an external source. |
| `relations` | Optional | Links to broader, narrower, or related concepts when they clarify the meaning. |
| `status` | Optional | `proposed`, `accepted`, or `retired`; absence means accepted in a legacy glossary. A retired entry points to its replacement when one exists. |

### 5.2 Validation

1. A record identifies one concept; distinct meanings receive distinct keys and scopes, even when their names match.
2. Every accepted record resolves to a definition and an identifiable authority. A proposed term with incomplete evidence remains visibly proposed.
3. An external definition is attributed to its owner and source. `local_usage` identifies any project interpretation separately.
4. Within the same language and scope, two accepted concepts cannot silently claim the same preferred term. Either distinguish their contexts or record the ambiguity.
5. Alternatives and discouraged terms refer to the same concept as the preferred term; a genuinely different meaning is a separate record.
6. Existing authoritative Specs and vendor definitions remain authoritative for their own facts; a glossary reference does not override them.
7. A changed source is checked before its dependent record is updated. A broken or inaccessible source is marked for verification rather than treated as confirmation.

### 5.3 Interchange

The logical fields are independent of serialization. A project that exchanges
multilingual terminology with a termbase may map concept records to TBX. A
project that publishes a linked controlled vocabulary may map preferred,
alternative, and discouraged labels and concept relations to SKOS. Exporters
must document any fields they cannot round-trip; a Markdown glossary does not
claim TBX or SKOS conformance merely because its concepts resemble them.

## 6. Anti-patterns

- One row for the spelling "account" that conflates a customer, login, and billing account.
- A copied vendor definition with no product/version/source locator.
- A project's custom meaning presented as the vendor's own meaning.
- A second glossary created while an existing authoritative glossary remains current.
- A local abbreviation shown as universally accepted without its scope.
- A proposed AI-generated definition published as accepted without source checking.

## 7. Examples

The following is a small Markdown representation of the logical fields:

```markdown
### ai-cortex-skill

- Scope: AI Cortex asset types
- Definition: [Core terminology](../docs/architecture/terminology.md#skill)
- Preferred: English — Skill
- Alternatives: English — agent skill (when the asset type needs disambiguation)
- Origin: project
- Authority: [Core terminology](../docs/architecture/terminology.md#skill)
- Status: accepted
```

## 8. Relationship to other assets

This model borrows the concept-and-label distinction from [W3C SKOS](https://www.w3.org/TR/skos-reference/)
and the concept-oriented multilingual interchange purpose of [TBX](https://www.tbxinfo.net/developer-resources/).
AI Cortex's [core terminology](../docs/architecture/terminology.md) remains the
authority for its four asset types.
The [Project Terminology Rule](../rules/project-terminology.md) constrains how
adopting projects use accepted terminology in current work.
