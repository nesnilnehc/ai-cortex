# prune-content

**Status**: experimental  
**Quality Score**: 16/20  

Identifies and archives obsolete project content based on user judgment or onboarding analysis. Invoke when user asks to clean up, archive, or audit repository content.

## Purpose

Help the user maintain a clean codebase by identifying and archiving "expired" or obsolete content. Instead of relying solely on mechanical timestamps or "deprecated" tags, this skill prioritizes **contextual relevance** and **user judgment**, often leveraging insights from `onboard-repo` or project cognition.

## When to use

- **Post-Onboarding Cleanup**: "The onboard-repo report says `docs/v1` is obsolete. Please archive it."
- **Contextual Archiving**: "Archive the old prototype code in `experiments/`."
- **Manual Cleanup**: "Move `README-old.md` to the archive."

## Inputs

- `user_instruction`: Natural language request (e.g., "archive the legacy folder")
- `file_list`: Specific list of files/directories to process
- `context`: Findings from other skills (e.g., onboard-repo report)

## Outputs

- `archived_files_report`: List of files moved and their new locations
- `cleanup_confirmation`: Status of the operation

## Behavior

1. **Identification (Interactive)**: Consults context or asks user to identify targets (e.g., "I see a `prototypes` folder. Archive?").
2. **Proposal**: Presents a clear plan of what will be moved where.
3. **Execution**: Uses `git mv` (preferred) or `mv` to move content to `_archive/<original_path>`, preserving directory structure.
4. **Cleanup**: Removes empty parent directories.

## Restrictions

- **No Deletion by Default**: Always prefers moving to `_archive` over `rm`.
- **Protect Critical Paths**: Never touches `.git`, `node_modules`, etc. without explicit confirmation.
- **Refactoring**: Does not fix broken imports after archiving.

## License

MIT
