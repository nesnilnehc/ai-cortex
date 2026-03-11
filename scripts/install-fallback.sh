#!/usr/bin/env bash
set -euo pipefail

repo="nesnilnehc/ai-cortex"
ref="main"
dest=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo)
      repo="${2:-}"
      shift 2
      ;;
    --ref)
      ref="${2:-}"
      shift 2
      ;;
    --dest)
      dest="${2:-}"
      shift 2
      ;;
    *)
      echo "Unsupported argument: $1" >&2
      exit 1
      ;;
  esac
done

if [[ -z "$dest" ]]; then
  echo "Missing required argument: --dest <directory>" >&2
  exit 1
fi

tmp_dir="$(mktemp -d)"
trap 'rm -rf "$tmp_dir"' EXIT

archive_url="https://codeload.github.com/${repo}/tar.gz/${ref}"
curl -fsSL "$archive_url" | tar -xz -C "$tmp_dir"

source_root="$(find "$tmp_dir" -mindepth 1 -maxdepth 1 -type d | head -n 1)"
if [[ -z "$source_root" ]]; then
  echo "Failed to resolve extracted repository directory." >&2
  exit 1
fi

mkdir -p "$dest"

for path in AGENTS.md README.md llms.txt manifest.json skills rules spec; do
  if [[ -e "${source_root}/${path}" ]]; then
    cp -R "${source_root}/${path}" "${dest}/"
  fi
done

echo "Installed AI Cortex fallback package to: ${dest}"
