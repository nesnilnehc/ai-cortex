#!/usr/bin/env node
/**
 * Verify skills producing document-artifact outputs align with spec/artifact-contract.md.
 * - Each contract owner_skill has output_schema with artifact_type and path_pattern.
 * - path_pattern references the contract's canonical paths.
 * Run from repo root: node scripts/verify-artifact-contract.mjs
 */
import { readFileSync, existsSync } from 'fs';
import { dirname, join } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, '..');

const contractPath = join(root, 'spec', 'artifact-contract.md');
const skillsDir = join(root, 'skills');

// Expected mapping (sync with spec/artifact-contract.md Appendix A)
const CONTRACT_SKILLS = {
  'capture-work-items': {
    artifact_type: 'backlog-item',
    path_must_contain: ['project-board/backlog', 'docs/backlog'],
  },
  'bootstrap-docs': {
    artifact_type: 'adr',
    path_must_contain: ['process-management/decisions'],
  },
  'brainstorm-design': {
    artifact_type: 'design',
    path_must_contain: ['design-decisions'],
  },
  'assess-doc-readiness': {
    artifact_type: 'doc-readiness',
    path_must_contain: ['calibration'],
  },
};

function extractYamlFrontmatter(path) {
  const content = readFileSync(path, 'utf8');
  const match = content.match(/^---\n([\s\S]*?)\n---/);
  if (!match) return null;
  const block = match[1];
  const meta = {};
  for (const line of block.split('\n')) {
    if (line.startsWith('  ') || line.startsWith('-')) continue;
    const colon = line.indexOf(':');
    if (colon === -1) continue;
    const key = line.slice(0, colon).trim();
    const val = line.slice(colon + 1).trim().replace(/^['"]|['"]$/g, '');
    if (key && val) meta[key] = val;
  }
  return meta;
}

function extractOutputSchema(content) {
  const schema = {};
  let inOutput = false;
  for (const line of content.split('\n')) {
    if (line.match(/^output_schema:/)) {
      inOutput = true;
      continue;
    }
    if (inOutput) {
      if (line.match(/^\w+_schema:/) && !line.startsWith('  ')) break;
      const colon = line.indexOf(':');
      if (colon > 0 && line.startsWith('  ')) {
        const key = line.slice(0, colon).trim();
        const val = line.slice(colon + 1).trim().replace(/^['"]|['"]$/g, '');
        if (key && val) schema[key] = val;
      }
    }
  }
  return schema;
}

let failed = false;

if (!existsSync(contractPath)) {
  console.error('spec/artifact-contract.md not found');
  process.exit(1);
}

for (const [skillName, expected] of Object.entries(CONTRACT_SKILLS)) {
  const skillPath = join(skillsDir, skillName, 'SKILL.md');
  if (!existsSync(skillPath)) {
    console.error(`Skill "${skillName}" (contract owner) not found at ${skillPath}`);
    failed = true;
    continue;
  }

  const content = readFileSync(skillPath, 'utf8');
  const schema = extractOutputSchema(content);

  if (!schema.artifact_type || schema.artifact_type !== expected.artifact_type) {
    console.error(
      `Skill "${skillName}": output_schema must have artifact_type: ${expected.artifact_type}, found: ${schema.artifact_type || 'missing'}`
    );
    failed = true;
  }

  const pathVal = schema.path_pattern || schema.description || '';
  const hasPath = expected.path_must_contain.some((p) => pathVal.includes(p));
  if (!hasPath) {
    console.error(
      `Skill "${skillName}": output path must reference one of [${expected.path_must_contain.join(', ')}], got: ${pathVal.slice(0, 80)}...`
    );
    failed = true;
  }
}

if (failed) process.exit(1);
console.log('Artifact contract OK: document-artifact skills align with spec/artifact-contract.md.');
process.exit(0);
