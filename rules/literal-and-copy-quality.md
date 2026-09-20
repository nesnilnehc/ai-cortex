---
artifact_type: rule
name: literal-and-copy-quality
version: 1.1.0
model: RULE_MODEL_V1
rule_prefix: LIT
scope: code that produces text a person sees, or that carries a value read by more than one runtime
recommended_scope: project
status: active
created_by: ai-cortex
lifecycle: living
created_at: 2026-09-20
---

# Rule: Literal and Copy Quality

## Scope

Applies to a change that produces text a person sees, or that introduces a value read by more than one runtime — an address, a storage key, an identifier, a product name, a quota limit.

The defects this set covers share one shape: **nothing fails**. The code compiles, the existing tests stay green, no error is logged, and the product goes on serving a screen that contradicts itself — one record showing two different times, a link that resolves on one platform and not another. Only a reader notices, and usually a reader who has already lost a little trust by the time they do.

Three neighbouring concerns are owned elsewhere, and a finding belongs to them rather than here:

- **Whether a message tells the person what to do** belongs to [error-surfacing-quality](./error-surfacing-quality.md). The boundary: how the words are assembled is decided here, whether they are the right words to act on is decided there. A system-supplied diagnostic concatenated into localized copy is a defect here under LIT-003; it is additionally a defect there only when the resulting message also fails to say what to do next.
- **Internal logging and diagnostic strings never shown to a person** belong to the observability quality criteria.
- **Where a value should be defined, decided before the code is written** belongs to `TDES-028` in [technical-design-quality](./technical-design-quality.md). That item is this set's design-time counterpart: it asks the design to name each value's single defining place, and this set checks afterwards that no second copy appeared.

## Profiles and parameters

| Name | Kind | Provenance | Meaning |
| --- | --- | --- | --- |
| `multi-runtime` | profile | — | The product is implemented by more than one runtime — a web client and a native client, or several services |
| `multi-locale` | profile | — | The product supports more than one language |
| `static-page` | profile | — | A page carries text it fills in at run time rather than through a template engine |

Provenance follows [rule-modeling](../specs/rule-modeling.md) §5.4: a project writes only the `declared` values.

## Rules

### LIT-001 — A value more than one runtime reads has one defining place

| Field | Value |
| --- | --- |
| Level | `profile:multi-runtime` |
| Requirement | An address, storage key, identifier, product name, quota limit or any other value read by more than one runtime **MUST** be defined once in a shared contract and read by each runtime, rather than copied into each. |
| Applies when | The change introduces or edits a value that more than one runtime reads. |
| Default severity | `major` |
| Enforcement | `tool-assisted` |
| Evidence | A search of product source for each shared value's literal; every hit is the contract, a point that consumes it, or a fallback copy recorded under LIT-005. |
| Pass condition | Every hit outside the contract is a consumption point or a recorded fallback copy, and a reader confirms that none is an unrecorded second definition. |
| Not applicable when | The value is read by one runtime only and appears in no outward-facing material. |
| Remediation | Move the value into the contract and have each runtime read it. Where a runtime cannot read the contract, record the copy as a fallback and add a check that reconciles it. |
| Tool limits | A repository search enumerates every occurrence of a literal and where it sits. It cannot decide whether an occurrence is a consumption point, a recorded fallback or a second definition, and it cannot find a copy spelled differently — a second string that means the same value. A reviewer classifies the hits. |

### LIT-002 — A displayed format comes from a formatting API, not from cutting a string

| Field | Value |
| --- | --- |
| Level | `baseline` |
| Requirement | A time, date, ordinal, currency amount or percentage shown to a person **MUST NOT** be produced by indexing into a serialized string, by hand-padding or by prefix concatenation; it **MUST** come from the runtime's localized formatting API. |
| Applies when | The change writes code that renders one of those values to a person. |
| Default severity | `major` |
| Enforcement | `tool-assisted` |
| Evidence | A search of the display layer for substring slicing of serialized values and for hand-rolled padding. |
| Pass condition | No hit slices a serialized value for display, and a reader confirms each remaining hit is not on a display path. |
| Not applicable when | The value is not shown to a person. |
| Remediation | Replace with the localized formatting API. A deliberately fixed format **MUST** pin its locale and state in a comment why it is fixed. |
| Tool limits | A linter or AST search finds substring slicing of serialized values and hand-rolled padding. It cannot decide whether the sliced value reaches a person or stays internal, and it does not follow into a helper that formats on the item's behalf. A reviewer decides which hits are display paths. |

### LIT-003 — A copy entry is a whole sentence, not a fragment awaiting concatenation

| Field | Value |
| --- | --- |
| Level | `profile:multi-locale` |
| Requirement | Each entry in a copy table **MUST** stand on its own as a sentence or phrase, with variables expressed as named placeholders, and code **MUST NOT** join two entries, or an entry and a number, into one sentence. |
| Applies when | The change adds or edits a copy entry, or code that reads one. |
| Default severity | `major` |
| Enforcement | `tool-assisted` |
| Evidence | A search for copy lookups taking part in string concatenation, and for entries ending in a colon or a trailing space. |
| Pass condition | No copy lookup's return value is concatenated into a sentence, and a reader confirms that entries carrying trailing punctuation are not fragments. |
| Not applicable when | Neither side of the join is natural language. |
| Remediation | Merge into one entry carrying a named placeholder. |
| Tool limits | A search finds copy lookups taking part in concatenation and entries ending in a colon or space. It cannot decide whether the joined pieces are natural language — a number joined to a slash is legitimate — so a reviewer reads each join. |

