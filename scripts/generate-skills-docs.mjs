#!/usr/bin/env node
/**
 * Generate skills/INDEX.md, skills/skillgraph.md, and skills/scenario-map.md.
 * Run from repo root: node scripts/generate-skills-docs.mjs
 * Call this before verify-registry when scenario-map.json or skill composition changes.
 */
import { spawnSync } from 'child_process';
import { dirname, join } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, '..');

const scripts = [
  join(root, 'scripts', 'generate-skills-index.mjs'),
  join(root, 'scripts', 'generate-skillgraph.mjs'),
  join(root, 'scripts', 'generate-scenario-map.mjs'),
];

for (const script of scripts) {
  const r = spawnSync('node', [script], { cwd: root, stdio: 'inherit' });
  if (r.status !== 0) process.exit(r.status || 1);
}
