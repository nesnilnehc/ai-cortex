---
artifact_type: technical-design
lifecycle: snapshot
created_at: 2026-10-28
parent: ./2026-10-28-skill-provenance-functional-design.md
status: approved
---

# Technical design: Skill provenance presentation

## Goal

Validate version-bound provenance decisions for the whole catalogue and generate matching index and static website labels with accessible evidence navigation.

## Architecture and service decomposition

| Boundary | Input and responsibility | Output |
| --- | --- | --- |
| Local maintenance | Current Skill files, creation evidence, external sources and explicit human decisions | Reviewed records |
| Shared Python validator | Local records and complete file inventory; no network | Validated catalogue or actionable errors |
| Index and website export | Same validated catalogue | Markdown index and static provenance JSON |
| Browser presentation | Static JSON and existing locale resources | Badges and evidence links |

Internal dependencies are the existing index generator, provenance module and website discovery components. External sources are maintenance evidence only, never runtime dependencies. There is no new service or network approval endpoint. Covers requirement R1–R7 through the approved functional design.

## Components and detailed design

Extend `scripts/skill-provenance.py`, keeping validation independent of presentation:

- `inventory(skill_dir: Path) -> dict[str, str]`: complete distributed relative file paths and SHA-256 values; reject symlinks and paths outside the Skill. Ignore no distributed files.
- `load(root: Path, skills_dir: Path) -> dict[str, ValidatedRecord]`: validate the full record set, evidence references, confirmations and file inventories. Missing and extra Skill keys are errors.
- `validate_record(name: str, record: dict, inventory: dict) -> ValidatedRecord`: bind the decision to content and check category-specific evidence.
- `review_packet(name: str, record: dict, inventory: dict) -> str`: produce the R7 review fields and a reasoned recommendation; never create a human confirmation automatically.
- `export_public(records: dict, source_revision: str) -> dict`: allowlist public fields, resolve evidence to version-pinned repository URLs and return the static projection.

`ProvenanceError` carries `code`, `skill`, `field`, `message` and `next_action`. The implementation must replace the current regular-expression-based source-registry extraction with a parser for the explicitly supported registry grammar, rejecting unsupported structures rather than guessing. Preserve the no-third-party-runtime-dependency constraint; parser behavior needs focused boundary tests.

Extend `scripts/sync-skills-index.py`: validate once, render index, public JSON and the managed static fallback regions in memory, then write only after all validation and rendering pass. `--check` compares every generated artifact without writing. Preserve existing flags and exit codes; add the isolated preview option defined below. A generation interrupted between replacements is detected by the next full artifact check.

Website changes follow the functional design's UI decisions:

| Component | Ownership and change |
| --- | --- |
| `website/explore/workflow.mjs` | Join static provenance with metadata by Skill ID; reject incomplete joins before mounting an interactive catalogue |
| New `website/explore/provenance.mjs` | `getProvenance(id, locale)` and `createEvidenceAction(id, locale)`; text via text nodes, checked links, no HTML interpolation |
| Classification, relationship and search renderers | Badge top-right region and sibling evidence action; retain existing selection controls and state ownership |
| Detail panel renderer | Same classification/evidence; preserve focus restoration and existing mobile sheet behavior |
| `website/explore/dual.css` | Reuse tokens; reserve badge space and wrap before names rather than overlaying them |
| Static English and Chinese pages | The index generator owns explicitly marked provenance fallback regions in `website/index.html`, `website/zh.html`, `website/explore/index.html` and `website/explore/zh.html`; reject missing/duplicate region markers and preserve surrounding content. Check fallback labels/evidence against the projection |
| Website catalogue maintenance | Frontend contributor updates `website/explore/skill-metadata.json`, both locale files, `classification.json` and applicable relationship/support inventories; validate against repository IDs before generation |

No new persistence for reader state: existing selection/search/view/scroll owners remain authoritative. Evidence navigation uses native links with the existing source-link convention and return path. No interactive element is nested inside another interactive control. Render no partially classified Skill while loading. A failed join produces an accessible catalogue error and retains access to previously generated static content; delivery checks prevent that mismatch from being shipped.

## Database design

No database change. Repository files are the storage model.

