#!/usr/bin/env node
/**
 * Generate skills/skillgraph.md from manifest and SKILL frontmatter.
 * Run from repo root: node scripts/generate-skillgraph.mjs
 * Output: skills/skillgraph.md (auto-generated; do not edit manually)
 */
import { readFileSync, writeFileSync, readdirSync, existsSync } from 'fs';
import { dirname, join } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, '..');
const skillsDir = join(root, 'skills');
const manifestPath = join(root, 'manifest.json');

// Review skill type mapping (convention-based)
const REVIEW_TYPE = {
  scope: ['review-diff', 'review-codebase'],
  language: [
    'review-dotnet', 'review-java', 'review-go', 'review-php', 'review-powershell',
    'review-python', 'review-sql', 'review-typescript',
  ],
  framework: ['review-vue', 'review-react'],
  library: ['review-orm-usage'],
  cognitive: ['review-security', 'review-performance', 'review-architecture', 'review-testing'],
  meta: ['review-code'],
};

const REVIEW_TYPE_LABELS = {
  scope: 'What to review: current change (diff) or current state (paths/repo).',
  language: 'Language and runtime conventions.',
  framework: 'Application framework conventions.',
  library: 'Key library usage and pitfalls.',
  cognitive: 'Cross-cutting concerns: security, performance, architecture, testing.',
  meta: 'Orchestration only; no analysis.',
};

// Non-review chains: skill -> chain label
const NON_REVIEW_CHAIN = {
  lifecycle: [
    'analyze-requirements', 'brainstorm-design', 'commit-work', 'run-automated-tests',
    'run-repair-loop', 'align-planning', 'align-architecture', 'assess-documentation-readiness',
    'orchestrate-governance-loop',
  ],
  onboarding: ['onboard-repo', 'generate-standard-readme', 'write-agents-entry', 'discover-skills'],
  governance: [
    'curate-skills', 'refine-skill-design', 'generate-standard-readme', 'bootstrap-project-documentation',
    'install-rules',
  ],
  standalone: [
    'decontextualize-text', 'generate-github-workflow', 'capture-work-items',
    'validate-document-artifacts', 'discover-document-norms',
  ],
};

// Orchestrator chains (orchestrator -> ordered skills for diagram)
const ORCHESTRATOR_CHAINS = {
  'onboard-repo': ['review-codebase', 'review-architecture', 'generate-standard-readme', 'write-agents-entry', 'discover-skills'],
  'curate-skills': ['refine-skill-design', 'generate-standard-readme'],
  'orchestrate-governance-loop': ['align-planning', 'assess-documentation-readiness', 'align-architecture', 'analyze-requirements', 'brainstorm-design', 'run-repair-loop'],
};

// Fixed composition chains (conceptual, not from single orchestrator)
const LIFECYCLE_CHAIN = ['analyze-requirements', 'brainstorm-design', 'review-code', 'run-repair-loop', 'run-automated-tests', 'commit-work'];
const GOVERNANCE_CHAIN = ['curate-skills', 'refine-skill-design', 'generate-standard-readme', 'bootstrap-project-documentation', 'install-rules'];
const PROJECT_LOOP_CHAIN = ['orchestrate-governance-loop', 'align-planning', 'assess-documentation-readiness', 'align-architecture', 'analyze-requirements', 'brainstorm-design', 'run-repair-loop'];

const manifest = JSON.parse(readFileSync(manifestPath, 'utf8'));
const allSkills = (manifest.capabilities || []).map((c) => c.name);
const reviewAtoms = Object.values(REVIEW_TYPE).flat().filter((s) => s !== 'review-code');
const reviewMeta = 'review-code';

const link = (name) => `[${name}](./${name}/SKILL.md)`;
const mermaidId = (name) => name.replace(/-/g, '_');

function getReviewType(skill) {
  for (const [type, list] of Object.entries(REVIEW_TYPE)) {
    if (list.includes(skill)) return type;
  }
  return null;
}

