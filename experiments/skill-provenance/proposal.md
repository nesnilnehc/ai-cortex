# Skill provenance markers — working proposal

Date: 2026-10-28. Historical proposal; the user subsequently chose index presentation and exact upstream identity for unchanged copies. The first implementation is in [PROVENANCE.json](../../skills/PROVENANCE.json), the [source contract](../../specs/skill-source-modeling.md#54-provenance-presentation) and generated [index](../../skills/INDEX.md). It does not import `eli5` or establish facts about unaudited skills. Website presentation was not changed.

## Objective

Allow maintainers and users to distinguish an upstream-identical copy, a locally adapted upstream skill and a skill created in AI Cortex. Preserve unknown provenance rather than presenting it as original. Keep skill discovery and runtime behavior independent of provenance labeling.

## Current evidence

- [Skill Source Modeling](../../specs/skill-source-modeling.md) and [SOURCES.yaml](../../skills/SOURCES.yaml) register externally derived skills only, currently with `origin: vendored-derived` and a non-empty modifications list. That does not express an unchanged upstream copy or attest that an unlisted skill is original.
- [Attributions](../../docs/references/ATTRIBUTIONS.md) is the human-readable view of the upstream registry; notices and license files remain legal evidence. Two current registered skills (`commit-work`, `changelog-video`) are demonstrably adapted according to their recorded modifications and pinned upstreams. No blanket conclusion follows for the other 68 skills.
- [Index generator](../../scripts/sync-skills-index.py) reads each Skill's frontmatter, not the upstream registry. [ADR 0011](../../docs/adr/0011-vendor-external-skills.md) forbids runtime download or installation and requires reviewed, pinned external sources.
- Local `eli5` has a `SKILL.md` without an upstream URL, author, license or immutable source revision. Its provenance, distribution rights and whether it is an unchanged copy are unverified. No import is made by this proposal.

## Candidate definitions

| Display category | Proposed criterion | Evidence |
| --- | --- | --- |
| Third-party original | A reviewed local distribution matches a pinned upstream skill at the declared comparison scope; no local changes within that scope. The scope must explicitly address `SKILL.md`, bundled references/scripts/assets and metadata; byte-level identity is the conservative default. | Pinned source and exact files/digests, license and notice; comparison result and date. |
| Third-party adapted | The local skill copies, adapts or substantially derives its workflow or assets from a third-party skill, with local changes. | Existing source registry: immutable pin, license, notice and changes. |
| AI Cortex original | Evidence supports creation in this repository and no identified substantially copied third-party skill; ordinary citations and tool dependencies alone do not make it adapted. | Recorded basis and review date; creation history alone is a clue, not proof of absence of earlier upstream work. |
| Unverified | Evidence is missing or conflicting. | Missing evidence is explicit; never infer original merely from registry absence. |

The user chose exact identity: minor compatibility or format changes count as adaptation. A local wording or frontmatter adjustment is not described as byte-identical. A license may constrain modification and distribution regardless of category.

## Proposed design boundaries

- Maintain one authoritative provenance record per skill, with exact evidence and review scope; generate labels in the chosen discovery surfaces from that record. Avoid duplicating editable claims in a Skill body and a registry. Skills may link to the record for human readers.
- Reuse the existing upstream registry where practical. An unchanged third-party copy needs a compatible representation: current `origin` is fixed as `vendored-derived` and `modifications` cannot be empty. The Spec must be deliberately revised before claiming it supports such an entry. Do not conflate origin with local modification state merely to bypass the existing contract.
- Separate identity/evidence for original skills from the upstream registry's current external-only scope, or explicitly redesign that registry. Compare the cost and compatibility before choosing the authoritative location. Existing Skill frontmatter, index, source registry, licensing and historical consumers must stay consistent.
- A metadata/source mismatch, missing license or unresolved upstream is not automatically repaired by relabeling. A generator must detect conflicts and show or fail on `unverified`, not silently classify by omission. Avoid making existing skill invocation depend on network access or on a provenance field.
- Original upstream vs adapted is a property of a specified local version and comparison scope, not a permanent claim. Reclassify when the compared distributed files change. A provenance marker does not establish security or quality.

## Local validation plan

The index is the first presentation surface; the website and individual Skill bodies remain unchanged. Tests cover original, adapted, unchanged upstream, unknown and several conflicting/missing or changed inputs. They validate local structure and recorded hashes, not authorship or licensing truth. Continue independent source/license review before asserting a provenance class or distributing an external Skill. Never modify an unverified skill's origin merely to make the index complete.

`eli5` intake requires determining its actual source and applicable license before copying or redistributing. It may be original to a user, externally derived, or unverified; its name and local location do not establish which. Validate naming, package contents, license and repository policy at that time.