Proposed `skills/PROVENANCE.json` schema version 2 retains the three classification identifiers as identifiers, not display strings. Each Skill record has:

| Field | Type and constraints |
| --- | --- |
| `classification` | One of the existing three identifiers; no unknown category |
| `version` | Nonempty Skill frontmatter version |
| `reviewed_files` | Nonempty relative-path to SHA-256 map matching current inventory |
| `reviewed_evidence` | Non-confirmation evidence file path to SHA-256 map; exact structure below |
| `evidence` | Nonempty array of repository-relative public evidence references |
| `creation` | Original only: creation commit or requirement reference |
| `sources` | Array of source IDs and roles: creative reference, tool lookup or copied upstream |
| `decision` | Maintainer identity, ISO date, confirmed/corrected action, rationale and public evidence references |
| `upstream_ref`, `upstream_files` | Unchanged upstream only: immutable source revision and complete upstream file map |

All records are version-bound. A packet is a derived maintenance artifact, not a second classification authority. Its pending/withdrawn states must never become public classifications. Store a human-confirmed result only after explicit confirmation; the validator checks completeness and version binding, not the truth of a human attestation.

`skills/SOURCES.yaml` continues owning upstream-copy pins, notices, licenses and modifications. For non-copy creative references, add a separate `references` collection inside that registry keyed by stable source IDs: URL, title, access date, source kind and local public evidence path. Such entries do not assert copying or reuse rights. Copy/adaptation of upstream Skill files still requires the existing licensing records. Article-informed rewrites link to reference entries without inventing an upstream repository or file version. Original records may contain tool-lookup references only.

### Exact record and decision binding

The root is `{schema_version: 2, skills: {<directory-name>: <record>}}`. Reject unknown fields, duplicate JSON keys, invalid dates, empty required strings and dangling source IDs. Category identifiers are `native`, `third_party_original` and `third_party_adapted`.

| Object | Exact fields and conditions |
| --- | --- |
| Evidence reference | `{path: string, anchor: string?}`; normalized repository-relative regular file, no traversal or symlink; anchor must resolve when present |
| `creation` | `{kind: "commit", revision: string}` with a resolvable 40-hex creation commit touching this Skill, or `{kind: "requirement", evidence: EvidenceReference}`; required for native, omitted otherwise |
| `sources[]` | `{id: string, role: "creative_reference" or "tool_lookup" or "copied_upstream", adaptation: string?}`; unique IDs, resolved against registry; adaptation required for creative reference or modified upstream copies |
| `decision` | `{maintainer: string, confirmed_at: ISO-date, action: "confirmed" or "corrected", classification: CategoryId, rationale: string, evidence: EvidenceReference[], subject_digest: Sha256}`; classification must equal the record's category; evidence is a nonempty public confirmation record |
| `reviewed_evidence` | Map of all non-confirmation evidence file paths to SHA-256 bytes; includes creation requirement and source evidence paths; compare against actual files |
| Source registry reference | `references.<id>` contains `{url: HTTPS-string, title: string, accessed_at: ISO-date, kind: "article" or "method" or "workflow" or "tool_documentation" or "skill", evidence: EvidenceReference}` |

For source-copy IDs, use `skill:<registered-name>` to resolve the existing `skills` registry entry; use `reference:<id>` for the new `references` collection. Native permits only tool-lookup roles and requires creation evidence. Adapted requires at least one creative-reference or modified-copy source. Unchanged requires a copied-upstream source, immutable revision and complete matching upstream file map. All categories require `decision`, `reviewed_files`, `reviewed_evidence`, version and nonempty public evidence references. Record-level `evidence` may point to the confirmation record as well as the non-confirmation evidence.

Bind confirmation to a subject object containing Skill ID, version, classification, reviewed file map, creation, ordered sources, resolved source-registry entries, non-confirmation evidence references and reviewed evidence hashes. Serialize with Python `json.dumps(sort_keys=True, separators=(',', ':'), ensure_ascii=False)`, encode UTF-8 and hash with SHA-256. Map keys sort; source arrays sort by ID and role; evidence arrays sort by path and anchor before serialization. Preserve string contents without silent normalization. `subject_digest` and all `decision` fields, including the confirmation document itself, are excluded to avoid self-reference. A decision's evidence reference cannot also be a non-confirmation input.

