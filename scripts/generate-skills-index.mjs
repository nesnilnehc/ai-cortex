#!/usr/bin/env node
/**
 * Generate skills/INDEX.md registry table from manifest.json and SKILL frontmatter.
 * Run from repo root: node scripts/generate-skills-index.mjs
 */
import { existsSync, readFileSync, writeFileSync } from 'fs';
import { dirname, join } from 'path';
import { fileURLToPath } from 'url';
import { parseSkillFrontmatter } from './lib/parse-skill-frontmatter.mjs';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, '..');
const manifestPath = join(root, 'manifest.json');
const indexPath = join(root, 'skills', 'INDEX.md');

if (!existsSync(manifestPath)) {
  console.error('manifest.json not found at repo root');
  process.exit(1);
}
if (!existsSync(indexPath)) {
  console.error('skills/INDEX.md not found');
  process.exit(1);
}

const manifest = JSON.parse(readFileSync(manifestPath, 'utf8'));
const capabilities = manifest.capabilities || [];
const currentIndex = readFileSync(indexPath, 'utf8');

const getStability = (version) => {
  const major = Number((version || '').split('.')[0]);
  if (!Number.isFinite(major) || major < 0) return 'stable';
  if (major === 0) return 'experimental';
  if (major >= 2) return 'mature';
  return 'stable';
};

const normalizePurpose = (description) => {
  const text = String(description || '').trim().replace(/\|/g, '\\|');
  if (!text) return 'No description.';
  if (/[.!?]$/.test(text)) return text;
  return `${text}.`;
};

const rows = capabilities.map((cap) => {
  const skillPath = join(root, cap.path);
  if (!existsSync(skillPath)) {
    console.error(`Missing skill file for capability "${cap.name}": ${cap.path}`);
    process.exit(1);
  }
  const meta = parseSkillFrontmatter(readFileSync(skillPath, 'utf8'));
  if (!meta?.name || !meta?.version || !meta?.tags || !meta?.description) {
    console.error(`Invalid frontmatter for "${cap.name}" at ${cap.path}`);
    process.exit(1);
  }
  const tags = meta.tags.join(', ');
  const version = meta.version;
  const stability = getStability(version);
  const purpose = normalizePurpose(meta.description_zh || meta.description);
  return `| [${meta.name}](./${meta.name}/SKILL.md) | ${tags} | \`${version}\` | ${stability} | ${purpose} |`;
});

const registrySection = [
  '## 3. Skill registry',
  '',
  '| Skill name | Tags | Version | Stability | Purpose |',
  '| :--- | :--- | :--- | :--- | :--- |',
  ...rows,
  '',
  '---',
  '',
  '',
].join('\n');

const sectionPattern = /## 3\. Skill registry[\s\S]*?---\n+## 4\. (?:Scheduling and extension|调度与扩展)/;
if (!sectionPattern.test(currentIndex)) {
  console.error('Failed to locate skills/INDEX.md section "## 3. Skill registry"');
  process.exit(1);
}

const updated = currentIndex.replace(
  sectionPattern,
  `${registrySection}## 4. 调度与扩展`
);

writeFileSync(indexPath, `${updated.trimEnd()}\n`, 'utf8');
console.log('Generated skills/INDEX.md from manifest.json and SKILL frontmatter.');
