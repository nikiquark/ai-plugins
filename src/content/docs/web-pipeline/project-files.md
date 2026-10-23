---
title: "Файлы в проекте"
---

Всё, что web-pipeline создаёт или читает в вашем проекте.

```text
CLAUDE.md                          # раздел «Web pipeline» (init)
Makefile                           # check, dev, test, lint, fmt, seo (init, D1)
TODO.md                            # отложенные minor из ревью, карантин тестов
scripts/anti_slop.py               # проверка на «ИИ-вид» (init)
scripts/seo_check.py               # проверка индексации и превью (init)
.env.example                       # пример конфигурации (backend-dev)
.claude/
  web-pipeline.json                # включает хуки и хранит их настройки (init)
  state/                           # в .gitignore
    pipeline.json                  # состояние оркестратора
    review-loop.json               # состояние цикла ревью
    gate-*.seen, gate-*.blocks, gate-pass.tree   # stop-gate
docs/
  spec.md                          # что и зачем (new-project)
  content.md                       # смысл, тексты, SEO-метаданные (content-strategist)
  architecture.md                  # как (architect)
  adr/NNNN-<slug>.md               # трудно обратимые решения (architect)
  plan.md                          # задачи T1… с отметками (architect, оркестратор)
  design.md                        # дизайн-система (designer)
  design/concepts/<letter>-<slug>.html   # концепты (designer)
  design/og-template.html          # шаблон OG-картинки (designer)
  changes/NNNN-<slug>.md           # документы изменений (change)
  deploys/<YYYY-MM-DD>-<env>.md    # отчёты о деплое (deploy)
  security/<YYYY-MM-DD>.md         # отчёты безопасности (secure-maintain)
deploy/ansible/                    # см. ansible-conventions
```

## Что коммитить

| Путь | В git? |
|---|---|
| `.claude/web-pipeline.json` | Да: настройки хуков нужны всем, кто работает с проектом |
| `.claude/state/` | Нет: локальное состояние, `init` добавляет его в `.gitignore` |
| `docs/` | Да: это документация проекта и память пайплайна |
| `scripts/anti_slop.py`, `scripts/seo_check.py` | Да: работают в CI |
| `TODO.md` | Да |

## Вне проекта

| Путь | Что |
|---|---|
| `${CLAUDE_PLUGIN_DATA}/font-registry.md` | Реестр использованных пар шрифтов, общий для всех проектов ([designer](agents/designer.md)) |
| `${XDG_CACHE_HOME:-~/.cache}/claude-context/` | Кэш процента контекста от строки состояния ([context-guard](../dev-core/context-guard.md)) |

## Ветки и теги

| Имя | Кто создаёт |
|---|---|
| `main` | `new-project` при `git init` |
| `change/<slug>` | [`change`](commands/change.md) |
| `security/<YYYY-MM-DD>` | [`secure-maintain fix`](commands/secure-maintain.md) |
| тег `deploy-<env>-<YYYYMMDD-HHMM>` | [`deploy`](commands/deploy.md), локально, без push |
