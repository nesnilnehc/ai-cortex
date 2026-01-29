#!/usr/bin/env bash
# AI Cortex 安装脚本：同步 .cortex/ 与 AGENTS.md，可选注入 Bridges（GitHub Actions、Cursor 等）
# 用法：
#   curl -sL https://raw.githubusercontent.com/nesnilnehc/ai-cortex/main/scripts/install.sh | bash
#   curl -sL .../install.sh | bash -s -- [安装目录] [bridge...]
# 参数：第 1 个为安装目录（默认 .cortex）；后续为 bridge 名称：github-actions, cursor
# 环境变量：CORTEX_SOURCE（Raw 根 URL）、CORTEX_ROOT（安装目录）、CORTEX_BRIDGES（逗号分隔，如 github-actions,cursor）
# 未指定 bridge 且未设 CORTEX_BRIDGES 且为交互终端时，会询问是否注入各 bridge

set -e
set -o pipefail

INSTALL_ROOT="${1:-${CORTEX_ROOT:-.cortex}}"
shift || true
# 剩余参数为 bridge 列表
BRIDGE_ARGS=("$@")
BASE_URL="${CORTEX_SOURCE:-https://raw.githubusercontent.com/nesnilnehc/ai-cortex/main}"

if ! command -v jq &>/dev/null; then
  echo "❌ 需要 jq。请安装后重试：https://stedolan.github.io/jq/"
  exit 1
fi

echo "--- 🧠 AI Cortex: 导入到 [$INSTALL_ROOT]，来源 [$BASE_URL] ---"

mkdir -p "$INSTALL_ROOT"/{skills,rules,commands}
MANIFEST=$(curl -sfL "$BASE_URL/manifest.json") || { echo "❌ 无法获取 manifest.json，请检查网络或 BASE_URL：$BASE_URL"; exit 1; }
VERSION=$(echo "$MANIFEST" | jq -r '.version // "unknown"')

# 索引（失败则中止，避免静默部分安装）
for idx in skills/INDEX.md rules/INDEX.md commands/INDEX.md; do
  curl -sfL "$BASE_URL/$idx" -o "$INSTALL_ROOT/$idx" || { echo "❌ 获取 $idx 失败"; exit 1; }
done

# 技能（含 SKILL.md 与 tests/）
for name in $(echo "$MANIFEST" | jq -r '.capabilities[]?.name // empty'); do
  path=$(echo "$MANIFEST" | jq -r --arg n "$name" '.capabilities[] | select(.name==$n) | .path')
  test_path=$(echo "$MANIFEST" | jq -r --arg n "$name" '.capabilities[] | select(.name==$n) | .test_path // empty')
  mkdir -p "$INSTALL_ROOT/skills/$name"
  curl -sfL "$BASE_URL/$path" -o "$INSTALL_ROOT/skills/$name/SKILL.md" || { echo "❌ 获取技能 $name 失败"; exit 1; }
  if [ -n "$test_path" ]; then
    mkdir -p "$INSTALL_ROOT/skills/$name/tests"
    for f in assertions.md cases.json; do
      curl -sfL "$BASE_URL/$test_path$f" -o "$INSTALL_ROOT/skills/$name/tests/$f" 2>/dev/null || true
    done
  fi
done

# 规则
for path in $(echo "$MANIFEST" | jq -r '.rules[]?.path // empty'); do
  f=$(basename "$path")
  curl -sfL "$BASE_URL/$path" -o "$INSTALL_ROOT/rules/$f" || { echo "❌ 获取规则 $f 失败"; exit 1; }
done

# 命令
for path in $(echo "$MANIFEST" | jq -r '.commands[]?.path // empty'); do
  f=$(basename "$path")
  curl -sfL "$BASE_URL/$path" -o "$INSTALL_ROOT/commands/$f" || { echo "❌ 获取命令 $f 失败"; exit 1; }
done

# 消费方 config.json（使用 jq 转义，避免注入）
jq -n \
  --arg source "$BASE_URL" \
  --arg version "$VERSION" \
  --arg install_root "$INSTALL_ROOT" \
  '{source: $source, version: $version, mode: "auto", install_root: $install_root, assets: {skills: "*", rules: "*", commands: "*"}}' \
  > "$INSTALL_ROOT/config.json"

# 一步注入：写入 AGENTS.md（若当前目录无则创建）
AGENTS_URL="$BASE_URL/AGENTS.md"
if [ ! -f AGENTS.md ] || ! grep -q "AI Cortex" AGENTS.md 2>/dev/null; then
  curl -sfL "$AGENTS_URL" -o AGENTS.md || { echo "❌ 获取 AGENTS.md 失败"; exit 1; }
  echo "✅ 已写入 AGENTS.md（CORTEX_MODE=auto）"
fi

echo "✅ 核心导入完成：$INSTALL_ROOT/（version $VERSION）"

# --- Bridges：收集要注入的 bridge ---
BRIDGES=()
if [ ${#BRIDGE_ARGS[@]} -gt 0 ]; then
  BRIDGES=("${BRIDGE_ARGS[@]}")
elif [ -n "$CORTEX_BRIDGES" ]; then
  IFS=',' read -ra BRIDGES <<< "$CORTEX_BRIDGES"
elif [ -t 0 ]; then
  echo ""
  echo "--- 可选：注入 Bridges（与 IDE/CI 的同步与配置） ---"
  for name in github-actions cursor; do
    desc=""
    hint=""
    [ "$name" = "github-actions" ] && desc="GitHub Actions 定时同步规则到仓库"
    [ "$name" = "cursor" ] && desc="生成 .cursorrules 供 Cursor 使用"
    if [ "$name" = "github-actions" ] && { [ -d .git ] || [ -d .github ]; }; then
      hint=" [检测到 Git/ GitHub 仓库，建议注入]"
    fi
    if [ "$name" = "cursor" ] && { [ -d .cursor ] || [ -f .cursorrules ]; }; then
      hint=" [检测到 Cursor 相关配置，建议注入]"
    fi
    printf "  是否注入 %s (%s)?%s [y/N] " "$name" "$desc" "$hint"
    read -r ans
    case "${ans,,}" in
      y|yes) BRIDGES+=("$name") ;;
    esac
  done
fi

# --- 注入各 bridge ---
for bridge in "${BRIDGES[@]}"; do
  case "$bridge" in
    github-actions)
      mkdir -p .github/workflows
      curl -sfL "$BASE_URL/bridges/github-actions/sync-template.yml" | \
        sed "s|https://raw.githubusercontent.com/nesnilnehc/ai-cortex/main|$BASE_URL|g" \
        > .github/workflows/ai-cortex-sync.yml
      echo "✅ 已注入 GitHub Actions：.github/workflows/ai-cortex-sync.yml"
      ;;
    cursor)
      SYNC_SH=$(curl -sfL "$BASE_URL/scripts/sync.sh") || { echo "❌ 获取 sync.sh 失败"; exit 1; }
      echo "$SYNC_SH" | bash -s -- cursor "$BASE_URL"
      echo "✅ 已注入 Cursor：.cursorrules"
      ;;
    *)
      echo "⚠️ 未知 bridge: $bridge（已跳过）"
      ;;
  esac
done

echo ""
echo "   后续：Agent 将优先读取 $INSTALL_ROOT/skills/INDEX.md 与 $INSTALL_ROOT/rules/INDEX.md"
