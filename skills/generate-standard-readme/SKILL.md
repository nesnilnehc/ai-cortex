---
name: generate-standard-readme
description: Generate lean, high-density README. Sections pruned by value threshold — not fixed count. Primary goal — reader knows what the project is, where to look, and how to use it within 30 seconds.
description_zh: 生成高信息密度 README。章节按价值门槛裁剪，非固定数量。首要目标：读者 30 秒内知道项目是啥、去哪看、怎么用。
tags: [documentation, devops, writing]
version: 2.1.1
license: MIT
recommended_scope: user
metadata:
  author: ai-cortex
triggers: [generate readme, readme]
input_schema:
  type: code-scope
  description: Repository or project path to generate README for
output_schema:
  type: document-artifact
  description: Lean README.md written to the project root; section count varies by project type and available content
---

# Skill: Generate Lean README

## Purpose

Generate a **high-density, low-redundancy** front page for any software project or documentation repository.

The one core goal: within 30 seconds the reader knows —
1. What this project is (one sentence)
2. Where the key entry points are
3. How to use it (the shortest runnable path)

---

## Scope

**This skill handles**:
- Lean README generation, with sections pruned by a value threshold
- Project-type triage (code/application repository vs documentation/spec repository)
- Anti-fluff output (every claim lands on a concrete path, command, behavior, or constraint)

**This skill does NOT handle**:
- A full docs/ suite → taken on by the AgentFabric runtime or by a person, per `docs/ARTIFACT_NORMS.md`
- AGENTS.md / agent contract files → use `generate-agent-entry`
- Redaction of sensitive information → use `decontextualize-text`

---

## Use Cases

- **New repository**: The project has just been created and needs a front page; no README exists yet.
- **Asset governance**: Unify README style across services to improve indexability.
- **Legacy systems**: Fill in the missing documentation, covering the core entry points with the least information that works.
- **Handover and release**: Make the front page complete before the project is transferred or published.

**Trigger signals**: The user says "write me a README", "generate a readme", or simply hands over a repository path.

---

## Behavior

### Interaction Policy

| Situation | Behavior |
| :--- | :--- |
| Project type known | Generate directly, no questions |
| Project type unclear | Inspect the repository structure first (is there a `package.json` / `pyproject.toml` / `Dockerfile` / `INDEX.md`, and so on) to infer the type; when the inference is solid, generate directly and state what it rests on; when it is not, ask the user |
| User gave no description | Infer the most conservative description from the repository name and file structure, mark it `TBD`, invent nothing |
| Before writing the file | By default write `README.md` directly; if the repository already has a README, warn that it will be overwritten and wait for confirmation |

### Default Skeleton

```markdown
# <project name> [badges (optional)]

<one-sentence description> (required)

## <Core entry points / How to use> (required)

## License (required)
```

Every other section is kept or dropped by the value threshold.

### Section Value Threshold

**Decision rule**: If a section carries no decision-making information the other sections lack, delete it or fold it into the nearest section.

| Section | Type | Kept when |
| :--- | :--- | :--- |
| Title + one-sentence description | **Required** | Always kept |
| Core entry points / How to use | **Required** | Always kept |
| License | **Required** | Always kept, with a working link |
| Feature list | Optional | There are ≥2 non-obvious features and the one-sentence description cannot carry them |
| Installation | Optional (code type only) | Installation takes more than a single `pip install` / `npm install` line |
| Quick start | Optional (code type only) | A copy-pasteable minimal runnable example exists |
| Configuration / usage notes | Optional | There are non-obvious configuration options or parameters |
| Contributing guide | Optional | The contribution process has particular requirements (PR conventions, test gates, and so on) |
| Authors / acknowledgements | Optional | There is an explicit attribution need |

**Omission rules**:
- `doc` type repository: by default no installation or quick-start section is generated; a navigation index takes their place
- Any section whose content is empty or only TBD → omit it (no hollow sections)
- If the contributing or authors section can only hold boilerplate → omit it

### Project-Type Triage

**code type** (code/application repository)

Signals: a `package.json` / `pyproject.toml` / `Makefile` / `Dockerfile` / main entry-point file exists.

Output focus: the installation path, a minimal runnable example, the key API entry points.

```markdown
# MyApp

One line on what the project does.

## Installation

\```bash
npm install myapp
\```

## Usage

\```bash
myapp --input file.csv --output result.json
\```

## License

MIT — see [LICENSE](LICENSE)
```

**doc type** (documentation/spec repository)

Signals: no executable entry point; the bulk of the content is `.md` / `.yaml` / `.json` spec files; an `INDEX.md` / `skills/INDEX.md` exists.

Output focus: a navigation index and reading paths. Installation and quick start are omitted by default.

```markdown
# MySpec

One line on the scope and audience of the spec or docs.

## How to use

- Start from [INDEX.md](INDEX.md)
- Core definitions: [docs/architecture/terminology.md](docs/architecture/terminology.md)
- Contribution conventions: [CONTRIBUTING.md](CONTRIBUTING.md)

## License

MIT — see [LICENSE](LICENSE)
```

### Anti-Fluff Rules

The following are forbidden:

