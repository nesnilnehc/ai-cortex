#!/usr/bin/env node
/**
 * Generate skills/intent-routing.md from skills/intent-routing.json.
 * Run from repo root: node scripts/generate-intent-routing.mjs
 * Output: skills/intent-routing.md (auto-generated; edit intent-routing.json instead)
 */
import { readFileSync, writeFileSync, existsSync } from 'fs';
import { dirname, join } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, '..');
const skillsDir = join(root, 'skills');
const configPath = join(skillsDir, 'intent-routing.json');
const outPath = join(skillsDir, 'intent-routing.md');

if (!existsSync(configPath)) {
  console.error('skills/intent-routing.json not found');
  process.exit(1);
}

const config = JSON.parse(readFileSync(configPath, 'utf8'));

const link = (name) => `[${name}](./${name}/SKILL.md)`;

function renderIntent(s, i) {
  const optList = (s.optional || []).map((o) => {
    const note = s.optional_note && o === (s.optional || [])[0] ? ` (${s.optional_note})` : '';
    return `  - ${link(o)}${note}`;
  }).join('\n');
  const optSection = optList ? `\n- **可选技能**：\n${optList}` : '';
  const triggersEn = (s.short_triggers && s.short_triggers.length)
    ? `\n- **Short triggers**：${s.short_triggers.join(', ')}`
    : '';
  const triggersZh = (s.short_triggers_zh && s.short_triggers_zh.length)
    ? `\n- **中文触发**：${s.short_triggers_zh.join(', ')}`
    : '';
  const triggersSection = triggersEn + triggersZh;
  const intentSection = s.intent ? `\n- **意图**：${s.intent}` : '';
  return `## ${i}) ${s.title}

- **适用情境**：${s.when_to_use}${intentSection}
- **主技能**：${link(s.primary)}${optSection}${triggersSection}
- **产出**：${s.output}
- **停止条件**：${s.stop_condition}`;
}

const routingRules = config.routing_rules || [];
const rulesText = routingRules.map((r, i) => `${i + 1}. ${r}`).join('\n');

const intents = config.intents || [];
const body = intents.map((s, i) => renderIntent(s, i + 1)).join('\n\n');

const doc = `# 意图-技能映射

*由 \`scripts/generate-intent-routing.mjs\` 从 intent-routing.json 自动生成。请编辑 JSON，勿直接修改本文件。*

按用户工作习惯（意图）选择技能，无需记忆技能名。

规范技能注册见 [INDEX.md](./INDEX.md)。

---

${body}

---

## 路由规则

${rulesText}
`;

writeFileSync(outPath, doc, 'utf8');
console.log(`Written ${outPath}`);
