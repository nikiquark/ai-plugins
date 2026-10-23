#!/usr/bin/env bash
# PreToolUse(Bash): commands that change servers or history need the user's explicit OK.
# Active in every project (it only ever asks or denies, never runs anything).
set -uo pipefail
cmd=$(jq -r '.tool_input.command // empty')

decide() {  # <ask|deny> <reason>
  jq -n --arg d "$1" --arg r "$2" \
    '{hookSpecificOutput: {hookEventName: "PreToolUse", permissionDecision: $d, permissionDecisionReason: $r}}'
  exit 0
}

if grep -Eq '\brm[[:space:]]+-[a-zA-Z]*r[a-zA-Z]*[[:space:]]+(/|~|\$HOME)/?(\*)?([[:space:]]|$)' <<<"$cmd"; then
  decide deny "Recursive delete of / or the home directory is never allowed."
fi

if grep -Eq '(^|[;&|(][[:space:]]*|[[:space:]])ansible-playbook([[:space:]]|$)' <<<"$cmd" \
  && ! grep -Eq '(^|[[:space:]])(--check|-C|--syntax-check|--list-hosts|--list-tasks)([[:space:]]|$)' <<<"$cmd"; then
  decide ask "ansible-playbook without --check changes real servers. Approve only if this is the deploy you agreed to."
fi

if grep -Eq '\bgit[[:space:]]+push\b.*([[:space:]]--force(-with-lease)?\b|[[:space:]]-f([[:space:]]|$))' <<<"$cmd"; then
  decide ask "Force push rewrites remote history."
fi

exit 0
