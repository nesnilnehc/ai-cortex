# AI Cortex

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> A governance and delivery asset library for AI agents — skills, specs, protocols and rules. See [mission](docs/project-overview/mission.md) and [vision](docs/project-overview/vision.md).

When an agent works inside this repository, [AGENTS.md](AGENTS.md) is authoritative for the execution contract, the four asset layers, precedence, discovery and skill matching. Terminology is defined in [docs/architecture/terminology.md](docs/architecture/terminology.md).

---

## 🧭 What's inside

**55 skills** ([index](skills/INDEX.md)), **21 rules** ([index](rules/INDEX.md)), **16 specs** ([index](specs/INDEX.md)) and protocols ([index](protocols/INDEX.md)).

| Area | Count | Representative skills |
| :--- | ---: | :--- |
| **Governance & planning** | 17 | Deriving mission → vision → North Star → strategic goals → roadmap layer by layer; backlog scoring, dependency mapping, promotion and archival; `plan-next` diagnoses what to do next |
| **Code review** | 20 | `orchestrate-code-review` sequences scope → language → framework → library → cognitive; atomic review skills for 8 languages plus React, Vue and ORM usage |
| **Delivery & release** | 9 | Commits, worktree delivery and integration, release package build and publication, announcements, test execution, local redeployment |
| **Docs & assets** | 5 | Generating README, AGENTS.md and GitHub Actions; refining skill design; decontextualizing text |
| **Integration & ops** | 4 | NATS cross-team messaging, macOS Keychain credential management, agent test scaffolding |

Skills are callable from Claude Code, Cursor, Codex and 20+ other agents. For a worked end-to-end flow, see the [roadmap planning guide](docs/guides/roadmap-planning-usage.md); to find an entry point by collaboration stage, see the [stage-to-skill table](docs/guides/proactive-suggestions.md).

### How this differs from similar libraries

- **Four separated asset layers** — Skill (what an agent can do) / Spec (what a thing looks like) / Protocol (how parties coordinate) / Rule (what must not happen), with explicit boundaries. See [terminology](docs/architecture/terminology.md).
- **Orchestrators are thin** — an `orchestrate-*` skill does exactly four things: detect context, sequence calls, halt on failure, aggregate output. Domain logic stays in the atomic skills.
- **Review criteria live outside the skills** — evaluative skills read their criteria from `rules/*-quality.md`, so one definition serves the producing, diagnosing and reviewing sides.
- **Vendored-only distribution** — externally derived skills are pinned to a commit and digest with their license recorded. Nothing is installed from the network at runtime. See [ADR 0011](docs/adr/0011-vendor-external-skills.md).

---

## 📦 Install and use

### Quick start

```bash
mkdir -p ~/.local/share
git clone --depth 1 https://github.com/nesnilnehc/ai-cortex.git ~/.local/share/ai-cortex
~/.local/share/ai-cortex/bin/cortex install
```

`cortex install` symlinks every skill — including reviewed local copies of externally derived ones — into `~/.agents/skills/<skill>`, where Codex and other agents reading that path discover them in a new session. It also detects installed IDEs (Claude Code, Cursor) and syncs their skill paths. Rules are symlinked for Claude Code and converted to `.mdc` for Cursor. `specs/` and `protocols/` need no installation — agents read them from the canonical path. Nothing is ever installed from skills.sh or GitHub at runtime.

### Upgrade

```bash
cortex update
```

Pulls the latest AI Cortex commit and re-syncs, pruning orphaned links for deleted skills and rules. Upstream updates to externally derived skills are reviewed by maintainers before entering AI Cortex; they are not upgraded independently at the user's runtime.

### Status

```bash
cortex status
```

Shows `CORTEX_HOME`, the current commit, link counts per IDE, and any legacy artifacts detected.

### Clean up legacy artifacts

If this machine previously installed AI Cortex some other way, review before removing:

```bash
cortex clean --dry-run   # report only
cortex clean             # interactive, confirms each category
```

### Uninstall

```bash
cortex uninstall                # remove cortex-managed symlinks and .mdc files, keep CORTEX_HOME
cortex uninstall --remove-home  # also delete the CORTEX_HOME directory
```

Install design is recorded in [ADR 0010](docs/adr/0010-installation-strategy.md); external skill management in [ADR 0011](docs/adr/0011-vendor-external-skills.md).

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md), and read the [Code of Conduct](CODE_OF_CONDUCT.md) before taking part. Report security issues privately per the [security policy](SECURITY.md) rather than opening a public issue.

Documentation is written in English; the exceptions are listed in [docs/LANGUAGE_SCHEME.md](docs/LANGUAGE_SCHEME.md).

---

## 📄 License

Original AI Cortex content is [MIT](LICENSE). Vendored externally derived skills keep their own licenses — see the [license policy](docs/references/LICENSE_POLICY.md) and [third-party notices](docs/references/THIRD_PARTY_NOTICES.md).

---

## 🙏 Acknowledgements

- [Contributors](https://github.com/nesnilnehc/ai-cortex/graphs/contributors)
- Pinned sources and local modifications for externally derived skills are listed in [ATTRIBUTIONS.md](docs/references/ATTRIBUTIONS.md) and [skills/SOURCES.yaml](skills/SOURCES.yaml)
