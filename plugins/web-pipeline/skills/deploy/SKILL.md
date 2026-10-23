---
name: deploy
description: Deploy the current project to staging or production with Ansible - preflight, check/diff with user approval, apply, smoke tests, post-deploy security checks, report and rollback offer.
disable-model-invocation: true
argument-hint: "[staging|production]"
---

# Deploy

Target environment: `$ARGUMENTS`. If empty, use `staging`. Production requires that the same commit is already green on staging, unless the user explicitly says otherwise.

Follow the `web-pipeline:ansible-conventions` skill. Act **only** on hosts in `deploy/ansible/inventories/<env>/`. Talk to the user in their language.

## 1. Preflight (stop at the first failure)

- The working tree is clean, and the branch is the one the user wants to ship (normally `main`).
- `make check` passes.
- `ansible-playbook --syntax-check` passes and `ansible-lint` is clean.
- The vault is reachable without printing secrets: `ansible-inventory -i inventories/<env> --list >/dev/null`.
- For production, confirm the commit SHA that is on staging now (from the last deploy report).
- Note any migrations in this release. For each irreversible one, warn the user explicitly.

## 2. Dry run → GATE

Run `ansible-playbook -i inventories/<env> playbooks/deploy.yml --check --diff` (or `site.yml` if roles changed). Summarize for the user what changes on which hosts: packages, configs, services, release. Show the relevant diff excerpts. **Wait for an explicit "go".** The guard hook will also ask for permission on the real run, and that prompt is expected.

## 3. Apply

- Tag the release: `git tag -a deploy-<env>-<YYYYMMDD-HHMM> -m "deploy <env>"`. Do not push the tag unless the user asks.
- Run the playbook without `--check`. On failure, stop and show the failing task and its output. Offer to roll back. Never retry blindly.

## 4. Smoke tests

- `playbooks/smoke.yml` if it exists. Otherwise run `curl -fsS` against `/healthz` and `/readyz` and against the key routes from `docs/spec.md`, and check the status codes and response times.
- If the project has Playwright tests tagged `@smoke`, run them with `BASE_URL=<env url>`.
- **Indexing**: run `python3 scripts/seo_check.py https://<host>`, or the plugin's copy at `${CLAUDE_PLUGIN_ROOT}/templates/seo_check.py` if the project has none. Staging always uses `--expect noindex`. Production uses `--expect index`, unless `docs/content.md` says the app is private. A production that blocks crawlers, or a staging that can be indexed, is a high finding.

## 5. Post-deploy security checks (own hosts only)

Run what is installed. List what is missing, with install hints, rather than skipping silently:
- **Headers**: `curl -sI https://<host>`. Check HSTS, CSP, X-Content-Type-Options, Referrer-Policy and frame-ancestors/X-Frame-Options, and that no `Server`/`X-Powered-By` version is leaked.
- **TLS**: `testssl.sh --quiet --severity MEDIUM https://<host>`, or check the expiry with `openssl s_client`.
- **Open ports**: `nmap -Pn --top-ports 200 <host>`. Only 22/80/443 (or the documented ports) may be open.
- **Images and filesystem**: `trivy image <image:tag>` for containers, or `trivy fs` on the release through an ad-hoc Ansible command if trivy is on the host.
- **Passive DAST**: `docker run --rm -t ghcr.io/zaproxy/zaproxy:stable zap-baseline.py -t https://<host>`. This is passive only, never the active scan.

Classify each finding as critical, high, medium or low. A critical or high finding means you recommend a rollback or an immediate fix, and the user decides.

## 6. Report and rollback

Write `docs/deploys/<YYYY-MM-DD>-<env>.md` with the commit SHA, the tag, the duration, the changes, the smoke results, the security findings and their decisions. If anything failed, offer `playbooks/rollback.yml` with `--check` first, and run it only after the user approves.
