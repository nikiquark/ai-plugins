# Delivery phases (shared by `new-project` and `change`)

These phases run after the plan is approved. The orchestrator (the main conversation) delegates and tracks. It does not write application code itself, except for trivial glue between finished pieces.

## Delegation rules

- Subagents do not see the conversation. Every delegation message must stand on its own: give the task id, the paths to `docs/spec.md` (or the change doc), `docs/architecture.md`, `docs/design.md` and `docs/plan.md`, the acceptance criteria, and what to return.
- Pass **paths, not pasted content**.
- Ask each implementer to return: the files it changed, the tests it added, its `reuse:` notes, the check status, and anything it could not do.
- Run independent delegations in parallel, in one message. Run dependent ones in sequence.
- Update `.claude/state/pipeline.json` (`phase`, `current_task`) after each step, so a new session can resume.

## Models and effort

Each agent's frontmatter sets its own model and effort to fit its job. Opus handles decisions and review (architect, designer, the reviewers). Sonnet writes code. Haiku handles bulk scanner output. Do not override those defaults with the Agent tool's `model` parameter, except for the one escalation step in D3. Claude Fable is never used automatically. Suggest it to the user only when a problem survived the Opus escalation.

## Context hygiene

The main conversation is the orchestrator. Keep it lean: model quality degrades as the context fills, and auto-compaction is lossy.
- Never read whole source files, long logs or full test output in the main conversation. Delegate to subagents and keep only their summaries.
- The state file and the `docs/` files are the pipeline's memory, so a fresh session loses nothing. **Clean restart points** are: after GATE 1, after GATE 2, between tasks in D3, and before D4.
- At a restart point, if the conversation is long, or the context-guard hook reports 50% or more, save the state and tell the user: "Run `/clear`, then `/web-pipeline:<same command>`. It resumes from `<phase>`." Recommend `/clear` over `/compact`, because the files already hold everything that matters.

## D1. Scaffold and quality gate (new projects, or projects missing one)

Delegate to `web-pipeline:backend-dev`, with the frontend parts going to `web-pipeline:frontend-dev`. Set up the skeleton from `docs/architecture.md`, plus a working `make check` that runs:
lint · format check · type check · unit tests · duplication (`jscpd`) · dead code (`knip` / `vulture`) · `semgrep --config auto` · `gitleaks detect` · dependency audit · `python3 scripts/anti_slop.py` · `ansible-lint` (when `deploy/ansible` exists).

A tool that is not installed must fail the check with an install hint. It must not be skipped silently. Confirm that `make check` passes on the skeleton. Then set `stop_gate.enabled` to `true` in `.claude/web-pipeline.json`, and fill in `format_file`, `lint_file` and `lint_extensions` for the chosen stack. From now on, the Stop hook blocks finishing while the check is red.

## D2. Contract first

Delegate the API contract to `web-pipeline:backend-dev`: an OpenAPI spec, or typed route schemas for full-stack frameworks. Generate the client types from it. From this point, frontend work builds on the contract and does not wait for the backend.

## D3. Implement the plan

For each task in `docs/plan.md`, in dependency order:
1. Delegate it to `web-pipeline:backend-dev` or `web-pipeline:frontend-dev`. When a backend task and a frontend task are independent, run them in parallel.
2. When the implementer reports back, run `make check` yourself. If it fails, send the output back to the same implementer once. If it fails again, **escalate once**: re-delegate the task with the Agent tool's `model: "opus"` override and a summary of both failed attempts. If that also fails, stop and tell the user.
3. Tick the task in `docs/plan.md`.

As soon as the contract and the acceptance criteria exist, delegate to `web-pipeline:qa-engineer` in parallel. It writes the Playwright e2e tests **from the spec**, not from the implementation.

## D4. Bounded review

Invoke the `dev-core:review-loop` skill with:
- reviewers: `web-pipeline:code-reviewer`, `web-pipeline:security-reviewer`, plus `web-pipeline:design-critic` when the UI changed;
- fixers: backend files → `web-pipeline:backend-dev`, frontend files → `web-pipeline:frontend-dev`, e2e tests → `web-pipeline:qa-engineer`;
- base: the `implementation_base` snapshot from `.claude/state/pipeline.json`;
- check command: `make check`;
- max rounds: 2.

## D5. Local hand-off (gate)

Stop and give the user:
- how to run it locally (`make dev` or the equivalent) and the URL;
- a short checklist of what to look at, taken from the acceptance criteria;
- what the review loop deferred, and anything in `TODO.md`;
- the next step: run `/web-pipeline:deploy staging` once they are happy.

Do not deploy, push or tag anything yourself.
