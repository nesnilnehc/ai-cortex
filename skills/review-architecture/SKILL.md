---
name: review-architecture
description: "Review code for architecture: module and layer boundaries, dependency direction, single responsibility, cyclic dependencies, interface stability, and coupling. Cognitive-only atomic skill; output is a findings list."
tags: [eng-standards]
related_skills: [review-diff, review-codebase, review-code]
version: 1.0.0
license: MIT
recommended_scope: project
metadata:
  author: ai-cortex
input_schema:
  type: code-scope
  description: Source files or directories to review
output_schema:
  type: findings-list
  description: Zero or more findings with location, category, severity, and suggestion
---

# Skill: Review Architecture

## Purpose

Review code for **architecture** concerns only. Do not define scope (diff vs codebase) or perform language/framework/security analysis; those are separate atomic skills. Emit a **findings list** in the standard format for aggregation. Focus on module and layer boundaries, dependency direction, single responsibility, cyclic dependencies, interface stability, and coupling and extension points.

---

## Core Objective

**Primary Goal**: Produce an architecture-focused findings list covering module/layer boundaries, dependency direction, single responsibility, cyclic dependencies, interface stability, and coupling for the given code scope.

**Success Criteria** (ALL must be met):

1. ✅ **Architecture-only scope**: Only architecture dimensions are reviewed; no scope selection, language/framework conventions, security, or performance analysis performed
2. ✅ **All six architecture dimensions covered**: Module/layer boundaries, dependency direction, single responsibility, cyclic dependencies, interface stability, and coupling are assessed where relevant
3. ✅ **Findings format compliant**: Each finding includes Location, Category (`cognitive-architecture`), Severity, Title, Description, and optional Suggestion
4. ✅ **Location-precise references**: All findings reference specific modules, packages, or files (not vague descriptions)
5. ✅ **Actionable output**: Each finding provides a concrete refactoring suggestion or improvement direction

**Acceptance Test**: Does the output contain an architecture findings list covering all relevant structural dimensions with specific module/file references and actionable refactoring suggestions?

---

## Scope Boundaries

**This skill handles**:
- Module and layer boundary clarity (API, domain, data layer separation)
- Dependency direction analysis (inward toward domain, stable abstractions)
- Single responsibility assessment per module/class
- Cyclic dependency detection and break points
- Interface stability and leaking implementation details
- Coupling analysis and extension point design

**This skill does NOT handle**:
- Scope selection (deciding which files/paths to analyze) — scope is provided by the caller
- Language/framework convention analysis — use `review-dotnet`, `review-java`, `review-go`, etc.
- Security review — use `review-security`
- Performance review — use `review-performance`
- Current-state codebase review combining all dimensions — use `review-codebase`
- Full orchestrated review — use `review-code`

**Handoff point**: When all architecture findings are emitted, hand off to `review-code` orchestrator for aggregation, or deliver directly to the user for architecture-focused sessions. For deep codebase audits, suggest also running `review-codebase`.

---

## Use Cases

- **Orchestrated review**: Used as a cognitive step when [review-code](../review-code/SKILL.md) runs scope → language → framework → library → cognitive.
- **Architecture-focused review**: When the user wants only boundaries, dependencies, and structure checked.
- **Refactor or onboarding**: Understand and critique current structure for planning or documentation.

**When to use**: When the task includes architecture or design review. Scope and code scope are determined by the caller or user.

---

## Behavior

### Scope of this skill

- **Analyze**: Architecture dimensions in the **given code scope** (files or diff provided by the caller). Do not decide scope; accept the code range as input. For large scope, consider layers or modules and summarize.
- **Do not**: Perform scope selection, language/framework conventions, or security review. Focus only on architecture and structure.

### Review checklist (architecture dimension only)

1. **Module and layer boundaries**: Are module/service boundaries clear? Are layers (e.g. API, domain, data) respected? Do high-level modules avoid depending on low-level details?
2. **Dependency direction**: Do dependencies point in the intended direction (e.g. inward toward domain, or toward stable abstractions)? No reverse or circular dependency direction at module level.
3. **Single responsibility**: Does each module/class have one clear responsibility? Are boundaries cohesive?
4. **Cyclic dependencies**: Are there cycles between modules, packages, or components? Suggest break points (e.g. extract interface, move shared code).
5. **Interface stability**: Are public APIs and interfaces stable and minimal? Are implementation details leaking across boundaries?
6. **Coupling and extension points**: Is coupling to concrete types or frameworks minimized where extension is expected? Are extension points (e.g. plugins, strategies) clear?

