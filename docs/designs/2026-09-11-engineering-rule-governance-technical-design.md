---
artifact_type: technical-design
lifecycle: snapshot
created_at: 2026-09-11
parent: ../adr/0012-adopt-profiled-engineering-rules.md
status: approved
---

# Technical design: profiled engineering Rule governance

## Goal

Turn architecture and cross-cutting quality principles into versioned, selectable, evidence-backed Rules reusable before coding and enforceable after coding, without duplicating policy across project entry files, memory or Skills.

## Industry evidence

### Quality attributes must become system-specific and measurable

ISO/IEC 25010:2023 defines a product-quality model with nine characteristics and positions it for requirements, design objectives, test objectives, quality control and acceptance across the lifecycle.[^1] This supports a shared quality vocabulary, but it does not make “maintainability” or “security” directly verifiable by itself.

The Software Engineering Institute makes the missing step explicit: quality attributes such as modifiability, performance, availability and security should be characterized through scenarios, just as use cases characterize functional requirements.[^2] Its QAW and ATAM guidance applies scenario-based analysis before implementation and evaluates risks, sensitivities and trade-offs as architecture becomes concrete.[^3] The design therefore puts measurable Quality Attribute Scenarios in requirements and system-specific tactics plus evidence in technical design. The reusable Rule is cited by ID; it is not copied into either artifact.

### A common baseline needs risk profiles, not project forks

NIST SSDF practices are outcome-based and intended to integrate into an existing lifecycle. NIST explicitly describes profiles as baseline practices enhanced for a use case, and says organizations align and prioritize them with business requirements, risk tolerance and resources.[^4] NIST Cybersecurity Framework profiles similarly align common outcomes with a particular implementation scenario and distinguish current from target state.[^5]

The inference for AI Cortex is broader than security: a canonical baseline can be common, while deployable services, public APIs, sensitive-data paths and distributed workflows activate additional mandatory profiles. Project-specific topology and thresholds are parameters, not edited copies. “Profile-specific” cannot mean “optional once the condition is true”.

### Stable identifiers and machine-readable policy enable reuse

OWASP ASVS publishes verification requirements with version-qualified identifiers and machine-readable forms, specifically recommending the version in external references because identifiers can change between releases.[^6] OPA separates declarative policy decisions from enforcement and accepts structured input from many enforcement points.[^7] These practices support stable Rule IDs, explicit versions and separation between the canonical policy and the Skill or CI tool that evaluates it.

Architecture tools demonstrate why enforcement strength must be explicit. ArchUnit can test package/layer dependencies and cycles as ordinary automated tests, and its freezing mechanism records existing violations so only new deterioration fails.[^8] Dependency-cruiser similarly models forbidden, allowed and required dependencies with severities.[^9] These tools can decide graph properties; they cannot fully decide whether a responsibility is cohesive or an abstraction is speculative. The Rule model therefore distinguishes `automated`, `tool-assisted` and `judgment` rather than pretending every criterion is machine-enforceable.

### Gates should block concrete risk, not optimize an opaque score

Google's review guidance treats code health as a direction of travel, distinguishes mandatory findings from non-blocking nits, and prioritizes technical facts over preference.[^10] Small, self-contained changes are easier to review thoroughly, less likely to introduce bugs and easier to roll back.[^11] GitHub code scanning records severity, location and dismissal reason, while delegated dismissal can require approval.[^12] These practices support item-level findings, change-surface budgets and audited waivers rather than a single architecture score.

### Observability and reliability require distinct evidence

OpenTelemetry defines traces, metrics and logs as signals and emphasizes correlation by trace/span context and resource identity.[^13] Google SRE defines user-facing SLIs/SLOs and connects an error-budget policy to release decisions.[^14] Microsoft's reliability guidance treats timeouts, bounded retries, backoff with jitter, idempotency and aggregate retry budgets as a coordinated system; it warns that layered retries can multiply load and worsen failure.[^15] These sources justify separate observability and reliability Rule sets. Performance may detect expensive retries, but reliability owns whether retry behavior preserves correctness; observability owns whether operators can see the outcome.

## Architecture and service decomposition

The governance architecture uses the repository's existing four asset layers and two existing orchestrators.

