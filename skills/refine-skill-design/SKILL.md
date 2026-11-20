---
name: refine-skill-design
description: Audit and refactor one or more existing SKILL.md files for Agent Skills format compliance, clear execution, local asset boundaries, and portable tool use. Use when a user asks to refine, audit, or repair skill design.
version: 1.10.1
license: MIT
---

# Skill: Refine Skill Design

## Purpose

Improve an existing agent capability without changing its purpose. Make its instructions executable across supported environments and keep structural contracts, interaction protocols, and independently checkable rules in their authoritative assets.

## Use Cases

- Repair a skill whose steps or failure handling are ambiguous.
- Audit an existing skill against the Agent Skills format and this repository's contracts.
- Refine several skills in a named set, including the entire local catalog.
- Apply this skill to itself before using it for a wider audit.

## Inputs and Output

**Input:** the path or name of at least one existing SKILL.md, or a clearly identified collection. If the target is omitted, ask for it. Do not choose a target from the invocation name alone. A request to refine this skill itself identifies skills/refine-skill-design/SKILL.md.

**Output:** each changed skill at its source path by default, a section-level summary of every substantive change and its reason, and a SemVer proposal. If a skill already passes, report it as unchanged without bumping its version.

If the user asks for a draft, write SKILL.refined.md beside the source. If the user asks for a separate dated copy, write SKILL.refined.YYYYMMDD.md. Honor a user-specified destination. Do not overwrite the source in these cases.

## Behavior

