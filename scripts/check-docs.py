#!/usr/bin/env python3
"""Fail when a plugin component has no page in docs/.

Expected pages:
  plugins/<p>/skills/<s>/SKILL.md  ->  docs/<p>/skills/<s>.md or docs/<p>/commands/<s>.md
  plugins/<p>/agents/<a>.md        ->  docs/<p>/agents/<a>.md
  plugins/<p>/bin/<b>              ->  docs/<p>/<b>.md

Only checks that the pages exist; mkdocs build --strict checks that they are in the nav.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"


def expected() -> list[tuple[Path, list[Path]]]:
    pairs: list[tuple[Path, list[Path]]] = []
    for plugin in sorted((ROOT / "plugins").iterdir()):
        if not plugin.is_dir():
            continue
        docs = DOCS / plugin.name
        for skill in sorted(plugin.glob("skills/*/SKILL.md")):
            name = skill.parent.name
            pairs.append((skill, [docs / "skills" / f"{name}.md", docs / "commands" / f"{name}.md"]))
        for agent in sorted(plugin.glob("agents/*.md")):
            pairs.append((agent, [docs / "agents" / agent.name]))
        for exe in sorted(plugin.glob("bin/*")):
            pairs.append((exe, [docs / f"{exe.name}.md"]))
    return pairs


def main() -> int:
    missing = [(src, pages) for src, pages in expected() if not any(p.is_file() for p in pages)]
    for src, pages in missing:
        options = " or ".join(str(p.relative_to(ROOT)) for p in pages)
        print(f"{src.relative_to(ROOT)}: no docs page ({options})")
    if missing:
        print(f"check-docs: {len(missing)} component(s) undocumented", file=sys.stderr)
        return 1
    print("check-docs: every skill, agent and bin command has a page", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