```text
                    canonical reusable policy
                  ┌──────────────────────────┐
                  │ rules/*-quality.md       │
                  │ stable ID + applicability│
                  │ evidence + pass condition│
                  └────────────┬─────────────┘
                               │ cites / executes
      project context          │                    artifact contracts
┌──────────────────────┐       v             ┌─────────────────────────┐
│ .ai-cortex/config    │  review-* Skills    │ specs/*-modeling.md     │
│ profiles, topology,  │<────────────────────│ requirement/design/task │
│ targets, waivers     │       │             └─────────────────────────┘
└──────────────────────┘       │ findings-list
                               v
              ┌─────────────────────────────────────┐
              │ post-coding sibling gates           │
              │ engineering: orchestrate-code-review│
              │ functional: alignment + acceptance  │
              └─────────────────┬───────────────────┘
                                v
                      orchestrate-repair-loop
                      fix + rerun affected gates
```

| Boundary | Responsibility | Explicit non-responsibility |
|---|---|---|
| `specs/rule-modeling.md` | Rule document, profile, project parameter and waiver data contracts | No review or maintenance workflow |
| `rules/*-quality.md` | Canonical independently verifiable obligations | No execution sequence or project topology |
| Concern `review-*` Skill | Resolve applicability, gather evidence and emit Rule-traceable findings | No local policy copy and no repair |
| `orchestrate-code-review` | Aggregate the engineering gate | No functional-completeness claim and no fixes |
| `review-implementation-alignment` | Compare approved intent with code and evidence | No intrinsic engineering-quality review |
| `orchestrate-repair-loop` | Consume both gates, apply targeted fixes and repeat | No new criteria and no replacement for atomic Skills |
| `AGENTS.md` / `CLAUDE.md` | Project constitution and routing links | No detailed Rule catalogue |
| Memory | Verified facts and recent lessons | No normative policy, topology authority or permanent waiver |

There is no `engineering-governance` Protocol: no two active roles exchange messages in a defined sequence. There is no umbrella governance Skill: phase routing alone has no unique output beyond what the artifact reviewers and repair loop already own.

## Components and detailed design

### Rule model and validator

- `specs/rule-modeling.md` defines `RULE_MODEL_V1`.
- A modeled Rule file declares `model`, `rule_prefix`, version and lifecycle metadata.
- Each item uses `### PREFIX-NNN — title` and a fixed field table: level, requirement, applicability, severity, enforcement, evidence, pass condition, non-applicability and remediation.
- `scripts/validate-rules.py` discovers opted-in documents, validates structure, checks the registry and rejects duplicate IDs.

The opt-in marker is a boundary of need, not of age: existing Rules are not made invalid, and editing a document does not oblige it to adopt the model. A set adopts the model when its items must be addressed from outside — waived, counted in coverage, or cited by another artifact — as [workflow-rule-governance](../../rules/workflow-rule-governance.md) states. Every engineering concern set qualifies, since a project genuinely needs to waive a legacy cycle or record which items a review could not decide. Among the pre-coding sets, task quality qualifies because tasks cite its obligations and resolve waivers against them, and technical design quality qualifies for the same citation reasons; both migrated with this change. Requirement quality and functional design quality do not qualify: their criteria are read while authoring, fixed on the spot and never waived, so they stay checklists and gain nothing from identifiers.

### Applicability resolver contract

Atomic review Skills resolve effective policy with this deterministic order:

1. Include all baseline items whose local `applies_when` condition is true.
2. Include profile items when a declared project profile or directly evidenced context matches.
3. Include project items when their named parameter is obtainable, resolving it by the provenance the Rule set declares: compute a `derived` value from the repository, read or take a `baseline` snapshot, and read a `declared` value from project configuration.
4. Handle an absent value by that same provenance. A failed derivation is evidence-limited. A first-run `baseline` is recorded, reported as baselined and fails nothing on that run. An absent `declared` value is evidence-limited and names the decision the project still owes. None of these ever becomes a pass.
5. Apply only valid, unexpired waivers matching the exact versioned Rule ID and narrower scope.

Provenance exists so that adoption effort falls only where a human decision is genuinely required. A universal obligation is never gated behind a parameter a project has not written; such an item is `baseline` level and uses the parameter to sharpen evidence rather than to switch itself on.

