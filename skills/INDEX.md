# Skills Index

**Canonical capability list**: definitive skill registry (name, tags, version, purpose) and tagging/versioning policy. For ASQM quality, lifecycle status, overlap detection and ecosystem position (from curate-skills), see [ASQM_AUDIT.md](./ASQM_AUDIT.md) or each skill's `agent.yaml`.

This document is the central skills index for **AI Cortex** (the agent-first, governance-ready capability inventory; repo [ai-cortex](https://github.com/nesnilnehc/ai-cortex)). It defines standardized SKILL metadata, the tagging system, and versioning policy. Install with `npx skills add nesnilnehc/ai-cortex`; compatible with [skills.sh](https://skills.sh) and [SkillsMP](https://skillsmp.com).

**Scenario-first navigation**: See [scenario-map.md](./scenario-map.md) to pick skills by use case.

---

## 1. Tagging system

All SKILLs in this repo are tagged along the dimensions below to support task matching and scheduling by Agents.

| Tag | Description | Typical use |
| :--- | :--- | :--- |
| `writing` | Content creation and style | Docs, blogs, emails |
| `security` | Compliance and sensitive data | De-identification, anonymization, vulnerability notes |
| `privacy` | Privacy and data anonymization | Personal or organizational secrets |
| `documentation` | Standardized documentation | README, API docs, Wiki |
| `generalization` | Abstraction and generalization | Method extraction, jargon removal |
| `eng-standards` | Engineering standards and practices | Code review, architecture docs, infra config |
| `devops` | Delivery and operations automation | CI/CD docs, deployment |
| `meta-skill` | Design and refactor of skills/specs | SKILL audit, normalization, quality |
| `automation` | Automation and dynamic loading | Skill discovery, hot-load, batch ops |
| `infrastructure` | Infra and runtime capabilities | Discovery, loading, runtime support |
| `optimization` | Optimization and refactoring | Design and structure improvements |
| `git` | Git workflow and version control | Commits, branching, history |
| `workflow` | Development workflow orchestration | Multi-step processes, pipelines |

---

## 2. Versioning and stability

This project follows **[Semantic Versioning (SemVer)](https://semver.org/)**.

- **MAJOR**: Breaking or major structural change to the SKILL.
- **MINOR**: New steps, interaction policy, or materially improved examples.
- **PATCH**: Typos, metadata tweaks, or reference updates.

### Stability levels

Each skill has a **Stability** indicator that reflects contract maturity, independent of the ASQM quality score (which measures structural quality).

| Stability | Version convention | Meaning |
| :--- | :--- | :--- |
| `experimental` | `0.x.x` | API and behavior may change significantly between versions. |
| `stable` | `≥ 1.0.0` | Contract is settled; breaking changes require a major bump. |
| `mature` | `≥ 2.0.0` or long-stable `1.x` | Battle-tested; widely used; minimal churn expected. |

Convention: a skill at `0.x.x` with ASQM status "validated" should be upgraded to `1.0.0` once the contract stabilizes.

---

## 3. Skill registry

| Skill name | Tags | Version | Stability | Purpose |
| :--- | :--- | :--- | :--- | :--- |
| [decontextualize-text](./decontextualize-text/SKILL.md) | generalization, privacy, security, writing | `1.3.0` | stable | Convert text with private context or internal dependencies into generic, unbiased expressions that are standalone and reusable. Core goal - produce decontextualized text that preserves logic while removing organizational identifiers. Use for project handoff, open-source prep, methodology abstraction, cross-team sharing. |
| [generate-standard-readme](./generate-standard-readme/SKILL.md) | devops, documentation, eng-standards, writing | `1.2.0` | stable | Generate professional, governance-ready README with fixed structure. Core goal - produce standardized front-page documentation that explains purpose, usage, and contribution guidelines. Use for asset governance, audit, or unified documentation standards. |
| [discover-document-norms](./discover-document-norms/SKILL.md) | documentation, eng-standards, workflow | `1.0.0` | stable | Help users establish project-specific artifact norms (paths, naming, lifecycle) through dialogue and scanning. Core goal - produce docs/ARTIFACT_NORMS.md and optional .ai-cortex/artifact-norms.yaml. |
| [discover-skills](./discover-skills/SKILL.md) | automation, generalization, infrastructure | `1.3.0` | stable | Identify missing skills and recommend installations from AI Cortex or public skill catalogs. Core goal - provide top 1-3 skill matches with install commands for Agent capability gaps. Use when discovering capabilities or suggesting skills to fill gaps. |
| [refine-skill-design](./refine-skill-design/SKILL.md) | eng-standards, meta-skill, optimization, writing | `1.3.0` | stable | Audit and refactor existing SKILLs to meet spec compliance and LLM best practices. Use when improving drafts, fixing quality, or aligning to spec. |
| [write-agents-entry](./write-agents-entry/SKILL.md) | documentation, eng-standards | `1.0.0` | stable | Write or revise AGENTS.md per embedded output contract to establish project identity, authoritative sources, and behavioral expectations. Use when creating Agent entry for new projects, auditing existing AGENTS.md, or adopting the AI Cortex entry format. |
| [review-code](./review-code/SKILL.md) | eng-standards | `2.6.0` | mature | Orchestrate comprehensive code reviews by running scope, language, framework, library, and cognitive review skills in sequence, then aggregate findings into a unified report. |
| [review-codebase](./review-codebase/SKILL.md) | eng-standards | `1.3.0` | stable | Architecture and design review for specified files/dirs/repo. Covers tech debt, patterns, quality. Diff-only review use review-diff. Complements review-code (orchestrated). |
| [review-diff](./review-diff/SKILL.md) | eng-standards | `1.3.0` | stable | Review only git diff for impact, regression, correctness, compatibility, and side effects. Scope-only atomic skill; output is a findings list for aggregation. |
| [review-dotnet](./review-dotnet/SKILL.md) | eng-standards | `1.0.0` | stable | "Review .NET (C#/F#) code for language and runtime conventions: async/await, nullable, API versioning, IDisposable, LINQ, and testability. Language-only atomic skill; output is a findings list.". |
| [review-java](./review-java/SKILL.md) | eng-standards | `1.0.0` | stable | "Review Java code for language and runtime conventions: concurrency, exceptions, try-with-resources, API versioning, collections and Streams, NIO, and testability. Language-only atomic skill; output is a findings list.". |
| [review-go](./review-go/SKILL.md) | eng-standards | `1.0.0` | stable | "Review Go code for language and runtime conventions: concurrency, context usage, error handling, resource management, API stability, type semantics, and testability. Language-only atomic skill; output is a findings list.". |
| [review-php](./review-php/SKILL.md) | eng-standards | `1.0.0` | stable | "Review PHP code for language and runtime conventions: strict types, error handling, resource management, PSR standards, namespaces, null safety, generators, and testability. Language-only atomic skill; output is a findings list.". |
| [review-powershell](./review-powershell/SKILL.md) | eng-standards | `1.0.0` | stable | "Review PowerShell code for language and runtime conventions: advanced functions, parameter design, error handling, object pipeline behavior, compatibility, and testability. Language-only atomic skill; output is a findings list.". |
| [review-python](./review-python/SKILL.md) | eng-standards | `1.0.0` | stable | "Review Python code for language and runtime conventions: type hints, exceptions, async/await, context managers, dependencies, and testability. Language-only atomic skill; output is a findings list.". |
| [review-sql](./review-sql/SKILL.md) | eng-standards | `1.0.0` | stable | Review SQL and query code for injection risk, parameterization, indexing and performance, transactions, NULL and constraints, and dialect portability. Language-only atomic skill; output is a findings list. |
| [review-vue](./review-vue/SKILL.md) | eng-standards | `1.0.0` | stable | Review Vue 3 code for Composition API, reactivity, components, state (Pinia), routing, and performance. Framework-only atomic skill; output is a findings list. |
| [review-security](./review-security/SKILL.md) | eng-standards, security | `1.0.0` | stable | "Review code for security: injection, sensitive data, auth, dependencies, config, and crypto. Atomic skill; output is a findings list.". |
| [review-architecture](./review-architecture/SKILL.md) | eng-standards | `1.0.0` | stable | "Review code for architecture: module and layer boundaries, dependency direction, single responsibility, cyclic dependencies, interface stability, and coupling. Cognitive-only atomic skill; output is a findings list.". |
| [review-testing](./review-testing/SKILL.md) | eng-standards | `1.0.0` | stable | "Review code for testing: test existence, coverage adequacy, test quality and structure, edge-case and error-path coverage, and test maintainability. Cognitive-only atomic skill; output is a findings list.". |
| [generate-github-workflow](./generate-github-workflow/SKILL.md) | devops, eng-standards | `1.0.0` | stable | "GitHub Actions YAML with embedded output contract: security-first, minimal permissions, version pinning. For CI, release, PR checks. Differs from generic templates by spec compliance and auditability.". |
| [curate-skills](./curate-skills/SKILL.md) | documentation, eng-standards, meta-skill | `1.0.0` | stable | Govern skill inventory through ASQM scoring, lifecycle management, and overlap detection. Core goal - produce validated quality scores and normalized documentation for all skills in repository. |
| [install-rules](./install-rules/SKILL.md) | automation, eng-standards, infrastructure | `1.2.0` | stable | Install rules from source repo into Cursor or Trae IDE with explicit confirmation and conflict detection. Core goal - install rules to editor destinations with user approval before any write. |
| [review-performance](./review-performance/SKILL.md) | eng-standards, optimization | `1.0.0` | stable | "Review code for performance: complexity, database/query efficiency, I/O and network cost, memory and allocation behavior, concurrency contention, caching, and latency/throughput regressions. Cognitive-only atomic skill; output is a findings list.". |
| [run-automated-tests](./run-automated-tests/SKILL.md) | automation, devops, eng-standards | `1.0.0` | stable | Discover and execute repository test commands safely with evidence-based command selection and safety guardrails. |
| [run-repair-loop](./run-repair-loop/SKILL.md) | automation, devops, eng-standards, optimization | `1.1.0` | stable | Iteratively review changes, run automated tests, and apply targeted fixes until issues are resolved (or a stop condition is reached). |
| [bootstrap-docs](./bootstrap-docs/SKILL.md) | documentation, eng-standards, writing | `1.1.1` | stable | Bootstrap or adapt project docs using project-documentation-template. Core goal - produce structured lifecycle documentation aligned with enterprise template. Initialize (empty) or Adjust (non-empty); repeatable; strict kebab-case naming. |
| [capture-work-items](./capture-work-items/SKILL.md) | documentation, eng-standards, workflow, writing | `1.0.0` | stable | Capture requirements, bugs, or issues from free-form input into structured, persistent artifacts. Use when user wants to record a work item quickly without deep validation. |
| [commit-work](./commit-work/SKILL.md) | automation, eng-standards, git, workflow | `2.0.0` | mature | Create high-quality git commits with clear messages and logical scope. Core goal - produce reviewable commits following Conventional Commits format with pre-commit quality checks. |
| [brainstorm-design](./brainstorm-design/SKILL.md) | documentation, eng-standards, writing | `1.0.0` | stable | Transform rough ideas into validated design documents through structured dialogue before any implementation. Use when user has a vague idea needing concrete design. |
| [review-typescript](./review-typescript/SKILL.md) | eng-standards | `1.0.0` | stable | Review TypeScript/JavaScript code for type safety, async patterns, error handling, and module design. Atomic skill; output is a findings list. |
| [review-react](./review-react/SKILL.md) | eng-standards | `1.0.0` | stable | Review React code for component design, hooks correctness, state management, rendering performance, and accessibility. Framework-only atomic skill; output is a findings list. |
| [onboard-repo](./onboard-repo/SKILL.md) | automation, documentation, eng-standards | `1.0.0` | stable | Orchestrate repository onboarding by running codebase review, architecture assessment, README generation, and Agent entry setup in sequence. Meta skill; no analysis of its own. |
| [review-orm-usage](./review-orm-usage/SKILL.md) | eng-standards, optimization | `1.0.0` | stable | Review ORM usage patterns for N+1 queries, connection management, migration safety, transaction handling, and query efficiency. Library-level atomic skill; output is a findings list. |
| [analyze-requirements](./analyze-requirements/SKILL.md) | documentation, eng-standards, writing | `1.0.0` | stable | Transform vague intent into validated, testable requirements through diagnostic state progression and structured dialogue. Use when user has an idea, feature request, or problem statement that needs requirements clarification before design or implementation. |
| [align-planning](./align-planning/SKILL.md) | documentation, eng-standards, workflow | `1.3.0` | stable | Perform post-task traceback, drift detection, and top-down recalibration to keep planning (goals, requirements, milestones, roadmap) aligned with task execution. |
| [align-architecture](./align-architecture/SKILL.md) | documentation, eng-standards, workflow | `1.2.0` | stable | Verify architecture and design documents against code implementation; produce an Architecture Compliance Report when implementation diverges from ADR or design decisions. |
| [assess-doc-readiness](./assess-doc-readiness/SKILL.md) | documentation, eng-standards, workflow | `1.1.0` | stable | Assess doc evidence readiness across project layers, report gaps, and produce a minimum-fill plan to improve alignment reliability. |
| [run-checkpoint](./run-checkpoint/SKILL.md) | automation, eng-standards, workflow | `1.3.0` | stable | Analyze project state and produce next-action plan by running alignment, doc readiness, and output-driven follow-ups. Single-cycle report with executed steps and Recommended Next Tasks. |
| [validate-doc-artifacts](./validate-doc-artifacts/SKILL.md) | documentation, eng-standards, workflow | `1.0.0` | stable | Validate docs under project against artifact norms. Check paths, naming, front-matter for compliance. Output findings list for remediation. |
| [prune-content](./prune-content/SKILL.md) | documentation, eng-standards, optimization, workflow | `1.1.0` | stable | Identifies and archives obsolete project content based on user judgment or onboarding analysis. Invoke when user asks to clean up, archive, or audit repository content. |

---

## 4. Scheduling and extension

When scheduling a Skill, the Agent should resolve `INDEX.md` first to understand the capability graph and use `related_skills` for chained or multi-step tasks.