| Forbidden pattern | Example | Fix |
| :--- | :--- | :--- |
| Piled-up empty adjectives | "reusable, governable, actionable" | Delete, or replace with concrete behavior: "registered through `skills/INDEX.md` and self-checked alongside each change" |
| Subjectless value claims | "improves engineering standards" | Delete or make concrete: "keeps `skills/INDEX.md` consistent with the document links" |
| Repeating known information | Restating the description section inside the installation section | Merge or delete |
| Placeholder boilerplate | "Contributions welcome! Send a PR." | With no concrete process to describe, omit the contributing section |
| Invented commands or features | Writing `docker compose up` when there is no `docker-compose.yml` | Use `TBD`, or omit |

**Every claim must land on**: a concrete file path / a shell command / an observable behavior / an explicit constraint.

---

## Input & Output

### Input

| Field | Required | Notes |
| :--- | :--- | :--- |
| Project name | Required | Used as the title |
| One-sentence description | Required | States precisely what the project does |
| Project type | Recommended | `code` or `doc`; inferred from the repository structure when not given |
| License | Recommended | Type + file path; `TBD` when not given |
| Installation command | Optional | Used only for `code` type projects |
| Quick-start example | Optional | Used only for `code` type projects |
| Core entry point list | Optional | Key files, directories, URLs |

**Fields not supplied**: use `TBD` as a placeholder, or drop the section outright; inventing them is forbidden.

### Output

- `README.md` written to the project root
- The section count follows from the value threshold, with a floor of 3 sections (title + description, entry points/usage, license)
- No broken links; internal paths preferred

---

## Restrictions

- **Never invent**: every command, path, and feature must come from the input or from what the repository actually contains; when one is missing, use `TBD` or omit it
- **Never leave a broken link**: use an external link only where it is highly stable (shields.io, for example); an internal path must be verifiable as existing
- **Never keep a hollow section**: every section kept carries at least one actionable piece of information; an empty one is omitted
- **Hard limit on doc type**: a doc type repository gets no installation or quick-start section; if the user asks for one anyway, explain the reason
- **License cannot be dropped**: always include a License section; when none is given use `TBD` rather than omitting it
- **An existing README must be confirmed**: if the target directory already holds a README.md, the user must be prompted before it is overwritten

---

## Self-Check

After generating the README, work through each item:

- [ ] **30-second test**: Can a reader new to the project read the one-sentence description and find the usage entry point within 30 seconds?
- [ ] **No empty adjectives**: no "reusable", "governable", "professional" or similar adjectives with no concrete behavior behind them
- [ ] **Nothing invented**: every command, path, and feature comes from the input or from what the repository actually contains
- [ ] **No broken links**: internal paths verified to exist; external links used only where highly stable
- [ ] **No hollow sections**: every section kept carries at least one actionable piece of information
- [ ] **License section present**: license type + a working link (or TBD)
- [ ] **Project type matches**: a doc type has no installation or quick-start section; a code type's installation command actually runs
- [ ] **Value threshold passed**: every section kept supplies decision-making information the other sections do not carry

**Acceptance criteria**: all 8 items above pass, or each item that does not has an explicit waiver reason.

---

## Examples

### Example 1: Code repository (lean output)

**Input**: name `img-crush`, description "batch-compress images", install `pip install img-crush`, usage `img-crush ./images`, license MIT.

**Output**:

```markdown
# img-crush

Batch-compress images; supports WebP / PNG / JPEG.

## Installation

\```bash
pip install img-crush
\```

## Usage

\```bash
img-crush ./images          # compress in place
img-crush ./images -o out/  # write to a chosen directory
\```

## License

MIT — see [LICENSE](LICENSE)
```

---

### Example 2: Documentation/spec repository (doc type)

**Input**: name `ai-cortex`, description "agent-first skill library", license MIT, core entry points `skills/INDEX.md` and `AGENTS.md`.

**Output**:

```markdown
# ai-cortex

An agent-first skill library for software delivery and project governance.

## How to use

- Start at [AGENTS.md](AGENTS.md) for the agent behavior contract
- Browse [skills/INDEX.md](skills/INDEX.md) for the available skills
- Core terminology: [docs/architecture/terminology.md](docs/architecture/terminology.md)

## License

MIT — see [LICENSE](LICENSE)
```

---

### Example 3: Edge case — a legacy project with almost no information

**Input**: name `legacy-auth`, no description, no feature list, installation and environment unknown.

**Handling**:
- One-sentence description: infer the most conservative wording from the name, marked `TBD`
- Installation section: omitted (no runnable command)
- Feature section: omitted (nothing to say)
- License: `TBD` (not omitted, only left to be filled in)

**Output**:

```markdown
# legacy-auth

Authentication service (details to be filled in).

## How to use

TBD — see the project's internal documentation.

## License

TBD
```

---

### Example 4: Failure case — an installation section generated for a doc type repository

**Symptom**: An `## Installation` section was generated for a documentation/spec repository, holding `npm install` or an empty TBD.

**Root cause**: The project type was not identified, so the code template was applied.

**Fix**: Inspect the repository structure → no executable entry point means doc type → delete the installation and quick-start sections and put a navigation index in their place.
