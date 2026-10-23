---
name: research-standards
description: Evidence and analysis standards for researching a product idea - hypothesis-driven MECE work, answer-first writing, claim labels ([S#], [calc], [est], [hyp], [user]), dated source records, triangulated market sizing as ranges, confidence levels, research depth tiers, per-market source catalogs, and the idea-claims gate. Load for any market, competitor, customer, strategy or review work on an idea.
---

# Research standards

The bar is a top-tier strategy consultancy's work, not a long essay. What makes analysis that good is method: start from a hypothesis, break the question into parts that do not overlap and leave nothing out, back every number, show where the number came from, say how sure you are, and state the answer before the reasoning. A reader must be able to check any claim in under a minute.

Research on an idea is desk research. It produces hypotheses, signals and a plan to test them. It never proves that people will pay. Say so wherever a conclusion could be read as validation.

## Hypothesis-driven, MECE

- Work from `docs/idea/issue-tree.md`. Every section you write answers one or more of its leaves. Cite the leaf ids (`H2.1`) in the section, so the reader sees which question is being answered.
- Break each question into parts that are **mutually exclusive and collectively exhaustive**. Revenue = customers × purchase frequency × price, not "customers, pricing, online sales". When a split overlaps or leaves a gap, fix the split before researching.
- Spend effort where it changes the decision (80/20). A leaf that cannot change the go/no-go answer gets a line, not a page.
- Look for disconfirming evidence as hard as for confirming evidence. A section with no evidence against its hypothesis is incomplete.

## Answer first

- Every file opens with **Key findings**: 3–6 bullets, each a full-sentence conclusion with its confidence, ordered by how much it matters to the decision.
- Every section opens with its conclusion in one sentence and ends with **So what**: what this means for the idea and the decision.
- Prefer exhibits to prose: tables, ranked lists, a 2×2, a Mermaid chart. An exhibit has a title that states its point ("Three incumbents hold most of the SMB segment"), not a label ("Competitors").

## Claim labels

Every number, and every factual claim that a decision rests on, carries exactly one label at the end of its sentence or table row:

| Label | Meaning | Rule |
|---|---|---|
| `[S3]` | Fact from source 3 | The source is listed in this file's **Sources** section. Several: `[S3, S7]` |
| `[calc]` | Calculated | The formula and its inputs are shown next to it, and every input has its own label |
| `[est]` | Estimate | A judgment or analogy. Say what it is based on |
| `[hyp]` | Hypothesis | Unverified assumption. It must appear in the issue tree or in `experiments.md` |
| `[user]` | Stated by the founder | From `docs/idea/brief.md` or the interview. Not verified |

`idea-claims` (on PATH) fails on any number without a label and on any `[S#]` that is not in the file's Sources. Never invent a number to fill a gap: write the gap, what data would fill it, and where to get it.

## Sources

Each file ends with a `## Sources` section, one line per source:

```text
- [S3] Title — publisher or author, YYYY[-MM]. URL (accessed YYYY-MM-DD). Type: primary | secondary | vendor | user-provided. Note.
```

- **Open the page before citing it.** A search snippet is not a source. The number you cite must be on the page you link.
- **Date everything.** Data older than `stale_years` from `.claude/idea-pipeline.json` (3 by default) is marked stale in the text, and `idea-claims` warns about it. Markets for new technology age faster: prefer the last 12–24 months.
- **Rank sources by reliability**: official statistics and filings > audited company reports > reputable research firms with stated methods > trade press > vendor marketing and press releases > forums. Vendor and marketing numbers (a "$50B market" from a press release) are `[S#]` with type `vendor` and never the only basis of a conclusion.
- **Data you cannot reach** (paywalled databases, keyword volume tools, private registries): list it under **Data requests** at the end of the file, with what to export and why. The orchestrator asks the user for it. Data the user supplies becomes a source of type `user-provided`.

## Market sizing

- **Define the market first**: who buys, what job they pay to get done, geography, and the unit (money per year, by default in the currency from `.claude/idea-pipeline.json`). A size without a definition is meaningless.
- **TAM, SAM, SOM**:
  - TAM: everyone with this job in the chosen geography, at today's spend on solving it (including the alternatives and non-consumption that cost money or time).
  - SAM: the part this product's model can serve (segment, channel, language, regulation).
  - SOM: what this team can realistically win in 3–5 years with its channels and resources. Derive it from the go-to-market (reachable customers × conversion × price), not as a percentage of TAM.
- **Triangulate**: at least two independent methods (three on the deep tier):
  - **top-down**: a published market figure narrowed by segment shares;
  - **bottom-up**: number of buyers × adoption × price × frequency, each input labeled;
  - **analog**: the size or penetration of a comparable market or product in another geography or adjacent category, adjusted.
- Give **ranges** (low / base / high) and explain the gap between methods. When methods disagree by more than 3×, the definition or an input is wrong: find out which before going on.
- Show growth (historic and forecast CAGR) with its source, and the drivers behind it. Separate the market's growth from inflation and from a vendor's hype.

## Confidence

Every key finding has a confidence level:

- **High**: several independent, reliable, recent sources agree, or primary evidence from customers.
- **Medium**: one reliable source, or several weaker ones that agree; or a solid calculation on labeled inputs.
- **Low**: estimates, analogies, vendor claims, old data, or a single anecdote.

Evidence quality and confidence are separate. A finding can rest on strong evidence that answers the wrong question: then confidence in the conclusion stays low.

## Depth tiers

The tier is chosen at GATE 1 and stored as `depth` in `.claude/idea-pipeline.json`.

| | light | standard | deep |
|---|---|---|---|
| Sizing methods | 2 | 2 | 3 |
| Competitors profiled in full | 5 | 8–10 | 15+ |
| Customer-voice quotes with links | 10 | 20 | 40 |
| Segments analyzed | 1–2 | 2–4 | all plausible |
| Minimum distinct sources per file | 8 | 15 | 25 |

## Market and language

The target market is chosen per idea and stored in `.claude/idea-pipeline.json` (`market.geography`, `market.languages`, `market.currency`). Research in the market's languages, not only in English: the customers' words and the local competitors are there. Load the source catalog for the market:

- Russia and CIS: [references/sources-ru.md](references/sources-ru.md)
- Global, US, EU and other markets: [references/sources-global.md](references/sources-global.md)

Use both when the geography spans them. A catalog is a starting point, not a limit.

## Signals that a market exists

Desk research can find indirect evidence that people already spend money or effort on the job. Look for each and report what you found and what you did not:

- competitors with revenue, funding, paying customers or price lists;
- paid advertising on the job's search queries (someone finds it worth paying for);
- job postings for people who do the job by hand;
- complaints, workarounds and "is there a tool for…" threads in communities;
- 1–3 star reviews of existing products (unmet needs) and 4–5 star reviews (what must not be lost);
- marketplace listings, sales counts, app store rankings;
- search demand, only from data the user exports (you have no keyword volume tool).

## Writing

- Write in the language of `docs/idea/brief.md`. Keep quotes from customers in their original language.
- No filler, no hype words, no "in today's fast-paced world". Short sentences, concrete nouns, numbers with labels.
- Never claim validation from desk research. "There is demand" needs customer evidence; desk research supports "there are signals of demand".
