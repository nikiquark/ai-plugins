---
name: testing-standards
description: Testing standards for this user's web projects - TDD per task, test pyramid, behavior-focused tests, integration with real services, Playwright e2e from acceptance criteria, flakiness policy. Load when writing or reviewing tests.
---

# Testing standards

## Workflow

- **TDD per task**: write a failing test for the acceptance criterion, make it pass with the simplest code, then refactor while the tests stay green.
- Bug fixes start with a test that reproduces the bug.
- Code you change in a legacy area first gets a **characterization test** that pins down its current behavior.

## The pyramid

| Level | What it covers | Tools | Rules |
|---|---|---|---|
| Unit | Pure domain rules, utilities | vitest/jest, pytest | Fast, no network, no database, no clock (inject the clock) |
| Integration | Service + repo + real database, HTTP handlers | testcontainers or docker compose, supertest/httpx | A real database engine, never SQLite as a stand-in for Postgres; each test isolated by a transaction or truncation |
| Contract | Responses match the OpenAPI spec | schemathesis, or openapi validators in tests | Run against the real app |
| E2E | User journeys from the acceptance criteria | Playwright | Few, critical paths only; mobile and desktop viewports |

## Writing good tests

- Test **behavior through public interfaces**, not implementation details. A refactor that keeps behavior must not break the tests.
- Structure each test as Arrange, Act, Assert, with one behavior per test. Name tests after the behavior: `rejects_expired_coupon`, not `test_coupon_3`.
- Use factories or builders for test data, not giant shared fixtures.
- Mock only at the system boundaries: third-party APIs, email, payments. Never mock what you own just to make a test easier.
- No snapshot tests for logic. A snapshot is only acceptable for a small, stable serialized output.
- E2E tests use accessible selectors (`getByRole`, `getByLabel`), never CSS classes or nth-child.

## E2E from the spec (qa-engineer)

- Write one or more Playwright tests per acceptance criterion in `docs/spec.md` or the change doc, and tag each one with the AC id (`test('AC-1.2 …')`).
- Write them from the spec **before reading the implementation**, so they test what was asked for, not what was built.
- Cover at least: the happy path, one validation failure, an auth boundary (when it applies), and a mobile viewport (375 px).

## Coverage and flakiness

- Coverage is a signal, not a goal. Aim for ≥ 80% line coverage on the domain and service layers, and do not chase it on glue code.
- A flaky test is a bug. Fix it or quarantine it with a tracking entry in `TODO.md` within the same task. Never "retry until green", and never use `sleep` to wait for something; use proper waits.
- Never skip, delete or weaken a test to get the check green without telling the user.
