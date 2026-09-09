# Architecture Decision Records

This repository uses Architecture Decision Records to capture the decisions that shape its structure and its governance.

## Why an ADR

A good decision record answers four questions: **What** was decided / **Why** / which **Alternatives** were considered / what **Consequences** follow. Scattered across commits, pull requests and conversations, those answers disappear fast. Gathered into an ADR, a team member six months later can reconstruct the context instead of finding a "why is it built this way" puzzle in the code.

## The data contract and the writing discipline

- **The data contract** — frontmatter fields, the status enum, the body structure → [specs/adr-modeling.md](../../specs/adr-modeling.md)
- **The writing discipline** — the bar for admission, enforcing status, the decay policy → [rules/adr-management.md](../../rules/adr-management.md)

## How to add an ADR

1. Copy [`templates/adr-template.md`](./templates/adr-template.md)
2. Name it `NNNN-{slug}.md`, taking the highest number in the index below + 1 (the first new ADR started at `0010`)
3. Fill in the frontmatter and the 4 body sections (Context / Decision / Alternatives / Consequences)
4. Append a row to the index below

## The ADR index

| Number | Title | Status |
|---|---|---|
| [0001](./0001-io-contract-protocol.md) | The skill-chain I/O contract protocol | accepted |
| [0002](./0002-plan-next-v6-restructure.md) | Restructuring plan-next for v6 | accepted |
| [0003](./0003-plan-next-v6.3-execution-state-and-linking.md) | plan-next v6.3: execution state and artifact linking | accepted |
| [0004](./0004-norms-driven-artifact-architecture.md) | A norms-driven artifact architecture | accepted |
| [0005](./0005-retract-linking-mode-enum.md) | Retracting the linking_mode enum | accepted |
| [0006](./0006-delete-linking-mode-and-unify-artifact-paths.md) | Deleting linking_mode and unifying the artifact paths | accepted |
| [0007](./0007-remove-plan-next-execute-flag.md) | Removing the plan-next execute flag | accepted |
| [0008](./0008-replace-asqm-with-acceptance-criteria.md) | Replacing ASQM with acceptance criteria | accepted |
| [0009](./0009-replace-merge-worktree-with-deliver-and-integrate.md) | Replacing merge-worktree with deliver-feature + integrate-worktrees | accepted |
| [0010](./0010-installation-strategy.md) | The installation strategy: an XDG canonical path plus bin/cortex | accepted |
| [0011](./0011-vendor-external-skills.md) | Unifying the management of vendored external skills | accepted |
