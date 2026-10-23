---
name: evidence
description: Record new evidence for an idea researched with idea-pipeline - an interview, expert call, smoke-test result, pre-order, letter of intent, pilot, survey or usage data - as an evidence note, rescore the KTH readiness levels, judge experiments against their locked thresholds, and run the stage gate (GO, ITERATE, PIVOT, KILL) when the evidence is in. Use after any contact with customers or any experiment result.
argument-hint: "[path to notes or results, or a short description]"
---

# Record evidence

Talk to the user in their language. Write the notes in the language of `docs/idea/brief.md`.

Evidence: $ARGUMENTS

## Before you start

If `docs/idea/readiness.md` or `.claude/idea-pipeline.json` is missing, the idea has not been researched yet: point the user to `/idea-pipeline:new-idea` and stop. Read the current `stage` and the experiments of that stage in `docs/idea/experiments.md`.

## 1. Get the raw material

Use the files or text the user gave. If they only described what happened, ask for the raw notes and the raw numbers (for example 14 sign-ups out of 310 visitors, not "about 5%"). One interview, call or result per note.

## 2. Write the evidence notes

For each piece, write `docs/idea/evidence/NNNN-<slug>.md` (NNNN is the next free number) using the template at `${CLAUDE_PLUGIN_ROOT}/templates/evidence-note.md`:
- facts only: what people said about their past and did; quotes in the original language;
- opinions about the future, compliments and "I would buy it" are noted as such and never counted as support;
- commitments given (time, introduction, data, pre-payment, letter of intent), or none;
- the experiment it belongs to, and the leaves it supports or refutes, with the reason;
- the raw numbers for the experiment's metric;
- no personal data beyond what is needed: role, segment and company size instead of names, unless the user asks otherwise.

Show the user the leaf mapping when it is a judgment call.

## 3. Rescore

Delegate to `idea-pipeline:fact-checker` in **assess mode** with the path to `docs/idea/`. Report the result in a few lines: the overall level and the weakest link, the axes that moved, the leaves whose status changed, and each experiment's verdict (pass, kill or inconclusive) against its thresholds.

If a refuted or newly validated leaf changes the picture in `customers.md` or `strategy.md`, offer to update them: delegate to `idea-pipeline:customer-researcher` or `idea-pipeline:strategist` in fix mode, with the evidence notes as `user-provided` sources. Do this only if the user agrees.

## 4. Gate (when the evidence is in)

Run the gate when every experiment of the current stage has a verdict, when a kill threshold is hit, or when the user asks.

Present the gate thresholds from `readiness.md` next to the measured values, with the evidence note ids. Point out any threshold changed after its results were seen (post-hoc). **GATE**: the user decides:
- **GO**: advance `stage` in `.claude/idea-pipeline.json` and in `readiness.md`. Delegate to `idea-pipeline:strategist` in memo mode to plan the next stage's experiments and refresh the memo.
- **ITERATE**: add or change experiments for the same stage with the strategist in memo mode.
- **PIVOT**: point the user to `/idea-pipeline:new-idea`, which runs in pivot mode.
- **KILL**: stop.

Record the decision in the Decision log of `readiness.md` with the date and the evidence. A request to change a locked threshold goes into the Threshold changes log with the reason and whether results were already seen; never change one silently.

When stage C is passed, tell the user that `/web-pipeline:new-project` can build the MVP and will reuse `docs/idea/`.
