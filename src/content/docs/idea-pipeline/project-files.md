---
title: "Файлы в проекте"
---

Всё, что idea-pipeline создаёт в папке проекта. Шаблоны лежат в `plugins/idea-pipeline/templates/`. Заголовки шаблонов на английском, а документы пишутся на языке интервью.

## docs/idea/

| Файл | Кто пишет | Шаблон | Содержимое |
|---|---|---|---|
| `brief.md` | Оркестратор после [grill-me](../dev-core/skills/grill-me.md) | `brief.md` | Идея, проблема и клиенты, рынок и модель, команда и нечестные преимущества, амбиция, минимальный результат, условия остановки, журнал pivot |
| `preflight.md` | [red-team](agents/red-team.md) | `preflight.md` | Быстрая проверка и вердикт green, yellow или red |
| `issue-tree.md` | [strategist](agents/strategist.md); статусы — [fact-checker](agents/fact-checker.md) | `issue-tree.md` | Главный вопрос, гипотеза, пять ветвей, листья со статусами, глубина |
| `market.md` | [market-analyst](agents/market-analyst.md) | `market.md` | Определение рынка, TAM/SAM/SOM разными способами, рост, сигналы, Data requests, Sources |
| `competitors.md` | [competitor-analyst](agents/competitor-analyst.md) | `competitors.md` | Ландшафт, профили, карта позиционирования, пробелы, провалы предшественников |
| `customers.md` | [customer-researcher](agents/customer-researcher.md) | `customers.md` | Сегменты, JTBD, боли и выгоды, голос клиента, процесс покупки, кандидаты в плацдарм |
| `strategy.md` | [strategist](agents/strategist.md) | `strategy.md` | Плацдарм, ценностное предложение, позиционирование, преимущество, GTM, модель и юнит-экономика, реализуемость |
| `risks.md` | [red-team](agents/red-team.md) | `risks.md` | Pre-mortem, рискованные допущения, реестр рисков, условия остановки, искажения |
| `readiness.md` | Оркестратор (оси, пороги, журналы), [fact-checker](agents/fact-checker.md) (уровни) | `readiness.md` | Дерево KTH, цели стадий, пороги гейтов, журнал изменений порогов, журнал решений |
| `experiments.md` | [strategist](agents/strategist.md); результаты — [fact-checker](agents/fact-checker.md) | `experiments.md` | Эксперименты с заранее заданными порогами pass и kill |
| `memo.md` | [strategist](agents/strategist.md) | `memo.md` | Рекомендация первой, кейс на страницу, что должно быть правдой, план на 30 дней |
| `evidence/NNNN-*.md` | [`evidence`](commands/evidence.md) | `evidence-note.md` | Одно интервью или результат: факты, обязательства, затронутые гипотезы, сырые числа |
| `interviews/script-*.md` | [customer-researcher](agents/customer-researcher.md) | `interview-script.md` | Скрипт интервью по The Mom Test |

## Остальное

| Путь | Кто пишет | Назначение |
|---|---|---|
| `.claude/idea-pipeline.json` | [`new-idea`](commands/new-idea.md) | Настройки идеи ([Конфигурация](configuration.md)). Коммитится |
| `.claude/state/pipeline.json` | `new-idea` | Состояние запуска с `"flow": "idea"`. Удаляется в конце запуска |
| `.claude/state/review-loop.json` | [review-loop](../dev-core/skills/review-loop.md) | Раунды ревью. Удаляется в конце запуска |
| `.gitignore` | `new-idea` | Строка `.claude/state/` |
| `TODO.md` | review-loop | Отложенные мелкие находки ревью |

## Что коммитить

`docs/idea/` и `.claude/idea-pipeline.json`. Это вся память идеи: [`evidence`](commands/evidence.md), [`readiness`](commands/readiness.md) и pivot работают только по этим файлам. Прежние версии исследования после pivot остаются в истории git.

## Переход к продукту

Когда стадия C пройдена, в той же папке можно запустить [`/web-pipeline:new-project`](../web-pipeline/commands/new-project.md). Он увидит `docs/idea/memo.md` и возьмёт из исследования персоны, ценностное предложение, позиционирование, конкурентов и доказательства в `docs/spec.md`.
