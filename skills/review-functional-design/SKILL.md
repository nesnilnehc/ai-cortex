---
name: review-functional-design
description: "Review an existing functional design against its modeling Spec and canonical quality Rule before technical design begins. Evaluative atomic skill; outputs findings without rewriting."
description_zh: 在技术设计开始前依据功能设计规范和权威质量规则审查既有功能设计，只输出 findings，不改写。
tags: [review, functional-design, pre-coding]
version: 1.0.0
license: MIT
recommended_scope: both
metadata:
  author: ai-cortex
triggers: [review functional design, functional design review, validate functional design]
input_schema:
  type: document-artifact
  description: Existing functional-design document path or content
  artifact_type: functional-design
output_schema:
  type: findings-list
  description: Zero or more functional-design-quality findings
---

# Skill: Review Functional Design

## Purpose

Evaluate an existing functional design against [functional-design-modeling](../../specs/functional-design-modeling.md) and [functional-design-quality](../../rules/functional-design-quality.md). This is a pre-coding business-behavior gate, not an architecture review and not a meta-skill.

## Core objective

Determine whether business modules, workflows, states, permissions, exceptions and acceptance criteria are complete and traceable enough for technical design.

## Scope boundaries

This Skill reviews one functional-design artifact and its requirement references. It does not create the design, make technical choices, review implementation or aggregate other Skills.

## Use cases

- After functional design is drafted and before technical design
- After business workflow, state or permission changes
- Before accepting a functional design imported from another system

## Behavior

1. Load the active modeling Spec and quality Rule.
2. Verify artifact identity, approved parent, required sections and conditional state/permission sections.
3. Check workflow closure, exception behavior, business boundaries and acceptance traceability without introducing technical implementation detail.
4. Emit one finding per violation with category `functional-design-quality` and a precise section or flow/state location.
5. Report zero findings as ready for technical design, without invoking it.

## Input and output

Input is one existing functional-design path or full content. Output follows [findings-list](../../specs/findings-list.md).

## Restrictions

- Do not rewrite the design or requirement.
- Do not demand database, API or deployment detail in this layer.
- Do not restate business rules that should be cited from the requirement.

## Self-Check

- [ ] Both canonical assets were loaded.
- [ ] Conditional state and permission sections were evaluated.
- [ ] Every finding is grounded and uses category `functional-design-quality`.
- [ ] No technical-design criterion was introduced.

## Examples

### Example 1: approval roles differ

If two roles have different operation permissions and no permission matrix exists, emit the matching conditional-section finding.

### Example 2: purely technical refactor

If the input is an ADR-authorized refactor with no user-visible behavior, stop and redirect to technical design; a functional design is not required.

## Change record

- Initial atomic reviewer for the existing functional-design Spec and Rule.

