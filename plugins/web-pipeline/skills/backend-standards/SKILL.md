---
name: backend-standards
description: Backend engineering standards for this user's web projects - DRY/KISS/YAGNI/SOLID applied pragmatically, reuse-first, contract-first APIs, validation, error model, data access, security baseline, observability and the tools that enforce them. Load for backend design, implementation or review.
---

# Backend standards

## Before every module

Run the `dev-core:reuse-first` protocol: the project, then the standard library or framework, then a maintained library, and only then custom code. Leave a `reuse:` note in your hand-off.

## Principles, applied pragmatically

- **KISS**: the simplest design that meets the acceptance criteria. No speculative layers, plugin systems or generic repositories "for later".
- **DRY with the rule of three**: abstract on the third repetition. Duplicated *knowledge*, such as business rules, constants or validation, is fixed at the second copy. Duplicated *shape* waits for the third.
- **YAGNI**: build no feature, flag or config option that the spec does not ask for.
- **SOLID where it pays**: single responsibility per module, dependencies passed in rather than imported globals for anything with I/O, small interfaces at the boundaries.
- **A functional core with an imperative shell**: business rules are pure functions or methods with no I/O. Handlers, jobs and adapters do the I/O and call the core.
- **Explicit over clever**: no metaprogramming magic, no hidden global state, no boolean flag arguments that switch behavior.
- **Fail fast**: validate at the edge, assert invariants, never swallow errors. A `catch` either handles the error or adds context and rethrows.

## Structure

Organize by feature (vertical slices), not by technical layer, once the project has more than a handful of modules:

```
src/
  orders/          # one feature: routes, service, domain, repo, tests
    api.ts | routes.py
    service.ts     # use cases, orchestrates the domain and repos
    domain.ts      # pure rules
    repo.ts        # data access only
    orders.test.ts
  shared/          # only code used by 2+ features; it must earn its place
```

Dependencies point inward: api → service → domain. The repo is injected into the service. Enforce this with `dependency-cruiser` or `import-linter` in `make check`.

## APIs

- **Contract first**: write the OpenAPI spec or typed route schemas before the handlers, and generate the client types from it.
- Validate every input at the boundary with a schema library: zod or valibot in TypeScript, pydantic in Python. Never trust the client.
- Report errors in one format, RFC 9457 Problem Details (`type`, `title`, `status`, `detail`), with stable machine-readable codes. Never leak stack traces.
- Use correct status codes; make retried POSTs idempotent (idempotency keys) where clients may retry; use cursor pagination for lists that grow.
- Version only when a breaking change is unavoidable.

## Data

- Migrations through the stack's standard tool (Prisma/Drizzle migrations, Alembic, Django migrations), forward-only and reviewed. No schema changes outside migrations.
- Parameterized queries or an ORM only. **Never build SQL by concatenating strings.**
- Transactions around multi-write use cases. Make the right indexes part of the feature, not an afterthought.
- Store timestamps in UTC; store money as integer minor units or decimal, never float.

## Configuration and secrets

- Follow the 12-factor approach: configuration comes from the environment and is validated at startup with a schema, so the app crashes if anything is missing.
- Secrets never go in the repo or in logs. Locally they live in a `.env` file covered by `.gitignore`, with a committed `.env.example`. On servers they come from Ansible Vault (see `ansible-conventions`).

## Security baseline

- Use a proven auth library or framework built-in. **Never hand-roll sessions, JWT handling or password storage.** Hash passwords with argon2id.
- Session cookies are `HttpOnly`, `Secure` and `SameSite=Lax` or stricter. Protect cookie-authenticated mutations against CSRF.
- Check authorization on every resource access (object-level), not just authentication.
- Rate-limit auth and expensive endpoints. Set request size limits. Validate file uploads by content, never by extension, and store them outside the web root.
- Send security headers: CSP, HSTS, X-Content-Type-Options, Referrer-Policy, frame-ancestors. Use a strict CORS allowlist.
- Give the database user least privilege. Keep dependencies pinned through lock files.

## Observability

- Structured JSON logs with a request id; no personal data or secrets in logs.
- `GET /healthz` (liveness) and `GET /readyz` (dependencies reachable). The deploy smoke tests use both.
- Clear error tracking hook-up points; Sentry or similar only if the spec allows it.

## Enforcement (wire into `make check`)

| Concern | TypeScript / Node | Python |
|---|---|---|
| Lint and format | `eslint` + `prettier`, or `biome` | `ruff check` + `ruff format` |
| Types | `tsc --noEmit` (strict) | `mypy --strict` or `pyright` |
| Tests | `vitest` / `jest` | `pytest` |
| Duplication | `jscpd` | `jscpd` |
| Dead code | `knip` | `vulture` |
| Architecture boundaries | `dependency-cruiser` | `import-linter` |
| SAST | `semgrep --config auto` | `semgrep --config auto`, `bandit` |
| Secrets | `gitleaks detect` | `gitleaks detect` |
| Dependencies | `npm audit` / `pnpm audit`, `osv-scanner` | `pip-audit`, `osv-scanner` |

## Definition of done (per task)

The acceptance criteria are covered by tests · `make check` is green · there are no TODOs without a tracking entry · the `reuse:` note is written · public functions and endpoints have clear names and docstrings only where the *why* is not obvious · migrations are included · `.env.example` is updated if the configuration changed.
