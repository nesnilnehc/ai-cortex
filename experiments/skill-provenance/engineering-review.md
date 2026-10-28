# REQ 08 engineering review record

Date: 2026-10-28. Scope: provenance-related changed and untracked files in the shared main checkout. Unrelated release/backlog work is excluded. This record preserves review checkpoints and repaired findings; the complete feature-branch engineering gate passes at closeout.

## Findings and repair evidence

| Location | Category | Severity | Title | Description | Maturity | Suggestion / disposition |
| --- | --- | --- | --- | --- | --- | --- |
| `scripts/sync-skills-index.py:43` | scope | major | Folded description becomes a YAML indicator | Ponytail uses a folded description, but the generated discovery index contained only `>`. A self-consistency check could not detect the lost description. | ready | Fixed: normalize folded/literal description blocks into one index paragraph. Four independent expected-value cases failed before the fix and pass afterwards. |
| `scripts/skill_provenance_v2.py:423` | language-python | minor | Malformed review candidates raise runtime exceptions | A non-object candidate raises AttributeError; list/dict classifications raise TypeError during set membership. The maintenance interface loses its actionable validation report. | ready | Fixed: validate the candidate object and classification type. Four malformed candidate shapes failed before the guard and pass afterwards. |
| `scripts/skill_provenance_v2.py:30` | cognitive-reliability | major | Git inspection has no finite attempt limit | `reliability-quality@1.3.0/REL-001`: local Git subprocesses could wait indefinitely, preventing review or generation from completing. | ready | Fixed: all provenance Git attempts use a 30-second subprocess timeout and convert timeout/start failures to actionable stable errors. A deterministic injected timeout failed before implementation and passes afterwards. No implicit retries or network fetches were added. |

## Review progress and limits

The scope checklist covered intent, regression, compatibility, repeated generation and failure visibility. Python inspection covered exception handling, synchronous subprocesses, context-managed staging, standard-library dependencies, mutable defaults, naming and test injection. No React/Vue or ORM is used; those steps do not apply.

Security inspection traced JSON/YAML inputs to filesystem paths, Git argument arrays, HTML escaping and allowlisted browser evidence URLs. The change adds no shell execution or credential access. SHA-256 uses Python hashlib to bind evidence bytes; it does not prove authorship. Tool-assisted security coverage and the remaining cognitive checks still require completion before the engineering gate can pass. No vulnerability or secret scan is claimed.

All cognitive review steps have now been evaluated for the implemented scope. [Per-Skill Rule coverage](engineering-coverage.json) preserves passed, waived, not-applicable and evidence-limited outcomes separately. No waiver was granted. Framework and ORM steps remain not applicable. The final assembly evidence for TST-003 is limited by the missing real manifest and final migration/browser checks; the complete delivery gate therefore remains open.

Additional findings were repaired after observed failing regressions:

| Location | Category | Severity | Title | Description | Maturity | Disposition |
| --- | --- | --- | --- | --- | --- | --- |
| `scripts/skill_provenance_v2.py#link_inventory` | cognitive-security | major | A replaced parent directory escapes the distribution | `security-quality@1.3.0/SEC-001`: a tracked child could be read through a replaced, ignored parent symlink. The demonstrated consequence is hashing outside-distribution bytes rather than disclosure of their raw contents, supporting major severity. | ready | Reject symlink parents before reading files. Real temporary Git regression passes. |
| `scripts/skill_provenance_output.py#fallback` | cognitive-security | critical | Group identifiers are unescaped HTML attributes | `security-quality@1.3.0/SEC-001`: a quoted group identifier could insert an event-handler attribute into generated HTML. | ready | Escape attribute values and audit adjacent name/source attributes. Injected-quote regression passes. |
| `scripts/skill_provenance_v2.py#validate_record` | cognitive-error-surfacing | minor | Nested failures omit the affected Skill | `error-surfacing-quality@1.2.0/ERR-004`: batch validation errors could report an invalid maintainer without saying which Skill needs correction. | ready | Preserve existing structured errors and attach the Skill identity at the record boundary; regression passes. |
| `website/explore/provenance.mjs#initializeProvenance` | cognitive-observability | minor | Bootstrap failure loses diagnostic context | `observability-quality@1.3.0/OBS-008`: a generic reader alert alone cannot distinguish fetch, parse, projection and revision failures. | ready | Emit one safe stage diagnostic through the owning host; exclude raw exception contents. Direct negative assertion passes. |

The cumulative repaired findings are one critical, three major and three minor findings across seven file/function sites. There are no unresolved production-defect findings from these inspected paths; evidence limitations remain explicit. [Static import analysis](import-review.json) found zero cycles across 30 local modules. [Credential-pattern scan](security-scan.json) found no matches in 84 changed/untracked text files; it is not a universal secret detector or vulnerability scan.

## Reproduction

- `python3 scripts/test-skills-index.py`: clean-tree, metadata, malformed-tree and block-description fixtures, plus legacy and reviewed provenance suites.
- `python3 scripts/test-skill-provenance-v2.py`: 31 tests pass, including deterministic malformed-input, timeout and interrupted-generation cases.
- `python3 scripts/sync-skills-index.py --check`: full 72-Skill migration index must match generated sources.

The live provenance manifest still uses migration schema 1. The user has confirmed all 72 proposed classifications and the stated originality facts. The actual confirming maintainer is now identified by task and all 72 effective schema-2 decisions have been written and validated; synthetic tests do not replace that remaining field.

## Final cutover and delivery

The final cutover exposed one additional major scope finding at `scripts/sync-skills-index.py#main`: the migration-only schema-1 write fallback could regenerate an unresolved catalogue after schema 2 became authoritative. An observed failing regression showed exit 0 and an overwritten index; formal generation now requires schema 2 and returns `MIGRATION_REQUIRED` without writing. The legacy maintenance review remains read-only. The corresponding contract text is explicit.

The eight previously recorded production findings are repaired: one critical, four major and three minor. A separate committed-tree test-oracle correction now checks HTML-encoded names and purposes rather than requiring raw ampersands. Final Rule coverage has no unresolved evidence limitation for the delivered scope; the complete real bundle and public links are verified in [delivery closeout](delivery-closeout.md). Historical review-progress statements above describe their earlier checkpoints.

Legacy fallback presentation was also reconciled in both `website/explore/index.html` and `zh.html`: shared local stylesheets were absent. The new style-parity assertion failed before the links were added and passes afterwards. The 360px script-excluded legacy page now has four stylesheets, zero badge overlap and zero horizontal overflow; the final canonical homepage uses the public fixed-revision evidence.
