---
artifact_type: guide
lifecycle: living
created_at: 2026-10-23
status: active
---

# Stable-core consumer compatibility evidence

This guide records the scope and maintenance of the compatibility suite under the
[stable-core policy](../project-overview/stable-core.md). It is evidence tooling,
not an additional public schema, a runtime parser shipped to consumers, or a
claim that all stable dependencies have passed acceptance.

## Baselines and consumer model

[Historical descriptors](../../tests/fixtures/stable-consumers/) pin the exact
0.5.1 and 0.6.0 tag targets and SHA-256 of Findings, Release Package and Rule
modeling sources. They intentionally preserve the same contracted shapes where
those releases made no schema change. Historical package fixtures are JSON
exports of the published manifest records, with source paths and byte digests.
The review fixture is authored from the contract, not a captured model run.

The test-owned JSON review envelope represents fields recoverable from prose,
lists or tables. It does not require Skills to emit JSON. The reference consumer
uses the frozen historical descriptor or reads current Spec tables; independent
expected projections in fixtures determine acceptance. This is a bounded model
of consumer decisions, not two independently deployed applications.

| Surface | Protected observations | Limits |
| --- | --- | --- |
| Findings | Required fields; severity and maturity enums; optional suggestion; severity/location order; unchanged finding content, duplicates and count | Category semantics, sentence quality and all location normalization shapes are not validated |
| Rule coverage dependency | All coverage fields present, list types, evidence-limited items retained, metadata preserved separately per emitter | Does not implement Rule applicability, maturity derivation, parameter provenance or waiver evaluation |
| Release Package | Historical identity projection; required identity fields; status/action enums; compatible 1.x schema selection; required artifacts; blocked required checks; publication receipt presence | Does not execute publication, verify receipt URLs, interpret arbitrary prose evidence or validate every nested Spec field |
| Optional extensions | Historical readers retain decisions; original extended Findings remain intact | Accepting an optional field does not prove new mandatory fields or enum values are compatible |

12 permanent regression methods exercise old/current readers, malformed and
missing data, absence of optional suggestion, unknown enums/schema major,
optional extension, empty/zero/all-skipped execution evidence, preservation,
missing artifacts/receipt, ready-only publication admission, and an injected required-field drift in the current
Spec. These methods use subtests; the method count is not a supported-project or
model-run count. Text evidence is checked for emptiness and explicit zero/all-
skipped reports; nonempty prose alone cannot prove execution.

## Run and maintain

```sh
python3 scripts/check-stable-consumers.py
python3 scripts/test-stable-consumers.py
```

Use a complete Git checkout containing the pinned historical objects. CI's
registry job already uses full history; no model, network service or third-party
Python/YAML dependency is needed. The checker reports two historical descriptors,
four historical release-reader pairs and two historical review-reader pairs;
the regression suite additionally exercises current readers and negative cases.

Do not regenerate historical descriptors or expected outcomes just to make a
contract change pass. Review the change against the stable policy; retain old
fixtures and add a new baseline and migration cases as needed. Unknown enums
are not presumed compatible. Freeze a fixture's source commit/digest and review
its projection together; JSON exports are maintained test evidence, not an
automatic YAML round-trip validator. The selected table checks detect structural
changes; semantic prose changes still require review and actual consumer cases.

Remaining work includes actual project/host consumers, project-entry/configuration
loading, applicable Rule parameter/waiver cases, deprecation migrations and the
other selected core dependencies. Existing installer integration, Rule scenario,
asset-version and research tests supply separate evidence; they do not turn this
bounded matrix into complete 1.0 acceptance. See the
[readiness assessment](../project-overview/release-readiness.md).
