# Contributing

Thanks for your interest in AI Cortex. This document covers how to contribute skills, rules and improvements.

## Quick start

1. Fork the repository
2. Create a branch: `git checkout -b feat/your-skill-name`
3. Make your changes following the guidance below
4. Run the [checks](#checks) and open a pull request

## Language

Write in English. The only exceptions are immutable records — existing ADRs, released changelog entries and design snapshots — documented in [docs/LANGUAGE_SCHEME.md](docs/LANGUAGE_SCHEME.md).

If you are converting existing Chinese content, read §6 of that document first. **Machine translation is not accepted.** Read the paragraph, understand what it asserts, then write that assertion in English.

## Adding a skill

Skills follow the [agentskills.io](https://agentskills.io) standard format. Draft new skills against this section and the existing directory layout; do not install an external skill generator as part of the contribution flow.

1. **Draft**: write `skills/<skill-name>/SKILL.md`. The YAML frontmatter must contain `name`, `description`, `tags`, `triggers`, `version` and `license`.
2. **Optional**: add a `README.md` as a quick reference.
3. **Register**: run `python3 scripts/sync-skills-index.py`. That regenerates `skills/INDEX.md` from the frontmatter; do not edit the registry by hand, because CI rejects one that disagrees with the skills it registers.
4. **Open a PR.**

`description` and `triggers` must be English — skills.sh and agentskills.io parse them, and skill matching depends on them.

Research Skills use optional `metadata.ai_cortex_type` (`foundation`, `domain`, or `orchestrator`) and `metadata.ai_cortex_user_invocable` (`"true"` or `"false"`). Declare both together; the index generator validates and displays them. The flag is a repository routing contract, not a guarantee that every host hides an internal Skill. Use explicit local artifact handoffs between Skills and preserve the [Research Evidence](specs/research-evidence.md) and [Opportunity Package](specs/opportunity-package.md) contracts. The five public research names are a narrow [naming exception](docs/adr/0013-research-skill-entry-names.md).

The new research Skills are original AI Cortex content. Only copy an external Skill through the vendored-source process below; a link to an external prompt is not a local implementation. The [checks](#checks) below say what to run before opening a pull request.

### Externally derived skills

AI Cortex distributes vendored copies only. We do not accept a skill that requires an agent to run `npx skills add`, clone an external repository, or read a floating raw URL at runtime.

When you copy, adapt or fork an external skill you must:

1. Place a complete, callable copy under `skills/<skill-name>/`, removing any dependency on sibling skills that are not distributed with this repository.
2. Pin the upstream in `skills/SOURCES.yaml`: repository, path, full commit, tree, `SKILL.md` SHA-256, license, local modifications and update policy.
3. Preserve license and copyright notices, and update `docs/references/ATTRIBUTIONS.md` and `THIRD_PARTY_NOTICES.md`.
4. Review scripts, assets and licensing. Do not copy fonts, music, images or binaries that are not explicitly licensed for redistribution.
5. Verify the skill passes validation and that `bin/cortex install` / `update` distributes it alongside the other local skills.

**License compatibility is a hard requirement.** This repository is MIT. A skill derived from a copyleft or non-commercial upstream — CC BY-NC-SA, AGPL and similar — cannot be redistributed under MIT and will not be accepted. Check the upstream license before you start, not after.

The full data contract is [skill-source-modeling](specs/skill-source-modeling.md).

### Naming

See [docs/architecture/asset-naming.md](docs/architecture/asset-naming.md), the single document covering naming for all four asset types.

## Adding a rule

Rules live in `rules/` and must be registered in `rules/INDEX.md`. Follow the format of the existing rules. `bin/cortex` installs user-scoped Rules for supported IDEs (Claude Code links them; Cursor receives `.mdc` translations), while project-scoped Rules stay in the canonical clone for on-demand loading. Other consumers must follow their own supported loading path.

## Versioning

This project follows [Semantic Versioning](https://semver.org/). When you modify a skill:

- **PATCH** (1.0.0 → 1.0.1): errata, metadata adjustments, reference updates
- **MINOR** (1.0.0 → 1.1.0): new steps, improved examples, interaction policy changes
- **MAJOR** (1.0.0 → 2.0.0): breaking structural changes, including making a previously optional output format mandatory

After bumping `version` in the SKILL.md frontmatter, run `python3 scripts/sync-skills-index.py` so any description, tag or trigger change reaches `skills/INDEX.md`.

## Checks

CI runs these on every pull request and they all block a merge, so run the ones your change touches first. Each prints what it validated rather than only a pass or fail.

| Command | Run it when |
| --- | --- |
| `python3 scripts/check-markdown-links.py` | Any markdown change — relative links must resolve, and a Spec, Protocol or Rule must not link into `skills/` |
| `python3 scripts/check-doc-hygiene.py` | Any markdown change — orphaned documents, temporary filenames, and a temporary document that is not labelled as one |
| `python3 scripts/check-cortex-docs.py` | `bin/cortex` gained or lost a subcommand or flag, or a document changed how it tells someone to invoke it |
| `python3 scripts/check-asset-counts.py` | A skill, rule, spec or protocol was added or removed — the README states the counts in a sentence and again in the capability table |
| `python3 scripts/sync-skills-index.py --check` | A skill's frontmatter changed; regenerate with the same script without `--check` |
| `python3 scripts/check-asset-versions.py` | A skill, rule, spec or protocol changed — an edited asset must move its `version`, and the check compares the range since the last product tag |
| `python3 scripts/validate-rules.py` | A modeled Rule document changed |
| `python3 scripts/test-rule-scenarios.py` | A modeled Rule item changed, or its fixtures did |
| `python3 scripts/test-skills-index.py`, `python3 scripts/test-research-artifacts.py`, `python3 scripts/test-markdown-links.py`, `python3 scripts/test-doc-hygiene.py`, `python3 scripts/test-asset-counts.py`, `python3 scripts/test-cortex-docs.py`, `python3 scripts/test-asset-versions.py` | The generator or checker they cover changed |
| `python3 scripts/mutation-check.py` | A checker, its fixtures, or `rules/task-quality.md` changed |
| `npx markdownlint-cli2 "**/*.md" "!.cortex/vendor/**" "!tests/fixtures/**"` | Any markdown change |

`mutation-check.py` is the one that needs explaining. Every other check reports a verdict, and a clean verdict proves nothing on its own — a checker that has stopped looking returns exactly the same thing. This one perturbs what each checker reads and requires the verdict to change: a defect seeded into a checker must turn its fixture test red, an edit to an already-translated document must be blocked by the translation verifier, and two controls must be allowed through, or the verifier is refusing everything rather than catching anything.

A perturbation whose pattern no longer matches its target fails the run rather than being skipped. So a refactor that moves the code a case quotes, or an edit to `rules/task-quality.md`, means updating the case — that coupling is the point. Its predecessor skipped instead, and eleven of its fifteen cases had quietly stopped matching before anyone noticed.

## Releasing

Releases go through `prepare-release` and then `publish-release`, never by hand. [docs/guides/releasing.md](docs/guides/releasing.md) covers what counts as worth releasing, how the independent version domains work, and the three details that are easy to get wrong.

## Code of conduct

See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md). Report security issues privately per [SECURITY.md](SECURITY.md) rather than opening a public issue.

## Questions

Open an issue with the `question` label, or browse [the skill index](skills/INDEX.md) to see what already exists.
