---
name: review-react
description: Review React code for component design, hooks correctness, state management, rendering performance, and accessibility. Framework-only atomic skill; output is a findings list.
description_zh: 审查 React 代码：组件设计、hooks 正确性、状态管理、渲染性能与可访问性；框架级原子技能。
tags: [code-review, framework]
version: 1.0.0
license: MIT
recommended_scope: project
metadata:
  author: ai-cortex
triggers: [review react]
input_schema:
  type: code-scope
  description: Source files or directories to review
output_schema:
  type: findings-list
  description: Zero or more findings with location, category, severity, and suggestion
---

# Skill: Review React

## Purpose

Review **React** code for **framework conventions** only. Do not define scope (diff vs codebase) or perform security/architecture analysis; those are handled by the scope and cognitive skills. Emit a **findings list** in the standard format for aggregation. Focus on function component design, hooks correctness, state management (local and external), rendering performance, side effects and data fetching, routing and code splitting, and accessibility.

---

## Core Objective

**Primary goal**: produce a React framework findings list covering component design, hooks correctness, state management, rendering performance, side effects, routing/code splitting, and accessibility for the given code scope.

**Success criteria** (all must hold):

1. ✅ **React framework scope only**: reviews React framework conventions only; performs no scope selection, security, or architecture analysis
2. ✅ **All seven React dimensions covered**: component design, hooks correctness, state management, rendering performance, side effects/data fetching, routing/code splitting, and accessibility are assessed where relevant
3. ✅ **Findings format compliant**: each finding carries location, category (`framework-react`), severity, title, description, and an optional suggestion
4. ✅ **Component/file references**: every finding cites a specific file:line or component name
5. ✅ **Non-React code excluded**: non-React files are not analyzed against React-specific rules unless they are explicitly in scope

**Acceptance test**: does the output contain a React-centered findings list with component/file references covering all relevant framework dimensions, without performing security, architecture, or scope analysis?

---

## Scope Boundaries

**This skill owns**:

- Function component design (single responsibility, composition patterns, prop types/defaults, children patterns)
- Hooks correctness (dependency arrays, stale closures, custom hook extraction, the rules of hooks, cleanup in useEffect)
- State management (local vs global state, Context usage, reducer patterns, external stores such as Zustand/Redux, server state via TanStack Query/SWR)
- Rendering performance (memo/useMemo/useCallback usage, key stability in lists, avoiding unnecessary re-renders, virtualization for large lists)
- Side effects and data fetching (useEffect patterns, race conditions, abort controllers, loading/error states, data fetching libraries)
- Routing and code splitting (React.lazy, Suspense boundaries, route-based splitting, error boundaries)
- Accessibility (ARIA attributes, semantic HTML, keyboard navigation, focus management, screen reader support)

**This skill does not own**:

- Scope selection — the scope is supplied by the caller
- Security analysis (XSS, injection risk) — use `review-security`
- Architecture analysis — use `review-architecture`
- Language/runtime (JavaScript/TypeScript) conventions - use `review-typescript` or general JS/TS analysis
- Full orchestrated review — use `orchestrate-code-review`

**Handoff point**: once all React findings are emitted, hand them to `orchestrate-code-review` for aggregation. For XSS risk (dangerouslySetInnerHTML misuse, unsanitized content), note it and point at `review-security`.

---

## Use Cases

- **Orchestrated review**: serves as the framework step when [orchestrate-code-review](../orchestrate-code-review/SKILL.md) runs scope → language → framework → library → cognitive on a React project.
- **React-only review**: when the user wants nothing but React/frontend framework conventions checked.
- **Pre-PR React checklist**: confirm hook usage, component design, and state management patterns are correct.

**When to use**: when the code under review is React and the task includes framework quality. Scope is set by the caller or the user.

---

## Behavior

### What this skill covers

- **Analyse**: React framework conventions inside the **given code scope** (files or a diff supplied by the caller). Does not decide scope; takes the code scope as input.
- **Do not**: perform scope selection, security review, or architecture review; do not check React rules against non-React files unless they are in scope (a mixed repository, for example).

### Review checklist (React framework only)

