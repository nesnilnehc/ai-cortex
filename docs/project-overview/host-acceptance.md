---
artifact_type: assessment
lifecycle: living
created_at: 2026-10-23
status: complete
---

# Host and personal-project acceptance

A live Codex CLI rehearsal on a Shijian snapshot and a subsequent real personal-site
delivery closeout passed on 2026-10-23. The personal site now has committed Cortex
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
