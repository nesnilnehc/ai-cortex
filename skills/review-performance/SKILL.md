---
name: review-performance
description: "Review code against the canonical performance quality Rule set, covering bounded work, I/O amplification, complexity, memory, concurrency, caching, budgets and resource ownership."
description_zh: 依据权威性能质量规则审查工作边界、I/O 放大、复杂度、内存、并发、缓存、预算与资源生命周期。
tags: [code-review, cognitive, optimization]
version: 2.0.0
license: MIT
recommended_scope: project
metadata:
  author: ai-cortex
triggers: [review performance, performance review]
input_schema:
  type: code-scope
  description: Source files, directories or a diff selected by the caller
output_schema:
  type: findings-list
  description: Zero or more performance findings traceable to canonical Rule IDs
---

# Skill: Review Performance

## Purpose

Evaluate the supplied scope against [performance-quality](../../rules/performance-quality.md). The Rule owns the criteria; this Skill owns applicability resolution, measurement and [findings-list](../../specs/findings-list.md) output with category `cognitive-performance`.

## Core objective

Identify demonstrated or mechanically implied performance regressions and missing bounds, while separating measured results from reasoned risk and avoiding speculative micro-optimization.

Success requires one outcome for every applicable Rule item, representative evidence where a project budget applies, a Rule ID in every finding, and a coverage footer.

## Scope boundaries

This Skill reviews performance only. It does not select scope, review reliability semantics, architecture, security, observability or test quality, change performance budgets, or modify code.

## Use cases

- Performance-focused review of request paths, queries, jobs or large-data code
- The performance cognitive step in `orchestrate-code-review`
- Verification of a declared latency, throughput, memory or query-count budget

## Behavior

1. Load [performance-quality](../../rules/performance-quality.md) and record its version.
2. Resolve active profiles, `performance.budgets`, the representative load model and any valid waivers from project evidence.
3. Trace the dominant work path and gather the evidence required by applicable items: operation counts, query/call traces, complexity, allocation/retention, concurrency limits, cache semantics, benchmarks and resource cleanup.
4. Distinguish three states: measured defect, structural risk with a mechanically implied growth path, and insufficient evidence. Only the first two produce findings; the third is reported as an evidence limitation.
5. Emit one finding per failed obligation with the fully qualified Rule ID and category `cognitive-performance`.
6. Return Rule coverage using the exact `passed`, `waived`, `not_applicable` and `evidence_limited` fields from the findings-list Spec.

## Input and output

Input is an already selected code scope plus optional project budgets/load model. Output is a [findings list](../../specs/findings-list.md); descriptions cite `performance-quality@<version>/<PERF-ID>`.

## Restrictions

- Do not invent numeric targets when the project has none.
- Do not treat a tiny synthetic benchmark as representative without a declared load model.
- Do not recommend caching without evaluating ownership, invalidation, capacity and failure behavior.
- Do not duplicate reliability findings about retry correctness; hand those to `review-reliability`.
- Do not repair or change budgets during review.

## Self-Check

- [ ] The canonical performance Rule and version were loaded.
- [ ] Profiles, budgets, load model and waivers were resolved.
- [ ] Every applicable PERF item has a pass, finding, valid waiver or evidence limitation.
- [ ] Measured and inferred risks are labelled accurately.
- [ ] Findings have precise locations, valid severity, actionable remediation and Rule IDs.

## Examples

### Example 1: repeated query in a loop

Emit a `major` finding citing PERF-002, identify the loop and query location, and state the observed or implied query count. Do not invent a latency number.

### Example 2: no benchmark environment

If PERF-007 applies but a representative benchmark cannot run, report an evidence limitation. Do not mark the budget passed from code inspection alone.

## Change record

- Externalized performance criteria to `performance-quality`.
- Added explicit measurement, profile, waiver and coverage behavior.
- Preserved the `code-scope -> findings-list` contract and category.

Version `2.0.0` reflects the new canonical policy source and completeness semantics.
