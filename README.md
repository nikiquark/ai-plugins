# nikiquark-agents

Marketplace плагинов для Claude Code.

| Плагин | Назначение |
|---|---|
| `dev-core` | Общие компоненты пайплайнов: интервью `grill-me`, ограниченный цикл ревью `review-loop`, протокол `reuse-first`, команда `git-snapshot`, контроль контекста, MCP Context7 |
| `web-pipeline` | Веб-проекты от идеи до продакшена: спецификация, архитектура, дизайн-концепты, бэкенд и фронтенд, проверки качества, ревью, деплой через Ansible, обслуживание безопасности. Зависит от `dev-core` |

## Установка

```bash
claude plugin marketplace add ~/Projects/AI/agents-setup        # или <github-user>/agents-setup
claude plugin install web-pipeline@nikiquark-agents             # dev-core ставится как зависимость
```

В сессии то же самое делают `/plugin marketplace add …` и `/plugin install …`. При установке из локальной папки правки подхватываются через `/reload-plugins`.

## web-pipeline

### Команды

| Команда | Что делает |
|---|---|
| `/web-pipeline:new-project <идея>` | grill-me → `spec.md` → архитектура ✋ → три дизайн-концепта ✋ → API-контракт → бэкенд, фронтенд и e2e → `make check` → ревью, не больше двух раундов → локальная проверка ✋ |
| `/web-pipeline:change <что изменить>` | аудит кода → grill-me по изменению → анализ влияния и план ✋ → дизайн, если меняется UI ✋ → реализация, проверки и ревью → локальная проверка ✋ |
| `/web-pipeline:deploy [staging\|production]` | preflight → `ansible-playbook --check --diff` ✋ → применение → smoke-тесты → заголовки, TLS, порты, trivy, ZAP baseline → отчёт, предложение отката |
| `/web-pipeline:secure-maintain [report\|fix] [env]` | osv-scanner, trivy, lynis и обновления на хостах → разбор находок ✋ → ветка с исправлениями → отчёт |
| `/web-pipeline:init` | Подключает проект к пайплайну. Вызывается из `new-project` и `change` |

✋ означает, что пайплайн ждёт вашего решения. Деплой на серверы запускаете только вы.

### Субагенты

| Агент | Модель | Effort | Роль |
|---|---|---|---|
| `architect` | Opus 5.5 | high | Архитектура, ADR, таблица «готовое или своё», план задач; аудит существующего кода |
| `designer` | Opus 5.5 | high | Дизайн-концепты в HTML и дизайн-система `docs/design.md` |
| `backend-dev` | Sonnet 5.5 | medium | Каркас, API-контракт, серверная логика по TDD |
| `frontend-dev` | Sonnet 5.5 | high | Интерфейс строго по `docs/design.md` |
| `qa-engineer` | Sonnet 5.5 | medium | Playwright e2e по критериям приёмки из спецификации |
| `code-reviewer` | Opus 5.5 | high | Корректность, переиспользование, простота, тесты. Только чтение |
| `security-reviewer` | Opus 5.5 | high | OWASP, авторизация, секреты, зависимости. Только чтение |
| `design-critic` | Opus 5.5 | medium | Проверка интерфейса по скриншотам. Только чтение |
| `ops-auditor` | Haiku 5.5 | medium | Сканеры уязвимостей по репозиторию, образам и хостам. Только чтение |

Если реализация дважды не проходит `make check`, задача один раз передаётся Opus. Оркестратор работает на модели текущей сессии. Переменные `CLAUDE_CODE_SUBAGENT_MODEL` и `CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1` переводят всех субагентов на одну модель.

### Навыки-знания

| Навык | Содержание |
|---|---|
| `frontend-style` | Визуальные запреты (карточная вёрстка, бейджи, сферы на фоне, эмодзи, стоковые иконки, заезженные шрифты), требование смелого направления, процесс работы с концептами, минимальная планка доступности |
| `backend-standards` | DRY, KISS, YAGNI, структура по фичам, API-контракт, валидация, модель ошибок, работа с данными, базовая безопасность, инструменты контроля |
| `testing-standards` | TDD, пирамида тестов, e2e по критериям приёмки, политика нестабильных тестов |
| `ansible-conventions` | Структура `deploy/ansible`, Vault, идемпотентные роли, атомарные релизы с откатом, роль базового харденинга |

### Хуки

Хуки активны только в проектах, где есть `.claude/web-pipeline.json`.

| Событие | Действие |
|---|---|
| PostToolUse (Write, Edit) | Форматирование и линтер изменённого файла. Ошибки сразу уходят Claude |
| Stop, SubagentStop (`backend-dev`, `frontend-dev`, `qa-engineer`) | `make check` при изменениях кода. Правки в `docs/` и `*.md` проверку не запускают. После трёх неудачных попыток подряд хук перестаёт блокировать. Включается флагом `stop_gate.enabled` |
| PreToolUse (Bash) | Подтверждение для `ansible-playbook` без `--check` и для `git push --force`. Запрет `rm -rf /` и `rm -rf ~`. Работает во всех проектах |

### Файлы в проекте

```
.claude/web-pipeline.json    # настройки хуков: команды, лимиты
.claude/state/               # состояние пайплайна и ревью (в .gitignore)
scripts/anti_slop.py         # проверка на шаблонный «ИИ-вид», запускается из make check
docs/spec.md · architecture.md · adr/ · design.md · design/concepts/ · plan.md · changes/ · deploys/ · security/
```

## Контекст

Качество ответов падает по мере заполнения контекста, а автосжатие теряет информацию. Поэтому основной диалог только координирует работу, объёмные задачи выполняют субагенты, а состояние пайплайна хранится в `.claude/state/pipeline.json` и в `docs/`.

Хук `dev-core` во время работы пайплайна сообщает оркестратору о заполнении контекста на 50%, 60% и далее. На ближайшей границе этапов оркестратор предлагает `/clear` и повторный запуск той же команды, и пайплайн продолжает с места остановки. Порог задаётся переменной `CONTEXT_WARN_PCT`. Процент хук берёт из кэша, который пишет строка состояния `~/.claude/statusline.sh`.

## Зависимости

Обязательные: `git`, `jq`, `python3`, `make`.

По стеку проекта: `semgrep`, `gitleaks`, `osv-scanner`, `trivy`, `jscpd`, `knip` или `vulture`, `ansible`, `ansible-lint`, `testssl.sh`, `nmap`, `docker` (для ZAP), на серверах `lynis`. Если инструмента нет, проверка завершается ошибкой с подсказкой по установке.

## Разработка

```bash
claude plugin validate .                                                  # marketplace и все плагины
claude --plugin-dir plugins/dev-core --plugin-dir plugins/web-pipeline    # запуск без установки
```

Соглашения по устройству плагинов описаны в [CLAUDE.md](CLAUDE.md). При публикации изменений поднимайте `version` в `plugin.json`: при установке с GitHub плагины закреплены на версии.
