#!/usr/bin/env bash
# PostToolUse(Write|Edit): format, then lint the edited file. Lint errors go back to Claude
# (exit 2 + stderr) so it fixes them right away; the edit itself is never blocked.
set -uo pipefail
source "$(dirname "$0")/lib.sh"
read_hook_input
opted_in || exit 0

file=$(jq -r '.tool_input.file_path // empty' <<<"$HOOK_INPUT")
[[ -n $file && -f $file ]] || exit 0
case "$file" in "$PROJECT"/*) ;; *) exit 0 ;; esac
case "$file" in */node_modules/*|*/.git/*|*/dist/*|*/build/*|*/.claude/*|*/.venv/*) exit 0 ;; esac

ext=".${file##*.}"
jq -e --arg e "$ext" '(.lint_extensions // []) | index($e) != null' "$CONFIG" >/dev/null || exit 0

format_cmd=$(config_get '.commands.format_file')
lint_cmd=$(config_get '.commands.lint_file')

[[ -n $format_cmd ]] && run_template "$format_cmd" "$file" >/dev/null

if [[ -n $lint_cmd ]]; then
  if ! output=$(run_template "$lint_cmd" "$file"); then
    {
      echo "Lint failed for ${file#"$PROJECT"/} - fix before moving on:"
      tail -n 60 <<<"$output"
    } >&2
    exit 2
  fi
fi
exit 0
