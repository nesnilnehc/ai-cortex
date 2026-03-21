#!/usr/bin/env node
/**
 * Shared frontmatter parser for SKILL.md files.
 * Used by verify-registry.mjs and verify-skill-structure.mjs to avoid duplication.
 *
 * Parses YAML frontmatter (--- ... ---) and extracts skill metadata fields.
 * Handles simple single-line values; for list fields, normalizes (trim, filter empty, sort).
 */

/**
 * Normalize a list of strings: trim, filter empty, optionally sort.
 * @param {string[]} list - Raw list items
 * @param {boolean} [sort=true] - Whether to sort (e.g. for tags)
 * @returns {string[]}
 */
export function normalizeList(list, sort = true) {
  const out = list
    .map((v) => String(v).trim())
    .filter(Boolean);
  return sort ? [...out].sort((a, b) => a.localeCompare(b)) : out;
}

/**
 * Parse SKILL.md frontmatter and extract metadata.
 * @param {string} content - Full file content or raw YAML block
 * @returns {{ name?: string; description?: string; version?: string; license?: string; tags?: string[]; triggers?: string[]; aliases?: string[] } | null}
 */
export function parseSkillFrontmatter(content) {
  const match = content.match(/^---\n([\s\S]*?)\n---/);
  if (!match) return null;
  const raw = match[1];
  const lines = raw.split('\n');

  const meta = {};
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    if (line.startsWith('name:')) {
      meta.name = line.split(':').slice(1).join(':').trim();
      continue;
    }
    if (line.startsWith('description:')) {
      meta.description = line.split(':').slice(1).join(':').trim();
      continue;
    }
    if (line.startsWith('version:')) {
      meta.version = line.split(':').slice(1).join(':').trim();
      continue;
    }
    if (line.startsWith('license:')) {
      meta.license = line.split(':').slice(1).join(':').trim();
      continue;
    }
    if (line.startsWith('tags:')) {
      const tagMatch = line.match(/tags:\s*\[(.*)\]\s*$/);
      if (tagMatch) {
        meta.tags = normalizeList(tagMatch[1].split(','));
      }
      continue;
    }
    if (line.startsWith('triggers:')) {
      const tMatch = line.match(/triggers:\s*\[(.*)\]\s*$/);
      if (tMatch) {
        meta.triggers = normalizeList(tMatch[1].split(','));
      }
      continue;
    }
    if (line.startsWith('aliases:')) {
      const aMatch = line.match(/aliases:\s*\[(.*)\]\s*$/);
      if (aMatch) {
        meta.aliases = normalizeList(aMatch[1].split(','), false);
      }
    }
  }
  return meta;
}
