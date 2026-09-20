---
artifact_type: adr
created_by: decision-record
lifecycle: snapshot
created_at: 2026-09-20
status: accepted
description: Key Rule activation on enforcement rather than an undefined blocking term, and carry a derived maturity on every finding instead of suppressing immature criteria.
---

# ADR 0014: Rule activation keys on enforcement, and maturity travels with the finding

## Context

[workflow-rule-governance](../../rules/workflow-rule-governance.md) §8 scaled its activation obligations by "blocking item". Nothing in this repository blocks a merge on a Rule item: the review Skills emit a findings list that a person reads, and `orchestrate-code-review` aggregates and sorts it. [findings-list](../../specs/findings-list.md) §5.2 defines only `critical` as "must be fixed before the change ships", while `major` is explicitly a cost paid later.

So the population §8 reached was undecidable — 11 items, 22 or 118 depending on the reader. That, rather than neglect, is why two of its three bullets had gone unmet since the constraint was written: nobody could say whom they applied to. The `automated` bullet was met for 16 items, because `scripts/test-rule-scenarios.py` names §8 directly and forward-tests against fixtures; the `tool-assisted` bullet was met for 1 item of 47, and the `judgment` bullet for 0 of 41.

## Decision

1. **Remove "blocking" from the governance model.** Each §8 bullet names its enforcement class directly. Severity states what a defect costs once established; it does not decide what evidence the criterion behind it owes.
2. **Give each class a row to carry its evidence**: `Verification` for `automated`, `Tool limits` for `tool-assisted`, `Worked pass` and `Worked failure` for `judgment`. The rows are conditional on `Enforcement`, so a missing one is a reported state rather than a validation error.
3. **Derive maturity, never declare it.** An item whose owed rows are all present and non-empty is `ready`; otherwise `provisional`. A hand-written `Maturity` row is rejected. The derivation is defined once, in [rule-modeling](../../specs/rule-modeling.md) §5.2.
4. **Carry maturity on the finding rather than suppressing it.** A `provisional` item reports findings as usual, and each finding states the maturity of the criterion behind it, per [findings-list](../../specs/findings-list.md) §5.1.
5. **Locate verification that this repository cannot host.** An item whose population needs a running service, a benchmark suite, a declared service level or a reviewed project's coverage report sets `Verification: adopter` and names the route back, which CONTRIBUTING documents as a procedure.

## Alternatives

**Define "blocking" as `critical` and leave the rest of the model alone.** Rejected: it keeps activation keyed on severity, and severity answers a different question. A `minor` judgment item is exactly as likely to be wrong as a `critical` one; it simply costs less when it fires.

**Suppress findings from immature items until their evidence is complete.** Rejected: honest classification put 118 of 118 items at `provisional` on the first run, so suppression would have silenced the entire corpus to close a documentation gap. Withholding a finding loses information; labelling it costs one field. §9 of the same Rule already prescribes narrowing, sharpening or lowering severity for a noisy item, and never hiding it.

**Declare maturity as a hand-written field.** Rejected: a status anyone can type is a status nobody has earned, and it would have become the second obligation in this model that nothing executes.

**Drop the worked-example requirement to match what the corpus actually did.** Rejected: a judgment item has no tool to calibrate against, so the example is the only place a reader learns where the author drew the line. The obligation was reachable; it had simply never been addressed to anyone.

## Consequences

- `workflow-rule-governance` takes a major version: §8's semantics changed and "blocking" is gone.
- `validate-rules.py` derives maturity, rejects a hand-written one and prints the distribution on every run. `test-validate-rules.py` asserts that distribution in three directions, so inverting the derivation fails a test rather than printing a plausible number.
- Every item now carries its owed rows: 118 `ready`, 0 `provisional`. Four items sit at `Verification: adopter` and depend on an adopting project to return fixtures.
- The findings contract gains a required element, which is a breaking change for a producer built against the previous version, so `findings-list` takes a major version.
- Adding a fourth enforcement class, or a third maturity state, now means editing one derivation in one Spec and one obligation in one Rule.