A source URL, adaptation description, category, creation reference, source evidence bytes or Skill file change invalidates the subject digest. Regenerate the packet and obtain fresh confirmation; do not update a digest on behalf of the maintainer. The confirmation record must state the subject digest and decision, so changing the record or its classification inconsistently fails validation. Public export revision changes alone do not invalidate a subject.

Examples use symbolic fixtures, not real attestations: a valid native fixture has `creation={kind: "requirement", evidence: {path: "evidence/creation.md"}}`, `sources=[]`, exact file/evidence hash maps and a confirmed native decision for the computed subject digest. A valid article-adapted fixture omits creation, references `reference:article-a` with role `creative_reference` and a nonempty adaptation, and has a matching adapted decision. An unchanged fixture resolves `skill:copy-a`, has matching upstream/local file maps and an unchanged decision. Store executable JSON instances with computed hashes in the schema tests; malformed or partially filled examples are not accepted records.

## Interface contracts

No HTTP API or event interface change. Local contracts:

- Existing generator command and `--check`: canonical generation requires the pinned-evidence checks below; success 0, invalid/stale data 1, bad arguments 2. Diagnostics go to stderr and identify the Skill, field and remediation. Authorized repository editing controls writes; no new authentication system.
- Proposed `python3 scripts/sync-skills-index.py --preview-dir <directory>`: generate index, projection and a local evidence mirror only into a new directory outside the repository; refuse existing/nonempty destinations and combination with `--check`. Mark the output as a local preview with `delivery_ready: false`; it cannot replace canonical outputs or pass the delivery gate. Evidence URLs are contained relative paths to copied public evidence. No unreviewed category is invented: unresolved records produce diagnostic packets rather than reader-facing output.
- Proposed `python3 scripts/skill-provenance.py --review <skill>`: read-only packet on stdout, same error codes; permits incomplete candidate records and reports missing fields without requiring whole-catalogue acceptance; never writes confirmations or fetches sources.
- Generated `website/explore/skill-provenance.json`: root `schema_version: 1`, `source_revision`, and `skills` keyed by ID, each containing only classification and public evidence URLs. It has no maintainer private conversation or raw investigation notes. Browser consumers reject unknown schema versions.

### Evidence revision and delivery readiness

Add `provenanceRevision` (40-hex Git commit) to `website/explore/source-manifest.json`; it is the single source of `source_revision` in the projection. Preserve `assetsRevision` for existing asset links. The revisions need not be equal: each must resolve and contain the bytes of the content it claims. Extend the source-link helper with a separate provenance evidence resolver supporting validated evidence paths, including `docs/`; do not relax the existing asset-path allowlist.

Before canonical generation, use local Git object reads to ensure the provenance commit contains the manifest, referenced registry entries, Skill files and all public evidence/confirmation records with exactly the reviewed bytes. Reject a pin to HEAD when those inputs have uncommitted changes; never silently substitute HEAD or the older asset pin. Generated outputs and the pin declaration itself are excluded from these source-content comparisons, avoiding a generated-file commit cycle.

Future delivery ordering: review and confirm local content; commit the source/evidence inputs under separate commit authorization; set the evidence pin to that commit; generate outputs; commit the generated bundle when authorized. Do not require the generated files to exist in the evidence commit. Local preview supports uncommitted but confirmed inputs without making remote links. The publication gate additionally requires evidence at the canonical public repository revision to be available, verified through an authorized publication/read workflow; offline generation asserts only local Git existence, never remote availability. No commits, pushes or authenticated requests are authorized by this design itself.

| Shared value | Single defining location | Consumers and reconciliation |
| --- | --- | --- |
| Per-Skill decision | `skills/PROVENANCE.json` | Python validation -> index and website projection; `--check` verifies generated copies |
| Category identifiers | `specs/skill-source-modeling.md` | Python and browser enum checks use contract fixtures containing all three values |
| English label wording | `website/explore/locales/en.json`, new provenance keys | Browser directly; index generation reads the same three strings |
| Chinese wording and evidence/error text | `website/explore/locales/zh.json` and corresponding English keys | Existing locale resolver; locale-key parity tests |
| Source details | `skills/SOURCES.yaml` | Validator resolves source IDs; public projection links to pinned evidence |
| Evidence commit | `website/explore/source-manifest.json`, `provenanceRevision` | Generator exports it; browser consumes projection; delivery checks verify provenance pin and separately validate asset pin |

