/**
 * Integration tests: run verify-registry and verify-skill-structure against the real repo.
 * Assumes run from repo root.
 */
import { describe, it } from 'node:test';
import assert from 'node:assert';
import { spawnSync } from 'child_process';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, '..', '..');

describe('verify-registry', () => {
  it('exits 0 when registry is consistent', () => {
    const r = spawnSync('node', ['scripts/verify-registry.mjs'], {
      cwd: root,
      encoding: 'utf8',
    });
    assert.strictEqual(
      r.status,
      0,
      `verify-registry failed: ${r.stderr || r.stdout}`
    );
  });
});

describe('verify-skill-structure', () => {
  it('exits 0 when all skills conform to spec', () => {
    const r = spawnSync('node', ['scripts/verify-skill-structure.mjs'], {
      cwd: root,
      encoding: 'utf8',
    });
    assert.strictEqual(
      r.status,
      0,
      `verify-skill-structure failed: ${r.stderr || r.stdout}`
    );
  });
});
