---
id: RULE_MODELING_SPEC_V1
name: Rule Modeling Schema
description: Spec defining modeled Rule documents, stable rule items, applicability profiles, project parameters and auditable waivers.
version: 1.0.0
status: active
lifecycle: living
created_at: 2026-09-11
scope: |
  Defines the structural contract for engineering Rule documents that opt into RULE_MODEL_V1,
  plus the project profile and waiver objects used to apply them. It does not redefine legacy
  Rule documents, execute reviews or prescribe a delivery workflow.
related:
  - ./spec-modeling.md
  - ./findings-list.md
  - ../rules/workflow-rule-governance.md
  - ../docs/adr/0012-adopt-profiled-engineering-rules.md
---

# Rule Modeling Schema

> **Data contract**: defines versioned, selectable and independently verifiable engineering Rule items

## 1. Position and scope

A modeled Rule document is a canonical policy set for one quality concern. It groups independently verifiable Rule items under a stable namespace while keeping execution in review Skills and project context in `.ai-cortex/config.yaml`.

This spec applies only when a Rule document declares `model: RULE_MODEL_V1`. Existing Rule documents remain valid indefinitely; the model is not retroactive merely because the file lives under `rules/`, and adopting it is not an improvement a document owes simply for having been edited. [workflow-rule-governance](../rules/workflow-rule-governance.md) states when a set should adopt the model: when its items must be waived, counted in coverage, or cited by another artifact. A criterion that a person reads, fixes on the spot and never waives stays a checklist.

In scope:

- The frontmatter and body shape of a modeled Rule document
- Stable identifiers and compatibility of Rule items
- Baseline, profile and project applicability
- Project parameters consumed by Rule items
- The structure and validity of a waiver

Out of scope:

- The process for creating, reviewing or retiring rules; that is constrained by [workflow-rule-governance](../rules/workflow-rule-governance.md)
- Running a review or fixing findings; those are Skills
- A fixed project architecture or numeric threshold; those are project parameters
- The shape of a finding; that belongs to [findings-list](./findings-list.md)

## 2. Mental model

The effective policy is resolved from four layers. A lower layer supplies context; it does not copy or silently weaken the layer above it.

| Layer | Owns | Example |
|---|---|---|
| Canonical Rule item | The invariant, default severity and pass condition | `ARC-003`: module dependency graph has no cycle |
| Profile | A reusable applicability condition | `deployable-service`, `public-api`, `sensitive-data` |
| Project parameters | The local facts needed to evaluate the rule | module map, allowed dependencies, p95 target |
| Waiver | A temporary, scoped exception with accountability | allow one legacy cycle until a dated extraction |

Applicability has three levels:

| Level | Meaning |
|---|---|
| `baseline` | Applies whenever the Rule document's scope is present; no profile selection can turn it off |
| `profile` | Applies when the named profile is active or its `applies_when` condition is true |
| `project` | Applies only when the project explicitly declares the named parameter or policy |

`profile` and `project` do not mean optional. Once their conditions hold, the item is mandatory unless a valid waiver covers the exact item and scope.

## 3. Naming

A modeled quality Rule document is named `<concern>-quality.md`, where `<concern>` is a stable kebab-case quality concern such as `architecture`, `security` or `observability`.

Rule item identifiers use `<PREFIX>-<nnn>`:

- `PREFIX` is the document's uppercase `rule_prefix`, 3-8 letters.
- `nnn` is a zero-padded sequence beginning at `001`.
- An identifier is never reused, including after an item is retired.
- A finding and a waiver cite the fully qualified form `<document-version>/<rule-id>`, for example `architecture-quality@1.0.0/ARC-003`, when exact historical meaning matters.

## 4. Frontmatter contract

```yaml
---
artifact_type: rule
name: <concern>-quality
version: <SemVer>
model: RULE_MODEL_V1
rule_prefix: <UPPERCASE>
scope: <where the rule set applies>
recommended_scope: user | project | both
status: draft | active | superseded | archived
created_by: ai-cortex
lifecycle: living
created_at: YYYY-MM-DD
# conditional
superseded_by: <rule document name>  # required when status: superseded
---
```

