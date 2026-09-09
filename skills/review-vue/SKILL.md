---
name: review-vue
description: Review Vue 3 code for Composition API, reactivity, components, state (Pinia), routing, and performance. Framework-only atomic skill; output is a findings list.
description_zh: 审查 Vue 3 代码：Composition API、响应式、组件、状态 (Pinia)、路由与性能；框架级原子技能。
tags: [code-review, framework]
version: 1.0.0
license: MIT
recommended_scope: project
metadata:
  author: ai-cortex
triggers: [review vue]
input_schema:
  type: code-scope
  description: Source files or directories to review
output_schema:
  type: findings-list
  description: Zero or more findings with location, category, severity, and suggestion
---

# Skill: Review Vue

## Purpose

Review only the **framework conventions** of **Vue 3** code. Do not define the scope (diff vs codebase) and do not run security/architecture analysis; the scope and cognitive skills handle those. Emit a **findings list** in the standard format for aggregation. Concentrate on the Composition API and `<script setup>`, reactivity (ref/reactive, computed/watch), component boundaries and props/emits, state (Pinia/store), routing and guards, performance (v-memo, for example) and the accessibility that goes with them.

---

## Core Objective

**Primary goal**: produce a Vue 3 framework findings list covering Composition API usage, reactivity correctness, component boundaries, state management, routing, performance and accessibility across the given code scope.

**Success criteria** (all of them must hold):

1. ✅ **Vue 3 framework scope only**: only Vue 3 framework conventions were reviewed; no scope selection, security or architecture analysis was performed
2. ✅ **All seven Vue dimensions covered**: Composition API/script setup, reactivity (ref/reactive/computed/watch), component boundaries/props/emits, state (Pinia), routing/guards, render performance, and accessibility where relevant
3. ✅ **Findings format compatible**: every finding carries location, category (`framework-vue`), severity, title, description and an optional suggestion
4. ✅ **Component/file references**: every finding points at a specific file:line or component name
5. ✅ **Non-Vue code excluded**: Vue-specific rules are not applied to non-Vue files unless they are explicitly in scope

**Acceptance** test: does the output carry a Vue 3-centred findings list, with component/file references covering every relevant framework dimension, and without security, architecture or scope analysis?

---

## Scope Boundary

**This skill owns**:

- Composition API and `<script setup>` correctness (defineProps, defineEmits, defineExpose, lifecycle hooks)
- Reactivity correctness (ref vs reactive, computed vs watch, prop mutation, deep reactivity)
- Component boundary design (props/emits contract, prop drilling, provide/inject)
- State management (Pinia/Vuex: actions vs direct mutation, avoid duplicating server state)
- Routing (Vue Router, navigation guards, lazy loading, route param/query handling)
- Performance (v-memo, v-for key stability, needless re-renders)
- Accessibility (semantic HTML, ARIA, form labels, focus management)

**This skill does not own**:

- Scope selection — the scope comes from the caller
- Security analysis (XSS, injection risk) — use `review-security`
- Architecture analysis — use `review-architecture`
- Language/runtime (JavaScript/TypeScript) conventions — use general JS/TS analysis, or note them as a separate concern
- A full orchestrated review — use `orchestrate-code-review`

**Handoff point**: once every Vue finding has been emitted, hand off to `orchestrate-code-review` for aggregation. For XSS risks (v-html misuse, unsanitized content), note them and suggest `review-security`.

---

## Use Cases

- **Orchestrated review**: used as the framework step when [orchestrate-code-review](../orchestrate-code-review/SKILL.md) runs scope → language → framework → library → cognitive over a Vue project.
- **Vue-only review**: when the user wants to check Vue/frontend framework conventions alone.
- **Pre-PR Vue checklist**: confirm that Composition API usage, reactivity and component contracts are correct.

**When to use**: when the code under review is Vue 3 and the task includes framework quality. The scope is set by the caller or the user.

---

## Behavior

### What this skill covers

- **Analyze**: Vue 3 framework conventions inside the **given code scope** (files or a diff supplied by the caller). It does not decide the scope; it takes the code scope as input.
- **Do not**: perform scope selection, a security review or an architecture review; do not apply Vue rules to non-Vue files unless they are in scope (a mixed repository, for example).

### Review checklist (Vue framework only)

