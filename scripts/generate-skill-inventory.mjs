#!/usr/bin/env node
// Generate skills/SKILL_INVENTORY.md from agent.yaml files.
// Replaces the legacy ASQM_AUDIT.md per ADR 008.
import { readdirSync, readFileSync, writeFileSync, statSync } from 'node:fs';
import { join } from 'node:path';

const SKILLS_DIR = join(process.cwd(), 'skills');
const OUT_PATH = join(SKILLS_DIR, 'SKILL_INVENTORY.md');

function parseSimpleYaml(text) {
  // Minimal YAML parser for our agent.yaml files (top-level scalars + lists).
  const obj = {};
  const lines = text.split('\n');
  let i = 0;
  while (i < lines.length) {
    const line = lines[i];
    if (!line.trim() || line.startsWith('#')) { i++; continue; }
    const m = line.match(/^([A-Za-z_][A-Za-z0-9_]*)\s*:\s*(.*)$/);
    if (!m) { i++; continue; }
    const key = m[1];
    const rest = m[2];
    if (rest === '' || rest === '|' || rest === '>') {
      // block scalar or list follows on indented lines
      const list = [];
      let j = i + 1;
      let folded = '';
      while (j < lines.length && (lines[j].startsWith('  ') || lines[j].startsWith('-') || lines[j].startsWith(' -') || lines[j].trim() === '')) {
        const l = lines[j];
        if (/^\s*-\s+/.test(l)) {
          list.push(l.replace(/^\s*-\s+/, '').trim());
        } else if (l.startsWith('  ')) {
          folded += (folded ? ' ' : '') + l.trim();
        } else if (l.trim() === '') {
          // blank
        } else {
          break;
        }
        j++;
      }
      obj[key] = list.length > 0 ? list : folded;
      i = j;
      continue;
    }
    if (rest === '[]') { obj[key] = []; i++; continue; }
    if (rest === 'true' || rest === 'false') { obj[key] = rest === 'true'; i++; continue; }
    obj[key] = rest;
    i++;
  }
  return obj;
}

const skills = readdirSync(SKILLS_DIR)
  .filter((n) => {
    try { return statSync(join(SKILLS_DIR, n)).isDirectory(); } catch { return false; }
  })
  .sort();

const rows = [];
for (const name of skills) {
  const yamlPath = join(SKILLS_DIR, name, 'agent.yaml');
  let raw;
  try { raw = readFileSync(yamlPath, 'utf8'); } catch { continue; }
  const data = parseSimpleYaml(raw);
  rows.push({
    name,
    status: data.status || 'unknown',
    has_output_contract: data.has_output_contract === true,
    acceptance_criteria_count: Array.isArray(data.acceptance_criteria) ? data.acceptance_criteria.length : 0,
    market_position: data.market_position || 'unspecified',
    tags: Array.isArray(data.tags) ? data.tags : [],
  });
}

const today = new Date().toISOString().slice(0, 10);
const total = rows.length;
const validated = rows.filter((r) => r.status === 'validated');
const experimental = rows.filter((r) => r.status === 'experimental');
const archive = rows.filter((r) => r.status === 'archive_candidate');
const withContract = rows.filter((r) => r.has_output_contract);
const withoutContract = rows.filter((r) => !r.has_output_contract);
const missingAc = rows.filter((r) => r.acceptance_criteria_count === 0);