No central runtime resolver is added in this version. Skills follow the Spec, while the deterministic structural and architecture-scenario checks run in CI. A shared executable resolver can be added later if multiple runtimes demonstrate incompatible resolution behavior.

### Rule sets

| Rule set | Stable namespace | Core ownership |
|---|---|---|
| `architecture-quality` | `ARC` | Cohesion, dependency direction, cycles, boundary leakage, contracts, coupling, composition, change surface |
| `security-quality` | `SEC` | Trust boundaries, authorization, secrets, protected data, cryptography, supply chain, secure defaults |
| `reliability-quality` | `REL` | Timeouts, retries, idempotency, partial failure, isolation, terminal work, recovery evidence |
| `performance-quality` | `PERF` | Work bounds, I/O amplification, complexity, streaming, concurrency, caching, budgets, resources |
| `observability-quality` | `OBS` | Structured outcomes, correlation, SLIs, traces, telemetry safety, error ownership, background visibility |
| `testing-quality` | `TST` | Discriminating oracles, edge paths, integration assembly, contracts, determinism and coverage evidence |
| `implementation-alignment-quality` | `ALN` | Acceptance/design/task intent mapped to production code and independent evidence |

### Pre-coding artifact reviewers

`review-requirements`, `review-functional-design`, `review-technical-design` and `review-tasks` are independent atomic Skills. Each evaluates one artifact against one modeling Spec and one quality Rule. They are not meta-skills because they neither design another Skill nor aggregate several capabilities.

`review-functional-design` is used only when the functional layer exists: after user-visible behavior, workflow, state or permission design is drafted and before technical design. Pure refactoring or infrastructure work may skip it and derive technical design from an authorizing ADR.

## Database design

No database change. Governance configuration and waivers are YAML objects in the adopting repository; AI Cortex stores no central waiver database. Git history provides version and audit history for Rule and configuration changes.

## Interface contracts

### Rule reference

External artifacts and findings use either:

- `ARC-003` when the active Rule-set version is unambiguous in the current review; or
- `architecture-quality@1.0.0/ARC-003` when a waiver, audit record or historical report must pin exact semantics.

### Review output

Every atomic review continues to emit `findings-list`. A finding keeps its concern category and cites one failed Rule ID in its description. The Skill appends coverage metadata with four sets: passed, waived, not applicable and evidence limited.

### Project configuration

`.ai-cortex/config.yaml` accepts:

```yaml
governance:
  profiles: [deployable-service, public-api]
  parameters: {<concern>: <facts and targets>}
  waivers: [<waiver objects from rule-modeling>]
```

Unknown profiles or parameters are configuration errors. A project entry file points to this configuration and to the AI Cortex assets; it does not copy their content.

## Data flow and error handling

### Normal flow

1. Requirement review checks measurable quality scenarios when triggered.
2. Technical design maps scenario and Rule IDs to tactics, trade-offs, verification and owner.
3. Task review checks affected scope, Rule references and concrete verification for quality-sensitive work.
4. After coding, the engineering gate evaluates intrinsic quality; the functional gate evaluates intent alignment and executes acceptance checks.
5. Repair fixes a blocking signal and reruns every affected gate.

### Failure path: missing project parameter

When ARC-002 needs an allowed dependency map but none exists, the reviewer marks ARC-002 evidence-limited. Baseline cycle, leakage, coupling and cohesion items still run. The review cannot claim a full pass, but it also does not invent a topology.

### Failure path: invalid or expired waiver

The reviewer reports the underlying finding normally and separately reports why the waiver is invalid. It does not refresh expiry, widen scope or infer approval.

### Failure path: tool covers only part of an item

The tool result becomes one evidence source. For example, a static analyzer can detect a dangerous sink but may not establish authorization semantics. The Skill evaluates remaining evidence or marks the item limited; “tool clean” does not imply “Rule passed”.

### Failure path: tests pass but intent is missing

`review-implementation-alignment` builds an acceptance-to-code-to-evidence matrix. An unimplemented criterion, dropped field or absent production registration produces an ALN finding even when the current tests pass. Repair adds the missing behavior/evidence and reruns the engineering dimensions affected by that code change.

