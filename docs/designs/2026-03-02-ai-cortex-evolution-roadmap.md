# AI Cortex Evolution Roadmap

**Date:** 2026-03-02
**Status:** Approved
**Approved by:** User
**Method:** brainstorm-design skill (structured dialogue)

## Goal

Define the evolution and optimization directions for AI Cortex beyond v2.0.0, covering engineering infrastructure, skill coverage, orchestration, ecosystem, and specification maturity.

## Context

At the time of this analysis:

- Version 2.0.0, solo-maintained (57 commits), ~33 days of active development
- 28 canonical skills, 7 rules, 1 spec (skill.md v2.0.0)
- Spec v2.0.0 migration just completed: all skills now have Core Objective sections
- No CI/CD; `verify-registry.mjs` is the only automated check (run manually)
- Code review ecosystem is mature: 15/28 skills are review-related with a clear composition graph
- ASQM audit last run 2026-02-27; 2 new skills (`brainstorm-design`, `commit-work`) not yet audited
- Multi-channel distribution: skills.sh, SkillsMP, Claude Plugin (8/28 skills exposed)

## Architecture

The roadmap is organized into 5 layers with 4 implementation phases:

```
Layer A: Engineering Infrastructure (CI/CD, quality gates)
Layer B: Skill Coverage (languages, frameworks, libraries)
Layer C: Orchestration & Composition (orchestrators, skill chains)
Layer D: Ecosystem & Distribution (Plugin sync, community)
Layer E: Specification Evolution (lifecycle, testable spec)
```

Phases are ordered by dependency: infrastructure first, then capabilities, then composition, then ecosystem.

## Components

### A1. CI/CD Automation

**Recommended approach:** Minimal GitHub Actions + Dogfooding

- PR trigger: run `verify-registry.mjs` to validate registry sync
- Main branch merge: trigger ASQM audit check
- Use the project's own `generate-github-workflow` skill to generate the initial workflow

| Alternative | Pros | Cons | Best for |
| :--- | :--- | :--- | :--- |
| **A: Minimal CI + Dogfood (recommended)** | Dogfoods own assets; low maintenance | Limited CI value for pure-Markdown project | Current stage |
| B: Extended CI + Spec compliance | Also solves E12 (spec testing) | Higher dev effort; script-spec sync burden | Governance-focused stage |
| C: CI + Release automation | Full release pipeline | Over-engineering for solo project | Community-ready stage |

### A2. Quality Gate Automation

**Recommended approach:** CI-integrated incremental audit

- Structural checks on new/modified skills: YAML metadata completeness, Core Objective presence
- Registry sync: INDEX + manifest consistency
- ASQM dimension hints (non-blocking): estimated scores for human confirmation

| Alternative | Pros | Cons | Best for |
| :--- | :--- | :--- | :--- |
| **A: CI integration + incremental audit (recommended)** | Low friction; informational | ASQM scoring needs LLM; scripts can only check structure | Near-term |
| B: ASQM scoring scripted | Repeatable, objective | Cannot replace human judgment on semantic dimensions | Mid-term enhancement |

### B3. Language Review Expansion

**Recommended approach:** TypeScript/JavaScript first, Rust second

Priority matrix by Agent programming scenario frequency:

| Language | Priority | Rationale |
| :--- | :--- | :--- |
| **TypeScript/JavaScript** | P0 | Most common Agent dev language; covers frontend + Node.js + Deno |
| **Rust** | P1 | Systems + WASM; high review complexity (ownership, lifetimes) |
| Ruby | P2 | Rails ecosystem still active but niche |
| Kotlin | P2 | Android + server-side; overlaps with Java review |
| Swift | P3 | Apple ecosystem only |
| C/C++ | P3 | Extremely complex review rules; ROI needs evaluation |

| Alternative | Pros | Cons | Best for |
| :--- | :--- | :--- | :--- |
| **A: TS/JS first + Rust next (recommended)** | Maximizes coverage value | Two skills to build | Broadest impact |
| B: Demand-driven | Avoids unused skills | Reactive; may miss market window | Resource-constrained |
| C: Full rollout | Wide coverage | Maintenance burden; quality may vary | Community with contributors |

### B4. Framework Review Expansion

**Recommended approach:** React first, then ASP.NET Core

Priority matrix:

| Framework | Priority | Rationale |
| :--- | :--- | :--- |
| **React** | P0 | Highest market share frontend framework |
| **Next.js** | P1 | React meta-framework; SSR/RSC review scenarios are unique |
| **ASP.NET Core** | P1 | Completes .NET review chain with review-dotnet |
| Spring Boot | P2 | Complements review-java |
| Django/FastAPI | P2 | Complements review-python |
| Angular | P3 | Declining market share |

