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
const indexPath = join(skillsDir, 'INDEX.md');

if (!existsSync(manifestPath)) {
  console.error('manifest.json not found at repo root');
  process.exit(1);
}
if (!existsSync(skillsDir)) {
  console.error('skills/ not found');
  process.exit(1);
}
if (!existsSync(indexPath)) {
  console.error('skills/INDEX.md not found');
  process.exit(1);
}

const manifest = JSON.parse(readFileSync(manifestPath, 'utf8'));
const capabilities = manifest.capabilities || [];
const manifestNames = new Set(capabilities.map((c) => c.name));

let failed = false;

const normalizeList = (list) =>
  list
    .map((v) => v.trim())
    .filter(Boolean)
    .sort((a, b) => a.localeCompare(b));

const readSkillFrontmatter = (skillPath) => {
  const content = readFileSync(skillPath, 'utf8');
  const match = content.match(/^---\n([\s\S]*?)\n---/);
  if (!match) return null;
  const meta = {};
  for (const line of match[1].split('\n')) {
    if (line.startsWith('name:')) {
      meta.name = line.split(':').slice(1).join(':').trim();
      continue;
    }
    if (line.startsWith('version:')) {
      meta.version = line.split(':').slice(1).join(':').trim();
      continue;
    }
    if (line.startsWith('tags:')) {
      const tagMatch = line.match(/tags:\s*\[(.*)\]\s*$/);
      if (tagMatch) {
        meta.tags = normalizeList(tagMatch[1].split(','));
      }
    }
  }
  return meta;
};

const readIndexEntries = () => {
  const text = readFileSync(indexPath, 'utf8');
  const entries = [];
  for (const line of text.split('\n')) {
    if (!line.startsWith('| [')) continue;
    const match = line.match(/^\|\s+\[([^\]]+)\]\(([^)]+)\)\s+\|\s+([^|]+)\s+\|\s+`([^`]+)`\s+\|/);
    if (!match) continue;
    const [, name, path, tagsRaw, version] = match;
    entries.push({
      name: name.trim(),
      path: path.trim(),
      tags: normalizeList(tagsRaw.split(',')),
      version: version.trim(),
    });
  }
  return entries;
};

// Every capability path must exist
for (const cap of capabilities) {
  const fullPath = join(root, cap.path);
  if (!existsSync(fullPath)) {
    console.error(`Missing path for capability "${cap.name}": ${cap.path}`);
    failed = true;
  }
  const expectedPath = `skills/${cap.name}/SKILL.md`;
  if (cap.path !== expectedPath) {
    console.error(`Capability "${cap.name}" path should be "${expectedPath}", found "${cap.path}"`);
    failed = true;
  }
}

// Every skills/*/SKILL.md directory must be in manifest
const entries = readdirSync(skillsDir, { withFileTypes: true });
const skillDirNames = new Set();
for (const e of entries) {
  if (!e.isDirectory()) continue;
  const skillPath = join(skillsDir, e.name, 'SKILL.md');
  if (!existsSync(skillPath)) continue;
  skillDirNames.add(e.name);
  if (!manifestNames.has(e.name)) {
    console.error(`Skill directory "${e.name}" has SKILL.md but is not in manifest.json capabilities`);
    failed = true;
  }
}

// INDEX.md entries must align with manifest and skills directory
const indexEntries = readIndexEntries();
const indexNames = new Set();
for (const entry of indexEntries) {
  if (indexNames.has(entry.name)) {
    console.error(`Duplicate skill "${entry.name}" in skills/INDEX.md`);
    failed = true;
    continue;
  }
  indexNames.add(entry.name);
  const expectedIndexPath = `./${entry.name}/SKILL.md`;
  if (entry.path !== expectedIndexPath) {
    console.error(`skills/INDEX.md path for "${entry.name}" should be "${expectedIndexPath}", found "${entry.path}"`);
    failed = true;
  }
  if (!manifestNames.has(entry.name)) {
    console.error(`skills/INDEX.md lists "${entry.name}" but it is missing from manifest.json capabilities`);
    failed = true;
  }
  if (!skillDirNames.has(entry.name)) {
    console.error(`skills/INDEX.md lists "${entry.name}" but skills/${entry.name}/SKILL.md is missing`);
    failed = true;
  }
  const skillPath = join(skillsDir, entry.name, 'SKILL.md');
  if (existsSync(skillPath)) {
    const meta = readSkillFrontmatter(skillPath);
    if (!meta || !meta.name || !meta.version || !meta.tags) {
      console.error(`Failed to parse front matter for "${entry.name}" at ${skillPath}`);
      failed = true;
    } else {
      if (meta.name !== entry.name) {
        console.error(`Skill name mismatch for "${entry.name}": front matter "${meta.name}"`);
        failed = true;
      }
      if (meta.version !== entry.version) {
        console.error(`Skill version mismatch for "${entry.name}": INDEX "${entry.version}" vs SKILL "${meta.version}"`);
        failed = true;
      }
      const indexTags = normalizeList(entry.tags);
      const metaTags = normalizeList(meta.tags);
      if (indexTags.join(',') !== metaTags.join(',')) {
        console.error(`Skill tags mismatch for "${entry.name}": INDEX "${indexTags.join(', ')}" vs SKILL "${metaTags.join(', ')}"`);
        failed = true;
      }
    }
  }
}

for (const name of manifestNames) {
  if (!indexNames.has(name)) {
    console.error(`manifest.json capability "${name}" is missing from skills/INDEX.md`);
    failed = true;
  }
}

for (const name of skillDirNames) {
  if (!indexNames.has(name)) {
    console.error(`skills/${name}/SKILL.md exists but is missing from skills/INDEX.md`);
    failed = true;
  }
}

if (failed) process.exit(1);
console.log('Registry OK: manifest, skills/INDEX.md, and skills/*/SKILL.md are consistent.');
process.exit(0);
