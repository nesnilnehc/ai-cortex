#!/usr/bin/env python3
"""Render skills/INDEX.md from the SKILL.md frontmatter of every skill.

AGENTS.md §4 resolves a skill by ranking `triggers`, then `tags`, then
`description` — all three read from skills/INDEX.md. The registry therefore has
to carry those three fields and has to agree with the skills it registers, so it
is derived here rather than maintained by hand.
"""

from __future__ import annotations

import pathlib
import re
import sys


ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
INDEX = SKILLS_DIR / "INDEX.md"

USAGE = """usage:
  scripts/sync-skills-index.py            rewrite the registry
  scripts/sync-skills-index.py --check    fail when it is out of date"""

HEADER = """# Skills

Generated from each skill's own `SKILL.md` frontmatter by
`scripts/sync-skills-index.py`. Edit the skill, then regenerate — an edit made
here alone is overwritten and does not reach the skill.
"""

REGISTRY_FIELDS = ("name", "description", "tags", "triggers")
LIST_FIELDS = ("tags", "triggers")
SCALAR = re.compile(r"^(name|description):\s*(.+?)\s*$", re.M)
FLOW_LIST = re.compile(r"^(tags|triggers):\s*\[(.*?)\]\s*$", re.M)


class SkillError(Exception):
    """A skill cannot supply the fields the registry is built from."""


def read_frontmatter(skill_md: pathlib.Path) -> dict[str, object]:
    """Return the registry fields declared by one SKILL.md.

    skill_md: path to a skill's SKILL.md
    Returns: dict with `name` and `description` as str, `tags` and `triggers`
        as list[str]
    Raises: SkillError when a field is absent or not written as a flow list
    """
    text = skill_md.read_text(encoding="utf-8")
    if not text.startswith("---"):
        raise SkillError(f"{relative(skill_md)}: no frontmatter block")
    block = text.split("---", 2)[1]

    fields: dict[str, object] = {
        key: value.strip("\"'") for key, value in SCALAR.findall(block)
    }
    for key, raw in FLOW_LIST.findall(block):
        fields[key] = [
            item.strip().strip("\"'") for item in raw.split(",") if item.strip()
        ]

    for key in REGISTRY_FIELDS:
        if not fields.get(key):
            raise SkillError(f"{relative(skill_md)}: {absence_reason(key, block)}")
    return fields


def absence_reason(key: str, block: str) -> str:
    """Explain why a required field did not parse.

    A list written in block form parses as absent, and reporting it as missing
    sends the author looking for a field that is already there.
    """
    declared = re.search(rf"^{key}:", block, re.M)
    if key in LIST_FIELDS and declared:
        return (
            f"`{key}` must be a flow list on one line, "
            f"for example `{key}: [first, second]`"
        )
    return f"frontmatter is missing `{key}`"


def collect(skills_dir: pathlib.Path) -> list[tuple[str, dict[str, object]]]:
    """Return (directory name, registry fields) for every skill, sorted by name.

    skills_dir: directory holding one subdirectory per skill
    Returns: list of pairs in directory-name order
    Raises: SkillError when a directory has no SKILL.md, or when its declared
        name disagrees with the directory it lives in
    """
    skills: list[tuple[str, dict[str, object]]] = []
    for skill_dir in sorted(p for p in skills_dir.iterdir() if p.is_dir()):
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            raise SkillError(f"{relative(skill_dir)}: directory has no SKILL.md")
        fields = read_frontmatter(skill_md)
        if fields["name"] != skill_dir.name:
            raise SkillError(
                f"{relative(skill_md)}: frontmatter name `{fields['name']}` "
                f"does not match directory `{skill_dir.name}`"
            )
        skills.append((skill_dir.name, fields))
    return skills


def render(skills: list[tuple[str, dict[str, object]]]) -> str:
    """Return the full INDEX.md text for the given skills."""
    lines = [HEADER]
    for name, fields in skills:
        lines.append(f"- [{name}](./{name}/SKILL.md) — {fields['description']}")
        lines.append(
            f"  - tags: {code_list(fields['tags'])}"
            f" · triggers: {code_list(fields['triggers'])}"
        )
    return "\n".join(lines) + "\n"


def code_list(values: list[str]) -> str:
    """Render a list as backticked, comma-separated values."""
    return ", ".join(f"`{value}`" for value in values)


def relative(path: pathlib.Path) -> str:
    """Path relative to the repository root, or absolute when it lies outside."""
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def main(argv: list[str]) -> int:
    check_only = False
    for argument in argv:
        if argument == "--check":
            check_only = True
            continue
        # Falling through to the write branch on an unrecognised argument would
        # turn the CI gate into a silent no-op that still reports success.
        print(f"error: unknown argument `{argument}`\n{USAGE}", file=sys.stderr)
        return 2

    try:
        skills = collect(SKILLS_DIR)
    except SkillError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    rendered = render(skills)
    if check_only:
        if INDEX.read_text(encoding="utf-8") != rendered:
            print(
                "error: skills/INDEX.md is out of date — run "
                "`python3 scripts/sync-skills-index.py`",
                file=sys.stderr,
            )
            return 1
        print(f"skills/INDEX.md is in sync ({len(skills)} skills)")
        return 0

    INDEX.write_text(rendered, encoding="utf-8")
    print(f"wrote skills/INDEX.md ({len(skills)} skills)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
