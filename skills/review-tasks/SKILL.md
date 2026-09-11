---
name: review-tasks
description: "Review an existing task list against its modeling Spec and canonical quality Rule before assignment or coding, including design coverage, affected scope, Rule references and verification evidence."
description_zh: 在分派或编码前依据任务规范和权威质量规则审查任务列表，包括设计覆盖、影响面、规则引用与验证证据。
tags: [review, tasks, pre-coding]
version: 1.0.0
license: MIT
recommended_scope: both
metadata:
  author: ai-cortex
triggers: [review tasks, task review, validate task list]
input_schema:
  type: document-artifact
  description: Existing task-list document path or content
  artifact_type: tasks
output_schema:
  type: findings-list
  description: Zero or more task-quality findings
---

# Skill: Review Tasks

## Purpose

Evaluate an existing task list against [task-modeling](../../specs/task-modeling.md) and [task-quality](../../rules/task-quality.md). This atomic pre-coding gate ensures implementation work preserves design traceability and verification obligations.

## Core objective

Determine whether every task is independently executable, dependency-safe, bounded, traceable to design and explicit about applicable engineering checks.

## Scope boundaries

This Skill reviews one task-list artifact and its technical-design parent. It does not schedule work, assign people, implement tasks, run tests or aggregate other reviews.

## Use cases

- After task derivation and before assignment or coding
- After design changes alter task coverage or dependencies
- Before an agent starts a quality-sensitive implementation task

## Behavior

1. Load [task-quality](../../rules/task-quality.md) in full, record its version, and resolve the approved technical-design parent.
2. Resolve applicability per [rule-modeling](../../specs/rule-modeling.md): whether the list is being handed off, which tasks meet an engineering-governance trigger, any declared parameters, and any valid waivers.
3. Evaluate each applicable item independently, gathering only the evidence that item declares. A missing declared parameter makes its item evidence-limited; it never suppresses a baseline item.
4. Emit one finding per failed obligation, with category `task-quality`, a task ID or document-level location, and the failed Rule ID in the description, for example `task-quality@<active-version>/TASK-004`.
5. Apply a waiver only when every waiver field is valid and its Rule ID and scope cover the exact finding. Report waived items separately; do not erase their existence.
6. Return Rule coverage using the exact `passed`, `waived`, `not_applicable` and `evidence_limited` fields from the findings-list Spec.
7. Report the list ready for assignment only after every applicable item has a pass, a valid waiver or an explicit evidence limitation; do not start implementation.

## Input and output

Input is one task-list artifact plus its local technical-design parent. Output follows [findings-list](../../specs/findings-list.md): every finding uses category `task-quality` and cites the failed Rule ID, and the coverage footer is metadata rather than a finding.

## Restrictions

- Do not invent tasks, dependencies, owners, estimates or verification commands.
- Do not mark tasks complete.
- Do not copy engineering Rule text into a task; require stable Rule references.

## Self-Check

- [ ] The active Spec and Rule were loaded.
- [ ] Parent status, DAG and design coverage were checked.
- [ ] Conditional engineering governance annotations were checked.
- [ ] Every finding names a precise task or section, uses category `task-quality` and cites one failed Rule ID.
- [ ] Every applicable Rule ID received a pass, a finding, a valid waiver or an explicit evidence limitation.
- [ ] The coverage footer distinguishes passed, waived, not applicable and evidence limited.

## Examples

### Example 1: cross-module task has no checks

A task changes two declared modules but has no affected-scope or ARC verification annotation. Emit a task-quality finding; do not decide the missing topology.

### Example 2: local documentation task

If the technical design has no engineering quality mapping and the task changes one document, do not require governance annotations.

## Change record

- Initial atomic reviewer for task readiness and engineering-governance annotations.