### LIT-004 — Every visible string covers all supported languages

| Field | Value |
| --- | --- |
| Level | `profile:multi-locale` |
| Requirement | Copy tables, a static page's per-language blocks, and each platform's manifest and bundle resources **MUST** each cover every language the product declares. |
| Applies when | The change adds a visible string, or adds a supported language. |
| Default severity | `major` |
| Enforcement | `tool-assisted` |
| Evidence | A key-by-key comparison of each copy table, per-language block and platform manifest against the declared language set. |
| Pass condition | No gap, or a gap recorded as an intentional fall-through with its reason. |
| Not applicable when | The product supports one language. |
| Remediation | Fill the gap, or record the waiver. |
| Tool limits | A key-by-key comparison decides that a key is absent from a table, block or manifest. It cannot decide whether the gap is an intended fall-through, nor whether a value that is present is written in the language it claims. A reviewer settles both. |

### LIT-005 — A fallback copy agrees with its defining source

| Field | Value |
| --- | --- |
| Level | `profile:static-page` |
| Requirement | Seed text and addresses placed in static markup for the case where scripting has not yet run **MUST** equal the current value in the copy table or contract, and **MUST** be in the language that page declares. |
| Applies when | The change edits static markup carrying seed values. |
| Default severity | `minor` |
| Enforcement | `tool-assisted` |
| Evidence | A value-by-value comparison of each seed against its defining source, and of the page's declared language against the seed's language. |
| Pass condition | Each seed equals its source and matches the page's declared language. |
| Not applicable when | The page injects every value at build time. |
| Remediation | Synchronise the seed, or move it to build-time injection. |
| Tool limits | A value comparison decides that a seed and its source differ. It cannot decide which of the two is authoritative when both are plausible, nor whether a seed differs deliberately. A reviewer decides the direction of the fix. |

### LIT-006 — A value that expires is not written into the display layer

| Field | Value |
| --- | --- |
| Level | `baseline` |
| Requirement | A copyright year, a reference to "this year", a version number or a build time **MUST** be computed at run time or injected at build time rather than written into the display layer. |
| Applies when | The change writes a time-varying value into the display layer. |
| Default severity | `minor` |
| Enforcement | `tool-assisted` |
| Evidence | A search of the display layer for four-digit year literals and version strings. |
| Pass condition | No hit in the display layer is a value that changes with time. |
| Not applicable when | The value is a fixed historical date, such as a founding year. |
| Remediation | Compute at run time, or inject at build time. |
| Tool limits | A search finds four-digit year literals and version strings in the display layer. It cannot distinguish a fixed historical date, such as a founding year, from a stale reference to the current one. A reviewer reads each hit. |

### LIT-007 — A natural-language word used as a machine value is declared and bounded

| Field | Value |
| --- | --- |
| Level | `profile:multi-runtime` |
| Requirement | Where a contract uses a natural-language word as an enum value, the contract **MUST** state that these values are identifiers rather than display text and are not to be translated, and a check **MUST** bound the accepted set. |
| Applies when | A contract's enum values contain natural-language words. |
| Default severity | `major` |
| Enforcement | `judgment` |
| Evidence | The contract's declaration, the bounding check, and how each runtime consumes the value. |
| Pass condition | The declaration exists, the bounding check exists, and every runtime compares by equality rather than translating. |
| Not applicable when | No enum value contains a natural-language word. |
| Remediation | Add the declaration and the bounding check. Renaming is **not** recommended once the value has entered user data through a sync protocol, since the cost of the migration exceeds the benefit of the better name. |

## Severity and gate policy

A defect a reader would recognise as wrong on the screen is `major`: a second defining place for a shared value, a display format cut out of a serialized string, a sentence assembled from copy fragments, a language left uncovered, and an undeclared natural-language enum.

Presentation and staleness defects are `minor`: a fallback copy that has drifted from its source, and a time-varying value written into the display layer.

**No item in this set blocks a merge.** Every item is `tool-assisted` or `judgment`, which is a deliberate reduction from the enforcement the originating proposal asked for. [workflow-rule-governance](./workflow-rule-governance.md) §8 admits an `automated` blocking item only after it has been forward-tested against three representative shapes of the population it governs; the evidence behind this set is one project carrying three runtimes and four kinds of page, which its own authors said was not three independent projects. Raising any item to `automated` requires that evidence from adopting projects, collected rather than manufactured here.

## Waivers

A waiver may accept a fallback copy that cannot read its defining source, when the copy is recorded and a check reconciles it. It **MUST NOT** be used to accept a second defining place for a shared value with no reconciliation, since that is the condition every other item in this set exists to detect.

## References

- [Rule Modeling Schema](../specs/rule-modeling.md)
- [Findings List Schema](../specs/findings-list.md)
- [Technical Design Quality](./technical-design-quality.md) — `TDES-028`, the design-time counterpart
- [Error Surfacing Quality](./error-surfacing-quality.md)
- [Rule Governance](./workflow-rule-governance.md)
