# Contributing

Thanks for your interest in AI Cortex. This document covers how to contribute skills, rules and improvements.

## Quick start

1. Fork the repository
2. Create a branch: `git checkout -b feat/your-skill-name`
3. Make your changes following the guidance below
4. Open a pull request

## Language

Write in English. The only exceptions are immutable records — existing ADRs, released changelog entries and design snapshots — documented in [docs/LANGUAGE_SCHEME.md](docs/LANGUAGE_SCHEME.md).

If you are converting existing Chinese content, read §6 of that document first. **Machine translation is not accepted.** Read the paragraph, understand what it asserts, then write that assertion in English.

## Adding a skill

Skills follow the [agentskills.io](https://agentskills.io) standard format. Draft new skills against this section and the existing directory layout; do not install an external skill generator as part of the contribution flow.

1. **Draft**: write `skills/<skill-name>/SKILL.md`. The YAML frontmatter must contain `name`, `description`, `tags`, `version` and `license`.
2. **Optional**: add a `README.md` as a quick reference.
3. **Register**: add the skill to `skills/INDEX.md`.
4. **Open a PR.**

`description` and `triggers` must be English — skills.sh and agentskills.io parse them, and skill matching depends on them.

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

Rules live in `rules/` and must be registered in `rules/INDEX.md`. Follow the format of the existing rules. Downstream consumers such as Cursor and Trae copy or symlink `rules/` in their own way; this repository does not ship an installer for them.

## Versioning

This project follows [Semantic Versioning](https://semver.org/). When you modify a skill:

- **PATCH** (1.0.0 → 1.0.1): errata, metadata adjustments, reference updates
- **MINOR** (1.0.0 → 1.1.0): new steps, improved examples, interaction policy changes
- **MAJOR** (1.0.0 → 2.0.0): breaking structural changes, including making a previously optional output format mandatory

After bumping `version` in the SKILL.md frontmatter, update the matching entry in `skills/INDEX.md`.

## Code of conduct

See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md). Report security issues privately per [SECURITY.md](SECURITY.md) rather than opening a public issue.

## Questions

Open an issue with the `question` label, or browse [the skill index](skills/INDEX.md) to see what already exists.