## Technology choices and trade-offs

| Option | Advantages | Drawbacks | Decision |
|---|---|---|---|
| Detailed Rules in `CLAUDE.md` / `AGENTS.md` | Immediate visibility | Entry files become large, provider-specific and duplicated; no stable item lifecycle | Rejected |
| Checklists embedded in each review Skill | Easy initial authoring | Criteria drift across producing, reviewing and repair paths | Rejected |
| One global mandatory checklist with fixed thresholds | Simple selection | Produces noise for libraries and misses context-specific obligations for critical services | Rejected |
| Canonical modeled Rules + profiles + parameters + waivers | Shared IDs, context-sensitive enforcement, distributable, auditable | More schema and maintenance discipline | Chosen |
| Central umbrella governance Skill/Protocol | One apparent entry point | Routing layer has no unique capability; Protocol semantics are invalid; encourages one rigid sequence | Rejected |

The chosen model favors policy stability over a minimal file count. It deliberately keeps some judgment-based items because architecture and design cannot be reduced honestly to static analysis, while requiring the evidence and pass condition to make that judgment reviewable.

## Test strategy

### Structural checks

- `scripts/validate-rules.py` validates every `RULE_MODEL_V1` Rule file, item field completeness, stable prefix shape, duplicate IDs and registry presence.
- Existing registry CI verifies the Skill directory count and required frontmatter.
- Existing relative-link CI verifies new local references.

### Vertical-slice forward test

`scripts/test-rule-scenarios.py` decides every `automated` blocking item across the repository's modeled Rule sets — 15 items over 9 fixtures, grouped into three populations. Constraint 8 of [rule governance](../../rules/workflow-rule-governance.md) requires three representative shapes **of the population a Rule set governs**, which differs by what the set is about: a task list's dependency cycle has nothing to do with whether the project is a library or a distributed service.

| Population | Shapes | What the shapes exercise |
|---|---|---|
| Engineering concerns (`ARC`, `SEC`, `TST`) | single-package library, layered application, distributed public service | Declared dependency direction, cycles, change surface, secret handling and contract compatibility, without letting service-only rules become universal noise |
| Task lists (`TASK`) | minimal conforming, defective at hand-off, engineering governance triggered | Required fields, hand-off state, dependency graph, upstream parent, and annotation citations that only apply once a governance trigger fires |
| Technical designs (`TDES`) | minimal conforming, defective, quality attribute triggered | Required sections, candidate approaches, parent approval state, and Rule citations that only apply once a quality trigger fires |

Every shape carries both a case that must be reported and a case that must not, and each assertion is mutation-checked: inverting the underlying fact turns the run red, while a variant whose profile is inactive keeps it green.

Enforcement strength decides the activation evidence. A `tool-assisted` item is not fixture-tested; it names the tool class supplying its decidable evidence and what that class cannot decide. A `judgment` item is not fixture-tested either, and authored prose is not presented as a test of it; it activates on a source anchor, an evidence contract, a bounded pass condition and worked pass/fail examples, with empirical calibration collected from adopting projects rather than manufactured here.

### Skill self-checks

Every changed or new review Skill is checked against `refine-skill-design`: canonical criteria are linked rather than copied; purpose, boundaries, behavior, I/O, restrictions, self-check and examples are present; reviewers emit findings and never repair.

## Quality attribute design

| source | rule_refs | design tactic | trade-off | verification | owner |
|---|---|---|---|---|---|
| ADR 0012: canonical reusable policy | ARC-001, ARC-006, ALN-003 | Keep criteria in Rules and execution in atomic Skills; no umbrella protocol/router | More cross-links and files | Rule validator, registry/link checks, Skill boundary audit | AI Cortex maintainers |
| ADR 0012: contextual enforcement | SEC-007, PERF-007, REL-008 | Profiles activate conditions; parameters supply topology/targets; missing parameters remain evidence-limited | Adopting projects must configure meaningful facts | Three-shape applicability tests and project-config examples | Project owner |
| ADR 0012: auditable exception | SEC-003, REL-004 | Versioned, scoped, approved and expiring waiver object with compensating controls | More effort than silent suppression | Structural validation plus review coverage footer | Rule owner and project approver |
| Operable post-coding loop | OBS-008, TST-001, ALN-001 | Separate engineering and functional gates; rerun affected gates after repair | Some checks may repeat | Repair-loop self-check and representative scenario review | Repair-loop Skill |

