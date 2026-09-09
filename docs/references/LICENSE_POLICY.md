---
artifact_type: reference
created_by: ai-cortex
lifecycle: living
created_at: 2026-03-24
status: active
---

# License policy

This file defines the license and notice requirements for AI Cortex's original skills and for externally derived ones.

## 1. Original skills

- An original AI Cortex `skills/*/SKILL.md` declares `license: MIT` by default.
- The [`LICENSE`](../../LICENSE) at the repository root covers AI Cortex's original content. It does not cover vendored content that carries a license of its own.

## 2. Externally derived skills

- Every externally derived skill must enter `skills/` as a reviewed local copy and be registered in [`skills/SOURCES.yaml`](../../skills/SOURCES.yaml).
- The source must be pinned to a full commit, a Git tree and the SHA-256 of `SKILL.md`. A branch, a tag, `latest` or a raw URL must never be the basis for distribution.
- Only a license that explicitly permits copying, modification and redistribution is accepted. MIT, Apache-2.0, BSD-2-Clause and BSD-3-Clause may go to review; where no license is found, or the license is unclear, the skill must not be vendored.
- A skill's frontmatter `license` must carry the SPDX license expression that actually applies to that local copy. Labelling Apache-2.0-derived content as MIT for the sake of a uniform look is forbidden.
- The copyright and license text the upstream requires must be preserved. The central notices are in [THIRD_PARTY_NOTICES.md](./THIRD_PARTY_NOTICES.md), and the full license may be kept alongside the skill as `LICENSE.upstream`.

## 3. Maintenance and release

- Checking and updating the upstream happens only during maintenance, and lands after the diff, the license, the scripts and the assets have all been re-reviewed. An agent must never install or upgrade an external skill at runtime.
- SPDX is generated from `skills/SOURCES.yaml`, the local files and the license notices. It is a release audit artifact and replaces neither the source registry nor the update process.
- When an externally derived skill is deleted, remove its source registration, any license copy no longer used by anything else, and its notice entry at the same time. Git history keeps the provenance of the old version.

## 4. References

- [skill-source-modeling.md](../../specs/skill-source-modeling.md): the data contract for the source registry
- [ATTRIBUTIONS.md](./ATTRIBUTIONS.md): the human index of the externally derived skills
- [THIRD_PARTY_NOTICES.md](./THIRD_PARTY_NOTICES.md): the license and copyright notices
