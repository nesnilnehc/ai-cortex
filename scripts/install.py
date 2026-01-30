#!/usr/bin/env python3
"""
Install AI Cortex Cursor/TRAE assets into a project or user environment.

This script installs from the generated outputs in this repo:
  - .cursor/**
  - .trae/**

It writes an install manifest to ensure uninstall is safe and reversible.
Re-installing with a different preset does not remove files from a previous
install; for a clean state, run uninstall then install.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import ssl
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path
from typing import Dict, List, Literal, Optional, Tuple
from urllib.request import urlopen

REPO_ARCHIVE_URL = "https://github.com/nesnilnehc/ai-cortex/archive/refs/heads/main.zip"
ARCHIVE_TOP_DIR = "ai-cortex-main"


Target = Literal["cursor", "trae"]
Scope = Literal["project", "user"]
Preset = Literal["full", "user-recommended", "project-recommended"]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def copy_file(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_bytes(src.read_bytes())


def load_json(path: Path) -> Dict:
    return json.loads(read_text(path))


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def normalize_recommended_scope(v: Optional[str]) -> str:
    vv = (v or "").strip().strip('"').strip("'").lower()
    if vv in {"user", "project", "both"}:
        return vv
    return "both"


def _looks_like_repo(path: Path) -> bool:
    """True if path has scripts/install.py (repo root)."""
    return (path / "scripts" / "install.py").exists()


def _ssl_context() -> ssl.SSLContext:
    """Build SSL context with default certs; on macOS, optionally use certifi if available."""
    ctx = ssl.create_default_context()
    try:
        import certifi
        ctx.load_verify_locations(certifi.where())
    except ImportError:
        pass
    return ctx


def _download_and_extract_repo() -> Path:
    """Download repo zip from GitHub and extract to a temp dir; return repo root path."""
    tmp = Path(tempfile.mkdtemp(prefix="ai-cortex-"))
    try:
        zip_path = tmp / "main.zip"
        with urlopen(REPO_ARCHIVE_URL, context=_ssl_context()) as resp:
            zip_path.write_bytes(resp.read())
        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(tmp)
        repo_root = tmp / ARCHIVE_TOP_DIR
        if not repo_root.exists():
            raise RuntimeError(f"Archive missing top dir {ARCHIVE_TOP_DIR}")
        return repo_root
    except OSError as e:
        import shutil
        if tmp.exists():
            shutil.rmtree(tmp, ignore_errors=True)
        if "CERTIFICATE_VERIFY_FAILED" in str(e) or "certificate" in str(e).lower():
            raise RuntimeError(
                "HTTPS certificate verification failed. On macOS with Python from python.org, "
                "run the 'Install Certificates.command' from your Python folder, or install certifi: "
                "pip install certifi"
            ) from e
        raise
    except Exception:
        import shutil
        if tmp.exists():
            shutil.rmtree(tmp, ignore_errors=True)
        raise


def ensure_generated(repo_root: Path, no_generate: bool) -> None:
    """
    Ensure .cursor/.trae are present by running sync script if needed.
    When no_generate is True, skip generation and require metadata to exist (e.g. install from tarball).
    """
    cursor_meta = repo_root / ".cursor" / ".ai-cortex-metadata.json"
    trae_meta = repo_root / ".trae" / ".ai-cortex-metadata.json"
    if cursor_meta.exists() and trae_meta.exists():
        return
    if no_generate:
        raise RuntimeError(
            "Missing .cursor/.trae metadata. Run without --no-generate from a writable clone, "
            "or use a release that includes pre-generated .cursor/.trae."
        )

    sync_script = repo_root / "scripts" / "sync_ide_assets.py"
    if not sync_script.exists():
        raise RuntimeError(f"Missing generator script: {sync_script}")

    subprocess.check_call(
        [sys.executable, str(sync_script), "--repo-root", str(repo_root)],
        cwd=repo_root,
    )


def load_metadata(repo_root: Path, target: Target) -> Dict[str, Dict[str, Dict[str, str]]]:
    meta_path = repo_root / f".{target}" / ".ai-cortex-metadata.json"
    if not meta_path.exists():
        raise RuntimeError(f"Missing metadata file: {meta_path}")
    return load_json(meta_path)


def preset_allows(preset: Preset, recommended_scope: str) -> bool:
    rs = normalize_recommended_scope(recommended_scope)
    if preset == "full":
        return True
    if preset == "user-recommended":
        return rs in {"user", "both"}
    if preset == "project-recommended":
        return rs in {"project", "both"}
    return True


def iter_selected_assets(
    metadata: Dict[str, Dict[str, Dict[str, str]]], preset: Preset
) -> Tuple[List[str], List[str], List[str]]:
    rules = [k for k, v in metadata.get("rules", {}).items() if preset_allows(preset, v.get("recommended_scope"))]
    commands = [
        k for k, v in metadata.get("commands", {}).items() if preset_allows(preset, v.get("recommended_scope"))
    ]
    skills = [k for k, v in metadata.get("skills", {}).items() if preset_allows(preset, v.get("recommended_scope"))]
    return sorted(rules), sorted(commands), sorted(skills)


def cursor_user_rules_bundle(repo_root: Path, selected_rule_names: List[str]) -> str:
    """
    Cursor user rules live in Settings UI, not in filesystem.
    We generate a bundle file for copy-paste.
    """
    parts: List[str] = []
    parts.append("# AI Cortex 用户规则（复制粘贴到 Cursor User Rules）\n")
    parts.append(
        "说明：Cursor 的 User Rules 需要在 `Cursor Settings → Rules` 中粘贴配置。\n"
        "本文件由 AI Cortex 安装脚本生成；如需更新，重新运行 install 即可。\n\n"
    )
    for name in selected_rule_names:
        rule_path = repo_root / "rules" / f"{name}.md"
        if not rule_path.exists():
            continue
        raw = read_text(rule_path)
        # Drop frontmatter if present (find second line that is exactly "---")
        lines = raw.splitlines(keepends=True)
        if lines and lines[0].strip() == "---":
            for i in range(1, len(lines)):
                if lines[i].strip() == "---":
                    raw = "".join(lines[i + 1 :]).lstrip("\n")
                    break
        parts.append(f"\n---\n\n## {name}\n\n")
        parts.append(raw.strip() + "\n")
    return "".join(parts)


def resolve_dest_base(target: Target, scope: Scope, project_dir: Optional[Path]) -> Path:
    if scope == "project":
        base = (project_dir or Path.cwd()).resolve()
        return base / f".{target}"
    # user
    return Path.home().resolve() / f".{target}"


def _install_to_dest(
    repo_root: Path,
    target: Target,
    dest_base: Path,
    scope: Scope,
    rule_names: List[str],
    command_names: List[str],
    skill_names: List[str],
    preset: Preset,
) -> None:
    """Copy selected assets to dest_base and write install manifest. Used by install() and interactive flow."""
    src_root = repo_root / f".{target}"
    installed_files: List[str] = []

    if scope == "user" and target == "cursor":
        bundle_dir = dest_base / "ai-cortex"
        bundle_path = bundle_dir / "user-rules.md"
        write_text(bundle_path, cursor_user_rules_bundle(repo_root, rule_names))
        installed_files.append(str(bundle_path.relative_to(dest_base)))
        for name in rule_names:
            src = src_root / "rules" / f"{name}.mdc"
            if not src.exists():
                continue
            dst = bundle_dir / "rules" / f"{name}.mdc"
            copy_file(src, dst)
            installed_files.append(str(dst.relative_to(dest_base)))
    else:
        for name in rule_names:
            src = src_root / "rules" / f"{name}.mdc"
            if not src.exists():
                continue
            dst = dest_base / "rules" / f"{name}.mdc"
            copy_file(src, dst)
            installed_files.append(str(dst.relative_to(dest_base)))

    for name in command_names:
        src = src_root / "commands" / f"{name}.md"
        if not src.exists():
            continue
        dst = dest_base / "commands" / f"{name}.md"
        copy_file(src, dst)
        installed_files.append(str(dst.relative_to(dest_base)))

    for name in skill_names:
        src = src_root / "skills" / name / "SKILL.md"
        if not src.exists():
            continue
        dst = dest_base / "skills" / name / "SKILL.md"
        copy_file(src, dst)
        installed_files.append(str(dst.relative_to(dest_base)))

    manifest_path = dest_base / ".ai-cortex-install-manifest.json"
    manifest = {
        "managed_by": "ai-cortex",
        "target": target,
        "scope": scope,
        "preset": preset,
        "installed_at": now_iso(),
        "repo_root": str(repo_root),
        "dest_base": str(dest_base),
        "files": sorted(set(installed_files + [str(manifest_path.relative_to(dest_base))])),
        "notes": (
            "Cursor user rules are not file-based; see ai-cortex/user-rules.md for copy-paste."
            if (scope == "user" and target == "cursor")
            else ""
        ),
    }
    write_text(manifest_path, json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")

    print(f"Installed {len(manifest['files'])} files into: {dest_base}")
    if scope == "user" and target == "cursor":
        print(f"  Cursor User Rules bundle: {dest_base / 'ai-cortex' / 'user-rules.md'}")


def _prompt(text: str, default: str) -> str:
    """Prompt and return one char; empty input returns default."""
    raw = input(text).strip().lower()
    return raw if raw else default


def _interactive_install(
    repo_root: Path,
    target: Target,
    metadata: Dict[str, Dict[str, Dict[str, str]]],
    no_generate: bool,
) -> None:
    """Interactive: ask default vs per-asset, then install."""
    print("1) 使用默认（按本项目推荐的 scope 与预设安装）")
    print("2) 逐项确认（每项有默认建议）")
    mode = _prompt("请选择 [1/2] (1): ", "1")

    if mode == "1":
        scope_choice = _prompt("安装到 (u)ser 全局 / (p)roject 项目? [p]: ", "p")
        scope: Scope = "user" if scope_choice == "u" else "project"
        preset: Preset = "user-recommended" if scope == "user" else "full"
        project_dir: Optional[Path] = None
        if scope == "project":
            pd = input("项目目录 (留空=当前目录): ").strip()
            project_dir = Path(pd).resolve() if pd else None
            if project_dir is not None and (not project_dir.exists() or not project_dir.is_dir()):
                print(f"错误：项目目录不存在或不是目录: {project_dir}", file=sys.stderr)
                sys.exit(1)
        install(
            repo_root=repo_root,
            target=target,
            scope=scope,
            preset=preset,
            project_dir=project_dir,
            no_generate=no_generate,
        )
        return

    # Mode 2: per-asset
    rec_short = {"user": "u", "project": "p", "both": "b"}
    user_rules: List[str] = []
    user_commands: List[str] = []
    user_skills: List[str] = []
    project_rules: List[str] = []
    project_commands: List[str] = []
    project_skills: List[str] = []

    def ask(kind: str, name: str, rec: str) -> str:
        default = rec_short.get(normalize_recommended_scope(rec), "b")
        prompt = f"  {kind} '{name}' (推荐: {rec}) → (u)ser/(p)roject/(b)oth/(s)kip? [{default}]: "
        return _prompt(prompt, default)

    for name, info in sorted(metadata.get("rules", {}).items()):
        rec = info.get("recommended_scope") or "both"
        c = ask("rule", name, rec)
        if c == "u":
            user_rules.append(name)
        elif c == "p":
            project_rules.append(name)
        elif c == "b":
            user_rules.append(name)
            project_rules.append(name)
        # s: skip

    for name, info in sorted(metadata.get("commands", {}).items()):
        rec = info.get("recommended_scope") or "both"
        c = ask("command", name, rec)
        if c == "u":
            user_commands.append(name)
        elif c == "p":
            project_commands.append(name)
        elif c == "b":
            user_commands.append(name)
            project_commands.append(name)

    for name, info in sorted(metadata.get("skills", {}).items()):
        rec = info.get("recommended_scope") or "both"
        c = ask("skill", name, rec)
        if c == "u":
            user_skills.append(name)
        elif c == "p":
            project_skills.append(name)
        elif c == "b":
            user_skills.append(name)
            project_skills.append(name)

    project_dir = None
    if project_rules or project_commands or project_skills:
        pd = input("项目目录（用于 project/both）(留空=当前目录): ").strip()
        project_dir = Path(pd).resolve() if pd else None
        if project_dir is not None and (not project_dir.exists() or not project_dir.is_dir()):
            print(f"错误：项目目录不存在或不是目录: {project_dir}", file=sys.stderr)
            sys.exit(1)

    if user_rules or user_commands or user_skills:
        dest_user = resolve_dest_base(target, "user", None)
        _install_to_dest(
            repo_root, target, dest_user, "user",
            user_rules, user_commands, user_skills, "full",
        )
    if project_rules or project_commands or project_skills:
        dest_proj = resolve_dest_base(target, "project", project_dir)
        _install_to_dest(
            repo_root, target, dest_proj, "project",
            project_rules, project_commands, project_skills, "full",
        )
    if not (user_rules or user_commands or user_skills or project_rules or project_commands or project_skills):
        print("未选择任何资产，跳过安装。")
    else:
        print("安装完成。")
        if target == "cursor" and (user_rules or user_commands or user_skills):
            print(f"  Cursor 用户级 manifest: {Path.home() / f'.{target}' / '.ai-cortex-install-manifest.json'}")


def install(
    repo_root: Path,
    target: Target,
    scope: Scope,
    preset: Preset,
    project_dir: Optional[Path],
    no_generate: bool,
) -> None:
    ensure_generated(repo_root, no_generate=no_generate)
    metadata = load_metadata(repo_root, target)
    rule_names, command_names, skill_names = iter_selected_assets(metadata, preset)
    dest_base = resolve_dest_base(target, scope, project_dir)
    _install_to_dest(
        repo_root, target, dest_base, scope,
        rule_names, command_names, skill_names, preset,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Install AI Cortex assets into Cursor/TRAE.")
    parser.add_argument("--target", choices=["cursor", "trae"], default="cursor")
    parser.add_argument(
        "--scope",
        choices=["project", "user"],
        default=None,
        help="Where to install (default: none = interactive). Set to skip interactive.",
    )
    parser.add_argument(
        "--preset",
        choices=["full", "user-recommended", "project-recommended"],
        default=None,
        help="Which assets to install (default: none = interactive). Set to skip interactive.",
    )
    parser.add_argument(
        "--repo-root",
        default=None,
        help="Path to ai-cortex repo root (defaults to parent of this script).",
    )
    parser.add_argument(
        "--project-dir",
        default=None,
        help="Project directory to install into (only for --scope project; defaults to CWD).",
    )
    parser.add_argument(
        "--no-generate",
        action="store_true",
        help="Do not run sync script; require .cursor/.trae to exist (e.g. install from tarball).",
    )
    args = parser.parse_args()

    if args.repo_root is not None and not args.repo_root.strip():
        parser.error("--repo-root must be non-empty")
    if args.repo_root:
        repo_root = Path(args.repo_root).resolve()
    else:
        try:
            repo_root = Path(__file__).resolve().parents[1]
        except NameError:
            repo_root = None
        if repo_root is None or not _looks_like_repo(repo_root):
            print("No local repo found; downloading from GitHub...", file=sys.stderr)
            repo_root = _download_and_extract_repo()
    project_dir = Path(args.project_dir).resolve() if args.project_dir else None
    if project_dir is not None and (not project_dir.exists() or not project_dir.is_dir()):
        parser.error(f"--project-dir must be an existing directory: {project_dir}")

    # No --scope and no --preset → interactive (choose default or per-asset)
    if args.scope is None and args.preset is None:
        ensure_generated(repo_root, no_generate=args.no_generate)
        _interactive_install(
            repo_root=repo_root,
            target=args.target,  # type: ignore[arg-type]
            metadata=load_metadata(repo_root, args.target),  # type: ignore[arg-type]
            no_generate=args.no_generate,
        )
        return

    install(
        repo_root=repo_root,
        target=args.target,  # type: ignore[arg-type]
        scope=args.scope or "project",
        preset=args.preset or "full",
        project_dir=project_dir,
        no_generate=args.no_generate,
    )


if __name__ == "__main__":
    main()

