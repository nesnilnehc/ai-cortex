---
artifact_type: rule
name: repo-structure-hygiene
version: 1.0.0
scope: auditing or self-checking the repository directory structure (run by the runtime, a linter, CI or a person)
recommended_scope: user
status: active
---

# Rule: Repository Structure Hygiene

> Hard constraints on the repository's directory structure. A runtime (AgentFabric, a linter, CI, or a person) performs the detection against this rule; the rule states the criteria only, not how to detect them.
>
> Complementary to `rules/doc-health-criteria.md` — that one covers document health (links, SSOT, alignment), this one covers directory structure (misplacement, naming, empty directories, staleness).

---

## 1. Misplaced files

- [ ] A file sits in a directory matching its type and content (`.md` not under `src/`, `.py` not under `docs/`)
- [ ] The `docs/` root holds only index and governance files (README / INDEX / ARTIFACT_NORMS / CONTRIBUTING and the like); everything else goes to the path_pattern for its type in `docs/ARTIFACT_NORMS.md`
- [ ] The artifact_type inferred from frontmatter, filename or content agrees with the directory the file is in

---

## 2. Naming consistency

- [ ] Filenames follow kebab-case, per `docs/architecture/asset-naming.md`
- [ ] The `YYYY-MM-DD-` timestamp prefix is used only for artifact types that allow it (`adr`, `design-decision`); other types do not carry a timestamp
- [ ] The timestamp format must be `YYYY-MM-DD` — `YYYY/MM/DD`, `YYYYMMDD`, `YY-M-D` and other variants are not accepted
- [ ] Naming style is consistent within a directory — no mixing of PascalCase, snake_case and kebab-case

---

## 3. Empty directories

- [ ] A directory is non-empty (one containing only `.gitkeep` counts as empty)
- [ ] Exception: dependency directories (`node_modules`, `.venv`, `dist`, `build`, `__pycache__`) are not empty-directory violations — they belong in `.gitignore`

---

## 4. Stale artifacts

A file is stale when:

- [ ] Its extension is `.bak`, `.tmp`, `.orig` or `.swp`
- [ ] Its filename carries an explicit marker such as `DEPRECATED`, `OLD`, `UNUSED` or `LEGACY`
- [ ] It has not been modified for over 180 days and a repository-wide grep finds no reference to it — orphaned and old

A stale artifact should be deleted, archived under `.archive/`, or marked `status: deprecated` in its frontmatter.

---

## 5. Duplicate entries

- [ ] Files with highly similar names should not coexist in one directory (`util.py` alongside `utils.py`, `auth.py` alongside `Auth.py`)
- [ ] Where they do, there must be a stated reason for the distinction, in a comment or a README

---

## 6. Top-level structure

- [ ] Only directories named in the project's conventions appear at the top level, as listed in `docs/ARTIFACT_NORMS.md` or the repository README
- [ ] The standard directories the project requires (`docs/`, `src/`) must exist

---

## Anti-patterns

- ❌ A filename that is not kebab-case and is not listed as an exemption in the project conventions
- ❌ Backup files such as `.bak` or `.tmp` committed to the repository
- ❌ An empty directory committed without a `.gitkeep` to signal the intent to keep it
- ❌ A concrete artifact file dropped in the docs/ root (`docs/goals.md` belongs under something like `docs/process-management/goals/`)
- ❌ A misplaced timestamp prefix — a requirement or spec carrying `2026-03-01-`

---

## Related assets

- Detection (`find`, `ls`, custom scripts, linters) is carried out by the runtime or CI tooling; this rule states criteria only
- Safe, reversible operations (`git mv` on a file, `rmdir` on an empty directory) are performed by a person or by the AgentFabric runtime after user confirmation
- Dangerous operations (deleting a non-empty directory, rewriting git history, a rename that requires updating many references) must be performed by a person and are out of scope for automation