| Alternative | Pros | Cons | Best for |
| :--- | :--- | :--- | :--- |
| **A: React first + chain completion (recommended)** | Fills largest gap; synergy with TS/JS | Need to prioritize among many options | Maximum value |
| B: One framework per language skill | Complete orchestration chains | Some combinations may be low-frequency | Completeness-oriented |

### B5. Library-Level Review Skills

**Recommended approach:** Domain-based rather than library-specific

- `review-orm-usage`: N+1 queries, connection leaks, migration safety (covers Prisma, EF, SQLAlchemy, etc.)
- `review-http-client-usage`: timeout, retry, circuit breaker patterns
- `review-auth-library-usage`: token handling, session security

| Alternative | Pros | Cons | Best for |
| :--- | :--- | :--- | :--- |
| B: Domain-based (recommended) | Not tied to specific libraries; broader applicability | Cannot provide library-specific best practices | Sustainable approach |
| A: Specific libraries (Prisma, EF) | Deep, actionable advice | Fast library iteration; high maintenance | High-traffic libraries |
| C: Skip for now | Zero maintenance | Misses deep review value | If cognitive skills suffice |

### C7. Multi-Orchestrator Pattern

**Recommended approach:** `onboard-repo` orchestrator

Flow: review-codebase (understand) → review-architecture (identify issues) → generate-standard-readme (document) → write-agents-entry (establish Agent contract)

| Alternative | Pros | Cons | Best for |
| :--- | :--- | :--- | :--- |
| **A: onboard-repo (recommended)** | High-frequency scenario; demonstrates skill composition | Needs cross-skill data passing format | Demonstration value |
| B: quality-gate | Directly supports CI/CD | Overlaps with run-repair-loop | CI-focused |
| C: Protocol first, orchestrators later | One-time investment benefits all | May over-engineer | Spec-purist approach |

### C8. Skill Chain & Workflow Protocol

**Recommended approach:** Lightweight I/O contracts

- Add optional fields to spec: `input_schema` and `output_schema`
- Define standard intermediate artifact formats (Findings List, Document Artifact, Diagnostic Report)
- Orchestrators auto-match upstream/downstream by schema

| Alternative | Pros | Cons | Best for |
| :--- | :--- | :--- | :--- |
| **A: I/O contracts in spec (recommended)** | Incremental; backward-compatible | Schema granularity needs careful design | Natural spec evolution |
| B: Event-driven model | Loose coupling; flexible | Too complex for pure-Markdown project | Platform with runtime |
| C: Explicit pipeline YAML | Declarative; easy to understand | New spec maintenance burden | Pipeline-centric workflows |

### D9. Claude Plugin Sync Strategy

**Recommended approach:** Define selection criteria + CI validation

- Plugin inclusion criteria: ASQM ≥ 18, non-atomic review skill, standalone usage value
- CI check: validate `marketplace.json` consistency with INDEX (like verify-registry)

| Alternative | Pros | Cons | Best for |
| :--- | :--- | :--- | :--- |
| **A: Selection criteria + CI (recommended)** | Principled; auto-prevents staleness | Need to maintain criteria | Governed approach |
| B: Expose all 28 skills | Maximum coverage | Atomic review skills add noise | Simplicity |
| C: Tiered exposure (Core + Extended) | Good UX | Claude Plugin may not support tiers | If platform supports it |

### D10. Community Infrastructure

**Recommended approach:** Gradual community-readiness

- Phase 1 (now): CONTRIBUTING.md (references spec/skill.md), Issue templates (Bug / Feature / New Skill Request)
- Phase 2 (when contributors appear): PR template with Self-Check checklist, CHANGELOG.md
- Phase 3 (active community): CODEOWNERS, Discussion templates

| Alternative | Pros | Cons | Best for |
| :--- | :--- | :--- | :--- |
| **A: Gradual (recommended)** | Invest as needed | Requires discipline to phase | Solo → small team transition |
| B: Full setup at once | Complete | Empty files if no community | Projects expecting contributors |
| C: Stay as-is | Zero maintenance | Barrier for external contributors | Purely solo project |

### E11. Skill Version Lifecycle Strategy

**Recommended approach:** Decouple version number from lifecycle + convention

- Version number (SemVer): reflects content maturity; `0.x.x` = unstable API, `1.0.0+` = stable contract
- ASQM status: reflects quality score (validated / experimental / archive_candidate)
- Add "Stability" column to INDEX.md: experimental / stable / mature
- Convention: validated skills at `0.x.x` should be upgraded to `1.0.0` when contract stabilizes