1. **Composition API and script setup**: prefer `<script setup>` and the Composition API; correct use of defineProps, defineEmits, defineExpose; lifecycle hooks (onMounted, onUnmounted and so on).
2. **Reactivity**: correct use of ref vs reactive; computed vs watch; avoid mutating props; deep reactivity and unwrapping in templates.
3. **Component boundaries**: explicit props/emits contracts; avoid prop drilling where a store or provide/inject fits; one responsibility per component.
4. **State (Pinia/store)**: appropriate use of the Pinia (or Vuex) store; avoid duplicating server state in several places; actions vs direct mutation.
5. **Routing and guards**: Vue Router usage; navigation guards and lazy loading; route param and query handling.
6. **Performance**: v-memo for expensive list rendering; avoid needless re-renders; key usage in lists.
7. **Accessibility**: semantic HTML and ARIA where relevant; form labels and focus management.

### Tone and references

- **Professional and technical**: cite a concrete location (file:line or component name). Emit findings carrying location, category, severity, title, description, suggestion.

---

## Input and Output

### Input

- **Code scope**: files or directories (or a diff) holding Vue 3 code (.vue, or .ts that uses the Vue API). Supplied by the user or by the scope skill.

### Output

- Emit zero or more **findings** in the format defined in **Appendix: Output Contract**.
- The category for this skill is **framework-vue**.

---

## Restrictions

### Hard Boundaries

- **Do not** perform scope selection, security or architecture review. Stay inside Vue 3 framework conventions.
- **Do not** land a conclusion without a concrete location or an actionable suggestion.
- **Do not** apply Vue-specific rules to non-Vue code unless it is explicitly in scope.

### Skill Boundaries

**Do not do these** (other skills handle them):

- Do not select or define the code scope - the caller or `orchestrate-code-review` sets it
- Do not perform security analysis (XSS, injection) — use `review-security`
- Do not perform architecture analysis — use `review-architecture`

**When to stop and hand off**:

- Once every Vue finding has been emitted, hand it to `orchestrate-code-review` for aggregation
- When an XSS risk turns up (unsafe `v-html` usage, for example), note it and suggest `review-security`
- When the user wants a full review (scope + language + cognitive), redirect to `orchestrate-code-review`

---

## Self-Check

### Core success criteria

- [ ] **Vue 3 framework scope only**: only Vue 3 framework conventions were reviewed; no scope selection, security or architecture analysis was performed
- [ ] **All seven Vue dimensions covered**: Composition API/script setup, reactivity (ref/reactive/computed/watch), component boundaries/props/emits, state (Pinia), routing/guards, render performance, and accessibility where relevant
- [ ] **Findings format conformant**: every finding carries location, category (`framework-vue`), severity, title, description and an optional suggestion
- [ ] **Component/file references**: every finding points at a specific file:line or component name
- [ ] **Non-Vue code excluded**: Vue-specific rules are not applied to non-Vue files unless they are explicitly in scope

### Process quality checks

- [ ] Were only the Vue framework dimensions reviewed (no scope/security/architecture)?
- [ ] Were the relevant Composition API, reactivity, component, state, routing and performance aspects covered?
- [ ] Does every finding carry location, category=framework-vue, severity, title, description and an optional suggestion?
- [ ] Is every issue tied to a file:line or a component?

### Acceptance test

Does the output carry a Vue 3-centred findings list, with component/file references covering every relevant framework dimension, and without security, architecture or scope analysis?

---

## Examples

### Example 1: mutating props

- **Input**: a component that assigns to a prop in its script or template.
- **Expected**: emit a finding for the prop mutation (major/minor); suggest local state or an emit to the parent. category=framework-vue.

### Example 2: missing key in v-for

- **Input**: a v-for with no :key, or with an unstable key (the array index, for example).
- **Expected**: emit a finding on list identity and performance; suggest a stable, unique key. category=framework-vue.

### Edge case: Vue 2 Options API

- **Input**: legacy Vue 2 Options API in a mixed codebase.
- **Expected**: if the skill is extended to Vue 2, review the Vue 2 patterns (data, methods, lifecycle); otherwise note "use the Vue 3 Composition API" where migration is feasible. For this skill, concentrate on Vue 3; note Vue 2 only when it is explicitly in scope.
