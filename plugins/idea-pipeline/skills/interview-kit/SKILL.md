---
name: interview-kit
description: Prepare customer interviews for an idea researched with idea-pipeline - a Mom Test script tied to the hypotheses being tested, a screener, the channels to find respondents with first messages, the target number of interviews from the gate, and the note-taking flow. Use before problem or solution interviews.
argument-hint: "[segment]"
---

# Prepare an interview kit

Talk to the user in their language.

Segment: $ARGUMENTS

## Steps

1. If `docs/idea/customers.md` or `docs/idea/experiments.md` is missing, point the user to `/idea-pipeline:new-idea` and stop.
2. **Choose the segment**: the one in the arguments, or else the beachhead from `docs/idea/strategy.md`. Confirm it with the user if `customers.md` lists a closer match.
3. **Choose the experiment**: the interview experiment of the current stage in `docs/idea/experiments.md`, with the leaves it tests. If there is none, ask the user which leaves the interviews should test and what the pass and kill thresholds are, and add the experiment to `docs/idea/experiments.md` before the script is written: pre-registration comes first.
4. Delegate to `idea-pipeline:customer-researcher` in **interview-kit mode** with the segment, the leaf ids, the experiment id, and the paths to `docs/idea/customers.md`, `docs/idea/issue-tree.md`, `docs/idea/readiness.md` and `.claude/idea-pipeline.json`. It writes `docs/idea/interviews/script-<segment-slug>.md`.
5. Give the user the path and a short summary: the number of interviews to run, the channels to recruit from, and the three questions that matter most.
6. Remind them of the rules that make interviews count as evidence: no pitching, ask about the past, count commitments rather than compliments. Each interview goes in as an evidence note with `/idea-pipeline:evidence` on the same day.
