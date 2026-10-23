---
artifact_type: governance
lifecycle: living
created_at: 2026-10-23
status: active
---

# Stable core and compatibility policy

Approved by the maintainer on 2026-10-23 for the 1.0 preparation scope, based on
0.5.1. This document owns stable membership, compatibility and version policy.
[SECURITY](../../SECURITY.md) owns security support and response commitments.
The [readiness assessment](release-readiness.md) owns evidence and open gaps.
Approval selects the target contract; it does not certify unverified capabilities
or authorize a 1.0 release. Existing 0.x releases are not retroactively stable.

## Stable contract and inventory

The intended use is maintainer-led work in personal software projects: explicitly
adopt assets, run review and acceptance, repair bounded findings, then commit and
release with authorization. Stable means predictable contracts and authority
boundaries, not identical model prose, exhaustive defect detection or equal
performance across models. Project instructions and human authorization remain
controlling; installed assets do not automatically adopt a project workflow.

The following entry Skills are the stable 1.0 target. Their names, local defining
paths, documented inputs/defaults, output contracts, failure/stop conditions and
authorization boundaries are protected:

- [skills/generate-agent-entry/SKILL.md](../../skills/generate-agent-entry/SKILL.md)
- [skills/automate-tests/SKILL.md](../../skills/automate-tests/SKILL.md)
- [skills/review-diff/SKILL.md](../../skills/review-diff/SKILL.md)
- [skills/review-implementation-alignment/SKILL.md](../../skills/review-implementation-alignment/SKILL.md)
- [skills/orchestrate-code-review/SKILL.md](../../skills/orchestrate-code-review/SKILL.md)
- [skills/orchestrate-repair-loop/SKILL.md](../../skills/orchestrate-repair-loop/SKILL.md)
- [skills/commit-work/SKILL.md](../../skills/commit-work/SKILL.md)
- [skills/prepare-release/SKILL.md](../../skills/prepare-release/SKILL.md)
- [skills/publish-release/SKILL.md](../../skills/publish-release/SKILL.md)

### Conditional execution dependencies

The code-review orchestrator selects scope, language, framework and library
reviewers as applicable, and runs the seven cognitive reviewers in its declared
order. The following are stable dependencies with the same contract protection;
listing them is not evidence that every stack has passed host acceptance:

- [skills/review-codebase/SKILL.md](../../skills/review-codebase/SKILL.md)
- [skills/review-typescript/SKILL.md](../../skills/review-typescript/SKILL.md)
- [skills/review-python/SKILL.md](../../skills/review-python/SKILL.md)
- [skills/review-go/SKILL.md](../../skills/review-go/SKILL.md)
- [skills/review-java/SKILL.md](../../skills/review-java/SKILL.md)
- [skills/review-php/SKILL.md](../../skills/review-php/SKILL.md)
- [skills/review-powershell/SKILL.md](../../skills/review-powershell/SKILL.md)
- [skills/review-dotnet/SKILL.md](../../skills/review-dotnet/SKILL.md)
- [skills/review-sql/SKILL.md](../../skills/review-sql/SKILL.md)
- [skills/review-react/SKILL.md](../../skills/review-react/SKILL.md)
- [skills/review-vue/SKILL.md](../../skills/review-vue/SKILL.md)
- [skills/review-orm-usage/SKILL.md](../../skills/review-orm-usage/SKILL.md)
- [skills/review-security/SKILL.md](../../skills/review-security/SKILL.md)
- [skills/review-reliability/SKILL.md](../../skills/review-reliability/SKILL.md)
- [skills/review-error-surfacing/SKILL.md](../../skills/review-error-surfacing/SKILL.md)
- [skills/review-performance/SKILL.md](../../skills/review-performance/SKILL.md)
- [skills/review-architecture/SKILL.md](../../skills/review-architecture/SKILL.md)
- [skills/review-observability/SKILL.md](../../skills/review-observability/SKILL.md)
- [skills/review-testing/SKILL.md](../../skills/review-testing/SKILL.md)

