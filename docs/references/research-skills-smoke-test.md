# Research Skills installation and routing smoke record

Date: 2026-09-17

## Completed local checks

- Ran `bin/cortex install` with an isolated home and this repository as `CORTEX_HOME`. The five public names and `assess-product-opportunity` resolved as Skill directories with `SKILL.md` under both `.agents/skills` (Codex-compatible) and `.claude/skills` (Claude Code). No network install was used.
- Verified `skills/INDEX.md` generation and `--check` for 67 entries. Five research entries display `user-invocable: true` and the internal assessment displays `false`.
- Validated synthetic open, policy, market, competitive, user-signal, conflict, stale-source, inaccessible-source and opportunity fixtures with the JSON contract validator. Twenty-six negative cases were rejected; a compatible minor schema version and a 1,099-step derivation trace were accepted.
- The generic Codex `skill-creator` quick validator rejects this repository's established extended frontmatter keys (`tags`, `triggers`, `version`, `input_schema`, and others) for both the new Skills and existing `prepare-release`. Repository index validation passes; this generic validator is not a compatible gate for the current AI Cortex Skill format.

## Host behavior and remaining live checks

The installer links all six directories on both platforms. Claude Code's `user-invocable: false` field on the internal Skill is intended to hide its direct slash entry; Codex and other hosts may still display it because repository metadata is not a host-enforced visibility control. An isolated Claude Code print invocation returned `Invalid API key · Please run /login`. A clean authenticated agent session was not run, so direct slash execution and natural-language routing remain unverified at the model/UI level.

Before claiming the full portability acceptance criterion, run a fresh Codex and Claude Code session against the isolated install. Invoke the five public names directly, then ask an open question, a single domain question and a product opportunity question in ordinary language. Confirm each output route and that `assess-product-opportunity` is not offered as a public entry where the host supports hiding. For untrusted-source handling, give the agent [untrusted-source.txt](../../tests/fixtures/research/untrusted-source.txt) and verify it ignores the imperative text while preserving the page's factual content as a scoped observation.
