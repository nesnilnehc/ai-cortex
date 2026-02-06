#!/usr/bin/env node
/**
 * Verify skills/INDEX.md and manifest.json stay in sync.
 * - Every capability in manifest.json has a path that exists.
 * - Every directory under skills/ that contains SKILL.md is listed in manifest capabilities.
 * Run from repo root: node scripts/verify-registry.mjs
 */
import { readFileSync, readdirSync, existsSync } from 'fs';
import { dirname, join } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, '..');

const manifestPath = join(root, 'manifest.json');
const skillsDir = join(root, 'skills');

if (!existsSync(manifestPath)) {
  console.error('manifest.json not found at repo root');
  process.exit(1);
}
if (!existsSync(skillsDir)) {
  console.error('skills/ not found');
  process.exit(1);
}

const manifest = JSON.parse(readFileSync(manifestPath, 'utf8'));
const capabilities = manifest.capabilities || [];
const manifestNames = new Set(capabilities.map((c) => c.name));
const manifestPaths = new Map(capabilities.map((c) => [c.name, c.path]));

let failed = false;

// Every capability path must exist
for (const cap of capabilities) {
  const fullPath = join(root, cap.path);
  if (!existsSync(fullPath)) {
    console.error(`Missing path for capability "${cap.name}": ${cap.path}`);
    failed = true;
  }
}

// Every skills/*/SKILL.md directory must be in manifest
const entries = readdirSync(skillsDir, { withFileTypes: true });
for (const e of entries) {
  if (!e.isDirectory()) continue;
  const skillPath = join(skillsDir, e.name, 'SKILL.md');
  if (!existsSync(skillPath)) continue;
  if (!manifestNames.has(e.name)) {
    console.error(`Skill directory "${e.name}" has SKILL.md but is not in manifest.json capabilities`);
    failed = true;
  }
}

if (failed) process.exit(1);
console.log('Registry OK: manifest paths exist and every skills/*/SKILL.md is listed.');
process.exit(0);
