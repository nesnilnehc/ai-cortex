---
artifact_type: assessment
lifecycle: living
created_at: 2026-10-23
status: complete
---

# AI Cortex 1.0 readiness

Assessment baseline: `1ef7026a27cc52ab7e7cb606144e8e8dc740be1e`, following 0.5.1 publication on 2026-10-23. Tested installer content is `485d787561427d10ed0208ffef566427b4100811`; release tag `v0.5.1` targets `95a1e001afb49e04368a7d12dd1aace92c583ff9`. The subsequent commit records the publication receipt. The maintainer approved the bounded [1.0 core and compatibility policy](stable-core.md) on 2026-10-23. This assessment tracks its admission evidence; it is not a roadmap promotion or release authorization.

## Decision

Do not release 1.0 yet. Core definitions, versioned assets and reproducible release preparation exist. The three reproduced installer ownership/rollback defects are resolved in 0.5.1, with permanent regression tests and Linux/macOS CI. The stable scope, experimental boundary, compatibility/deprecation rules and latest-stable security strategy are now approved and documented. A bounded historical/current reference-consumer suite now covers Findings, Release Package and Rule coverage. A live Codex CLI rehearsal on a scoped Shijian committed snapshot now verifies explicit installed-asset review/repair invocation. A real personal-site closeout now records permanent adoption, CI/documentation repairs, browser acceptance and a scoped commit/push. Remaining gaps include broader product-code delivery, other core dependencies, wider host configuration and real future deprecation migrations, host/environment acceptance and applicable adopter evidence. The stable upgrade entry shipped in 0.6.0; the canonical macOS/Codex CLI upgrade, 0.5.1 rollback and stable recovery cycle now passes with original-state restoration. The patch closes the installation findings; it does not establish the broader 1.x guarantee.

A personal tool can legitimately reach 1.0. On 2026-10-23 the maintainer confirmed that use is primarily personal and no consuming-project acceptance records are available. Do not equate this with no real use, nor with independently verified cross-team production adoption. The selected core covers project adoption, review/repair and commit/release; validate those workflows before broadening the promise.

