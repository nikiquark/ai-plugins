# ai-plugins

Marketplace плагинов для Claude Code (`nikiquark-ai-plugins`).

**Документация: <https://nikiquark.github.io/ai-plugins/>**

| Плагин | Назначение |
|---|---|
| `dev-core` | Общие компоненты пайплайнов: интервью `grill-me`, ограниченный цикл ревью `review-loop`, протокол `reuse-first`, команда `git-snapshot`, контроль контекста, MCP Context7 |
| `web-pipeline` | Веб-проекты от идеи до продакшена: спецификация, смысл и тексты с SEO, архитектура, дизайн-концепты, бэкенд и фронтенд, проверки качества, ревью, деплой через Ansible, обслуживание безопасности. Зависит от `dev-core` |

## Установка

С GitHub:

```bash
claude plugin marketplace add nikiquark/ai-plugins
claude plugin install web-pipeline@nikiquark-ai-plugins    # dev-core ставится как зависимость
```

Из локального клона:

```bash
git clone https://github.com/nikiquark/ai-plugins.git
claude plugin marketplace add ./ai-plugins                 # или абсолютный путь к клону
claude plugin install web-pipeline@nikiquark-ai-plugins
```

В сессии то же самое делают `/plugin marketplace add …` и `/plugin install …`. При установке из локальной папки правки подхватываются через `/reload-plugins`.

Подробнее: [установка](https://nikiquark.github.io/ai-plugins/getting-started/installation/), [quickstart](https://nikiquark.github.io/ai-plugins/getting-started/quickstart/), [первый проект](https://nikiquark.github.io/ai-plugins/getting-started/first-project/).

## Команды web-pipeline

| Команда | Что делает |
|---|---|
| `/web-pipeline:new-project <идея>` | Новый проект от интервью до локальной проверки |
| `/web-pipeline:change <что изменить>` | Доработка существующего проекта |
| `/web-pipeline:deploy [staging\|production]` | Деплой через Ansible с dry run и проверками безопасности |
| `/web-pipeline:secure-maintain [report\|fix] [env]` | Сканирование уязвимостей и исправления |
| `/web-pipeline:init` | Подключение проекта к пайплайну |

## Разработка

```bash
claude plugin validate .                                                  # marketplace и все плагины
claude --plugin-dir plugins/dev-core --plugin-dir plugins/web-pipeline    # запуск без установки
```

Документация собирается из `docs/` с помощью MkDocs Material:

```bash
pip install -r requirements-docs.txt
mkdocs serve
```

Соглашения описаны в [CLAUDE.md](CLAUDE.md) и в разделе [Разработка](https://nikiquark.github.io/ai-plugins/development/conventions/). При публикации изменений поднимайте `version` в `plugin.json`: при установке с GitHub плагины закреплены на версии.
