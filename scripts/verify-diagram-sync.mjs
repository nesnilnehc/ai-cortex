#!/usr/bin/env node
import { readFileSync } from 'fs';
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

function main() {
  const readme = readFileSync(readmePath, 'utf8');
  const readmeBlocks = extractMermaidBlocks(readme);

  if (readmeBlocks.length < 2) {
    console.error(`README.md must contain at least 2 Mermaid blocks, found ${readmeBlocks.length}.`);
    process.exit(1);
  }

  const workflow = extractSingleMermaid(readFileSync(workflowPath, 'utf8'), 'docs/images/workflow-sequence.mmd');
  const ecosystem = extractSingleMermaid(readFileSync(ecosystemPath, 'utf8'), 'docs/images/ecosystem-topology.mmd');

  const checks = [
    {
      name: 'workflow-sequence',
      readmeBlock: readmeBlocks[0],
      sourceBlock: workflow,
      sourcePath: 'docs/images/workflow-sequence.mmd',
    },
    {
      name: 'ecosystem-topology',
      readmeBlock: readmeBlocks[1],
      sourceBlock: ecosystem,
      sourcePath: 'docs/images/ecosystem-topology.mmd',
    },
  ];

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
