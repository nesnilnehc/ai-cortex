---
id: AIC-REQ-06
artifact_type: requirement
lifecycle: snapshot
created_at: 2026-10-28
status: approved
parent: ../project-overview/strategic-goals.md#goal-1-delivery-chain-capabilities-are-available
---

# Requirement: [Functional] Generic release workflow adaptation

## Background & Value

Maintainers need one prepare, publish and announce workflow across projects without confusing release identity, build identity or incomplete delivery evidence.

## Objective

A maintainer can prepare, execute and resume a project release while preserving project version policy and existing consumer behavior.

## Scope

Deliver the independent `build-project` Skill, the prepare/publish/announce handoffs,
and the versioned Release Package contract, with their guides, registries and
bilingual website descriptions. A candidate artifact is a particular build output;
the Release Package records release evidence and is not the binary package itself.
Generic combined-pipeline and Apple examples explain the contract without executing
those systems or prescribing a consumer project's version policy.

Acceptance is limited to contracts and repository assets. Independent Agent behavior
evaluations, real consumer-project builds, provider integration, uploads, announcements
and channel publication are not acceptance gates for this requirement. Do not create
a second implementation of the workflow merely to simulate Skill compliance. Existing
executable assets still require their applicable code-quality checks; their results
must not be described as evidence that an Agent followed a Markdown Skill.

## Business Rules

| ID | Condition | Required behavior |
| --- | --- | --- |
| R1 | A release has builds | A release and a build have distinct identities; their versions follow the project policy. Preserve their relationship and never infer equality from numeric format. |
| R2 | Preparation precedes artifact production | Distinguish execution prerequisites from later delivery acceptance. A required future artifact remains required; its absence cannot be relabeled passed or optional. |
| R3 | A project already has release instructions and tools | Reuse applicable instructions and tools through the generic release workflow; no project-specific duplicate trio or new configuration framework is mandatory. |
| R4 | An operation is interrupted | Read actual state before repeating writes; preserve partial and unknown results. Announcement recovery cannot rebuild or re-upload completed artifacts. |
| R5 | Existing consumers are supported | Preserve existing contract semantics or provide an explicitly versioned, verified migration boundary before mutation. |
| R6 | A build is requested without a release | Build-only use is available independently of release preparation when a suitable project capability exists; it does not require a release decision or create a formal release or authorize publication. A combined build-and-publication operation is not run as a build-only action. |
| R7 | A release has candidate builds | Multiple pre-builds may be considered for one release. Formal release identifies the build or builds actually selected for each applicable target; other builds are not silently represented as published. Association alone does not establish successful publication. |
| R8 | A release has publication targets | Overall publication completes only if at least one target is successfully published and every project-designated required target is complete. Target completion uses the project's applicable delivery requirements and evidence; an unknown result is not success. Failed, pending or unknown required targets block overall completion; optional outcomes remain visible but do not block an otherwise complete release. |
| R9 | Candidate artifacts are considered for release | Retain each candidate's build/source identity and its verification outcomes. Selection identifies the candidate artifacts for each target and uses project-required verification applicable at selection; failed or missing evidence is not a pass, and a different candidate does not inherit those results. Exceptions follow R11. |
| R10 | A selected candidate is delivered | Prefer delivery of the verified candidate itself when the project and channel support it. If delivery transforms or rebuilds it, retain evidence connecting the candidate to the actual delivered result and verify that result as required by project and channel policy. A missing or contradictory relationship prevents a completion claim; a missing or failed required check blocks completion unless an R11 exception applies. |
| R11 | A required check fails or is unexecuted | Across all channels, an explicitly authorized person may accept risk only for an internal check that project policy permits waiving; an absent or unclear policy does not permit an exception. Record the approver, candidate, target, check, scope, rationale and evidence; retain the actual result and do not apply the exception to another candidate or scope. Missing authorization, unverified or mismatched candidate/artifact identity, and channel-enforced blockers cannot be waived. An eligible exception permits only its applicable next action or completion gate. |

## Acceptance Criteria

Only contract and asset evidence is required. Review the defining Skill/Spec text,
its static examples and repository checks; no product or channel operation is needed.

