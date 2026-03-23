#!/usr/bin/env node
/**
 * Verify skills/INDEX.md, manifest.json, skillgraph.md, and marketplace.json stay in sync.
 * Regenerates INDEX.md and skillgraph.md from sources first, then validates.
 * - Every capability in manifest.json has a path that exists.
 * - Every directory under skills/ that contains SKILL.md is listed in manifest capabilities.
 * - Every skill in marketplace.json exists in skills/ and is registered in INDEX.md.
 * Run from repo root: node scripts/verify-registry.mjs
 */
import { spawnSync } from 'child_process';
import { readFileSync, readdirSync, existsSync } from 'fs';
import { dirname, join } from 'path';
import { fileURLToPath } from 'url';
import { parseSkillFrontmatter, normalizeList } from './lib/parse-skill-frontmatter.mjs';

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

// Regenerate INDEX.md and skillgraph.md from sources
const genScript = join(root, 'scripts', 'generate-skills-docs.mjs');
if (existsSync(genScript)) {
  const r = spawnSync('node', [genScript], { cwd: root, stdio: 'pipe', encoding: 'utf8' });
  if (r.status !== 0) {
    console.error('generate-skills-docs failed:', r.stderr || r.error);
    process.exit(r.status || 1);
  }
}

const manifest = JSON.parse(readFileSync(manifestPath, 'utf8'));
const capabilities = manifest.capabilities || [];
const manifestNames = new Set(capabilities.map((c) => c.name));

let failed = false;

const readSkillFrontmatter = (skillPath) => {
  const content = readFileSync(skillPath, 'utf8');
  return parseSkillFrontmatter(content);
};

const readIndexEntries = () => {
  const text = readFileSync(indexPath, 'utf8');
  const entries = [];
  for (const line of text.split('\n')) {
    if (!line.startsWith('| [')) continue;
    const match = line.match(/^\|\s+\[([^\]]+)\]\(([^)]+)\)\s+\|\s+([^|]+)\s+\|\s+`([^`]+)`\s+\|\s+\w+\s+\|/);
    const matchLegacy = line.match(/^\|\s+\[([^\]]+)\]\(([^)]+)\)\s+\|\s+([^|]+)\s+\|\s+`([^`]+)`\s+\|/);
    const m = match || matchLegacy;
    if (!m) continue;
    const [, name, path, tagsRaw, version] = m;
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

// marketplace.json sync check (if file exists)
const marketplacePath = join(root, '.claude-plugin', 'marketplace.json');
if (existsSync(marketplacePath)) {
  const marketplace = JSON.parse(readFileSync(marketplacePath, 'utf8'));
  const plugins = marketplace.plugins || [];
  for (const plugin of plugins) {
    for (const skillPath of plugin.skills || []) {
      const skillName = skillPath.replace(/^\.\/skills\//, '');
      if (!skillDirNames.has(skillName)) {
        console.error(`marketplace.json lists "${skillName}" but skills/${skillName}/SKILL.md is missing`);
        failed = true;
      }
      if (!indexNames.has(skillName)) {
        console.error(`marketplace.json lists "${skillName}" but it is missing from skills/INDEX.md`);
        failed = true;
      }
    }
  }
}

// Optional: warn if triggers contain non-ASCII (spec prefers English)
for (const cap of capabilities) {
  const fullPath = join(root, cap.path);
  if (!existsSync(fullPath)) continue;
  const meta = readSkillFrontmatter(fullPath);
  if (meta?.triggers?.length) {
    const nonAscii = meta.triggers.filter((t) => !/^[a-zA-Z0-9\s\-]+$/.test(t));
    if (nonAscii.length) {
      console.warn(`Skill "${cap.name}": triggers should be English (ASCII): ${nonAscii.join(', ')}`);
    }
  }
}

if (failed) process.exit(1);
console.log(
  'Registry OK: manifest, skills/INDEX.md, skillgraph.md, marketplace.json, and skills/*/SKILL.md are consistent.'
);
process.exit(0);
