/**
 * Unit tests for scripts/lib/parse-skill-frontmatter.mjs
 */
import { describe, it } from 'node:test';
import assert from 'node:assert';
import { parseSkillFrontmatter, normalizeList } from '../lib/parse-skill-frontmatter.mjs';

describe('normalizeList', () => {
  it('trims and filters empty', () => {
    assert.deepStrictEqual(
      normalizeList([' a ', '', 'b', '  ']),
      ['a', 'b']
    );
  });

  it('sorts by default', () => {
    assert.deepStrictEqual(
      normalizeList(['z', 'a', 'm']),
      ['a', 'm', 'z']
    );
  });

  it('skips sort when sort=false', () => {
    assert.deepStrictEqual(
      normalizeList(['z', 'a'], false),
      ['z', 'a']
    );
  });
});

describe('parseSkillFrontmatter', () => {
  it('returns null for empty or invalid content', () => {
    assert.strictEqual(parseSkillFrontmatter(''), null);
    assert.strictEqual(parseSkillFrontmatter('no frontmatter'), null);
  });

  it('extracts name, version, tags', () => {
    const content = `---
name: foo-skill
version: 1.0.0
tags: [a, b, c]
---`;
    const meta = parseSkillFrontmatter(content);
    assert.strictEqual(meta?.name, 'foo-skill');
    assert.strictEqual(meta?.version, '1.0.0');
    assert.deepStrictEqual(meta?.tags, ['a', 'b', 'c']);
  });

  it('extracts description, license, related_skills', () => {
    const content = `---
name: bar
description: A skill
license: MIT
related_skills: [skill-a, skill-b]
---`;
    const meta = parseSkillFrontmatter(content);
    assert.strictEqual(meta?.description, 'A skill');
    assert.strictEqual(meta?.license, 'MIT');
    assert.deepStrictEqual(meta?.related_skills, ['skill-a', 'skill-b']);
  });

  it('handles value with colon in name', () => {
    const content = `---
name: foo: extended name
version: 1.0.0
---`;
    const meta = parseSkillFrontmatter(content);
    assert.strictEqual(meta?.name, 'foo: extended name');
  });

  it('normalizes and sorts tags', () => {
    const content = `---
name: x
tags: [ z , a ,  b ]
---`;
    const meta = parseSkillFrontmatter(content);
    assert.deepStrictEqual(meta?.tags, ['a', 'b', 'z']);
  });
});