| Alternative | Pros | Cons | Best for |
| :--- | :--- | :--- | :--- |
| **A: Decouple + convention (recommended)** | Clear; two dimensions serve distinct purposes | One more field to maintain in INDEX | Pragmatic approach |
| B: Version = status | Simple; one glance | May force premature 1.0.0 | Strict versioning |
| C: lifecycle YAML field | Machine-readable | Overlaps with ASQM status | Automation-heavy |

### E12. Testable Specification (Executable Verification)

**Recommended approach:** Progressive spec verification scripts + JSON Schema

**Script `verify-skill-structure.mjs`** checks:

- YAML metadata completeness (name, description, tags, version, license)
- Required headings (Purpose, Core Objective, Use Cases, Behavior, I/O, Restrictions, Self-Check, Examples)
- Core Objective sub-sections (Primary Goal, Success Criteria, Acceptance Test)
- Success Criteria count: 3-6 items
- Name matches directory name
- Name format: 1-64 chars, kebab-case, no consecutive hyphens

**JSON Schema for YAML metadata** validates:

- Field types and constraints
- Tag values against INDEX tag system
- Version format (SemVer)
- Name format regex

| Alternative | Pros | Cons | Best for |
| :--- | :--- | :--- | :--- |
| **A+B: Script + JSON Schema (recommended)** | Covers structural + metadata; industrial tooling | Semantic checks still need human/LLM | Comprehensive |
| A: Custom script only | Full control | Reinvents schema validation | Quick start |
| C: LLM-assisted audit | Handles semantic checks | Non-deterministic; costly; not CI-friendly | Manual audits |

## Implementation Phases

Ordered by dependency and value:

### Phase 1: Foundation (Infrastructure)

```
E12 Testable Spec  →  A1 CI/CD Automation  →  A2 Quality Gates
```

Build checking capability first, then put it in CI, then automate quality assessment.

**Deliverables:**

- `scripts/verify-skill-structure.mjs`
- `schemas/skill-metadata.json`
- `.github/workflows/pr-check.yml`
- `.github/workflows/audit.yml`

### Phase 2: Capability Expansion

```
E11 Lifecycle Strategy (define conventions before adding new skills)
B3  review-typescript  →  B4 review-react
```

Establish lifecycle conventions, then build the frontend review chain (TS language + React framework).

**Deliverables:**

- Updated INDEX.md with Stability column
- `skills/review-typescript/`
- `skills/review-react/`

### Phase 3: Composition Upgrade

```
C8 I/O Contract Protocol  →  C7 onboard-repo Orchestrator
B5 Domain-level library review (review-orm-usage, etc.)
```

Define the protocol first, then build orchestrators on top of it.

**Deliverables:**

- Spec amendment: optional `input_schema` / `output_schema` fields
- `skills/onboard-repo/`
- `skills/review-orm-usage/`

### Phase 4: Ecosystem Maturity

```
D9  Plugin Sync Strategy
D10 Community Infrastructure Phase 1
```

**Deliverables:**

- Plugin selection criteria document
- CI check for `marketplace.json` sync
- `CONTRIBUTING.md`
- `.github/ISSUE_TEMPLATE/` (bug, feature, new-skill)

## Trade-offs Considered

| Direction | Chosen approach | Key trade-off |
| :--- | :--- | :--- |
| CI/CD | Minimal + dogfood | Value vs. overhead for pure-Markdown project |
| Language expansion | TS/JS priority | Breadth vs. depth; chose highest-impact language |
| Framework expansion | React first | Market share vs. chain completeness |
| Library review | Domain-based | Generality vs. library-specific depth |
| Orchestrators | onboard-repo | Demo value vs. CI integration (quality-gate) |
| Skill chains | I/O contracts | Simplicity vs. event-driven flexibility |
| Plugin sync | Selection criteria | Curation quality vs. full exposure |
| Community | Gradual | Investment vs. actual contributor demand |
| Lifecycle | Convention-based | Clarity vs. additional maintenance |
| Spec testing | Script + Schema | Coverage vs. semantic check limitations |

## Acceptance Criteria

- [x] Phase 1 deliverables: spec verification scripts and CI workflows operational
- [x] Phase 2 deliverables: review-typescript and review-react published and audited
- [x] Phase 3 deliverables: I/O contract protocol defined; onboard-repo orchestrator functional
- [x] Phase 4 deliverables: Plugin sync automated; CONTRIBUTING.md and Issue templates live
- [x] All new skills pass ASQM validation (quality ≥ 17)
- [x] No regression in existing skill quality or registry sync
