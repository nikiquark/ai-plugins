---
name: new-idea
description: Research a product idea before building it - intake interview, pre-flight kill check, MECE hypothesis tree, parallel market, competitor and customer research with sourced numbers, strategy (beachhead, value proposition, positioning, advantage, go-to-market, unit economics), red-team pre-mortem, bounded fact-check review, KTH readiness assessment, and an answer-first decision memo with pre-registered experiments, with user approval gates. Use when the user wants to validate or research an idea, or to pivot one.
disable-model-invocation: true
argument-hint: "[idea in a few words]"
---

# Research a new idea

You orchestrate this run from the main conversation. Specialist subagents do the heavy work, so keep bulky research out of this conversation: read their reports and the Key findings of their files, not whole files. The user approves at every **GATE**: never skip one, and never treat silence as approval. Talk to the user in their language. Write the docs in the user's language too, unless they ask otherwise.

Idea: $ARGUMENTS

One project directory holds one idea. Its research lives in `docs/idea/`, its settings in `.claude/idea-pipeline.json`.

## Resume first

- If `.claude/state/pipeline.json` exists with `"flow": "idea"`, read it, tell the user which phase the last run stopped at, and continue from there instead of starting over.
- If it exists with another `flow`, another pipeline is in progress in this project. Tell the user and stop: they finish that run or delete the file first.
- If there is no state file but `docs/idea/brief.md` exists, an earlier run finished. Ask whether this is a **pivot** of that idea (go to Phase 1 in pivot mode) or a new idea (which belongs in its own directory).

## Phase 0: Bootstrap

1. If the directory is not a git repository, run `git init` (branch `main`). The review loop compares snapshots of the tree.
2. Create `docs/idea/` and `.claude/state/`, and add `.claude/state/` to `.gitignore`.
3. Write `.claude/state/pipeline.json`: `{ "flow": "idea", "phase": "intake" }`.

## Phase 1: Intake

Invoke the `dev-core:grill-me` skill on the idea. Outputs, written once the user confirms:
- `docs/idea/brief.md`, using the template at `${CLAUDE_PLUGIN_ROOT}/templates/brief.md`;
- `.claude/idea-pipeline.json`, from `${CLAUDE_PLUGIN_ROOT}/templates/idea-pipeline.json`;
- `docs/idea/readiness.md`, from `${CLAUDE_PLUGIN_ROOT}/templates/readiness.md`, with the required axes and the proposed gate thresholds filled in. Not locked yet.

The design tree must cover at least:
- the problem in the customer's words, who has it first, and what they do today instead;
- why now;
- the **target market for this idea**: geography, the languages to research in, the currency, and the model (B2B, B2C, B2B2C, B2G; who uses, who pays, who decides);
- the revenue idea and the price range in mind;
- the team, its time commitment, its **unfair advantages** and founder–market fit, the budget and the constraints;
- the ambition (lifestyle or venture) and the **minimum outcome** that makes this worth doing;
- **kill conditions**, written now, before any research;
- the **required readiness axes** (CRL, BRL, TRL, TMRL by default; IPRL and FRL only if they matter);
- the **gate thresholds** for A → B, B → C, C → D and D → E. Load the `idea-pipeline:readiness-levels` skill and offer its defaults as the recommended answers, adjusted to the model and the price point. The user decides each one.

Market sizes, competitors and customer facts are not questions for the user: research finds them. Ask only for what the founder knows or decides.

**Pivot mode**: interview only about what changes (segment, problem, solution, model or channel) and why. Add a row to the brief's Pivot log, update the brief and the settings, then continue with Phase 3. Earlier research stays in git history.

## Phase 2: Pre-flight → GATE 0

Update `phase` in the state file. Delegate to `idea-pipeline:red-team` in **pre-flight mode** with the paths to `docs/idea/brief.md` and `.claude/idea-pipeline.json`. It writes `docs/idea/preflight.md`.

Present the verdict (green, yellow or red) and its key findings. **GATE 0**: continue, reframe (update the brief and re-run the pre-flight), or stop. Stopping is a KILL: record it in the Decision log of `readiness.md` with the date and the reason, then go to **Finish**.

## Phase 3: Framing → GATE 1

Delegate to `idea-pipeline:strategist` in **issue-tree mode** with the paths to the brief, the pre-flight and the settings. It writes `docs/idea/issue-tree.md`.

