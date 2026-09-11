---
name: review-observability
description: "Review production telemetry against the canonical observability quality Rule set, including structured outcomes, correlation, SLIs, tracing, data safety, error ownership and background-work visibility."
description_zh: 依据权威可观测性规则审查结构化结果、关联上下文、SLI、追踪、数据安全、错误归属与后台任务可见性。
tags: [code-review, cognitive, observability]
version: 1.0.0
license: MIT
recommended_scope: project
metadata:
  author: ai-cortex
triggers: [review observability, observability review]
input_schema:
  type: code-scope
  description: Source, configuration and telemetry definitions selected by the caller
output_schema:
  type: findings-list
  description: Zero or more observability findings traceable to canonical Rule IDs
---

# Skill: Review Observability

## Purpose

Evaluate the supplied scope against [observability-quality](../../rules/observability-quality.md). This atomic Skill gathers production-signal evidence and emits [findings-list](../../specs/findings-list.md) output with category `cognitive-observability`.

## Core objective

Determine whether changed production behavior can be measured, correlated and diagnosed safely, with one outcome for every applicable OBS item.

## Scope boundaries

This Skill reviews observability only. It does not design incident processes, operate monitoring systems, review reliability behavior or performance efficiency, select scope, or modify code.

## Use cases

- Review of deployable services, distributed workflows and background jobs
- The observability cognitive step in `orchestrate-code-review`
- Verification that a new behavior or failure path has safe operational evidence

## Behavior

1. Load [observability-quality](../../rules/observability-quality.md) and record its version.
2. Resolve service/workflow profiles, critical operations, SLI targets, data policy and waivers.
3. Trace representative success and failure paths across telemetry calls, propagation, metrics, spans and job lifecycle signals.
4. Inspect representative emitted fields or schemas. Validate correlation, bounded cardinality and protected-data handling rather than judging log prose alone.
5. Emit one finding per failed item, citing `observability-quality@<version>/<OBS-ID>` and category `cognitive-observability`.
6. Return Rule coverage using the exact `passed`, `waived`, `not_applicable` and `evidence_limited` fields from the findings-list Spec.

## Input and output

Input is selected source, configuration and telemetry definitions. Output is a standard findings list plus the coverage footer.

## Restrictions

- Do not require logs, metrics and traces indiscriminately; apply each profile and item condition.
- Do not inspect live production data unless explicitly provided and authorized.
- Do not include protected values in findings.
- Do not treat dashboard existence as proof that the underlying signal is correct.
- Do not restate a security obligation about disclosure. This Skill owns where and how often a failure is recorded; `review-security` owns whether security telemetry is actionable without leaking secrets or exploitable internals.

## Self-Check

- [ ] The canonical observability Rule and version were loaded.
- [ ] Profiles, critical operations, targets, data policy and waivers were resolved.
- [ ] Every applicable OBS item has a pass, finding, valid waiver or evidence limitation.
- [ ] Findings cite precise locations and Rule IDs without exposing protected data.

## Examples

### Example 1: asynchronous correlation is dropped

The producer starts a trace but omits context from message metadata. Emit an OBS-002 finding at the publish call and identify the consumer path that becomes disconnected.

### Example 2: library-only change

A pure parser emits no telemetry and crosses no process boundary. Mark service/profile items N/A; evaluate OBS-005 only if telemetry was added or changed.

## Change record

- Initial atomic observability reviewer using externalized, profile-aware Rule criteria.
