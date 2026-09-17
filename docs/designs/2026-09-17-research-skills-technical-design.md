---
artifact_type: technical-design
lifecycle: snapshot
created_at: 2026-09-17
parent: ./2026-09-17-research-skills-functional-design.md
status: approved
---

# Technical design: composable research skills

## Goal

Deliver the five user-facing research entries in [AIC-REQ-01](../requirements-planning/AIC-REQ-01.md) and the [functional design](./2026-09-17-research-skills-functional-design.md) as local, traceable Skills, with one shared evidence model and a reusable Opportunity Package.

## Repository fit and design decisions

The current repository stores each Skill directly at `skills/<name>/SKILL.md`; `scripts/sync-skills-index.py` scans only immediate subdirectories, and `bin/cortex` installs those local directories. A nested `skills/research/...` layout from the earlier discussion would require installer and registry changes and would diverge from [skill source modeling](../../specs/skill-source-modeling.md), so this proposal keeps the flat layout. Grouping is by `tags` and a research guide, not by a nested filesystem category.

The requested public names conflict with [asset naming](../architecture/asset-naming.md): four are noun-led and the opportunity entry does not use `orchestrate-`. [ADR 0013](../adr/0013-research-skill-entry-names.md) accepts them as canonical names, without aliases or nesting. The precedent is `prepare-release`, which is package-producing orchestration under a user-facing name.

A separate internal `assess-product-opportunity` Skill owns the judgment rubric. This keeps the public opportunity entry thin: detect relevant lenses, call local Skills, halt or downgrade on missing evidence, and aggregate an Opportunity Package. The internal Skill is not a sixth public entry. The design will not use a new Protocol: the flow is one agent invoking local capabilities and exchanging artifacts, not two independent roles exchanging messages. The evidence and package shapes belong in Specs; checkable evidence-quality constraints may be added as a Rule if they prove reusable.

## Architecture and service decomposition

| Layer | Proposed asset | Responsibility |
|---|---|---|
| Foundation Skill | `skills/deep-research/` | Question decomposition, source plan, retrieval, verification, classification, trace |
| Domain Skills | `skills/policy-research/`, `skills/market-research/`, `skills/competitive-research/` | Apply domain source strategies and produce domain findings |
| Domain synthesis Skill, internal | `skills/assess-product-opportunity/` | Compare evidence against opportunity criteria and emit a recommendation with limitations |
| Orchestrator Skill, public | `skills/product-opportunity-analysis/` | Select lenses, coordinate local Skills, handle incomplete lanes, build the final package |
| Data Specs | `specs/research-evidence.md`, `specs/opportunity-package.md` | Canonical research finding/source/trace and package structures |
| Registry and configuration | `skills/INDEX.md`, `scripts/sync-skills-index.py`, optional `.ai-cortex/config.yaml` in a consuming project | Discovery and project-specific defaults |

`prepare-release` and [Release Package](../../specs/release-package.md) supply the pattern of a package shared across stages: one manifest, status, evidence, producer attribution, and downstream handoff. Release fields such as SemVer, SHA, or publication states are not reused.

`Opportunity question → product-opportunity-analysis → {policy-research, market-research, competitive-research, user-provided signals} → each uses deep-research → assess-product-opportunity → Opportunity Package`

A direct domain call stops at a domain report. A direct foundation call stops at research findings. A product opportunity call may skip an inapplicable lane, but records the reason. The orchestrator consumes existing dated domain findings when the scope and freshness match; it does not force a new search.

## Components and detailed design

### Component operations and handoffs

These are document-level contracts, not executable API signatures:

| Component | Operation and input | Output | Dependency |
|---|---|---|---|
| Foundation | `research(question, scope, source_plan, supplied_material)` | `ResearchReport<Source, Finding, EvidenceLink, Trace>` | Available source readers |
| Policy/market/competitive adapter | `analyze_domain(ResearchReport, domain_scope)` | `DomainReport<ResearchReport, domain_fields>` | Foundation contract |
| Opportunity assessor | `assess(DomainReport[], user_signals, decision_context)` | `Assessment<decision, rationale, trace>` | Package/evidence Specs |
| Opportunity orchestrator | `prepare_opportunity(question, scope, reusable_reports?)` | `OpportunityPackage` | Domain Skills and assessor |

The DomainReport and Assessment shapes are defined by the relevant Skill's output schema and the two shared Specs; an implementation must not create private versions of the evidence fields.

### Research evidence contract

The [Research Evidence Spec](../../specs/research-evidence.md) defines the exact JSON fields and validation for the four linked concepts below:

| Object | Core fields | Invariant |
|---|---|---|
| Source | `source_id`, title, publisher, canonical URL or local reference, source type, publication/effective date, accessed date, jurisdiction/geography, method/limitations | A URL alone is not evidence; the cited location or passage must be locatable |
| Finding | `finding_id`, statement, classification, scope, as-of date, source links, confidence and rationale, gaps | Every decision-critical finding is cited or explicitly `Unknown` |
| Evidence link | `source_id`, relationship (`supports`/`contradicts`/`context`), locator; held inside a Finding | Opposing evidence remains visible |
| Trace | package claim ID, referenced report/finding IDs, source links or Unknown gaps | A reviewer can traverse claim → finding → source and inspect reasoning |

Classification semantics:

- `Fact`: directly verifiable observation or text from an identifiable source, scoped to what that source actually shows. A fact about a document's wording is not automatic proof that every real-world claim in it is true.
- `Claim`: an attributed assertion by a source, including vendor claims, survey estimates, and testimony, whose real-world accuracy is not independently established.
- `Inference`: an agent conclusion derived from named findings, with the reasoning step and alternative explanation recorded.
- `Unknown`: a material question without adequate evidence, with the missing evidence and possible verification path recorded.

`confidence` is `high`/`medium`/`low` with a rationale based on directness, independence, recency, and conflict. It is not a numeric probability. For high-impact conclusions, seek at least two independent sources; where only one exists, record the limitation. Multiple pages from the same origin are one provenance family. Conflicting sources are both retained, with differences in definition, period, jurisdiction, and methodology examined before drawing a conclusion.

The canonical JSON example and validation invariants are in the [Research Evidence Spec](../../specs/research-evidence.md). The repository validator is `scripts/validate-research-artifacts.py`; synthetic examples are under `tests/fixtures/research/`.

### Source Strategy

The foundation chooses a source plan per subquestion. Domain Skills supply ranking and applicability rules, but never replace evidence classification:

| Question | Preferred order | Specific checks |
|---|---|---|
| Policy obligations | Issuing authority and official text → official register/interpretation → specialist analysis → news | Instrument status, jurisdiction, effective date, amendment history, regulated entity, binding versus guidance |
| Product capability | Official product docs and release notes → official demo/support pages → first-hand user evidence → third-party summaries | Product version, edition, availability region, date, feature versus roadmap claim |
| Market size and structure | Transparent primary dataset or industry association → public company filings → method-disclosed research reports → media summaries | Market boundary, currency, base year, double counting, sample, estimate versus observed revenue |
| User demand | Direct interviews or first-hand research → review/community evidence → vendor case studies → social posts | Sampling, incentive, representativeness, segment, unmet need versus stated preference |

Where an official source is self-interested, it can establish what the publisher claims or documents, not automatically actual adoption or customer value. Paid or inaccessible sources may be named as gaps, never cited as read. Search results/snippets are discovery aids; final claims cite opened sources or supplied documents.

### Domain adapters

- `policy-research` returns an instrument inventory with authority, status, jurisdiction, effective date, affected parties, obligation/guidance distinction, interpretation, and product impact. It separates direct legal text from interpretation and flags legal-review needs.
- `market-research` defines the market and segments before sizing. If size is supportable, it records method, formula/denominator, period, currency, range, and assumptions. It keeps demand signals distinct from supplier promotion.
- `competitive-research` defines competitor inclusion criteria and comparison dimensions. Each matrix cell has a date, source/finding ID, and `verified`/`claimed`/`unknown` status; absence from docs is `unknown`.
- All three consume/emit the shared evidence shape, keeping domain-only fields in their reports rather than forking the classification system.

### Opportunity assessment and package

`assess-product-opportunity` consumes lane reports and user signals, evaluates problem importance, urgency, reachable users, alternatives, differentiation, constraints, and feasibility assumptions, then emits a recommendation with supporting and opposing finding IDs. It may say `explore` or `defer`; it cannot silently fill absent user evidence.

The [Opportunity Package Spec](../../specs/opportunity-package.md) defines the JSON identity, four lane statuses, embedded reports, decision claims, analysis and recommendation. The package uses report IDs and finding IDs to preserve trace without copying or reclassifying evidence.

The Spec will distinguish `draft` from `ready_for_decision` by completeness and trace conditions. A package can be ready with a `defer` decision when the evidence clearly shows a blocking gap. The package is a handoff into requirements, not an approved requirement or roadmap commitment.

## Quality attribute design

