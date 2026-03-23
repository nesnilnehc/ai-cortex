#!/usr/bin/env node
/**
 * Verify every SKILL.md under skills/ conforms to spec/skill.md.
 *
 * Checks:
 *   1. YAML metadata completeness and format
 *   2. Required heading structure
 *   3. Core Objective sub-sections (Primary Goal, Success Criteria, Acceptance Test)
 *   4. Success Criteria count (3-6 items)
 *   5. Name matches directory name
 *   6. Name format (1-64 chars, kebab-case, no consecutive hyphens)
 *   7. Self-Check section present
 *   8. At least 2 examples
 *   9. agent.yaml and README.md existence (warning)
 *  10. (removed) related_skills — skill relations documented in Handoff/Scope Boundaries prose
 *  11. evolution.sources: if present, each source has required fields and MIT-compatible license
 *
 * Run from repo root: node scripts/verify-skill-structure.mjs
 */
import { readFileSync, readdirSync, existsSync } from 'fs';
import { dirname, join } from 'path';
import { fileURLToPath } from 'url';
import { parseSkillFrontmatter } from './lib/parse-skill-frontmatter.mjs';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, '..');
const skillsDir = join(root, 'skills');

const REQUIRED_YAML_FIELDS = ['name', 'description', 'tags', 'version', 'license'];

const REQUIRED_HEADINGS = [
  'Purpose',
  'Core Objective',
  'Use Cases',
  'Behavior',
  'Input & Output',
  'Restrictions',
  'Self-Check',
  'Examples',
];

/** Spec §3: English and Chinese equivalents; used to match bilingual headings like ## 目的 (Purpose). */
const REQUIRED_HEADING_ALIASES = {
  'Purpose': ['目的'],
  'Core Objective': ['核心目标'],
  'Use Cases': ['使用场景', '用例'],
  'Behavior': ['行为'],
  'Input & Output': ['输入与输出', '输入&输出'],
  'Restrictions': ['限制'],
  'Self-Check': ['自检'],
  'Examples': ['示例'],
};

const CORE_OBJECTIVE_SUBSECTIONS = [
  'Primary Goal',
  'Success Criteria',
  'Acceptance Test',
];

const NAME_REGEX = /^[a-z0-9]([a-z0-9-]*[a-z0-9])?$/;
const SEMVER_REGEX = /^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(-[\w.]+)?(\+[\w.]+)?$/;

const ALLOWED_SOURCE_LICENSES = ['MIT', 'Apache-2.0', 'BSD-3-Clause', 'BSD-2-Clause'];
const REQUIRED_SOURCE_FIELDS = ['name', 'repo', 'version', 'license', 'type', 'borrowed'];

let errors = 0;
let warnings = 0;

function error(skill, msg) {
  console.error(`❌ [${skill}] ${msg}`);
  errors++;
}

function warn(skill, msg) {
  console.warn(`⚠️  [${skill}] ${msg}`);
  warnings++;
}

function parseFrontmatter(content) {
  return parseSkillFrontmatter(content);
}

