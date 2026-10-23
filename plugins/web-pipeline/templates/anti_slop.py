#!/usr/bin/env python3
"""Anti-slop checker: flags the visual tells of generic AI-generated frontends.

Owned by the project (copied from the web-pipeline plugin), stdlib only, safe for CI.

    python3 scripts/anti_slop.py [paths...] [--since REF] [--strict] [--quiet]

Errors fail the run (exit 1). Warnings are printed for the design critic to judge;
--strict turns them into errors. Silence a deliberate exception on one line with a
comment containing `anti-slop: allow <reason>`.

Edit the lists below to tune the rules for this project.
"""
from __future__ import annotations

import argparse
import colorsys
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

UI_EXTENSIONS = {
    ".html", ".htm", ".css", ".scss", ".sass", ".less", ".js", ".jsx", ".mjs", ".ts", ".tsx",
    ".vue", ".svelte", ".astro", ".mdx", ".jinja", ".jinja2", ".j2", ".twig", ".erb", ".hbs",
    ".njk", ".liquid", ".php", ".heex", ".templ",
}
EXTRA_FILES = {"package.json"}
SKIP_DIRS = {
    "node_modules", ".git", "dist", "build", ".next", ".nuxt", ".svelte-kit", ".astro", "out",
    "coverage", "vendor", ".venv", "venv", "__pycache__", "target", ".turbo", ".cache",
    "playwright-report", "test-results", "staticfiles",
}
ALLOW_MARKER = "anti-slop: allow"

BANNED_FONTS = [
    "Inter", "Roboto", "Open Sans", "Lato", "Arial", "Montserrat", "Poppins", "Geist",
    "Geist Mono", "Space Grotesk", "system-ui", "-apple-system", "BlinkMacSystemFont",
]
ICON_PACKAGES = r"lucide(?:-[a-z]+)?|@heroicons/[\w/-]+|@tabler/icons[\w/-]*|react-icons(?:/\w+)?|feather-icons|react-feather"

_font_alt = "|".join(re.escape(f) for f in BANNED_FONTS)
_font_url_alt = "|".join(re.escape(f.replace(" ", "+")) for f in BANNED_FONTS)
_font_ident_alt = "|".join(re.escape(f.replace(" ", "_")) for f in BANNED_FONTS)
_font_pkg_alt = "|".join(re.escape(f.lower().replace(" ", "-")) for f in BANNED_FONTS)

EMOJI = re.compile("[\U0001F000-\U0001FAFF☀-➿⬀-⯿️]")
HEX = re.compile(r"#(?:[0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b")
PURPLE_NAMES = re.compile(r"\b(purple|violet|indigo|fuchsia|magenta|blueviolet|mediumpurple|rebeccapurple)\b", re.I)


@dataclass(frozen=True)
class Rule:
    name: str
    level: str  # "error" | "warn"
    message: str
    patterns: tuple[re.Pattern[str], ...]  # all must match the same line


def rule(name: str, level: str, message: str, *patterns: str) -> Rule:
    return Rule(name, level, message, tuple(re.compile(p, re.I) for p in patterns))


RULES: list[Rule] = [
    # Hard bans from the user's design brief.
    rule("icon-library", "error",
         "stock icon set (lucide/heroicons/tabler/feather/react-icons); use no icons or custom SVG",
         rf"""(['"])(?:{ICON_PACKAGES})\1|unpkg\.com/lucide|cdn\.jsdelivr\.net/npm/lucide"""),
    rule("banned-font", "error", "overused default font as primary family",
         rf"""font-family\s*:\s*['"]?(?:{_font_alt})\b"""),
    rule("banned-font", "error", "overused default font as primary family",
         rf"""fontFamily\s*:\s*['"`]\s*['"]?(?:{_font_alt})\b"""),
    rule("banned-font", "error", "overused default font as primary family (Tailwind theme)",
         rf"""\b(?:sans|serif|display|body|heading|headline|text|base)\s*:\s*\[\s*['"](?:{_font_alt})['"]"""),
    rule("banned-font", "error", "overused default font loaded from Google Fonts",
         rf"""fonts\.googleapis\.com/[^'")\s]*family=(?:{_font_url_alt})\b"""),
    rule("banned-font", "error", "overused default font via next/font",
         rf"""import\s*\{{[^}}]*\b(?:{_font_ident_alt})\b[^}}]*\}}\s*from\s*['"](?:next/font/google|geist/font[\w/]*)['"]"""),
    rule("banned-font", "error", "overused default font via @fontsource",
         rf"""@fontsource(?:-variable)?/(?:{_font_pkg_alt})\b"""),
    rule("background-orb", "error", "blurred circle / glowing orb decoration",
         r"\brounded-full\b", r"\bblur-(?:2xl|3xl|\[\d{2,}px\])"),
    # Clichés that Claude's frontend-design guidance itself rejects (gradients are otherwise allowed).
    rule("purple-gradient", "error", "purple/indigo/violet SaaS gradient cliché (Tailwind)",
         r"\bbg-(?:gradient|linear|radial|conic)-", r"\b(?:from|via|to)-(?:purple|violet|indigo|fuchsia)-\d{2,3}\b"),
    # Warnings: likely slop, judged visually by the design critic.
    rule("gradient-text", "warn", "gradient-filled text (the classic AI hero headline)",
         r"\bbg-clip-text\b", r"\btext-transparent\b"),
    rule("gradient-text", "warn", "gradient-filled text (the classic AI hero headline)",
         r"(?:-webkit-)?background-clip\s*:\s*text"),
    rule("badge", "warn", "badge/pill styling; the brief bans decorative badges",
         r"\brounded-full\b", r"\bpx-(?:1\.5|2|2\.5|3)\b", r"\bpy-(?:0|0\.5|1)\b", r"\btext-(?:xs|\[1[01]px\])\b"),
    rule("card", "warn", "rounded shadowed card; the brief bans card-based layouts",
         r"\brounded-(?:lg|xl|2xl|3xl)\b", r"\bshadow(?:-sm|-md|-lg|-xl|-2xl)?\b(?!-)"),
    rule("glassmorphism", "warn", "frosted-glass panel",
         r"\bbackdrop-blur(?:-\w+)?\b|backdrop-filter\s*:\s*blur"),
    rule("eyebrow", "warn", "tracked all-caps eyebrow label",
         r"\buppercase\b", r"\btracking-(?:wide|wider|widest|\[0?\.\d+em\])\b", r"\btext-(?:xs|sm)\b"),
]