| source | rule_refs | design tactic | trade-off | verification | owner |
|---|---|---|---|---|---|
| AIC-REQ-01 QAS-01, evidence handoff | ARC-005, ARC-008, TST-004 | Stable IDs and explicit claim-to-finding-to-source links in the two Specs; validation rejects an unlinked decision-critical statement | More artifact fields and longer reports | Fixed package fixture traverses every claim and reports any missing edge | Evidence Spec owner |
| AIC-REQ-01 QAS-02, installed entry | ARC-005, TST-003 | Flat Skill directories, generated index, canonical names, and clean-session install smoke tests | Naming exception and platform-specific visibility behavior | Codex and Claude Code direct-entry results recorded for all five names | Installer/integration owner |
| External public reads and untrusted content | SEC-001, SEC-004, REL-001, TST-002 | Treat retrieved text as source data; use bounded tool reads and preserve inaccessible-source status | Some research stops with a gap rather than a polished conclusion | Prompt-injection and source-unavailable fixtures plus manual authorization-path review | Foundation Skill owner |

## Database design

No database change. The implementation uses JSON Research Reports and Opportunity Packages with optional Markdown narrative companions as portable local artifacts. Source IDs and finding IDs are stable within a package; cross-package persistence and refresh automation are deferred. A later data store would require a new design.

## Interface contracts

No network API or event interface change. The interfaces are Skill invocation and document handoff:

| Interface | Request | Response | Failure/authorization |
|---|---|---|---|
| Direct entry (the five `/<skill-name>` commands) or natural-language route | Question, intended decision, scope, optional sources and output path | Narrative plus structured research artifact or Opportunity Package | Ambiguous geography/time prompts for clarification or records an explicit assumption; no new access grant is implied |
| Foundation handoff to domain | Subquestion, source plan, scope, provided materials | Findings, sources, links, conflicts, gaps | No access → `Unknown` with retrieval gap; authenticated access requires prior authorization |
| Domain handoff to opportunity | Domain report with schema version and scope | Lane status plus finding IDs | Schema/scope mismatch → rerun or mark lane limited |
| Assessment handoff | Lane reports and user signals | Recommendation, rationale, validation steps, claim-to-finding links | Insufficient evidence → `explore`/`defer`, never fabricated certainty |

