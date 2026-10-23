---
name: ansible-conventions
description: Conventions for deploying and hardening this user's web projects with Ansible - repo layout, inventories, vault, idempotent roles, atomic releases with rollback, base hardening role, check/diff-first workflow. Load when writing deploy code, deploying or changing servers.
---

# Ansible conventions

## Layout (in each project)

```
deploy/ansible/
  ansible.cfg
  requirements.yml                # pinned collections and roles
  inventories/
    staging/hosts.yml
    staging/group_vars/all/{vars.yml,vault.yml}
    production/hosts.yml
    production/group_vars/all/{vars.yml,vault.yml}
  roles/
    base/                         # hardening: users, ssh, ufw, fail2ban, unattended-upgrades, time sync
    app/                          # app runtime, release dirs, systemd or compose
    proxy/                        # nginx/caddy, TLS, security headers
    db/                           # only if self-hosted
    backup/
  playbooks/
    site.yml                      # full converge (base + all roles)
    deploy.yml                    # app release only
    rollback.yml                  # switch to the previous release
    smoke.yml                     # health checks from the control host
```

## Rules

- **Every change to a server goes through a role.** No ad-hoc fixes by SSH. A fix made by hand must be written back into a role straight away.
- **Idempotent**: a second run reports `changed=0`. Prefer modules over `shell`/`command`. When `shell` is unavoidable, add `creates:`/`removes:` or `changed_when:`.
- **Check first**: `ansible-playbook … --check --diff` precedes every real run, and the user sees the diff. The plugin's guard hook asks for confirmation on any run without `--check`.
- **Secrets** live in `vault.yml`, encrypted with `ansible-vault`, and are referenced as `vault_*` variables from `vars.yml`. Never print vault contents and never pass the vault password on the command line. Use `--vault-password-file` pointing outside the repo, or `--ask-vault-pass`.
- **Pin versions**: collections in `requirements.yml`, packages where it matters, container images by tag and digest.
- `ansible-lint` runs in `make check` (production profile).
- Use tags for partial runs (`--tags app`), handlers for restarts, and `serial` plus health-check `until:` loops for multiple hosts.
- Target only hosts in this project's inventory. Never scan or touch anything else.

## Atomic releases and rollback

```
/srv/<app>/releases/<timestamp>-<gitsha>/
/srv/<app>/shared/        # .env, uploads, persisted state
/srv/<app>/current -> releases/<…>
```

`deploy.yml` uploads or builds into a new release directory, links `shared/`, runs migrations (forward-only), switches `current` atomically, restarts through a handler, waits for `/readyz`, and keeps the last 5 releases. `rollback.yml` points `current` back at the previous release and restarts. A migration that cannot be rolled back must be flagged before the deploy.

For containerized apps, the equivalent is a `docker compose` stack whose image tags are pinned per release, with the previous tag recorded for rollback.

## The base role (hardening)

- A non-root deploy user with key-only SSH. Disable `PasswordAuthentication` and `PermitRootLogin`.
- `ufw` allows only 22 (or a custom SSH port), 80 and 443.
- `fail2ban` protects sshd.
- `unattended-upgrades` installs security updates, with automatic reboot during a set window if the user allows it.
- `chrony` for time sync, `logrotate`, and a swap file if memory is low.
- TLS through certbot or Caddy, with auto-renew checked by a timer.
- The proxy sends security headers: HSTS, CSP, X-Content-Type-Options, Referrer-Policy, Permissions-Policy, frame-ancestors.
