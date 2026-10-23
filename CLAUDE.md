# ai-plugins

A Claude Code plugin marketplace (`nikiquark-ai-plugins`). Plugins live in `plugins/<name>/`, and each is listed in `.claude-plugin/marketplace.json`.

## Conventions

- Shared logic belongs in `dev-core`. Domain plugins (such as `web-pipeline`) declare `"dependencies": ["dev-core"]` and reference shared skills by their namespaced names (`dev-core:review-loop`). Never copy a skill between plugins.
- Plugin hooks fire in every project, so each domain plugin gates its hooks on an opt-in marker file in the project (`.claude/<plugin>.json`).
- Plugin agents ignore `permissionMode`, `hooks` and `mcpServers`. Make a pure reviewer (an agent that never writes, such as web-pipeline's code-reviewer) read-only with `disallowedTools`. An agent that reviews in one mode and writes its own files in another (such as idea-pipeline's red-team and fact-checker) gets a `tools` allowlist instead, and its review mode forbids edits in the agent body.
- `${CLAUDE_PLUGIN_ROOT}` is substituted in skill and agent text and is exported to hooks, but it is **not** present in the Bash tool's environment. Executables that Claude must run go in the plugin's `bin/`.
- Installed plugins live in per-version cache directories, so never reference a sibling plugin by a relative path.
- Every pipeline keeps its resumable state in `.claude/state/pipeline.json` in the project. dev-core's context-guard hook keys off that file. Orchestrator skills must be resumable from the state file and the docs, so that `/clear` and re-running the command loses nothing. Each orchestrator resumes only its own `flow` and stops when the file holds another one, so pipelines never overwrite each other's state.
- Plugin hooks fire in every project, so a plugin without hooks (such as `idea-pipeline`) needs no opt-in marker. Its `.claude/<plugin>.json` then holds settings only.
- Skill and agent bodies are written in English. User-facing docs (README and `src/content/docs/`) are written in Russian.
- After any change, run `claude plugin validate .` and bump `version` in the changed plugin's `plugin.json`.
- The docs site in `src/content/docs/` (Astro Starlight, published to GitHub Pages) is written by hand. When you change a plugin, update its pages in the same change: every skill, agent and `bin/` file has its own page, and new pages go into `sidebar` in `astro.config.mjs`. Check with `python3 scripts/check-docs.py && npm run build`.
