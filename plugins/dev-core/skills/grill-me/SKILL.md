---
name: grill-me
description: Interview the user relentlessly about a plan, decision, or idea until reaching a shared understanding. Use when the user wants to stress-test their thinking, get grilled on their design, or uses any "grill" trigger phrase like "grill me".
---

Interview the user relentlessly until you reach a shared understanding. Map this as a **design tree**: every decision branches into the decisions that hang off it.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled: the questions you can ask _now_ without guessing at answers you haven't heard yet. Ask the whole frontier in one round, with your recommended answer for each question. Then wait for the user's answers before the next round.

## Asking a round

Ask through the `AskUserQuestion` tool, so the user picks an answer instead of typing it:

- One call holds up to 4 questions. For a larger frontier, make several calls back to back; together they are still one round.
- Each question gets a `header` of at most 12 characters and 2–4 options. Each option has a short `label` and a `description` that states its trade-off. The tool adds "Other" for a free-text answer by itself, so never add one.
- Put your recommendation first and end its label with " (Recommended)", written in the user's language.
- Use `multiSelect: true` when the choices are not mutually exclusive, such as features, locales or integrations. Use `preview` when the user must compare concrete artifacts: an ASCII layout, a code snippet, a config.
- When a question needs more context than fits in the question and its option descriptions, write that context as a short message before the call.
- When you cannot offer even two sensible options (a name, a URL, a budget you cannot guess), ask that question as text after the tool calls of the round.

An "Other" answer is the user's own words: settle the decision from it, and if it opens new decisions, they join the next round's frontier.

If `AskUserQuestion` is not available, as in a non-interactive run, ask the round as text:

```
❓ **Q1** - **<question title>**: <question body, including the choices>

➡️ <your recommended answer>

---

❓ **Q2** - …
```

## Moving the frontier

Each round the user answers reshapes the tree: settled decisions push the frontier outward and unblock questions that depended on them. Recompute the frontier and ask the next round. A question whose answer depends on another question still open in this round belongs to a _later_ round, not this one.

Finding _facts_ is your job, never the user's. When a frontier question needs a fact from the environment (filesystem, tools, etc.), dispatch a sub-agent to find it; don't ask the user for anything you could look up yourself. Don't block on it: a running exploration is an unsettled prerequisite, so only the questions downstream of it wait for the sub-agent to report; ask the rest of the frontier now. The _decisions_ are the user's: put each to them and wait.

The session is done when the frontier is empty: every branch of the design tree visited, nothing left silently assumed. Do not act on it until the user confirms you have reached a shared understanding. Ask for that confirmation the same way: summarize the decisions in a message, then ask one question whose options are to confirm or to change something.

## Writing the result

When the caller (the user or an orchestrator skill) names an output file or a template, write the confirmed shared understanding there once the user confirms it, using the template's sections. Record every decision with its rationale, and list anything deliberately left open under "Open questions" instead of silently assuming it.
