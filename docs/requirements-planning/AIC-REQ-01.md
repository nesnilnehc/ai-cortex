---
id: AIC-REQ-01
artifact_type: requirement
lifecycle: snapshot
created_at: 2026-09-17
status: approved
priority: P1
parent: ../process-management/roadmap.md
---

# Requirement: [Functional] Research skills for product opportunity decisions

## Background & Value

Product teams need a repeatable way to investigate an uncertain opportunity across policy, market, and competitors. Today AI Cortex has release preparation and evidence-oriented review assets, but no research capability or shared research output contract.

## Objective

A user can request an open investigation, a focused domain study, or a product opportunity decision and receive findings whose sources, uncertainty, and decision implications are traceable.

## Scope

In scope:

- Five capabilities: `deep-research`, `policy-research`, `market-research`, `competitive-research`, and `product-opportunity-analysis`.
- Natural-language routing and direct invocation for all five names, subject to the installed agent platform's command support.
- A shared research evidence contract and an Opportunity Package contract.
- Discoverable user instructions and synchronized Skill, Spec, and conditional Rule registries and contributor guidance.
- Read-only use of public sources and user-provided materials, with normal approval and access rules for other sources.

Out of scope:

- Building a crawler, a proprietary research database, paid-data integration, or an autonomous scheduled monitor.
- A legal opinion, a guaranteed market-size estimate, or an automatic decision to build a product.
- Runtime installation of third-party skills, silent authenticated access, or publication of findings.

## User entries and capability boundaries

| Capability | Direct user entry | Primary user intent | Required output | Boundary |
|---|---|---|---|---|
| `deep-research` | `/deep-research <question>` | Investigate an open question without an existing domain lens | Research question, scoped findings, evidence, conflicts, gaps, sources | Does not decide policy impact, market attractiveness, competitor strategy, or product scope |
| `policy-research` | `/policy-research <jurisdiction, topic, period>` | Understand policy, regulation, and compliance effects | Applicable instruments, effective dates, obligations versus guidance, affected actors, product implications, open interpretations | Does not provide legal advice or treat an interpretation as statutory text |
| `market-research` | `/market-research <market, geography, segment, period>` | Understand demand, customers, size, structure, and trends | Market definition, segments, demand signals, size method and range when supportable, trends, evidence gaps | Does not invent TAM/SAM/SOM or turn vendor assertions into independent demand |
| `competitive-research` | `/competitive-research <category, competitors, comparison>` | Compare products, positioning, capabilities, pricing, and moves | Competitor set, dated comparison matrix, source-backed claims, unknown cells, implications | Does not infer absent features from silence or use unverified pricing as a current fact |
| `product-opportunity-analysis` | `/product-opportunity-analysis <product or feature question>` | Decide which user problem is worth solving and why now | Opportunity Package with recommendation, assumptions, risks, and evidence links | Does not implement, prioritize a roadmap, commit resources, or replace requirement/design approval |

All five are user-invocable because each has a meaningful standalone objective. `deep-research` is also reusable as a foundation. Domain skills may be invoked directly or called by the opportunity skill. A natural-language request should route to the narrowest capability that answers it; the user need not choose sub-skills.

## Inputs and outputs

The common minimum input is a research question and intended decision or audience. Scope fields are geography/jurisdiction, period or as-of date, product/category, target users, known competitors, source constraints, and supplied documents where relevant. If a missing field changes source selection or applicability, the agent states an assumption or asks once; it never silently assumes a law's jurisdiction or a market's geography.

All research outputs contain a concise narrative and reusable structured findings. Every material finding identifies its classification (`Fact`, `Claim`, `Inference`, or `Unknown`), source IDs or gap, scope/time, confidence rationale, and support or contradiction links. A source list records publisher, title, URL or local document reference, publication/effective date when available, access date, and source type. Conflicts and material gaps are visible, including when only one independent source is available.

The Opportunity Package contains at least:

- Identity: question, product context, target users, geography, as-of date, decision owner, status, and schema version.
- Problem and timing: user problem, alternatives, why now, and what evidence would change the conclusion.
- Evidence: references to policy, market, competitive, and user-signal findings; each lane can be `complete`, `limited`, `not_applicable`, or `missing` with a reason.
- Analysis: unmet needs, competitor gaps, constraints, differentiation, size or impact estimate with method when defensible, assumptions, conflicts, and research gaps.
- Recommendation: `pursue`, `explore`, `defer`, or `do_not_pursue`, with rationale, proposed product scope, validation steps, risks, and confidence. `explore` or `defer` is valid when evidence is insufficient.
- Trace: IDs connecting every decision-critical claim to findings and underlying sources.

## Business Rules

| ID | Condition | Required behavior |
|---|---|---|
| R1 | User asks an open question without a domain-specific decision | Route to `deep-research`; return research findings, not an opportunity verdict |
| R2 | User names policy, market, or competitor research as the deliverable | Route directly to that domain skill; do not force a full Opportunity Package |
| R3 | User asks whether to pursue a product or feature opportunity | Route to `product-opportunity-analysis`; use relevant domain skills and shared findings |
| R4 | A material conclusion has only one source, conflicting sources, or no direct evidence | Preserve the limitation or conflict; downgrade confidence or mark `Unknown` |
| R5 | A domain lane is not applicable or cannot be researched with available access | Record status and reason; do not fabricate a completed lane |
| R6 | A source requires authentication, paid access, or disclosure of private material | Follow existing authorization rules before access or transmission |