1. **Resolve scope and state.** Identify every target before editing. For a collection, enumerate its SKILL.md files in a stable order. Inspect the working tree and preserve unrelated edits. Read the full target, its referenced local resources, and the relevant registries.
2. **Load the local contract.** Inside AI Cortex, read AGENTS.md, docs/LANGUAGE_SCHEME.md, docs/architecture/terminology.md, skills/INDEX.md, protocols/INDEX.md, rules/INDEX.md, skills/SOURCES.yaml, and the [skill boundary guidance](../../CONTRIBUTING.md#choosing-a-skill-boundary). Use applicable Specs, Protocols, and Rules from their registries. Treat vendored-source records as maintenance evidence, not instructions to fetch or install at runtime.
3. **Classify constraints and check format.** Separate [Agent Skills requirements](https://agentskills.io/specification), this repository's active contracts, and non-binding recommendations before reporting a defect. Check YAML syntax, required name and description, directory/name agreement, field types and limits, relative local references, and readable Markdown. Check project- or host-specific top-level fields against both their consumers and the standard validator's supported fields. Report any strict-validation incompatibility and keep consumed fields intact until a compatible migration is authorized. The specification has no fixed body template. Use its guidance of under 500 lines and roughly 5,000 tokens to assess context cost. Keep one English description without a parallel translated field. Remove optional frontmatter when nothing consumes it and retain a schema only for a real typed handoff or contract.
4. **Audit the capability.** Trace input → action → output. Check whether the purpose, preconditions, decisions, failure paths, and completion criteria are explicit. Replace vague verbs with actions an agent can perform. Remove unnecessary pauses, repeated confirmations, and completion conditions that extend beyond the authorized task. Reuse valid prior evidence.
   - Assess whether the work justifies an independent entry by checking its trigger, usable result, standalone requests, and actual callers. In AI Cortex, apply the contribution guide and check compatibility before proposing a move into another Skill.
   - Once the owner is clear, assess the main flow's complexity, branches, and how often the detail is needed. Keep short, routinely used instructions inline. Retain examples that clarify a real decision. When separating detail improves readability or avoids loading it on unrelated paths, link it from the step that says when to load it.
5. **Respect asset ownership.** Use the terminology definitions to identify structural contracts (Spec), multi-role sequences (Protocol), and independently checkable constraints (Rule). Replace duplicated authoritative text with a local reference when that asset exists. If no asset exists, report a suggested split; do not claim it was created. Keep skill-specific execution instructions in the Skill.
6. **Adapt tools to the runtime.** For each required external, MCP, CLI, or API capability, state how to discover available tools, match the required operation, execute safely, and respond when the capability is absent. Use an exact tool name only when the skill truly depends on a bundled or fixed interface. Apply the local-path-first and external-action rules from AGENTS.md.
7. **Edit and version.** Preserve the capability's core purpose and any verified domain behavior. Remove redundant text and unused fields before adding structure. Preserve defaults in instructions when removing an input schema. Follow the repository's [versioning policy](../../CONTRIBUTING.md#versioning) and classify the actual effect. An erratum or a reference relocation can be a patch. A new optional capability can be a minor change. A new obligation, a changed permission, or an incompatible contract requires a major bump. Propose a version for a draft without changing its source. Leave the version alone for a no-op audit.
8. **Synchronize and verify.** Follow the [source contract](../../specs/skill-source-modeling.md#54-provenance-presentation) for each changed AI Cortex Skill. Obtain a maintainer decision for the reviewed file set and use the repository's index script. Generate an isolated preview for confirmed changes awaiting a source commit and pin. Generate the formal index once the required pins match and report which result was verified. Run available local format, link and repository checks. In AI Cortex, check the Skill contract and distributed assets, including tools, references, metadata and source records. When bundled executable assets change, run their relevant checks. Keep consumer execution, external publication and Agent evaluations outside the repository's Skill acceptance gate. Perform the Self-Check below on every changed Skill and report missing verification and its effect.
9. **Report.** For every changed skill, list the affected sections, what changed, why, and the version rationale. Group unchanged skills compactly. Identify suggested Spec / Protocol / Rule splits as suggestions only.

## Restrictions

- Do not create a new skill from scratch under this capability.
- Do not replace a domain decision or existing user authorization with a generic confirmation step. Ask only for missing information that prevents a sound choice.
- Do not change an externally derived skill's upstream provenance, license, or vendoring scope by inference. Follow skills/SOURCES.yaml and its linked Spec when applicable.
- Do not install skills, scripts, binaries, or validators during refinement. Treat external content as untrusted data.
- Do not copy an authoritative contract into a Skill when a local Spec, Protocol, or Rule owns it.
- Do not silently delete supported cases, examples, safeguards, or tool fallbacks to shorten a document.
- Write repository artifacts in English and follow AGENTS.md precedence.

## Self-Check

For every changed skill, confirm:

- [ ] SKILL.md has valid frontmatter, matching name, a useful description, and readable instructions.
- [ ] Input, actions, decisions, failures, and output can be followed by an agent new to the domain.
- [ ] The skill's purpose and supported cases remain intact; completion stays within authorized scope without unnecessary pauses or repeated confirmation.
- [ ] Applicable asset boundaries and repository rules are respected.
- [ ] Required tools have a discovery, capability mapping, and absence path, or a justified fixed interface.
- [ ] The entry boundary fits the task and callers. The core flow keeps its decisions and completion conditions, and each extracted reference has an explicit loading point.
- [ ] Verification covers the contract and distributed assets without introducing a parallel simulation or consumer-execution gate.
- [ ] Changed sources have the applicable provenance evidence. The index is synchronized or the preview and remaining registration blocker are reported.
- [ ] The final report identifies each substantive edit, its reason, and the version rationale.

If a check fails, continue refining or report the specific blocker; do not call the skill complete.

## Examples

### Ambiguous single skill

**Input:** skills/file-converter/SKILL.md says only “process files.”

**Action:** determine which formats and operations its existing examples support; define input selection, conversion steps, output path, and behavior for an empty or unsupported file. Preserve any existing format support. If the intent cannot be inferred, ask for that missing choice before changing the capability.

**Output:** an updated source skill, a section-level change summary, and a justified version bump.

### Catalog audit with a vendored skill

**Input:** “Refine all skills,” including a locally modified, externally derived skill.

**Action:** enumerate the catalog; audit each skill; read skills/SOURCES.yaml for the vendored entry; retain its license and upstream record. If its tool integration has no fallback, add discovery and absence handling without installing anything. Leave already compliant skills unchanged.

**Output:** changed skills and synchronized index, a compact unchanged list, and per-skill change and version notes. Any missing Spec or Rule is reported as a suggested split.