function buildMermaidReviewDiagram() {
  const lines = [
    'flowchart LR',
    '  subgraph meta [Meta]',
    `    review_code[review-code]`,
    '  end',
    '  subgraph scope [Scope]',
    ...REVIEW_TYPE.scope.map((s) => `    ${mermaidId(s)}[${s}]`),
    '  end',
    '  subgraph lang [Language]',
    ...REVIEW_TYPE.language.map((s) => `    ${mermaidId(s)}[${s}]`),
    '  end',
    '  subgraph fw [Framework]',
    ...REVIEW_TYPE.framework.map((s) => `    ${mermaidId(s)}[${s}]`),
    '  end',
    '  subgraph lib [Library]',
    ...REVIEW_TYPE.library.map((s) => `    ${mermaidId(s)}[${s}]`),
    '  end',
    '  subgraph cognitive [Cognitive]',
    ...REVIEW_TYPE.cognitive.map((s) => `    ${mermaidId(s)}[${s}]`),
    '  end',
  ];
  for (const s of reviewAtoms) {
    lines.push(`  review_code --> ${mermaidId(s)}`);
  }
  for (const s of reviewAtoms) {
    lines.push(`  ${mermaidId(s)} --> aggregate[Aggregate findings]`);
  }
  return lines.join('\n');
}

function buildNonReviewQuickRef() {
  const skillToChain = {};
  for (const [chain, skills] of Object.entries(NON_REVIEW_CHAIN)) {
    for (const s of skills) {
      if (!skillToChain[s]) skillToChain[s] = [];
      if (!skillToChain[s].includes(chain)) skillToChain[s].push(chain);
    }
  }
  const chainLabels = { lifecycle: 'lifecycle', onboarding: 'onboarding', governance: 'governance', standalone: 'standalone' };
  const ioBrief = {
    'analyze-requirements': ['vague intent', 'validated requirements doc'],
    'brainstorm-design': ['validated requirements', 'approved design doc'],
    'commit-work': ['staged changes', 'git commits'],
    'run-automated-tests': ['repo path', 'test execution results'],
    'run-repair-loop': ['repo + scope', 'converged clean state'],
    'align-planning': ['completed task context', 'planning alignment report'],
    'align-architecture': ['ADR/design scope + code scope', 'architecture compliance report'],
    'assess-documentation-readiness': ['docs scope + mapping', 'documentation readiness report + minimal fill plan'],
    'orchestrate-governance-loop': ['trigger + project context', 'cycle governance report'],
    'onboard-repo': ['repo path', 'onboarding report'],
    'curate-skills': ['skills directory', 'ASQM audit report'],
    'refine-skill-design': ['SKILL.md', 'optimized SKILL.md'],
    'generate-standard-readme': ['project context', 'standardized README'],
    'write-agents-entry': ['project context', 'AGENTS.md'],
    'discover-skills': ['capability gaps', 'skill recommendations'],
    'decontextualize-text': ['private text', 'generic text'],
    'generate-github-workflow': ['workflow requirements', 'GitHub Actions YAML'],
    'bootstrap-project-documentation': ['project directory', 'documentation tree'],
    'install-rules': ['source rules', 'IDE rule files'],
    'capture-work-items': ['free-form input', 'structured work item(s)'],
    'validate-document-artifacts': ['docs scope', 'findings list'],
    'discover-document-norms': ['project path', 'docs/ARTIFACT_NORMS.md'],
  };
  const allNonReview = [...new Set(Object.values(NON_REVIEW_CHAIN).flat())];
  const rows = allNonReview.map((s) => {
    const chains = (skillToChain[s] || ['standalone']).join(', ');
    const [input, output] = ioBrief[s] || ['—', '—'];
    return `| ${link(s)} | ${chains} | ${input} | ${output} |`;
  });
  return rows.join('\n');
}