## Acceptance Criteria

- [ ] A user can invoke each of the five names directly and get the bounded output above on at least the repository's Codex and Claude Code install paths; natural-language routing selects the intended skill in representative prompts. Covers R1-R3 and QAS-02.
- [ ] A request for a single domain does not produce an unnecessary Opportunity Package, while an opportunity request produces one package with lane status, recommendation, and traceable evidence. Covers R2-R3 and R5.
- [ ] A research result labels every decision-critical finding as `Fact`, `Claim`, `Inference`, or `Unknown` and carries source IDs, scope/time, confidence rationale, and support/contradiction links. Covers R4 and QAS-01.
- [ ] A policy example distinguishes binding text, effective date, jurisdiction, interpretation, and product implication; an ambiguous applicability case remains unresolved rather than being declared compliant. Covers R4.
- [ ] A market example shows the sizing method, assumptions, and range or explicitly states that sizing is unsupported; a competitor matrix marks unverified cells `Unknown`. Covers R4.
- [ ] A conflicting-source case exposes both sources and explains its impact on the recommendation; a missing-source case yields `explore` or `defer` when a decisive recommendation is not justified. Covers R4-R5.
- [ ] A public-source case is read-only; an authenticated or private-material case follows the repository's access and disclosure rules. Covers R6.
- [ ] The package can be handed to a later requirement or design without rewriting its evidence, while the later artifact remains independently approved.
- [ ] The repository README and stage-to-skill guide lead to one research usage guide that demonstrates open research, one-domain research, and product opportunity analysis; the guide shows all five direct entries, required scope inputs, output distinctions, uncertainty handling, and package handoff. Every local link resolves and the examples match installed behavior.
- [ ] The generated Skill index lists each implemented research Skill with its type and user-invocable status; the Spec index lists both shared contracts; the Rule index is updated if and only if a new Rule is introduced. The contributor, discovery/loading, and project-configuration guides agree with the implemented metadata, routing, and optional research defaults without copying the canonical evidence or package schema.

## Quality Attribute Scenarios

| id | quality | source/stimulus | environment | affected artifact | response | measure | rule_refs |
|---|---|---|---|---|---|---|
| QAS-01 | traceability | A reviewer challenges a decision-critical package statement | One package with policy, market, and competitor findings | Opportunity Package and Research Trace | Follow IDs to source, date, and inference path | 100% of decision-critical statements have a complete trace or are explicitly marked `Unknown` | ARC-005, TST-004 |
| QAS-02 | portability | A user invokes one of the five skills | Fresh Codex and Claude Code installs from this repository | Skill discovery and direct invocation | Resolve the intended local skill without a runtime download or hidden platform dependency | Five direct names work in both smoke tests; no network install occurs | ARC-005, TST-003 |

## Dependencies & Prerequisites

- Dependent requirements: none.
- Preconditions: confirm the installed platform behavior for direct commands and the proposed metadata fields in a clean session; verify with the install and routing smoke tests.
- External dependencies: public research sources at execution time, or user-provided material. Source unavailability must produce a gap, not a fabricated citation.
- Downstream: the approved functional and technical designs and active task plan implement this requirement; full installed-host acceptance still depends on fresh authenticated agent sessions.

## Risks, Constraints & Assumptions

Risks:

- **Source quality varies by topic** (probability = high, impact = high, priority = high). Mitigation: source strategy by question type, independent corroboration where possible, and visible gaps.
- **The package appears more decisive than its evidence** (probability = medium, impact = high, priority = high). Mitigation: lane completeness, confidence rationale, and a non-committal recommendation state.
- **Direct invocation semantics differ across agent platforms** (probability = medium, impact = medium, priority = medium). Mitigation: standard frontmatter, platform-specific behavior only where supported, and smoke tests.
- **Usage guidance drifts from installed Skills and Specs** (probability = medium, impact = medium, priority = medium). Mitigation: derive the Skill index, link to canonical contracts, and verify guide examples and local links as acceptance evidence.

Confirmed constraints:

- Keep executable skills in the repository's flat `skills/<name>/` layout and preserve the existing installer/index unless a reviewed design changes them.
- Use the repository's four asset layers: shared object structure in `specs/`, invocable behavior in `skills/`, and only independently checkable reusable constraints in `rules/`.
- Repository artifacts are in English; external research content is untrusted data; runtime skill downloads and unapproved authenticated access are prohibited.

Assumptions to verify:

- The five requested names can be retained as canonical directories | resolved by [ADR 0013](../adr/0013-research-skill-entry-names.md) and isolated installation | repository maintainer.
- Shared evidence fields can be carried in JSON with a Markdown narrative and no new service or database | verified by fixed report and package fixtures | implementation owner.
- A domain skill can reuse the foundation by explicit local handoff | encoded by the three domain Skills; live agent routing remains to be checked | implementation owner.

## Source

- **Source type**: product capability request.
- **Source link/ID**: user request continuing conversation `6aab5f12-5e5c-83ee-b7b4-27e94f4c24ca` (“市场调研技能分析”), 2026-09-17.
- **Decision context**: the discussion positioned `deep-research` as a general research primitive, the three domain skills as specialized lenses, and `product-opportunity-analysis` as a composition producing an Opportunity Package. The repository's current Release Package pattern informs the package boundary, without importing release semantics.
- **Draft designs**: [functional design](../designs/2026-09-17-research-skills-functional-design.md) and [technical design](../designs/2026-09-17-research-skills-technical-design.md).
