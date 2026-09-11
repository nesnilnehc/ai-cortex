---
artifact_type: rule
name: architecture-quality
version: 1.0.1
model: RULE_MODEL_V1
rule_prefix: ARC
scope: production code and its declared module, component and public-contract boundaries
recommended_scope: project
status: active
created_by: ai-cortex
lifecycle: living
created_at: 2026-09-11
---

# Rule: Architecture Quality

## Scope

Applies to code with more than one responsibility, module or externally consumed contract. Generated code is excluded when its source schema is reviewed and regeneration is deterministic. Evaluate project topology from `.ai-cortex/config.yaml`, architecture documentation and build metadata; do not assume clean, hexagonal or layered architecture unless declared.

## Profiles and parameters

| Name | Kind | Provenance | Meaning |
|---|---|---|---|
| `public-api` | profile | — | Other independently released code or external users consume a contract |
| `dependency-injection` | profile | — | A composition root wires abstractions to implementations |
| `architecture.modules` | parameter | derived | Named modules and ownership boundaries |
| `architecture.allowed_dependencies` | parameter | baseline | Allowed directed edges between modules |
| `architecture.protected_contracts` | parameter | derived | Public APIs, event schemas and persisted formats requiring compatibility |
| `architecture.change_budgets` | parameter | baseline | Expected file, module, contract and migration surface by change size |

Provenance follows [rule-modeling](../specs/rule-modeling.md) §5.4: a project writes only the `declared` values.

## Rules

### ARC-001 — Responsibilities have one owner

| Field | Value |
|---|---|
| Level | `baseline` |
| Requirement | Each business or technical responsibility **MUST** have one clear module owner, and a module **MUST NOT** mix responsibilities that change for unrelated reasons. |
| Applies when | A scope contains two or more responsibilities or modules. |
| Default severity | `minor` |
| Enforcement | `judgment` |
| Evidence | Module names from `architecture.modules`, public entry points, change history or the current diff, and responsibility descriptions. |
| Pass condition | Each responsibility maps to one owner and every module has one coherent reason to change. |
| Not applicable when | A single-purpose script or generated artifact has no meaningful internal boundary. |
| Remediation | Move the misplaced responsibility to its owner or split the module along independent change reasons. |

### ARC-002 — Dependencies follow declared direction

| Field | Value |
|---|---|
| Level | `project:architecture.allowed_dependencies` |
| Requirement | Every inter-module dependency **MUST** be an allowed directed edge in the project's declared topology. |
| Applies when | `architecture.allowed_dependencies` is declared. |
| Default severity | `major` |
| Enforcement | `automated` |
| Evidence | Resolved import/build dependency graph and the declared allowed-edge map. |
| Pass condition | The actual edge set is a subset of the allowed edge set. |
| Not applicable when | The project has not declared module topology; ARC-003 and the other baseline items still apply. |
| Remediation | Move the dependency, introduce an owned contract, or update topology through an approved architecture decision. |

### ARC-003 — A module graph has no cycles

| Field | Value |
|---|---|
| Level | `baseline` |
| Requirement | A module dependency graph **MUST NOT** contain a directed cycle. |
| Applies when | Two or more modules exist. |
| Default severity | `major` |
| Enforcement | `automated` |
| Evidence | Imported module graph from the build or dependency analysis tool, resolved over `architecture.modules`. |
| Pass condition | Every strongly connected component contains exactly one module. |
| Not applicable when | The code scope contains one module only. |
| Remediation | Move the shared contract to its owner, merge inseparable modules, or invert one dependency through an interface. |

### ARC-004 — Boundaries do not leak implementation details

| Field | Value |
|---|---|
| Level | `baseline` |
| Requirement | A module's outward contract **MUST NOT** expose an implementation-only type, storage model, framework primitive or private dependency. |
| Applies when | One module is consumed across a boundary. |
| Default severity | `minor` |
| Enforcement | `tool-assisted` |
| Evidence | Exported types, function signatures, serialized schemas and imports in consumers. |
| Pass condition | Consumers can use the contract without importing or understanding the provider's private implementation. |
| Not applicable when | The symbol is private to one module. |
| Remediation | Define an owned boundary type and translate at the adapter edge. |

### ARC-005 — Public contracts evolve compatibly

| Field | Value |
|---|---|
| Level | `profile:public-api` |
| Requirement | A protected public contract **MUST** remain backward compatible, or carry an explicit version and migration path approved by its owner. |
| Applies when | A changed artifact is listed in `architecture.protected_contracts` or has independent consumers. |
| Default severity | `critical` |
| Enforcement | `tool-assisted` |
| Evidence | Contract diff, consumer compatibility tests, version declaration and migration plan. |
| Pass condition | Existing consumers continue to work, or the breaking change is versioned with tested migration. |
| Not applicable when | The contract has no released or independent consumer and is not protected. |
| Remediation | Restore compatibility, add a new version, or provide and verify a migration adapter. |

### ARC-006 — Cross-module coupling is necessary and bounded

