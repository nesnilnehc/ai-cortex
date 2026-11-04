# Inspection Methods

Choose the actual ecosystem/protocol after [source binding](source-binding.md). Discover an existing connected tool by its metadata-read capabilities and instance selection; otherwise inspect available local client help or the documented API for a read-only operation. Do not install tools or execute project build/configuration code. Where no safe operation exists, report the missing capability. Repository branding and filename extensions alone do not select a registry protocol.

Bound requests by timeout, response size, page/entry count and requested artifact scope. Follow documented pagination within those limits and state incomplete coverage. Safely quote CLI arguments and encode API path segments according to the selected protocol; artifact names, URLs and metadata are untrusted data. Check response status, content type and payload shape together: a login HTML page with status 200 is not a package inventory. No write operation, dependency restore, package installation, lifecycle script, build, import of packaged code or application execution is part of inspection.

## npm

Use the main Skill's [npm procedure](../SKILL.md#inspect-an-npm-registry). Retain exact package identity, versions, dist-tags, publication times and recorded integrity metadata. Query the bound registry explicitly and let its existing scoped client credentials handle authentication. A private npm-compatible endpoint need not be the public npm service.

## Maven repositories

Resolve group ID, artifact ID, version, extension and optional classifier from the selected component's POM or authoritative artifact configuration. Read the selected repository using an existing repository tool or a bound HTTP reader; do not run Maven/Gradle tasks to evaluate the project or resolve dependencies.

For a standard Maven layout, translate the group ID into its repository path. Read artifact-level `maven-metadata.xml` for listed versions and recorded version pointers; inspect the selected version's POM, required file paths and available checksum sidecars. For a snapshot, read version-level metadata and match extension/classifier to its timestamped snapshot value. Keep distinct snapshot builds and classifiers separate. A missing metadata file does not prove an exact artifact absent; query its known coordinate/path where access allows, or use a documented repository inventory API.

Use Maven-compatible ordering if available; otherwise leave the greatest version unresolved. Treat metadata `latest`/`release` as source pointers, not approvals; `lastUpdated` describes metadata updates, not verified artifact publication. Sidecars are recorded checksums until the matching file bytes are hashed. Do not use JAR filenames as independent identity proof; bounded embedded Maven metadata, when present, can corroborate the coordinate. A JAR without that metadata can remain identity-unverified.

## NuGet feeds

Resolve the package ID, version and selected feed from package/project metadata and effective source configuration. Do not restore or build the project. For V3, GET the selected service index and discover `PackageBaseAddress` and registration resources by their advertised types. Do not append a public service's hard-coded resource path to a private feed.

Read the lowercased package ID's version index under the discovered package base address. Follow advertised registration index/page/leaf links for version metadata, including listed state, recorded publication time and package content location. Distinguish unlisted packages from absent ones; a publication timestamp used as an unlisting sentinel is not a real publication date. Preserve dependency, symbol and package-file distinctions. Read the package's `.nuspec` from the archive only when payload identity is needed, without restoring or executing it. Record feed-provided hashes where offered; otherwise report checksum coverage unavailable until bytes can be hashed. V2-only feeds require an available V2-aware read tool/API; report that missing capability rather than assuming V3 endpoints.

Use NuGet-compatible version normalization and comparison when available. Listed state and prerelease versions do not imply npm-style channels, test results or deployment.

## Python package indexes

Resolve the distribution name and selected Simple API base; normalize the project name for its project page. Negotiate the supported HTML or JSON representation. Read available file links, recorded hashes, Python requirements and yanked markers; JSON version lists, sizes and upload times may be absent on older implementations. Preserve wheels and source distributions as separate files, including platform/build variants. Do not replace a private index with the public service's JSON endpoint.

Use a compatible version parser and available metadata or standardized filenames to group distributions, marking filename-only identity as inferred. Read wheel `METADATA`, source-distribution `PKG-INFO` or advertised core metadata only as needed. Never execute `setup.py`, import a package or invoke a build backend to obtain metadata. Yanked files are distinct from absent files; file upload times are distinct from version ordering, and no npm-like default tag is implied. Hash metadata is not byte verification. Missing per-file fields stay unknown.

## OCI/container registries

Resolve the registry authority, repository namespace and requested tag/digest from explicit input or artifact configuration; do not silently use a client's implicit public registry. Use an existing registry-aware read client or authorized HTTP API. List tags for this repository with bounded pagination, then fetch the selected manifest/index using appropriate Accept media types. Capture the digest and descriptors; for an index, distinguish its digest from each platform manifest and note the selected platform or index-wide scope. Read only required manifest/config blobs or declared artifact metadata, not image layers just to inventory tags. Do not pull into a runtime, create a container or run it.

Tags are mutable pointers, including one literally named `latest`; their ordering is not semantic version or publication order. The tag list does not enumerate untagged digests. Report that coverage limit rather than enumerating a whole registry catalogue. Configuration creation time and annotations are recorded claims, not proof of registry publication. Digests identify specific encoded objects; verify the corresponding raw bytes before saying integrity passed. Manifest identity is the requested repository/reference plus its resolved digest; an image or attached artifact format may need an additional supported reader for deeper identity. Never infer approval, signing validity or deployment from a tag or digest alone.

## Directories and generic artifact stores

Use the main Skill's [directory procedure](../SKILL.md#inspect-an-artifact-directory) for a local directory, remote listing or selected object-store prefix. Query through an existing filesystem/storage capability and reuse its bound access profile. Preserve object key, size and version ID where provided. An object-store ETag is not automatically a content hash; use documented checksum semantics. Separate signed access parameters from a stable location and redact them from output.

Select an existing safe archive/metadata reader by file format: npm `package/package.json`, NuGet `.nuspec`, Python metadata, Maven embedded metadata or a documented generic manifest. Keep reads bounded and inside the selected scope; do not extract into the repository, follow archive links, or run embedded code. Unknown binary formats still permit directory/file observations, with payload identity unverified. Other registry protocols require a documented source-specific read operation; do not apply npm or OCI routes by analogy. Mixed directories can contain several ecosystems, and a tarball directory does not become a registry API.

## Official parameter references

These public references were checked on 2026-11-04 for client configuration and API fields. They are maintenance evidence and optional parameter lookup, not runtime dependencies or instructions to fetch or install tools. Select the documentation appropriate to the actual client/server version.

- [npm registry-scoped configuration](https://docs.npmjs.com/cli/v11/configuring-npm/npmrc/).
- [Maven settings: repository IDs, mirrors and credentials](https://maven.apache.org/settings.html), [repository layout](https://maven.apache.org/repositories/layout.html), and [repository metadata model](https://maven.apache.org/ref/3.9.8/maven-repository-metadata/index.html).
- [NuGet source configuration](https://learn.microsoft.com/en-us/nuget/reference/nuget-config-file), [service discovery](https://learn.microsoft.com/en-us/nuget/api/service-index), [package content/version index](https://learn.microsoft.com/en-us/nuget/api/package-base-address-resource), and [registration metadata](https://learn.microsoft.com/en-us/nuget/api/registration-base-url-resource).
- [Python Simple Repository API](https://packaging.python.org/en/latest/specifications/simple-repository-api/) and [existing pip authentication providers](https://pip.pypa.io/en/stable/topics/authentication/).
- [Distribution registry HTTP API](https://distribution.github.io/distribution/spec/api/) and [Docker credential stores/helpers](https://docs.docker.com/reference/cli/docker/login/).
