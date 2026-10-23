---
title: "readiness"
---

Показывает, где идея сейчас: дерево готовности KTH, общий уровень и слабое звено, пороги гейта, текущие эксперименты и ближайшие milestones. Ничего не меняет.

| | |
|---|---|
| Вызов | `/idea-pipeline:readiness` |
| Автовызов | Да, когда вы спрашиваете, где стоит идея или что делать дальше |
| Читает | `docs/idea/readiness.md`, `docs/idea/experiments.md`, `docs/idea/evidence/`, `.claude/idea-pipeline.json` |
| Исходник | `plugins/idea-pipeline/skills/readiness/SKILL.md` |

## Пример вывода

```text
Stage B · Problem validation · thresholds locked 2026-10-24

CRL  Customer        ███░░░░░░  3 / 9   target 4   ← weakest link
BRL  Business model  ████░░░░░  4 / 9   target 4
TRL  Technology      ██░░░░░░░  2 / 9   target 3
TMRL Team            ████░░░░░  4 / 9   target 4
FRL  Funding         ██░░░░░░░  2 / 9   (optional)

Overall: 2 (minimum of the required axes)
```

Дальше идут:

- **ближайшие milestones**: чего не хватает до следующего уровня по слабому звену и по каждой обязательной оси ниже цели;
- **эксперименты** текущей стадии: статус, срок, пороги и вердикт, если есть результаты. Просроченные помечаются;
- **гейт**: пороги текущей стадии и насколько доказательства к ним приблизились;
- последнее решение из журнала и изменения порогов post-hoc, если они были.

## Устаревшая оценка

Если есть заметки-доказательства новее даты оценки, команда предупреждает, что уровни устарели, и предлагает [`evidence`](evidence.md): она пересчитывает их.

Как считаются уровни — на странице [readiness-levels](../skills/readiness-levels.md).
