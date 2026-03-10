---
name: review-powershell
description: "Review PowerShell code for language and runtime conventions: advanced functions, parameter design, error handling, object pipeline behavior, compatibility, and testability. Language-only atomic skill; output is a findings list."
tags: [eng-standards]
related_skills: [review-diff, review-codebase, review-code]
version: 1.0.0
license: MIT
recommended_scope: project
metadata:
  author: ai-cortex
triggers: [review powershell]
input_schema:
  type: code-scope
  description: Source files or directories to review
output_schema:
  type: findings-list
  description: Zero or more findings with location, category, severity, and suggestion
---

# Skill: Review PowerShell

## Purpose

Review code in **PowerShell** for **language and runtime conventions** only. Do not define scope (diff vs codebase) or perform security/architecture analysis; those are handled by scope and cognitive skills. Emit a **findings list** in the standard format for aggregation. Focus on advanced function design, parameter validation and binding, error handling semantics, object pipeline behavior, module/export and naming conventions, compatibility (Windows PowerShell vs PowerShell 7+), and testability.

---

## Core Objective

**Primary Goal**: Produce a PowerShell language/runtime findings list covering function design, parameter contracts, error handling, pipeline behavior, state/scope, compatibility, and testability for the given code scope.

**Success Criteria** (ALL must be met):

1. ✅ **PowerShell-only scope**: Only PowerShell language and runtime conventions are reviewed; no scope selection, security, or architecture analysis performed
2. ✅ **All seven PowerShell dimensions covered**: Advanced functions/cmdlet conventions, parameter design/validation, error handling semantics, object pipeline behavior, state/scope/strictness, compatibility/portability, and testability are assessed where relevant
3. ✅ **Findings format compliant**: Each finding includes Location, Category (`language-powershell`), Severity, Title, Description, and optional Suggestion
4. ✅ **File:line references**: All findings reference specific file locations with line numbers
5. ✅ **Non-PowerShell code excluded**: Non-PowerShell files are not analyzed for PowerShell-specific rules unless explicitly in scope

**Acceptance Test**: Does the output contain a PowerShell-focused findings list with file:line references covering all relevant language/runtime dimensions without performing security, architecture, or scope analysis?

---

## Scope Boundaries

**This skill handles**:

- `[CmdletBinding()]`, `Verb-Noun` naming, approved verbs, `begin/process/end` blocks
- Parameter types, `Mandatory`, `ValueFromPipeline`, parameter sets, validation attributes
- Terminating vs non-terminating errors, `-ErrorAction Stop`, silent failure prevention
- Object pipeline behavior (prefer objects over formatted text, `Write-Host` vs `Write-Verbose`)
- State, scope, strictness (global/stateful side effects, preference variable changes)
- Windows PowerShell 5.1 vs PowerShell 7+ compatibility and portability
- Performance and testability (Pester-friendly function design, DI seams)

**This skill does NOT handle**:

- Scope selection — scope is provided by the caller
- Security analysis — use `review-security`
- Architecture analysis — use `review-architecture`
- Full orchestrated review — use `review-code`

**Handoff point**: When all PowerShell findings are emitted, hand off to `review-code` for aggregation. For security concerns (e.g. command injection, credential exposure), note them and suggest `review-security`.

---

## Use Cases

- **Orchestrated review**: Used as the language step when [review-code](../review-code/SKILL.md) runs scope -> language -> framework -> library -> cognitive for PowerShell projects.
- **PowerShell-only review**: When the user wants only language/runtime conventions checked.
- **Pre-PR script quality check**: Validate parameter contracts, pipeline behavior, and error semantics before merge.

**When to use**: When the code under review is PowerShell (`.ps1`, `.psm1`, `.psd1`) and the task includes language/runtime quality. Scope is determined by the caller or user.

---

## Behavior

### Scope of this skill

- **Analyze**: PowerShell language and runtime conventions in the **given code scope** (files or diff provided by the caller). Do not decide scope; accept the code range as input.
- **Do not**: Perform scope selection, security review, or architecture review; do not review non-PowerShell files for PowerShell-specific rules unless explicitly in scope.

### Review checklist (PowerShell dimension only)

1. **Advanced function and cmdlet conventions**: Use `[CmdletBinding()]` where appropriate, `Verb-Noun` naming with approved verbs, and `begin/process/end` blocks only when needed.
2. **Parameter design and validation**: Parameter types, `Mandatory`, `ValueFromPipeline`, parameter sets, and validation attributes (`ValidateSet`, `ValidatePattern`, `ValidateScript`) are coherent and not contradictory.
3. **Error handling semantics**: Distinguish terminating vs non-terminating errors; use `-ErrorAction Stop` where required; avoid silent failures and empty `catch`.
4. **Object pipeline behavior**: Prefer objects over formatted text for internal flow; avoid `Write-Host` for data output; ensure function output is predictable and pipeline-safe.
5. **State, scope, and strictness**: Avoid unintended global/stateful side effects, uncontrolled preference variable changes, and ambiguous variable initialization; use strict mode where appropriate.
6. **Compatibility and portability**: Account for differences between Windows PowerShell 5.1 and PowerShell 7+, platform-specific commands/modules, and path handling.
7. **Performance and testability**: Avoid expensive pipeline misuse and repeated array concatenation; structure functions for Pester-friendly testing and dependency isolation.

