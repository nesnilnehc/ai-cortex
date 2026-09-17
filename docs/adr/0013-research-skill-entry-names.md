---
artifact_type: adr
created_by: decision-record
lifecycle: snapshot
created_at: 2026-09-17
status: accepted
description: Keep five requested research commands as canonical flat Skills, with one internal assessment Skill and ID-named requirements.
---

# ADR 0013: Research Skill entry names and requirement paths

## Context

AI Cortex installs one Skill per immediate `skills/<name>/` directory. The five research names requested by users are `deep-research`, `policy-research`, `market-research`, `competitive-research` and `product-opportunity-analysis`. Four are noun-led and the package-producing entry lacks the usual `orchestrate-` prefix. Renaming them would change the commands users were promised. A nested `skills/research/` directory would not be discovered by the current index generator or installer.

The requirement modeling Spec requires an ID filename (`<PROJECT>-REQ-<nn>.md`), while `docs/ARTIFACT_NORMS.md` still says `{topic}.md`. The hierarchy in `AGENTS.md` gives the Spec precedence.

## Decision

Keep the five requested names as canonical flat Skill directory names and direct commands. Add a narrow naming exception for this research family; other new Skills continue to follow the verb-noun rule, and an orchestrator outside this named package entry continues to use `orchestrate-`.

Add `assess-product-opportunity` as a local domain synthesis Skill. It owns the recommendation logic, while `product-opportunity-analysis` selects relevant research lanes, coordinates handoffs and aggregates the Opportunity Package. It is internal by repository metadata; platform UI hiding is a compatibility concern tested separately.

Use `docs/requirements-planning/<PROJECT>-REQ-<nn>.md` for requirement files, matching the higher-precedence requirement Spec. Keep descriptive H1 titles and links for discovery. This naming decision does not alter the requirement lifecycle defined by the Spec.

## Alternatives

- **Rename the public Skills to verb-noun forms**: rejected because the direct commands would differ from the user-facing contract already established in AIC-REQ-01.
- **Add alias Skills under the requested names**: rejected because duplicate Skill directories would create extra registry entries and two versions of the same behavior.
- **Nest the research family under `skills/research/`**: rejected because it requires a broad installer and index migration for a presentation concern.
- **Keep `{topic}.md` for requirements**: rejected because it conflicts with the higher-precedence requirement modeling Spec.

## Consequences

The naming rule gains one documented exception, while the normal naming formula remains intact. Six Skill directories will be installed for five public entries; runtimes that do not honor a hidden/internal flag may still list the internal Skill, so the usage guide and smoke tests must state the actual behavior. Requirement links and planning guidance must use the ID filename. The Opportunity Package remains a separate Spec and does not redefine the Release Package.
