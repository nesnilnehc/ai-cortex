---
artifact_type: assessment
lifecycle: living
created_at: 2026-10-23
status: complete
---

# AI Cortex 1.0 readiness

Assessment baseline: `1ef7026a27cc52ab7e7cb606144e8e8dc740be1e`, following 0.5.1 publication on 2026-10-23. Tested installer content is `485d787561427d10ed0208ffef566427b4100811`; release tag `v0.5.1` targets `95a1e001afb49e04368a7d12dd1aace92c583ff9`. The subsequent commit records the publication receipt. The maintainer approved the bounded [1.0 core and compatibility policy](stable-core.md) on 2026-10-23. This assessment tracks its admission evidence; it is not a roadmap promotion or release authorization.

## Decision

Do not release 1.0 yet. Core definitions, versioned assets and reproducible release preparation exist. The three reproduced installer ownership/rollback defects are resolved in 0.5.1, with permanent regression tests and Linux/macOS CI. The stable scope, experimental boundary, compatibility/deprecation rules and latest-stable security strategy are now approved and documented. Remaining gaps are supported-consumer fixtures, actual personal-project acceptance, host/environment acceptance, applicable adopter evidence and a tested stable-release upgrade entry. The patch closes the installation findings; it does not establish the broader 1.x guarantee.

A personal tool can legitimately reach 1.0. On 2026-10-23 the maintainer confirmed that use is primarily personal and no consuming-project acceptance records are available. Do not equate this with no real use, nor with independently verified cross-team production adoption. The selected core covers project adoption, review/repair and commit/release; validate those workflows before broadening the promise.