1. **Component design**: prefer function components; one responsibility per component; composition over deep nesting; explicit prop types with sensible defaults (TypeScript interfaces or PropTypes); appropriate use of children and render props.
2. **Hooks correctness**: correct dependency arrays in useEffect/useMemo/useCallback; avoid stale closures; extract reusable logic into custom hooks; follow the rules of hooks (top level only, React functions only); cleanup functions in useEffect for subscriptions and timers.
3. **State management**: choose local state (useState) vs global state appropriately; use Context for cross-cutting concerns without overusing it; prefer useReducer for complex state transitions; integrate external stores correctly (Zustand, Redux Toolkit); keep server state (TanStack Query, SWR) separate from client state.
4. **Rendering performance**: apply React.memo, useMemo, useCallback where the benefit is demonstrable; stable keys in lists (no index as key for dynamic lists); avoid creating objects/functions inline in JSX when that causes re-renders; virtualize large lists (react-window, react-virtuoso).
5. **Side effects and data fetching**: correct useEffect patterns (single-purpose effects, proper cleanup); handle race conditions with abort controllers or flags; represent loading/error/success states explicitly; prefer a data fetching library (TanStack Query, SWR) over a bare useEffect + fetch.
6. **Routing and code splitting**: route-based code splitting with React.lazy and Suspense; error boundaries defined around lazily loaded routes; route definitions kept declarative; avoid eagerly loading whole modules where lazy loading fits.
7. **Accessibility**: use semantic HTML elements; apply ARIA attributes correctly (roles, labels, live regions); ensure keyboard navigation and focus management; support screen readers; test interactive components for accessibility compliance.

### Tone and references

- **Professional and technical**: cite the exact location (file:line or component name). Emit findings carrying location, category, severity, title, description, and suggestion.

---

## Input & Output

### Input

- **Code scope**: files or directories (or a diff) containing React code (.tsx, .jsx, .ts, .js that use React APIs). Supplied by the user or by a scope skill.

### Output

- Emit zero or more **findings** in the format defined in **Appendix: Output Contract**.
- The category for this skill is **framework-react**.

---

## Restrictions

### Hard Boundaries

- **Do not** perform scope selection, security, or architecture review. Stay inside React framework conventions.
- **Do not** state a finding without a concrete location or an actionable suggestion.
- **Do not** review non-React code against React-specific rules unless it is explicitly in scope.

### Skill Boundaries

**Do not do these** (other skills handle them):

- Do not select or define the code scope - it is set by the caller or by `orchestrate-code-review`
- Do not perform security analysis (XSS, injection) — use `review-security`
- Do not perform architecture analysis — use `review-architecture`

**When to stop and hand off**:

- Once all React findings are emitted, hand them to `orchestrate-code-review` for aggregation
- When XSS risk turns up (unsafe `dangerouslySetInnerHTML` usage, for example), note it and point at `review-security`
- When the user wants a full review (scope + language + cognitive), redirect to `orchestrate-code-review`

---

## Self-Check

### Core success criteria

- [ ] **React framework scope only**: reviews React framework conventions only; performs no scope selection, security, or architecture analysis
- [ ] **All seven React dimensions covered**: component design, hooks correctness, state management, rendering performance, side effects/data fetching, routing/code splitting, and accessibility are assessed where relevant
- [ ] **Findings format compliant**: each finding carries location, category (`framework-react`), severity, title, description, and an optional suggestion
- [ ] **Component/file references**: every finding cites a specific file:line or component name
- [ ] **Non-React code excluded**: non-React files are not analyzed against React-specific rules unless they are explicitly in scope

### Process quality checks

- [ ] Were only React framework dimensions reviewed (no scope/security/architecture)?
- [ ] Were component design, hooks, state, performance, side effects, routing, and accessibility covered where relevant?
- [ ] Does every finding carry location, category = framework-react, severity, title, description, and an optional suggestion?
- [ ] Is each issue tied to a file:line or a component?

### Acceptance test

Does the output contain a React-centered findings list with component/file references covering all relevant framework dimensions, without performing security, architecture, or scope analysis?

---

## Examples

### Example 1: missing cleanup in useEffect

- **Input**: a component that opens a WebSocket connection in useEffect with no cleanup.
- **Expected**: a finding for the missing cleanup (major); the suggestion is to return a cleanup function that closes the connection. Category = framework-react.

### Example 2: index as key in a dynamic list

- **Input**: a component rendering a sortable/filterable list with the array index as the key.
- **Expected**: a finding for key instability and the state bugs it can cause; the suggestion is to use a stable unique identifier as the key. Category = framework-react.

### Edge case: class components in a modern codebase

- **Input**: legacy class components in a codebase that otherwise uses function components and hooks.
- **Expected**: raise the suggestion of migrating to function components with hooks where that is practical; check the class components for lifecycle correctness (componentDidMount, componentWillUnmount cleanup). Note that for stable, well-tested components migration is a suggestion, not always warranted.
