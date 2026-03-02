#!/usr/bin/env node
/**
 * Verify every SKILL.md under skills/ conforms to spec/skill.md v2.0.0.
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
 *
 * Run from repo root: node scripts/verify-skill-structure.mjs
 */
import { readFileSync, readdirSync, existsSync } from 'fs';
import { dirname, join } from 'path';
import { fileURLToPath } from 'url';

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

const CORE_OBJECTIVE_SUBSECTIONS = [
  'Primary Goal',
  'Success Criteria',
  'Acceptance Test',
];

const NAME_REGEX = /^[a-z0-9]([a-z0-9-]*[a-z0-9])?$/;
const SEMVER_REGEX = /^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(-[\w.]+)?(\+[\w.]+)?$/;

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
  const match = content.match(/^---\n([\s\S]*?)\n---/);
  if (!match) return null;
  const raw = match[1];
  const meta = {};
  for (const line of raw.split('\n')) {
    if (line.startsWith('name:')) {
      meta.name = line.replace(/^name:\s*/, '').trim();
    } else if (line.startsWith('description:')) {
      meta.description = line.replace(/^description:\s*/, '').trim();
    } else if (line.startsWith('version:')) {
      meta.version = line.replace(/^version:\s*/, '').trim();
    } else if (line.startsWith('license:')) {
      meta.license = line.replace(/^license:\s*/, '').trim();
    } else if (line.startsWith('tags:')) {
      const tagMatch = line.match(/tags:\s*\[(.*)\]\s*$/);
      if (tagMatch) {
        meta.tags = tagMatch[1].split(',').map((t) => t.trim()).filter(Boolean);
      }
    }
  }
  return meta;
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

function countSuccessCriteria(content) {
  const coreObjMatch = content.match(
    /## Core Objective\b([\s\S]*?)(?=\n## [A-Z]|\n---\s*$|$)/
  );
  if (!coreObjMatch) return -1;
  const section = coreObjMatch[1];

  const criteriaLines = section
    .split('\n')
    .filter((l) => /^\d+\.\s+/.test(l.trim()));
  return criteriaLines.length;
}

function countExamples(content) {
  const examplesMatch = content.match(
    /## Examples\b([\s\S]*?)(?=\n## [A-Z]|\n---\s*$|$)/
  );
  if (!examplesMatch) return 0;
  const section = examplesMatch[1];

  const h3Examples = (section.match(/^###\s+/gm) || []).length;
  const boldExamples = (section.match(/^\*\*(Example|Edge case|Before)/gm) || []).length;
  return h3Examples > 0 ? h3Examples : boldExamples;
}

function hasSelfCheckCriteria(content) {
  const selfCheckMatch = content.match(
    /## Self-Check\b([\s\S]*?)(?=\n## [A-Z]|\n---\s*$|$)/
  );
  if (!selfCheckMatch) return false;
  return selfCheckMatch[1].includes('- [ ]');
}

function hasSkillBoundaries(content) {
  return /Skill Boundaries/i.test(content) || /This skill does NOT handle/i.test(content);
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
  const h2Texts = headings
    .filter((h) => h.level === 2)
    .map((h) => h.text.replace(/\s*\(.*\)$/, ''));

  for (const req of REQUIRED_HEADINGS) {
    if (!h2Texts.some((h) => h === req || h.startsWith(req))) {
      error(dirName, `Missing required heading: ## ${req}`);
    }
  }

  if (h2Texts.some((h) => h === 'Core Objective' || h.startsWith('Core Objective'))) {
    for (const sub of CORE_OBJECTIVE_SUBSECTIONS) {
      if (!content.includes(`**${sub}**`)) {
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

  if (!hasSkillBoundaries(content)) {
    warn(dirName, 'No Skill Boundaries section found (overlap risk)');
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