## Data flow and error handling

Maintenance review -> record edit -> complete inventory and evidence validation -> both renders -> artifact checks -> existing website delivery preparation. No delivery or remote publication is performed by this command.

| Failure | Detection | Recovery |
| --- | --- | --- |
| Missing, duplicate, malformed or inconsistent record | Strict JSON key/type checks and full ID-set comparison | Fail before output writes; list affected Skill and missing field |
| Content or source evidence changes after confirmation | Compare current subject digest, evidence hashes and version/file inventory | Require a fresh packet and decision for current content |
| Traversal, symlink or unsafe evidence URL | Resolve local paths under repository root; allow only generated HTTPS public source URLs | Reject and identify the invalid reference; never follow it |
| Output write interrupted | Write temporary siblings then replace; compare both outputs on next check | Nonzero exit; do not publish; regenerate both from authority. Two-file replacement is not an atomic transaction |
| Browser projection mismatch | Schema and full join check before mount | Accessible error and static fallback; build/integration gate blocks delivery |
| Evidence target unavailable remotely | Native navigation failure | Reader retry/back; maintenance repairs evidence. Local validation makes no remote-availability claim |

## Technology choices and trade-offs

| Option | Advantages | Drawbacks | Decision |
| --- | --- | --- | --- |
| Extend existing Python validator and static export | One validation path, no network/runtime service | Additional generated artifact and checks | Chosen |
| Browser reads raw registries | Fewer generated files | Duplicated validation and exposure of maintenance-only fields | Rejected |
| New review web service | Structured interactive approvals | Accounts, deployment and operational burden without a required new user capability | Rejected |

Dependencies: existing Python standard library, static ES modules, locale resources and Node/Python test runners. No new download or installation. Risks: manual attestation quality, whole-catalogue backfill effort and stale deployment bundles; mitigate with review packets, coverage gate and complete-bundle parity checks.

## Migration plan

This is a breaking local manifest migration. First implement schema-2 validation, fixtures and exporters in isolation. Extend the source contract and reference registry model, retaining the current source-copy obligations. Prepare per-Skill packets against current content, obtain actual maintainer confirmations and backfill records; never translate schema-1 dates or generic originality prose into fabricated attestations.

The inspected baseline has 72 repository Skills and 70 website metadata entries; eli5 and Ponytail are absent from the latter. Treat these numbers as dated evidence, not a hardcoded target. Before switching, the frontend contributor adds their metadata and source hashes, English/Chinese names, purposes and guidance, and reachable classification ownership. Use a task-appropriate existing category; determine its ID by inspecting the existing category definitions during implementation and ensure the selected owner resolves. Add relationship/support entries only when supported by the corresponding Skill, without inventing links to satisfy counts. Verify search and detail access for each addition. Preserve the already imported Skill files and external-source records.

The generator contributor owns a coverage preflight: the set discovered from `skills/*/SKILL.md`, provenance record IDs, website metadata IDs, locale Skill IDs and the union of classification memberships must match exactly. Relationship/support references must resolve to that same set; their subsets need not cover it. Fail on dangling IDs, missing locale guidance, unresolved owners and dropped Skills. Fixture tests start from the observed 72/70 mismatch and show that adding provenance records alone is insufficient. Recompute the current ID set rather than freezing these counts.

Switch both consumers and generation together only when every Skill has a valid record and website coverage passes. Regenerate index, projection and static fallbacks; reconcile counts against the full repository catalogue. Existing eli5/Ponytail files and source records are inputs, not reimports. Preserve all unrelated working changes.

Before switching, retain the previous manifest and generated bundle through normal Git review history or an explicit local backup if still uncommitted. If checks fail, retain the prior delivery bundle and investigate. Rollback restores the previous reader, manifest and generated outputs together; retain collected confirmation evidence for reapplication. Do not publish a schema-2 partial catalogue or remove unresolved Skills to make validation pass.

## Test strategy

