---
name: readiness-levels
description: The readiness tree for a product idea, based on the KTH Innovation Readiness Level - six axes (customer, business, technology, team, IPR, funding) with nine levels each, how to score them from evidence, the overall level as the weakest required axis, the stages A-E with their target levels, default gate thresholds, pre-registration and locking of thresholds, and the GO/ITERATE/PIVOT/KILL decision. Load for scoring readiness, planning experiments, or deciding whether an idea moves to the next stage.
---

# Readiness levels

An idea is ready for the next step when the evidence says so, not when the slides look good. The tree below follows the **KTH Innovation Readiness Level** (KTH Innovation, Stockholm): six axes, nine levels each. Criteria are paraphrased and adapted to software products in [references/kth-irl.md](references/kth-irl.md). Read it before scoring.

## The tree

```
Idea readiness = min(required axes)
├── CRL  Customer readiness      required
├── BRL  Business model readiness required
├── TRL  Technology readiness    required (software reading)
├── TMRL Team readiness          required
├── IPRL IPR readiness           optional
└── FRL  Funding readiness       optional
```

Which axes are required is decided per idea at intake and stored as `required_axes` in `.claude/idea-pipeline.json`. IPRL is usually optional for software. FRL is required only when the plan depends on outside money (investors or grants).

The overall level is the **minimum** over the required axes, and the axis that sets it is the **weakest link**. Name it in every assessment: it is where the next effort goes.

## Scoring

- An axis is at level N when the criteria of level N **and of every level below it** are met. No half levels and no rounding up.
- Each claimed level cites its evidence: a section of a `docs/idea/` file, an evidence note `docs/idea/evidence/NNNN-*.md`, or an experiment result. A level without cited evidence is not reached.
- **Desk research never counts as customer evidence.** It can carry CRL to 2, BRL to 4 and TRL to 2. CRL 3 and above need contact with real customers or experts; BRL 5 and above need the market's reaction to the model; TRL 3 and above need working code.
- What the founder says is `[user]` evidence: enough for TMRL and for the starting point of other axes, never enough for CRL or BRL above 2.
- For every required axis, write what is missing for the next level, as concrete evidence to collect.
- Score conservatively. When two levels fit, pick the lower one and say why.

## Stages and target levels

| Stage | Question | CRL | BRL | TRL | TMRL | How it is reached |
|---|---|---|---|---|---|---|
| **A. Desk research** | Is this worth testing with real people? | 2 | 4 | 2 | 3 | `/idea-pipeline:new-idea` |
| **B. Problem validation** | Do these people have this problem, badly enough? | 4 | 4 | 3 | 4 | Interviews (`/idea-pipeline:interview-kit`), recorded with `/idea-pipeline:evidence` |
| **C. Demand and solution validation** | Will they want our solution and pay this price? | 6 | 6 | 4 | 5 | Smoke-test landing, pre-orders or letters of intent, pricing test, clickable prototype or concierge MVP |
| **D. MVP and product-market fit** | Do they keep using it and paying? | 8 | 7 | 7 | 6 | Working product with paying customers |
| **E. Scale** | Does it grow repeatably and profitably? | 9 | 9 | 9 | 8 | Growth |

IPRL and FRL, when required, get their targets per stage at intake (for example FRL 4 by the end of stage C when a round is planned after it).

## Gate thresholds

Every move from one stage to the next passes a gate. Its thresholds are **set per idea at intake**, written in `docs/idea/readiness.md`, and **locked** at the end of `new-idea`, before any experiment runs. Pre-registering them is what keeps the decision honest: a threshold chosen after seeing the result can justify anything.

Defaults to propose at intake (the user decides; adjust to the segment, price point and ambition):

| Gate | Metric | Default pass | Default kill |
|---|---|---|---|
| A → B | Desk research | No red flag in the pre-flight left unanswered; SOM base case ≥ the founder's minimum viable outcome; a plausible beachhead segment you can reach | A dominant free alternative that solves the job well; SOM below the minimum outcome in every scenario |
| B → C | Problem interviews | B2B 5–10, B2C 10–20 interviews in the beachhead segment, without pitching the solution | — |
| | Problem confirmed | ≥ 60% rank it among their top 3 problems in this area and already spend money or time on a workaround | < 30% |
| | Commitment | ≥ 30% give a commitment: another meeting, an introduction, a pilot, a pre-payment | < 10% |
| C → D | Smoke test | ≥ 5% visitor → sign-up on at least 300 targeted visitors (B2C); ≥ 3 letters of intent or paid pilots (B2B) | < 1.5% or 0 letters |
| | Willingness to pay | ≥ 10 pre-orders or deposits (B2C) at the planned price; the planned price inside the acceptable range of a pricing survey | No one pays at any tested price |
| | Solution | ≥ 4 of 5 test users complete the core job in the prototype | ≤ 2 of 5 |
| D → E | Product-market fit | ≥ 40% "very disappointed" without the product (Sean Ellis survey, ≥ 40 active users); cohort retention curve flattens | < 25%; retention keeps falling to zero |
| | Unit economics | LTV / CAC ≥ 3; CAC payback ≤ 12 months | LTV / CAC < 1 |

Each experiment in `docs/idea/experiments.md` restates its own pass and kill thresholds, minimum sample and deadline.

## Locking and changing thresholds

- Before the lock, thresholds can change freely. The end of `new-idea` locks them: `readiness.md` gets `Locked: YYYY-MM-DD`.
- After the lock, a threshold changes only by the user's explicit decision. Record it in the **Threshold changes** log in `readiness.md`: date, old, new, reason, and whether results were already seen. A change made after seeing results is marked **post-hoc**, and the decision it supports says so.
- Never relax a threshold silently to let an idea pass.

## Decisions

At every gate the user chooses one, and the decision goes into the **Decision log** in `readiness.md` with the date and the evidence it rests on:

- **GO**: pass thresholds met; move to the next stage.
- **ITERATE**: inconclusive; stay in the stage with changed experiments (more interviews, another channel, a sharper landing).
- **PIVOT**: a core hypothesis failed (segment, problem, solution, model or channel). Change it, record what was learned, and re-run `new-idea` from the issue tree with the new framing.
- **KILL**: kill thresholds hit, or no plausible pivot. Record why. A killed idea with clear reasons is a good outcome: it is time not spent building something nobody needs.

Results between pass and kill are inconclusive: they lead to ITERATE, never to GO.
