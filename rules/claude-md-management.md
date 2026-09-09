---
artifact_type: rule
name: claude-md-management
version: 1.0.0
scope: writing and maintaining CLAUDE.md at every level (personal / project / module)
recommended_scope: user
status: active
---

# Rule: CLAUDE.md Management

## Scope

Every act of writing, modifying or auditing a CLAUDE.md, including:

- Written by hand
- Written with AI assistance
- Drafted automatically by Claude Code's built-in `/init` skill

Output from `/init` **does not go straight into the repository**; it may be committed only after passing the §5 self-check in this rule.

The data contract — section structure and form requirements — is in [specs/claude-md-modeling.md](../specs/claude-md-modeling.md); this rule constrains behaviour: length, expression, no-go content, revision, self-check.

---

## §1 Length limits

| Level | Limit |
|---|---|
| Project (repository root `CLAUDE.md`) | ≤ 300 lines |
| Module (subdirectory `CLAUDE.md`) | ≤ 100 lines |
| Personal (`~/.claude/CLAUDE.md`) | Not enforced; equal restraint recommended |

When the project limit is exceeded, first split out a module-level CLAUDE.md, then trim by deleting low-value entries. **Working around the limit by adding links to side specs is not allowed** — CLAUDE.md is loaded directly, and the volume loaded is itself the cost.

---

## §2 Expression

### Use imperatives or assertions

✅ "Use pnpm, not npm"
❌ "After team discussion this project settled on pnpm as its package manager, because..."

### Mark the critical constraints explicitly

Prefix an unbreakable rule with `IMPORTANT:`, `NEVER:` or `ALWAYS:`. The model is sensitive to these signals and follows a marked rule more reliably during generation.

### A prohibition beats a positive requirement

"Do not do X" is followed more reliably than "you should do Y". Where a prohibition expresses it, prefer the prohibition.

### No vague wording

Avoid hedges — "try to", "ideally", "where possible", "consider", "if practical". In Chinese documents the equivalents are "尽量", "建议", "最好". A rule's binding strength needs to be unambiguous: either it is mandatory, or it is deleted.

---

## §3 Content no-go zones

The following **must not** appear in a CLAUDE.md:

| No-go zone | Why |
|---|---|
| General programming knowledge (Docker, REST, the test pyramid and the like) | The AI already knows it; writing it in only dilutes the context |
| Volatile state (sprint, owner, todos, temporary branch names) | That belongs in an issue tracker or a wiki |
| Sensitive material (keys, tokens, production IPs, internal domains, PII) | A security risk; once CLAUDE.md is in git, it has leaked |
| A full restatement of the README, CONTRIBUTING or architecture docs | Two sources drift apart; link instead |
| A speculative "just in case" rule | A rule must come from a real pain point, not from a prediction |

---

## §4 Revision principles

### The deletion test — every rule has to pass it

Before adding any rule, ask: **would the AI behave worse if this were deleted?**

- Yes → keep it
- No → do not add it

### When to revise

- The AI keeps making the same mistake — the rule is missing or unclear
- A team convention changed
- A related spec was upgraded and needs alignment. In particular, when [spec §5.2 required sections](../specs/claude-md-modeling.md#52-required-sections-at-project-level) or [§1 position and scope](../specs/claude-md-modeling.md#1-position-and-scope) changes, §1 length limits and the §5 self-check in this rule must be reviewed alongside it
- An improvement identified in the monthly retrospective

### When not to revise

- A one-off incident
- A situation specific to a single project — that belongs in the project's CLAUDE.md, not promoted into a general rule
- An idea not yet validated in practice

### DRY

Link overlapping content rather than copying it. One piece of information is maintained in one place.

---

## §5 Self-check

Before committing any CLAUDE.md change, confirm each item:

- [ ] Required sections all present (see [spec §5.2](../specs/claude-md-modeling.md#52-required-sections-at-project-level))
- [ ] No crossover of responsibility between levels (see [spec §5.1](../specs/claude-md-modeling.md#51-the-three-levels-and-how-responsibility-divides))
- [ ] Form requirements met — concise, actionable, decision-oriented, kept close to what it governs (see [spec §5.4](../specs/claude-md-modeling.md#54-form-requirements))
- [ ] Length within the §1 limit of this rule
- [ ] Critical constraints marked with `IMPORTANT:`, `NEVER:` or `ALWAYS:` (see §2)
- [ ] No §3 no-go content (general knowledge / volatile state / sensitive material / README restatement / speculative rules)
- [ ] Overlapping content linked rather than copied (see §4 DRY)
- [ ] Every added rule passes the deletion test (see §4)

---

## Bad patterns

```markdown
<!-- ❌ general knowledge explained -->
## Docker

Docker is a containerisation platform; images are defined with a Dockerfile...
```

```markdown
<!-- ❌ volatile state -->
## Current tasks

- [ ] @zhangsan is doing the OAuth refactor (expected to land in Q3)
- [ ] @lisi owns the database migration
```

```markdown
<!-- ❌ vague wording -->
## Testing

Try to write tests, and ideally keep coverage fairly high.
```

```markdown
<!-- ❌ restating the README -->
## About this project

(the first 50 lines of the README, pasted in)
```

---

## Remediation

1. **Too long**: split out a module-level CLAUDE.md, or delete the "general knowledge" sections
2. **Written as prose**: rewrite as imperatives; keep the constraint, drop the argument for it
3. **No-go content crept in**: delete general knowledge; move volatile state to the issue tracker; remove sensitive material at once and rotate it
4. **Missing critical marks**: prefix the high-stakes rules — those whose violation is costly — with `IMPORTANT:` and move them to the end of the file
5. **README restatement**: replace with a `> For an introduction to the project see [README.md](../README.md)` link

---

## Related guidance

- Data contract: [specs/claude-md-modeling.md](../specs/claude-md-modeling.md)
- General documentation policy: [rules/workflow-documentation.md](./workflow-documentation.md)

---

## Change log

### 1.0.0 — 2026-05-15

**Initial Release**: defines 5 sets of constraints (length, expression, no-go content, revision, self-check), with each self-check item citing the spec as its yardstick. Paired with [specs/claude-md-modeling.md](../specs/claude-md-modeling.md).
