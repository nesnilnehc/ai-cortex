#!/usr/bin/env node
import { existsSync, readdirSync, readFileSync } from 'fs';
import { dirname, extname, join, resolve } from 'path';
import { fileURLToPath } from 'url';

const __dirname = fileURLToPath(new URL('.', import.meta.url));
const root = join(__dirname, '..');

const IGNORE_DIRS = new Set(['.git', 'node_modules', '.claude']);
const LINK_REGEX = /!?\[[^\]]*]\(([^)]+)\)/g;

function walk(dir, out = []) {
  const entries = readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    if (entry.isDirectory()) {
      if (!IGNORE_DIRS.has(entry.name)) {
        walk(join(dir, entry.name), out);
      }
      continue;
    }
    if (extname(entry.name).toLowerCase() === '.md') {
      out.push(join(dir, entry.name));
    }
  }
  return out;
}

function stripCodeFences(markdown) {
  return markdown.replace(/```[\s\S]*?```/g, '');
}

function isSkippableLink(link) {
  const lower = link.toLowerCase();
  return (
    lower.startsWith('#') ||
    lower.startsWith('http://') ||
    lower.startsWith('https://') ||
    lower.startsWith('mailto:') ||
    lower.startsWith('tel:') ||
    lower.startsWith('data:')
  );
}

function parseTarget(rawLink) {
  const link = rawLink.trim().replace(/^<|>$/g, '');
  const [pathPart] = link.split('#');
  return decodeURI(pathPart);
}

function checkFile(filePath) {
  const content = readFileSync(filePath, 'utf8');
  const searchable = stripCodeFences(content);
  const failures = [];

  for (const match of searchable.matchAll(LINK_REGEX)) {
    const rawLink = match[1]?.trim() || '';
    if (!rawLink || isSkippableLink(rawLink)) continue;

    const target = parseTarget(rawLink);
    if (!target) continue;

    const resolved = resolve(dirname(filePath), target);
    if (!existsSync(resolved)) {
      failures.push({ rawLink, resolved });
    }
  }

  return failures;
}

function main() {
  const files = walk(root);
  let failed = 0;

  for (const file of files) {
    const failures = checkFile(file);
    if (failures.length === 0) continue;
    failed += failures.length;
    const rel = file.replace(`${root}/`, '');
    console.error(`✗ ${rel}`);
    for (const f of failures) {
      console.error(`  - ${f.rawLink} -> ${f.resolved.replace(`${root}/`, '')}`);
    }
  }

  if (failed > 0) {
    console.error(`\nMarkdown link check failed: ${failed} broken local link(s).`);
    process.exit(1);
  }

  console.log(`Markdown link check passed: ${files.length} Markdown files scanned.`);
}

main();
