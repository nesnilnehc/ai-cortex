---
name: review-reliability
description: "Review failure behavior against the canonical reliability quality Rule set, including timeouts, retries, idempotency, partial failure, isolation, dead letters, fault tests and release objectives."
description_zh: 依据权威可靠性规则审查超时、重试、幂等、部分失败、隔离、死信、故障测试与发布目标。
tags: [code-review, cognitive, reliability]
version: 1.0.0
license: MIT
recommended_scope: project
metadata:
  author: ai-cortex
triggers: [review reliability, reliability review, resilience review]
input_schema:
  type: code-scope
  description: Source, configuration and tests selected by the caller
output_schema:
  type: findings-list
  description: Zero or more reliability findings traceable to canonical Rule IDs
---

# Skill: Review Reliability

## Purpose

Evaluate the supplied scope against [reliability-quality](../../rules/reliability-quality.md). Emit [findings-list](../../specs/findings-list.md) output with category `cognitive-reliability`.

## Core objective

Determine whether dependency and partial failures terminate predictably, preserve correct durable state and remain recoverable under the applicable project profiles.

## Scope boundaries

This Skill reviews reliability behavior only. Performance cost, telemetry completeness, architecture structure, test quality, scope selection and repairs belong to their respective Skills, though their evidence may be cited where a reliability Rule requires it.

## Use cases

- Review of remote calls, durable workflows, queues and critical services
- The reliability cognitive step in `orchestrate-code-review`
- Verification of timeout/retry/idempotency and partial-failure design after implementation

## Behavior

1. Load [reliability-quality](../../rules/reliability-quality.md) and record its version.
2. Resolve remote-dependency, durable-workflow, background and critical-service profiles, plus SLO/recovery parameters and waivers.
3. Follow each fallible operation across timeout, retry ownership, duplicate execution, transaction boundaries, terminal state, isolation and recovery tests.
4. Include framework/SDK retry defaults in the effective policy; hidden retries still count toward aggregate behavior.
5. Emit one finding per failed Rule item, citing `reliability-quality@<version>/<REL-ID>` with category `cognitive-reliability`.
6. Return Rule coverage using the exact `passed`, `waived`, `not_applicable` and `evidence_limited` fields from the findings-list Spec.

## Input and output

Input is selected source, configuration and tests. Output is a standard findings list and coverage footer.

## Restrictions

- Do not recommend retries before checking idempotency, timeout and ownership.
- Do not assume exactly-once delivery from a queue or network without end-to-end evidence.
- Do not rewrite SLO, RTO or RPO targets during review.
- Do not duplicate performance findings about cost unless failure behavior is affected.

## Self-Check

- [ ] The canonical reliability Rule and version were loaded.
- [ ] Profiles, targets, SDK behavior and waivers were resolved.
- [ ] Every applicable REL item has a pass, finding, valid waiver or evidence limitation.
- [ ] Partial failure and duplicate execution were checked at durable boundaries.
- [ ] Findings cite precise locations and Rule IDs.

## Examples

### Example 1: retry without idempotency

A payment call retries on timeout but has no idempotency key or durable outcome record. Emit REL-003 as `critical`; REL-002 may also fail if retry behavior is unbounded or layered.

### Example 2: local pure function

For a deterministic parser with no external resource or durable state, mark remote and workflow profile items N/A. Do not force service resilience patterns onto it.

## Change record

- Initial atomic reliability reviewer using externalized, profile-aware Rule criteria.
