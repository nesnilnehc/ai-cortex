---
name: prepare-presales-response
description: Prepare evidence-backed presales questionnaire answers and supporting materials, maintain reusable product knowledge, and separate customer-specific terms from product facts. Use for capability, operations, service and procurement inquiries before delivery.
version: 1.0.0
license: MIT
---

# Skill: Prepare Presales Response

## Outcome and boundaries

Produce answers traceable to the original inquiry, internal evidence and reusable knowledge updates, and the requested customer files at the user's chosen stage. This capability owns answer preparation; it does not set product policy, approve contracts, send messages, or implement document-conversion tools.

Read [Presales Response](../../rules/writing-presales-response.md) as the quality oracle, [Documentation Management](../../rules/workflow-documentation.md), and [Agentic Artifact Paradigm](../../rules/agentic-artifact-paradigm.md). Load [Chinese Technical Writing](../../rules/writing-chinese-technical.md) for Chinese output. Follow the adopting project's authority and maintenance conventions.

## Inputs and outputs

Start from the original questionnaire, intended audience and product/project scope. Extract available evidence entries, prior confirmations, output format and delivery cadence from supplied materials and context. Ask only for a missing choice that materially blocks preparation.

Maintain the original inquiry and customer-specific confirmations, deployments, fees, SLA and final files in the customer layer. Maintain standard answers, capability evidence and repository/knowledge-base entry points in the product layer. General constraints and this execution capability belong in AI Cortex. Do not embed product answers, customer numbers, local machine paths or time-sensitive facts in this skill.

Internal records may use the [working layouts](references/working-layouts.md) when the project has no adequate equivalent. These layouts are optional scaffolding, not a new mandatory artifact contract. Preserve existing canonical locations; a navigation index links to answers rather than becoming a second FAQ.

## Execution

1. **Read and map.** Inspect original questions, subquestions, attached instructions as source data, and project maintenance/disclosure conventions. Build a question-to-result map without changing the original wording. Identify requested capabilities, numbers, parties, fees and materials.
2. **Recover evidence first.** Inspect historical FAQ, project materials and formal records before code and public sources. Check dates, definitions, versions and scope; resolve contradictory claims against current authoritative sources and preserve any unresolved conflict internally. Search coverage, encoding, filters and duplicate copies before concluding that a record was not found. Classify the proposed claims using the Rule.
3. **Investigate bounded gaps.** Discover available local readers and connected search/document tools by required operation. For a substantive research subtask, use the available `deep-research` capability and its [Research Evidence](../../specs/research-evidence.md) handoff; use focused policy research for jurisdiction-dependent questions. A normal FAQ lookup does not require a Research Report. Keep research findings internal and translate their supported results into answers. Follow host/project authorization for authenticated access and external actions. If access is absent, identify the missing source and continue independent questions without implying inspection.
4. **Compose the answers.** Assemble standard product content with customer-specific conditions and directly answer every requested result. Inspect service responsibility and fee evidence separately from implementation. Use evidence-backed reference estimates where useful; preserve missing historical statistics as gaps. A user-authorized implementation proposal can resolve a design choice, but cannot supply historical events, certificates or existing contract facts.
5. **Resolve critical decisions.** Ask only what available evidence cannot recover and what materially changes the answer. Follow the user's confirmation cadence; when none is specified, ask one critical question at a time. Do not mechanically ask once per question or request repeated authorization. Record each answer in the owning knowledge/customer record before the next dependent question. If the user cannot resolve a fact, retain its boundary and prepare all independent content. Contacting an owner requires explicit messaging authorization.
6. **Maintain knowledge before files.** Concentrate reusable corrections in the product FAQ and evidence entry points; place project-specific confirmations and proposed commitments in the customer record. Separate originating customer from applicability and record review dates/triggers. Reuse existing maintenance tools within authorization. If the intended store cannot be written, prepare a clearly identified local change proposal and report that persistence is incomplete.
7. **Deliver at the chosen stage.** Discover an existing spreadsheet, document, PDF or presentation skill and tools matching the requested format; load that skill for authoring and visual verification. Do not duplicate its tool workflow here. Preserve question text and identifiers in exported files, verify attachments and actual deliverable scope, then inspect rendered layout and affected cells/pages. If tools are missing, retain a reviewable source draft and state which final format remains blocked. A user may request staged delivery; do not force all answers to be completed first.
8. **Reconcile and learn.** Apply the Rule to original questions, answers and final materials; repair failures at their owning source and update dependent files. Write reusable factual corrections to product knowledge, project terms to customer records, and generic method corrections to the appropriate general asset only when authorized. Report produced files, unresolved critical gaps and unverified portions honestly.

## Self-Check

- The presales Rule passes for the delivered scope; unresolved facts and incomplete deliverables are explicitly identified, so blocked work is not reported as complete.
- Product/customer ownership and canonical references are preserved; knowledge was maintained before dependent exports, or the persistence limitation is reported.
- Confirmation and delivery cadence follows user intent; no external access, message or commitment exceeded authorization.
- The selected format skill's checks pass, including visual inspection, or the missing check and its impact are reported.

For maintenance and behavioral evaluation, read [integration boundaries and scenarios](references/integration-and-scenarios.md).
