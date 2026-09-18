---
name: review-error-surfacing
description: "Review code against the canonical error surfacing quality Rule set, covering boundary decisions on untrusted input, stopping on a broken invariant, detection layer, and messages a person or a program can act on. Cognitive-only atomic skill; output is a findings list."
description_zh: 依据权威的错误暴露质量规则审查边界输入判定、不变量破坏时的停止、检测层次，以及人或程序能据以行动的失败消息。
tags: [code-review, cognitive, error-handling]
version: 1.0.0
license: MIT
recommended_scope: project
metadata:
  author: ai-cortex
triggers: [review error handling, error surfacing review, error message review]
input_schema:
  type: code-scope
  description: Source files, directories or a diff selected by the caller
output_schema:
  type: findings-list
  description: Zero or more error-surfacing findings traceable to canonical Rule IDs
---

# Skill: Review Error Surfacing

## Purpose

Evaluate the supplied code scope against [error-surfacing-quality](../../rules/error-surfacing-quality.md). This Skill owns execution and evidence gathering; the Rule owns every criterion. Emit a [findings list](../../specs/findings-list.md), never a score or a rewrite.

## Core objective

Produce location-precise findings for every applicable failed Rule item, and report which items were not applicable or could not be evaluated because a project parameter or a profile was absent.

Success requires:

1. The active Rule version and every applicable item ID are named.
2. Active profiles, declared parameters and valid waivers are resolved before judgment.
3. Every finding cites one failed Rule ID and uses category `cognitive-error-surfacing`.
4. Zero findings is reported only after every applicable item has a pass, a valid waiver or an explicit evidence limitation.

## Scope boundaries

This Skill reviews where a defect is decided and how a failure is reported. Three neighbours are owned elsewhere and are flagged rather than judged here: retry, timeout and partial-failure behaviour belongs to `review-reliability`; the telemetry event and its alert ownership belong to `review-observability`; what a security-relevant failure may disclose belongs to `review-security`.

The distinction against observability is the one most often confused: **this Skill reads the message handed back to whoever asked, that one reads the event written for whoever operates.**

## Use cases

- The error-surfacing cognitive step inside `orchestrate-code-review`
- Review of a change that adds an input boundary, a guard or a failure path
- Review of a command-line tool, compiler or interface whose failures a person reads
- Review of an API or agent-facing contract whose failures a program branches on

## Behavior

1. Load [error-surfacing-quality](../../rules/error-surfacing-quality.md) in full and record its version.
2. Resolve active profiles (`human-facing`, `machine-consumer`) and declared parameters from `.ai-cortex/config.yaml` and the nearest `AGENTS.md`, per [rule-modeling](../../specs/rule-modeling.md). A tool whose failures only a person reads activates `human-facing` and not `machine-consumer`; a library both activates both.
3. Build only the evidence applicable items require: entry points and the shapes they return, guards and what follows a failed one, the declared detection layers, and the text or payload at each failure path.
4. Evaluate each applicable item independently. An absent parameter makes only its `project:*` item not evaluable; baseline items still run.
5. Emit one finding per failed obligation, citing the active version, for example `error-surfacing-quality@<active-version>/ERR-002`.
6. Apply a waiver only when every field is valid and its Rule ID and scope cover the exact finding. Report waived items separately.
7. Return Rule coverage using the exact `passed`, `waived`, `not_applicable` and `evidence_limited` fields from the findings-list Spec.

## Input and output

Input is an already selected code scope: files, directories or a diff. Optional project context may include the declared detection layers and the false-positive threshold.

Output is zero or more findings in [findings-list](../../specs/findings-list.md) format, category `cognitive-error-surfacing`. The coverage footer is metadata, not a finding.

## Restrictions

- Do not restate or locally extend the criteria; propose a Rule change when one is missing.
- Do not rewrite code or author replacement messages beyond naming what is missing.
- Do not emit a reliability, observability or security finding under this category.
- Do not treat an awkwardly worded message as a defect when it carries what the Rule requires.

## Self-Check

- [ ] The active Rule version is recorded and cited in every finding
- [ ] Profiles and declared parameters were resolved before judgment
- [ ] Every finding carries a `file:line` reference and one failed Rule ID
- [ ] Items with no evidence are reported `evidence_limited`, never merged into `passed`
- [ ] No neighbouring concern was folded into this category

## Examples

### Example 1: a boundary that accepts and a layer that reinterprets — ERR-001 fails

Input: a handler stores an incoming date as the string it arrived as, and three call sites downstream each parse it again, two of them with different assumptions about the format.

Expected: emit a `major` finding citing ERR-001 at the handler. The defect is at the boundary, not at the three call sites — each of those is a symptom, and fixing them individually leaves the next caller free to invent a fourth interpretation. The remediation names the shape the boundary should return, not the parsing to add downstream.

### Example 2: a boundary that decides — ERR-001 passes

Input: the same handler parses the date at entry, returns a typed value, and rejects what it cannot parse with the field named. No downstream site re-parses.

Expected: record ERR-001 as `passed`. The absence of downstream checks is the evidence, not their presence — the pass condition is that no later layer repeats a decision the boundary already made.

### Example 3: a guard whose failure path continues — ERR-002 fails

Input: a function checks that a configuration key exists, logs a warning when it does not, and proceeds with an empty string. The empty string reaches a path builder forty lines later and writes to the wrong directory.

Expected: emit a `major` finding citing ERR-002 at the guard, not at the path builder. The pass condition is that no detected violation flows into subsequent work; the warning does not satisfy it, because execution ignores the warning.

### Example 4: a documented fallback — ERR-002 does not apply

Input: the same missing key, but the contract declares a default, the default is returned through a value the caller can inspect, and the caller branches on it.

Expected: record ERR-002 `not_applicable`, naming the declared contract. A fallback the caller can observe is the item's own exclusion, not a waiver.

### Example 5: profiles decide which message item runs

Input: a library that returns an error object to callers and never prints.

Expected: ERR-005 applies and ERR-004 is `not_applicable`. Where the same repository also ships a command-line front end, both profiles are active and both items run — against their own paths, not against each other's.
