---
name: change
description: Improve or rework an existing web project - audit the codebase, interview only about the change, update the content plan when public pages change, plan with impact analysis, implement, quality gates, bounded review and local hand-off, with user approval gates. Use when the user wants a feature, fix, refactor or redesign in an existing project.
disable-model-invocation: true
argument-hint: "[what to change]"
---

# Change an existing web project

You orchestrate from the main conversation. Subagents do the heavy work. The user approves at every **GATE**. Talk to the user in their language.

Requested change: $ARGUMENTS

## Resume first

If `.claude/state/pipeline.json` exists with `"flow": "change"`, tell the user where the last run stopped and continue from there.

## Phase 0: Audit (facts before questions)

1. If `.claude/web-pipeline.json` is missing, invoke the `web-pipeline:init` skill. On a legacy codebase, init sets anti-slop to check only changed files.
2. If `docs/architecture.md` is missing or stale, delegate to `web-pipeline:architect` in **audit mode**. It writes an as-is `docs/architecture.md`: the stack, the modules and their boundaries, the existing utilities and shared components worth reusing, the test setup, how deploys work (`deploy/ansible`), and known debt. If it is current, read it yourself.
3. Create a branch: `change/<short-slug>`.
4. Write `.claude/state/pipeline.json`: `{ "flow": "change", "phase": "requirements", "change_doc": "docs/changes/NNNN-<slug>.md" }`. NNNN is the next free number.

## Phase 1: Interview about the change only

Invoke the `dev-core:grill-me` skill on the requested change. Give it the audit as known facts: never ask the user anything the code already answers. Cover the behavior change and its acceptance criteria, who is affected, compatibility (data migrations, API consumers, URLs and SEO), rollout (a feature flag or not), and what must not change. If the change adds, removes or renames public pages, or changes what they say, also cover what the affected pages must convey and the one action they ask for.

Output: the change doc at the path in the state file, using the template at `${CLAUDE_PLUGIN_ROOT}/templates/change.md`.

## Phase 2: Content (only if public pages or their copy change)

Delegate to `web-pipeline:content-strategist` in update mode with the change doc and `docs/content.md`. It updates the affected pages in `docs/content.md` (the message, sections, copy, metadata), or writes the file for those pages if it is missing, and records a 301 redirect for every renamed or removed URL. Skip this phase for changes that touch no public page and no user-facing copy.

## Phase 3: Impact and plan → GATE 1

Delegate to `web-pipeline:architect` with the change doc, `docs/architecture.md` and, if it exists, `docs/content.md`. It adds to the change doc: the impact analysis (touched modules, migrations, contract changes, risk), the build-vs-reuse decisions, and a task plan. If a decision is architectural, it also writes an ADR. It updates `docs/plan.md`, or writes the plan inside the change doc for small changes.

Present the impact, the risks and the plan, plus the content changes and redirects if Phase 2 ran. **GATE 1**: get explicit approval.

## Phase 4: Design (only if the UI changes)

- **Small UI change**: no gate. The frontend follows `docs/design.md`, and the copy in `docs/content.md` when it exists. If that file does not exist, delegate to `web-pipeline:designer` to extract one from the current UI first.
- **New screens or a visual overhaul**: delegate to `web-pipeline:designer`. It makes 2–3 concepts within the existing design system, or radical ones if the user asked for a redesign. **GATE 2**: the user picks, and the designer updates `docs/design.md`.

## Phase 5 onward: Delivery

Snapshot with `git-snapshot` (from dev-core, on PATH) and save the hash as `implementation_base` in the state file. Then read `${CLAUDE_PLUGIN_ROOT}/shared/delivery-phases.md` and follow D2–D5. Run D1 only if `make check` is missing or broken. Skip D2 when the API contract is unchanged.

Extra rules for existing code:
- Follow the conventions already in the codebase, even where the standards would differ, unless the change doc says to migrate. Note a conflict as a deferred finding. Do not rewrite code you were not asked to touch.
- Any behavior that must not change gets a characterization test **before** it is modified.
