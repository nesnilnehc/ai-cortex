---
artifact_type: reference
created_by: ai-cortex
lifecycle: living
created_at: 2026-03-24
status: active
---

# README diagram standards

**Version**: 1.0.0
**Purpose**: set the standard for visual communication in the project README, so it stays clear, maintainable and accessible.

---

## 1. Core principles

1. **Semantic-first**: a diagram must convey meaning — logic, flow, structure — and never be mere decoration.
1. **Native rendering**: prefer a code-based diagram (Mermaid) over a binary image (PNG/SVG), which keeps it under version control and searchable.
1. **Minimalism**: one diagram answers one question — "what is this?", "how does it work?", "what is inside?".
1. **Accessibility**: every diagram must carry accompanying text, or explain itself through its labels.

---

## 2. Diagram types and what each is for

| Type | Purpose | The question it answers | Recommended format |
| :--- | :--- | :--- | :--- |
| **Concept diagram** | High-level architecture, the entities and their relationships | "What system is this?" | Mermaid flowchart (LR/TB) |
| **Workflow diagram** | A dynamic process, a user interaction, a data flow | "How do I use it?" | Mermaid sequence or flowchart |
| **Ecosystem / topology diagram** | The catalogue of components, how they group, and the scale | "What capabilities are there?" | Mermaid graph (TB) or mindmap |

---

## 3. Technical standards

### 3.1 Format, in order of preference

1. **Mermaid, embedded from `.mmd`**: the first choice. GitHub renders it natively. *Upside*: editable, diffable, and it adapts to the light or dark theme. *Downside*: limited control over styling.
1. **SVG, vector**: the second choice, for complex branding or an unconventional layout. *Requirement*: the source file — `.drawio`, `.excalidraw` or similar — must be kept in `docs/designs/`.
1. **PNG/JPG, bitmap**: avoid for diagrams; use only for a screenshot or a photograph.

### 3.2 Mermaid style guide

- **Direction**:
  - `LR`, left to right, for a process or a timeline.
  - `TB`, top to bottom, for a hierarchy or an ecosystem diagram.
- **Nodes**: keep labels short and clear; avoid long blocks of text.
- **Classes**: prefer a semantic class name (`classDef user`, `classDef system`) over a hard-coded colour, so the diagram can be themed later.

### 3.3 Complexity limits

- **Maximum node count**: about 15 per diagram. Beyond that, split into subgraphs or raise the level of abstraction.
- **Depth**: at most 3 levels of nested subgraphs.

---

## 4. The standard diagram set for a README

The README of a professional infrastructure project should carry:

1. **A "concept" diagram, as the banner or introduction**: a simple input-process-output model. *Goal*: the reader grasps the value proposition within 5 seconds.
1. **A "flow" diagram, for usage**: the typical path a user takes. *Goal*: the reader understands how it runs.
1. **An "ecosystem" diagram, for the feature catalogue**: the capabilities at a glance. *Goal*: the reader sees the breadth of the tool.

---

## 5. Maintenance

- A diagram is code. It must be updated in the same PR as the change it describes.
- An out-of-date diagram must be deleted or archived.
- `docs/images/*.mmd` is the canonical source for the Mermaid blocks in the README. Keep the README and the source files in step.
- Before committing, compare `docs/images/*.mmd` against the Mermaid blocks in the README, so the two do not drift apart.
