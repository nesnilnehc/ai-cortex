---
name: generate-standard-readme
description: Generate professional, governance-ready README with fixed structure. Core goal - produce standardized front-page documentation that explains purpose, usage, and contribution guidelines. Use for asset governance, audit, or unified documentation standards.
tags: [documentation, eng-standards, devops, writing]
related_skills: [decontextualize-text, bootstrap-project-documentation, write-agents-entry]
version: 1.2.0
license: MIT
recommended_scope: user
metadata:
  author: ai-cortex
---

# Skill: Generate Standard README

## Purpose

Create **professional, consistent, highly readable** front-page documentation for **any software project** (open source, internal services, microservices, tooling). A standardized information layout reduces collaboration cost, improves engineering norms, and keeps core assets discoverable.

---

## Core Objective

**Primary Goal**: Produce a standardized README document with fixed structure that enables readers to understand project purpose, install, and contribute within 3 minutes.

**Success Criteria** (ALL must be met):

1. ✅ **README file created**: Written to project root as `README.md` with complete standard structure
2. ✅ **All 9 required sections present**: Title/badges, Description, Features, Installation, Quick start, Usage, Contributing, License, Authors
3. ✅ **Installation commands executable**: Copy-paste commands work without modification (no hardcoded paths or broken links)
4. ✅ **Three-second clarity test passed**: Reader understands project purpose within 3 seconds of viewing
5. ✅ **License section included**: License type specified and linked to LICENSE file

**Acceptance Test**: Can a new developer understand what the project does, install it, and run a basic example within 3 minutes using only the README?

---

## Scope Boundaries

**This skill handles**:
- README generation with fixed 9-section structure
- Professional tone and governance-ready formatting
- Standardized documentation for asset discovery and audit
- Badge generation and section ordering

**This skill does NOT handle**:
- Project-type-specific templates (use `crafting-effective-readmes` from softaworks/agent-toolkit)
- Comprehensive project documentation (use `bootstrap-project-documentation`)
- Agent entry files or AGENTS.md (use `write-agents-entry`)
- Privacy/security redaction (use `decontextualize-text` if needed)

**Handoff point**: When README is complete with all 9 sections and passes acceptance test, hand off to user for review or commit to version control.

---

## Use Cases

- **New project**: Quickly add a standard README for a new repo.
- **Asset governance**: Unify README style across internal services or libraries for better indexing and cross-team discovery.
- **Audit and compliance**: Bring legacy systems up to documentation standards for internal audit or architecture review.
- **Handover and release**: When transferring a project, changing ownership, or releasing publicly, ensure the audience can understand purpose, usage, and how to contribute.

**When to use**: When the project needs a “first face” that explains what it is, how to use it, and how to collaborate.

---

**Scope**: This skill emphasizes a **fixed output structure** and **governance** (unified style, audit, discoverability); the output contract is embedded in the skill. For template-by-project-type or guided Q&A creation, use skills.sh’s `crafting-effective-readmes` (e.g. softaworks/agent-toolkit).

---

## Behavior

### Principles

- **Clarity**: Readers immediately understand what the project is and what problem it solves.
- **Completeness**: Include everything users and contributors need.
- **Actionable**: Provide copy-paste install and quick-start commands.
- **Professional**: Use standard Markdown and a conventional section order.

### Tone and style

- Use **neutral, objective** language; avoid hype (“The best,” “Revolutionary”) unless backed by data.
- **Direct and concise**: Short sentences; avoid filler adjectives and bureaucratic phrasing; professionalism through clarity and scannability, not formality.
- Keep code examples short and comments clear.

### Visual elements

- **Badges**: Include License, Version, Build Status, etc. at the top.
- **Structure**: Use `---` or clear heading levels to separate sections.
- **Emoji**: Use sparingly (e.g. 📦, 🚀, 📖) to improve scannability.

---

## Input & Output

### Input

- **Project metadata**: Name, one-line description.
- **Features**: Core capabilities.
- **Requirements**: e.g. Node.js/Python version.
- **Install/run**: Concrete shell commands.

### Output

- **README source**: Markdown with this structure:
  1. Title and badges
  2. Core description
  3. ✨ Features
  4. 📦 Installation
  5. 🚀 Quick start
  6. 📖 Usage / configuration
  7. 🤝 Contributing
  8. 📄 License
  9. 👤 Authors and acknowledgments

---

## Restrictions

### Hard Boundaries