def is_purple(hex_color: str) -> bool:
    h = hex_color.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    hue, light, sat = colorsys.rgb_to_hls(r, g, b)
    return 250 <= hue * 360 <= 300 and sat >= 0.35 and 0.2 <= light <= 0.8


def check_css_specials(line: str) -> list[tuple[str, str, str]]:
    found: list[tuple[str, str, str]] = []
    for m in re.finditer(r"(?:linear|radial|conic)-gradient\(([^;]*)", line, re.I):
        body = m.group(1)
        if PURPLE_NAMES.search(body) or any(is_purple(c) for c in HEX.findall(body)):
            found.append(("purple-gradient", "error", "purple/violet gradient cliché (CSS)"))
    for m in re.finditer(r"(?<!backdrop-)filter\s*:\s*blur\(\s*(\d+)px", line, re.I):
        if int(m.group(1)) >= 40:
            found.append(("background-orb", "error", f"blur({m.group(1)}px) glow/orb decoration"))
    if EMOJI.search(line):
        found.append(("emoji", "error", "emoji or pictographic symbol in UI source"))
    return found


def scan_file(path: Path) -> list[tuple[int, str, str, str]]:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []
    hits: list[tuple[int, str, str, str]] = []
    for lineno, line in enumerate(text.splitlines(), 1):
        if ALLOW_MARKER in line:
            continue
        seen: set[str] = set()
        for r in RULES:
            if r.name not in seen and all(p.search(line) for p in r.patterns):
                hits.append((lineno, r.level, r.name, r.message))
                seen.add(r.name)
        for name, level, message in check_css_specials(line):
            if name not in seen:
                hits.append((lineno, level, name, message))
                seen.add(name)
    return hits


def is_candidate(path: Path) -> bool:
    if any(part in SKIP_DIRS for part in path.parts):
        return False
    if path.name.endswith((".min.js", ".min.css")):
        return False
    return path.suffix.lower() in UI_EXTENSIONS or path.name in EXTRA_FILES


def git_lines(*args: str) -> list[str] | None:
    try:
        out = subprocess.run(["git", *args], capture_output=True, text=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError):
        return None
    return [line for line in out.splitlines() if line]


def collect_files(paths: list[str], since: str | None) -> list[Path]:
    if since:
        changed = git_lines("diff", "--name-only", "--diff-filter=ACMR", f"{since}...HEAD") or []
        changed += git_lines("diff", "--name-only", "--diff-filter=ACMR", "HEAD") or []
        changed += git_lines("ls-files", "--others", "--exclude-standard") or []
        files = {Path(p) for p in changed}
    else:
        files = set()
        for root in paths:
            listed = git_lines("ls-files", "--cached", "--others", "--exclude-standard", "--", root)
            if listed is not None:
                files.update(Path(p) for p in listed)
                continue
            for dirpath, dirnames, filenames in os.walk(root):
                dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
                files.update(Path(dirpath) / f for f in filenames)
    return sorted(p for p in files if p.is_file() and is_candidate(p))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("paths", nargs="*", default=["."])
    parser.add_argument("--since", help="only check files changed since this git ref (legacy codebases)")
    parser.add_argument("--strict", action="store_true", help="treat warnings as errors")
    parser.add_argument("--quiet", action="store_true", help="print errors only")
    args = parser.parse_args()

    errors = warnings = 0
    for path in collect_files(args.paths, args.since):
        for lineno, level, name, message in scan_file(path):
            if level == "warn" and args.strict:
                level = "error"
            if level == "error":
                errors += 1
            else:
                warnings += 1
                if args.quiet:
                    continue
            print(f"{path}:{lineno}: [{level}] {name}: {message}")

    summary = f"anti-slop: {errors} error(s), {warnings} warning(s)"
    print(summary, file=sys.stderr)
    if errors:
        print(f"Fix them, or mark a deliberate exception with `{ALLOW_MARKER} <reason>` on that line.",
              file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