### Tone and references

- **Professional and technical**: Reference specific locations (file:line). Emit findings with Location, Category, Severity, Title, Description, Suggestion.

---

## Input & Output

### Input

- **Code scope**: Files or directories (or diff) already selected by the user or by the scope skill. This skill does not decide scope; it reviews the provided PowerShell code for language conventions only.

### Output

- Emit zero or more **findings** in the format defined in **Appendix: Output contract**.
- Category for this skill is **language-powershell**.

---

## Restrictions

### Hard Boundaries

- **Do not** perform security, architecture, or scope selection. Stay within PowerShell language and runtime conventions.
- **Do not** give conclusions without specific locations or actionable suggestions.
- **Do not** review non-PowerShell code for PowerShell-specific rules unless explicitly in scope.

### Skill Boundaries

**Do NOT do these** (other skills handle them):

- Do NOT select or define the code scope — scope is determined by the caller or `review-code`
- Do NOT perform security analysis (credential handling, injection risks) — use `review-security`
- Do NOT perform architecture analysis — use `review-architecture`

**When to stop and hand off**:

- When all PowerShell findings are emitted, hand off to `review-code` for aggregation
- When the user needs a full review (scope + language + cognitive), redirect to `review-code`
- When security concerns (credential exposure, command injection) are found, note them and suggest `review-security`

---

## Self-Check

### Core Success Criteria

- [ ] **PowerShell-only scope**: Only PowerShell language and runtime conventions are reviewed; no scope selection, security, or architecture analysis performed
- [ ] **All seven PowerShell dimensions covered**: Advanced functions/cmdlet conventions, parameter design/validation, error handling semantics, object pipeline behavior, state/scope/strictness, compatibility/portability, and testability are assessed where relevant
- [ ] **Findings format compliant**: Each finding includes Location, Category (`language-powershell`), Severity, Title, Description, and optional Suggestion
- [ ] **File:line references**: All findings reference specific file locations with line numbers
- [ ] **Non-PowerShell code excluded**: Non-PowerShell files are not analyzed for PowerShell-specific rules unless explicitly in scope

### Process Quality Checks

- [ ] Was only the PowerShell language/runtime dimension reviewed (no scope/security/architecture)?
- [ ] Are function/parameter conventions, error handling, pipeline behavior, compatibility, and testability covered where relevant?
- [ ] Is each finding emitted with Location, Category=language-powershell, Severity, Title, Description, and optional Suggestion?
- [ ] Are issues referenced with file:line?

### Acceptance Test

Does the output contain a PowerShell-focused findings list with file:line references covering all relevant language/runtime dimensions without performing security, architecture, or scope analysis?

---

## Examples

### Example 1: Pipeline contract mismatch

- **Input**: Function claims pipeline input but does not declare `ValueFromPipeline` and processes only full arrays in `end`.
- **Expected**: Emit a finding for pipeline contract mismatch and suggest parameter attribute + `process` usage. Category = language-powershell.

### Example 2: Error handling

- **Input**: Script wraps risky command in `try/catch` but does not set `-ErrorAction Stop`, so non-terminating errors bypass `catch`.
- **Expected**: Emit a finding for ineffective error handling; suggest explicit terminating behavior. Category = language-powershell.

### Edge case: Data output polluted by host writes

- **Input**: Function returns objects but also uses `Write-Host` within processing loops.
- **Expected**: Emit finding for mixed presentation/data output that harms automation and composability; suggest `Write-Verbose`/`Write-Information` for diagnostics and clean object output for pipeline consumers.

---

## Appendix: Output contract

Each finding MUST follow the standard findings format:

| Element | Requirement |
| :--- | :--- |
| **Location** | `path/to/file.ext` (optional line or range). |
| **Category** | `language-powershell`. |
| **Severity** | `critical` \| `major` \| `minor` \| `suggestion`. |
| **Title** | Short one-line summary. |
| **Description** | 1-3 sentences. |
| **Suggestion** | Concrete fix or improvement (optional). |

Example:

```markdown
- **Location**: `scripts/Build.ps1:34`
- **Category**: language-powershell
- **Severity**: major
- **Title**: Function output mixes objects and host-formatted text
- **Description**: The function emits `Write-Host` output in the data path, which makes automation output unstable.
- **Suggestion**: Return structured objects only and move diagnostics to `Write-Verbose` or `Write-Information`.
```
