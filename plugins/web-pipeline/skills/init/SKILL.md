---
name: init
description: Opt a project into the web pipeline - create .claude/web-pipeline.json (enables the plugin's hooks), install the anti-slop and SEO checkers, wire `make check` and `make seo`, set up .claude/state and the CLAUDE.md section. Use when starting the web pipeline in a project for the first time.
argument-hint: "[--legacy]"
---

# Opt a project into the web pipeline

The plugin's hooks (lint after edits, `make check` before stopping) do nothing unless `.claude/web-pipeline.json` exists. That keeps other projects, such as scientific ones, untouched. This skill creates that file and the pieces it relies on. **Never overwrite an existing file without asking.** Merge instead, and show the diff.

## Steps

1. **Detect the stack** from the lock files and manifests: `package.json`, `pnpm-lock.yaml`, `pyproject.toml`, `uv.lock`, `requirements*.txt`, `manage.py`, `Dockerfile`, `deploy/ansible/`. For a new, empty project, record the stack as `TBD`.

2. **Write `.claude/web-pipeline.json`** from `${CLAUDE_PLUGIN_ROOT}/templates/web-pipeline.json`. Fill in the commands for the detected stack:
   - `format_file` and `lint_file`: single-file commands with a `{file}` placeholder that the post-edit hook runs on every edited file. Examples: `npx prettier --write {file}` / `npx eslint {file}`, `ruff format {file}` / `ruff check {file}`. Leave them empty while the stack is TBD.
   - `check`: normally `make check`.
   - `lint_extensions`: the file extensions that `lint_file` understands.
   - `stop_gate.enabled`: leave it `false` until `make check` exists and passes. For a new project, delivery phase D1 turns it on. For an existing project, run `make check` once: set it to `true` if the check passes; otherwise leave it `false` and list the failures for the user.

3. **Install the checkers.** Copy `${CLAUDE_PLUGIN_ROOT}/templates/anti_slop.py` to `scripts/anti_slop.py`. The project owns its copy, so it also runs in CI and without Claude. For an existing codebase (`--legacy`, or when the audit found existing UI), make the `make check` target run it as `python3 scripts/anti_slop.py --since origin/main`. That checks only changed files, so legacy code does not block every change. Explain this to the user.

   Copy `${CLAUDE_PLUGIN_ROOT}/templates/seo_check.py` to `scripts/seo_check.py` the same way. It checks a running site, so it is not part of `make check`.

4. **Wire `make check` and `make seo`.** If a Makefile exists, add a `check` target or extend the existing one, and show the diff. If there is no Makefile, create one with `check`, `dev`, `test`, `lint`, `fmt` and `seo` targets. Use placeholders for tools that are not chosen yet, and make each placeholder fail with a clear message (`@echo "configure lint for <stack>" && exit 1`). Do not make placeholders pass silently. The `seo` target runs the SEO checker against the dev server:
   ```make
   BASE_URL ?= http://localhost:3000
   SITE_URL ?=
   SEO_EXPECT ?= index
   seo:
   	python3 scripts/seo_check.py $(BASE_URL) --expect $(SEO_EXPECT) $(if $(SITE_URL),--site-url $(SITE_URL))
   ```
   Set `BASE_URL` to the dev server's URL. `SITE_URL` (the canonical origin) and `SEO_EXPECT` (`noindex` for a private app) come from `docs/content.md` once it exists.

5. **State directory.** Create `.claude/state/` and add `.claude/state/` to `.gitignore`.

6. **CLAUDE.md section.** Append `${CLAUDE_PLUGIN_ROOT}/templates/claude-md-section.md` to the project's `CLAUDE.md`, creating the file if needed, and fill in the stack and the commands. If the section already exists, update it in place.

7. **Report**: what was created or changed, which tools `make check` expects that are not installed (with install commands), and that the hooks are now active for this project.
