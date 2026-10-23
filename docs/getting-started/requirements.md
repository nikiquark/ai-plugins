# Зависимости

Плагины состоят из Markdown, JSON и shell-скриптов. Внешние инструменты нужны хукам и проверкам, которые пайплайн подключает в проект.

## Обязательные

| Инструмент | Зачем |
|---|---|
| `git` | Снимки дерева (`git-snapshot`, stop-gate), ветки, теги деплоя |
| `jq` | Все хуки читают и пишут JSON через `jq` |
| `python3` | `scripts/anti_slop.py` (только стандартная библиотека) |
| `make` | `make check`, `make dev`, `make test` |
| `bash`, `timeout` (coreutils) | Скрипты хуков |

Без `jq` хуки не работают, поэтому ставьте его в первую очередь.

## Для MCP-серверов

| Сервер | Что нужно |
|---|---|
| Context7 | Доступ в интернет к `https://mcp.context7.com/mcp` |
| Playwright | Node.js с `npx`: сервер запускается как `npx -y @playwright/mcp@latest` |

## По стеку проекта

Эти инструменты вызывает `make check`, который собирает [фаза D1](../web-pipeline/delivery.md#d1-каркас-и-проверка-качества). Если инструмента нет, проверка должна упасть с подсказкой по установке, а не пропустить его молча.

| Задача | TypeScript / Node | Python |
|---|---|---|
| Линтер и форматирование | `eslint` + `prettier` или `biome` | `ruff` |
| Типы | `tsc` | `mypy` или `pyright` |
| Тесты | `vitest` / `jest`, Playwright | `pytest`, Playwright |
| Дублирование | `jscpd` | `jscpd` |
| Мёртвый код | `knip` | `vulture` |
| Границы модулей | `dependency-cruiser` | `import-linter` |
| SAST | `semgrep` | `semgrep`, `bandit` |
| Секреты | `gitleaks` | `gitleaks` |
| Уязвимые зависимости | `npm audit` / `pnpm audit`, `osv-scanner` | `pip-audit`, `osv-scanner` |

## Для деплоя и безопасности

| Инструмент | Где используется |
|---|---|
| `ansible`, `ansible-lint` | [deploy](../web-pipeline/commands/deploy.md), [secure-maintain](../web-pipeline/commands/secure-maintain.md), `make check` |
| `trivy` | Сканирование образов и файловой системы |
| `osv-scanner` | Уязвимости зависимостей |
| `testssl.sh` | Проверка TLS после деплоя |
| `nmap` | Открытые порты после деплоя |
| `docker` | Пассивный ZAP baseline |
| `lynis` (на серверах) | Аудит харденинга хостов |

Если инструмента нет, [ops-auditor](../web-pipeline/agents/ops-auditor.md) и команда `deploy` сообщают об этом и дают команду установки. Сами они ничего не ставят.
