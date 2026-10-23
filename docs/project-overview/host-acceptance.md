---
artifact_type: assessment
lifecycle: living
created_at: 2026-10-23
status: complete
---

# Host and personal-project acceptance

One live Codex CLI review/repair rehearsal passed on 2026-10-23 using a scoped
committed snapshot of the maintainer's Shijian project. This establishes actual
installed-asset invocation and scoped behavior, not full project, desktop GUI,
organic delivery or production acceptance. The [readiness assessment](release-readiness.md)
retains those separate gaps.

## Inspected adoption state

The bundled CLI reports `codex-cli 0.163.0-alpha.11.2`; the observed machine is
macOS 27.0.1, arm64. The canonical installation is at
`~/.local/share/ai-cortex`, commit `dfad16371b7d658d678ba66b94956180d763379a`,
with no exact release tag. Generic Skill links resolve into that installation.
The selected `review-diff` 1.0.2, `automate-tests` 1.1.0 and Findings Spec 2.0.1
are byte-identical to their 0.6.0 release files. The installation was not updated.
This comparison covers those three files, not every asset in the old clone.

Root `AGENTS.md`, `CLAUDE.md` and `.ai-cortex/config.yaml` were inspected where
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

Remaining acceptance includes organic project work and interventions, explicit
permanent project adoption, wider host/configuration paths, the complete stable
chain, applicable adopter populations and any claimed additional environments.
