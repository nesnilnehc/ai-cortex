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


ROOT = pathlib.Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "skills-index"

EXPECTED_CLEAN = """# Skills

Generated from each skill's own `SKILL.md` frontmatter by
`scripts/sync-skills-index.py`. Edit the skill, then regenerate — an edit made
here alone is overwritten and does not reach the skill.

- [alpha-skill](./alpha-skill/SKILL.md) — Do the alpha thing.
  - tags: `alpha`, `demo` · triggers: `do alpha`, `alpha thing`
- [beta-skill](./beta-skill/SKILL.md) — Do the beta thing.
  - tags: `beta` · triggers: `do beta`
"""

# Rejections the generator must make, as fixture directory -> expected message
# fragment. Each one is a way the registry could otherwise go silently wrong.
REJECTIONS = {
    "name-mismatch": "does not match directory",
    "block-list": "must be a flow list",
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
    if fields["tags"] != ["alpha", "demo"]:
        errors.append(f"clean: tags parsed as {fields['tags']}")
    if fields["triggers"] != ["do alpha", "alpha thing"]:
        errors.append(f"clean: triggers parsed as {fields['triggers']}")

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


def main() -> int:
    sync = load_generator()
    errors: list[str] = []
    check_clean(sync, errors)
    check_rejections(sync, errors)
    check_unknown_argument(sync, errors)

    if errors:
        print("skills registry generator tests failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(
        f"Validated the skills registry generator on 1 clean tree "
        f"and {len(REJECTIONS)} malformed ones."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