const header = `# Skill Composition Graph

*Auto-generated by \`scripts/generate-skillgraph.mjs\`. Do not edit manually.*

This document describes how skills compose into orchestration chains, governance workflows, and development pipelines. For human and Agent reading only; Skills.sh and the manifest do not depend on it. For the canonical skill list, see [INDEX.md](./INDEX.md) and [manifest.json](../manifest.json). For scenario-first routing, see [scenario-map.md](./scenario-map.md).

---

## 1. Global overview

The skill ecosystem has five major domains:

| Domain | Purpose | Entry skills |
| :--- | :--- | :--- |
| **Code Review** | Aggregate scope, language, framework, library, and cognitive findings | [review-code](./review-code/SKILL.md) |
| **Development Lifecycle** | Requirements → design → implementation → review → commit | [analyze-requirements](./analyze-requirements/SKILL.md), [run-repair-loop](./run-repair-loop/SKILL.md), [commit-work](./commit-work/SKILL.md) |
| **Repository Onboarding** | New team member or inherited repo | [onboard-repo](./onboard-repo/SKILL.md) |
| **Governance & Curation** | Skill inventory, docs, project governance | [curate-skills](./curate-skills/SKILL.md), [orchestrate-governance-loop](./orchestrate-governance-loop/SKILL.md) |
| **Standalone** | Single-skill tasks | [decontextualize-text](./decontextualize-text/SKILL.md), [generate-github-workflow](./generate-github-workflow/SKILL.md), [capture-work-items](./capture-work-items/SKILL.md), etc. |

\`\`\`mermaid
flowchart TB
  subgraph review [Code Review]
    rc[review-code]
  end
  subgraph lifecycle [Development Lifecycle]
    req[analyze-requirements]
    repair[run-repair-loop]
    commit[commit-work]
  end
  subgraph onboarding [Repository Onboarding]
    onboard[onboard-repo]
  end
  subgraph governance [Governance]
    curate[curate-skills]
    loop[orchestrate-governance-loop]
  end
  subgraph standalone [Standalone]
    dectx[decontextualize-text]
    gwf[generate-github-workflow]
  end
\`\`\`

---

## 2. Skill types (Code Review)

Atomic review skills are grouped by dimension:

| Type | Description | Skills |
| :--- | :--- | :--- |
`;

const skillTypesRows = Object.entries(REVIEW_TYPE)
  .filter(([k]) => k !== 'meta')
  .map(([type, list]) => {
    const skills = list.map((s) => link(s)).join(', ');
    return `| **${type.charAt(0).toUpperCase() + type.slice(1)}** | ${REVIEW_TYPE_LABELS[type]} | ${skills} |`;
  })
  .join('\n');

const skillTypesMetaRow = `| **Meta** | ${REVIEW_TYPE_LABELS.meta} | ${link('review-code')} |`;

const executionOrder = `
---

## 3. Execution order

When running a **full** code review (via ${link('review-code')}), the execution order is:

1. **Scope** → choose one: \`review-diff\` (current change) or \`review-codebase\` (given paths/repo).
2. **Language** → choose one or none: ${REVIEW_TYPE.language.join(', ')} (by project).
3. **Framework** → optional: ${REVIEW_TYPE.framework.join(', ')} or future framework skills.
4. **Library** → optional: ${REVIEW_TYPE.library.join(', ')} or future library skills.
5. **Cognitive** → run in order: ${REVIEW_TYPE.cognitive.join(', then ')} (and future: reliability, maintainability).

All findings from the steps above are **aggregated** into a single report (same finding format: Location, Category, Severity, Title, Description, Suggestion).

---

## 4. Composition diagram

\`\`\`mermaid
${buildMermaidReviewDiagram()}
\`\`\`

---

## 5. Finding format (shared)

Every atomic skill emits findings in this format so ${link('review-code')} can merge them:

- **Location**: \`path/to/file.ext\` (optional line or range)
- **Category**: scope | language-* | framework-* | library-* | cognitive-*
- **Severity**: critical | major | minor | suggestion
- **Title**: Short one-line summary
- **Description**: 1–3 sentences
- **Suggestion**: Concrete fix or improvement (optional)

---

## 6. Quick reference (review)

| Skill | Type | Input | Output |
| :--- | :--- | :--- | :--- |
`;