`prepare-release` optionally dispatches `changelog-video`, and publication or
review may use project tooling. Those extensions remain experimental or external.
Their existing selection, authorization, missing-capability and failure reporting
contracts are stable; success of the extension is not implied by the core.
External tool versions and project test commands belong to the host acceptance
matrix, not a promise to support every provider indefinitely.

### Shared contracts, constraints and references

The inventory below includes transitive local Markdown references from the
Skills above and all globally loaded Rules (`recommended_scope: user` or `both`)
at source baseline `1ef7026a27cc52ab7e7cb606144e8e8dc740be1e`. It deliberately includes reference-only material so a
reviewer can inspect the complete linked surface. It is not an instruction to
load every reference on every invocation.

Specs protect the fields, enums, identifiers, meanings, compatibility paths and
obligations actually consumed by stable execution. Rules protect applicable
obligations and applicability/waiver semantics. Guides protect the configuration,
loading and handoff sections used by the core; tutorials and unrelated examples
are supporting references, not additional stable workflows. Requirement, design,
task and roadmap contracts used as review inputs are protected dependencies;
automatic generation or governance of those artifacts remains experimental.

- [docs/guides/document-decision-tree.md](../../docs/guides/document-decision-tree.md)
- [docs/guides/engineering-quality-governance.md](../../docs/guides/engineering-quality-governance.md)
- [docs/guides/project-config.md](../../docs/guides/project-config.md)
- [docs/guides/research-skills-usage.md](../../docs/guides/research-skills-usage.md)
- [docs/guides/ui-design-decisions.md](../../docs/guides/ui-design-decisions.md)
- [rules/adr-management.md](../../rules/adr-management.md)
- [rules/agentic-artifact-paradigm.md](../../rules/agentic-artifact-paradigm.md)
- [rules/architecture-quality.md](../../rules/architecture-quality.md)
- [rules/claude-md-management.md](../../rules/claude-md-management.md)
- [rules/diagram-selection.md](../../rules/diagram-selection.md)
- [rules/doc-health-criteria.md](../../rules/doc-health-criteria.md)
- [rules/error-surfacing-quality.md](../../rules/error-surfacing-quality.md)
- [rules/functional-design-quality.md](../../rules/functional-design-quality.md)
- [rules/implementation-alignment-quality.md](../../rules/implementation-alignment-quality.md)
- [rules/observability-quality.md](../../rules/observability-quality.md)
- [rules/performance-quality.md](../../rules/performance-quality.md)
- [rules/reliability-quality.md](../../rules/reliability-quality.md)
- [rules/repo-structure-hygiene.md](../../rules/repo-structure-hygiene.md)
- [rules/requirement-intake-triage.md](../../rules/requirement-intake-triage.md)
- [rules/requirement-quality.md](../../rules/requirement-quality.md)
- [rules/roadmap-quality.md](../../rules/roadmap-quality.md)
- [rules/security-quality.md](../../rules/security-quality.md)
- [rules/standards-agent-testing.md](../../rules/standards-agent-testing.md)
- [rules/standards-coding.md](../../rules/standards-coding.md)
- [rules/standards-import.md](../../rules/standards-import.md)
- [rules/standards-shell.md](../../rules/standards-shell.md)
- [rules/standards-test-code.md](../../rules/standards-test-code.md)
- [rules/task-quality.md](../../rules/task-quality.md)
- [rules/technical-design-quality.md](../../rules/technical-design-quality.md)
- [rules/test-case-quality.md](../../rules/test-case-quality.md)
- [rules/test-coverage-quality.md](../../rules/test-coverage-quality.md)
- [rules/testing-quality.md](../../rules/testing-quality.md)
- [rules/workflow-documentation.md](../../rules/workflow-documentation.md)
- [rules/workflow-rule-governance.md](../../rules/workflow-rule-governance.md)
- [rules/writing-chinese-technical.md](../../rules/writing-chinese-technical.md)
- [specs/adr-modeling.md](../../specs/adr-modeling.md)
- [specs/agent-test-modeling.md](../../specs/agent-test-modeling.md)
- [specs/claude-md-modeling.md](../../specs/claude-md-modeling.md)
- [specs/findings-list.md](../../specs/findings-list.md)
- [specs/functional-design-modeling.md](../../specs/functional-design-modeling.md)
- [specs/opportunity-package.md](../../specs/opportunity-package.md)
- [specs/release-package.md](../../specs/release-package.md)
- [specs/requirement-modeling.md](../../specs/requirement-modeling.md)
- [specs/research-evidence.md](../../specs/research-evidence.md)
- [specs/roadmap-modeling.md](../../specs/roadmap-modeling.md)
- [specs/rule-modeling.md](../../specs/rule-modeling.md)
- [specs/spec-modeling.md](../../specs/spec-modeling.md)
- [specs/task-modeling.md](../../specs/task-modeling.md)
- [specs/technical-design-modeling.md](../../specs/technical-design-modeling.md)
- [specs/test-case-modeling.md](../../specs/test-case-modeling.md)
- [specs/test-coverage-modeling.md](../../specs/test-coverage-modeling.md)
- [specs/universal-notification.md](../../specs/universal-notification.md)

