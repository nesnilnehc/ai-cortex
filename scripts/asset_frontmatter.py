"""Read AI Cortex asset version declarations without YAML dependencies."""

from __future__ import annotations

import re


FRONTMATTER = re.compile(r"\A---[ \t]*\r?\n(.*?)^---[ \t]*\r?$", re.MULTILINE | re.DOTALL)
METADATA = re.compile(r"^metadata:[ \t]*(?:#[^\r\n]*)?\r?\n((?:[ \t]+[^\n]*\n|\r?\n)*)", re.MULTILINE)
VERSION_VALUE = r"""[ \t]*(['"]?)([^\s'"#]+)\1[ \t]*(?:#[^\r\n]*)?\r?$"""


def declared_version(text: str | None, *, is_skill: bool = False) -> str | None:
    """Read standard Skill metadata and the legacy top-level declaration."""
    header = FRONTMATTER.match(text or "")
    if header is None:
        return None
    legacy = re.search(r"^version:" + VERSION_VALUE, header[1], re.MULTILINE)
    metadata = METADATA.search(header[1]) if is_skill else None
    nested = None
    if metadata is not None:
        indent = re.search(r"^( +)[^ \t#\r\n]", metadata[1], re.MULTILINE)
        if indent is not None:
            nested = re.search(r"^" + indent[1] + "version:" + VERSION_VALUE, metadata[1], re.MULTILINE)
    if nested is not None and legacy is not None and nested[2] != legacy[2]:
        return None
    version = nested if nested is not None else legacy
    return version[2] if version is not None else None
