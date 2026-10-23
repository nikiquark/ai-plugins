---
title: "Все команды"
---

## Команды web-pipeline

| Команда | Аргументы | Автовызов | Точки решения | Страница |
|---|---|---|---|---|
| `/web-pipeline:new-project` | `[идея]` | нет | интервью, GATE 1, GATE 2, D5 | [new-project](../web-pipeline/commands/new-project.md) |
| `/web-pipeline:change` | `[что изменить]` | нет | интервью, GATE 1, GATE 2*, D5 | [change](../web-pipeline/commands/change.md) |
| `/web-pipeline:deploy` | `[staging|production]`, по умолчанию `staging` | нет | dry run, применение, critical/high, откат | [deploy](../web-pipeline/commands/deploy.md) |
| `/web-pipeline:secure-maintain` | `[report|fix] [staging|production|all]`, по умолчанию `report production` | нет | triage | [secure-maintain](../web-pipeline/commands/secure-maintain.md) |
| `/web-pipeline:init` | `[--legacy]` | да | — | [init](../web-pipeline/commands/init.md) |

\* только для новых экранов или редизайна.

## Команды idea-pipeline

| Команда | Аргументы | Автовызов | Точки решения | Страница |
|---|---|---|---|---|
| `/idea-pipeline:new-idea` | `[идея]` | нет | интервью, GATE 0, GATE 1, GATE 2 | [new-idea](../idea-pipeline/commands/new-idea.md) |
| `/idea-pipeline:evidence` | `[заметки или результаты]` | да | гейт стадии | [evidence](../idea-pipeline/commands/evidence.md) |
| `/idea-pipeline:readiness` | — | да | — | [readiness](../idea-pipeline/commands/readiness.md) |
| `/idea-pipeline:interview-kit` | `[сегмент]` | да | — | [interview-kit](../idea-pipeline/commands/interview-kit.md) |

## Скиллы dev-core

| Скилл | Аргументы | Автовызов | Страница |
|---|---|---|---|
| `/dev-core:grill-me` | `<тема>` | да | [grill-me](../dev-core/skills/grill-me.md) |
| `/dev-core:review-loop` | `[max-rounds]`, по умолчанию 2 | да | [review-loop](../dev-core/skills/review-loop.md) |
| `/dev-core:reuse-first` | — | да | [reuse-first](../dev-core/skills/reuse-first.md) |

## Навыки-знания web-pipeline

Их можно вызвать вручную, чтобы загрузить стандарты в текущую сессию, но обычно они предзагружаются в агентов.

| Скилл | Страница |
|---|---|
| `/web-pipeline:frontend-style` | [frontend-style](../web-pipeline/skills/frontend-style.md) |
| `/web-pipeline:seo-standards` | [seo-standards](../web-pipeline/skills/seo-standards.md) |
| `/web-pipeline:backend-standards` | [backend-standards](../web-pipeline/skills/backend-standards.md) |
| `/web-pipeline:testing-standards` | [testing-standards](../web-pipeline/skills/testing-standards.md) |
| `/web-pipeline:ansible-conventions` | [ansible-conventions](../web-pipeline/skills/ansible-conventions.md) |

## Навыки-знания idea-pipeline

| Скилл | Страница |
|---|---|
| `/idea-pipeline:research-standards` | [research-standards](../idea-pipeline/skills/research-standards.md) |
| `/idea-pipeline:readiness-levels` | [readiness-levels](../idea-pipeline/skills/readiness-levels.md) |

## Команды оболочки

| Команда | Плагин | Страница |
|---|---|---|
| `git-snapshot` / `git snapshot` | dev-core | [git-snapshot](../dev-core/git-snapshot.md) |
| `python3 scripts/anti_slop.py` | web-pipeline (копия в проекте) | [anti_slop.py](../web-pipeline/anti-slop.md) |
| `python3 scripts/seo_check.py`, `make seo` | web-pipeline (копия в проекте) | [seo_check.py](../web-pipeline/seo-check.md) |
| `idea-claims` | idea-pipeline | [idea-claims](../idea-pipeline/idea-claims.md) |

## Управление плагинами

| Команда | Что делает |
|---|---|
| `claude plugin marketplace add nikiquark/ai-plugins` | Подключить marketplace с GitHub |
| `claude plugin marketplace add <путь>` | Подключить marketplace из локальной папки |
| `claude plugin marketplace update nikiquark-ai-plugins` | Обновить каталог marketplace |
| `claude plugin install <plugin>@nikiquark-ai-plugins` | Установить плагин |
| `claude plugin update <plugin>@nikiquark-ai-plugins` | Обновить плагин |
| `claude plugin disable <plugin>@nikiquark-ai-plugins` | Отключить, не удаляя |
| `claude plugin uninstall <plugin>@nikiquark-ai-plugins` | Удалить |
| `claude plugin validate .` | Проверить marketplace и все плагины |
| `/reload-plugins` | Перечитать плагины в текущей сессии |