[SemVer 2.0.0](https://semver.org/spec/v2.0.0.html), accessed 2026-10-23, makes 1.0 the definition of a public API. Its sections 1, 5, 7 and 8 require a declared boundary and compatible version evolution; it does not prescribe a user count, a stability-period length or a particular test count. The stable-core policy now defines the approved target; this report separates that decision from uncompleted verification.

## Evidence and remaining gaps

| Dimension | Satisfied or verified | Remaining gap | Assessment |
| --- | --- | --- | --- |
| Core definitions | [AGENTS](../../AGENTS.md), [terminology](../architecture/terminology.md) and registries distinguish Skills, Specs, Protocols and Rules; installation/loading authority is explicit | [Stable-core inventory](stable-core.md#stable-contract-and-inventory) selects entry Skills, conditional reviewers and shared dependencies; consumer fixtures must prove protected contracts | Scope decision resolved; verification pending |
| Version discipline | Product tags and independent asset versions are separate. The 0.5.0 package verifies 85 edited versioned assets moved their versions | [Compatibility and deprecation](stable-core.md#compatibility-and-deprecation) and independent/product version rules are adopted; old/new consumer fixtures remain missing | Policy resolved; compatibility evidence pending |
| Behavioral evidence | Existing live roadmap trace passes the canonical freshness/completeness validator: 10 cases and 30 turns | Bounded JSON decision adapter plus real local renderer; not unrestricted agent editing, a production project acceptance or a live external adapter acceptance. Provider model ID is not exposed | Real but narrow evidence |
| Actual use | Maintainer confirms personal use. The 0.5.0 and 0.5.1 Release Packages and GitHub receipts establish this repository's own preparation/publication flow was used | No supplied consuming-project requirement-to-acceptance trace; no independently verified multi-project or multi-agent acceptance matrix | Personal use and self-hosting; broader evidence absent |
| Rule activation | [Rule modeling](../../specs/rule-modeling.md#52-rule-item-contract) derives 118 ready items from nonempty activation rows; recorded release validation passes | OBS-003, PERF-007, REL-008 and TST-008 still use `Verification: adopter`. Required return fixtures are not substituted by the ready count | Activation materials complete; adopter evidence still owed |
| Installation/update | 0.5.1 fixes ownership and cleanup; 22 permanent integration tests pass locally and on Linux/macOS CI, including foreign links, markers, repeated install, rollback and dirty-update refusal | macOS/Linux POSIX installer target selected; record exact accepted OS/shell/Git and host versions. IDE runtime discovery and Windows were not verified. Filesystem fault injection and concurrent writers are outside current evidence | Three findings resolved; bounded installer evidence present |
| Release and recovery | 0.5.1 has a verified annotated tag, notes, changelog and publication receipt; actual 0.5.0 → 0.4.0 asset rollback with a retained fixed manager verifies exact membership and no broken managed links | Older tags retain older installers: the fixed manager must remain outside the clone and be used explicitly while pinned. Consuming-project edits require separate recovery | Reported stale-asset defect resolved; recovery procedure bounded and verified |
| Support | [SECURITY](../../SECURITY.md) retains current 0.x main support and adopts latest-stable support starting at 1.0; no older-pin backport or LTS promise; response timelines retained | Implement/test the stable-release upgrade entry without changing current update semantics; host acceptance remains pending | Strategy decision resolved; upgrade delivery pending |

## Resolved installation findings

The initial 0.5.0 assessment executed eight isolated checks: five passed and three
failed. Those failures are historical reproduction evidence, not the current
installer result. All three are resolved by fix commit
`485d787561427d10ed0208ffef566427b4100811`, included in 0.5.1.

| Original finding | Status | Fix and regression evidence |
| --- | --- | --- |
| Foreign same-name rule symlink overwritten | Resolved in 0.5.1 | Rule installation preserves valid and broken foreign links; Cursor generation also preserves symlinks to marked foreign files |
| Foreign prefix-similar skill link removed | Resolved in 0.5.1 | Shared literal direct-child ownership checks cover install, prune, scope cleanup and uninstall; regression cases include similar prefixes, traversal, pattern characters and trailing slashes |
| Pin/reinstall rollback leaves stale installed assets | Resolved in 0.5.1 with retained fixed manager | Install now prunes before synchronization; regression cases verify obsolete skills/rules and generated translations are removed, including global-to-on-demand scope changes |

### Permanent verification and release evidence

- [Installer suite](../../scripts/test-cortex-installer.py): 22 real POSIX CLI
  integration tests using isolated homes, fixture assets and local Git origins.
  The suite also checks positive managed refresh, idempotency, user-owned real
  files, dirty-update refusal and ordinary uninstall.
- TDD records in the [0.5.1 manifest](../../.cortex/release/0.5.1/manifest.yaml)
  retain the red-to-green evidence: the original installer failed 12 of the first
  17 cases; additional trailing-slash and status cases also failed before repair.
  The final 22 cases passed locally.
- [CI run 39923150165](https://github.com/nesnilnehc/ai-cortex/actions/runs/39923150165)
  passed links, shell, Markdown, registry and both installer jobs on the tested
  content SHA. The [workflow](../../.github/workflows/lint.yml) permanently runs
  the suite on `ubuntu-latest` and `macos-latest`. The PR-only translation job was
  skipped on this push, not counted as a passed check.
- Separate local tagged-asset recovery installed actual 0.5.0 assets (70 skills per
  IDE), then actual 0.4.0 assets (68), using the retained fixed manager. Exact skill
  and global-rule membership and absence of broken managed links were verified
  across generic, Claude and Cursor installation directories.
- The [0.5.1 Release](https://github.com/nesnilnehc/ai-cortex/releases/tag/v0.5.1)
  and manifest record the successful publication, annotated tag target and note
  body verification. The tag adds only the three release artifacts after the
  tested implementation commit; the later receipt commit does not change code.

### Recovery boundary and unverified behavior

Use the [installer recovery guide](../guides/installer-recovery.md) and
[release upgrade/rollback notes](../../.cortex/release/0.5.1/release-notes.md).
Checking out an old tag also restores its old `bin/cortex`; the patch does not
retroactively repair old tags. Retain a 0.5.1-or-newer manager outside the clone
and use it explicitly with `CORTEX_HOME` while pinned to old assets. Ordinary
`cortex update` follows the default branch and does not maintain a release pin.

These results verify installed files and links, not discovery or invocation inside
running IDE agents. No Windows acceptance, filesystem fault injection, concurrent
writer safety or large-home benchmark was established. Installation remains
nontransactional. These are scope limits to resolve or explicitly exclude from
1.0 claims, not evidence that the three repaired cases still fail. The selected
asset rollback does not restore consuming-project documents or remote pages.

## Approved scope and policy

The maintainer approved [Stable core and compatibility policy](stable-core.md)
on 2026-10-23. It is the canonical membership/dependency and versioning source;
[SECURITY](../../SECURITY.md) owns the support transition and response timelines.
Selection of the core is complete. No asset was promoted on a test count alone.

Admission work remains: supported old/new consumer fixtures for protected shared
contracts, actual personal-project acceptance for the selected chains, exact
OS/shell/Git/host acceptance records, and delivery of the stable-release upgrade
entry. `cortex update` still follows the remote default branch and can discard
clean local-only commits; it does not preserve a release pin. This policy update
changes no installer behavior and does not imply those gaps have closed.

The inventory includes conditional language/framework reviewers and globally
loaded Rules, not just top-level Skills. Experimental generation, research,
planning, remote adapters and optional media cannot change stable dependencies
incompatibly under an experimental label. Their independent real-use maturity
must not be inferred from inclusion in the catalog.

## Real-use evidence to collect

Use actual personal projects already relying on the intended core. For each selected workflow, retain the Cortex tag/asset versions, host/agent and tools, original requirement, invoked assets, review findings, repairs, final acceptance result and known limitations. Preserve failures and user interventions. Private evidence can stay private; a redacted result and reviewable pointer are sufficient if the claim can be audited.

Prioritize project entry/loading → review/repair → functional acceptance → commit/release in actual personal projects, tracing findings and release-package handoffs. Requirements and implementation provide host context; their automatic generation is not a stable workflow claim. Planning-maintenance, remote and multi-agent chains remain experimental and need not block this bounded core. Any broader claim requires materially different contexts and its own evidence. Counts follow the claim and risk, not a universal 1.0 threshold.

For the four adopter Rule items, follow the existing [contribution return procedure](../../CONTRIBUTING.md#returning-forward-test-evidence): three representative shapes for each applicable population, implemented evaluation and a demonstrated red run when that check is removed. Alternatively, keep those items outside the stable evidence claim and state the limitation; do not rename `adopter` or manufacture fixtures without a representative population.

The project's [roadmap](../process-management/roadmap.md) and [checkpoint definitions](../process-management/roadmap-strategy.md#checkpoint-definitions) retain unresolved M5/M6/M7 denominator, threshold and production-evidence differences. Resolve these before citing them as completion evidence. They are not already-approved 1.0 gates, and this assessment does not promote work or redefine them.

## Recommended progression

Completed prerequisites: consistent installer ownership checks, complete managed
asset resynchronization with the retained manager, permanent regression tests,
Linux/macOS CI, recovery documentation and the 0.5.1 corrective release. Do not
schedule those same defects again without new failing evidence.

| Order | Remaining proposed work | Completion evidence | Indicative story points |
| --- | --- | --- | ---: |
| Complete | Select stable scope and compatibility/support strategy | Approved policy, explicit dependency inventory, security transition and experimental boundaries documented; admission evidence remains separate | — |
| 1 | Deliver the stable-release upgrade entry and exact supported-host acceptance | Existing update semantics retained; stable selection/upgrade and retained-manager recovery verified; primary host versions and real discovery/invocation recorded | 5 |
| 2 | Add supported-consumer compatibility cases for the selected core | Versioned old/new consumer fixtures verify promised output contracts, enum semantics, adopted schemas and upgrade behavior; unsupported cases are explicitly bounded | 5 |
| 3 | Record acceptance in actual personal projects | Auditable adoption, review/repair and commit/release chains retain versions, environment, inputs, findings, interventions and outcomes; optional planning/remote chains remain outside stable admission | 5 |
| 4 | Resolve adopter evidence and strategic thresholds within that scope | Representative Rule return fixtures or an explicit exclusion from stable evidence claims; reconcile M5/M6/M7 definitions if they are used for admission | 3 |
| 5 | Rehearse a bounded 1.0 candidate | Approved core passes installer, consumer and project gates; supported environments and upgrade/recovery are exercised; prepare-release determines readiness before an authorized publication | 3 |

These estimates are planning advice, not scheduled commitments. Scope selection is complete. Upgrade/host work,
consumer fixtures and personal-project evidence can proceed together; adopter
returns can be collected in the same real projects. Final rehearsal depends on
those results and uses the existing installer suite as a baseline rather than
substituting it for consumer acceptance. No extra feature, fixed user count,
release date, RC count or observation period is imposed by this assessment.

## Search and verification limits

The original assessment reviewed the root entry and registries, terminology,
README/CONTRIBUTING/SECURITY, release guidance and 0.4.0/0.5.0 records, CI and
repository validators, roadmap sources, the four adopter rows, roadmap live
validation and installer behavior. Local adopter-entry spot checks in shijian,
laya and deepseek-harness were not an exhaustive acceptance-record search. The
maintainer's statement remains the basis for the personal-use assessment.

This update checked the 0.5.1 implementation and permanent test cases, CI
configuration, release manifest and recovery instructions against that baseline.
It reuses the recorded successful local and Linux/macOS runs and actual tagged
asset recovery; it does not claim a new execution of those behavioral tests or a
new live-model/project/IDE acceptance run. The subsequent policy update resolves the scope and support decisions through
explicit maintainer approval. Consumer, adopter and host evidence and upgrade
delivery remain open. No roadmap promotion or 1.0 release is authorized by this
document. Documentation links, hygiene and Markdown formatting
are checked for this update.
