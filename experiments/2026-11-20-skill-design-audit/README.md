# AI Cortex Skill design audit

Reviewed on 2026-11-20 against source revision `705691a` and the local Skill
changes. Scope covers all 79 repository entry points. Each was checked for its
trigger, outcome, handoff to related Skills, format and on-demand loading.
The execution checks relevant to this document review are local. The audit does
not certify the behavior of a host or execute every Skill's workflow.

All 79 remain independently discoverable. Five received patch-level guidance
changes in this audit. The four earlier working-tree patches were reviewed
again. The catalog preview includes all of them.

## Format and progressive disclosure

All 79 files have parseable YAML and locally checked standard field names,
types, lengths and directory agreement. They also have the top-level
`version` extension. The official reference validator rejects unknown top-level
fields, so all 79 would fail its strict field check. In addition, 27 declare
`output_schema` and one declares `argument-hint`. The official binary was
not installed. This conclusion follows from comparing the actual field
inventory with the reference validator's explicit allowlist.
[Agent Skills specification](https://agentskills.io/specification) and
[reference validator](https://raw.githubusercontent.com/agentskills/agentskills/main/skills-ref/src/skills_ref/validator.py).

Migration would affect [provenance validation](../../scripts/skill_provenance_v2.py),
[version checks](../../scripts/check-asset-versions.py),
[findings routing](../../specs/findings-list.md), and published packages and
their readers. A candidate is to move version strings into standard `metadata`
and introduce compatible readers before converting the catalog. Confirm publishing
and old-reader behavior as part of that migration.

References were extracted only when material is needed for a specific execution
route or judgment. The required decisions and completion conditions stay in each
owning Skill. No entry was selected for retirement. The entry and loading
criteria are defined in [Contributing](../../CONTRIBUTING.md#choosing-a-skill-boundary)
and [Agent Skills best practices](https://agentskills.io/skill-creation/best-practices#structure-large-skills-with-progressive-disclosure).

## Operational issues for follow-up

| Skill | Evidence and impact | Acceptance for a follow-up |
| --- | --- | --- |
| [manage-secret](../../skills/manage-secret/SKILL.md#stage-3-execute) | A credential can enter a logged tool argument or captured output through the documented CLI paths, despite the cleartext restriction. No actual credential was accessed. | Keep values out of visible tool arguments, output and logs. Use a supported secret-aware input or retrieval path, and give a usable manual path when the host cannot provide one. |
| [generate-agent-entry](../../skills/generate-agent-entry/SKILL.md#scope-boundaries) | Authoring success is tied to a commit even when the authoring request does not specify one. Local authoring and commit authorization can differ. | Make completion explicit for both a request limited to authoring and one that also authorizes a commit. Check implications for the stable-core contract. |
| [commit-work](../../skills/commit-work/SKILL.md#workflow) | It asks for canonical Skill catalog synchronization before committing. Canonical generation also requires a pin to the reviewed source commit. | Provide a sequence for validating the uncommitted source and then pinning and generating the formal catalog, within the authorized commit scope. |
| [redeploy-local](../../skills/redeploy-local/SKILL.md#behavior) | Core acceptance requires a healthy service. Execution and failure handling can return without a passing health check. | Report the build and restart result separately from the observed or unverified health result, and keep cache writes gated on verified health. |

## Entry-by-entry outcomes

### Strategy

| Skill | Result | Scope or change |
| --- | --- | --- |
| [define-mission](../../skills/define-mission/SKILL.md) | Retain | Persist a confirmed purpose statement. Vision, measurement and plans are later handoffs. |
| [define-north-star](../../skills/define-north-star/SKILL.md) | Retain | Derive one actionable user-value metric and expose measurement limitations. |
| [define-strategic-pillars](../../skills/define-strategic-pillars/SKILL.md) | Retain | Produce durable strategic themes that can guide several goals or roadmap entries. |
| [define-vision](../../skills/define-vision/SKILL.md) | Retain | Persist the desired future state with the mission as its upstream constraint. |
| [design-strategic-goals](../../skills/design-strategic-goals/SKILL.md) | Retain | Produce outcome goals from strategy or bounded cold-start evidence. |

### Planning

| Skill | Result | Scope or change |
| --- | --- | --- |
| [archive-milestone](../../skills/archive-milestone/SKILL.md) | Retain | Archive snapshots and completed work packages with source evidence and open work preserved. |
| [capture-work-items](../../skills/capture-work-items/SKILL.md) | Earlier patch 2.3.1 verified | Capture a classified record. The earlier patch loads only the selected template at persistence. |
| [clarify-product-requirement](../../skills/clarify-product-requirement/SKILL.md) | Retain | Resolve material business choices and hand off settled scope or report the blocking choice. |
| [define-roadmap](../../skills/define-roadmap/SKILL.md) | Refined to 9.0.1 | Keep structure selection and publication permission in the core. Read generation or delivery mechanics on demand. |
| [map-item-dependencies](../../skills/map-item-dependencies/SKILL.md) | Retain | Return prerequisite evidence and readiness before planning or promotion. |
| [orchestrate-governance-step](../../skills/orchestrate-governance-step/SKILL.md) | Retain | Execute one eligible action and return a bounded continuation report. Report schemas and unusual cases already have conditional loading points. |
| [orchestrate-roadmap-planning](../../skills/orchestrate-roadmap-planning/SKILL.md) | Refined to 2.12.2 | Keep the authorized route and its halt semantics in the core. Load worked routing cases on demand. |
| [plan-milestones](../../skills/plan-milestones/SKILL.md) | Retain | Create or revise event-based milestone plans, with optional local calendar generation. |
| [plan-next](../../skills/plan-next/SKILL.md) | Retain | Diagnose what can happen next. The diagnostic, output and examples have separate loading points. |
| [prioritize-backlog](../../skills/prioritize-backlog/SKILL.md) | Retain | Settle priority using current policy or an explicitly selected reassessment mode. Load the assessment methods only in framework modes. |
| [promote-roadmap-items](../../skills/promote-roadmap-items/SKILL.md) | Retain | Make tier decisions from priority and readiness evidence while preserving version and timing decisions. |
| [record-milestone-achievement](../../skills/record-milestone-achievement/SKILL.md) | Retain | Record an already achieved milestone with independently stored evidence. |
| [review-roadmap](../../skills/review-roadmap/SKILL.md) | Retain | Return scoped structure or business findings without writing the roadmap. |
| [split-product-delivery](../../skills/split-product-delivery/SKILL.md) | Retain | Propose separately acceptable increments after the material choices are settled. |
| [update-roadmap](../../skills/update-roadmap/SKILL.md) | Retain | Maintain dates, status and affected projections without making tier-promotion decisions. |

### Research

| Skill | Result | Scope or change |
| --- | --- | --- |
| [competitive-research](../../skills/competitive-research/SKILL.md) | Retain | Return a dated competitor matrix and traceable claims for standalone questions and opportunity analysis. |
| [deep-research](../../skills/deep-research/SKILL.md) | Retain | Answer a bounded open question and supply the shared evidence method to several domain Skills. |
| [market-research](../../skills/market-research/SKILL.md) | Retain | Return segment, demand and defensible market-size evidence without forcing estimates. |
| [policy-research](../../skills/policy-research/SKILL.md) | Retain | Return dated, jurisdiction-scoped evidence and flag unresolved applicability. |
| [product-opportunity-analysis](../../skills/product-opportunity-analysis/SKILL.md) | Retain | Own the opportunity decision package. The main assessment is inline and detailed guidance has explicit loading conditions. |

### Design

| Skill | Result | Scope or change |
| --- | --- | --- |
| [orchestrate-repair-requirements-loop](../../skills/orchestrate-repair-requirements-loop/SKILL.md) | Retain | Repair an existing requirement in bounded iterations while preserving frozen versions and user-owned decisions. |
| [review-functional-design](../../skills/review-functional-design/SKILL.md) | Retain | Return findings on one existing functional design and its requirement alignment. |
| [review-requirements](../../skills/review-requirements/SKILL.md) | Retain | Evaluate an existing requirement against its own Spec and Rule before downstream design. |
| [review-tasks](../../skills/review-tasks/SKILL.md) | Retain | Review implementation-task coverage and verifiability against the approved parent design. |
| [review-technical-design](../../skills/review-technical-design/SKILL.md) | Retain | Review a technical design and applicable Rule profiles before implementation tasks. |

### Engineering quality

| Skill | Result | Scope or change |
| --- | --- | --- |
| [orchestrate-code-review](../../skills/orchestrate-code-review/SKILL.md) | Refined to 1.4.3 | Select and dispatch engineering reviewers. Its self-check now matches the workflow's responsibility for selection and aggregation. |
| [orchestrate-repair-loop](../../skills/orchestrate-repair-loop/SKILL.md) | Earlier patch 1.5.1 verified | Drive engineering and functional convergence. The earlier patch kept iteration and stop conditions in the main flow and moved scenarios. |
| [review-architecture](../../skills/review-architecture/SKILL.md) | Retain | Apply architecture Rules and evidence limits to a supplied scope. Keep a standalone architecture review entry. |
| [review-codebase](../../skills/review-codebase/SKILL.md) | Retain | Review the current state of a selected scope, with no dependence on a diff. |
| [review-diff](../../skills/review-diff/SKILL.md) | Retain | Review the changed scope, including the default inclusion of untracked additions. |
| [review-dotnet](../../skills/review-dotnet/SKILL.md) | Retain | Deliver .NET-specific findings from a supplied scope, including nullability and async use. |
| [review-error-surfacing](../../skills/review-error-surfacing/SKILL.md) | Refined to 1.2.2 | Review boundary decisions and error reporting. The 13 Rule-specific examples are available on demand. |
| [review-go](../../skills/review-go/SKILL.md) | Retain | Deliver Go-specific findings, including concurrency and context handling. |
| [review-implementation-alignment](../../skills/review-implementation-alignment/SKILL.md) | Retain | Compare code and verification evidence with approved requirements, designs and tasks. |
| [review-java](../../skills/review-java/SKILL.md) | Retain | Deliver Java-specific findings, including exception handling and resource ownership. |
| [review-observability](../../skills/review-observability/SKILL.md) | Retain | Review production-signal evidence and profile applicability. |
| [review-orm-usage](../../skills/review-orm-usage/SKILL.md) | Retain | Review ORM-specific queries and operations in a defined scope. |
| [review-performance](../../skills/review-performance/SKILL.md) | Retain | Review applicable performance criteria and expose absent measurement evidence. |
| [review-php](../../skills/review-php/SKILL.md) | Retain | Deliver PHP-specific findings, including strict typing and resource handling. |
| [review-powershell](../../skills/review-powershell/SKILL.md) | Retain | Deliver PowerShell-specific findings, including pipeline contracts and error behavior. |
| [review-python](../../skills/review-python/SKILL.md) | Retain | Deliver Python-specific findings, including exception scope and async behavior. |
| [review-react](../../skills/review-react/SKILL.md) | Retain | Deliver React-specific findings, including hooks and state ownership. |
| [review-reliability](../../skills/review-reliability/SKILL.md) | Retain | Review failure handling, durability and retry behavior under the applicable Rules. |
| [review-security](../../skills/review-security/SKILL.md) | Retain | Review trust boundaries and return Rule evidence, including tool-coverage limits. |
| [review-sql](../../skills/review-sql/SKILL.md) | Retain | Review SQL and queries for language, correctness and execution concerns. |
| [review-testing](../../skills/review-testing/SKILL.md) | Retain | Review test adequacy and evidence, leaving execution to the test runner. |
| [review-typescript](../../skills/review-typescript/SKILL.md) | Retain | Deliver TypeScript and JavaScript findings on types, async use and module conventions. |
| [review-vue](../../skills/review-vue/SKILL.md) | Retain | Deliver Vue-specific findings on reactivity, components and rendering. |

### Build and delivery

| Skill | Result | Scope or change |
| --- | --- | --- |
| [automate-tests](../../skills/automate-tests/SKILL.md) | Retain | Discover and run the selected checks and report reproducible evidence independently of repair. |
| [bump-version](../../skills/bump-version/SKILL.md) | Retain | Apply a settled version change and verify its references without running the release pipeline. |
| [establish-delivery-workflow](../../skills/establish-delivery-workflow/SKILL.md) | Retain | Establish or repair the project-owned delivery workflow. |
| [execute-delivery-workflow](../../skills/execute-delivery-workflow/SKILL.md) | Retain | Run the established workflow once against a bound source and destination. |
| [inspect-artifact-state](../../skills/inspect-artifact-state/SKILL.md) | Retain | Inspect existing artifact state through a bound read-only source. Detailed ecosystem methods already load on demand. |
| [prepare-version-notes](../../skills/prepare-version-notes/SKILL.md) | Retain | Compare evidenced versions and prepare scoped change notes after the target version is selected. |
| [redeploy-local](../../skills/redeploy-local/SKILL.md) | Retain with follow-up | Build and restart locally. Review the conflict between completion and optional health-check handling. |
| [scaffold-agent-tests](../../skills/scaffold-agent-tests/SKILL.md) | Retain | Create traceable test scaffolding from an agreed agent-testing contract. |
| [upgrade-dependencies](../../skills/upgrade-dependencies/SKILL.md) | Retain | Upgrade the selected dependencies in verified batches with migration and compatibility evidence. |

### Version control

| Skill | Result | Scope or change |
| --- | --- | --- |
| [commit-work](../../skills/commit-work/SKILL.md) | Retain with follow-up | Create scoped commits from exact staged changes. Review the ordering conflict with the canonical catalog's source-pin prerequisite. |
| [deliver-feature](../../skills/deliver-feature/SKILL.md) | Earlier patch 1.1.3 verified | Deliver one feature from its linked worktree. The earlier patch separated examples from merge, push and cleanup decisions. |
| [integrate-branches](../../skills/integrate-branches/SKILL.md) | Retain | Integrate a selected batch from the main worktree. Its existing examples are separate. |

### Project foundations

| Skill | Result | Scope or change |
| --- | --- | --- |
| [define-docs-norms](../../skills/define-docs-norms/SKILL.md) | Retain | Persist an approved documentation policy under the project's authoritative path. |
| [generate-agent-entry](../../skills/generate-agent-entry/SKILL.md) | Retain with follow-up | Author or audit the project entry point. Review how authoring completion applies commit authorization. |
| [generate-github-workflow](../../skills/generate-github-workflow/SKILL.md) | Retain | Generate a project-scoped Actions workflow. Specialized release examples already have references. |
| [generate-standard-readme](../../skills/generate-standard-readme/SKILL.md) | Retain | Create or revise a project README against its existing audience and purpose. |
| [manage-secret](../../skills/manage-secret/SKILL.md) | Retain with follow-up | Own personal macOS Keychain operations. Review the exposure of values through command arguments and output. |
| [refine-skill-design](../../skills/refine-skill-design/SKILL.md) | Refined to 1.10.1 | Audit existing Skills. The procedure now checks strict validation, distinguishes version impacts and identifies the preview and formal catalog prerequisites. |

### Collaboration

| Skill | Result | Scope or change |
| --- | --- | --- |
| [consume-nats-message](../../skills/consume-nats-message/SKILL.md) | Retain | Drain pending messages through discovered NATS operations and report message handling outcomes. |
| [decontextualize-text](../../skills/decontextualize-text/SKILL.md) | Retain | Remove private or organization-specific references while preserving usable meaning. |
| [eli5](../../skills/eli5/SKILL.md) | Retain | Produce a simple visual explanation for the selected subject and audience. |
| [ponytail](../../skills/ponytail/SKILL.md) | Earlier patch 1.0.2 verified | Apply an explicitly requested minimal-change mode. The earlier patch aligned discovery with activation. |
| [prepare-presales-response](../../skills/prepare-presales-response/SKILL.md) | Retain | Prepare evidence-backed responses and scoped files without taking on product or contractual authority. |
| [produce-presentation-video](https://github.com/nesnilnehc/ai-cortex/blob/705691a6ae50b33b47c72a090dfdbd52bd704593/skills/produce-presentation-video/SKILL.md) | Retain | Deliver or repair a verified narrated video. Tool, provider and production details have their own loading points. |
| [publish-nats-message](../../skills/publish-nats-message/SKILL.md) | Retain | Send a message under the producer contract and report the outcome or acknowledgement. |
| [rename-session](../../skills/rename-session/SKILL.md) | Retain | Rename or suggest a title for the current session, with a fallback when the host lacks the operation. |
