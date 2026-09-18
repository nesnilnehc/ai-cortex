---
artifact_type: rule
name: doc-health-criteria
version: 2.0.0
scope: assessing or self-checking document health (run by the runtime, a linter or CI)
recommended_scope: user
status: active
---

# Rule: Document Health Criteria

> Hard constraints on what makes the project's documentation "healthy". A runtime (AgentFabric, a linter, CI, or a person) performs the detection against this rule; the rule does not prescribe how to detect.
>
> Paired with the specs (requirement-modeling / functional-design-modeling / technical-design-modeling / task-modeling / universal-notification): a spec defines what an object looks like, this rule defines what a healthy graph between objects looks like.

---

## 1. Specification compliance

For each document:

- [ ] The file path matches the `path_pattern` for its `artifact_type` in `docs/ARTIFACT_NORMS.md`
- [ ] The filename follows the naming convention (kebab-case; timestamp prefixes only for the types that allow them)
- [ ] Frontmatter carries the required fields (artifact_type / lifecycle / created_at, plus any extensions the type defines)
- [ ] Frontmatter values are within their enums (artifact_type / lifecycle / status)

---

## 2. Link graph health

For the repository-wide Markdown link graph.

An **entry document** is one a reader reaches without following a link: the README, any INDEX.md, and any other root-level document the project designates as one. Both criteria below that speak of reachability use this same set; measuring one of them from the README alone and the other from a wider set makes them disagree about the same graph.

- [ ] **No broken links**: every relative link resolves to an existing file or anchor
- [ ] **No orphaned documents**: every document is reachable by link from an entry document. A tombstone is exempt — a document kept only so that a link arriving from outside still lands somewhere, and which says on its face that nothing inside links to it any more
- [ ] **Every deferral resolves**: where a document sends the reader elsewhere for a definition, following that chain arrives at the definition. Mutual links are not a defect, and neither is an index linking its members while they link back — those are how a graph is navigated, and a project whose documents cross-reference each other well will have many. What this forbids is following "the answer is over there" from document to document and arriving back where you started with nothing. It is a judgement about content, not a computation on edges: a cycle detector answers a different question and must not be run in its place
- [ ] **Chain length ≤ 4**: the shortest path from an entry document to any document is at most 4 hops
- [ ] **External URLs** are format-checked only — no HEAD requests

---

## 3. SSOT integrity

For documents that overlap semantically:

- [ ] **One canonical source**: a concept, a field or a metric has exactly one authoritative definition in the repository
- [ ] **Restatements stay in sync**: when one document refers to another, it links rather than copies the content
- [ ] **No contradictory definitions**: two documents describing the same thing must not give conflicting values — version numbers, dates, field definitions
- [ ] **Clear layering of intent**: path_layer / artifact_type / ownership / granularity do not overlap

---

## 4. Code and documentation alignment

For a code diff on a PR or branch:

- [ ] **New capability** has a matching README or ARCHITECTURE update
- [ ] **API change** has documentation synchronised — signature, fields, behaviour
- [ ] **Deprecation or removal** is explicitly noted in the CHANGELOG
- [ ] **Code samples** match the current code and do not reference a deleted API

---

## 5. Layer readiness

For the governance document layers (mission / vision / goals / roadmap / requirements / designs / tasks):

- [ ] **No layer runs ahead of the one above it**: requirements must trace to a roadmap node; designs must trace to a requirement; tasks must trace to a design
- [ ] **The frontmatter `parent` field** points at the correct upstream
- [ ] **The `parent` chain terminates**: following `parent` upward from any document reaches a root in a finite number of steps — no document is its own ancestor
- [ ] **Completion is computed bottom-up**: when all children are done, the parent counts as done

---

## Anti-patterns

- ❌ One field defined and maintained independently in 2 or more documents — an SSOT violation
- ❌ Documentation out of step with the code, such as a README listing a capability that was removed
- ❌ A timestamped filename for an artifact_type that does not allow one, such as a requirement or a spec
- ❌ An orphaned document that nothing links to, and that is not a tombstone saying so
- ❌ A definition that defers to a second document which defers back, so that following it never reaches the definition
- ❌ A `parent` chain that closes on itself, leaving no document in it with an upstream
- ❌ Reporting mutual links, or an index and its members, as a link-graph defect
- ❌ A misplaced parent across layers — a task whose `parent:` points at a requirement rather than a design

---

## Related assets

- Detection — building the link graph, scanning frontmatter, diffing, computing readiness — is carried out by the AgentFabric runtime or by linter and CI tooling; this rule states criteria only
- Suggested tools: lychee for links, markdownlint for formatting, custom scripts for SSOT, alignment and readiness
