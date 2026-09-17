---
artifact_type: tasks
lifecycle: living
created_at: 2026-09-17
parent: ./2026-09-17-research-skills-technical-design.md
status: active
---

# Tasks: implement composable research skills

This implementation plan tracks [AIC-REQ-01](../requirements-planning/AIC-REQ-01.md), the [functional design](./2026-09-17-research-skills-functional-design.md), the approved technical design, and [ADR 0013](../adr/0013-research-skill-entry-names.md). `P0` is the contract and usable core, `P1` completes the domain and opportunity flow, and `P2` covers navigation and evaluation. Dependencies are blocking unless acceptance text says otherwise. The task state below reflects the local implementation on 2026-09-17; the [smoke record](../references/research-skills-smoke-test.md) distinguishes verified install paths from pending authenticated agent routing.

| Id | Priority | Task | Depends on | Target files / directories | Acceptance | Owner / Hint | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| T1 | P0 | Record the research Skill naming decision | — | `docs/adr/0013-research-skill-entry-names.md` (or next free number), `docs/architecture/asset-naming.md`, `docs/ARTIFACT_NORMS.md` | Accepted ADR records canonical public names and the internal name, naming guidance permits only the approved exception, and the requirement filename policy is reconciled with the higher-precedence Spec (design: Repository fit, Open review points). | Architecture reviewer | Done |
| T2 | P0 | Define the shared research evidence Spec | T1 | `specs/research-evidence.md`, `specs/INDEX.md` | Spec covers source/finding/link/trace IDs, four classifications, conflict handling, confidence rationale, scope/date, and examples that distinguish a documented Fact from an unverified Claim (design: Research evidence contract). | Spec author | Done |
| T3 | P0 | Define the Opportunity Package Spec | T2 | `specs/opportunity-package.md`, `specs/INDEX.md` | Spec defines identity, lane statuses, analysis, recommendation, trace, draft/readiness criteria, and serialization; a missing lane and a defer decision validate without invented evidence (design: Opportunity assessment and package). | Spec author | Done |
| T4 | P0 | Extend Skill registry metadata rendering and validation | T1 | `scripts/sync-skills-index.py`, `scripts/test-skills-index.py`, `skills/INDEX.md`, relevant fixtures under `tests/fixtures/skills-index/` | Generator displays `ai_cortex_type` and `ai_cortex_user_invocable` for opted-in Skills, rejects invalid values, preserves existing entries, and passes `--check` (design: Interface contracts). | Repository tooling | Done |
| T5 | P0 | Implement the foundation research Skill and source strategy | T2, T4 | `skills/deep-research/SKILL.md`, `skills/deep-research/README.md`, optional local `references/` | Open-question fixture shows decomposition, source plan, two-source corroboration when available, Fact/Claim/Inference/Unknown, conflict and gap preservation, and complete trace; no product verdict or runtime Skill install (design: Foundation, Source Strategy). | Skill author | In Progress |
| T6 | P1 | Implement policy research domain adapter | T5 | `skills/policy-research/SKILL.md`, `skills/policy-research/README.md` | Fixture distinguishes official obligation, guidance, interpretation, jurisdiction, effective date, and product implication; an ambiguous law remains unresolved (design: Domain adapters). | Skill author | In Progress |
| T7 | P1 | Implement market research domain adapter | T5 | `skills/market-research/SKILL.md`, `skills/market-research/README.md` | Fixture states market boundary, segments, demand sources, and transparent sizing method/range or unsupported status; vendor claims are attributed (design: Domain adapters). | Skill author | In Progress |
| T8 | P1 | Implement competitive research domain adapter | T5 | `skills/competitive-research/SKILL.md`, `skills/competitive-research/README.md` | Dated feature matrix cites each populated cell, distinguishes verified/claimed/unknown, and never infers absence from documentation silence (design: Domain adapters). | Skill author | In Progress |
| T9 | P1 | Implement internal opportunity assessment Skill | T3, T6, T7, T8 | `skills/assess-product-opportunity/SKILL.md`, `skills/assess-product-opportunity/README.md` | Given fixed lane artifacts, emits a recommendation, opposing evidence, assumptions, validation steps, and finding IDs; missing user signals yields `explore` or `defer` when decisive pursuit lacks support (design: Opportunity assessment). | Skill author | In Progress |
| T10 | P1 | Implement the public opportunity orchestration Skill | T3, T6, T7, T8, T9 | `skills/product-opportunity-analysis/SKILL.md`, `skills/product-opportunity-analysis/README.md` | Selects relevant lanes, reuses scope-compatible reports, handles failed/irrelevant lanes, invokes local assessment, and emits a valid package; a direct domain request remains outside this flow (design: Architecture, Data flow). | Skill author | In Progress |
| T11 | P1 | Add deterministic research contract fixtures | T5, T6, T7, T8, T9, T10 | `tests/fixtures/research/` and focused validation under `tests/` or `scripts/` | Fixed fixtures cover foundation/domain reports, complete opportunity, conflict, stale source, inaccessible source, and missing user signal; every decision-critical package statement traces to a source or Unknown; no live-web CI dependency (design: Test strategy). | Verification owner | In Progress |
| T12 | P1 | Verify direct invocation on installed platforms | T4, T10, T11 | Smoke-test record under `tests/` or `docs/references/` | Clean Codex and Claude Code installs resolve five public names; record natural-language routing and the internal Skill's visibility per platform, with no runtime download (design: Interface contracts, Test strategy). | Integration owner; blocked by unauthenticated isolated Claude Code session and no fresh Codex agent check | Blocked |
| T13 | P2 | Publish the research user entry guide and stage map | T10, T12 | `README.md`, `docs/guides/research-skills-usage.md`, `docs/guides/proactive-suggestions.md` | README links to the guide and has the correct Skill count; stage map routes open/domain/opportunity intents; guide examples for all three routes match clean-session behavior and every local link resolves (design: Documentation and discovery integration). | Documentation owner | In Progress |
| T14 | P2 | Synchronize contributor, discovery, and configuration guidance | T3, T4, T12 | `CONTRIBUTING.md`, `docs/guides/discovery-and-loading.md`, `docs/guides/project-config.md`, `skills/INDEX.md`, `specs/INDEX.md`; `rules/INDEX.md` if a Rule is added | Metadata, public/internal invocation, local handoff, optional research defaults, provenance, and naming exception match the implementation; preserve the corrected Skill-index lookup and Rule-installation description; generated and manual indexes are current, and no guide duplicates the canonical Specs (design: Documentation and discovery integration). | Documentation owner | In Progress |

