# Commit Work

Creates high-quality git commits under AI Cortex governance — review the changes, split them along logical lines, write a Conventional Commits message, and sync the relevant INDEX.

## Overview

This skill helps you produce commits that are easy to review and safe to ship. It walks you through inspecting the changes, splitting mixed work into logical commits, writing a clear Conventional Commits message, and running the fitting verification steps.

## Origin and AI Cortex additions

This is a locally vendored derivative of `commit-work` from `softaworks/agent-toolkit`. AI Cortex keeps the commit inspection, logical splitting, patch staging, and Conventional Commits workflow, and adds this repository's review, INDEX sync, and output contract.

The pinned upstream commit, digest, local modifications, and license record live in [`../SOURCES.yaml`](../SOURCES.yaml); copyright notices live in [THIRD_PARTY_NOTICES](../../docs/references/THIRD_PARTY_NOTICES.md). The historical, unverified `anthropics/skills (assumed)` origin is no longer in use.

- **Current version**: 2.0.1
- **License**: MIT

## Install

Handled centrally by the canonical AI Cortex install; see the repository root [README](../../README.md#-install-and-use). An agent runtime must not download or replace this skill on its own, from upstream or from skills.sh.

The skill works in any git repository; inside the AI Cortex repository it additionally checks that the matching INDEX is in sync.

## Usage

Activate this skill when you need to:

- Commit your work in a clear, reviewable form
- Split mixed changes into logical, atomic commits
- Write a Conventional Commits message
- Get a commit up to the quality bar before pushing
- Keep the registries of an AI Cortex project in sync

The skill guides you through the whole workflow, from inspection to verification.

## Key features

### Workflow steps

1. Inspect the working tree before staging
2. **Run the pre-commit review** (AI Cortex addition)
3. Decide the commit boundaries and split as needed
4. Stage only the relevant changes
5. Review the staged changes carefully
6. Describe the change clearly
7. Write the Conventional Commits message
8. Run verification (tests/lint)
9. **Sync the registries if needed** (AI Cortex projects)
10.Repeat until the working tree is clean

### Conventional Commits format

```text
type(scope): short summary

body explaining what and why

footer (BREAKING CHANGE if needed)
```

Supported types: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`, `perf`, `style`

## Examples

See [SKILL.md](SKILL.md#examples) for worked examples, including:

- A simple feature addition
- Mixed changes that need splitting
- Adding an AI Cortex skill alongside the registry sync

## Related skills

- [review-diff](../review-diff/SKILL.md): pre-commit code review (wired into step 2)

## Contributing

This skill is part of the AI Cortex project. To propose an improvement:

1. Open an issue at [nesnilnehc/ai-cortex](https://github.com/nesnilnehc/ai-cortex)
2. Follow the contribution guidelines
3. Keep the change backward compatible, or document the breaking change explicitly

## License

MIT; upstream copyright notices are in [THIRD_PARTY_NOTICES](../../docs/references/THIRD_PARTY_NOTICES.md).

## Feedback

If you hit a problem or have an improvement in mind, open an issue in the [AI Cortex repository](https://github.com/nesnilnehc/ai-cortex/issues).