- **No broken links**: Do not add links that 404.
- **No redundant repetition**: Do not repeat the same fact (e.g. license) in multiple sections.
- **No hardcoded paths**: Use placeholders or variables in install and quick-start examples.
- **License required**: Always include a License section; do not omit it.
- **Fixed structure only**: Always use the 9-section structure; do not deviate or reorder sections.
- **No invention**: Do not invent features, commands, or details not provided by user; use placeholders for missing information.

### Skill Boundaries (Avoid Overlap)

**Do NOT do these (other skills handle them)**:

- **Project-type templates**: Creating README templates by project type (React, Python, etc.) → Use `crafting-effective-readmes` (softaworks/agent-toolkit)
- **Comprehensive documentation**: Creating full documentation suite (architecture docs, API docs, guides) → Use `bootstrap-project-documentation`
- **Agent entry files**: Creating AGENTS.md or agent contract files → Use `write-agents-entry`
- **Privacy redaction**: Removing PII or sensitive information from documentation → Use `decontextualize-text`
- **Content refinement**: Improving existing README prose or structure → Use general writing/editing skills

**When to stop and hand off**:

- User asks "can you create all project documentation?" → Hand off to `bootstrap-project-documentation`
- User asks "can you create an AGENTS.md file?" → Hand off to `write-agents-entry`
- User asks "can you customize this for a React project?" → Suggest `crafting-effective-readmes` for project-type templates
- README complete with all 9 sections → Hand off to user for review/commit

---

## Self-Check

### Core Success Criteria (ALL must be met)

- [ ] **README file created**: Written to project root as `README.md` with complete standard structure
- [ ] **All 9 required sections present**: Title/badges, Description, Features, Installation, Quick start, Usage, Contributing, License, Authors
- [ ] **Installation commands executable**: Copy-paste commands work without modification (no hardcoded paths or broken links)
- [ ] **Three-second clarity test passed**: Reader understands project purpose within 3 seconds of viewing
- [ ] **License section included**: License type specified and linked to LICENSE file

### Process Quality Checks

- [ ] **Tone**: Is the text direct and concise, without bureaucratic or report-like phrasing?
- [ ] **Badges**: Do badge links point to the correct branch or file?
- [ ] **Narrow screens**: Are tables and long code blocks readable on small screens?
- [ ] **No invention**: Did I avoid inventing features or commands not provided by user?
- [ ] **Placeholders used**: For missing information, did I use clear placeholders (e.g., "TBD") rather than guessing?

### Acceptance Test

**Can a new developer understand what the project does, install it, and run a basic example within 3 minutes using only the README?**

If NO: README is incomplete or unclear. Review sections for missing information or confusing instructions.

If YES: README is complete. Proceed to handoff.


## Examples

### Before vs after

**Before (minimal)**:

> # MyProject
>
> This program processes images.
> Install: pip install .
> Run: python run.py

**After (standard)**:

> # MyProject
>
> [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
>
> A high-performance image batch-processing tool that speeds up compression with concurrency.
>
> ---
>
> ## ✨ Features
>
> - **Concurrent compression**: Multi-threaded; faster than baseline.
> - **Formats**: WebP, PNG, JPEG conversion.
>
> ---
>
> ## 📦 Installation
>
> ```bash
> pip install my-project
> ```
>
> ---
>
> ## 🚀 Quick start
>
> ```python
> from myproject import Compressor
> Compressor('images/').run()
> ```

### Edge case: Legacy project with little info

- **Input**: Name: legacy-auth. No description. No feature list. Environment and install unknown.
- **Expected**: Still produce a structurally complete README; use placeholders (e.g. “See source for features”, “Install steps TBD”) and mark “to be completed”; do not invent features or commands; keep badges, section order, and License so the user can fill in later.

---

## Appendix: Output contract

When this skill produces a README, it follows this contract:

| Section order | Required |
| :--- | :--- |
| 1 | Title and badges |
| 2 | Core description |
| 3 | ✨ Features |
| 4 | 📦 Installation |
| 5 | 🚀 Quick start |
| 6 | 📖 Usage / configuration |
| 7 | 🤝 Contributing |
| 8 | 📄 License |
| 9 | 👤 Authors and acknowledgments |

Restrictions: no broken links; no redundant repetition; no hardcoded paths; License section required.

---

## References

- [GitHub README docs](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)
- [Awesome README](https://github.com/matiassingers/awesome-readme)
- [Shields.io (badges)](https://shields.io/)