const reviewQuickRefRows = [
  ...REVIEW_TYPE.scope.map((s) => `| ${link(s)} | scope | ${s === 'review-diff' ? 'git diff' : 'paths/dirs/repo'} | Findings (Category=scope) |`),
  ...REVIEW_TYPE.language.map((s) => {
    const suffix = s.replace('review-', '');
    return `| ${link(s)} | language | code scope | Findings (Category=language-${suffix}) |`;
  }),
  ...REVIEW_TYPE.framework.map((s) => {
    const suffix = s.replace('review-', '');
    return `| ${link(s)} | framework | code scope | Findings (Category=framework-${suffix}) |`;
  }),
  ...REVIEW_TYPE.library.map((s) => `| ${link(s)} | library | code scope | Findings (Category=library-orm) |`),
  ...REVIEW_TYPE.cognitive.map((s) => {
    const suffix = s.replace('review-', '');
    return `| ${link(s)} | cognitive | code scope | Findings (Category=cognitive-${suffix}) |`;
  }),
  `| ${link('review-code')} | meta | user intent + scope | Single aggregated report |`,
].join('\n');

const nonReviewSection = `
---

## 7. Non-review composition chains

### 7.1 Development lifecycle chain

Requirements → Design → Implementation → Review → Commit

\`\`\`mermaid
flowchart LR
  analyze[analyze-requirements]
  brainstorm[brainstorm-design]
  review_code_node[review-code]
  commit[commit-work]
  run_tests[run-automated-tests]
  repair[run-repair-loop]

  analyze -->|validated requirements| brainstorm
  brainstorm -->|approved design| review_code_node
  review_code_node -->|findings| repair
  repair --> run_tests
  repair --> review_code_node
  run_tests -->|tests pass| commit
\`\`\`

### 7.2 Repository onboarding chain

The ${link('onboard-repo')} orchestrator runs skills in sequence:

\`\`\`mermaid
flowchart LR
  onboard[onboard-repo]
  rcb[review-codebase]
  rarch[review-architecture]
  readme[generate-standard-readme]
  agents[write-agents-entry]
  discover[discover-skills]

  onboard --> rcb
  rcb --> rarch
  rarch --> readme
  readme --> agents
  agents --> discover
\`\`\`

### 7.3 Governance and curation chain

\`\`\`mermaid
flowchart LR
  curate[curate-skills]
  refine[refine-skill-design]
  readme_gen[generate-standard-readme]
  bootstrap[bootstrap-project-documentation]
  install[install-rules]

  curate -->|ASQM findings| refine
  refine -->|optimized SKILL.md| readme_gen
  bootstrap --> readme_gen
  install -.->|rules for quality| curate
\`\`\`

### 7.4 Project governance loop chain

Unified sequence: align-planning → assess-documentation-readiness; output-driven follow-ups (align-architecture, repair, brainstorm, analyze).

\`\`\`mermaid
flowchart LR
  loop[orchestrate-governance-loop]
  align[align-planning]
  alignarch[align-architecture]
  docreadiness[assess-documentation-readiness]
  req[analyze-requirements]
  design[brainstorm-design]
  repair[run-repair-loop]

  loop --> align
  loop --> docreadiness
  align -->|active defects| repair
  align -->|architecture compliance needed| alignarch
  docreadiness -->|doc gaps| req
  docreadiness -->|architecture gap| design
\`\`\`

### 7.5 Quick reference (non-review)

| Skill | Chain | Input | Output |
| :--- | :--- | :--- | :--- |
${buildNonReviewQuickRef()}
`;

const fullDoc =
  header +
  skillTypesRows +
  '\n' +
  skillTypesMetaRow +
  executionOrder +
  reviewQuickRefRows +
  nonReviewSection;

const outPath = join(skillsDir, 'skillgraph.md');
writeFileSync(outPath, fullDoc, 'utf8');
console.log(`Written ${outPath}`);
