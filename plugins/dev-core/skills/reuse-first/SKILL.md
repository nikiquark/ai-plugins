---
name: reuse-first
description: Protocol to run before writing any new module, function, helper or component - check the project, the standard library/framework and maintained libraries before writing custom code. Use whenever about to implement new functionality.
---

# Reuse first

Before writing a new module, function, helper, hook or component, answer these four questions **in order**, and stop at the first "yes". This applies throughout the task, not just once at the start.

## 1. Does this project already have it?

Search by meaning, not just by name. A slugify helper might be called `toUrlPart`.
- Grep for the verb and the noun (`format.*date`, `retry`, `paginate`, `debounce`), and for the key library you would use to build it.
- Check the usual places: `utils/`, `lib/`, `common/`, `shared/`, `core/`, `helpers/`, base classes, middleware, existing hooks and components, and the design system.
- If something close exists, **extend or generalize it** rather than writing a sibling. If extending would make it worse, explain why in the reuse note.

## 2. Does the language or framework already do it?

Standard library, framework built-ins, ORM features, platform APIs. Examples: `Intl.DateTimeFormat`, `URLSearchParams`, `structuredClone`, Python `itertools`, `functools.cache` and `pathlib`, Django forms and validators, FastAPI dependencies, Next.js route handlers, and native browser `<dialog>`, form validation and CSS `:has()`.

## 3. Is there a well-maintained library?

Look up current docs through the Context7 MCP tools (`resolve-library-id`, then `get-library-docs`) so you use the real, current API, not a remembered one. Accept a library only if it meets all of these:
- a release or meaningful commit in roughly the last 12 months, and issues being answered;
- a license compatible with the project (MIT, BSD, Apache-2.0, ISC, MPL-2.0; flag GPL/AGPL to the user);
- no open high or critical advisories (`osv-scanner` or `npm audit` / `pip-audit` on the candidate);
- a reasonable footprint: not a framework pulled in for one function, and transitive dependencies checked.

Prefer a library the project already depends on over a new one that does it slightly better.

## 4. Only now, write it

Write the smallest thing that works (KISS), in the place where the next person will look for it.

## Balance DRY against KISS

- **Rule of three**: duplicate once, abstract on the third occurrence. Two similar blocks are not yet a pattern.
- Do not add a dependency for something that is about 10 obvious lines with no edge cases. Dependencies have upgrade, security and supply-chain costs. Do add one for anything with real edge cases: dates and time zones, crypto, auth, parsing, validation, retries with backoff, CSV, Markdown, i18n, sanitizing HTML.
- Never hand-roll crypto, password hashing, auth/session handling, HTML sanitization or SQL escaping.

## Reuse note

Leave a one-line trace in your hand-off summary (not in the code) for each new module:

```
reuse: <module> - project: none (searched utils/, lib/) · stdlib: n/a · library: date-fns (already a dep) → used
```

Reviewers check these notes. A missing note, or a hand-written version of something found in step 1–3, is a **major** finding.
