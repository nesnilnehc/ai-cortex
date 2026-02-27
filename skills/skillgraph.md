# Code Review Skills: Composition Graph

This document describes how the **code review** skills compose. It is for human and Agent reading only; Skills.sh and the manifest do not depend on it. For the canonical skill list, see [INDEX.md](./INDEX.md) and [manifest.json](../manifest.json).

---

## 1. Skill types

Atomic review skills are grouped by dimension:

| Type | Description | Skills |
| :--- | :--- | :--- |
| **Scope** | What to review: current change (diff) or current state (paths/repo). | [review-diff](./review-diff/SKILL.md), [review-codebase](./review-codebase/SKILL.md) |
| **Language** | Language and runtime conventions. | [review-dotnet](./review-dotnet/SKILL.md), [review-java](./review-java/SKILL.md), [review-go](./review-go/SKILL.md), [review-php](./review-php/SKILL.md), [review-powershell](./review-powershell/SKILL.md), [review-python](./review-python/SKILL.md), [review-sql](./review-sql/SKILL.md) |
| **Framework** | Application framework conventions. | [review-vue](./review-vue/SKILL.md); *(reserved: review-aspnetcore, review-react, etc.)* |
| **Library** | Key library usage and pitfalls. | *(reserved: review-entityframework, etc.)* |
| **Cognitive** | Cross-cutting concerns: security, performance, architecture, testing. | [review-security](./review-security/SKILL.md), [review-performance](./review-performance/SKILL.md), [review-architecture](./review-architecture/SKILL.md), [review-testing](./review-testing/SKILL.md) |
| **Meta** | Orchestration only; no analysis. | [review-code](./review-code/SKILL.md) |

---

## 2. Execution order

When running a **full** code review (via [review-code](./review-code/SKILL.md)), the execution order is:

1. **Scope** → choose one: `review-diff` (current change) or `review-codebase` (given paths/repo).
2. **Language** → choose one or none: `review-dotnet`, `review-java`, `review-go`, `review-php`, `review-powershell`, `review-python`, `review-sql` (by project).
3. **Framework** → optional: `review-vue` or future framework skills.
4. **Library** → optional: future library skills (e.g. review-entityframework).
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
  end
  subgraph fw [Framework]
    review_vue[review-vue]
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
  review_code --> review_vue
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
  review_vue --> aggregate
  review_security --> aggregate
  review_perf --> aggregate
  review_arch --> aggregate
  review_testing --> aggregate
```

---

## 4. Finding format (shared)

Every atomic skill emits findings in this format so [review-code](./review-code/SKILL.md) can merge them:

- **Location**: `path/to/file.ext` (optional line or range)
- **Category**: scope | language-* | framework-* | library-* | cognitive-*
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
| [review-vue](./review-vue/SKILL.md) | framework | code scope | Findings (Category=framework-vue) |
| [review-security](./review-security/SKILL.md) | cognitive | code scope | Findings (Category=cognitive-security) |
| [review-performance](./review-performance/SKILL.md) | cognitive | code scope | Findings (Category=cognitive-performance) |
| [review-architecture](./review-architecture/SKILL.md) | cognitive | code scope | Findings (Category=cognitive-architecture) |
| [review-testing](./review-testing/SKILL.md) | cognitive | code scope | Findings (Category=cognitive-testing) |
| [review-code](./review-code/SKILL.md) | meta | user intent + scope | Single aggregated report |
