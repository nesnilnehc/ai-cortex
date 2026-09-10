---
artifact_type: guide
created_at: 2026-03-25
status: deprecated
lifecycle: living
deprecated_at: 2026-09-10
deprecated_reason: Described runtime remote loading, which ADR 0011 forbids and ADR 0010 replaced with a canonical local clone.
---

# Protocol registry and remote loading (superseded)

**This guide described a model the project no longer uses, and following it would violate the execution contract.** It is kept as a pointer so a link arriving from outside the repository — a bookmark, a search result, another project — still lands somewhere that explains the change. Nothing inside the repository links here any more, by design. The content is in git history.

## What it said, and why it is gone

It told an agent to know one registry URL, fetch `skills/INDEX.md` over HTTPS at startup, and load each protocol from a `canonical_url` on `raw.githubusercontent.com` — treating a local clone as "not recommended".

Three things now contradict it:

- **[ADR 0011](../adr/0011-vendor-external-skills.md)** decided that an agent runtime must not download, register or update anything from a registry, GitHub or a raw URL. External content enters as a reviewed local copy, and only through a maintenance pass.
- **[AGENTS.md](../../AGENTS.md) §1** encodes that as the execution contract: an agent `MUST NOT` fetch external links or raw-content URLs by default, and `MUST` prefer local relative paths.
- **[ADR 0010](../adr/0010-installation-strategy.md)** established the canonical clone at `${XDG_DATA_HOME:-~/.local/share}/ai-cortex`, which is where protocols are read from.

Its examples were also built on a structure that does not exist: they described `skills/INDEX.md` as JSON carrying a `protocols` array, and referenced `protocols/unp.md` and `protocols/inp.md`. `skills/INDEX.md` is a Markdown index, and the two protocol documents were split into a Spec and a Protocol when [terminology](../architecture/terminology.md) separated the four asset layers.

## Where to look instead

| For | See |
|---|---|
| How an agent discovers and loads a protocol | [AGENTS.md §4](../../AGENTS.md) and [discovery-and-loading.md](discovery-and-loading.md) |
| Where protocols live and how they are installed | [protocols-quickstart.md](protocols-quickstart.md) — they stay in the canonical clone; there is no install step |
| The protocols that exist | [protocols/INDEX.md](../../protocols/INDEX.md) |
| The notification pair this guide used as its example | [specs/universal-notification.md](../../specs/universal-notification.md) for the object, [protocols/im-notification-delivery.md](../../protocols/im-notification-delivery.md) for the delivery |
