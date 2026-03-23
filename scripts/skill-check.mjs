#!/usr/bin/env node
/**
 * skill:check — Health dashboard for skills and registry.
 *
 * Orchestrates:
 *   - verify-registry (manifest, INDEX sync)
 *   - verify-skill-structure (per-skill spec compliance)
 *   - Self-Check vs Success Criteria count alignment (warning)
 *
 * Run from repo root: node scripts/skill-check.mjs
 */
import { spawnSync } from 'child_process';
import { readFileSync, readdirSync, existsSync } from 'fs';
import { dirname, join } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, '..');
const skillsDir = join(root, 'skills');

let totalErrors = 0;
let totalWarnings = 0;

function findSection(content, englishName, chineseAliases = []) {
  const escapeRe = (s) => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const patterns = [
    new RegExp(`## ${escapeRe(englishName)}\\b([\\s\\S]*?)(?=\\n## |\\n---\\s*$|$)`, 'i'),
    ...chineseAliases.map(
      (a) =>
        new RegExp(`## ${escapeRe(a)}[^\\n]*([\\s\\S]*?)(?=\\n## |\\n---\\s*$|$)`, 'i')
    ),
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
  return section.split('\n').filter((l) => /^\d+\.\s+/.test(l.trim())).length;
}

function countSelfCheckItems(content) {
  const section = findSection(content, 'Self-Check', ['自检']);
  if (!section) return -1;
  const checklistItems = section.match(/^-\s+\[[\sx]\]/gm);
  return checklistItems ? checklistItems.length : 0;
}

// ─── 1. Registry ─────────────────────────────────────────────────

console.log('  Registry (manifest, INDEX):');
const registryResult = spawnSync('node', ['scripts/verify-registry.mjs'], {
  cwd: root,
  stdio: 'pipe',
  encoding: 'utf8',
});

if (registryResult.status !== 0) {
  totalErrors++;
  console.log('  ❌ FAILED');
  if (registryResult.stderr) process.stderr.write(registryResult.stderr);
  if (registryResult.stdout) process.stdout.write(registryResult.stdout);
} else {
  console.log('  ✅ OK');
}
console.log('');

// ─── 2. Skills (structure) ───────────────────────────────────────

console.log('  Skills (spec compliance):');
const structureResult = spawnSync('node', ['scripts/verify-skill-structure.mjs'], {
  cwd: root,
  stdio: 'pipe',
  encoding: 'utf8',
});

if (structureResult.status !== 0) {
  totalErrors++;
  console.log('  ❌ FAILED');
  if (structureResult.stderr) process.stderr.write(structureResult.stderr);
  if (structureResult.stdout) process.stdout.write(structureResult.stdout);
} else {
  console.log('  ✅ OK');
  if (structureResult.stdout && structureResult.stdout.includes('warning')) {
    totalWarnings++;
    const lines = structureResult.stdout.split('\n').filter((l) => l.includes('⚠️'));
    for (const line of lines) console.log('  ' + line.trim());
  }
}
console.log('');

// ─── 3. Self-Check vs Success Criteria alignment ─────────────────

console.log('  Self-Check vs Success Criteria alignment:');

const entries = readdirSync(skillsDir, { withFileTypes: true });
let alignmentWarnings = 0;

for (const e of entries) {
  if (!e.isDirectory()) continue;
  const skillPath = join(skillsDir, e.name, 'SKILL.md');
  if (!existsSync(skillPath)) continue;

  const content = readFileSync(skillPath, 'utf8');
  const criteriaCount = countSuccessCriteria(content);
  const selfCheckCount = countSelfCheckItems(content);

  if (criteriaCount >= 0 && selfCheckCount >= 0 && selfCheckCount < criteriaCount) {
    alignmentWarnings++;
    console.log(
      `  ⚠️  ${e.name}: Self-Check has ${selfCheckCount} item(s), Success Criteria has ${criteriaCount}`
    );
  }
}

if (alignmentWarnings === 0) {
  console.log('  ✅ OK');
} else {
  totalWarnings += alignmentWarnings;
}

// ─── Summary ─────────────────────────────────────────────────────

console.log('');
if (totalErrors > 0) {
  console.log('skill:check FAILED.');
  process.exit(1);
}
if (totalWarnings > 0) {
  console.log('skill:check PASSED with warnings.');
} else {
  console.log('skill:check PASSED.');
}
process.exit(0);
