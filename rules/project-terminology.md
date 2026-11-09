---
artifact_type: rule
name: project-terminology
version: 0.1.0
scope: projects that adopt the project terminology model and identify an authoritative glossary
recommended_scope: project
status: draft
created_by: ai-cortex
lifecycle: living
created_at: 2026-11-09
---

# Rule: Project Terminology

## Scope

Apply to current project documents and code-facing names when the project has
adopted [Project Terminology Modeling](../specs/project-terminology-modeling.md)
and identified its authoritative glossary. Preserve quoted source text, public
API names, historical records, and external product names unless their owners
authorize a change. A project glossary does not override a concept-defining
Spec or an external publisher's definition.

## Constraints

1. **Use the accepted name in its scope.** For a concept with an accepted
   preferred term, use that term in new project prose for the matching language
   and context. Introduce an alternative only when it helps readers recognize
   an existing name. Check by comparing the use with the concept's scope and
   language in the authoritative glossary.
2. **Keep distinct meanings distinct.** When the same spelling refers to
   different concepts, identify the intended context or use a more precise
   name. Check that the referenced definition matches the actual meaning.
3. **Attribute external meaning.** When asserting what a vendor, standard, or
   other project means by a term, cite its defining source and applicable
   version where relevant. Mark any narrower or extended local usage as the
   adopting project's usage. Check the claim against the cited source.
4. **Do not promote uncertainty.** A proposed or source-unverified term must
   not be presented as an accepted definition. Check its record status and
   source before using it as an authority.
5. **Keep one editable authority.** Update the project's chosen glossary or
   concept-defining source; other current documents link or summarize it.
   Check for a competing editable definition before adding one.

## Self-Check

- Each changed use resolves to the intended concept, language, and scope.
- External claims resolve to a checked source; local meanings are labelled.
- No proposed meaning is presented as settled and no second authority was created.