Additional local dependencies and authority sources are:

- [AGENTS.md](../../AGENTS.md): project identity, loading and authority order.
- [Skills](../../skills/INDEX.md), [Specs](../../specs/INDEX.md),
  [Protocols](../../protocols/INDEX.md), [Rules](../../rules/INDEX.md): discovery
  paths and mappings; catalog inclusion alone does not confer stable status.
- [Terminology](../architecture/terminology.md), [mission](mission.md),
  [vision](vision.md) and [asset naming](../architecture/asset-naming.md):
  identity and asset interpretation used by project entry/loading.
- [Artifact norms](../ARTIFACT_NORMS.md) and [language scheme](../LANGUAGE_SCHEME.md):
  repository maintenance inputs; consuming projects retain their own norms.
- [Vendored sources](../../skills/SOURCES.yaml) and
  [commit template](../../skills/commit-work/references/commit-message-template.md):
  provenance and commit format.
- [Recovery guide](../guides/installer-recovery.md) and
  [release guide](../guides/releasing.md): management and publication procedures.

The inventory protects consumed contract sections, not all future capabilities
mentioned by an authority or tutorial. The installer translates Rule metadata
and body for Cursor; that ownership and translation behavior is also protected.
References to consumer `AGENTS.md`, `CLAUDE.md`, `README.md`, `CONTRIBUTING.md`,
`TESTING.md` and `.ai-cortex/config.yaml` describe host inputs, not files this
repository promises to create. Configuration keys consumed by the core, including
`test_command`, `base_branch` and `governance` fields, retain their documented
meaning; research-only configuration remains outside this scope.

The public installer surface is [bin/cortex](../../bin/cortex): `install`,
`upgrade`, `update`, `status`, `uninstall`, their documented options, root resolution through
`CORTEX_HOME`/`XDG_DATA_HOME`, installed locations and ownership boundaries.
`status` is human-readable, not a machine-output schema. `update` follows the
remote default branch; it does not preserve a release pin. Unknown flags and
private helpers are not public APIs. `clean` is an experimental legacy-migration
operation, not part of the stable command surface.

### Dependency maintenance

A core change must review new direct, transitive, conditional and globally loaded
dependencies against this inventory. A required experimental behavior must either
be promoted with acceptance evidence or isolated behind an optional boundary
whose absence cannot break stable execution. Do not move an existing protected
contract outside the stable set to avoid a major version. Update this inventory
when adding references, registry entries or global Rules; inventory presence alone
does not establish successful verification.

## Experimental boundary and promotion

Every Skill not named above, and every unlisted Spec/Protocol/Rule behavior not
consumed by the core, is outside the initial stable promise. This includes
requirements/design/task generation, roadmap generation and governance routing,
research and presales, remote knowledge-base adapters, NATS, IM notification,
release media, and autonomous cross-project or multi-agent execution. The existing
catalog remains available; classification does not remove assets or relax rules.
Installation continues to distribute the catalog, not a stable-only subset.

