# Commit Work

Create high-quality git commits with AI Cortex governance - review changes, split logically, write clear messages (Conventional Commits), sync with INDEX/manifest.

## Overview

This skill helps you make commits that are easy to review and safe to ship. It guides you through inspecting changes, splitting mixed work into logical commits, writing clear Conventional Commits messages, and running appropriate verification steps.

## AI Cortex Enhanced Version

This is an enhanced version of the `commit-work` skill, evolved specifically for AI Cortex projects with additional governance and quality features:

### Enhancements

- **Pre-commit review integration**: Automatically invokes `review-diff` skill to catch issues before staging
- **Registry synchronization**: Ensures `skills/INDEX.md` and `manifest.json` stay in sync when skills are added or modified
- **Spec compliance**: Follows AI Cortex `spec/skill.md` standards for structure and quality
- **Enhanced Self-Check**: Comprehensive verification checklist aligned with AI Cortex governance

### Evolution Metadata

This skill integrates content from multiple sources:

#### Primary Source (Fork)
- **Skill**: `commit-work`
- **Repository**: Anthropic skills collection (assumed)
- **Version**: 1.0.0
- **License**: MIT
- **Borrowed**: Core workflow structure, Conventional Commits format, patch staging approach

#### Integrated Components
- **Skill**: `review-diff`
- **Repository**: nesnilnehc/ai-cortex
- **Version**: 1.3.0
- **License**: MIT
- **Borrowed**: Pre-commit review methodology

### Current Version

- **Version**: 2.0.0
- **License**: MIT

## Installation

### For AI Cortex users

```bash
npx skills add nesnilnehc/ai-cortex --skill commit-work
```

### For other projects

This skill works in any git repository but provides additional features when used in AI Cortex projects (automatic registry sync checks).

## Usage

Activate this skill when you need to:

- Commit your work with clear, reviewable commits
- Split mixed changes into logical, atomic commits
- Write Conventional Commits messages
- Ensure commits meet quality standards before pushing
- Maintain registry synchronization in AI Cortex projects

The skill will guide you through a comprehensive workflow from inspection to verification.

## Key Features

### Workflow Steps

1. Inspect working tree before staging
2. **Run pre-commit review** (AI Cortex enhancement)
3. Decide commit boundaries and split if needed
4. Stage only related changes
5. Review staged changes carefully
6. Describe changes clearly
7. Write Conventional Commits messages
8. Run verification (tests/lint)
9. **Sync registries if needed** (AI Cortex projects)
10. Repeat until working tree is clean

### Conventional Commits Format

```
type(scope): short summary

body explaining what and why

footer (BREAKING CHANGE if needed)
```

Supported types: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`, `perf`, `style`

## Examples

See [SKILL.md](SKILL.md#examples) for detailed examples including:

- Simple feature addition
- Mixed changes requiring split
- AI Cortex skill addition with registry sync

## Related Skills

- [review-diff](../review-diff/SKILL.md): Pre-commit code review (integrated in step 2)

## Contributing

This skill is part of the AI Cortex project. To suggest improvements:

1. Open an issue at [nesnilnehc/ai-cortex](https://github.com/nesnilnehc/ai-cortex)
2. Follow the contribution guidelines
3. Ensure changes maintain backward compatibility or clearly document breaking changes

## License

MIT License - same as the original `commit-work` skill and the AI Cortex project.

## Version History

- **2.0.0** (current): AI Cortex enhanced version with review integration and registry sync
- **1.0.0**: Original version (forked baseline)

## Feedback

If you find issues or have suggestions for improvements, please open an issue in the [AI Cortex repository](https://github.com/nesnilnehc/ai-cortex/issues).
