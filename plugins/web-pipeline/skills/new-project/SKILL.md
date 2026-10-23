---
name: new-project
description: Start a new web project end to end - requirements interview, message and content plan with SEO, architecture, bold design concepts, contract-first implementation, quality gates, bounded review and local hand-off, with user approval gates. Use when the user wants to build a new web app or site from an idea.
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
2. Invoke the `web-pipeline:init` skill. It creates `.claude/web-pipeline.json`, the anti-slop and SEO checkers, the state directory and the CLAUDE.md section. The stack is unknown at this point, so init records it as "TBD", and Phase 3 fills it in.
3. Write `.claude/state/pipeline.json`: `{ "flow": "new-project", "phase": "requirements" }`.

## Phase 1: Requirements

Invoke the `dev-core:grill-me` skill on the idea. Output file: `docs/spec.md`, using the template at `${CLAUDE_PLUGIN_ROOT}/templates/spec.md`.

The design tree must cover at least: who the users are and what job they hire this for, **the one thought a visitor must take away and the one action they should take**, the proof the user can back that up with, competitors or what people do today instead, whether the site must be found in search or is a closed app, the user stories with **testable acceptance criteria**, non-goals, the data and its sensitivity (personal data? payments?), integrations, auth model, expected load, languages and locales, hosting constraints (the user's own servers via Ansible), budget for paid services, and the visual mood. For the mood, ask for references they like and hate, not adjectives.

## Phase 2: Message and content

Delegate to `web-pipeline:content-strategist` in plan mode with the path to `docs/spec.md`. It writes `docs/content.md`: the core message, the primary action, the page map with URLs and indexing, page-by-page sections, copy and emphasis, the metadata (title, description, canonical, Open Graph, JSON-LD), and the robots and sitemap policy. Update `phase` in the state file. There is no gate here: the user approves the content together with the architecture at GATE 1.

## Phase 3: Architecture → GATE 1

Delegate to `web-pipeline:architect` with the paths to `docs/spec.md` and `docs/content.md`. It returns `docs/architecture.md`, `docs/adr/NNNN-*.md`, and `docs/plan.md` (small tasks with acceptance criteria, in dependency order).

Present to the user, in two parts:
- **Message**: the core message, the primary action, the page map, the home-page headline options with the recommended one, the robots policy, and the content's open questions.
- **Architecture**: the stack and why, how public pages are rendered, the build-vs-reuse table, the main risks, the number of tasks, and what was rejected.

**GATE 1**: get explicit approval or changes for both. If they change the message or the pages, re-delegate to `web-pipeline:content-strategist` with their feedback, and then to `web-pipeline:architect` if the page map changed. If they change the architecture, re-delegate to the architect. Then update the stack in `.claude/web-pipeline.json` and in CLAUDE.md, and mark `docs/content.md` approved.

## Phase 4: Design concepts → GATE 2

Delegate to `web-pipeline:designer` with the paths to `docs/spec.md`, `docs/content.md` and `docs/architecture.md`. It produces 3 deliberately different concepts in `docs/design/concepts/` (self-contained HTML), plus a summary of each: the name, the one bold idea, the palette, the type pairing, and the trade-offs.

Give the user the file paths. They open them in a browser. **GATE 2**: they pick one, or mix them ("A's type with C's layout"), or ask for a new round. When they choose, delegate to `web-pipeline:designer` again to write `docs/design.md` (tokens, type scale, layout rules, motion, component inventory) and the OG image template for the chosen direction.

## Phase 5 onward: Delivery

Snapshot the tree with `git-snapshot` (from dev-core, on PATH) and save the hash as `implementation_base` in `.claude/state/pipeline.json`.

Then read `${CLAUDE_PLUGIN_ROOT}/shared/delivery-phases.md` and follow phases D1–D5 exactly. D5 is the final gate.