- [ ] **AC1 — Responsibilities and handoffs.** The four Skills clearly define triggers, inputs, outputs, completion and failure reporting. Build-only use is independent; preparation, publication and announcement responsibilities are distinct. Conditional calls and project-tool reuse agree across the Skills and guide. Covers R3, R4 and R6.
- [ ] **AC2 — Release and candidate identity.** The Spec and public examples distinguish release, build, source and artifact identities, preserve multiple candidates and their individual checks, and identify selected artifacts per target. The example version policy is explicitly illustrative. Covers R1, R7 and R9.
- [ ] **AC3 — Stages and delivery evidence.** The contract and instructions distinguish preparation prerequisites from later acceptance, preserve pending checks and future required artifacts, and define evidence for unchanged and transformed delivery. Selection or build success alone cannot mean published. Covers R2, R9 and R10.
- [ ] **AC4 — Outcomes and recovery.** The contract and instructions retain target outcomes, require at least one successful target and all required targets to complete, and preserve optional failures. Recovery instructions require reconciliation of uncertain actions and reuse of completed results; announcement recovery cannot rebuild or upload. Covers R4 and R8.
- [ ] **AC5 — Risk exceptions.** The Spec and Skills consistently state the required approval, candidate/target/check/scope/rationale/evidence fields, preservation of the original check result, project-policy restrictions and non-waivable authorization, identity and provider blockers. Covers R9 and R11.
- [ ] **AC6 — Compatibility boundary.** Existing 1.x meanings are preserved; 2.x is explicitly versioned with declared admission and migration boundaries. Existing supported contract checks pass. No asset claims that a reference reader proves actual deployed-consumer behavior; unknown integrations remain disabled when used. Covers R5.
- [ ] **AC7 — Asset integrity and delivery consistency.** Changed assets have valid metadata, local references, provenance/license records and versions. Registries, guides, related Skill handoffs and both website editions agree. Applicable repository format, link, index, asset-version and compatibility checks pass. No private project identifiers or unnecessary workflow-simulation framework is required for acceptance.

## Quality Attribute Scenarios

These scenarios describe obligations expressed by the assets. Their acceptance
method is contract/instruction/example review, not execution against a provider.

| id | quality | source/stimulus | environment | affected artifact | response | measure | rule_refs |
| --- | --- | --- | --- | --- | --- | --- | --- |
| QAS-01 | reliability | A release action has an uncertain result or announcement is resumed | Skill and Spec review | Publication and announcement instructions | Define reconciliation before retry and prohibit repeating completed product actions during announcement recovery | AC4 review finds explicit unknown/conflict stop paths and completed-result reuse; no contradictory instruction | Applicable reliability obligations are reviewed at the asset boundary |
| QAS-02 | traceability | A selected candidate is delivered unchanged or transformed | Spec and static example review | Candidate-to-delivery contract | Preserve selected and delivered identities, relationship and applicable verification evidence | AC2/AC3 review can locate every required identity and relation, including missing-evidence blockers | Applicable contract/alignment obligations are reviewed at the asset boundary |

## Dependencies & Prerequisites

Dependent requirements: none. AIC-REQ-05 and AIC-REQ-07 refer to this requirement where shared contract changes are needed; their dependency status remains subject to their own review.

Acceptance prerequisites: the defining assets, local references and existing repository validation tools are available. When a consumer later uses these Skills, project identity policy, execution prerequisites and authorization must be established at that time; those execution conditions do not require a real consumer run for this library requirement.

External services are not needed for this requirement acceptance. Project-specific build, publication and announcement services belong to later consumer use and require their own availability and authorization checks.

## Risks, Constraints & Assumptions

- Incorrect completion or provenance claim: probability medium, impact high, priority high. Mitigation: preserve source evidence, review contradictory or missing-evidence examples, and keep contract-validation results separate from claims about Agent or provider execution.
Confirmed constraints:

- Current experimental documents are proposals, not approved contracts.
- Authenticated external requests and remote writes require explicit user authorization under the project agent entry; this requirement does not itself authorize a release or deployment.

## Source

