---
name: clarify-product-requirement
description: Resolve business choices that materially affect a product requirement's objective, scope, rules, or acceptance. Use for ambiguous feature requests or drafts with unresolved product decisions.
version: 0.2.0
license: MIT
---

# Clarify Product Requirement

Take the user's request or existing draft and its available sources. Use this
skill when a material business choice remains open. For settled requests, hand
off directly to the project's requirement authoring workflow.

1. Read the project conventions, existing item, and relevant evidence. Use
   `rules/requirement-intake-triage.md` from the AI Cortex asset root to classify
   raw intake. Route defects and technical work according to their kind.
2. Resolve factual gaps from available evidence. List the choices that still
   need a person and identify which choices depend on other answers.
3. Ask about decisions whose prerequisites are settled. Group independent
   questions when helpful. Give the practical consequence of each option and
   recommend one when supported. If an answer changes a premise, revisit the
   affected decisions.
4. Return the confirmed objective, scope, exclusions, and observable
   acceptance to the extent supported. Cite the decision sources and list
   what remains open. If an open choice would change a material part of the
   requirement, name the question and pause the affected drafting or
   splitting until it is resolved. When the remaining questions do not
   prevent drafting, hand off to the runtime using
   `specs/requirement-modeling.md`. Suggest `split-product-delivery` if the
   scope is clear and too broad for one delivery.

For an automatic approval request, settle which application types are in scope
before asking which exceptions need manual review. An existing approval policy
may already answer the second question.

## Self-check

Each question changes a material decision and has settled prerequisites.
Confirmed answers have a source. Open decisions remain visible. The handoff
does not imply approval or authorize changes to an existing requirement.
