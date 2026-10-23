---
title: "dev-core"
---

Общие компоненты для всех пайплайнов. Плагин не привязан к предметной области: на нём строятся доменные плагины вроде [web-pipeline](../web-pipeline/index.md), но его можно использовать и отдельно.

```bash
claude plugin install dev-core@nikiquark-ai-plugins
```

## Состав

| Компонент | Тип | Назначение |
|---|---|---|
| [`grill-me`](skills/grill-me.md) | Скилл | Интервью раундами по дереву решений до общего понимания |
| [`review-loop`](skills/review-loop.md) | Скилл | Ревью независимыми субагентами с исправлениями, не больше N раундов |
| [`reuse-first`](skills/reuse-first.md) | Скилл-протокол | Проверка «а нет ли уже готового» перед любым новым модулем |
| [`git-snapshot`](git-snapshot.md) | Команда в `bin/` | Хэш дерева рабочей копии без изменения индекса и истории |
| [context-guard](context-guard.md) | Хук | Предупреждает оркестратор о заполнении контекста |
| [Context7](context7.md) | MCP-сервер | Актуальная документация библиотек |

## Как вызывать

Скиллы вызываются по полному имени: `/dev-core:grill-me`, `/dev-core:review-loop`, `/dev-core:reuse-first`. Доменные плагины обращаются к ним так же, например `dev-core:review-loop` в фазе D4 web-pipeline.

У всех трёх скиллов есть `description`, поэтому Claude может вызвать их и сам, когда задача подходит под описание.

## Версия

Текущая версия указана в `plugins/dev-core/.claude-plugin/plugin.json`. Лицензия MIT.
