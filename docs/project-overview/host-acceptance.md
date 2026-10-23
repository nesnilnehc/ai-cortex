---
artifact_type: assessment
lifecycle: living
created_at: 2026-10-23
status: complete
---

# Host and personal-project acceptance

A live Codex CLI rehearsal, personal-site delivery closeout and canonical-install
stable upgrade/rollback/recovery cycle passed on 2026-10-23. The personal site now has committed Cortex
adoption, real gap repairs and scoped delivery evidence. These establish bounded
installed-asset invocation and organic closeout, not full autonomous development,
desktop GUI or production-wide acceptance. The [readiness assessment](release-readiness.md)
retains those separate gaps.

## Inspected adoption state

The bundled CLI reports `codex-cli 0.163.0-alpha.11.2`; the observed machine is
macOS 27.0.1, arm64. The canonical installation is at
`~/.local/share/ai-cortex`, commit `dfad16371b7d658d678ba66b94956180d763379a`,
with no exact release tag. Generic Skill links resolve into that installation.
The selected `review-diff` 1.0.2, `automate-tests` 1.1.0 and Findings Spec 2.0.1
are byte-identical to their 0.6.0 release files. The installation was not updated.
This comparison covers those three files, not every asset in the old clone.

Before the subsequent website onboarding, root `AGENTS.md`, `CLAUDE.md` and `.ai-cortex/config.yaml` were inspected where
present in Shijian, the personal website, Laya and DeepSeek Harness checkouts.
None of those checked files explicitly referenced AI Cortex. The personal website
had no root AGENTS entry; the other three did. This is a named-entry-file check,
not an exhaustive search of all project instructions or adoption records. Laya
and DeepSeek Harness are upstream checkouts, not evidence of maintainer ownership.
Shijian had 591 dirty/untracked entries at inspection, so its working tree was
excluded from execution. The other three checkouts were clean. No project was
permanently onboarded by this rehearsal.

## Rehearsal and evidence

The [versioned case record](../../tests/fixtures/host-acceptance/codex-shijian-2026-10-23.json)
contains the exact input, asset/source hashes, scoped configuration, regression
case, ordered selected host events, test output and host report. Full raw JSONL,
metadata, warnings and logs remain locally under
`~/.local/state/ai-cortex/acceptance/2026-10-23-codex-shijian`; its trace digest is
in the case record. Raw logs and private machine paths are not uploaded.

Source: `nesnilnehc/shijian` commit
`1329fd8d4f4f41ab7a07de799a156e182b2cec8d`. Only its committed AGENTS, README,
package manifest, Makefile, Node pin, draft module and draft tests were exported
into a disposable Git directory. Uncommitted project files were not copied.
The snapshot uses Node 20.20.2 from the project's `.nvmrc`.

Requirement: reopening an intentionally empty unsaved check-in draft must preserve
that empty string even when saved text exists; experiment/check-in isolation and
cleanup behavior must remain intact. A third test first passed against the
original code. Then the operator `?? original` was deliberately replaced with
`|| original` in the snapshot. This was an injected regression, not a discovered
production bug. No repair was applied or committed to the real personal project.

| Stage | Observed execution |
| --- | --- |
| Original project baseline | 2 tests passed |
| New boundary test before injection | 3 tests passed |
| Injected regression, before host | Nonzero exit and reproduced empty-string mismatch |
| Codex first scoped execution | Exit 1; 3 executed, 2 passed, 1 failed, 0 skipped |
| Review before edits | Location, category scope, severity major, title, description, maturity ready and suggestion all recoverable in the event stream |
| Repair | Only the selected module edited; nullish fallback restored |
| Codex final execution | Exit 0; 3 executed, 3 passed, 0 failed/skipped |
| Independent verification | Same 3 cases passed; module equals original source bytes and test equals the authored pre-host test bytes |

The CLI actually read installed Skill paths and the installed Findings Spec before
review. It read the scoped `.ai-cortex/config.yaml` and selected its test command.
The finding event precedes both recorded file-edit events, which precede the green
execution. Two patch events occurred; the final module has no remaining diff from
the source snapshot. The added regression remains in the isolated test file.
No tests were weakened or removed. The commands and patches are more specific
evidence than the model's final assertion of success.

## Host configuration and limits

