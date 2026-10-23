#!/usr/bin/env bash
# Shared helpers for web-pipeline hooks. Every hook is a no-op unless the project opted in
# by creating .claude/web-pipeline.json (see the init skill), so other projects are untouched.

# read_hook_input: stores the hook's JSON stdin in $HOOK_INPUT and resolves $PROJECT / $CONFIG.
read_hook_input() {
  HOOK_INPUT=$(cat)
  PROJECT=${CLAUDE_PROJECT_DIR:-$(jq -r '.cwd // empty' <<<"$HOOK_INPUT")}
  CONFIG="$PROJECT/.claude/web-pipeline.json"
}

opted_in() { [[ -n ${PROJECT:-} && -f $CONFIG ]]; }

config_get() { jq -r "$1 // empty" "$CONFIG" 2>/dev/null; }

# run_template <template-with-{file}> <file>: runs a project command with the file path shell-quoted.
run_template() {
  local quoted
  quoted=$(printf '%q' "$2")
  (cd "$PROJECT" && timeout "${3:-60}" bash -c "${1//\{file\}/$quoted}" 2>&1)
}
