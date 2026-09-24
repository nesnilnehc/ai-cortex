#!/usr/bin/env python3
"""Test the skills registry generator against fixture skill trees.

The CI `--check` step compares the generator's output with a file the same
generator wrote, so it cannot notice a parsing bug: a dropped field would
produce a consistently wrong registry that still matches. These fixtures give
that check a denominator by asserting the rendered text independently.
"""

from __future__ import annotations

import contextlib
import importlib.util
import io
import pathlib
import sys
import tempfile


ROOT = pathlib.Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "skills-index"

EXPECTED_CLEAN = """# Skills

Generated from each skill's own `SKILL.md` frontmatter by
`scripts/sync-skills-index.py`. Edit the skill, then regenerate — an edit made
here alone is overwritten and does not reach the skill.

- [alpha-skill](./alpha-skill/SKILL.md) — Do the alpha thing.
- [beta-skill](./beta-skill/SKILL.md) — Do the beta thing.
"""

# Rejections the generator must make, as fixture directory -> expected message
# fragment. Each one is a way the registry could otherwise go silently wrong.
REJECTIONS = {
    "name-mismatch": "does not match directory",
    "missing-description": "frontmatter is missing `description`",
    "no-skill-md": "has no SKILL.md",
    "no-frontmatter": "no frontmatter block",
}


def load_generator():
    """Import sync-skills-index.py, whose hyphenated name blocks a plain import."""
    path = pathlib.Path(__file__).with_name("sync-skills-index.py")
    spec = importlib.util.spec_from_file_location("sync_skills_index", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check_clean(sync, errors: list[str]) -> None:
    """Assert the fields and the rendered text for a well-formed skill tree."""
    skills = sync.collect(FIXTURES / "clean")
    names = [name for name, _ in skills]
    if names != ["alpha-skill", "beta-skill"]:
        errors.append(f"clean: expected both skills in name order, got {names}")
        return

    fields = dict(skills)["alpha-skill"]
    if fields["description"] != "Do the alpha thing.":
        errors.append(f"clean: description parsed as {fields['description']}")

    rendered = sync.render(skills)
    if rendered != EXPECTED_CLEAN:
        errors.append(
            "clean: rendered registry does not match the expected text\n"
            f"--- expected ---\n{EXPECTED_CLEAN}--- got ---\n{rendered}"
        )


def check_rejections(sync, errors: list[str]) -> None:
    """Assert each malformed tree is rejected with a message that names the cause."""
    for directory, fragment in REJECTIONS.items():
        try:
            sync.collect(FIXTURES / directory)
        except sync.SkillError as error:
            if fragment not in str(error):
                errors.append(
                    f"{directory}: expected a message containing "
                    f"{fragment!r}, got {str(error)!r}"
                )
        else:
            errors.append(f"{directory}: accepted a tree it must reject")


def check_unknown_argument(sync, errors: list[str]) -> None:
    """Assert an unrecognised argument refuses rather than rewriting the registry."""
    # The refusal writes its usage text to stderr; swallow it so a passing run
    # does not print something that reads like a failure.
    with contextlib.redirect_stderr(io.StringIO()):
        code = sync.main(["--not-a-real-flag"])
    if code != 2:
        errors.append(f"unknown argument: expected exit 2, got {code}")


def check_research_metadata(sync, errors: list[str]) -> None:
    """New metadata is optional for existing skills and strict when present."""
    with tempfile.TemporaryDirectory() as tmp:
        folder = pathlib.Path(tmp) / "research-example"
        folder.mkdir()
        skill = folder / "SKILL.md"
        base = (FIXTURES / "research-metadata" / "research-example" / "SKILL.md").read_text(encoding="utf-8")
        skill.write_text(base, encoding="utf-8")
        fields = sync.read_frontmatter(skill)
        if fields.get("ai_cortex_type") != "foundation" or fields.get("ai_cortex_user_invocable") != "true":
            errors.append(f"research metadata: parsed {fields}")
        rendered = sync.render([("research-example", fields)])
        if "type: `foundation` · user-invocable: `true`" not in rendered:
            errors.append("research metadata: missing from registry output")
        for old, bad, fragment in [
            ("ai_cortex_type: foundation", "ai_cortex_type: invalid", "ai_cortex_type"),
            ('ai_cortex_user_invocable: "true"', "ai_cortex_user_invocable: maybe", "ai_cortex_user_invocable"),
        ]:
            skill.write_text(base.replace(old, bad), encoding="utf-8")
            try:
                sync.read_frontmatter(skill)
            except sync.SkillError as exc:
                if fragment not in str(exc):
                    errors.append(f"research metadata: wrong error {exc}")
            else:
                errors.append(f"research metadata: accepted {bad}")


def main() -> int:
    sync = load_generator()
    errors: list[str] = []
    check_clean(sync, errors)
    check_rejections(sync, errors)
    check_unknown_argument(sync, errors)
    check_research_metadata(sync, errors)

    if errors:
        print("skills registry generator tests failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(
        f"Validated the skills registry generator on 1 clean tree, 1 metadata fixture "
        f"and {len(REJECTIONS)} malformed ones."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
