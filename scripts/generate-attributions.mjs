#!/usr/bin/env node
/**
 * Generate docs/references/ATTRIBUTIONS.md from skills' metadata.evolution.sources.
 * Run from repo root: node scripts/generate-attributions.mjs
 */
import { readFileSync, readdirSync, existsSync, writeFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, '..');
const skillsDir = join(root, 'skills');
const outPath = join(root, 'docs', 'references', 'ATTRIBUTIONS.md');

/** Extract evolution.sources from YAML frontmatter. */
function extractSources(content) {
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

/** Normalize repo to owner/repo for display. */
function normalizeRepo(repo) {
  if (!repo) return '';
  const m = repo.match(/github\.com[/:]([^/]+)\/([^/\s]+)/);
  if (m) return `${m[1]}/${m[2].replace(/\.git$/, '')}`;
  if (repo.includes('/') && !repo.includes('://')) return repo;
  return repo;
}

function main() {
  if (!existsSync(skillsDir)) {
    console.error('skills/ not found');
    process.exit(1);
  }
  const entries = readdirSync(skillsDir, { withFileTypes: true });
  const rows = [];
  for (const e of entries) {
    if (!e.isDirectory()) continue;
    const path = join(skillsDir, e.name, 'SKILL.md');
    if (!existsSync(path)) continue;
    const content = readFileSync(path, 'utf8');
    const sources = extractSources(content);
    for (const s of sources) {
      if (!s.name || !s.repo) continue;
      const repoNorm = normalizeRepo(s.repo);
      const repoClean = s.repo.replace(/\s*\(assumed\)\s*$/i, '').trim();
      const repoUrl =
        repoNorm && !repoClean.startsWith('http')
          ? `https://github.com/${repoNorm}`
          : repoClean;
      const repoDisplay =
        repoNorm ||
        s.repo.replace(/^https?:\/\/github\.com\/?/, '').replace(/\.git$/, '') ||
        s.repo;
      rows.push({
        repo: repoUrl,
        repoDisplay,
        name: s.name,
        version: s.version || '-',
        license: s.license || '-',
        type: s.type || '-',
        borrowed: (s.borrowed || '').slice(0, 80) + (s.borrowed && s.borrowed.length > 80 ? '...' : ''),
        usedBy: e.name,
      });
    }
  }
  rows.sort((a, b) => {
    const ra = a.repoDisplay.toLowerCase();
    const rb = b.repoDisplay.toLowerCase();
    if (ra !== rb) return ra.localeCompare(rb);
    return a.usedBy.localeCompare(b.usedBy);
  });
  const header = `# 参考来源与致谢

<!-- markdownlint-disable MD058 MD060 -->

本文件枚举 AI Cortex 技能中 \`metadata.evolution.sources\` 引用的外部仓库与技能，供许可合规与溯源使用。详见 [LICENSE_POLICY.md](./LICENSE_POLICY.md)。

---

## 按仓库

| 仓库 | 来源技能 | 版本 | 许可证 | 类型 | 借用内容 | 使用方 |
| --- | --- | --- | --- | --- | --- | --- |
`;
  const tableRows = rows.map(
    (r) =>
      `| [${r.repoDisplay}](${r.repo}) | ${r.name} | ${r.version} | ${r.license} | ${r.type} | ${r.borrowed} | ${r.usedBy} |`
  );
  const notes = `

---

## 备注

- **anthropics/skills**：上游仓库根目录未检出 LICENSE 文件；按惯例声明 MIT，建议定期复核。
- **jwynia/agent-skills**：GitHub API 未检测到仓库级 license；skills 目录下技能可能单独声明，建议定期复核。
- **nesnilnehc/ai-cortex**：本仓库内部引用。
`;
  const out = header + tableRows.join('\n') + notes;
  writeFileSync(outPath, out, 'utf8');
  console.log(`Wrote ${outPath} (${rows.length} entries)`);
}

main();
