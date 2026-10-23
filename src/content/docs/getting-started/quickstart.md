---
title: "Quickstart за 2 минуты"
---

Цель: поставить плагины и убедиться, что всё подключилось. Подробный проход по пайплайну описан на странице [Первый проект](first-project.md).

## 1. Установите

```bash
claude plugin marketplace add nikiquark/ai-plugins
claude plugin install web-pipeline@nikiquark-ai-plugins
claude plugin install idea-pipeline@nikiquark-ai-plugins    # если нужна проверка идей
```

## 2. Проверьте команды

Запустите `claude` в любой папке и наберите `/web-pipeline:`. Автодополнение должно показать:

| Команда | Что делает |
|---|---|
| `/web-pipeline:new-project <идея>` | Новый веб-проект от идеи до локальной проверки |
| `/web-pipeline:change <что изменить>` | Доработка существующего проекта |
| `/web-pipeline:deploy [staging|production]` | Деплой через Ansible |
| `/web-pipeline:secure-maintain [report|fix] [env]` | Сканирование уязвимостей и исправления |
| `/web-pipeline:init` | Подключение проекта к пайплайну |

Для `idea-pipeline` наберите `/idea-pipeline:`: `new-idea`, `evidence`, `readiness`, `interview-kit` ([обзор](../idea-pipeline/index.md)).

Скиллы `dev-core` доступны как `/dev-core:grill-me`, `/dev-core:review-loop` и `/dev-core:reuse-first`.

## 3. Проверьте агентов

Выполните `/agents`. В списке должны быть 10 агентов плагина: `web-pipeline:content-strategist`, `web-pipeline:architect`, `web-pipeline:designer`, `web-pipeline:backend-dev`, `web-pipeline:frontend-dev`, `web-pipeline:qa-engineer`, `web-pipeline:code-reviewer`, `web-pipeline:security-reviewer`, `web-pipeline:design-critic`, `web-pipeline:ops-auditor`. С `idea-pipeline` добавятся ещё 6: `market-analyst`, `competitor-analyst`, `customer-researcher`, `strategist`, `red-team`, `fact-checker`.

## 4. Проверьте MCP

Выполните `/mcp`. Должны быть видны серверы `context7` (из `dev-core`) и `playwright` (из `web-pipeline`). Для Playwright нужен Node.js с `npx`.

## 5. Попробуйте grill-me

Самый быстрый способ увидеть плагины в деле — интервью по любому решению:

```text
/dev-core:grill-me Перевести сборку проекта с webpack на vite
```

Claude будет задавать вопросы раундами, к каждому предложит ответ и ничего не начнёт делать, пока вы не подтвердите общее понимание.

## Дальше

- [Первый проект](first-project.md): полный проход `new-project`.
- [Зависимости](requirements.md): что поставить, чтобы `make check` и деплой работали.
- [Контекст и /clear](../concepts/context.md): как настроить строку состояния для контроля контекста.