## Acceptance criteria

- [x] A modeled Rule Spec defines stable IDs, SemVer, applicability, evidence, pass conditions, project parameters and auditable waivers. (Covers ADR 0012 Decision 1)
- [x] Architecture criteria form a complete vertical slice from canonical Rule through atomic Skill, project configuration and deterministic multi-shape validation. (Covers ADR 0012 Decision 2-3)
- [x] Security, reliability, performance, observability and testing use the same externalized Rule model, and implementation alignment has its own post-coding Rule/Skill. (Covers ADR 0012 Decision 2-4)
- [x] Requirements, technical designs and tasks carry scenario, tactic, Rule-reference and verification information without copying canonical policy. (Covers ADR 0012 quality-attribute chain)
- [x] `orchestrate-code-review` owns only the engineering gate; `orchestrate-repair-loop` converges engineering and functional sibling gates. (Covers ADR 0012 Decision 4)
- [x] `AGENTS.md` and `CLAUDE.md` remain unchanged; adopting repositories receive a short entry-file pattern and project configuration guide. (Covers ADR 0012 separation decision)
- [x] The experimental umbrella Protocol and Skill are removed. (Covers ADR 0012 rejected umbrella alternative)

## Sources

[^1]: [ISO/IEC 25010:2023 — Systems and software Quality Requirements and Evaluation](https://www.iso.org/standard/78176.html), International Organization for Standardization, accessed 2026-09-11.
[^2]: [Reasoning About Software Quality Attributes](https://www.sei.cmu.edu/library/reasoning-about-software-quality-attributes/), Carnegie Mellon Software Engineering Institute, accessed 2026-09-11.
[^3]: [SEI Architecture Analysis Techniques and When to Use Them](https://www.sei.cmu.edu/library/sei-architecture-analysis-techniques-and-when-to-use-them/), Carnegie Mellon Software Engineering Institute, accessed 2026-09-11.
[^4]: [Secure Software Development Framework](https://csrc.nist.gov/projects/ssdf), National Institute of Standards and Technology, accessed 2026-09-11.
[^5]: [Examples of Framework Profiles](https://www.nist.gov/cyberframework/examples-framework-profiles), National Institute of Standards and Technology, accessed 2026-09-11.
[^6]: [OWASP Application Security Verification Standard](https://owasp.org/www-project-application-security-verification-standard/), OWASP Foundation, accessed 2026-09-11.
[^7]: [Open Policy Agent documentation](https://www.openpolicyagent.org/docs), Cloud Native Computing Foundation project, accessed 2026-09-11.
[^8]: [ArchUnit User Guide](https://www.archunit.org/userguide/html/000_Index.html), ArchUnit, accessed 2026-09-11.
[^9]: [Dependency-cruiser Rules Reference](https://github.com/sverweij/dependency-cruiser/blob/main/doc/rules-reference.md), dependency-cruiser project, accessed 2026-09-11.
[^10]: [The Standard of Code Review](https://google.github.io/eng-practices/review/reviewer/standard.html), Google Engineering Practices, accessed 2026-09-11.
[^11]: [Small CLs](https://google.github.io/eng-practices/review/developer/small-cls.html), Google Engineering Practices, accessed 2026-09-11.
[^12]: [Resolving code scanning alerts](https://docs.github.com/en/code-security/how-tos/manage-security-alerts/manage-code-scanning-alerts/resolve-alerts), GitHub Docs, accessed 2026-09-11.
[^13]: [OpenTelemetry Logging and Correlation](https://opentelemetry.io/docs/specs/otel/logs/), OpenTelemetry, accessed 2026-09-11.
[^14]: [Service Level Objectives](https://sre.google/sre-book/service-level-objectives/) and [Example Error Budget Policy](https://sre.google/workbook/error-budget-policy/), Google SRE, accessed 2026-09-11.
[^15]: [Transient Fault Handling](https://learn.microsoft.com/en-us/azure/architecture/best-practices/transient-faults), Microsoft Azure Architecture Center, accessed 2026-09-11.
