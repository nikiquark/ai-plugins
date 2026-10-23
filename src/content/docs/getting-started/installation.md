---
title: "Установка"
---

Плагины распространяются как marketplace `nikiquark-ai-plugins`. Сначала подключается marketplace, затем из него ставятся плагины. `web-pipeline` объявляет `dev-core` зависимостью, поэтому `dev-core` ставится автоматически.

Каждую команду ниже можно выполнить в терминале (`claude plugin …`) или внутри сессии Claude Code (`/plugin …`).

## С GitHub

Обычный способ для работы с плагинами.

```bash
claude plugin marketplace add nikiquark/ai-plugins
claude plugin install web-pipeline@nikiquark-ai-plugins
```

Если нужен только общий набор без веб-пайплайна:

```bash
claude plugin install dev-core@nikiquark-ai-plugins
```

Плагины с GitHub закреплены на версии из `plugin.json`. Чтобы получить новую версию:

```bash
claude plugin marketplace update nikiquark-ai-plugins
claude plugin update web-pipeline@nikiquark-ai-plugins
```

## Из локального клона

Удобно, если вы правите плагины сами или хотите поставить версию из своей ветки.

```bash
git clone https://github.com/nikiquark/ai-plugins.git
claude plugin marketplace add ./ai-plugins       # или абсолютный путь к клону
claude plugin install web-pipeline@nikiquark-ai-plugins
```

`marketplace add` принимает любой путь к папке, в которой лежит `.claude-plugin/marketplace.json`. Чтобы сессия увидела правки в клоне, выполните `/reload-plugins`.

## Без установки

Для разработки и разовых экспериментов плагины можно подключить только на время одной сессии. Запускайте из корня клона:

```bash
claude --plugin-dir plugins/dev-core --plugin-dir plugins/web-pipeline
```

Флаг `--plugin-dir` повторяется для каждого плагина. Подключайте `dev-core` вместе с `web-pipeline`, иначе `web-pipeline` не найдёт свою зависимость.

## Область установки

По умолчанию плагин ставится для пользователя (`--scope user`) и доступен во всех проектах. Варианты:

| Scope | Где записывается | Когда выбирать |
|---|---|---|
| `user` | Ваши пользовательские настройки | Плагины нужны везде (по умолчанию) |
| `project` | `.claude/settings.json` проекта, попадает в git | Вся команда проекта работает с пайплайном |
| `local` | `.claude/settings.local.json` проекта, не в git | Только вы и только в этом проекте |

```bash
claude plugin install web-pipeline@nikiquark-ai-plugins --scope project
```

:::note[Хуки не мешают другим проектам]
Даже при установке для пользователя хуки `web-pipeline` ничего не делают, пока в проекте нет файла `.claude/web-pipeline.json`. Хук `dev-core` срабатывает только при активном пайплайне. Подробнее на странице [Хуки](../web-pipeline/hooks.md).
:::

## Проверка

```bash
claude plugin list
```

В списке должны быть `dev-core` и `web-pipeline`. Дальше выполните [Quickstart](quickstart.md), чтобы проверить команды и агентов внутри сессии.

## Удаление

```bash
claude plugin uninstall web-pipeline@nikiquark-ai-plugins
claude plugin uninstall dev-core@nikiquark-ai-plugins
claude plugin marketplace remove nikiquark-ai-plugins
```

Файлы, которые пайплайн создал в проектах (`.claude/web-pipeline.json`, `docs/`, `scripts/anti_slop.py`, `scripts/seo_check.py`), остаются на месте: они принадлежат проекту.
