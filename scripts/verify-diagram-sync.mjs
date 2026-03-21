#!/usr/bin/env node
import { readFileSync, existsSync } from 'fs';
import { join } from 'path';
import { fileURLToPath } from 'url';

const __dirname = fileURLToPath(new URL('.', import.meta.url));
const root = join(__dirname, '..');

const readmePath = join(root, 'README.md');
const workflowPath = join(root, 'docs/images/workflow-sequence.mmd');
const ecosystemPath = join(root, 'docs/images/ecosystem-topology.mmd');

const MERMAID_BLOCK_REGEX = /```mermaid\s*\n([\s\S]*?)\n```/g;

function normalize(text) {
  return text
    .replace(/\r\n/g, '\n')
    .split('\n')
    .map((line) => line.replace(/[ \t]+$/g, ''))
    .join('\n')
    .trim();
}

function extractMermaidBlocks(markdown) {
  const blocks = [];
  for (const match of markdown.matchAll(MERMAID_BLOCK_REGEX)) {
    blocks.push(normalize(match[1]));
  }
  return blocks;
}

function extractSingleMermaid(fileContent, filePath) {
  const blocks = extractMermaidBlocks(fileContent);
  if (blocks.length !== 1) {
    throw new Error(`${filePath} must contain exactly one Mermaid block, found ${blocks.length}.`);
  }
  return blocks[0];
}

/** Diagram sources that exist under docs/images/ */
const DIAGRAM_SOURCES = [
  { name: 'workflow-sequence', path: workflowPath, relPath: 'docs/images/workflow-sequence.mmd' },
  ...(existsSync(ecosystemPath)
    ? [{ name: 'ecosystem-topology', path: ecosystemPath, relPath: 'docs/images/ecosystem-topology.mmd' }]
    : []),
];

function main() {
  const readme = readFileSync(readmePath, 'utf8');
  const readmeBlocks = extractMermaidBlocks(readme);
  const requiredCount = DIAGRAM_SOURCES.length;

  if (readmeBlocks.length < requiredCount) {
    console.error(`README.md must contain at least ${requiredCount} Mermaid block(s), found ${readmeBlocks.length}.`);
    process.exit(1);
  }

  const checks = DIAGRAM_SOURCES.map((src, i) => ({
    name: src.name,
    readmeBlock: readmeBlocks[i],
    sourceBlock: extractSingleMermaid(readFileSync(src.path, 'utf8'), src.relPath),
    sourcePath: src.relPath,
  }));

  let failed = 0;
  for (const check of checks) {
    if (check.readmeBlock !== check.sourceBlock) {
      failed += 1;
      console.error(`✗ README Mermaid block mismatch: ${check.name}`);
      console.error(`  Source of truth: ${check.sourcePath}`);
    } else {
      console.log(`✓ Diagram synced: ${check.name}`);
    }
  }

  if (failed > 0) {
    console.error(`\nDiagram sync check failed: ${failed} mismatch(es).`);
    process.exit(1);
  }

  console.log('\nAll README Mermaid diagrams are synced with docs/images sources.');
}

main();