function extractHeadings(content) {
  const body = content.replace(/^---\n[\s\S]*?\n---/, '');
  const headings = [];
  for (const line of body.split('\n')) {
    const m = line.match(/^(#{1,3})\s+(.+)/);
    if (m) headings.push({ level: m[1].length, text: m[2].trim() });
  }
  return headings;
}

/** Matches ## Heading or ## 中文（English） style; returns the section body. */
function findSection(content, englishName, chineseAliases = []) {
  const patterns = [
    new RegExp(`## ${englishName.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}\\b([\\s\\S]*?)(?=\\n## |\\n---\\s*$|$)`, 'i'),
    ...chineseAliases.map((a) => new RegExp(`## ${a.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}[^\\n]*([\\s\\S]*?)(?=\\n## |\\n---\\s*$|$)`, 'i')),
  ];
  for (const re of patterns) {
    const m = content.match(re);
    if (m) return m[1];
  }
  return null;
}

function countSuccessCriteria(content) {
  const section = findSection(content, 'Core Objective', ['核心目标']);
  if (!section) return -1;
  const criteriaLines = section.split('\n').filter((l) => /^\d+\.\s+/.test(l.trim()));
  return criteriaLines.length;
}

function countExamples(content) {
  const section = findSection(content, 'Examples', ['示例']);
  if (!section) return 0;
  const h3Examples = (section.match(/^###\s+/gm) || []).length;
  const boldExamples = (section.match(/^\*\*(Example|Edge case|Before|示例|边界)/gm) || []).length;
  return h3Examples > 0 ? h3Examples : boldExamples;
}

function hasSelfCheckCriteria(content) {
  const section = findSection(content, 'Self-Check', ['自检']);
  if (!section) return false;
  return section.includes('- [ ]');
}

function extractSection(content, heading) {
  const aliases = REQUIRED_HEADING_ALIASES[heading] || [];
  const section = findSection(content, heading, aliases);
  return section !== null ? section : '';
}

/** Extract evolution.sources from YAML frontmatter for validation. */
function extractEvolutionSources(content) {
  const match = content.match(/^---\n([\s\S]*?)\n---/);
  if (!match) return [];
  const yaml = match[1];
  const sources = [];
  let inSources = false;
  let current = null;
  for (const line of yaml.split('\n')) {
    if (line.match(/^\s*sources:\s*$/)) {
      inSources = true;
      continue;
    }
    if (!inSources) continue;
    const listItem = line.match(/^\s+-\s+name:\s*["']?([^"'\n]+)["']?\s*$/);
    if (listItem) {
      if (current) sources.push(current);
      current = { name: listItem[1].trim() };
      continue;
    }
    if (current) {
      const repo = line.match(/^\s+repo:\s*["']?([^"'\n]+)["']?\s*$/);
      const version = line.match(/^\s+version:\s*["']?([^"'\n]+)["']?\s*$/);
      const license = line.match(/^\s+license:\s*["']?([^"'\n]+)["']?\s*$/);
      const type = line.match(/^\s+type:\s*["']?([^"'\n]+)["']?\s*$/);
      const borrowed = line.match(/^\s+borrowed:\s*["']?([^"'\n]+)["']?\s*$/);
      if (repo) current.repo = repo[1].trim();
      if (version) current.version = version[1].trim();
      if (license) current.license = license[1].trim();
      if (type) current.type = type[1].trim();
      if (borrowed) current.borrowed = borrowed[1].trim();
    }
    if (inSources && line.match(/^\s{4}\w+:\s*$/) && !line.trim().startsWith('sources:')) {
      inSources = false;
      if (current) sources.push(current);
      current = null;
    }
  }
  if (current) sources.push(current);
  return sources;
}

function extractSkillBoundariesBlock(restrictionsBlock) {
  if (!restrictionsBlock) return '';
  const markerMatch = restrictionsBlock.match(/### [^\n]*(Skill Boundaries|技能边界)[^\n]*/);
  if (!markerMatch) return '';
  const start = markerMatch.index;
  const after = restrictionsBlock.slice(start);
  const nextSubHeading = after.match(/\n### [\u4e00-\u9fa5A-Z]/);
  const nextH2 = after.match(/\n## /);
  const candidates = [nextSubHeading, nextH2].filter(Boolean).map((m) => m.index);
  const endOffset = candidates.length > 0 ? Math.min(...candidates) : after.length;
  return after.slice(0, endOffset);
}

function checkSkill(dirName) {
  const skillPath = join(skillsDir, dirName, 'SKILL.md');
  if (!existsSync(skillPath)) return;

  const content = readFileSync(skillPath, 'utf8');

  const meta = parseFrontmatter(content);
  if (!meta) {
    error(dirName, 'Missing or malformed YAML front-matter block');
    return;
  }

  for (const field of REQUIRED_YAML_FIELDS) {
    if (!meta[field] || (Array.isArray(meta[field]) && meta[field].length === 0)) {
      error(dirName, `Missing required YAML field: ${field}`);
    }
  }

  if (meta.name && meta.name !== dirName) {
    error(dirName, `YAML name "${meta.name}" does not match directory name "${dirName}"`);
  }

  if (meta.name && !NAME_REGEX.test(meta.name)) {
    error(dirName, `Name "${meta.name}" does not match kebab-case pattern (a-z0-9, hyphens, no start/end/consecutive hyphens)`);
  }

  if (meta.name && meta.name.includes('--')) {
    error(dirName, `Name "${meta.name}" contains consecutive hyphens`);
  }

  if (meta.name && meta.name.length > 64) {
    error(dirName, `Name "${meta.name}" exceeds 64 characters`);
  }

  if (meta.version && !SEMVER_REGEX.test(meta.version)) {
    error(dirName, `Version "${meta.version}" is not valid SemVer`);
  }

  if (meta.license && meta.license !== 'MIT') {
    error(dirName, `License "${meta.license}" should be "MIT"`);
  }

  const headings = extractHeadings(content);
  const h2Texts = headings.filter((h) => h.level === 2).map((h) => h.text);

  function headingMatchesRequired(h2Text, req) {
    const stripParens = (t) => t.replace(/\s*[（(][^）)]*[）)]\s*$/, '').trim();
    const raw = stripParens(h2Text);
    if (h2Text === req || h2Text.startsWith(req + ' ')) return true;
    if (h2Text.includes(`(${req})`) || h2Text.includes(`（${req}）`)) return true;
    const aliases = REQUIRED_HEADING_ALIASES[req] || [];
    if (aliases.some((a) => raw === a || h2Text.includes(`(${a})`) || h2Text.includes(`（${a}）`))) return true;
    return false;
  }

  for (const req of REQUIRED_HEADINGS) {
    if (!h2Texts.some((h) => headingMatchesRequired(h, req))) {
      error(dirName, `Missing required heading: ## ${req}`);
    }
  }

  const CORE_OBJECTIVE_ALIASES = {
    'Primary Goal': ['首要目标', '治理目标', '任务目标', '解决目标', '废水目标'],
    'Success Criteria': ['成功标准'],
    'Acceptance Test': ['验收测试', '验收', '仓库测试'],
  };

  function hasSubsection(pattern, aliases) {
    return [pattern, ...(aliases || [])].some(
      (p) =>
        content.includes(`**${p}**`) ||
        content.includes(`**${p}：`) ||
        content.includes(`**${p}:`)
    );
  }

  if (h2Texts.some((h) => headingMatchesRequired(h, 'Core Objective'))) {
    for (const sub of CORE_OBJECTIVE_SUBSECTIONS) {
      const aliases = CORE_OBJECTIVE_ALIASES[sub] || [];
      const found = hasSubsection(sub, aliases);
      if (!found) {
        error(dirName, `Core Objective missing required subsection: ${sub}`);
      }
    }

    const criteriaCount = countSuccessCriteria(content);
    if (criteriaCount >= 0 && (criteriaCount < 3 || criteriaCount > 6)) {
      error(dirName, `Success Criteria count is ${criteriaCount}; must be 3-6`);
    }
  }

  if (!hasSelfCheckCriteria(content)) {
    error(dirName, 'Self-Check section has no checklist items (expected "- [ ]" items)');
  }

  const exampleCount = countExamples(content);
  if (exampleCount < 2) {
    warn(dirName, `Only ${exampleCount} example(s) found; spec recommends at least 2`);
  }

  // Restrictions / Skill Boundaries (spec §4.2 — mandatory "don't" list)
  const restrictionsBlock = extractSection(content, 'Restrictions');
  const skillBoundariesBlock = extractSkillBoundariesBlock(restrictionsBlock);

  if (!restrictionsBlock) {
    error(dirName, 'Restrictions section missing or malformed');
  } else if (!skillBoundariesBlock) {
    error(dirName, 'Restrictions section missing Skill Boundaries subsection');
  } else if (!/Do NOT do these|不要做这些/i.test(skillBoundariesBlock)) {
    warn(
      dirName,
      'Skill Boundaries subsection does not contain an explicit "Do NOT do these (other skills handle them)" list'
    );
  }

  if (!existsSync(join(skillsDir, dirName, 'agent.yaml'))) {
    warn(dirName, 'Missing agent.yaml (governance artifact)');
  }

  if (!existsSync(join(skillsDir, dirName, 'README.md'))) {
    warn(dirName, 'Missing README.md (governance artifact)');
  }

  // evolution.sources validation (LICENSE_POLICY, spec §2.1)
  const sources = extractEvolutionSources(content);
  for (const s of sources) {
    for (const f of REQUIRED_SOURCE_FIELDS) {
      if (!s[f] || (typeof s[f] === 'string' && !s[f].trim())) {
        error(dirName, `evolution.sources[${s.name || '?'}]: missing required field "${f}"`);
      }
    }
    if (s.license && !ALLOWED_SOURCE_LICENSES.includes(s.license)) {
      error(
        dirName,
        `evolution.sources[${s.name}]: license "${s.license}" not in allowed list (${ALLOWED_SOURCE_LICENSES.join(', ')})`
      );
    }
    if (s.repo && !s.repo.startsWith('http') && s.repo.includes('/')) {
      warn(dirName, `evolution.sources[${s.name}]: repo should use full URL (https://github.com/owner/repo)`);
    }
  }
}

if (!existsSync(skillsDir)) {
  console.error('skills/ directory not found');
  process.exit(1);
}

const entries = readdirSync(skillsDir, { withFileTypes: true });
let checked = 0;
for (const e of entries) {
  if (!e.isDirectory()) continue;
  const skillPath = join(skillsDir, e.name, 'SKILL.md');
  if (!existsSync(skillPath)) continue;
  checkSkill(e.name);
  checked++;
}

console.log('');
console.log(`Checked ${checked} skill(s): ${errors} error(s), ${warnings} warning(s).`);

if (errors > 0) {
  console.error('\nSkill structure verification FAILED.');
  process.exit(1);
}

if (warnings > 0) {
  console.log('\nSkill structure verification PASSED with warnings.');
} else {
  console.log('\nSkill structure verification PASSED.');
}
process.exit(0);
