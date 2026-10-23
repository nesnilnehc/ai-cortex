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
| Rule coverage dependency | All coverage fields present, list types, evidence-limited items retained, metadata preserved separately per emitter | Does not implement runtime Rule applicability or maturity derivation; bounded parameter/waiver evidence is recorded below |
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
python3 scripts/check-stable-governance-consumers.py
python3 scripts/test-stable-governance-consumers.py
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

Remaining work includes actual project/host consumers, full YAML/Markdown
interpretation, remaining selected core dependencies and any future real stable
entry deprecation. The bounded configuration/Rule/migration cases below do not
substitute for those workflows. Existing installer integration, Rule scenario,
asset-version and research tests supply separate evidence; they do not turn this
bounded matrix into complete 1.0 acceptance. See the
[readiness assessment](../project-overview/release-readiness.md).

## Configuration, Rule and migration extension

The [governance baseline](../../tests/fixtures/stable-consumers/governance-v0.6.0.json)
pins 0.6.0 Rule modeling, project configuration, stable policy and modeled quality
Rule sources. The checker compares 29 historical profile names, 18 parameter
provenances and required profile/waiver fields against the live registry. New
optional profile/parameter names can coexist; removed names or changed provenance
and required-field contracts fail the compatibility check.

Twelve additional reference regression methods cover:

- Loading an explicit configuration before inference, preserving unoverridden nested fields and retaining fallback values
  when configuration is absent, refusing conflicts, and leaving source bytes
  unchanged. Fixtures use JSON-compatible YAML in `.ai-cortex/config.yaml` and a
  fixed JSON fence in `CLAUDE.md`. This is not a complete YAML or Markdown parser.
- Required profiles, unknown profiles/parameters, derived facts, first baseline,
  preserved existing baseline, absent declared values and an explicit zero value.
  Parameter resolution never asserts that the Rule itself passed, and writes no
  baseline or inferred configuration.
- Valid and explicitly pinned historical waivers; missing fields, expiry, reversed
  dates, unknown approvers/Rule IDs, empty controls, mismatched and overly broad
  scope. Invalid waiver evidence returns a finding; valid waiver evidence remains
  waived, never passed. The clock is fixed in fixtures. Scope is compared against
  an explicit finite production-path population; this is not arbitrary glob
  containment, authority verification or an actual waiver approval.
- Test-only old/replacement entries within a major, rejection of premature removal,
  later-major removal, migration example and old-consumer/migration evidence.
  Names `fixture-review-v1` and `fixture-review` are not distributed aliases. No
  real stable Skill has been deprecated or renamed by these tests. Evidence flags
  simulate admission conditions; they do not attest a real future migration.

The guides do not settle YAML-versus-CLAUDE precedence when explicit sources
conflict. The reference loader refuses such a conflict instead of inventing that
precedence. A later normative decision requires new cases. Validation remains
separate from executing configured commands; no fixture command is run.

Two additional [real installer tests](../../scripts/test-cortex-installer.py)
exercise the existing 0.x legacy aggregate entry migration in isolated homes:
`clean --dry-run` preserves bytes; explicit `clean --yes` followed by `install`
removes old aggregate roots and installs canonical entries repeatably while
preserving unrelated personal directories. These exercise an existing experimental
legacy command, not the 1.x promise to retain a deprecated stable alias. The
installer suite now has 31 methods; the original 29 remain unchanged.

TDD recorded 46 initial assertion failures across nine governance methods, then
separate failures for profile requirements, baseline overwrite, null declared
values and protected-registry drift. All twelve final reference methods pass.
The two installer migration cases passed against the existing implementation;
no installer repair or production configuration change was needed.
