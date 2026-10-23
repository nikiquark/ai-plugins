#!/usr/bin/env bash
# UserPromptSubmit / PostToolUse(Agent): when a pipeline is active and the main conversation's
# context passes CONTEXT_WARN_PCT (default 50), tell the orchestrator to steer the user to
# /clear + resume at the next phase boundary. Warns once per 10% band.
#
# Reads the percentage cached per session by the user's status line script
# (~/.claude/statusline.sh); silent when that cache or an active pipeline is missing.
set -uo pipefail
input=$(cat)
sid=$(jq -r '.session_id // empty' <<<"$input")
event=$(jq -r '.hook_event_name // empty' <<<"$input")
agent=$(jq -r '.agent_id // empty' <<<"$input")
project=${CLAUDE_PROJECT_DIR:-$(jq -r '.cwd // empty' <<<"$input")}

[[ -n $sid && -z $agent && -f $project/.claude/state/pipeline.json ]] || exit 0

cache=${XDG_CACHE_HOME:-$HOME/.cache}/claude-context
pct=$(cat "$cache/$sid" 2>/dev/null) || exit 0
[[ $pct =~ ^[0-9]+$ ]] || exit 0

if (( pct < ${CONTEXT_WARN_PCT:-50} )); then
  rm -f "$cache/$sid.band"
  exit 0
fi
band=$(( pct / 10 * 10 ))
[[ $(cat "$cache/$sid.band" 2>/dev/null) == "$band" ]] && exit 0
echo "$band" >"$cache/$sid.band"

msg="Context is at ${pct}% of the window, and answer quality degrades as it fills. At the next phase boundary or gate: bring .claude/state/pipeline.json and the docs up to date, then recommend that the user run /clear and re-run the pipeline command to resume from the state file. Until then, delegate anything bulky to subagents and avoid reading large files or long outputs in the main conversation."
jq -n --arg e "$event" --arg m "$msg" '{hookSpecificOutput: {hookEventName: $e, additionalContext: $m}}'