Experimental changes may break compatibility in a product MINOR, with independent
asset version changes, explicit release-note impact and migration instructions.
No silent breaking change is permitted through a stable dependency. Promotion
requires a named contract, representative consumer fixtures, real-use evidence
and host acceptance relevant to its claims, plus an inventory update in a MINOR.
The four adopter-backed items OBS-003, PERF-007, REL-008 and TST-008 remain
conditionally mandatory; missing return fixtures mean evidence-limited, not
passed, optional or disabled. Do not claim their populations are verified before
following the existing contribution return procedure.

## Compatibility and deprecation

For 1.x stable consumers, classify actual effects, not file type or commit prefix:

| Product change | Version action |
| --- | --- |
| Correct an error to restore the declared behavior, or clarify wording without changing obligations | PATCH |
| Add a backward-compatible optional capability, or announce deprecation | MINOR |
| Remove/rename a stable entry or path, change field/enum meaning, add a required obligation, or change default authorization behavior | MAJOR |

Additional fields or enum members are compatible only when supported old readers
can accept them. Preserve old supported consumer fixtures and test both old and
new inputs. Wording changes that add work, permissions or output requirements
are behavioral changes. Existing consumer artifacts need no silent rewrite.
Fixing unsafe implementation behavior to match an existing protection contract
can be a PATCH; a genuinely incompatible contract change requires a MAJOR even
when motivated by security, with impact and mitigation made explicit.

Announce deprecation in a MINOR with affected contracts, replacement, migration
example and intended removal major. Keep the old entry or compatible reader for
the rest of the current major. Removal is allowed only in a later MAJOR after
old-consumer and migration fixtures demonstrate the transition. No fixed time
window or parallel old-major maintenance is promised. Published tags and released
changelog sections are immutable. A retained tag is not a maintained release.

## Version and distribution strategy

Product SemVer lives only in Git tags. Assets keep independent frontmatter
versions; any edited asset still moves its own version. An incompatible stable
asset or dependency contract forces a product MAJOR regardless of its independent
number. Adding experimental capabilities does not freeze the whole catalog.
[Contribution versioning](../../CONTRIBUTING.md#versioning) applies to the asset;
this policy supplies the additional product-level decision.

Starting at 1.0, the latest stable Release is the target for everyday use and
compatible maintenance. Until then, the current 0.x security policy targets main. Older releases receive no per-version backport promise; upgrade to
the latest stable release for fixes. There is no default LTS or parallel major
maintenance. `main` is the development and early-validation channel, not evidence
that a development snapshot satisfies release compatibility. Pre-release tags
are candidates, not stable releases. Security support is defined in SECURITY.

Release 0.6.0 provides `cortex upgrade [version]` for stable
origin-tag selection, with isolated regression coverage and existing `update`
semantics retained. This entry is not retroactively present in older tags.
Primary-host discovery/invocation acceptance remains required before 1.0.
Rollback to older installers
requires the retained fixed manager in the [recovery guide](../guides/installer-recovery.md).
Protect local work, disclose that installation is nontransactional, and do not
promise source rollback restores project documents or external state.

## Supported environment target and admission

The initial installer target is macOS and Linux with POSIX shell and Git. Current
CI on `macos-latest` and `ubuntu-latest` verifies installation behavior, not a
minimum OS version or an IDE runtime. Windows is unverified. Before 1.0, retain
actual OS/shell/Git and host/agent versions and discovery/invocation results in the
readiness evidence. Accept the maintainer's primary host first; add hosts only
after their own acceptance. Do not infer Claude, Cursor or Codex runtime support
from symlink creation alone. Model quality has no universal guarantee.

Scope approval is complete; consumer compatibility fixtures, personal-project
acceptance, environment records and applicable adopter evidence remain admission work;
the upgrade entry shipped in 0.6.0 and still needs primary-host acceptance. A candidate rehearsal must verify those
against this bounded scope before the normal release preparation/publication.

## Consumer compatibility evidence

The [consumer compatibility guide](../guides/consumer-compatibility.md) records
pinned historical/current reference-reader coverage and its limits. This is a
partial evidence matrix; reference fixtures do not substitute for actual
personal-project or host acceptance and do not promote experimental capabilities.
