# agents-setup

A Claude Code plugin marketplace (`nikiquark-agents`). Plugins live in `plugins/<name>/`, and each is listed in `.claude-plugin/marketplace.json`.

## Conventions

- Shared logic belongs in `dev-core`. Domain plugins (`web-pipeline`, `science-pipeline`) declare `"dependencies": ["dev-core"]` and reference shared skills by their namespaced names (`dev-core:review-loop`). Never copy a skill between plugins.
- Plugin hooks fire in every project, so each domain plugin gates its hooks on an opt-in marker file in the project (`.claude/<plugin>.json`).
- Plugin agents ignore `permissionMode`, `hooks` and `mcpServers`. Make agents read-only with `disallowedTools`.
- `${CLAUDE_PLUGIN_ROOT}` is substituted in skill and agent text and is exported to hooks, but it is **not** present in the Bash tool's environment. Executables that Claude must run go in the plugin's `bin/`.
- Installed plugins live in per-version cache directories, so never reference a sibling plugin by a relative path.
- Every pipeline keeps its resumable state in `.claude/state/pipeline.json` in the project. dev-core's context-guard hook keys off that file. Orchestrator skills must be resumable from the state file and the docs, so that `/clear` and re-running the command loses nothing.
- Skill and agent bodies are written in English. User-facing docs (README) are written in Russian.
- After any change, run `claude plugin validate .` and bump `version` in the changed plugin's `plugin.json`.
