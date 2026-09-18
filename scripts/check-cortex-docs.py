#!/usr/bin/env python3
"""Check that the prose about `bin/cortex` matches the script.

Three audits in one day found the same shape of defect: the assets are
guarded by CI and correct, while the prose describing how the installer
behaves had drifted behind it. Semantics are beyond a checker — whether
"pulls the latest commit" fairly describes a hard reset needs a reader — but
two things are decidable, and they are the ones that went wrong.

1. A document must not name a subcommand or flag the script does not have.
   Writing `cortex sync` when the command is `cortex update` sends a reader
   to a "command not found".
2. Every subcommand the script offers must be documented somewhere, so a new
   one cannot ship with nobody told.

Only code is read — fenced blocks and inline spans — because that is where a
command is written. Prose saying "bin/cortex run from inside a clone" names
no subcommand, and reading it as one would report a defect that is not there.
"""

from __future__ import annotations

import pathlib
import re
import sys


ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = "bin/cortex"
DOCS = ("README.md", "AGENTS.md", "CLAUDE.md", "CONTRIBUTING.md")

DISPATCH = re.compile(r"^case \"\$_cmd\" in$(.*?)^esac$", re.MULTILINE | re.DOTALL)
DISPATCH_ARM = re.compile(r"^\s{2}([a-z][a-z-]*)\)\s", re.MULTILINE)
SCRIPT_FLAG = re.compile(r"--[a-z][a-z-]+")
# `cortex <command> [flags]`, with or without a leading path or backtick.
INVOCATION = re.compile(r"(?:^|[\s`/])cortex\s+([a-z][a-z-]*)((?:\s+--[a-z][a-z-]+)*)")


def script_commands(script: str) -> set[str]:
    body = DISPATCH.search(script)
    if not body:
        return set()
    return set(DISPATCH_ARM.findall(body.group(1)))


CODE_SPAN = re.compile(r"`([^`]+)`")


def code_lines(text: str) -> list[tuple[int, str]]:
    """Every line of a fenced block, plus the contents of each inline span."""
    out: list[tuple[int, str]] = []
    in_fence = False
    for number, line in enumerate(text.split("\n"), 1):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            out.append((number, line))
            continue
        for span in CODE_SPAN.findall(line):
            out.append((number, span))
    return out


def documented(root: pathlib.Path) -> dict[str, list[tuple[str, int, str]]]:
    """Map each documented `cortex <command>` to where it was written, with its flags."""
    found: dict[str, list[tuple[str, int, str]]] = {}
    for name in DOCS:
        path = root / name
        if not path.is_file():
            continue
        for number, line in code_lines(path.read_text(encoding="utf-8")):
            for command, flags in INVOCATION.findall(line):
                found.setdefault(command, []).append((name, number, flags.strip()))
    return found


def check(root: pathlib.Path) -> list[str]:
    script_path = root / SCRIPT
    if not script_path.is_file():
        return [f"no {SCRIPT} under {root}"]
    script = script_path.read_text(encoding="utf-8")

    commands = script_commands(script)
    if not commands:
        return [f"{SCRIPT}: could not read the command dispatch"]
    flags = set(SCRIPT_FLAG.findall(script))

    problems: list[str] = []
    mentions = documented(root)

    for command, places in sorted(mentions.items()):
        for name, number, flag_text in places:
            if command not in commands:
                problems.append(
                    f"{name}:{number} writes `cortex {command}`, which {SCRIPT} does not accept "
                    f"(it has: {', '.join(sorted(commands))})"
                )
                continue
            for flag in SCRIPT_FLAG.findall(flag_text):
                if flag not in flags:
                    problems.append(f"{name}:{number} writes `cortex {command} {flag}`, unknown to {SCRIPT}")

    for command in sorted(commands - set(mentions)):
        problems.append(f"{SCRIPT} offers `{command}`, which none of {', '.join(DOCS)} mentions")

    return problems


def main() -> int:
    problems = check(ROOT)
    if problems:
        print("The prose about bin/cortex does not match the script:")
        for problem in problems:
            print(f"- {problem}")
        return 1
    print("Every documented cortex command and flag exists, and every command is documented.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
