# Skill Composition Graph

This document describes how skills compose into orchestration chains, governance workflows, and development pipelines. It is for human and Agent reading only; Skills.sh and the manifest do not depend on it. For the canonical skill list, see [INDEX.md](./INDEX.md) and [manifest.json](../manifest.json). For scenario-first routing, see [scenario-map.md](./scenario-map.md).

---

## 1. Skill types

Atomic review skills are grouped by dimension:

| Type | Description | Skills |
| :--- | :--- | :--- |
| **Scope** | What to review: current change (diff) or current state (paths/repo). | [review-diff](./review-diff/SKILL.md), [review-codebase](./review-codebase/SKILL.md) |
| **Language** | Language and runtime conventions. | [review-dotnet](./review-dotnet/SKILL.md), [review-java](./review-java/SKILL.md), [review-go](./review-go/SKILL.md), [review-php](./review-php/SKILL.md), [review-powershell](./review-powershell/SKILL.md), [review-python](./review-python/SKILL.md), [review-sql](./review-sql/SKILL.md), [review-typescript](./review-typescript/SKILL.md) |
| **Framework** | Application framework conventions. | [review-vue](./review-vue/SKILL.md), [review-react](./review-react/SKILL.md); *(reserved: review-aspnetcore, review-nextjs, etc.)* |
| **Library** | Key library usage and pitfalls. | [review-orm-usage](./review-orm-usage/SKILL.md); *(reserved: review-http-client-usage, etc.)* |
| **Cognitive** | Cross-cutting concerns: security, performance, architecture, testing. | [review-security](./review-security/SKILL.md), [review-performance](./review-performance/SKILL.md), [review-architecture](./review-architecture/SKILL.md), [review-testing](./review-testing/SKILL.md) |
| **Meta** | Orchestration only; no analysis. | [review-code](./review-code/SKILL.md) |

---

## 2. Execution order

When running a **full** code review (via [review-code](./review-code/SKILL.md)), the execution order is:

1. **Scope** → choose one: `review-diff` (current change) or `review-codebase` (given paths/repo).
2. **Language** → choose one or none: `review-dotnet`, `review-java`, `review-go`, `review-php`, `review-powershell`, `review-python`, `review-sql`, `review-typescript` (by project).
3. **Framework** → optional: `review-vue`, `review-react`, or future framework skills.
4. **Library** → optional: `review-orm-usage` or future library skills.
5. **Cognitive** → run in order: `review-security`, then `review-performance`, then `review-architecture`, then `review-testing` (and future: reliability, maintainability).

All findings from the steps above are **aggregated** into a single report (same finding format: Location, Category, Severity, Title, Description, Suggestion).

---

## 3. Composition diagram

```mermaid
flowchart LR
  subgraph meta [Meta]
    review_code[review-code]
  end
  subgraph scope [Scope]
    review_diff[review-diff]
    review_codebase[review-codebase]
  end
  subgraph lang [Language]
    review_dotnet[review-dotnet]
    review_java[review-java]
    review_go[review-go]
    review_php[review-php]
    review_powershell[review-powershell]
    review_python[review-python]
    review_sql[review-sql]
    review_typescript[review-typescript]
  end
  subgraph fw [Framework]
    review_vue[review-vue]
    review_react[review-react]
  end
  subgraph lib [Library]
    review_orm[review-orm-usage]
  end
  subgraph cognitive [Cognitive]
    review_security[review-security]
    review_perf[review-performance]
    review_arch[review-architecture]
    review_testing[review-testing]
  end
  review_code --> review_diff
  review_code --> review_codebase
  review_code --> review_dotnet
  review_code --> review_java
  review_code --> review_go
  review_code --> review_php
  review_code --> review_powershell
  review_code --> review_python
  review_code --> review_sql
  review_code --> review_typescript
  review_code --> review_vue
  review_code --> review_react
  review_code --> review_orm
  review_code --> review_security
  review_code --> review_perf
  review_code --> review_arch
  review_code --> review_testing
  review_diff --> aggregate[Aggregate findings]
  review_codebase --> aggregate
  review_dotnet --> aggregate
  review_java --> aggregate
  review_go --> aggregate
  review_php --> aggregate
  review_powershell --> aggregate
  review_python --> aggregate
  review_sql --> aggregate
  review_typescript --> aggregate
  review_vue --> aggregate
  review_react --> aggregate
  review_orm --> aggregate
  review_security --> aggregate
  review_perf --> aggregate
  review_arch --> aggregate
  review_testing --> aggregate
```

---

## 4. Finding format (shared)

Every atomic skill emits findings in this format so [review-code](./review-code/SKILL.md) can merge them:

- **Location**: `path/to/file.ext` (optional line or range)
- **Category**: scope | language-\* | framework-\* | library-\* | cognitive-\*
- **Severity**: critical | major | minor | suggestion
- **Title**: Short one-line summary
- **Description**: 1–3 sentences
- **Suggestion**: Concrete fix or improvement (optional)

---

## 5. Quick reference