### 4.1 Field table

| Field | Type | Required | Description |
|---|---|---|---|
| `artifact_type` | string | yes | Fixed as `rule` |
| `name` | string | yes | Matches the filename without `.md` |
| `version` | SemVer | yes | Version of the whole Rule set |
| `model` | string | yes | Fixed as `RULE_MODEL_V1` |
| `rule_prefix` | string | yes | Uppercase namespace used by every item identifier |
| `scope` | string | yes | The code or artifact population governed by this Rule set |
| `recommended_scope` | enum | yes | `user`, `project` or `both` |
| `status` | enum | yes | `draft`, `active`, `superseded` or `archived` |
| `created_by` | string | yes | Fixed as `ai-cortex` for repository-owned rules |
| `lifecycle` | enum | yes | Fixed as `living` |
| `created_at` | date | yes | First publication date |
| `superseded_by` | string | conditional | Required when `status: superseded` |

### 4.2 State and compatibility semantics

| Change | Required version change |
|---|---|
| Clarify wording without changing pass/fail meaning | patch |
| Add an item, evidence method or non-breaking applicability profile | minor |
| Broaden an existing item's applicability, raise its default severity, or change its pass condition incompatibly | major |
| Retire an item | minor; keep the identifier in a `Retired identifiers` section |

An `active` Rule item is enforceable. A `draft` document can be tested but must not block delivery. A superseded or archived document must not be selected for new reviews.

## 5. Body structure contract

### 5.1 Required sections

Every modeled Rule document contains these sections in this order:

1. `Scope` — the governed population and explicit exclusions
2. `Profiles and parameters` — profiles and project facts referenced by its items
3. `Rules` — the independently verifiable items
4. `Severity and gate policy` — concern-specific severity rules, without redefining the global enum
5. `Waivers` — whether waivers are allowed and any concern-specific restrictions
6. `References` — authoritative sources and local assets

### 5.2 Rule item contract

Each item begins with `### <ID> — <title>` and contains exactly one field table with these rows:

| Field | Required | Contract |
|---|---|---|
| `Level` | yes | `baseline`, `profile:<name>` or `project:<parameter>` |
| `Requirement` | yes | One normative `MUST` or `MUST NOT` statement |
| `Applies when` | yes | A concrete condition; use `always` only for a true baseline |
| `Default severity` | yes | One value from `critical`, `major`, `minor`, `suggestion` |
| `Enforcement` | yes | `automated`, `tool-assisted` or `judgment` |
| `Evidence` | yes | Observable inputs used to decide the item |
| `Pass condition` | yes | A binary or explicitly bounded decision condition |
| `Not applicable when` | yes | A concrete exclusion, or `never` |
| `Remediation` | yes | The smallest normal direction for correction |

One item can have several evidence sources, but it has one obligation. If a paragraph contains independently violable obligations, split it into separate IDs.

### 5.3 Project profile object

Projects declare context in `.ai-cortex/config.yaml` without copying Rule text:

```yaml
governance:
  profiles: [deployable-service, public-api]
  parameters:
    architecture:
      modules: [domain, application, infrastructure, api]
      allowed_dependencies:
        domain: []
        application: [domain]
        infrastructure: [application, domain]
        api: [application]
      protected_contracts: [openapi/public.yaml]
      change_budgets:
        small: {files: 8, modules: 2, public_contracts: 0, data_migrations: 0}
```

| Field | Required | Description |
|---|---|---|
| `profiles` | yes | Reusable contexts activated for the project |
| `parameters` | optional | Facts or thresholds referenced by Rule items. A project only writes the `declared` ones; see §5.4 |

Unknown profiles and parameters are configuration errors; they are not silently ignored.

### 5.4 Parameter provenance

A parameter declares how its value is obtained. Provenance decides what a review does when the value is absent, so that configuration effort falls only where a human decision is genuinely required.

