#!/usr/bin/env python3
"""
Uninstall AI Cortex Cursor/TRAE assets using the install manifest.

Safety:
  - Only deletes files listed in the manifest.
  - Supports --dry-run.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Literal, Optional


Target = Literal["cursor", "trae"]
Scope = Literal["project", "user"]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> Dict:
    return json.loads(read_text(path))


def resolve_dest_base(target: Target, scope: Scope, project_dir: Optional[Path]) -> Path:
    if scope == "project":
        base = (project_dir or Path.cwd()).resolve()
        return base / f".{target}"
    return Path.home().resolve() / f".{target}"


def remove_empty_parents(path: Path, stop_at: Path) -> None:
    """
    Remove empty directories upward until stop_at (inclusive boundary; not removed).
    """
    cur = path
    while True:
        if cur == stop_at:
            return
        if not cur.exists() or not cur.is_dir():
            cur = cur.parent
            continue
        try:
            next(cur.iterdir())
            return
        except StopIteration:
            cur.rmdir()
            cur = cur.parent


def uninstall(dest_base: Path, target: Target, dry_run: bool) -> None:
    manifest_path = dest_base / ".ai-cortex-install-manifest.json"
    if not manifest_path.exists():
        raise RuntimeError(f"Install manifest not found: {manifest_path}")

    manifest = load_json(manifest_path)
    if manifest.get("managed_by") != "ai-cortex":
        raise RuntimeError("Refusing to uninstall: manifest missing managed_by=ai-cortex")
    if manifest.get("target") != target:
        raise RuntimeError(f"Refusing to uninstall: manifest target mismatch (expected {target})")

    files: List[str] = list(manifest.get("files") or [])
    if not files:
        print("Warning: manifest has no 'files' list; nothing to remove (manifest left in place).", file=sys.stderr)
        return
    # Delete children before parents by sorting longest first.
    files_sorted = sorted(set(files), key=lambda p: (-len(p), p))

    to_delete = [dest_base / f for f in files_sorted]

    if dry_run:
        print("Dry-run: would delete:")
        for p in to_delete:
            print(f"  - {p}")
        return

    deleted = 0
    for p in to_delete:
        if not p.exists():
            continue
        if p.is_dir():
            # Manifest should only include files, but guard anyway.
            continue
        p.unlink()
        deleted += 1

    # Cleanup empty directories within dest_base
    for p in to_delete:
        remove_empty_parents(p.parent, stop_at=dest_base)

    print(f"Deleted {deleted} files from: {dest_base}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Uninstall AI Cortex assets from Cursor/TRAE.")
    parser.add_argument("--target", choices=["cursor", "trae"], default="cursor")
    parser.add_argument(
        "--scope",
        choices=["project", "user"],
        default="project",
        help="Must match install scope (default: project = current or --project-dir).",
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--project-dir",
        default=None,
        help="Project directory to uninstall from (only for --scope project; defaults to CWD).",
    )
    args = parser.parse_args()

    project_dir = Path(args.project_dir).resolve() if args.project_dir else None
    if args.scope == "project" and project_dir is not None and (not project_dir.exists() or not project_dir.is_dir()):
        parser.error(f"--project-dir must be an existing directory: {project_dir}")
    dest_base = resolve_dest_base(args.target, args.scope, project_dir)  # type: ignore[arg-type]
    uninstall(dest_base, args.target, args.dry_run)  # type: ignore[arg-type]


if __name__ == "__main__":
    main()

