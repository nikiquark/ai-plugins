---
name: secure-maintain
description: Security maintenance for a deployed project - scan dependencies, running images and hosts (via Ansible) for known vulnerabilities, triage with the user, then patch on a branch, verify, and hand off to deploy. Report-only mode for scheduled runs.
disable-model-invocation: true
argument-hint: "[report|fix] [staging|production|all]"
---

# Security maintenance

Arguments: `$ARGUMENTS`. Mode is `report` (default; makes no changes) or `fix`. The environment defaults to `production`. Talk to the user in their language. Act only on hosts in this project's inventory.

## 1. Scan (delegate to `web-pipeline:ops-auditor`)

Delegate with a self-contained message: the project path, the environment, the inventory path, and the list of scans below. The auditor runs only read-only commands and returns one normalized findings table. Its tool output stays out of the main context.

- **Code dependencies**: `osv-scanner scan source -r .`, `trivy fs --scanners vuln,secret,misconfig .`, plus `npm audit --omit=dev` or `pip-audit` as they apply.
- **What actually runs**: the deployed release SHA (`readlink /srv/<app>/current`, or the image tags), compared with `main`. Then `trivy image` on the deployed images.
- **Hosts**: `ansible -i inventories/<env> all -b -m shell -a '…'` with read-only commands: pending security updates (`apt list --upgradable 2>/dev/null` or `unattended-upgrade --dry-run`), `lynis audit system --quick --no-colors` (just the warnings and suggestions), whether a reboot is required, open ports (`ss -tlnp`), TLS certificate expiry, and the sshd and ufw settings compared with the `base` role.
- **Ansible itself**: `ansible-lint`, and pinned collection versions in `requirements.yml`.

## 2. Triage → GATE

Show one table, sorted by real risk:

| ID | Where | Package / setting | Severity (CVSS) | Exploitable here? | Fix version / action | Effort |
|---|---|---|---|---|---|---|

Judge "exploitable here" honestly. A vulnerable code path the app never calls, or a dev-only dependency, counts for less. In `report` mode, write `docs/security/<YYYY-MM-DD>.md` and stop here. In `fix` mode, ask the user which items to fix now.

## 3. Fix (only in `fix` mode, only the approved items)

- Create a branch: `security/<YYYY-MM-DD>`.
- **Dependencies**: make the smallest bump that fixes the issue, preferring patch, then minor. A major upgrade becomes a separate item that you discuss with the user first. Update the lock files and read the changelog for breaking changes.
- **Host issues**: change the Ansible **roles** (the `base` role for hardening and updates). Never fix a server by hand.
- **No fix available**: propose a mitigation (config, WAF rule, disabling a feature) or a replacement library, and record the accepted risk.
- Run `make check`. Then delegate to `web-pipeline:security-reviewer` for one review of the diff. This is a single pass, not a loop.
- Do not apply anything to servers yourself. Deploys are user-triggered: the user runs `/web-pipeline:deploy staging`, which does `--check --diff` first.

## 4. Hand-off

Write `docs/security/<YYYY-MM-DD>.md` with the findings, what was fixed, what was deferred and why, and the accepted risks. Tell the user the next steps: `/web-pipeline:deploy staging`, check it, then `/web-pipeline:deploy production`. **Never deploy to production from this skill.**

## Scheduling

For a regular report, set up a schedule with the `schedule` skill, or a cron entry such as `claude -p "/web-pipeline:secure-maintain report production"` run in the project directory. Scheduled runs must use `report` mode. For routine patch bumps, Renovate or Dependabot is cheaper. This skill covers what they cannot: triage in context, majors, CVEs with no patch, and host configuration.