[SemVer 2.0.0](https://semver.org/spec/v2.0.0.html), accessed 2026-10-23, makes 1.0 the definition of a public API. Its sections 1, 5, 7 and 8 require a declared boundary and compatible version evolution; it does not prescribe a user count, a stability-period length or a particular test count. The stable-core policy now defines the approved target; this report separates that decision from uncompleted verification.

## Evidence and remaining gaps

| Dimension | Satisfied or verified | Remaining gap | Assessment |
| --- | --- | --- | --- |
| Core definitions | [AGENTS](../../AGENTS.md), [terminology](../architecture/terminology.md) and registries distinguish Skills, Specs, Protocols and Rules; installation/loading authority is explicit | [Stable-core inventory](stable-core.md#stable-contract-and-inventory) selects entry Skills, conditional reviewers and shared dependencies; reference-consumer fixtures cover selected protected contracts; remaining dependencies and actual consumers still need acceptance | Scope decision resolved; partial compatibility evidence |
| Version discipline | Product tags and independent asset versions are separate. The 0.5.0 package verifies 85 edited versioned assets moved their versions | [Compatibility and deprecation](stable-core.md#compatibility-and-deprecation) and independent/product version rules are adopted; old/current reference fixtures now cover Findings, Release Package and coverage; bounded configuration, parameter/waiver and synthetic deprecation cases now supplement those fixtures; real-host/remaining dependency cases remain missing | Policy resolved; bounded evidence present |
| Behavioral evidence | Existing live roadmap trace passes the canonical freshness/completeness validator: 10 cases and 30 turns | Bounded JSON decision adapter plus real local renderer; not unrestricted agent editing, a production project acceptance or a live external adapter acceptance. Provider model ID is not exposed | Real but narrow evidence |
| Actual use | Maintainer confirms personal use. The 0.5.0 and 0.5.1 Release Packages and GitHub receipts establish this repository's own preparation/publication flow was used | [Live host record](host-acceptance.md) adds a controlled requirement-to-review/repair/test trace on real project code; a subsequent permanent personal-site adoption and real CI/documentation closeout is now recorded; wider product-code chains and independent contexts remain unverified | Personal use, self-hosting, live rehearsal and one organic closeout |
| Rule activation | [Rule modeling](../../specs/rule-modeling.md#52-rule-item-contract) derives 118 ready items from nonempty activation rows; recorded release validation passes | OBS-003, PERF-007, REL-008 and TST-008 still use `Verification: adopter`. Required return fixtures are not substituted by the ready count | Activation materials complete; adopter evidence still owed |
| Installation/update | 0.5.1 fixes ownership and cleanup; 22 permanent integration tests pass locally and on Linux/macOS CI, including foreign links, markers, repeated install, rollback and dirty-update refusal | macOS/Linux POSIX installer target selected; exact macOS/shell/Git/CLI versions and canonical installation recovery are now recorded. Automatic desktop discovery, normal user configuration and Windows were not verified. Filesystem fault injection and concurrent writers are outside current evidence | Three findings resolved; bounded installer evidence present |
| Release and recovery | 0.5.1 has a verified annotated tag, notes, changelog and publication receipt; actual 0.5.0 → 0.4.0 asset rollback with a retained fixed manager verifies exact membership and no broken managed links | Older tags retain older installers: the fixed manager must remain outside the clone and be used explicitly while pinned. Consuming-project edits require separate recovery | Reported stale-asset defect resolved; recovery procedure bounded and verified |
| Support | [SECURITY](../../SECURITY.md) retains current 0.x main support and adopts latest-stable support starting at 1.0; no older-pin backport or LTS promise; response timelines retained | Upgrade entry shipped in 0.6.0; canonical Mac CLI selection/rollback/recovery now verified. Additional host/configuration claims require their own evidence | Strategy, upgrade delivery and bounded primary-host cycle verified |

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
contracts, actual personal-project acceptance for the selected chains, wider
host/configuration records and remaining core acceptance. The canonical macOS/CLI
upgrade entry shipped in 0.6.0 now has a recorded stable selection, rollback and
recovery cycle below with exact environment versions. `cortex update` still follows the remote default branch and can discard
clean local-only commits; it does not preserve a release pin. The scope policy itself
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
| Complete (primary Mac CLI) | Stable upgrade, rollback and recovery on canonical installation | Verified backup, actual 0.6.0 → 0.5.1 → 0.6.0 switches, three live adopted-project CLI runs, independent project/browser checks and exact original installation restoration; broader desktop/configuration claims remain separate | — |
| 2 (partial) | Expand reference coverage to actual consumers and remaining dependencies | Findings, Release Package, configuration and Rule parameter/waiver reference cases pass; synthetic deprecation and actual 0.x legacy installation migration are covered. Align the observed review-diff field wording with Findings and verify a nonempty host finding; full host loaders and any future real stable entry migration still require evidence | 5 |
| 3 (partial) | Expand actual personal-project acceptance | Shijian controlled trace plus permanent personal-site adoption and real delivery closeout are recorded with versions, review, repairs, tests and scoped commit/push; broader product-code and full commit/release chains remain open | 5 |
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
explicit maintainer approval. Consumer, adopter and broader host evidence remain
open; the subsequent canonical Mac CLI upgrade acceptance is recorded below. No roadmap promotion or 1.0 release is authorized by this
document. Documentation links, hygiene and Markdown formatting
are checked for this update.

## Stable upgrade implementation evidence

The development entry `cortex upgrade [version]` selects stable tags from origin,
not GitHub Release metadata; `update` retains default-branch semantics. The
[permanent installer suite](../../scripts/test-cortex-installer.py) now executes
29 cases, including seven upgrade regressions for latest/explicit selection,
dirty state, invalid/missing/unavailable versions, empty stable catalogs, moved
tags and incomplete release trees. All 29 passed locally on macOS.
[CI run 39930582778](https://github.com/nesnilnehc/ai-cortex/actions/runs/39930582778)
passed both Linux/macOS installer jobs, shell, Markdown, links and registry checks
on implementation commit `a461bcdf5b44f46b6282d0b3e6b1309a629df9fa`.
The PR-only translation job was skipped as configured, not counted as passed.

TDD first reproduced the absent entry, then exposed an empty default-branch
fallback in update and a forward-moved cached release tag. Each was corrected
without weakening its expectation. Existing 22 ownership/recovery cases remain.
This is fixture-based real CLI/Git integration, not a new real-host IDE invocation
or an acceptance of every historical installer. Older releases still require a
retained manager as documented in the recovery guide.

## Bounded consumer compatibility evidence

The [compatibility guide](../guides/consumer-compatibility.md) defines the evidence
boundary. Two historical contract descriptors pin 0.5.1/0.6.0 commits and source
digests. Actual published Release Package exports and an authored review fixture
have independent expected projections. Four historical release-reader pairs and
two review-reader pairs pass; current-reader and negative regressions pass in
12 test methods with subtests. These are reference readers of Markdown contracts,
not independent IDE adapters or captured end-to-end agent executions.

TDD first ran 9 methods against placeholder consumers: 36 assertion failures and
no test errors. A later preservation test batch exposed four failures before
original Findings and per-emitter coverage were retained. The final local suite
and checker pass.
[CI run 39932726458](https://github.com/nesnilnehc/ai-cortex/actions/runs/39932726458)
passed the full-history registry job containing both consumer commands, plus
links, Markdown, shell and Linux/macOS installer jobs on implementation commit
`c7c40759874e0cddc755f08386e5fb21f93a0034`. The PR-only translation job was skipped as configured. This does not complete the
full consumer matrix or authorize 1.0. No Skill/Spec/Rule/Protocol contract changed.

## Configuration, Rule and migration compatibility extension

The [compatibility guide](../guides/consumer-compatibility.md#configuration-rule-and-migration-extension)
records twelve additional historical/current reference test methods and a pinned
0.6.0 registry: 29 profiles, 18 parameter provenances and required profile/waiver
fields. Configuration wins over inference; conflicting explicit sources are
reported without inventing source precedence. Baseline snapshots remain unchanged;
missing declared values stay evidence-limited. Invalid waivers cannot suppress
findings, while valid ones retain waived status.

The configuration loader is limited to JSON-compatible YAML and a fixed CLAUDE
fixture representation. Waiver scope uses an explicit path population and test
approval identities. Deprecation uses test-only entry names and evidence flags;
it does not add aliases or announce a real deprecation. Two real installer cases
exercise preview/explicit migration from old aggregate directories to canonical
entries while preserving unrelated user directories. They pass on the existing
installer; its suite now contains 31 methods.

Local reference, historical provenance and installer checks pass.
[CI run 39936103143](https://github.com/nesnilnehc/ai-cortex/actions/runs/39936103143)
passed registry (including the new reference commands), Linux/macOS installer,
links, shell and Markdown jobs on implementation commit
`abcf83bccd714789c059823b85778a767fb75b44`. The PR-only translation job was skipped as configured.
This closes the selected bounded reference cases, not actual host/project
acceptance, full YAML/Markdown interpretation, real waiver authority verification,
or the complete stable dependency matrix. Applicable adopter evidence remains
open. No production asset contract or user configuration was changed.

## Live Codex and Shijian scoped acceptance

The [host acceptance record](host-acceptance.md) and linked case JSON retain one
actual Codex CLI run, not a reference-consumer simulation. On macOS arm64 with
Codex 0.163.0-alpha.11.2 and pinned Node 20.20.2, it read installed review-diff,
automate-tests and Findings assets byte-identical to 0.6.0. It interpreted a real
scoped configuration, reproduced an injected empty-draft failure, emitted a
Finding before edits, restored the selected source and passed 3/3 scoped tests.
An independent rerun and byte comparisons verified the result and unchanged tests.

This was a controlled committed snapshot of a real personal project, excluding
its active working tree. It was not an organic defect, a source-project delivery,
a full project gate, automatic Skill routing, desktop GUI acceptance or universal
model behavior. The canonical installation remains on its existing development
commit. At that rehearsal, inspected project entry files had no explicit Cortex adoption reference.
The subsequent personal-site adoption below changes that named project only. Broader
primary-host configuration, product-code acceptance, other core chains and adopter
evidence remain open.
The overall 1.0 decision remains not ready.

## Permanent adoption and natural delivery closeout

[Host acceptance](host-acceptance.md#permanent-personal-site-adoption-and-organic-closeout)
now records committed AGENTS/config adoption in the personal website and a real
closeout of its already-implemented analytics requirement. Missing model-test CI
and stale delivery statements were repaired; the operator committed/pushed the
scoped changes. The actual CLI loaded the new project entry and configured assets,
reviewed its adoption/configuration diff and passed 5 fast tests. Independent
pinned-Node tests, six-post content validation, Jekyll build and five browser groups
passed, including keyboard/no-JS and 1440/390/320 px layouts.

This resolves absence of persistent adoption for that project and supplies one
organic configuration/documentation delivery record. It is not a newly developed
product feature, a naturally discovered product-code bug, an autonomous full-chain
CLI repair or a Release Package acceptance. Browser checks are local; ordinary
user-config/desktop behavior, remaining core and
adopter evidence still need acceptance. Keep the overall decision **not ready**;
next resolve the inherited review-diff/Findings wording mismatch and verify a real
nonempty finding, then accept an actual behavior change when one arises and the
remaining stable-chain evidence. Wider host claims require their own scope.

## Canonical stable upgrade, rollback and recovery acceptance

[Host acceptance](host-acceptance.md#canonical-installation-stable-upgrade-and-recovery)
and its versioned case now close the selected primary macOS/CLI operational cycle.
A verified local backup preceded changes to the real installation. Latest stable
selected 0.6.0, the retained manager rolled assets back to 0.5.1 and recovered
0.6.0, and the initial clean `main@dfad163` was restored. The old native manager's
missing `upgrade` entry produced the expected refusal without changing HEAD.
Each of three actual CLI runs loaded the adopted site's entry/config/assets and
passed 5 fast tests. Independent pinned tests/content/build passed at all four
states; stable recovery also passed all five local browser groups.

All 1,255 installed-target entries and their contents/link strings/modes match the
backup after restoration; 1,004 non-managed entries were unchanged at every audited
stage. The personal-site source and commit remain unchanged. Private fetched
release refs/objects stay as selection evidence. This verifies normal
checkout/resynchronization recovery, not emergency archive extraction. Four loaded
core asset files and population counts are identical across the selected releases;
changed-contract compatibility, automatic desktop discovery, normal user config,
other hosts, concurrent writers and fault handling are not added to the claim.

The host also exposed inherited six-field wording in review-diff 1.0.2 that needs
alignment with the seven-element Findings Spec, followed by nonempty-output
verification. This was an observation during an empty-diff loading/test run; it
did not fail the operational cycle and must not be silently treated as repaired.
Overall 1.0 remains **not ready**. Prioritize that bounded core alignment and
nonempty real review evidence, actual product-behavior delivery when available,
remaining core dependencies/adopter evidence, then a bounded candidate rehearsal.
