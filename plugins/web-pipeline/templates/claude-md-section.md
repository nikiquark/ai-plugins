## Web pipeline

This project uses the `web-pipeline` plugin. Hooks are enabled by `.claude/web-pipeline.json`.

- **Stack**: <fill in>
- **Run locally**: `make dev` → <url>
- **Quality gate**: `make check` (lint, types, tests, duplication, dead code, gitleaks, anti-slop, ansible-lint). It must pass before any task counts as done.
- **Audit**: `make audit` (semgrep, dependency audit). Slow and needs the network, so it runs before deploys, not on every stop.
- **Docs**: `docs/spec.md` (what and why) · `docs/content.md` (message, copy, SEO metadata) · `docs/architecture.md` (how) · `docs/adr/` (decisions) · `docs/design.md` (visual system) · `docs/plan.md` (tasks) · `docs/changes/` (change requests)
- **Deploy**: `deploy/ansible/` via `/web-pipeline:deploy <env>`. Never run `ansible-playbook` without `--check` outside that skill.

Rules:
- Before writing any new module, follow `dev-core:reuse-first` and leave a `reuse:` note in the hand-off.
- Frontend follows `web-pipeline:frontend-style` and `docs/design.md`. `scripts/anti_slop.py` must pass.
- Copy and page metadata come from `docs/content.md`. Public pages follow `web-pipeline:seo-standards`, and `make seo` must pass against the running app.
- Backend follows `web-pipeline:backend-standards`. Tests follow `web-pipeline:testing-standards`.