T5-T11 have implementation files and passing local contract checks, but their behavior has not been accepted in an authenticated agent session. T12 is blocked because the isolated Claude Code session reports no API login; a fresh Codex agent check also remains open. T13 and T14 have their files in place, with clean-session routing checks pending. No user-global Skill paths were changed for this smoke test.

## Dependency path

`T1 → T2 → T5 → {T6, T7, T8} → T9 → T10 → T11 → T12 → {T13, T14}`. `T3` follows `T2` and gates `T9/T10`. `T4` follows `T1` and gates initial Skill creation and final registration. T6-T8 can be implemented independently once T5 is accepted. T13 and T14 follow the platform check and can be completed independently.

## Engineering governance

| task | affected_scope | rule_refs | verification | waiver |
|---|---|---|---|---|
| T2, T3 | Public artifact contracts in `specs/` | ARC-005, TST-004 | Validate examples against the written schemas; review schema version and compatibility rules | — |
| T4 | Skill registry parser, metadata, installed discovery | ARC-005, TST-003, TST-004, TST-006 | Existing index tests and fixtures pass; `python3 scripts/sync-skills-index.py --check` passes | — |
| T5, T6, T7, T8 | External-source read paths, untrusted content, cited outputs | SEC-001, SEC-004, SEC-007, REL-001, TST-002 | Fixed fixtures cover prompt injection in a source, unavailable/authenticated source, and no fabricated citation; manually inspect access behavior | — |
| T9, T10 | Cross-Skill handoff, package aggregation, incomplete lanes | ARC-001, ARC-008, REL-004, TST-003 | End-to-end fixture proves no hidden domain judgment in orchestrator and a truthful partial outcome on lane failure | — |
| T11, T12 | Regression fixtures and installed user entry paths | TST-001, TST-004, TST-006 | Deterministic fixture run plus recorded Codex/Claude Code clean-session invocation results | — |

## Delivery gates

1. Requirement, functional design, technical design, naming ADR, Specs and local Skill implementation are in place.
2. The task list is active; local contract and installation checks are recorded in the smoke record.
3. Complete the authenticated direct-invocation and natural-language routing check for five public entries in fresh Codex and Claude Code sessions.
4. Use one bounded real research case to inspect trace usability and untrusted-source behavior after agent access is available.
5. Reconcile T12-T14 acceptance, then run post-coding alignment review. `prepare-release` remains downstream release work.
