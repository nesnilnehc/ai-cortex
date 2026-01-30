#!/usr/bin/env python3
"""
Generate Cursor/TRAE consumable assets from AI Cortex sources.

Outputs:
  - .cursor/rules/*.mdc
  - .cursor/commands/*.md
  - .cursor/skills/*/SKILL.md
  - .trae/rules/*.mdc
  - .trae/commands/*.md
  - .trae/skills/*/SKILL.md

Design goals:
  - Single source of truth: rules/, commands/, skills/
  - Minimal dependencies (stdlib only)
  - Deterministic output (stable formatting)

Rule glob/scope mapping (cursor_rule_globs):
  - Explicit: documentation-markdown-format, workflow-documentation → **/*.md;
    standards-shell → **/*.sh.
  - Fallback: rule frontmatter "scope" text containing ".md" → **/*.md;
    ".sh" or "*.sh" → **/*.sh. New rules with other scope text get no globs
    unless added to the explicit map or the heuristic.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple


RE_FRONTMATTER_BOUNDARY = re.compile(r"^---\s*$")
RE_KV_LINE = re.compile(r"^(?P<key>[A-Za-z0-9_-]+)\s*:\s*(?P<value>.*)$")
RE_RULE_TITLE = re.compile(r"^#\s+Rule:\s+(?P<title>.+?)\s*$")


@dataclass(frozen=True)
class Frontmatter:
    raw: str
    data: Dict[str, str]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def split_frontmatter(md: str) -> Tuple[Optional[Frontmatter], str]:
    """
    If md starts with a YAML-ish frontmatter block delimited by ---,
    returns (frontmatter, body_without_frontmatter). Otherwise (None, md).

    Note: we only parse simple `key: value` lines; values remain raw strings.
    """
    lines = md.splitlines(keepends=True)
    if not lines or not RE_FRONTMATTER_BOUNDARY.match(lines[0]):
        return None, md

    end_idx = None
    for i in range(1, len(lines)):
        if RE_FRONTMATTER_BOUNDARY.match(lines[i]):
            end_idx = i
            break
    if end_idx is None:
        return None, md

    fm_lines = lines[1:end_idx]
    fm_raw = "".join(fm_lines).strip("\n")
    data: Dict[str, str] = {}
    for ln in fm_lines:
        m = RE_KV_LINE.match(ln.strip())
        if not m:
            continue
        data[m.group("key")] = m.group("value").strip()
    body = "".join(lines[end_idx + 1 :]).lstrip("\n")
    return Frontmatter(raw=fm_raw, data=data), body


def extract_rule_title(rule_body: str, fallback_name: str) -> str:
    for ln in rule_body.splitlines():
        m = RE_RULE_TITLE.match(ln.strip())
        if m:
            return m.group("title").strip()
    return fallback_name


def cursor_rule_globs(rule_name: str, rule_fm: Optional[Frontmatter]) -> List[str]:
    # Conservative mapping: only set globs when clearly file-scoped.
    if rule_name in {"documentation-markdown-format", "workflow-documentation"}:
        return ["**/*.md"]
    if rule_name == "standards-shell":
        return ["**/*.sh"]

    # Fallback heuristic based on scope text.
    scope = (rule_fm.data.get("scope") if rule_fm else "") or ""
    if ".md" in scope:
        return ["**/*.md"]
    if ".sh" in scope or "*.sh" in scope:
        return ["**/*.sh"]
    return []


def cursor_rule_always_apply(rule_name: str) -> bool:
    # Keep MVP conservative: default to intelligently applied rules.
    # Users can flip to alwaysApply in Cursor UI if desired.
    return False


def normalize_recommended_scope(value: Optional[str]) -> str:
    v = (value or "").strip().strip('"').strip("'").lower()
    if v in {"user", "project", "both"}:
        return v
    return "both"


def build_rule_mdc(repo_root: Path, rule_src_path: Path) -> str:
    src_text = read_text(rule_src_path)
    fm, body = split_frontmatter(src_text)
    rule_name = rule_src_path.stem
    title = extract_rule_title(body, fallback_name=rule_name)

    recommended_scope = normalize_recommended_scope(fm.data.get("recommended_scope") if fm else None)
    globs = cursor_rule_globs(rule_name, fm)
    always_apply = cursor_rule_always_apply(rule_name)

    try:
        source_rel = rule_src_path.relative_to(repo_root).as_posix()
    except ValueError:
        source_rel = rule_src_path.as_posix()

    # YAML frontmatter for Cursor/Trae project rules.
    desc_text = f"AI Cortex rule: {title}"
    fm_out_lines: List[str] = [
        "---",
        f"description: {json.dumps(desc_text, ensure_ascii=False)}",
    ]
    if globs:
        fm_out_lines.append("globs:")
        for g in globs:
            fm_out_lines.append(f"  - {json.dumps(g)}")
    fm_out_lines.append(f"alwaysApply: {str(always_apply).lower()}")
    fm_out_lines.append(f"recommended_scope: {recommended_scope}")
    fm_out_lines.append("managed_by: ai-cortex")
    fm_out_lines.append(f"source: {json.dumps(source_rel)}")
    fm_out_lines.append("---")

    header = "\n".join(fm_out_lines) + "\n\n"
    return header + body.rstrip() + "\n"


def build_cursor_command_md(command_src_path: Path) -> str:
    src_text = read_text(command_src_path)
    fm, body = split_frontmatter(src_text)
    name = (fm.data.get("name") if fm else None) or command_src_path.stem
    recommended_scope = normalize_recommended_scope(fm.data.get("recommended_scope") if fm else None)

    # MVP: single command supported today. Keep structure stable and concise.
    # For future commands, this can be upgraded to parse sections.
    if name == "readme":
        return (
            "# /readme\n\n"
            "生成或重写当前项目的根目录 `README.md`。\n\n"
            "## 执行要点\n\n"
            "- 调用技能：`generate-standard-readme`\n"
            "- 参数：`/readme [lang]`（默认 `lang=zh`）\n"
            f"- recommended_scope：`{recommended_scope}`\n"
        )

    return (
        f"# /{name}\n\n"
        "执行此命令描述的工作流。\n\n"
        f"- recommended_scope：`{recommended_scope}`\n\n"
        "## 原始说明（来自 AI Cortex）\n\n"
        + body.rstrip()
        + "\n"
    )


def copy_skill(skill_dir: Path, dest_dir: Path) -> List[Path]:
    """
    Copy skill SKILL.md only (tests excluded).
    Returns list of written files.
    """
    written: List[Path] = []
    src_skill = skill_dir / "SKILL.md"
    if not src_skill.exists():
        return written
    dest_skill = dest_dir / "SKILL.md"
    dest_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src_skill, dest_skill)
    written.append(dest_skill)
    return written


def list_skills_root(skills_root: Path) -> List[Path]:
    out: List[Path] = []
    for p in sorted(skills_root.iterdir()):
        if not p.is_dir():
            continue
        if p.name.startswith("."):
            continue
        if p.name in {"tests", "__pycache__"}:
            continue
        if (p / "SKILL.md").exists():
            out.append(p)
    return out


def list_rules(rules_root: Path) -> List[Path]:
    return sorted([p for p in rules_root.glob("*.md") if p.name != "INDEX.md"])


def list_commands(commands_root: Path) -> List[Path]:
    return sorted([p for p in commands_root.glob("*.md") if p.name != "INDEX.md"])


def clean_generated_root(root_dir: Path) -> None:
    """
    Remove previously generated content under root_dir, keeping the root dir itself.
    """
    if not root_dir.exists():
        return
    for child in root_dir.iterdir():
        # We only manage these subtrees.
        if child.name in {"rules", "commands", "skills"}:
            if child.is_dir():
                shutil.rmtree(child)
            else:
                child.unlink()


def generate(repo_root: Path) -> Dict[str, List[str]]:
    rules_root = repo_root / "rules"
    commands_root = repo_root / "commands"
    skills_root = repo_root / "skills"

    cursor_root = repo_root / ".cursor"
    trae_root = repo_root / ".trae"

    # Clear previous generated content (idempotent)
    cursor_root.mkdir(parents=True, exist_ok=True)
    trae_root.mkdir(parents=True, exist_ok=True)
    clean_generated_root(cursor_root)
    clean_generated_root(trae_root)

    written: Dict[str, List[str]] = {"cursor": [], "trae": []}

    metadata: Dict[str, Dict[str, Dict[str, str]]] = {
        "rules": {},
        "commands": {},
        "skills": {},
    }

    # Rules
    for rule_src in list_rules(rules_root):
        src_text = read_text(rule_src)
        src_fm, _ = split_frontmatter(src_text)
        metadata["rules"][rule_src.stem] = {
            "recommended_scope": normalize_recommended_scope(
                (src_fm.data.get("recommended_scope") if src_fm else None)
            )
        }

        mdc = build_rule_mdc(repo_root, rule_src)
        rel = Path("rules") / f"{rule_src.stem}.mdc"
        for target, root in (("cursor", cursor_root), ("trae", trae_root)):
            out_path = root / rel
            write_text(out_path, mdc)
            written[target].append(str(out_path.relative_to(repo_root)))

    # Commands
    for cmd_src in list_commands(commands_root):
        src_text = read_text(cmd_src)
        src_fm, _ = split_frontmatter(src_text)
        metadata["commands"][cmd_src.stem] = {
            "recommended_scope": normalize_recommended_scope(
                (src_fm.data.get("recommended_scope") if src_fm else None)
            )
        }

        md = build_cursor_command_md(cmd_src)
        rel = Path("commands") / cmd_src.name
        for target, root in (("cursor", cursor_root), ("trae", trae_root)):
            out_path = root / rel
            write_text(out_path, md)
            written[target].append(str(out_path.relative_to(repo_root)))

    # Skills
    for skill_dir in list_skills_root(skills_root):
        rel_dir = Path("skills") / skill_dir.name
        src_text = read_text(skill_dir / "SKILL.md")
        src_fm, _ = split_frontmatter(src_text)
        metadata["skills"][skill_dir.name] = {
            "recommended_scope": normalize_recommended_scope(
                (src_fm.data.get("recommended_scope") if src_fm else None)
            )
        }
        for target, root in (("cursor", cursor_root), ("trae", trae_root)):
            dest_dir = root / rel_dir
            for f in copy_skill(skill_dir, dest_dir):
                written[target].append(str(f.relative_to(repo_root)))

    # Product manifest (helps debugging; install manifest is written by installer)
    for target, root in (("cursor", cursor_root), ("trae", trae_root)):
        meta_path = root / ".ai-cortex-metadata.json"
        write_text(meta_path, json.dumps(metadata, ensure_ascii=False, indent=2) + "\n")
        written[target].append(str(meta_path.relative_to(repo_root)))

        manifest_path = root / ".ai-cortex-product-manifest.json"
        payload = {
            "managed_by": "ai-cortex",
            "target": target,
            "repo_root": str(repo_root),
            "files": sorted(written[target]),
        }
        write_text(manifest_path, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
        written[target].append(str(manifest_path.relative_to(repo_root)))

    return written


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate .cursor/ and .trae/ assets.")
    parser.add_argument(
        "--repo-root",
        default=None,
        help="Path to ai-cortex repo root (defaults to parent of this script).",
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve() if args.repo_root else Path(__file__).resolve().parents[1]
    written = generate(repo_root)
    print(json.dumps(written, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