| Skill | Type | Input | Output |
| :--- | :--- | :--- | :--- |
| [review-diff](./review-diff/SKILL.md) | scope | git diff | Findings (Category=scope) |
| [review-codebase](./review-codebase/SKILL.md) | scope | paths/dirs/repo | Findings (Category=scope) |
| [review-dotnet](./review-dotnet/SKILL.md) | language | code scope | Findings (Category=language-dotnet) |
| [review-java](./review-java/SKILL.md) | language | code scope | Findings (Category=language-java) |
| [review-go](./review-go/SKILL.md) | language | code scope | Findings (Category=language-go) |
| [review-php](./review-php/SKILL.md) | language | code scope | Findings (Category=language-php) |
| [review-powershell](./review-powershell/SKILL.md) | language | code scope | Findings (Category=language-powershell) |
| [review-python](./review-python/SKILL.md) | language | code scope | Findings (Category=language-python) |
| [review-sql](./review-sql/SKILL.md) | language | SQL/code scope | Findings (Category=language-sql) |
| [review-typescript](./review-typescript/SKILL.md) | language | code scope | Findings (Category=language-typescript) |
| [review-vue](./review-vue/SKILL.md) | framework | code scope | Findings (Category=framework-vue) |
| [review-react](./review-react/SKILL.md) | framework | code scope | Findings (Category=framework-react) |
| [review-orm-usage](./review-orm-usage/SKILL.md) | library | code scope | Findings (Category=library-orm) |
| [review-security](./review-security/SKILL.md) | cognitive | code scope | Findings (Category=cognitive-security) |
| [review-performance](./review-performance/SKILL.md) | cognitive | code scope | Findings (Category=cognitive-performance) |
| [review-architecture](./review-architecture/SKILL.md) | cognitive | code scope | Findings (Category=cognitive-architecture) |
| [review-testing](./review-testing/SKILL.md) | cognitive | code scope | Findings (Category=cognitive-testing) |
| [review-code](./review-code/SKILL.md) | meta | user intent + scope | Single aggregated report |

---

## 6. Non-review composition chains

Beyond code review, skills compose into three additional pipelines:

### 6.1 Development lifecycle chain

Requirements → Design → Implementation → Review → Commit

```mermaid
flowchart LR
  analyze[analyze-requirements]
  brainstorm[brainstorm-design]
  review_code_node[review-code]
  commit[commit-work]
  run_tests[run-automated-tests]
  repair[run-repair-loop]

  analyze -->|validated requirements| brainstorm
  brainstorm -->|approved design| review_code_node
  review_code_node -->|findings| repair
  repair --> run_tests
  repair --> review_code_node
  run_tests -->|tests pass| commit
```

### 6.2 Repository onboarding chain

The [onboard-repo](./onboard-repo/SKILL.md) orchestrator runs skills in sequence:

```mermaid
flowchart LR
  onboard[onboard-repo]
  rcb[review-codebase]
  rarch[review-architecture]
  readme[generate-standard-readme]
  agents[write-agents-entry]
  discover[discover-skills]

  onboard --> rcb
  rcb --> rarch
  rarch --> readme
  readme --> agents
  agents --> discover
```

### 6.3 Governance and curation chain

```mermaid
flowchart LR
  curate[curate-skills]
  refine[refine-skill-design]
  readme_gen[generate-standard-readme]
  bootstrap[bootstrap-project-documentation]
  install[install-rules]

  curate -->|ASQM findings| refine
  refine -->|optimized SKILL.md| readme_gen
  bootstrap --> readme_gen
  install -.->|rules for quality| curate
```

### 6.4 Project governance loop chain

```mermaid
flowchart LR
  loop[project-cognitive-loop]
  req[analyze-requirements]
  design[brainstorm-design]
  align[execution-alignment]
  docreadiness[documentation-readiness]
  repair[run-repair-loop]

  loop --> req
  loop --> design
  loop --> align
  loop --> docreadiness
  align -->|active defects| repair
  docreadiness -->|doc gaps| req
  docreadiness -->|architecture gap| design
```

### 6.5 Quick reference (non-review)

| Skill | Chain | Input | Output |
| :--- | :--- | :--- | :--- |
| [analyze-requirements](./analyze-requirements/SKILL.md) | lifecycle | vague intent | validated requirements doc |
| [brainstorm-design](./brainstorm-design/SKILL.md) | lifecycle | validated requirements | approved design doc |
| [commit-work](./commit-work/SKILL.md) | lifecycle | staged changes | git commits |
| [run-automated-tests](./run-automated-tests/SKILL.md) | lifecycle | repo path | test execution results |
| [run-repair-loop](./run-repair-loop/SKILL.md) | lifecycle | repo + scope | converged clean state |
| [execution-alignment](./execution-alignment/SKILL.md) | lifecycle | completed task context | execution alignment report |
| [documentation-readiness](./documentation-readiness/SKILL.md) | lifecycle | docs scope + mapping | documentation readiness report + minimal fill plan |
| [project-cognitive-loop](./project-cognitive-loop/SKILL.md) | lifecycle | trigger + project context | cycle governance report |
| [onboard-repo](./onboard-repo/SKILL.md) | onboarding | repo path | onboarding report |
| [curate-skills](./curate-skills/SKILL.md) | governance | skills directory | ASQM audit report |
| [refine-skill-design](./refine-skill-design/SKILL.md) | governance | SKILL.md | optimized SKILL.md |
| [generate-standard-readme](./generate-standard-readme/SKILL.md) | governance | project context | standardized README |
| [write-agents-entry](./write-agents-entry/SKILL.md) | onboarding | project context | AGENTS.md |
| [discover-skills](./discover-skills/SKILL.md) | onboarding | capability gaps | skill recommendations |
| [decontextualize-text](./decontextualize-text/SKILL.md) | standalone | private text | generic text |
| [generate-github-workflow](./generate-github-workflow/SKILL.md) | standalone | workflow requirements | GitHub Actions YAML |
| [bootstrap-project-documentation](./bootstrap-project-documentation/SKILL.md) | governance | project directory | documentation tree |
| [install-rules](./install-rules/SKILL.md) | governance | source rules | IDE rule files |
