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

Build and generic release capabilities, candidate artifact selection and verification, and their shared handoffs, with a generic combined pipeline and Apple as validation scenarios. A candidate artifact is a specific build output being considered for release; the Release Package is the release evidence record, not necessarily the artifact itself. Whether a separate build Skill is needed remains under review. Excludes provider-specific implementation, a mandatory project configuration framework and any predetermined schema-major choice.

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

- [ ] A build-only fixture invokes an available project build capability and records its result and produced artifacts without release preparation, a release decision, a formal release or publication. When only a combined build-and-publication operation is available, a build-only request reports that limitation without invoking it. Covers R6.
- [ ] A release fixture records two candidate builds and explicitly associates the selected build with the formal release. The other build remains identifiable, and neither its existence nor a change in build version silently creates a release. Covers R1 and R7.
- [ ] A generic fixture uses an explicitly supplied example policy to record release identity, selected build identity, source revision and evidence without inferring release identity from the build value. The example does not prescribe a project policy. Covers R1 and R7.
- [ ] A multi-target fixture records the selected build and publication evidence separately for each target. A build association or successful build alone does not mark its target published; missing or unknown delivery evidence remains visible. Covers R1 and R7.
- [ ] Two candidate artifacts have separate build/source identities and check outcomes. With no applicable exception, the first fails a project-required selection check and is not treated as eligible; after the second passes that check, it can be selected. Neither the first candidate's failure nor the second's success is overwritten or inherited by the other. Covers R7 and R9.
- [ ] A project-permitted internal check with an explicitly authorized exception permits its applicable next action or completion gate, records approver, candidate, target, check, scope, rationale and evidence, and leaves the failed or unexecuted result unchanged. A different candidate or scope does not inherit it. Covers R9 and R11.
- [ ] An exception does not permit progress past missing action authorization, unverified or mismatched candidate/artifact identity, a channel-enforced blocker, or a check that project policy does not permit waiving. With absent or unclear policy, the check is not treated as waivable. Covers R11.
- [ ] For a target that can deliver the verified candidate unchanged, a fixture identifies that candidate as the delivered result. For a channel that transforms it, a fixture records the relationship and required verification of the actual result; missing or contradictory relationship evidence prevents a completion claim, as does missing required verification without an applicable exception. Covers R10 and QAS-02.
- [ ] A fixture whose required server verification is only available after upload allows the authorized upload once its applicable earlier prerequisites are satisfied, retains the later verification as pending, and prevents target completion until that check passes or an applicable project-permitted exception is authorized. Covers R2, R9 and R10.
- [ ] A preparation fixture with all execution prerequisites satisfied and a required future artifact can complete preparation; the same artifact absent or failing acceptance prevents completion of the target that requires it. Covers R2 and R8.
- [ ] With two required targets, one successful and the other pending, failed or unknown, overall publication remains incomplete; it completes after both are complete. An optional pending or failed target remains visible without blocking an otherwise complete release. With no successful target, overall publication remains incomplete even if none is required. Covers R8.
- [ ] A combined-pipeline fixture reuses project instructions and existing execution tools without requiring three project Skills or a new configuration format. Covers R3.
- [ ] Unknown-trigger and announcement-only recovery fixtures cause zero duplicate completed writes. Covers R4 and QAS-01.
- [ ] Historical and current supported consumer fixtures exercise the affected Release Package and release Skill contracts under the [stable-core compatibility policy](../project-overview/stable-core.md#compatibility-and-deprecation). Unsupported incompatible execution inputs are rejected before mutation; an unverified consumer boundary remains unresolved. Covers R5.

## Quality Attribute Scenarios

| id | quality | source/stimulus | environment | affected artifact | response | measure | rule_refs |
| --- | --- | --- | --- | --- | --- | --- | --- |
| QAS-01 | reliability | Maintainer resumes after an uncertain trigger or an interrupted announcement | Trigger outcome unknown, or artifact publication completed before announcement interruption | Release workflow | Reconcile actual state before repeating writes; keep an ambiguous result unresolved and do not repeat completed publication during announcement recovery | Zero duplicate completed writes in both fixtures; an ambiguous trigger is not retried | Resolve applicable engineering Rule IDs during design |
| QAS-02 | traceability | Maintainer inspects the result of delivery | Representative unchanged and transformed candidate fixtures | Candidate-to-delivery evidence | Identify the selected candidate and actual delivered result and retain their verification and relationship evidence | Both identities and their relationship are recoverable; an unverified or contradictory relationship does not result in a completed target | Resolve applicable engineering Rule IDs during design |

## Dependencies & Prerequisites

Dependent requirements: none. AIC-REQ-05 and AIC-REQ-07 refer to this requirement where shared contract changes are needed; their dependency status remains subject to their own review.

Preconditions: confirm the project release identity policy and applicable execution prerequisites from project evidence before applying them; verify each prerequisite against its stated evidence. A combined build and upload operation is not build-only and its upload is not implicitly authorized.

External dependencies: project-specific build, publication and announcement services are needed only for a release that uses them; availability and authorization must be verified before the corresponding action.


## Risks, Constraints & Assumptions

- Incorrect completion or provenance claim: probability medium, impact high, priority high. Mitigation: preserve source evidence and verify the negative cases in acceptance fixtures.
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
