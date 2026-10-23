---
name: review-loop
description: Bounded multi-reviewer review-and-fix loop with a hard round cap (default 2), structured verdicts and diff-only re-review. Use when an orchestrator or the user wants code reviewed by independent subagents and the findings fixed without endless iteration.
argument-hint: "[max-rounds]"
---

# Bounded review loop

Run independent reviewers, fix what matters, and stop. The cap is the point: a loop that can always find one more nitpick never converges, so the procedure, not the reviewers, decides when it ends.

## Inputs (from the caller)

- **Reviewers**: subagent names to run in parallel, such as `web-pipeline:code-reviewer`.
- **Fixers**: which subagent fixes which area, such as backend files → `web-pipeline:backend-dev`.
- **Base**: the snapshot or git ref the work started from.
- **Context docs**: paths to the spec, architecture and design docs the reviewers check against.
- **Check command**: the project's quality gate, usually `make check`.
- **Max rounds**: `$ARGUMENTS` if given, otherwise **2**.

## State

Keep state in `.claude/state/review-loop.json` so the cap survives context compaction and session restarts:

```json
{ "round": 1, "max_rounds": 2, "base": "<tree>", "round_start": "<tree>", "open": [], "deferred": [] }
```

Take snapshots with `git-snapshot` (shipped in dev-core's `bin/`, so it is on PATH), which prints a git tree hash without touching the index or history. `git diff <a> <b>` compares two snapshots.

If the state file already shows `round > max_rounds`, do not review again. Report the open findings and stop.

## Verdict format (required from every reviewer)

Tell each reviewer to end its reply with exactly one fenced `json` block:

```json
{
  "reviewer": "code-reviewer",
  "findings": [
    {
      "id": "CR-1",
      "severity": "blocker | major | minor",
      "file": "src/app/orders.ts",
      "line": 42,
      "problem": "what is wrong, concretely",
      "evidence": "the code or the failing scenario",
      "fix": "the smallest change that resolves it"
    }
  ]
}
```

Severity rules to pass to reviewers:
- **blocker**: wrong behavior, data loss, security hole, broken acceptance criterion, failing check.
- **major**: clear violation of the project standards that will cost real time later, such as duplication of existing code, a missing test for a core path, or a hand-rolled version of something a dependency already provides.
- **minor**: style, naming, nice-to-have refactors.

## Round 1: full review of the change

1. Snapshot the tree as `round_start`. The review scope is `git diff <base> <round_start>`.
2. Launch all reviewers **in parallel, in one message**. Each delegation message is self-contained, because subagents do not see this conversation. It names the diff command, the context docs and the verdict format.
3. **Triage it yourself before fixing anything.** Merge duplicates across reviewers. Drop any finding that has no concrete file and line, that lies outside the diff and was not caused by it, or that contradicts an approved decision in the spec or an ADR. Note each dropped finding with its reason.
4. Send the **blockers and majors** to the fixers, grouped by area. Run the check command. Minors go to `deferred`.
5. Set `round = 2` in the state file.

## Round 2: re-review only the fixes

1. Snapshot again. The scope is **only** `git diff <round_start> <new snapshot>`, the fixes.
2. Reviewers get the fix diff plus the list of round-1 findings. They confirm each finding as resolved or unresolved. They may raise **new** findings only for problems the fix diff itself introduced.
3. Fix the remaining **blockers only**. Majors and minors go to `deferred`. Run the check command.
4. Set `round = 3`.

## Stop

- Stop after round 2, or earlier when a round has no blockers and no majors.
- **Never start round 3 on your own.** Present what is left: unresolved blockers, if any, plus deferred majors. Let the user decide. If they explicitly ask for another round, raise `max_rounds` by one in the state file and run one more round 2-style pass.
- Append deferred minors to `TODO.md` under a dated heading.
- Report in a few lines: findings per reviewer, how many were fixed, deferred and dropped, and the final check status.

If a fixer's attempt at a blocker fails the check twice, re-delegate that one fix once with the Agent tool's `model: "opus"` override. If the same blocker survives both rounds, do not try a third approach silently. Describe it to the user with the two attempts and ask how to proceed.
