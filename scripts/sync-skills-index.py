#!/usr/bin/env python3
"""Render the skill index from frontmatter and recorded provenance.

AGENTS.md §4 discovers skills through their descriptions. The registry is
derived here so its entries agree with the skills they register.
"""

from __future__ import annotations

import pathlib
import json
import importlib.util
import re
import sys


ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
INDEX = SKILLS_DIR / "INDEX.md"

USAGE = """usage:
  scripts/sync-skills-index.py            rewrite the registry
  scripts/sync-skills-index.py --check    fail when it is out of date
  scripts/sync-skills-index.py --preview-dir PATH  isolated schema-2 preview"""

HEADER = """# Skills

Generated from Skill `SKILL.md` frontmatter and `skills/PROVENANCE.json` by
`scripts/sync-skills-index.py`. Edit the sources, then regenerate — an edit
made here alone is overwritten and does not reach the sources.
"""

REGISTRY_FIELDS = ("name", "description")
SCALAR = re.compile(r"^(name|description):\s*(.+?)\s*$", re.M)
RESEARCH_METADATA = re.compile(r"^  (ai_cortex_type|ai_cortex_user_invocable):\s*(.+?)\s*$", re.M)
SKILL_TYPES = {"foundation", "domain", "orchestrator"}


class SkillError(Exception):
    """A skill cannot supply the fields the registry is built from."""


def read_frontmatter(skill_md: pathlib.Path) -> dict[str, object]:
    """Return the registry fields declared by one SKILL.md.

    skill_md: path to a skill's SKILL.md
    Returns: dict with `name` and `description` as strings
    Raises: SkillError when a required field is absent
    """
    text = skill_md.read_text(encoding="utf-8")
    if not text.startswith("---"):
        raise SkillError(f"{relative(skill_md)}: no frontmatter block")
    block = text.split("---", 2)[1]

    fields: dict[str, object] = {
        key: value.strip("\"'") for key, value in SCALAR.findall(block)
    }
    # The catalogue is a single paragraph even when frontmatter uses a block scalar.
    description = re.search(r"^description: [>|][+-]? *\n((?:[ \t]+[^\n]*(?:\n|$))*)", block, re.M)
    if description:
        fields['description'] = ' '.join(description.group(1).split())
    for key in REGISTRY_FIELDS:
        if not fields.get(key):
            raise SkillError(f"{relative(skill_md)}: frontmatter is missing `{key}`")
    metadata = re.search(r"^metadata:\s*\n((?:[ \t]+[^\n]*\n?)*)", block, re.M)
    if metadata:
        research = {key: value.strip("\"'") for key, value in RESEARCH_METADATA.findall(metadata.group(1))}
        if research:
            if research.get("ai_cortex_type") not in SKILL_TYPES:
                raise SkillError(f"{relative(skill_md)}: invalid `ai_cortex_type`")
            if research.get("ai_cortex_user_invocable") not in {"true", "false"}:
                raise SkillError(f"{relative(skill_md)}: invalid `ai_cortex_user_invocable`")
            fields.update(research)
    return fields


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


def render(skills: list[tuple[str, dict[str, object]]], origins: dict | None = None) -> str:
    """Return the full INDEX.md text for the given skills."""
    lines = [HEADER]
    if origins is not None:
        lines.append('Provenance markers come from [PROVENANCE.json](./PROVENANCE.json); confirmed AI Cortex originals omit the badge. An absent badge alone does not establish originality.\n')
    for name, fields in skills:
        lines.append(f"- [{name}](./{name}/SKILL.md) — {fields['description']}")
        if origins is not None and origins[name]['classification'] != 'unverified':
            record = origins[name]
            labels = json.loads((ROOT / 'website/explore/locales/en.json').read_text(encoding='utf-8'))['provenance']['labels']
            marker = '  - provenance:' if record['classification'] == 'native' else f"  - provenance: **{labels[record['classification']]}**"
            references = record.get('evidence', [])
            if isinstance(references, str):
                path, sep, anchor = references.partition('#')
                references = [{'path': path, **({'anchor': anchor} if sep else {})}]
            for reference in references:
                path = reference['path']
                target = ('./'+path[len('skills/'):]) if path.startswith('skills/') else ('../'+path)
                if reference.get('anchor'):
                    target += '#' + reference['anchor']
                marker += f" · [evidence]({target})"
            lines.append(marker)
        if "ai_cortex_type" in fields:
            lines.append(
                f"  - type: `{fields['ai_cortex_type']}`"
                f" · user-invocable: `{fields['ai_cortex_user_invocable']}`"
            )
    return "\n".join(lines) + "\n"


def relative(path: pathlib.Path) -> str:
    """Path relative to the repository root, or absolute when it lies outside."""
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def generate_reviewed(skills, *, check=False, preview_dir=None):
    from skill_provenance_output import generate
    generate(ROOT, skills, render, check=check, preview_dir=preview_dir)


def main(argv: list[str]) -> int:
    check_only = False
    preview_dir = None
    arguments = iter(argv)
    for argument in arguments:
        if argument == '--check':
            check_only = True
        elif argument == '--preview-dir':
            preview_dir = next(arguments, None)
            if not preview_dir:
                print(USAGE, file=sys.stderr)
                return 2
        else:
            print(f"error: unknown argument `{argument}`\n{USAGE}", file=sys.stderr)
            return 2
    if check_only and preview_dir is not None:
        print('error: --check cannot be combined with --preview-dir', file=sys.stderr)
        return 2

    try:
        skills = collect(SKILLS_DIR)
    except SkillError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    from skill_provenance_v2 import ProvenanceError as ReviewedError, read_json, require
    try:
        manifest = read_json(SKILLS_DIR / 'PROVENANCE.json')
        require(isinstance(manifest, dict), 'expected provenance object')
        schema = manifest.get('schema_version')
        if schema == 2 or preview_dir is not None:
            generate_reviewed(skills, check=check_only, preview_dir=preview_dir)
            print(f"{'Checked' if check_only else 'Generated'} reviewed provenance for {len(skills)} skills" + (' in isolated preview' if preview_dir else ''))
            return 0
    except (ReviewedError, OSError) as error:
        print(f'error: {error}', file=sys.stderr)
        return 1

    module_spec = importlib.util.spec_from_file_location('skill_provenance', ROOT / 'scripts/skill-provenance.py')
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    try:
        origins = module.load(ROOT, SKILLS_DIR)
    except module.ProvenanceError as error:
        print(f'error: {error}', file=sys.stderr)
        return 1
    rendered = render(skills, origins)
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
