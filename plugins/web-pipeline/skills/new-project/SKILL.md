---
name: new-project
description: Start a new web project end to end - requirements interview, architecture, bold design concepts, contract-first implementation, quality gates, bounded review and local hand-off, with user approval gates. Use when the user wants to build a new web app or site from an idea.
disable-model-invocation: true
argument-hint: "[idea in a few words]"
---

# New web project

You orchestrate this run from the main conversation. Specialist subagents do the heavy work. The user approves at every **GATE**: never skip one, and never treat silence as approval. Talk to the user in their language. Write the docs in the user's language too, unless they ask otherwise.

Idea: $ARGUMENTS

## Resume first

If `.claude/state/pipeline.json` exists, read it, tell the user which phase the last run stopped at, and continue from there instead of starting over.

## Phase 0: Bootstrap

1. If the directory is not a git repository, run `git init` (branch `main`).
2. Invoke the `web-pipeline:init` skill. It creates `.claude/web-pipeline.json`, the anti-slop script, the state directory and the CLAUDE.md section. The stack is unknown at this point, so init records it as "TBD", and Phase 2 fills it in.
3. Write `.claude/state/pipeline.json`: `{ "flow": "new-project", "phase": "requirements" }`.

## Phase 1: Requirements

Invoke the `dev-core:grill-me` skill on the idea. Output file: `docs/spec.md`, using the template at `${CLAUDE_PLUGIN_ROOT}/templates/spec.md`.

The design tree must cover at least: who the users are and what job they hire this for, the user stories with **testable acceptance criteria**, non-goals, the data and its sensitivity (personal data? payments?), integrations, auth model, expected load, languages and locales, SEO needs, hosting constraints (the user's own servers via Ansible), budget for paid services, and the visual mood. For the mood, ask for references they like and hate, not adjectives.

## Phase 2: Architecture → GATE 1

Delegate to `web-pipeline:architect` with the path to `docs/spec.md`. It returns `docs/architecture.md`, `docs/adr/NNNN-*.md`, and `docs/plan.md` (small tasks with acceptance criteria, in dependency order).

Present to the user: the stack and why, the build-vs-reuse table, the main risks, the number of tasks, and what was rejected. **GATE 1**: get explicit approval or changes. If they ask for changes, re-delegate with their feedback. Then update the stack in `.claude/web-pipeline.json` and in CLAUDE.md.

## Phase 3: Design concepts → GATE 2

Delegate to `web-pipeline:designer` with the paths to `docs/spec.md` and `docs/architecture.md`. It produces 3 deliberately different concepts in `docs/design/concepts/` (self-contained HTML), plus a summary of each: the name, the one bold idea, the palette, the type pairing, and the trade-offs.

Give the user the file paths. They open them in a browser. **GATE 2**: they pick one, or mix them ("A's type with C's layout"), or ask for a new round. When they choose, delegate to `web-pipeline:designer` again to write `docs/design.md` (tokens, type scale, layout rules, motion, component inventory) for the chosen direction.

## Phase 4 onward: Delivery

Snapshot the tree with `git-snapshot` (from dev-core, on PATH) and save the hash as `implementation_base` in `.claude/state/pipeline.json`.

Then read `${CLAUDE_PLUGIN_ROOT}/shared/delivery-phases.md` and follow phases D1–D5 exactly. D5 is the final gate.