| Field | Value |
|---|---|
| Level | `baseline` |
| Requirement | A change **MUST NOT** add cross-module dependencies that are unused, duplicative or avoidable through an existing owner contract. |
| Applies when | The change adds or broadens a dependency edge. |
| Default severity | `minor` |
| Enforcement | `judgment` |
| Evidence | New imports/calls, existing contracts and the reason each edge is required. |
| Pass condition | Every new edge serves a demonstrated requirement and uses the narrowest stable contract. |
| Not applicable when | No cross-module edge changes. |
| Remediation | Reuse the owner contract, move the behavior, or remove the unnecessary edge. |

### ARC-007 — Extension points correspond to demonstrated variation

| Field | Value |
|---|---|
| Level | `baseline` |
| Requirement | An abstraction or extension point **MUST** represent an existing contract boundary or at least two demonstrated variants; speculative generality is not allowed. |
| Applies when | The change introduces an interface, plugin point, strategy registry or generic framework. |
| Default severity | `suggestion` |
| Enforcement | `judgment` |
| Evidence | Call sites, implementations, roadmap requirement or public contract. |
| Pass condition | The abstraction isolates a real boundary or supports demonstrated variants with lower total coupling. |
| Not applicable when | The abstraction is required by an external contract or framework boundary. |
| Remediation | Keep the concrete implementation, narrow the interface, or defer the extension point until variation exists. |

### ARC-008 — Composition is explicit and complete

| Field | Value |
|---|---|
| Level | `profile:dependency-injection` |
| Requirement | Every required implementation **MUST** be wired at an explicit composition root, and production code **MUST** have a call path to newly delivered behavior. |
| Applies when | The project uses dependency injection, registries, plugins or route/handler registration. |
| Default severity | `major` |
| Enforcement | `tool-assisted` |
| Evidence | Composition root, registration metadata, production references and an integration test. |
| Pass condition | Required bindings resolve and a production entry point reaches the delivered behavior. |
| Not applicable when | The project has no runtime composition or registration mechanism. |
| Remediation | Add the binding/registration at the composition root and verify the complete path. |

### ARC-009 — Change surface stays within its declared budget

| Field | Value |
|---|---|
| Level | `project:architecture.change_budgets` |
| Requirement | A change that exceeds its declared file, module, public-contract or migration budget **MUST** be split or carry an approved impact justification. |
| Applies when | A change size and `architecture.change_budgets` are declared. |
| Default severity | `minor` |
| Enforcement | `automated` |
| Evidence | Diff statistics by module, public-contract diffs, migration files and the declared budget. |
| Pass condition | Every measured dimension is within budget, or an approved justification identifies why the wider surface is indivisible. |
| Not applicable when | No budget is declared; reviewers still assess avoidable coupling under ARC-006. |
| Remediation | Split the change, remove unrelated edits, or record and approve the cross-boundary impact. |

## Severity and gate policy

- `critical`: an unversioned breaking public contract or equivalent consumer outage risk.
- `major`: a defect that makes production behave wrongly or not at all — a violated dependency direction, a module cycle, or delivered behavior with no production call path.
- `minor`: structural debt that raises future cost without causing a present failure — mixed responsibility, a leaked boundary type, avoidable coupling, or a change surface over its declared budget.
- `suggestion`: a non-defect improvement supported by evidence.

Grade by what happens if the finding is not fixed. A structural defect that is genuinely correct at runtime does not block the gate merely because it is untidy.

## Waivers

Waivers follow [rule-modeling](../specs/rule-modeling.md). ARC-005 requires approval by the public-contract owner. ARC-003 waivers must freeze the existing cycle so no new edge or member can be added while remediation is pending.

## References

- [Classic software engineering sources](../docs/references/software-engineering-classics.md) — source hierarchy and applicability boundaries
- [Code Complete, Second Edition](https://www.microsoftpressstore.com/store/code-complete-9780735619678) — construction complexity and cohesive design; informs ARC-001, ARC-004 and ARC-006
- [The Pragmatic Programmer, 20th Anniversary Edition](https://pragprog.com/titles/tpp20/the-pragmatic-programmer-20th-anniversary-edition/) — orthogonality, DRY knowledge and decoupling; informs ARC-001, ARC-002 and ARC-006
- [Refactoring, Second Edition](https://martinfowler.com/books/refactoring.html) — behavior-preserving structural change in small steps; informs ARC-001, ARC-006 and ARC-009
- [Design Patterns](https://www.informit.com/store/design-patterns-elements-of-reusable-object-oriented-software-9780201633610) — applicability and trade-offs of recurring designs; informs ARC-004, ARC-007 and ARC-008 without requiring pattern use
- [The Mythical Man-Month, Anniversary Edition](https://www.informit.com/store/mythical-man-month-anniversary-edition-essays-on-software-9780132119160) — conceptual integrity and coordination complexity; informs ARC-001 and ARC-009
- [Rule Modeling Schema](../specs/rule-modeling.md)
- [Technical Design Quality](./technical-design-quality.md)
- [DORA: loosely coupled teams](https://dora.dev/capabilities/loosely-coupled-teams/)
- [ArchUnit user guide](https://www.archunit.org/userguide/html/000_Index.html)
- [SEI: Reasoning About Software Quality Attributes](https://www.sei.cmu.edu/library/reasoning-about-software-quality-attributes/)