Present the governing question and hypothesis, the five branches with their leaf counts, the five highest-priority leaves, and the recommended depth tier with what it means (from the depth table in `idea-pipeline:research-standards`: number of competitors, quotes and sources). **GATE 1**: the user approves or edits the tree and picks the depth. Re-delegate to the strategist with their changes if needed. Then write `depth` to `.claude/idea-pipeline.json` and mark the issue tree approved.

## Phase 4: Research

1. Snapshot the tree with `git-snapshot` (from dev-core, on PATH) and save the hash as `research_base` in the state file.
2. Launch **in parallel, in one message**: `idea-pipeline:market-analyst`, `idea-pipeline:competitor-analyst` and `idea-pipeline:customer-researcher`, each in research mode, each with the paths to `docs/idea/brief.md`, `docs/idea/issue-tree.md`, `docs/idea/preflight.md` and `.claude/idea-pipeline.json`. Delegation messages are self-contained: subagents do not see this conversation.
3. Run `idea-claims docs/idea` (on PATH). Send any errors to the agent that owns the file, in fix mode, once.
4. Collect the **Data requests** sections from the three files and show them to the user: what export would sharpen which number. Do not wait for it. If the user provides data now or later, give it to the owning agent in fix mode as a `user-provided` source.

## Phase 5: Strategy

Delegate to `idea-pipeline:strategist` in **strategy mode** with the paths to the brief, the issue tree, `market.md`, `competitors.md` and `customers.md`. It writes `docs/idea/strategy.md`.

## Phase 6: Pre-mortem

Delegate to `idea-pipeline:red-team` in **pre-mortem mode** with the path to `docs/idea/`. It writes `docs/idea/risks.md`.

## Phase 7: Review

Invoke the `dev-core:review-loop` skill with:
- **reviewers**: `idea-pipeline:fact-checker` and `idea-pipeline:red-team`, both in review mode;
- **fixers** by file: `market.md` → `idea-pipeline:market-analyst`, `competitors.md` → `idea-pipeline:competitor-analyst`, `customers.md` → `idea-pipeline:customer-researcher`, `issue-tree.md` and `strategy.md` → `idea-pipeline:strategist`, `preflight.md` and `risks.md` → `idea-pipeline:red-team` (pre-mortem mode), all in fix mode;
- **base**: `research_base` from the state file;
- **context docs**: `docs/idea/brief.md`, `docs/idea/issue-tree.md`, `.claude/idea-pipeline.json`;
- **check command**: `idea-claims docs/idea`;
- **max rounds**: 2.

## Phase 8: Readiness and memo

1. Delegate to `idea-pipeline:fact-checker` in **assess mode** with the path to `docs/idea/`. It scores the axes in `readiness.md` and updates the leaf statuses.
2. Delegate to `idea-pipeline:strategist` in **memo mode** with the path to `docs/idea/`. It writes `docs/idea/experiments.md` and `docs/idea/memo.md`.
3. Run `idea-claims docs/idea`. Send errors in `memo.md` to the strategist in fix mode, once.

## GATE 2: Decision

Present, briefly:
- the memo's recommendation and its three reasons with confidence;
- the readiness tree: each required axis with its level, the overall level and the weakest link;
- what has to be true, and the first experiments with their pass and kill thresholds;
- the top risks and the state of the kill conditions;
- the paths to `memo.md` and the other files for the full case.

**GATE 2**: first, the user confirms or changes the gate thresholds. Then lock them: set `Thresholds locked` in `readiness.md` to today's date. Then the user decides:
- **GO**: set `stage` to `B` in `.claude/idea-pipeline.json` and in `readiness.md`.
- **ITERATE**: re-delegate the research or strategy the user wants deepened, with their questions, then return to Phase 7.
- **PIVOT**: go to Phase 1 in pivot mode.
- **KILL**: stop here.

Record the decision in the Decision log of `readiness.md` with the date and the evidence it rests on.

## Finish

1. Delete `.claude/state/pipeline.json` and `.claude/state/review-loop.json`: the run is over, and the idea's progress lives in `docs/idea/` and `.claude/idea-pipeline.json`.
2. Suggest committing `docs/idea/` and `.claude/idea-pipeline.json`.
3. After a GO, tell the user what comes next:
   - `/idea-pipeline:interview-kit` prepares the problem interviews for stage B;
   - `/idea-pipeline:evidence` records each interview or experiment result, rescores readiness, and runs the next gate when the evidence is in;
   - `/idea-pipeline:readiness` shows the tree and the next milestones at any time;
   - once stage C is passed, `/web-pipeline:new-project` can build the MVP and reuses `docs/idea/` for its spec.
