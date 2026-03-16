# design-solution

Transform rough ideas into validated, production-grade designs through structured dialogue.

## Overview

This skill synthesizes best practices from 7 top-ranked skills on skills.sh (combined 650K+ installs) to help turn vague ideas into concrete, approved designs before implementation. It prevents premature coding by systematically exploring context, clarifying requirements, proposing alternatives, and validating designs incrementally.

## Key Features

- **Structured dialogue**: One question at a time, building understanding incrementally (from obra/superpowers brainstorming)
- **Phase-based validation**: Systematic process with clear checkpoints (from obra/superpowers systematic-debugging)
- **YAGNI & DRY principles**: Focus on minimum viable solution, reference existing patterns (from obra/superpowers writing-plans)
- **Production-grade quality**: Apply domain-specific best practices during design (from anthropics/vercel-labs skills)
- **Trade-off analysis**: Propose 2-3 approaches with clear pros/cons/best-for (from multiple sources)
- **HARD-GATE pattern**: Explicit prevention of premature implementation (from obra/superpowers)
- **Incremental documentation**: Scale design detail to project complexity (from multiple sources)

## Synthesized From

This skill integrates methodologies from these top-ranked skills:

1. **brainstorming** (obra/superpowers) - #40, 35.8K installs: Structured dialogue, HARD-GATE pattern
2. **writing-plans** (obra/superpowers) - #53, 17.9K installs: YAGNI, DRY, bite-sized granularity
3. **systematic-debugging** (obra/superpowers) - #49, 19.7K installs: Phase-based process, root cause methodology
4. **frontend-design** (anthropics/skills) - #5, 112.3K installs: Production-grade quality focus
5. **web-design-guidelines** (vercel-labs) - #3, 138.9K installs: Compliance checking pattern
6. **vercel-react-best-practices** (vercel-labs) - #2, 180.5K installs: Best practices encapsulation
7. **skill-creator** (anthropics/skills) - #34, 55.3K installs: Structured creation workflow

## When to Use

- Planning new features or functionality
- Making architecture decisions with trade-offs
- Clarifying vague or incomplete requirements
- Validating design approaches before development
- Applying domain-specific best practices during design phase

## Process

1. **Explore Context**: Review project state, constraints, existing patterns, applicable best practices
2. **Clarify Through Dialogue**: Ask focused questions one at a time, prefer structured questions
3. **Explore Alternatives**: Propose 2-3 approaches with trade-offs, lead with recommendation
4. **Present Design**: Show design incrementally (scaled to complexity), validate each section
5. **Document**: Write and commit validated design document with trade-offs analysis

## Core Principles

- **HARD-GATE**: No implementation before design approval (applies to ALL projects)
- **YAGNI**: You Aren't Gonna Need It - ruthlessly remove unnecessary features
- **DRY**: Don't Repeat Yourself - reference existing patterns
- **One question at a time**: Build understanding incrementally
- **Trade-off transparency**: Document alternatives considered and reasoning

## Installation

```bash
npx skills add nesnilnehc/ai-cortex --skill design-solution
```

## Related Skills

- `refine-skill-design`: Audit and improve skill definitions
- `generate-standard-readme`: Create standardized project documentation
- `bootstrap-docs`: Initialize project documentation structure

## License

MIT