This execution used `codex exec` with `--ignore-user-config`, `--ephemeral`,
`--sandbox workspace-write`, approval policy never and the user's configured model name
`gpt-6.1-sol`. The requested model and sandbox are recorded, but backend model
identity and OS sandbox enforcement were not independently attested. Ignoring
user configuration avoided unrelated MCP integrations. The host read Skills from
the existing installation through explicit paths; automatic matching and all
ordinary desktop/user-configuration behavior were not tested.

The subprocess environment put the pinned Node on PATH; a separate matching
login-shell check confirmed Node 20.20.2. No dependency installation, external
project service, delegation, source-project Git write, push or deployment was part
of the agent's tool trace. The Codex model request itself used the existing host
account. Nonfatal local state-database lookup fallback warnings were retained;
the process completed with exit 0. Normal CLI state/telemetry internals outside
the selected agent tool writes were not audited.

For reruns, recreate the scoped committed snapshot, append the recorded regression,
verify it passes before injection, inject the recorded operator change, and invoke
the recorded input through the CLI using the pinned Node and assets. A live model
rerun requires intentional execution; CI must not silently replay paid/authenticated
model calls. Final wording need not repeat, but command outcomes, edit scope,
asset identity and independent green checks must be retained. The official
[non-interactive documentation](https://developers.openai.com/codex/noninteractive/)
was consulted alongside this machine's actual CLI help; measured events govern
this record.

The following organic closeout supplements that rehearsal. Remaining acceptance
includes broader product-code delivery and interventions, wider host/configuration
paths, the complete stable chain, applicable adopter populations and any claimed
additional environments.

## Permanent personal-site adoption and organic closeout

The maintainer selected `nesnilnehc/nesnilnehc.github.io` for permanent adoption.
Its baseline was `f64ee148bb48d9655037b3d968e43c9a7695db2c`, with a clean worktree.
The only discovered backlog document was already `done`: music/film like-count
analytics had shipped in `3495001d278f00a255b9d389940ea551a11d5324`. The selected
small task was its real delivery closeout: CI did not execute the existing model
regressions and living requirement/design records still claimed it was uncommitted.
No open product feature or artificial production defect was invented.

[Site commit 4e0be4b](https://github.com/nesnilnehc/nesnilnehc.github.io/commit/4e0be4b0994410e95374fa80270b76d385b23f7b)
adds a version-controlled AGENTS entry and `.ai-cortex/config.yaml`, preserves
existing CLAUDE poster instructions, runs `make test` before Pages builds, extends
trigger paths, excludes agent instructions from generated output and reconciles
the requirement/design with an acceptance record. Its entry self-check covers
all applicable generate-agent-entry contract sections 3–6. The changes are
configuration/documentation only; TDD red was not manufactured and no existing
tests were weakened. UI design was skipped because no product interface changed;
actual existing-page acceptance was nevertheless rerun.

The [curated case](../../tests/fixtures/host-acceptance/codex-personal-site-2026-10-23.json)
retains input, versions and hashes, ordered completed host commands, review scope,
operator findings/repairs, test outcomes and trace digests. Raw host logs, test/build
logs and screenshots stay under
`~/.local/state/ai-cortex/acceptance/2026-10-23-codex-personal-site`.
The same canonical installation was used without upgrading it. Five selected
files, including generate-agent-entry 1.3.0 and commit-work 2.1.0, are individually
byte-identical to 0.6.0; this does not retag or certify the entire old installation.

The actual Codex CLI explicitly read the new project entry, resolved the default
root, read its index, configuration and complete review/test/commit assets, then
ran configured `make test`: 5 executed, 5 passed, none failed/skipped. Its review
returned an empty Findings list for the two modified configurations and two new
adoption files present at that point. Later documentation closeout received an
operator final diff review, not a second claimed CLI review. The two real residual
gaps were identified and repaired by the operator. This is a mixed host/operator
workflow, not autonomous full-chain editing or native automatic preload proof.

The CLI's login shell used Node 25.6.1. Independent execution using the CI pin
20.20.2 passed 5/5. Ruby 3.3.6 content validation passed for six posts and Jekyll
built successfully; generated output excludes AGENTS, CLAUDE and Cortex config.
Five existing Playwright 1.62.1/Chromium groups passed without skips, covering both
collections, filters/sort/count selection, keyboard, no-JS and invalid/empty states
at 1440/390/320 px. The 320 px music screenshot was visually checked. Browser
checks remain local and do not establish other engines or physical-device support.

The host used ephemeral, read-only, ignored-user-config execution with requested
model `gpt-6.1-sol`; actual backend identity and sandbox enforcement remain
unattested. One failed environment-variable lookup merely established both root
overrides were unset; it is not a failing test. The CLI reported denied cache
writes but executed the tests successfully. No source edits or remote mutations
were performed by that CLI. The operator reviewed/staged only the seven scoped
files and committed/pushed them with the user's authorization; both initial
worktrees were clean. Authenticated GitHub access and Pages deployment are operator
delivery steps, not part of the host review trace.

[Site CI 39962057167](https://github.com/nesnilnehc/nesnilnehc.github.io/actions/runs/39962057167)
passed Validate and build (including the new model-test gate) and Deploy Pages
on the adoption commit. Public music/film pages returned HTTP 200 with analytics
markup; the served model script matched local source bytes. This HTTP check is
not a substitute for the independently executed local browser interaction suite.
The subsequent documentation receipt preserves that run and corrects the install
link without changing product behavior.

## Canonical installation stable upgrade and recovery

The [versioned case](../../tests/fixtures/host-acceptance/stable-upgrade-rollback-2026-10-23.json)
records actual mutation of `~/.local/share/ai-cortex`, rather than a temporary-home
installer simulation. The initial clone was clean on
`main@dfad16371b7d658d678ba66b94956180d763379a`; the adopted personal site was clean
at `2e8f856f3d41d449a7d70c82af3f93f1851b8e2f`. Both root overrides were unset.

Before mutation, a local archive captured the canonical clone including Git
metadata, generic/Claude/Cursor skill directories, Claude/Cursor rule directories
and command link. Source-manager bytes and representative symlink metadata were
checked against the archive. A manager from development baseline
`9902e25ff24a6ae107b47506aef6c6cf5549a197` was retained outside the switched clone.
Archive, inventory, manager, raw host events/reports, checks and screenshots remain
under `~/.local/state/ai-cortex/acceptance/2026-10-23-stable-host`; only hashes and
curated evidence are committed. Backup restoration by emergency archive extraction
was not rehearsed; normal checkout/resynchronization restored the initial state.

| Stage | Selected commit | Observed result |
| --- | --- | --- |
| Latest stable `upgrade` | `a62a8e5238b1f3f54b50da8528248e6e9315639a` (0.6.0) | Origin stable selection, exact installed membership and CLI loading/tests passed |
| Explicit rollback `upgrade v0.5.1` | `95a1e001afb49e04368a7d12dd1aace92c583ff9` | Retained manager selected old assets; membership and CLI loading/tests passed |
| Old native manager `upgrade v0.6.0` | Unchanged 0.5.1 | Expected nonzero unknown-command refusal: old manager lacks the entry |
| Retained manager `upgrade v0.6.0` | 0.6.0 commit above | Stable recovery, membership and CLI loading/tests passed |
| Restore original `main`, retained manager `install` | Initial `dfad163` commit | Branch/content restored; complete installed-target inventory matches backup |

Each selected release had 70 Skills linked into each of generic, Claude and Cursor
paths, 20 Claude global Rule links and 20 generated Cursor Rules, matching the
selected source inventory with no broken managed links. Three separate actual
Codex CLI runs read the personal site's AGENTS/config, resolved the default root,
loaded index plus complete review/test/commit assets and Findings, then executed
`make test`: each ran 5 cases, all passed, none skipped. Diffs were empty; these
were loading/test acceptances, not nonempty review-output or new product repairs.
Four selected core asset files are byte-identical across 0.5.1 and 0.6.0 and those
population counts stay constant. Do not infer changed-contract compatibility or
all historical pruning cases from this cycle.

Independently, at upgrade, rollback, stable recovery and original restoration,
Node 20.20.2 / Ruby 3.3.6 passed the site's 5 model tests, six-post content validation
and Jekyll build. After stable recovery, five Playwright 1.62.1/Chromium groups
passed with no skips, covering both collections, keyboard/no-JS, filters/selection
and 1440/390/320 px layouts; the 320 px music screenshot was visually checked.
No personal-site commit, source or adoption configuration changed.

Final comparison to the verified archive found all 1,255 installed-target entries,
file contents, symlink strings and file/directory modes restored. The 1,004
non-managed entries were unchanged at every audited version. Two existing Vercel
legacy links were retained. The final clone is clean on its original main commit;
new private release refs and fetched Git objects deliberately remain as manager
selection evidence. No force update, old-history merge or development-main update
was used. This final state is the initial development snapshot, not a retained
stable pin or a new supported security version.

Measured environment: macOS 27.0.1 build 26A434, arm64, zsh 5.9, manager `/bin/sh`
(GNU bash 3.2.57), operator Git 2.51.0 and Codex CLI 0.163.0-alpha.11.2. CLI runs
used ephemeral/read-only/ignored-user-config execution with requested
`gpt-6.1-sol`; backend model identity, sandbox enforcement and the CLI's exact Node
version were not independently attested. Operator pinned-tool tests are distinct
from CLI fast tests. Cache/event-stream warnings were retained alongside actual
successful test counts. An exact local-tag lookup returned 128 because the upgrade
uses private release refs; selected commit/tag-object identity was separately verified.
Unset-root environment probes returned 1 as expected. Automatic native preload, ordinary desktop/user config,
other operating systems, filesystem/network faults and concurrent writers remain
outside this measured claim. Operator-only version changes and independent checks
must not be presented as autonomous agent recovery.

### Observation and remaining core gap

The rollback host identified an inherited wording mismatch in review-diff 1.0.2:
its self-check says six fields, while Findings Spec 2.0.1 requires `maturity` among
seven elements and makes `suggestion` optional. Current and released text confirm
this observation. The higher-authority Spec governs; loading/tests passed, but
empty diffs did not exercise a nonempty Findings output. Record this as a minor
stable-core documentation alignment gap to repair and then verify with an actual
finding; this acceptance does not change published tags or production assets.

The operator inventory check initially rejected trailing slashes in existing
symlink targets. The archive was already captured; the upgrade proceeded in that
same command batch. Subsequent membership checks normalized that representation,
then final restoration compared exact original link strings and all target modes.
The evidence parser also required correction for the host's Node spec reporter
rather than the operator's TAP reporter; strict 5/5/0/0 counters were retained.
These are retained acceptance-tool limitations, not installer failures. The
canonical recovery procedure remains in the [recovery guide](../guides/installer-recovery.md).

## Findings alignment and nonempty Codex output

The [case record](../../tests/fixtures/host-acceptance/nonempty-findings-2026-10-23.json)
resolves the previously recorded wording defect in development. review-diff,
review-codebase and orchestrate-code-review now cite Findings §5.1 instead of
copying its field inventory. Ten language/framework reviewers and
review-requirements also no longer make an optional suggestion mandatory.
All fourteen modified Skills receive independent PATCH errata versions; the
canonical Spec and protected output requirements are unchanged. The Skill index
was regenerated with no description/inventory change.

TDD exposed five missed forms before repair: slash-separated inventories, their
Markdown variants, duplicated inventories beside a citation and numeric/spelled
obsolete totals. The repaired checker passes seventeen positive/negative text
shapes plus the existing three-shape directory walk and scans all 28 emitters.
Six required fields plus an optional suggestion remains valid prose. Two new
mutation cases prove both detection branches can fail; the complete mutation
suite passes. Existing CI already runs the checker, its tests and mutation suite.

An actual Codex CLI 0.163.0-alpha.11.2 execution loaded the revised development
review-diff 1.0.3 and canonical Findings 2.0.1, inspected an isolated Git diff and
reproduced the changed function's failures for empty and multi-item inputs. Its
nonempty JSON finding has concrete location, category scope, severity major,
meaningful title/description, maturity ready and an actionable suggestion. Output
was independently parsed and validated; command outcomes and hashes are retained.
The fixture deliberately replaces sum(prices) with prices[0]; this is controlled
negative acceptance, not a naturally discovered production bug. The host did not
repair it. Raw logs remain in the case's local evidence directory.

The run used ephemeral/read-only/ignored-user-config mode with requested model
gpt-6.1-sol; backend identity and sandbox enforcement remain unattested. Global
installation and personal projects were not changed. The host loaded development
assets directly, so this does not certify installed distribution, every emitter,
provisional-Rule findings or full ordinary host configuration. No live model call
was added to CI. The prior observation remains historical evidence; its wording
alignment and one real nonempty output are now resolved within this scope.

## Remaining core gates on a real project behavior repair

The [versioned case](../../tests/fixtures/host-acceptance/core-gates-personal-site-2026-10-23.json)
adds a real source repair in the permanently adopted personal site. The analytics
backlog was already done; review of its approved invalid-count boundary found
that collection sorting silently converted missing values to zero and could show
a NaN count heading. Current personal collection records were valid. The defect
was in existing production code and exercised with abnormal DOM input data; no
source regression was injected and no prior organic user incident is claimed.

[Site repair 7a8fe5f](https://github.com/nesnilnehc/nesnilnehc.github.io/commit/7a8fe5f)
reuses the strict count parser, distinguishes invalid records from valid zero,
places invalid records last and orders model loading before collection wiring.
The new permanent browser regression covers music and films. An actual original
page failed the music assertion before repair (1 failed, 5 unselected); complete
post-repair browser execution passes 6 groups with no failures/skips. The operator
also passed 5 model tests, six-post content validation and Jekyll build. This is
an existing-design repair, not a new interface; browser behavior and a 320 px music
screenshot were still inspected. Browser tests remain a local gate, not current CI.

| Stable entry | Version | New bounded evidence |
| --- | --- | --- |
| review-implementation-alignment | 1.1.2 | Seven approved acceptance items mapped to production wiring and evidence; ALN coverage kept separate and refreshed after runtime execution |
| orchestrate-code-review | 1.4.1 | Codebase scope, JavaScript language and all seven cognitive reviewers in fixed order; absent framework/ORM skipped explicitly; original per-emitter findings and coverage preserved |
| orchestrate-repair-loop | 1.5.0 | Operator-coordinated TDD repair, engineering/alignment review, minor follow-up repair, independent acceptance and affected-gate refresh within a five-stage bound |

The actual Codex CLI first discovery exceeded its 360-second command bound while
the operator added a regression and repaired the workspace. It has no final report
and is not a passed initial gate. The next run reviewed a frozen scope: no
critical/major findings, one minor missing Covers comment, model tests passing,
and browser evidence still operator-only. After the comment repair, a third run
retained unchanged engineering coverage, refreshed testing/alignment and read the
actual red/green/build logs. It independently ran 6/6 browser groups and 5/5 model
tests, inspected the narrow-screen screenshot with an image tool and reported
scoped convergence with evidence limitations. No source assertions were weakened.

The first two runs requested read-only sandboxes. The runtime acceptance run
explicitly allowed existing local browser execution and screenshots and requested
danger-full-access mode; it started no service and performed no source/Git/install
or network-tool writes. The operator had started the local preview and performs
source repairs and authorized delivery. Requested model was gpt-6.1-sol with
Codex CLI 0.163.0-alpha.11.2, ephemeral and ignored-user-config execution; backend
identity and sandbox enforcement remain unattested. The canonical installation
remained on dfad163; these are direct development-asset invocations, not installed
or autonomous full-chain acceptance. Raw reports, commands, test logs, hashes and
screenshots stay under the case's local evidence directory.

Every modeled Rule ID in the reported coverage is checked for complete, disjoint
classification against its canonical inventory; cognitive judgments remain
agent-reported. No missing evidence is promoted to passed. Retained limits include
unrun secret scanning, undeclared SLO/performance/coverage/observability targets,
missing architecture baselines, absent separate technical-design/task artifacts,
and wider browser repeatability. Refreshed ALN-001/002/007 and TST-001/002/003/005
pass within scope; ALN-003/006 and TST-006/008 remain evidence-limited. Full original
finding wording and coverage reasons are preserved in private report hashes; the
case exports classifications and a curated English scope account.

This covers one real behavior repair and the three entries' cooperation. It does
not admit every dependency, language, provisional Rule population, ordinary host
configuration or consuming-project Release Package chain. The overall 1.0 decision
remains not ready; use this evidence rather than scheduling the same missing
three-entry exercise again without identifying a materially different gap.

[Site CI 39973504547](https://github.com/nesnilnehc/nesnilnehc.github.io/actions/runs/39973504547)
passed validation/build and Pages deployment for the repair commit. The public
site script returned HTTP 200 and matched the delivered local source bytes.
