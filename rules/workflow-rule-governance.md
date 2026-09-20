---
artifact_type: rule
name: workflow-rule-governance
version: 2.0.0
scope: modeled engineering Rule documents, profiles, project parameters and waivers
recommended_scope: user
status: active
created_by: ai-cortex
lifecycle: living
created_at: 2026-09-11
---

# Rule: Rule Governance

## Scope

These constraints apply to Rule documents declaring conformance to [RULE_MODEL_V1](../specs/rule-modeling.md), and to the profiles, project parameters and waivers that select them.

### When a Rule set should adopt the model

Adopt it when the set's items have to be **addressed from outside the document**:

- an item may need a waiver, so it must be nameable and its suppression must expire;
- a review must distinguish an item that passed from one that was never evaluated;
- another artifact — a task, a design, an audit record — cites the item.

Keep a checklist form when none of those hold. A criterion that a person reads while writing a document, fixes on the spot and never waives gains nothing from an identifier, and the schema it would carry is pure cost.

Recent editing activity is **not** a trigger. Whether a document was revised says nothing about whether anything needs to address its items, and treating revision as the trigger drags checklist-shaped criteria into a machinery that has nothing to bite on.

## Constraints

1. A Rule item must have one stable ID and one independently violable obligation. IDs are never reused.
2. A Rule item must state applicability, evidence, a pass condition, default severity, enforcement strength, non-applicability and remediation.
3. A baseline item must not be disabled by profile selection or a project parameter. Only a valid waiver can suppress it for a narrower scope.
4. A profile or project item is mandatory when its declared condition holds. “Context-specific” must not be interpreted as “optional”.
5. A project must customize policy through profiles and parameters; it must not copy a canonical Rule file and edit the copy.
6. A waiver must identify the exact versioned Rule item, narrow scope, reason, owner, approver, creation date, expiry, compensating controls and evidence. An invalid or expired waiver has no effect.
7. A breaking semantic change to an existing item requires a major Rule-set version. A retired ID remains recorded and must not acquire a new meaning.
8. Activation evidence scales with enforcement strength, and must be produced rather than asserted. What an item owes is decided by its `Enforcement`, never by its severity: severity says what a defect costs once established, and says nothing about whether the criterion that found it is sound.
   - An `automated` item must be forward-tested against at least three representative shapes of the population its own Rule set governs. For a Rule set governing code that is a single-package library, a layered application and a distributed service; for one governing an artifact it is a minimal conforming document, a defective one, and one whose conditional profiles are triggered. Record hits, misses, false positives and required parameters, and name where that record lives in the item's `Verification` row.
   - A `tool-assisted` item is not fully decidable and is not fixture-tested. It owes the tool class that supplies its decidable evidence and, in its `Tool limits` row, what that class cannot decide, so that a clean tool run is never read as a passed item.
   - A `judgment` item cannot be decided by a fixture, and authored prose must not be presented as a test of it. It owes an authoritative source anchor, a stated evidence contract, a binary or explicitly bounded pass condition, and one worked pass and one worked failure in its `Worked pass` and `Worked failure` rows. The source anchor may be an approved ADR, architecture decision or incident record of the adopting organization; §13 governs it only where the obligation derives from a book. Its empirical calibration is collected from adopting projects; this repository must not manufacture it.
   - Where the producing repository structurally cannot host the population an item governs, its `Verification` row reads `adopter`. That is a located responsibility, not a waiver: the adopting project owes the same three shapes, in the same record format, returned to this repository. An item left at `adopter` with no return path is the bad pattern below, merely renamed.
   - **Maturity is derived from those rows, never declared.** An item whose owed rows are all present is `ready`; otherwise it is `provisional`. A `provisional` item is not suppressed — it reports findings as usual, and its maturity travels with each finding per [findings-list](../specs/findings-list.md) §5.1, so a reader sees how well prepared the criterion is. Suppressing it would hide information rather than qualify it, and demoting its severity to express the same doubt would corrupt the one field that states consequence.
   - This constraint says nothing about blocking. Nothing in this repository blocks a merge on a Rule item: the review Skills emit a findings list a person reads. A term naming a mechanism that does not exist cannot decide which items an obligation reaches, which is why activation is keyed on enforcement alone.
9. A reported false positive is a Rule defect until shown otherwise. Where one item accounts for a disproportionate share of findings across adopting projects, narrow its applicability, sharpen its pass condition or lower its default severity — do not leave the criterion unchanged and absorb the noise. A zero-false-positive claim means nothing without the number of reviews it was measured over.
10. Automated enforcement may strengthen a Rule item's evidence, but a tool result must not claim coverage beyond the checks the tool actually performs.
11. The same criterion must not be restated in a Skill, project entry file or memory. Those assets cite the canonical Rule ID.
12. A classic book may motivate or explain a Rule, but it must not be the sole pass condition. Volatile technical claims require a current standard or authoritative implementation source, and language-specific guidance must remain in a matching profile or Skill rather than becoming a cross-language baseline.
13. When a new or broadened Rule obligation materially derives from a book, its reference must record the edition and a verified chapter, section or item locator. A title-only citation is contextual background and cannot justify a blocking semantic change.

## Bad patterns

- “Architecture quality must be high” without a checkable item.
- A project-local fork named `architecture-quality-custom.md`.
- A permanent waiver saying only “legacy code”.
- Raising severity from `minor` to `major` in a patch release.
- Treating zero findings from a static analyzer as proof that judgment-based items passed.
- Activating a new blocking rule after testing it only against this repository's Markdown assets.
- Presenting examples written by the Rule's own author as forward-test evidence for a judgment item.
- Requiring evidence that the producing repository structurally cannot generate, leaving the constraint permanently unmet.
- A `Verification` row reading `adopter` with no named return path, which relocates the obligation without discharging it.
- A hand-written maturity, or a severity lowered to express doubt about a criterion rather than the cost of the defect.
- Raising a finding because a named book or pattern recommends an approach, without a canonical Rule ID, applicability decision and concrete project evidence.
- Listing a shelf of classic titles with no mapping from content anchors to the Rule IDs they inform.

## Remediation

- Split compound statements and assign stable IDs.
- Move local topology and thresholds into `.ai-cortex/config.yaml`.
- Replace silent suppressions with bounded waiver objects.
- Preserve old meaning through SemVer or retire the old ID and add a new one.
- Derive maturity from the activation rows rather than declaring it; record where an existing forward test lives instead of leaving an item provisional by omission.
- Validate a deterministic change against three representative shapes of the population it governs before activation; for a judgment item, supply the source anchor, evidence contract, bounded pass condition and worked pass/fail examples instead.
- Map durable source ideas to the narrowest Rule IDs, then verify time-sensitive details against current authoritative material.
- Add edition-specific content anchors for book-derived obligations; keep title-only citations as further reading.

## Related assets

- Data contract: [rule-modeling](../specs/rule-modeling.md)
- Architecture decision: [ADR 0012](../docs/adr/0012-adopt-profiled-engineering-rules.md)
- Source map: [Classic software engineering sources](../docs/references/software-engineering-classics.md)
