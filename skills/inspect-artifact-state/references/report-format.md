# Artifact Inspection Report Format

## Default brief

Write as a colleague explaining the situation to a person, using connected prose. Start with the current artifact and what has actually been established. Follow with any material issue and its effect, then a useful next step if one is needed. Usually two or three short paragraphs are sufficient. Do not expose a fixed schema through labels such as "Current artifact", "Stage", "Issues", or "Next action". These are reasoning questions, not mandatory headings, numbered slots, or field names.

Cover these questions where relevant:

- What version/build is listed, at which location, and through which channel? Use the documented default when none was selected, and distinguish a newer candidate when it matters. A larger version is not automatically the recommended version.
- What channel, repository role, or directory/manifest label does the artifact currently have? Describe the observed placement or recorded label in ordinary language. Do not reconstruct lifecycle progress or infer testing, approval, or promotion from it.
- Does any observed problem affect this artifact or require attention? Focus on artifact-level findings such as missing requested files, conflicting identities, digest mismatches, or channel inconsistency against documented policy. CI job failures and historical publish errors are not default artifact findings; omit them from this artifact-only report.
- What, if anything, needs to happen next? Give the smallest useful action, distinguishing a current blocker from an optional check. Avoid inventing work merely to fill an action section. Recommendations do not authorize publishing, promotion, deletion, or configuration changes.

Keep technical names and identifiers only where they help locate or obtain the artifact. Prefer the project name in prose, with the exact package/channel when needed. Use precise link labels: a registry landing page is the documented instance/service name or "npm registry"; a package page is the package name; a verified tarball URL may be called an artifact download. Do not label a registry base URL as a direct download or promise installation/download success from metadata access alone. Prefer a known consumer endpoint when explaining how to obtain a package, while retaining the inspected source for evidence; if only a publication endpoint is known, do not invent an installation endpoint. Use artifact-source links rather than build records or repository changelogs. Do not force inventory counts, test counts, source SHAs, digests, status labels, or empty fields into the brief. Mention alternative channels when relevant to artifact choice, conflicts, or the user's question; keep full inventories for details.

Include observation time/timezone once when freshness matters, unobtrusively. If reusing an earlier observation, identify its time rather than implying a fresh query. For several artifacts, use a compact table when it makes comparison easier; avoid repeating a template for each artifact. Never omit a material issue or uncertainty to meet a length target.

Support major conclusions with one or two direct source links where available. Embed important limitations in the affected stage or issue instead of appending a long generic disclaimer. Unknown is not absent. Artifact presence, approval, integrity, and deployment are distinct. Never say "safe to use", "fully verified", or "ready for production" on the strength of publication metadata alone.

## Evidence and detail on demand

Expand only when the user asks, an anomaly needs explanation, or multiple artifacts require comparison. Preserve the plain-language summary and append only the relevant detail, not every table below. Do not create a report file or second JSON representation unless requested or required by project convention.

Collected evidence should retain these fields so a follow-up can be answered accurately; collect deeper artifact evidence only as warranted by the requested inspection. All artifact-state facts must originate in the registry, artifact directory, accompanying metadata, or inspected payload. Repository changelogs, release notes, Git history, and CI records are not report sources:

- **Scope:** project/component, actual ecosystem/protocol, artifact coordinates, instance/environment, effective endpoint and repository role, source-selection configuration, observation time/timezone, filters, access and traversal limits, pagination/truncation, and whether evidence was reused from an earlier observation. Retain the selected non-secret access-profile reference and whether the principal is known when relevant to coverage; do not expose credentials or insert account identifiers into the brief by default.
- **Inventory:** name, version, immutable artifact/build identifier, location, channel/stage, and time with its meaning. Keep separate builds/locations separate even if versions match. For npm, distinguish default-channel version, highest stable, highest prerelease, and most recent publication. Full inventories state count, coverage, and omitted entries. Publication, build, and modification times are not interchangeable.

- **Verification:** assess artifact presence/identity, location/version/channel, recorded stage, and integrity metadata. Source identifiers or test labels may be described only as metadata claims returned by the artifact source; do not investigate external process records here. Unknown or unperformed checks remain unverified; not every dimension needs its own row in the brief. Use the status vocabulary below in detailed tables.
- **Findings:** expected versus observed state, affected artifacts, evidence, and practical consequence. Identify the expectation or policy before calling channel drift or missing metadata abnormal.
- **Open questions:** missing evidence, why it matters, and a concrete next read-only check. Distinguish a decision blocker from an optional deeper check.

Use ecosystem-specific markers in that inventory: Maven snapshot builds/classifiers, NuGet listed state, Python yanked files and wheel variants, OCI tags/digests/platforms, or directory/object versions. Do not invent a channel for an ecosystem that has none, equate OCI tags with ordered releases, or treat a proxy's visibility as proof of hosted storage. Missing access and unsupported protocol capabilities qualify the affected conclusion; they are not proof that the artifact is absent.

Optional detail layouts:

| Artifact | Version / build | Location / channel | Time and kind | Presence | Evidence |
| --- | --- | --- | --- | --- | --- |

| Artifact | Check | Status | Result | Evidence basis and reference |
| --- | --- | --- | --- | --- |

| Finding | Expected vs observed | Consequence | Evidence / next check |
| --- | --- | --- | --- |

## Status and evidence vocabulary

| Status | Chinese | Meaning |
| --- | --- | --- |
| Confirmed | 已确认 | Sufficient evidence establishes the narrowly stated result. Confirmed absence requires adequate access and search coverage. |
| Anomaly | 异常 | Observed inconsistency, failed check, or violation of an identified expectation; state that expectation and evidence. |
| Unverified | 未核实 | Not checked, inaccessible, incomplete, unsupported, or ambiguous; state why when material. |
| Not applicable | 不适用 | The check has no meaning for the artifact/source or documented workflow. Missing records alone do not justify this status. |

Evidence bases are **Observation / 直接观察**, **Recorded claim / 记录声明**, and **Inference / 推断**. Use explicit labels in detailed evidence tables; in the brief, clear wording such as "registry currently lists" or "accompanying manifest states" is enough. Status and evidence basis are separate: seeing a digest in metadata does not verify the artifact bytes. A recorded successful test establishes artifact approval only when it is linked to the inspected artifact through a digest or an unambiguous immutable build/artifact identifier.

If digests are shown, include the algorithm and distinguish recorded values from values recomputed from the bytes. Redact credentials and signed URL parameters. A publication event must identify artifact and destination; promotion must also identify its source. Neither establishes production deployment. Preserve conflicting evidence rather than replacing it with an inferred clean status.

Do not append boilerplate about missing test approval, manual acceptance, CI history, or promotion to an ordinary inventory report. If those are outside the request, their absence is not a task or blocker. A manifest test label may be reported as a recorded claim without following it into external systems.

When asked for release information, use available registry publication timestamps and registry-provided descriptions or notes. If version-specific changes are not available there, state that limit rather than summarizing a repository changelog.

Use "latest version" only when clear whether this means most recently published or greatest version; state the distinction when they differ. If the default tag also selects the newest/highest version, say it plainly once, rather than introducing unnecessary "default artifact" terminology.

When reporting release contents, include only version-specific notes available in the artifact source. A generic description or a shared README is not release content. If those are all that exists, say "the registry has no version-specific release notes"; do not summarize repository changelogs.