| Provenance | Meaning | When the value is absent |
|---|---|---|
| `derived` | The reviewer computes the value from the repository. A project never has to write it, and may only narrow or extend it. | Compute it. Only a failed derivation makes the item evidence-limited. |
| `baseline` | The present state is recorded once as a starting point; afterwards only a change that worsens it fails. | Record the present state, report the item as baselined rather than passed, and fail nothing on that run. |
| `declared` | A target, budget, threshold or classification that cannot be observed from code because it is a business decision. | The item is evidence-limited and the report names the decision the project still owes. |

A `derived` or `baseline` parameter **MUST NOT** be what makes an item applicable. An obligation that holds regardless of local facts is a `baseline` level item and uses the parameter only to sharpen its evidence. Gating a universal obligation behind a parameter the project has not written yet silently disables that obligation, which §2 forbids for baseline items and which a reader cannot detect from the coverage report.

A baseline is a dated, reviewable artifact, not a silent allow-list. It records what already existed when the Rule set was adopted; it never absorbs a violation introduced after it was taken, and removing an entry from it is a normal improvement rather than a configuration change.

### 5.5 Waiver object

```yaml
waivers:
  - id: WV-2026-014
    rule_id: architecture-quality@1.0.0/ARC-003
    scope: src/legacy-billing/**
    reason: Existing cycle cannot be split before the billing cutover.
    owner: billing-team
    approved_by: architecture-owner
    created_at: 2026-09-11
    expires_at: 2026-11-30
    compensating_controls: [No new edges may join the cycle; dependency snapshot is gated.]
    evidence: docs/adr/0042-split-legacy-billing.md
```

Every field shown is required. `scope` must be narrower than the Rule set scope; `expires_at` must be later than `created_at`; `rule_id` must resolve to an active or historically pinned item. An expired, unresolved, unapproved or broader-than-needed waiver is invalid and does not suppress a finding.

### 5.6 Finding traceability

A review finding's description cites the Rule ID that failed. The finding's category remains the category defined by [findings-list](./findings-list.md); Rule IDs do not replace categories.

## 6. Anti-patterns

- A heading such as “keep coupling low” with no evidence or pass condition
- A project copying and editing a canonical Rule instead of supplying a profile or parameter
- Calling a profile “optional” after its applicability condition is true
- A blocking item whose pass condition depends only on an unexplained LLM score
- A waiver with no expiry, owner, approver or compensating control
- Reusing an identifier after deleting or moving its former meaning
- Combining authentication, secret handling and dependency provenance in one Rule item
- Treating “tool found no issue” as proof when the tool does not cover the whole Rule
- A Rule document containing review steps, repair loops or other process instructions

## 7. Examples

### 7.1 Baseline item

```markdown
### ARC-003 — A module graph has no cycles

| Field | Value |
|---|---|
| Level | `baseline` |
| Requirement | A module dependency graph **MUST NOT** contain a directed cycle. |
| Applies when | Two or more modules exist. |
| Default severity | `major` |
| Enforcement | `automated` |
| Evidence | Imported module graph from the repository's build or dependency tool. |
| Pass condition | The graph's strongly connected components all contain one module. |
| Not applicable when | The code scope contains one module only. |
| Remediation | Move the shared contract to its owner or invert one dependency through an interface. |
```

### 7.2 Profile item

```markdown
### OBS-002 — Correlation crosses process boundaries

| Field | Value |
|---|---|
| Level | `profile:distributed-workflow` |
| Requirement | Correlation context **MUST** propagate across every synchronous and asynchronous process boundary. |
| Applies when | A request or job crosses two independently executing components. |
| Default severity | `major` |
| Enforcement | `tool-assisted` |
| Evidence | Propagation code, telemetry schema and an integration trace. |
| Pass condition | One correlation or trace identity connects the complete representative path. |
| Not applicable when | Execution never crosses a process boundary. |
| Remediation | Propagate standard trace context in request headers and message metadata. |
```

## 8. Relationship to other assets

- [workflow-rule-governance](../rules/workflow-rule-governance.md) constrains maintenance, compatibility and rollout.
- Concern Rule sets instantiate this schema; review Skills execute the applicable items.
- [findings-list](./findings-list.md) defines how a failed item is reported.
- [ADR 0012](../docs/adr/0012-adopt-profiled-engineering-rules.md) records why the repository chose this layered model.
