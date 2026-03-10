# ADR 001: I/O Contract Protocol for Skill Chaining

**Status:** Accepted  
**Date:** 2026-03-06  
**Context:** spec/skill.md v2.1.0, roadmap Layer C (Orchestration & Composition)

## Context

Skills produce outputs (findings, reports, documents) that may feed into other skills or orchestrators. Without a standard way to describe input and output types, orchestrators and skill chains must rely on implicit knowledge to match upstream outputs to downstream inputs.

## Decision

Adopt optional `input_schema` and `output_schema` in spec/skill.md YAML frontmatter. Artifact types include: `findings-list`, `document-artifact`, `diagnostic-report`, `code-scope`, `free-form`.

Orchestrators use these schemas to:

1. Auto-match upstream output type to downstream input type
2. Validate handoff compatibility before execution
3. Document data flow without reading each skill's prose

## Consequences

- **Positive**: Orchestrators (run-checkpoint, review-code, onboard-repo) can route by type; new skills declare I/O for discoverability
- **Negative**: Additional metadata to maintain; schema granularity may need refinement over time
- **Neutral**: Optional — skills without I/O schema remain valid; backward compatible

## References

- spec/skill.md § I/O contracts
- [Evolution Roadmap](../designs/2026-03-02-ai-cortex-evolution-roadmap.md) C8 Skill Chain & Workflow Protocol
