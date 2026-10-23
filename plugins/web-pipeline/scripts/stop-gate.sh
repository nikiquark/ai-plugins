#!/usr/bin/env bash
# Quality gate: run the project's check command (make check) before Claude, or an implementer
# subagent, may finish. Designed not to loop or nag:
#   - only runs when code changed since the last passing check or the last gate run;
#   - doc-only changes (docs/, *.md, .claude/) never trigger it;
#   - stops blocking after stop_gate.max_blocks consecutive failures and tells the user.
#
# Modes:  stop-gate.sh             Stop / SubagentStop hook
#         stop-gate.sh --baseline  SessionStart hook: remember the starting tree, print nothing
set -uo pipefail
source "$(dirname "$0")/lib.sh"
read_hook_input
opted_in || exit 0
cd "$PROJECT" || exit 0
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || exit 0

STATE=.claude/state
mkdir -p "$STATE"

snapshot() {
  local idx
  idx="$(git rev-parse --git-dir)/gate-index.$$"
  {
    git rev-parse -q --verify HEAD >/dev/null && GIT_INDEX_FILE=$idx git read-tree HEAD
    GIT_INDEX_FILE=$idx git add -A -- . ':(exclude).claude/state'
    GIT_INDEX_FILE=$idx git write-tree
  } 2>/dev/null
  rm -f "$idx"
}

only_docs_changed() {  # <from-tree> <to-tree>
  [[ -n $1 ]] || return 1
  ! git diff --name-only "$1" "$2" 2>/dev/null | grep -qvE '^(docs/|\.claude/)|\.md$'
}

tree=$(snapshot)
[[ -n $tree ]] || exit 0

if [[ ${1:-} == --baseline ]]; then
  echo "$tree" >"$STATE/gate-main.seen"
  exit 0
fi

[[ $(config_get '.stop_gate.enabled') == false ]] && exit 0

event=$(jq -r '.hook_event_name // empty' <<<"$HOOK_INPUT")
key=main
if [[ $event == SubagentStop ]]; then
  agent=$(jq -r '.agent_type // empty' <<<"$HOOK_INPUT")
  [[ $agent =~ (backend-dev|frontend-dev|qa-engineer)$ ]] || exit 0
  key="agent-${agent##*:}"
fi

pass_file="$STATE/gate-pass.tree"
seen_file="$STATE/gate-$key.seen"
blocks_file="$STATE/gate-$key.blocks"
passed=$(cat "$pass_file" 2>/dev/null || true)
seen=$(cat "$seen_file" 2>/dev/null || true)

# Nothing relevant changed: already green, docs-only edits, or unchanged since the last gate run.
if [[ $tree == "$passed" ]] || only_docs_changed "$passed" "$tree"; then
  [[ -n $passed ]] && echo "$tree" >"$pass_file"
  exit 0
fi
if [[ $tree == "$seen" ]] || only_docs_changed "$seen" "$tree"; then
  echo "$tree" >"$seen_file"
  exit 0
fi
echo "$tree" >"$seen_file"

check_cmd=$(config_get '.commands.check')
check_cmd=${check_cmd:-make check}
limit=$(config_get '.stop_gate.timeout_seconds')
max_blocks=$(config_get '.stop_gate.max_blocks')

if output=$(timeout "${limit:-540}" bash -c "$check_cmd" 2>&1); then
  echo "$tree" >"$pass_file"
  rm -f "$blocks_file"
  exit 0
fi

blocks=$(( $(cat "$blocks_file" 2>/dev/null || echo 0) + 1 ))
if (( blocks > ${max_blocks:-3} )); then
  rm -f "$blocks_file"
  jq -n --arg m "web-pipeline: '$check_cmd' still fails after ${max_blocks:-3} fix attempts; the gate stopped blocking. Review the failures yourself." \
    '{systemMessage: $m}'
  exit 0
fi
echo "$blocks" >"$blocks_file"

reason="Quality gate failed ($check_cmd, attempt $blocks/${max_blocks:-3}). Fix the failures below, then finish. Do not disable checks or mark tests as skipped to get green.
$(tail -n 80 <<<"$output")"
jq -n --arg r "$reason" '{decision: "block", reason: $r}'
