# Skills Index

**Canonical capability list**: definitive skill registry (name, tags, version, purpose) and tagging/versioning policy. For ASQM quality, lifecycle status, overlap detection and ecosystem position (from curate-skills), see [ASQM_AUDIT.md](./ASQM_AUDIT.md) or each skill's `agent.yaml`.

This document is the central skills index for **AI Cortex** (the agent-first, governance-ready capability inventory; repo [ai-cortex](https://github.com/nesnilnehc/ai-cortex)). It defines standardized SKILL metadata, the tagging system, and versioning policy. Install with `npx skills add nesnilnehc/ai-cortex`; compatible with [skills.sh](https://skills.sh) and [SkillsMP](https://skillsmp.com).

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
| [decontextualize-text](./decontextualize-text/SKILL.md) | writing, security, privacy, generalization | `1.3.0` | stable | Remove context dependency and enable cross-boundary knowledge flow. |
| [generate-standard-readme](./generate-standard-readme/SKILL.md) | documentation, eng-standards, devops, writing | `1.2.0` | stable | Give project assets a standardized "first face". |
| [discover-skills](./discover-skills/SKILL.md) | automation, infrastructure, generalization | `1.3.0` | stable | Discover and recommend relevant skills; suggest install commands to fill capability gaps. |
| [refine-skill-design](./refine-skill-design/SKILL.md) | writing, eng-standards, meta-skill, optimization | `1.2.0` | stable | Audit and refactor SKILLs to meet production-grade standards. |
| [write-agents-entry](./write-agents-entry/SKILL.md) | documentation, eng-standards | `1.0.0` | stable | Write or revise AGENTS.md per the skill's embedded output contract; establish Agent entry and behavior. |
| [review-code](./review-code/SKILL.md) | eng-standards | `2.6.0` | mature | Orchestrator: run scope → language → framework → library → cognitive review skills in order, aggregate findings, and derive risk signals centrally. |
| [review-codebase](./review-codebase/SKILL.md) | eng-standards | `1.3.0` | stable | Review architecture, design, and tech debt for a given scope; focus on boundaries, patterns, and overall quality. |
| [review-diff](./review-diff/SKILL.md) | eng-standards | `1.3.0` | stable | Review only git diff (staged + unstaged, optional untracked) for impact, regression, correctness, compatibility, and side effects; scope-only atomic skill. |
| [review-dotnet](./review-dotnet/SKILL.md) | eng-standards | `1.0.0` | stable | Review .NET (C#/F#) for language and runtime conventions; language-only atomic skill. |
| [review-java](./review-java/SKILL.md) | eng-standards | `1.0.0` | stable | Review Java for language and runtime conventions; language-only atomic skill. |
| [review-go](./review-go/SKILL.md) | eng-standards | `1.0.0` | stable | Review Go for language and runtime conventions; language-only atomic skill. |
| [review-php](./review-php/SKILL.md) | eng-standards | `1.0.0` | stable | Review PHP for language and runtime conventions; language-only atomic skill. |
| [review-powershell](./review-powershell/SKILL.md) | eng-standards | `1.0.0` | stable | Review PowerShell for language and runtime conventions; language-only atomic skill. |
| [review-python](./review-python/SKILL.md) | eng-standards | `1.0.0` | stable | Review Python for language and runtime conventions; language-only atomic skill. |
| [review-sql](./review-sql/SKILL.md) | eng-standards | `1.0.0` | stable | Review SQL and query code for injection, performance, transactions, and portability; language-only atomic skill. |
| [review-vue](./review-vue/SKILL.md) | eng-standards | `1.0.0` | stable | Review Vue 3 for Composition API, reactivity, components, state, and performance; framework-only atomic skill. |
| [review-security](./review-security/SKILL.md) | eng-standards, security | `1.0.0` | stable | Review code for security: injection, sensitive data, auth, dependencies, secrets, crypto; cognitive-only atomic skill. |
| [review-performance](./review-performance/SKILL.md) | eng-standards, optimization | `1.0.0` | stable | Review code for performance: complexity, query efficiency, I/O, memory, contention, caching, and regression risk; cognitive-only atomic skill. |
| [review-architecture](./review-architecture/SKILL.md) | eng-standards | `1.0.0` | stable | Review code for architecture: boundaries, dependency direction, cycles, interfaces, coupling; cognitive-only atomic skill. |
| [review-testing](./review-testing/SKILL.md) | eng-standards | `1.0.0` | stable | Review code for testing: test existence, coverage adequacy, test quality, edge-case coverage, and maintainability; cognitive-only atomic skill. |
| [generate-github-workflow](./generate-github-workflow/SKILL.md) | devops, eng-standards | `1.0.0` | stable | Create GitHub Actions workflows per the skill's output spec (CI, PR checks, release); includes Go + Docker + GoReleaser appendix. |
| [curate-skills](./curate-skills/SKILL.md) | meta-skill, eng-standards, documentation | `1.0.0` | stable | Evaluate, score, tag, and normalize all Skills; write agent.yaml and README per skill, detect overlaps, produce SUMMARY or chat summary. |
| [install-rules](./install-rules/SKILL.md) | automation, infrastructure, eng-standards | `1.2.0` | stable | Install rules from this project or a specified Git repo into Cursor or Trae IDE. |
| [run-automated-tests](./run-automated-tests/SKILL.md) | automation, devops, eng-standards | `0.1.0` | experimental | Analyze a target repository's automated testing approach and run the most appropriate test command(s) safely. |
| [run-repair-loop](./run-repair-loop/SKILL.md) | automation, devops, eng-standards, optimization | `0.1.0` | experimental | Iteratively review, run tests, and apply targeted fixes until issues are resolved (or a stop condition is reached). |
| [bootstrap-project-documentation](./bootstrap-project-documentation/SKILL.md) | documentation, eng-standards, writing | `1.1.1` | stable | Bootstrap or adapt project docs from project-documentation-template; Initialize or Adjust modes; repeatable; strict kebab-case naming. |
| [commit-work](./commit-work/SKILL.md) | git, workflow, eng-standards, automation | `2.0.0` | mature | Create high-quality git commits with AI Cortex governance - review changes, split logically, write clear messages (Conventional Commits), sync with INDEX/manifest. |
| [brainstorm-design](./brainstorm-design/SKILL.md) | writing, eng-standards, documentation | `1.0.0` | stable | Transform rough ideas into validated design documents through structured dialogue. Core goal: produce approved design doc with alternatives analysis before any implementation. |
| [review-typescript](./review-typescript/SKILL.md) | eng-standards | `1.0.0` | stable | Review TypeScript and JavaScript code for language and runtime conventions including type safety, async patterns, error handling, module design, and runtime correctness; language-only atomic skill. |
| [review-react](./review-react/SKILL.md) | eng-standards | `1.0.0` | stable | Review React code for component design, hooks correctness, state management, rendering performance, and accessibility; framework-only atomic skill. |
| [onboard-repo](./onboard-repo/SKILL.md) | eng-standards, documentation, automation | `1.0.0` | stable | Orchestrator: run review-codebase → review-architecture → generate-standard-readme → write-agents-entry → discover-skills in order, aggregate outputs into one onboarding report. |
| [review-orm-usage](./review-orm-usage/SKILL.md) | eng-standards, optimization | `1.0.0` | stable | Review ORM usage patterns for N+1 queries, connection management, migration safety, transaction handling, and query efficiency; library-level atomic skill. |
| [analyze-requirements](./analyze-requirements/SKILL.md) | writing, eng-standards, documentation | `1.0.0` | stable | Transform vague intent into validated, testable requirements through diagnostic state progression and structured dialogue; problem-first, no design before validation. |

---

## 4. Scheduling and extension

When scheduling a Skill, the Agent should resolve `INDEX.md` first to understand the capability graph and use `related_skills` for chained or multi-step tasks.