const lines = [];
lines.push('# Skill Inventory — AI Cortex');
lines.push('');
lines.push(`**Generated**: ${today}`);
lines.push(`**Source**: \`skills/*/agent.yaml\` via \`scripts/generate-skill-inventory.mjs\``);
lines.push(`**Scope**: \`skills/\` — ${total} skills`);
lines.push('');
lines.push('---');
lines.push('');
lines.push('## Status Rule');
lines.push('');
lines.push('Per [ADR 008](../docs/architecture/adrs/008-replace-asqm-with-acceptance-criteria.md):');
lines.push('');
lines.push('```');
lines.push('validated         = has_output_contract AND len(acceptance_criteria) >= 1');
lines.push('experimental      = otherwise');
lines.push('archive_candidate = manual only');
lines.push('```');
lines.push('');
lines.push('No scoring system. ASQM (`scores`, `asqm_quality`, `validation_gates`, `cognitive_mode`) was removed in full on 2026-04-28.');
lines.push('');
lines.push('---');
lines.push('');
lines.push('## Distribution');
lines.push('');
lines.push('| Bucket | Count | % |');
lines.push('|---|---|---|');
lines.push(`| validated | ${validated.length} | ${((validated.length / total) * 100).toFixed(1)}% |`);
lines.push(`| experimental | ${experimental.length} | ${((experimental.length / total) * 100).toFixed(1)}% |`);
lines.push(`| archive_candidate | ${archive.length} | ${((archive.length / total) * 100).toFixed(1)}% |`);
lines.push('');
lines.push('### Output contract coverage');
lines.push('');
lines.push(`- has_output_contract: true → **${withContract.length} / ${total}** (${((withContract.length / total) * 100).toFixed(1)}%)`);
lines.push(`- has_output_contract: false → **${withoutContract.length} / ${total}**`);
lines.push('');
lines.push(`### acceptance_criteria coverage`);
lines.push('');
lines.push(`- skills with ≥1 acceptance_criterion → **${total - missingAc.length} / ${total}**`);
lines.push(`- skills with 0 acceptance_criteria  → **${missingAc.length} / ${total}**`);
lines.push('');
lines.push('---');
lines.push('');
lines.push('## All Skills');
lines.push('');
lines.push('| Skill | status | has_output_contract | acceptance_criteria | market_position |');
lines.push('|---|---|---|---|---|');
for (const r of rows) {
  lines.push(`| ${r.name} | ${r.status} | ${r.has_output_contract} | ${r.acceptance_criteria_count} | ${r.market_position} |`);
}
lines.push('');
lines.push('---');
lines.push('');
lines.push('## Skills missing output contract');
lines.push('');
if (withoutContract.length === 0) {
  lines.push('_None._');
} else {
  for (const r of withoutContract) {
    lines.push(`- ${r.name}`);
  }
}
lines.push('');
lines.push('---');
lines.push('');
lines.push('## Skills missing acceptance_criteria');
lines.push('');
if (missingAc.length === 0) {
  lines.push('_None._');
} else {
  for (const r of missingAc) {
    lines.push(`- ${r.name}`);
  }
}
lines.push('');
lines.push('---');
lines.push('');
lines.push('## Maintenance Protocol');
lines.push('');
lines.push('- This file is **regenerated** by `node scripts/generate-skill-inventory.mjs`. Do not hand-edit.');
lines.push('- `curate-skills` re-runs the generator after batch updates to `agent.yaml`.');
lines.push('- A skill flips from `experimental` to `validated` only when its `SKILL.md` has an output-contract appendix **and** `agent.yaml` has at least one `acceptance_criteria` entry.');
lines.push('- `archive_candidate` is set manually by a maintainer; the rule never assigns it.');
lines.push('');
lines.push('---');
lines.push('');
lines.push('## Final Recommendations');
lines.push('');
lines.push(`1. **Phase 10 (review-* output contracts)** — ${rows.filter((r) => r.name.startsWith('review-') && !r.has_output_contract).length} review-* skills still lack output contracts; batch-add YAML schema appendix.`);
lines.push(`2. **Phase 11 (governance skills)** — high-composability skills (plan-next, align-*, audit-docs) need output contracts to feed downstream consumers.`);
lines.push(`3. **Phase 12 (strategy + procedural)** — remaining ${withoutContract.length - rows.filter((r) => r.name.startsWith('review-') && !r.has_output_contract).length - rows.filter((r) => /^(plan-next|align-|audit-docs|prioritize-backlog|promote-roadmap-items|capture-work-items|assess-docs)/.test(r.name) && !r.has_output_contract).length} skills (define-*, design-*, generate-*, sync-*, tidy-*, etc.) follow.`);
lines.push(`4. **Acceptance criteria backfill** — all ${missingAc.length} skills need at least one observable input→output assertion to flip to \`validated\`.`);
lines.push('');

writeFileSync(OUT_PATH, lines.join('\n'), 'utf8');
console.log(`Wrote ${OUT_PATH}`);
console.log(`  total=${total} validated=${validated.length} experimental=${experimental.length} archive=${archive.length}`);
console.log(`  has_output_contract=${withContract.length} missing_contract=${withoutContract.length}`);
console.log(`  missing_acceptance_criteria=${missingAc.length}`);