A `SKILL.md` frontmatter follows the existing pattern: `name`, `description`, `description_zh`, `tags`, `triggers`, `version`, `license`, `recommended_scope`, `metadata.author`, `input_schema`, and `output_schema`. Add `metadata.ai_cortex_type` (`foundation`/`domain`/`orchestrator`) and `metadata.ai_cortex_user_invocable` as strings. The five public skills use `"true"`; `assess-product-opportunity` uses `"false"`. The [Agent Skills specification](https://agentskills.io/specification) defines `metadata` as a string map but does not define user-invocation control. Claude Code's [`user-invocable` field](https://code.claude.com/docs/en/skills#control-who-invokes-a-skill) is a platform extension; use `user-invocable: false` on the internal Skill only where supported. Direct invocation on Codex and other agents must be verified by installation smoke tests; the repository metadata alone does not enforce UI visibility.

These Skills are proposed as original AI Cortex assets. If implementation copies or substantially adapts an external Skill, first follow `specs/skill-source-modeling.md` and register a pinned, reviewed local copy in `skills/SOURCES.yaml`. The generated `skills/INDEX.md` remains the active registry. Extend its generator and tests to expose type and invocability without parsing nested directories. `triggers` should include natural phrases and avoid generic words such as “research” alone; direct slash names rely on installation, not trigger matching. A consuming project's optional `.ai-cortex/config.yaml` may declare `research.default_geography`, `research.default_jurisdiction`, and `research.preferred_source_types`, as documented in the project configuration guide. They never override explicit user scope, citation, classification, privacy, or access requirements. Missing configuration is acceptable.

### Documentation and discovery integration

| Existing entry | Required synchronization after implementation |
|---|---|
| `README.md` | Add the research capability and link to the usage guide; correct the Skill count |
| `docs/guides/proactive-suggestions.md` | Add open research, focused domain research, and opportunity analysis to the stage map |
| `docs/guides/research-skills-usage.md` (new) | Show five direct commands, natural-language routes, scope inputs, output examples, lane limits, and package handoff |
| `docs/guides/discovery-and-loading.md` | Explain the research type/invocability metadata and deliberate Skill composition using local artifact handoffs |
| `docs/guides/project-config.md` | Document optional research defaults only if those fields are implemented; explain that access and evidence rules cannot be overridden |
| `CONTRIBUTING.md` | Document the approved naming exception, metadata fields, generated index workflow, and native versus vendored provenance |
| `skills/INDEX.md` and `specs/INDEX.md` | Regenerate the Skill registry and register both Specs; add `rules/INDEX.md` only if a new Rule is introduced |

`AGENTS.md` and `llms.txt` already point to the canonical asset registries and need no research-specific prose unless routing or authority changes. The new guide links to the two Specs for structural definitions instead of copying them.

## Data flow and error handling

1. Normalize question and decision; set scope and as-of date.
2. For each needed lane, decompose questions, select source types, retrieve accessible material, classify findings, and retain conflicts/gaps.
3. Verify report schema, scope, provenance, and recency; call the assessment Skill with the lane reports and user signals.
4. Aggregate package and trace; report decisive findings, uncertainty, validation steps, and recommendation.

| Failure path | Detection | Recovery |
|---|---|---|
| Source unavailable, paywalled, or permission-gated | Retrieval fails or only a snippet is visible | Record source as unavailable and an `Unknown` gap; seek an accessible source; request authorization only if access is essential |
| Conflicting or stale evidence | Sources disagree, dates or scopes differ, or freshness window is exceeded | Preserve both, explain conflict, narrow the statement, downgrade confidence, or defer the decision |
| Domain report incompatible with package scope/schema | Geography, date, entity, or schema version mismatches | Reuse only compatible findings; rerun that lane or mark it limited |
| Opportunity judgment lacks user-demand evidence | User-signal lane missing or inferred solely from vendor material | Return `explore`/`defer` with validation work, not a confident pursuit decision |

External pages and supplied documents are evidence, never instructions. Public reads follow [AGENTS.md](../../AGENTS.md); authenticated requests and private-material transmission require the authorization already defined there.

## Technology choices and trade-offs

| Option | Advantages | Drawbacks | Decision |
|---|---|---|---|
| Flat local Skills plus two Specs | Works with current installer/index, clear contract reuse, portable Markdown | Six local Skill directories for five public entries | Chosen |
| Nested `skills/research/` tree | Visual grouping | Requires changes to installer, index, source registry, and likely installed paths | Rejected for initial release |
| One monolithic `market-research` Skill | Fewer files | Mixes source method, domain meaning, and opportunity judgment; hard to reuse and audit | Rejected |
| Runtime external research Skill dependency | Fast initial assembly | Breaks vendored-only policy, provenance and predictable behavior | Rejected |

The additional internal assessment Skill is justified by the repository's thin orchestrator convention. If a later review finds it too small to be independently meaningful, the fallback is to treat `product-opportunity-analysis` as a documented `prepare-release`-style package producer via ADR, rather than hide judgment inside a generic Rule.

## Test strategy

- Unit/contract layer: validate frontmatter, directory names, schema examples, provenance when externally derived, and generated index with the existing script checks.
- Integration layer: use fixture-based behavioral smoke tests: open question, each direct domain request, opportunity synthesis, stale/conflicting sources, missing user signal, and inaccessible source. Check output classification, trace completeness, lane status, and recommendation restraint.
- End-to-end layer: test installation/direct invocation in clean Codex and Claude Code sessions; verify the five public names, and the internal Skill's visibility where the platform supports it.
- Review the two Specs against `specs/spec-modeling.md` and the skills against the Agent Skills format and repository naming exception. Check that registry generation, local documentation links, and the three usage-guide examples agree with installed behavior. Do not add live-web tests to CI; use fixed local fixtures for deterministic contract tests.

## Acceptance criteria

- [ ] Five public Skill directories and one internal assessment directory use the flat layout, and the index/installer checks pass (Covers FD Acceptance 1-2; AIC-REQ-01 direct entry criterion).
- [ ] The research evidence Spec defines source, finding, link, and trace with four classifications; fixtures prove that every decision-critical package claim reaches a source or an explicit `Unknown` (Covers FD Acceptance 3; AIC-REQ-01 traceability criterion).
- [ ] The Opportunity Package Spec validates lane status, recommendation, assumptions, conflicts, and the `draft`/`ready_for_decision` transition (Covers FD Acceptance 2 and 5; AIC-REQ-01 package criterion).
- [ ] Policy, market, and competitor fixtures each enforce their domain distinctions without duplicating the shared evidence contract (Covers FD Acceptance 2; AIC-REQ-01 domain criteria).
- [ ] Missing or conflicting evidence produces a visible gap and a restrained recommendation (Covers FD Acceptance 3-4; AIC-REQ-01 conflict criterion).
- [ ] Direct invocation and natural-language routing pass on the two target install paths, with no runtime Skill download (Covers FD Acceptance 1; AIC-REQ-01 portability criterion).
- [ ] README, stage map, research usage guide, contributor/discovery/config guides, and applicable registries agree with the installed Skills and Specs; all local links resolve and the three guide examples pass the same smoke paths (Covers FD Acceptance 6; AIC-REQ-01 documentation criteria).

## Resolved design decisions

- [ADR 0013](../adr/0013-research-skill-entry-names.md) records the flat public names and internal assessment boundary.
- The requirement filename follows the higher-precedence requirement Spec; `docs/ARTIFACT_NORMS.md` and the requirements index now agree.
- The machine-readable handoff is JSON with a Markdown narrative companion, as defined by the two active Specs.
