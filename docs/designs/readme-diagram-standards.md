# README Diagram Design Standards

**Version:** 1.0.0  
**Purpose:** Establish a standard for visual communication in project READMEs to ensure clarity, maintainability, and accessibility.

---

## 1. Core Principles

1.  **Semantic-First**: Diagrams must convey meaning (logic, flow, structure), not just decoration.
2.  **Native Rendering**: Prefer code-based diagrams (Mermaid) over binary images (PNG/SVG) for version control and searchability.
3.  **Minimalism**: Each diagram should answer exactly one question ("What is this?", "How does it work?", "What's inside?").
4.  **Accessibility**: All diagrams must have accompanying text descriptions or be self-explanatory through labels.

---

## 2. Diagram Types & Usage

| Type | Purpose | Question Answered | Recommended Format |
| :--- | :--- | :--- | :--- |
| **Concept Diagram** | High-level architecture, entities, and relationships. | "What is this system?" | Mermaid Flowchart (LR/TB) |
| **Workflow Diagram** | Dynamic process, user interaction, data flow. | "How do I use it?" | Mermaid Sequence or Flowchart |
| **Ecosystem/Topology** | Component catalog, grouping, and scale. | "What capabilities exist?" | Mermaid Graph (TB) or Mindmap |

---

## 3. Technical Standards

### 3.1 Format Priority

1.  **Mermaid (`.mmd` embedded)**: Primary choice. GitHub renders natively.
    *   *Pros*: Editable, diffable, theme-adaptive (light/dark mode).
    *   *Cons*: Limited styling control.
2.  **SVG (Vector)**: Secondary choice for complex branding or non-standard layouts.
    *   *Requirement*: Must include source file (e.g., `.drawio`, `.excalidraw`) in `docs/designs/`.
3.  **PNG/JPG (Raster)**: Avoid for diagrams; use only for screenshots or photos.

### 3.2 Mermaid Style Guide

*   **Orientation**:
    *   Use `LR` (Left-to-Right) for flows and timelines.
    *   Use `TB` (Top-to-Bottom) for hierarchies and ecosystem maps.
*   **Nodes**: Use clear, concise labels. Avoid long text blocks.
*   **Classes**: Use semantic class names (`classDef user`, `classDef system`) rather than hardcoded colors where possible, to support future theming.

### 3.3 Complexity Limits

*   **Max Nodes**: ~15 per diagram. If more, split into sub-diagrams or use a high-level abstraction.
*   **Max Depth**: 3 levels of nesting (subgraphs).

---

## 4. Standard Diagram Set for README

A professional infrastructure project README should ideally contain:

1.  **The "Concept" (Banner/Intro)**:
    *   A simple input-process-output model.
    *   *Goal*: User understands the value proposition in < 5 seconds.

2.  **The "Flow" (Usage)**:
    *   A typical user interaction path.
    *   *Goal*: User understands the mechanism of action.

3.  **The "Ecosystem" (Features/Catalog)**:
    *   A map of available capabilities.
    *   *Goal*: User sees the breadth of the tool.

---

## 5. Maintenance

*   Diagrams are code. They must be updated in the same PR as the feature changes they depict.
*   Obsolete diagrams must be removed or archived.
*   `docs/images/*.mmd` is the source of truth for README Mermaid blocks. Keep README and source files synchronized.
*   Run `npm run verify:diagram-sync` before commit to prevent drift.
