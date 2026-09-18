# AI Cortex

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> A governance and delivery asset library for AI agents — skills, specs, protocols and rules. See [mission](docs/project-overview/mission.md) and [vision](docs/project-overview/vision.md).

When an agent works inside this repository, [AGENTS.md](AGENTS.md) is authoritative for the execution contract, the four asset layers, precedence, discovery and skill matching. Terminology is defined in [docs/architecture/terminology.md](docs/architecture/terminology.md).

---

## 🧭 What's inside

**68 skills** ([index](skills/INDEX.md)), **30 rules** ([index](rules/INDEX.md)), **19 specs** ([index](specs/INDEX.md)) and **1 protocol** ([index](protocols/INDEX.md)).

| Area | Count | Representative skills |
| :--- | ---: | :--- |
| **Governance & planning** | 17 | Deriving mission → vision → North Star → strategic goals → roadmap layer by layer; backlog scoring, dependency mapping, promotion and archival; `plan-next` diagnoses what to do next |
| **Code review** | 27 | Pre-coding artifact reviews, post-coding implementation alignment, and `orchestrate-code-review` across 8 languages, frameworks, libraries and six engineering concerns |
| **Delivery & release** | 9 | Commits, worktree delivery and integration, release package build and publication, announcements, test execution, local redeployment |
| **Docs & assets** | 5 | Generating README, AGENTS.md and GitHub Actions; refining skill design; decontextualizing text |
| **Integration & ops** | 4 | NATS cross-team messaging, macOS Keychain credential management, agent test scaffolding |
| **Research & opportunity** | 6 | Open, policy, market and competitive research; internal opportunity assessment; product opportunity package |

Skills are callable from Claude Code, Cursor, Codex and 20+ other agents. For a worked end-to-end flow, see the [roadmap planning guide](docs/guides/roadmap-planning-usage.md); to find an entry point by collaboration stage, see the [stage-to-skill table](docs/guides/proactive-suggestions.md).

For open research, focused policy/market/competitive studies and product opportunity decisions, see the [research Skills usage guide](docs/guides/research-skills-usage.md).

For project adoption of requirement/design/task constraints and the post-coding engineering + functional repair loop, see [engineering quality governance](docs/guides/engineering-quality-governance.md).

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

`cortex install` also puts the command itself at `~/.local/bin/cortex`, which is where the short `cortex` used below comes from; it warns if `~/.local/bin` is not on your `PATH`, and until it is, call the script by its full path.

It symlinks every skill — including reviewed local copies of externally derived ones — into `~/.agents/skills/<skill>`, where Codex and other agents reading that path discover them in a new session. It also detects installed IDEs (Claude Code, Cursor) and syncs their skill paths. User-scoped Rules are symlinked for Claude Code and converted to `.mdc` for Cursor; project-scoped engineering Rule sets stay in the canonical clone and are loaded on demand by their review Skills, avoiding permanent context inflation. `specs/` and `protocols/` need no installation — agents read them from the canonical path. Nothing is ever installed from skills.sh or GitHub at runtime.

### Upgrade

```bash
cortex update
```

Fetches `origin` and **hard-resets the canonical clone onto it**, then re-syncs, pruning orphaned links for deleted skills and rules. It refuses to run on a dirty working tree; `cortex update --force` overrides that and discards whatever was uncommitted. Local commits on the tracked branch are discarded either way, so keep your own changes on a branch or a fork rather than in the canonical clone.

Upstream updates to externally derived skills are reviewed by maintainers before entering AI Cortex; they are not upgraded independently at the user's runtime.

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
Engineering Rule profiles and review-gate responsibilities are recorded in [ADR 0012](docs/adr/0012-adopt-profiled-engineering-rules.md).

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md), and read the [Code of Conduct](CODE_OF_CONDUCT.md) before taking part. Report security issues privately per the [security policy](SECURITY.md) rather than opening a public issue.

Maintainers releasing AI Cortex: [docs/guides/releasing.md](docs/guides/releasing.md) covers what counts as worth releasing, the independent version domains, and the Skills that own each step.

Documentation is written in English; the exceptions are listed in [docs/LANGUAGE_SCHEME.md](docs/LANGUAGE_SCHEME.md).

---

## 📄 License

Original AI Cortex content is [MIT](LICENSE). Vendored externally derived skills keep their own licenses — see the [license policy](docs/references/LICENSE_POLICY.md) and [third-party notices](docs/references/THIRD_PARTY_NOTICES.md).

---

## 🙏 Acknowledgements

- [Contributors](https://github.com/nesnilnehc/ai-cortex/graphs/contributors)
- Pinned sources and local modifications for externally derived skills are listed in [ATTRIBUTIONS.md](docs/references/ATTRIBUTIONS.md) and [skills/SOURCES.yaml](skills/SOURCES.yaml)
