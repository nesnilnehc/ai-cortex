---
artifact_type: rule
name: diagram-selection
version: 1.0.0
created_by: ai-cortex
lifecycle: living
created_at: 2026-06-24
recommended_scope: user
status: active
---

# Rule: Diagram Selection

> Criteria for drawing a technical diagram: judge the kind of relationship first to pick the diagram, then pick the tool, then steer clear of the rendering traps and split into several diagrams where needed.
>
> **Position**: this rule governs **judgement** — which diagram, which tool, will it render, does it need splitting. It does not govern **shape** (which diagram a design document must contain belongs to [specs/functional-design-modeling.md](../specs/functional-design-modeling.md) and [specs/technical-design-modeling.md](../specs/technical-design-modeling.md)), and it does not teach syntax (PlantUML, Mermaid and Graphviz syntax is general knowledge).
>
> **When it applies**: any act of drawing — a flowchart or state diagram embedded in a design document, or a one-off diagram — defers to these criteria.

---

## 1. Scope

Any situation where a technical diagram is produced with a text-based drawing tool (PlantUML, Mermaid, Graphviz, flowchart.js). The focus is selection and renderability; the correctness of the diagram's business content is out of scope.

---

## 2. Step one: pick the diagram by the kind of relationship

A good diagram answers one main question. Decide **which kind of relationship you are expressing** first, then pick the diagram type — do not make one diagram carry several explanatory jobs at once.

| Relationship to express | Diagram type | First-choice tool |
| :--- | :--- | :--- |
| Sequence — how it happens, step by step | Flowchart, activity diagram, user journey | Mermaid, PlantUML |
| Interaction — who talks to whom, in what order | Sequence diagram | PlantUML, Mermaid |
| State — what states an object has, and how it moves | State diagram | PlantUML, Mermaid |
| Structure — what parts the system is made of | C4, component diagram, class diagram, ER diagram | PlantUML, Mermaid |
| Deployment and network | Deployment diagram, topology, dependency graph | PlantUML, Graphviz |
| Schedule | Gantt chart, timeline | Mermaid, PlantUML |
| Decomposition — a task or knowledge hierarchy | WBS, mind map, tree | PlantUML, Mermaid |
| Complex relationships — many nodes, many edges | Directed graph, undirected graph, knowledge graph | Graphviz |
| Quantities — volume, flow, proportion | Sankey, XY chart, radar, treemap | Mermaid |

Tune the abstraction level to the reader: for the business side, fewer nodes and less jargon (flowchart, user journey, timeline); for engineers, keep service names, interface names, state names and exception branches (C4, component, sequence, state); for operations, emphasise where things are deployed, what depends on what, and the call chain (topology, deployment, dependency graph).

---

## 3. Step two: heuristics for choosing across tools

Default to Mermaid, and leave it only when a row of the table below applies. Do not choose on "can it draw this?" — choose on renderability and long-term maintenance.

| Condition | Choice |
| :--- | :--- |
| Embedded in a document, quick to pick up, README / blog / knowledge base / lightweight plan | **Mermaid** (default) |
| Formal engineering modelling: UML / C4 / deployment / activity, going into a design document | **PlantUML** |
| Many nodes and edges, needing automatic layout: dependency graph / call chain / topology / knowledge graph | **Graphviz** |
| Just a simple standard flow rendered in a web page, with no other diagram type needed | **flowchart.js** |

Where the platform has standardised on a documentation tool, check which renderer version it supports first, and pay particular attention to Mermaid's version differences.

Pick the right Graphviz layout engine: `dot` for layered directed graphs, dependency graphs and call chains; `neato` and `fdp` for general networks and undirected graphs; `sfdp` for large graphs; `circo` for circular and cyclic relationships; `twopi` for radial, centre-outward layouts; `osage` for grouped clusters.

---

## 4. Rendering traps checklist

A diagram must render on its target platform. Check before committing:

- [ ] **Quote Mermaid reserved words**: node text containing a reserved word such as `end`, or a special character, is easily swallowed by the parser — quote it consistently
- [ ] **Confirm the platform's Mermaid version**: check which version the target platform supports before embedding, avoiding a failure where newer syntax meets an older renderer
- [ ] **Switch to ELK layout for complex flows**: where lines cross heavily, switch the flowchart or state diagram to ELK layout to reduce crossings
- [ ] **Confirm the PlantUML rendering chain**: PlantUML depends on Java and a renderer, and a pure documentation platform may not be able to render it — confirm the chain before choosing it
- [ ] **Render or validate in CI**: for a diagram that will be maintained long-term, prefer a text DSL the team knows and that CI can render or validate

---

## 5. Constraints on splitting into several diagrams

- One diagram answers one core question. When it no longer fits legibly on one screen, stop adjusting the styling and **split it**
- A common split: business flowchart + C4 or component diagram + sequence diagram + deployment diagram, each standing alone
- Name a diagram after its conclusion, not its type — "Order state transitions" beats "State diagram"
- Name nodes after stable business concepts or system boundaries, not after a transient code variable
- For a plain field list, interface parameters or a simple comparison, use a table rather than a diagram. A diagram earns its place only when relationships, sequence, hierarchy, dependency, state transitions or quantity flows are the point

---

## Anti-patterns

- ❌ Reaching for Mermaid reflexively without judging the kind of relationship
- ❌ One diagram answering several questions
- ❌ Forcing a large diagram to fit by styling instead of splitting it
- ❌ Naming a diagram after its type rather than its conclusion
- ❌ Using a diagram for a simple list or comparison instead of a table
- ❌ Embedding without confirming the platform's Mermaid version, so it fails to render
- ❌ Naming nodes after transient variables, so the diagram drifts with the code and loses long-term readability

---

## Related assets

- **Design review rules**: [functional-design-quality](./functional-design-quality.md) / [technical-design-quality](./technical-design-quality.md) — embedding a flowchart or state diagram in a design document defers to these criteria
- **Design data contracts**: [specs/functional-design-modeling.md](../specs/functional-design-modeling.md) / [specs/technical-design-modeling.md](../specs/technical-design-modeling.md) — they define which diagram an artifact must contain; this rule complements them, the spec giving the shape and this rule the judgement
- **Chinese writing**: [writing-chinese-technical](./writing-chinese-technical.md)

---

## Change log

### 1.0.0 — 2026-06-24

**Initial Release**: defines the diagram selection criteria — a lookup from relationship kind to diagram type to tool, heuristics for choosing across tools (default Mermaid, and when to leave it), the rendering traps checklist, and constraints on splitting into several diagrams.
