---
name: readiness
description: Show the readiness tree of an idea researched with idea-pipeline - the KTH axes with their levels and stage targets, the overall level and the weakest link, the gate thresholds, the experiments in flight and the next milestones. Read-only. Use when the user asks where the idea stands or what to do next.
---

# Show readiness

Talk to the user in their language. Do not change any file.

## Steps

1. If `docs/idea/readiness.md` is missing, point the user to `/idea-pipeline:new-idea` and stop.
2. Read `docs/idea/readiness.md`, `.claude/idea-pipeline.json` and `docs/idea/experiments.md`. List `docs/idea/evidence/` by name.
3. **Staleness**: if any evidence note is dated after the `Assessed` date, say that the levels are out of date and suggest `/idea-pipeline:evidence`, which rescores them.
4. Show the tree as text, one line per axis, required axes first, with the current level against the current stage's target:

   ```text
   Stage B · Problem validation · thresholds locked 2026-10-24

   CRL  Customer        ███░░░░░░  3 / 9   target 4   ← weakest link
   BRL  Business model  ████░░░░░  4 / 9   target 4
   TRL  Technology      ██░░░░░░░  2 / 9   target 3
   TMRL Team            ████░░░░░  4 / 9   target 4
   FRL  Funding         ██░░░░░░░  2 / 9   (optional)

   Overall: 2 (minimum of the required axes)
   ```

5. **Next milestones**: for the weakest link and every required axis below its target, what is missing for the next level, from the readiness table.
6. **Experiments in flight**: each one of the current stage with its status, deadline, thresholds and, if it has results, its verdict. Flag any experiment past its deadline.
7. **The gate**: the current stage's gate thresholds and how close the evidence is to each.
8. The last entry of the Decision log, and any post-hoc threshold change.