### Tone and references

- **Professional and technical**: Reference specific locations (file, module, or package). Emit findings with Location, Category, Severity, Title, Description, Suggestion.

---

## Input & Output

### Input

- **Code scope**: Files or directories (or diff) already selected by the user or scope skill. This skill does not decide scope; it reviews the provided code for architecture only.

### Output

- Emit zero or more **findings** in the format defined in **Appendix: Output contract**.
- Category for this skill is **cognitive-architecture**.

---

## Restrictions

### Hard Boundaries

- **Do not** perform scope selection, language, framework, or security review. Stay within architecture dimensions.
- **Do not** give conclusions without specific locations or actionable suggestions.
- **Do not** assume a specific architecture style (e.g. clean/hexagonal) unless the project states it; evaluate against general boundaries and dependency principles.

### Skill Boundaries

**Do NOT do these** (other skills handle them):
- Do NOT select or define the code scope — scope is determined by the caller or `review-code`
- Do NOT perform language/framework convention analysis — use `review-dotnet`, `review-java`, `review-go`, etc.
- Do NOT perform security or performance review — use `review-security` or `review-performance`
- Do NOT assume a specific architecture pattern (clean, hexagonal, etc.) unless explicitly stated

**When to stop and hand off**:
- When all architecture findings are emitted, hand off to `review-code` for aggregation in an orchestrated review
- When the user needs a full review (scope + language + cognitive), redirect to `review-code`
- When comprehensive codebase state review is needed beyond architecture, redirect to `review-codebase`

---

## Self-Check

### Core Success Criteria

- [ ] **Architecture-only scope**: Only architecture dimensions are reviewed; no scope selection, language/framework conventions, security, or performance analysis performed
- [ ] **All six architecture dimensions covered**: Module/layer boundaries, dependency direction, single responsibility, cyclic dependencies, interface stability, and coupling are assessed where relevant
- [ ] **Findings format compliant**: Each finding includes Location, Category (`cognitive-architecture`), Severity, Title, Description, and optional Suggestion
- [ ] **Location-precise references**: All findings reference specific modules, packages, or files (not vague descriptions)
- [ ] **Actionable output**: Each finding provides a concrete refactoring suggestion or improvement direction

### Process Quality Checks

- [ ] Was only the architecture dimension reviewed (no scope/language/security)?
- [ ] Are boundaries, dependency direction, responsibility, cycles, interfaces, and coupling covered where relevant?
- [ ] Is each finding emitted with Location, Category=cognitive-architecture, Severity, Title, Description, and optional Suggestion?
- [ ] Are module/package/file references precise enough to act on?

### Acceptance Test

Does the output contain an architecture findings list covering all relevant structural dimensions with specific module/file references and actionable refactoring suggestions?

---

## Examples

### Example 1: Reverse dependency

- **Input**: Domain layer imports from infrastructure (e.g. DB driver) directly.
- **Expected**: Emit a finding for dependency direction; suggest interface in domain and implementation in infrastructure. Category = cognitive-architecture.

### Example 2: Cycle between packages

- **Input**: Package A imports B, B imports C, C imports A.
- **Expected**: Emit finding(s) identifying the cycle and suggest break point (e.g. extract shared interface or type to a neutral package). Category = cognitive-architecture.

### Edge case: Small or single-file scope

- **Input**: Single file or very small module.
- **Expected**: Review internal structure (responsibility, coupling to external types); if scope is too small for module-level concerns, state that and emit only findings that apply (e.g. single responsibility, interface clarity).

---

## Appendix: Output contract

Each finding MUST follow the standard findings format:

| Element | Requirement |
| :--- | :--- |
| **Location** | `path/to/file.ext` or module/package name (optional line or range). |
| **Category** | `cognitive-architecture`. |
| **Severity** | `critical` \| `major` \| `minor` \| `suggestion`. |
| **Title** | Short one-line summary. |
| **Description** | 1–3 sentences. |
| **Suggestion** | Concrete fix or improvement (optional). |

Example:

```markdown
- **Location**: `pkg/domain/order.go`
- **Category**: cognitive-architecture
- **Severity**: major
- **Title**: Domain imports infrastructure directly
- **Description**: Order service imports DB driver; domain should not depend on infrastructure.
- **Suggestion**: Define repository interface in domain; implement in infrastructure and inject.
```
