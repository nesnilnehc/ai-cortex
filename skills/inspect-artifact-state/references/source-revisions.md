# Source Revision Evidence

Collect artifact-provided source identifiers so another workflow can decide whether they are usable inputs to version comparison. This inspection does not choose a release baseline, resolve Git history or determine release membership. The source must remain the selected registry, directory, accompanying metadata or inspected payload; source checkout configuration may locate an artifact but cannot establish which commit produced it.

## Collect within the requested scope

Start with the exact artifact/version/build already being inspected. Read any source repository/revision fields in its metadata and small accompanying source records. Keep metadata-read attempts in ordinary inventory; deeper payload/attestation reads are warranted when the user needs a source association for comparison or a material discrepancy needs explaining. Respect existing access, size, pagination and archive limits. If a required reader, record or permission is missing, state the limitation instead of installing tools, running package code or querying CI.

| Artifact/source | Source identifiers to inspect when exposed |
| --- | --- |
| npm | Query `gitHead` and `repository` for the exact package version alongside its dist digest. Preserve a repository object, URL and directory where provided. Some registries omit these fields. A homepage/shared README or a repository URL alone does not bind a commit to this artifact. |
| Maven | Inspect the selected artifact's published POM `scm` data and any documented accompanying build/source record or embedded revision metadata. SCM connection/URL locates source; `scm.tag` can be a tag or `HEAD`, not a full commit. Keep it as a recorded ref and leave the full commit unresolved rather than following it into Git. |
| NuGet | Read the selected package's `.nuspec` repository `url`, `commit`, `branch` and type when accessible, or corresponding version-specific source metadata exposed by the feed. An ordinary source URL is not a commit; absent optional attributes remain unavailable. Do not restore packages or run a build to generate missing metadata. |
| Python | Inspect advertised core metadata or requested wheel/sdist metadata and accompanying source/build records. Project URLs may locate a repository without pinning a commit. Preserve an explicitly recorded revision and its association with the specific file; do not invent a universal commit field, execute `setup.py` or import the distribution. |
| OCI | Look for `org.opencontainers.image.source` and `org.opencontainers.image.revision` in the selected index/manifest annotations or image config labels where supplied. Record the exact object/digest and platform carrying each claim. Do not confuse a base image's revision with the produced artifact's source or apply one platform's claim to every image. |
| Directory/object store | Inspect accompanying manifests, per-artifact source records and supported embedded metadata. Keep the build identifier and the actual file/object version or digest in the association. A nearby file with a SHA is not necessarily about the selected artifact. |

For linked attestations or other source records, stay within authorized artifact-source scope and the established destination/access binding. Do not follow an arbitrary source URL into a repository or external build service. Never copy credentials or signed access parameters into retained evidence.

## Retain the association, not just a SHA

Keep the artifact name/version and immutable build, object version or digest with its algorithm where supplied; the recorded source repository; the full commit value when supplied; the component/directory or platform/build scope when supplied; and the evidence location, field and observation time. Missing values remain explicit gaps for a comparison handoff. Artifact digest and Git commit identify different objects and must have distinct names.

Preserve source-provided non-secret values faithfully. Mark an abbreviated hash as abbreviated; do not expand it from the local checkout. A branch, tag, `HEAD`, build number or version string is not a full commit hash. Hash-looking text alone does not establish its algorithm, repository, existence or build relationship. Do not invent missing repository, component or clean-worktree status from local package metadata. If the artifact lists multiple source repositories or components, retain them separately; never collapse them into one arbitrary commit.

Retain registry-versus-payload or platform-versus-platform conflicts without silently picking a winner. Different digests for one version need separate observations. A shared description/source URL may help locate source but cannot supply a version-specific revision. A digest match links the bytes to a checksum record; it does not prove that the bytes were built from the recorded commit.

## Explain confidence and gaps

- **Recorded claim:** the registry, manifest, label, POM or package metadata states a repository/revision. Reading that field confirms the statement exists, not that the build used that source unchanged. This is the default classification for self-reported source metadata.
- **Verified provenance binding:** use this wording only if an available trusted verification method actually validates the provenance record, its issuer/signature under an established trust policy, and its subject against the inspected artifact's digest, with the stated source revision included. Describe the verified scope and remaining limits. A signed but untrusted record, matching version string or digest check alone is insufficient. This does not imply an independently reproduced build or a complete dependency inventory.
- **Unavailable, partial or conflicting:** distinguish a missing source field from inaccessible/unread metadata, a source URL without a full commit, a short/mutable revision, and competing claims. Missing source information does not make the artifact absent or defective unless a documented requirement demands it.

When these details matter for a later comparison, identify the precise uncertainty. For example, say that package metadata records a full commit but its association with the build has not been independently verified, or that the artifact source provides no full source commit and therefore cannot supply that comparison endpoint. Preserve useful partial evidence instead of replacing it with an inferred clean result.

## Handoff boundary

The caller must separately decide which artifact is the intended baseline and which source revision is the target. Greatest version, a channel named `latest`, and actual deployment are distinct selections. Even a trusted source association supplies only a possible endpoint: downstream work must check repository identity, graph relationships, component scope, and relevant source changes before deriving a release range. Cherry-picks, reverts, divergent history, multiple source inputs and unrecorded build changes prevent a lone SHA from defining business release contents. Do not perform that analysis here.

Official field/parameter references: [npm metadata field queries](https://docs.npmjs.com/cli/v11/commands/npm-view/), [Maven SCM fields](https://maven.apache.org/pom.html#SCM), [NuGet repository attributes](https://learn.microsoft.com/en-us/nuget/reference/nuspec#repository), and [OCI source/revision annotations](https://github.com/opencontainers/image-spec/blob/main/annotations.md). These are lookup references, not runtime dependencies or instructions to fetch source history.
