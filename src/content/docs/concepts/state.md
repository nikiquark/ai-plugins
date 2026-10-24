---
title: "Состояние и возобновление"
---

Каждый оркестратор можно прервать в любой момент и продолжить в новой сессии. Для этого состояние хранится в файлах проекта, а не в контексте диалога.

## Файлы состояния

Все они лежат в `.claude/state/`. [`init`](../web-pipeline/commands/init.md) добавляет эту папку в `.gitignore`.

| Файл | Кто пишет | Содержимое |
|---|---|---|
| `pipeline.json` | Оркестраторы `new-project`, `change` и `new-idea` | Текущий поток, фаза, задача, базовый снимок |
| `review-loop.json` | [`dev-core:review-loop`](../dev-core/skills/review-loop.md) | Номер раунда, лимит, снимки, открытые и отложенные находки |
| `gate-*.seen`, `gate-*.blocks`, `gate-pass.tree` | [Stop-хук](../web-pipeline/hooks.md#stop-gate) | Снимки дерева и счётчики неудачных проверок |

### pipeline.json

```json
{
  "flow": "new-project",
  "phase": "requirements",
  "current_task": "T4",
  "implementation_base": "<git tree hash>",
  "change_doc": "docs/changes/0003-export-csv.md"
}
```

| Поле | Значение |
|---|---|
| `flow` | `new-project`, `change` или `idea` |
| `phase` | Фаза, с которой продолжать: `requirements`, архитектура, дизайн, `D1`…`D5` |
| `current_task` | Текущая задача из `docs/plan.md` во время D3 |
| `implementation_base` | Снимок [`git-snapshot`](../dev-core/git-snapshot.md) перед началом реализации. От него считается diff для ревью |
| `change_doc` | Только для `change`: путь к документу изменения |
| `research_base` | Только для `idea`: снимок перед исследованием. От него считается diff для ревью фактов |

Наличие `pipeline.json` — признак активного пайплайна. По нему срабатывает [context-guard](../dev-core/context-guard.md).

## Как работает возобновление

Каждый оркестратор начинается с раздела «Resume first»:

1. Если `.claude/state/pipeline.json` есть со своим `flow`, оркестратор читает его. Если `flow` чужой, в проекте идёт другой пайплайн: оркестратор сообщает об этом и останавливается, чтобы не перезаписать чужое состояние.
2. Сообщает, на какой фазе остановился прошлый запуск.
3. Продолжает с неё, а не начинает заново.

Документы в `docs/` — вторая половина памяти: спецификация, архитектура, план с отметками выполненных задач, дизайн-система. Новая сессия читает их по путям и получает весь контекст решений.

```mermaid
sequenceDiagram
  participant U as Вы
  participant O as Оркестратор
  participant S as pipeline.json + docs/
  O->>S: phase = D3, current_task = T4
  O->>U: Контекст 60%. Выполните /clear и ту же команду
  U->>O: /clear, затем /web-pipeline:new-project
  O->>S: читает состояние
  O->>U: Продолжаю с D3, задача T4
```

## Сброс

Обычно сбрасывать ничего не нужно. [`new-project`](../web-pipeline/commands/new-project.md) и [`change`](../web-pipeline/commands/change.md) удаляют `pipeline.json` и `review-loop.json`, когда вы принимаете результат на [D5](../web-pipeline/delivery.md#d5-локальная-проверка-gate), а `new-idea` удаляет их в конце запуска. `review-loop.json` с чужой базой review-loop сам перезаписывает.

Чтобы начать прерванный поток заново, удалите `.claude/state/pipeline.json` (и при необходимости `review-loop.json`). Документы в `docs/` при этом останутся, и новый запуск их учтёт.

## Состояние идеи

Проверка идеи длится неделями, а `pipeline.json` нужен только на время одного запуска. Поэтому [`new-idea`](../idea-pipeline/commands/new-idea.md) удаляет `pipeline.json` и `review-loop.json` в конце запуска. Долгая память идеи — `.claude/idea-pipeline.json` (стадия, рынок, обязательные оси) и `docs/idea/` (уровни готовности, пороги, эксперименты, доказательства). По ним работают [`evidence`](../idea-pipeline/commands/evidence.md) и [`readiness`](../idea-pipeline/commands/readiness.md).
