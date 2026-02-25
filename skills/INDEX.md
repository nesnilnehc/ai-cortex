# Skills Index

**Canonical capability list**: definitive skill registry (name, tags, version, purpose) and tagging/versioning policy. For ASQM quality, lifecycle status, overlap detection and ecosystem position (from curate-skills), see [ASQM_AUDIT.md](./ASQM_AUDIT.md) or each skill’s `agent.yaml`.

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

---

## 2. Versioning

This project follows **[Semantic Versioning (SemVer)](https://semver.org/)**.

- **MAJOR**: Breaking or major structural change to the SKILL.
- **MINOR**: New steps, interaction policy, or materially improved examples.
- **PATCH**: Typos, metadata tweaks, or reference updates.

---

## 3. Skill registry

| Skill name | Tags | Version | Purpose |
| :--- | :--- | :--- | :--- |
| [decontextualize-text](./decontextualize-text/SKILL.md) | writing, security, privacy, generalization | `1.3.0` | Remove context dependency and enable cross-boundary knowledge flow. |
| [generate-standard-readme](./generate-standard-readme/SKILL.md) | documentation, eng-standards, devops, writing | `1.2.0` | Give project assets a standardized “first face”. |
| [discover-skills](./discover-skills/SKILL.md) | automation, infrastructure, generalization | `1.3.0` | Discover and recommend relevant skills; suggest install commands to fill capability gaps. |
| [refine-skill-design](./refine-skill-design/SKILL.md) | writing, eng-standards, meta-skill, optimization | `1.2.0` | Audit and refactor SKILLs to meet production-grade standards. |
| [write-agents-entry](./write-agents-entry/SKILL.md) | documentation, eng-standards | `1.0.0` | Write or revise AGENTS.md per the skill’s embedded output contract; establish Agent entry and behavior. |
| [review-code](./review-code/SKILL.md) | eng-standards | `2.5.0` | Orchestrator: run scope → language → framework → library → cognitive review skills in order, aggregate findings, and derive risk signals centrally. |
| [review-codebase](./review-codebase/SKILL.md) | eng-standards | `1.3.0` | Review architecture, design, and tech debt for a given scope; focus on boundaries, patterns, and overall quality. |
| [review-diff](./review-diff/SKILL.md) | eng-standards | `1.3.0` | Review only git diff (staged + unstaged, optional untracked) for impact, regression, correctness, compatibility, and side effects; scope-only atomic skill. |
| [review-dotnet](./review-dotnet/SKILL.md) | eng-standards | `1.0.0` | Review .NET (C#/F#) for language and runtime conventions; language-only atomic skill. |
| [review-java](./review-java/SKILL.md) | eng-standards | `1.0.0` | Review Java for language and runtime conventions; language-only atomic skill. |
| [review-go](./review-go/SKILL.md) | eng-standards | `1.0.0` | Review Go for language and runtime conventions; language-only atomic skill. |
| [review-powershell](./review-powershell/SKILL.md) | eng-standards | `1.0.0` | Review PowerShell for language and runtime conventions; language-only atomic skill. |
| [review-sql](./review-sql/SKILL.md) | eng-standards | `1.0.0` | Review SQL and query code for injection, performance, transactions, and portability; language-only atomic skill. |
| [review-vue](./review-vue/SKILL.md) | eng-standards | `1.0.0` | Review Vue 3 for Composition API, reactivity, components, state, and performance; framework-only atomic skill. |
| [review-security](./review-security/SKILL.md) | eng-standards, security | `1.0.0` | Review code for security: injection, sensitive data, auth, dependencies, secrets, crypto; cognitive-only atomic skill. |
| [review-performance](./review-performance/SKILL.md) | eng-standards, optimization | `1.0.0` | Review code for performance: complexity, query efficiency, I/O, memory, contention, caching, and regression risk; cognitive-only atomic skill. |
| [review-architecture](./review-architecture/SKILL.md) | eng-standards | `1.0.0` | Review code for architecture: boundaries, dependency direction, cycles, interfaces, coupling; cognitive-only atomic skill. |
| [generate-github-workflow](./generate-github-workflow/SKILL.md) | devops, eng-standards | `1.0.0` | Create GitHub Actions workflows per the skill’s output spec (CI, PR checks, release); includes Go + Docker + GoReleaser appendix. |
| [curate-skills](./curate-skills/SKILL.md) | meta-skill, eng-standards, documentation | `1.0.0` | Evaluate, score, tag, and normalize all Skills; write agent.yaml and README per skill, detect overlaps, produce SUMMARY or chat summary. |
| [install-rules](./install-rules/SKILL.md) | automation, infrastructure, eng-standards | `1.2.0` | Install rules from this project or a specified Git repo into Cursor or Trae IDE. |
| [run-automated-tests](./run-automated-tests/SKILL.md) | automation, devops, eng-standards | `0.1.0` | Analyze a target repository's automated testing approach and run the most appropriate test command(s) safely. |
| [run-repair-loop](./run-repair-loop/SKILL.md) | automation, devops, eng-standards, optimization | `0.1.0` | Iteratively review, run tests, and apply targeted fixes until issues are resolved (or a stop condition is reached). |
| [bootstrap-project-documentation](./bootstrap-project-documentation/SKILL.md) | documentation, eng-standards, writing | `1.0.0` | Bootstrap or adapt project docs from project-documentation-template; Initialize (empty) or Adjust (non-empty) modes. |

---

## 4. Scheduling and extension

When scheduling a Skill, the Agent should resolve `INDEX.md` first to understand the capability graph and use `related_skills` for chained or multi-step tasks.
