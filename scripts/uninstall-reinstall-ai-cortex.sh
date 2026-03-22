#!/usr/bin/env bash
# 卸载本机已安装的 AI Cortex 技能并重新安装
# 用途：技能可能已改名或重新定义，需要干净重装
set -euo pipefail

echo "=== 1. 卸载 AI Cortex 技能（全局） ==="
# 从 .skill-lock.json 提取 nesnilnehc/ai-cortex 来源的技能名
AI_CORTEX_SKILLS=$(node -e "
const fs = require('fs');
const lockPath = process.env.HOME + '/.agents/.skill-lock.json';
if (!fs.existsSync(lockPath)) {
  console.log('');
  process.exit(0);
}
const lock = JSON.parse(fs.readFileSync(lockPath, 'utf8'));
const names = Object.entries(lock.skills || {})
  .filter(([_, v]) => v.source === 'nesnilnehc/ai-cortex')
  .map(([name]) => name);
console.log(names.join(' '));
" 2>/dev/null || echo "")

if [[ -z "$AI_CORTEX_SKILLS" ]]; then
  echo "未在 .skill-lock.json 中发现 AI Cortex 技能，可能已卸载或从未安装。"
else
  echo "将卸载以下技能："
  echo "$AI_CORTEX_SKILLS" | tr ' ' '\n' | sed 's/^/  - /'
  npx skills remove $AI_CORTEX_SKILLS -g -y
  echo "卸载完成。"
fi

echo ""
echo "=== 2. 重新安装 AI Cortex（全局，使用 --force 覆盖） ==="
npx skills add nesnilnehc/ai-cortex -g --force -y

echo ""
echo "=== 3. 验证 ==="
npx skills list -g 2>&1 | head -30

echo ""
echo "完成。"