- Source type: user feature request. The user requested a reusable workflow that preserves project version policy and existing consumer behavior.
- Existing [Release Package contract](../../specs/release-package.md) describes a record for one release candidate, has artifact and check entries, and requires all required checks to pass for readiness before publication. Its current fields do not explicitly bind checks to multiple candidate artifacts, selection per target, or transformed delivered results; a check that requires a future artifact needs a later gate without misrepresenting its result. Whether to extend that contract or use another versioned record is a design choice, subject to the existing compatibility policy and a single authoritative source for each fact.
- Capability assessment, 2026-10-29: existing test, local redeployment and release Skills do not declare a general standalone build-only workflow. A project may provide independent build tools or a combined publication pipeline; verify its actual capabilities and authorization before execution.
- Compatibility evidence, 2026-10-29: [stable core](../project-overview/stable-core.md) includes prepare-release, publish-release and the Release Package as protected 1.0 target contracts. Existing 0.x releases are not retroactively stable; assess actual readers and boundary evidence under the policy rather than assume all historical consumers fail closed.
- Consumer evidence, 2026-10-29: [the bounded reference checker](../../scripts/check-stable-consumers.py) and its [12 regression methods](../../scripts/test-stable-consumers.py) passed locally. Its 0.5.1 and 0.6.0 descriptors validate real package fixture projections and reject an unknown major in the reference model; they are not historical deployed parsers and perform no external writes. They do not prove that actual agents or project consumers reject new inputs before mutation. The current publish Skill requires a 1.x `ready` package, the announcement Skill requires overall `published`, and the video Skill consumes release identity and change items. Preserve their declared behavior or verify an explicit transition; do not use an ignored optional extension as proof that an old reader enforces new gates. See the [consumer evidence guide](../guides/consumer-compatibility.md) for scope and limits.
- Revision 2026-10-28: clarified the unresolved identity policy, stage-specific evidence and recovery scenario after a read-only review of representative project sources.
- Revision 2026-10-29: the user proposed distinguishing builds from releases, allowing multiple pre-builds and associating the selected build with the formal release, and suggested an independent build Skill. The user subsequently clarified that these are hypotheses for critical assessment. The existing publication Skill also orchestrates build/package; its future responsibility and compatibility require review rather than an assumed migration.
- Revision 2026-10-29: added build-only and per-target evidence cases, clarified the generic example and compatibility scope, and recorded the unresolved cross-target completion decision after reviewing existing Skills and representative project records.
- Revision 2026-10-29: the user confirmed the cross-target completion rule in R8. Clarified that build-only use does not require release preparation; the choice of a separate Skill remains a design question.
- Revision 2026-10-29: the user confirmed that formal publication should be associated with project-verified candidate artifacts and that transformations require a recorded relationship and verification of the actual delivery. Added candidate-specific verification, selection and stage-aware delivery evidence cases without selecting a contract design.
- Revision 2026-10-29: the user extended the policy-scoped risk-acceptance principle to all publication channels, including non-waivable authorization, identity and channel-enforced blockers. Added R11 and positive and negative acceptance cases.
- Revision 2026-10-29: checked bounded old/current consumer evidence and inventoried locally available project branch snapshots; recorded their coverage limits without treating reference models or script presence as proof of actual execution.
- Industry evidence inspected 2026-10-29: [Google Cloud's CI/CD guidance](https://docs.cloud.google.com/kubernetes-engine/docs/concepts/best-practices-continuous-integration-delivery-kubernetes) recommends promoting the tested container image rather than rebuilding it; [Cloud Deploy](https://docs.cloud.google.com/deploy/docs/overview) distinguishes a release from its target-specific rollouts. [App Engine](https://docs.cloud.google.com/appengine/docs/standard/testing-and-deploying-your-app) also documents a deployment workflow that builds during deployment. These sources support traceable build and delivery identities but do not mandate a separate Skill or a single build for every release.
- Revision 2026-10-29: the user accepted the requirement and authorized implementation with a public, de-identified delivery.

- Revision 2026-10-30: the user limited Skill acceptance to contracts and assets. Replaced the former 14 execution-oriented criteria with AC1–AC7 above. Business rules R1–R11 remain unchanged. Agent evaluation, real-project/channel execution and a parallel simulated workflow are not required to close this library requirement. The [acceptance and closeout record](../../experiments/release-workflow/acceptance-review.md) uses the revised criteria.