Use TDD for parser, version-binding, validation, export and browser state logic: observe focused tests failing before implementation, then pass and refactor. Unit fixtures cover category precedence, creation/attestation evidence, tool-only references, article rewrites, duplicate keys, all file mutations, traversal, source conflicts and missing confirmation.

Integration: temporary isolated repository fixtures feed all generated outputs, compare every Skill and label, exercise `--check` without writes, and verify invalid inputs leave outputs unchanged. Existing `scripts/test-skill-provenance.py` and `scripts/test-skills-index.py` are extended; do not weaken existing licensing checks. Add generator/browser contract tests under `tests/website/`.

Browser acceptance owner: implementing contributor; classification acceptance owner: maintainer. Inspect both third-party labels and unbadged confirmed originals across all Skill locations at 360px/1280px and both themes in English/Chinese, including long names. Exercise keyboard-only selection, evidence navigation, return focus, search, empty search and view-state preservation. Inspect no-JavaScript fallback and inaccessible evidence recovery. Record screenshots and interaction results; code assertions do not prove visual acceptance.

Existing commands: `python3 scripts/test-skill-provenance.py`, `python3 scripts/test-skills-index.py`, `python3 scripts/sync-skills-index.py --check`, `node --test tests/website/*.test.mjs`, and `python3 -m unittest discover -s tests/website -p 'test_*.py'`. Documentation/asset changes additionally follow CONTRIBUTING checks. Add integration cases for a nonexistent evidence commit, stale asset/evidence pins, dirty source files, a valid source commit without generated outputs, preview output isolation and unavailable public evidence at the publication gate. Change source URLs, source descriptions and evidence bytes without modifying Skill files and assert that confirmation is invalidated. Verify that confirmation-document self-reference is rejected and that unchanged pins reproduce identical outputs. No implementation tests have run as part of this design document.

## Quality attribute design

| source | rule_refs | design tactic | trade-off | verification | owner |
| --- | --- | --- | --- | --- | --- |
| QAS-01, FD-06/07 | TST-001, TST-003 | Sibling evidence actions, reserved layout regions, existing focus/state owners | More row space | Browser visual and keyboard checks at required widths/themes | Frontend contributor |
| FD-01/03 | ARC-001, ARC-005 | One validator; explicit manifest version and synchronized consumer migration | Coordinated backfill | Old/new schema fixtures and full output parity | Generator contributor |
| FD-05 | REL-004 | Validate before writes; detect partial output and keep old deployment bundle | Local generation needs rerun after interruption | Write-failure and changed-content tests | Generator contributor |
| FD-04/08 | SEC-001, SEC-003 | Contained evidence paths, escaped text and allowlisted public projection | Extra validation | Traversal, injection and private-field rejection fixtures | Generator/frontend contributor |

Rule references resolve to the existing architecture, testing, reliability and security quality documents. This local static change introduces no service SLO, retry loop, background queue or production telemetry budget. No project configuration file was present during investigation; no profiles or waivers are inferred. Resolve any additional applicable parameters during engineering review before approval.

## Acceptance criteria

1. Whole-catalogue validation and both output checks pass only with a complete, current manifest; invalid input preserves outputs. Covers FD §Acceptance 1 and 5.
2. Original, unchanged-copy and reference-informed adaptation fixtures obey classification and evidence contracts. Covers FD §Acceptance 2 and 3.
3. The read-only review command emits the full packet and recommendation; only an actual recorded human decision satisfies validation. Covers FD §Acceptance 4.
4. All required browser surfaces pass documented responsive, keyboard, evidence-navigation and state-recovery checks. Covers FD §Acceptance 6 and 7.
5. Generator and browser consume the declared sources without upstream retrieval or changes to Skill invocation. Covers FD §Acceptance 8.
6. Full migration includes website metadata/locales/classification backfill, exact dynamic ID-set equality, separate asset/evidence pin validation, isolated local preview and rollback checks before delivery preparation. Covers FD §Acceptance 1 and 5.

## Approved display amendment — 2026-10-28

The [REQ 08 display amendment](../requirements-planning/AIC-REQ-08.md#display-amendment--2026-10-28) changes rendering only: `native` suppresses the badge after complete record validation; both third-party categories retain badges. Index, static fallbacks, directory rows and dynamic renderers retain evidence access for all three categories. No projection record or validation requirement is removed.
