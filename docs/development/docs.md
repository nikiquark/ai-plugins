# Документация

Этот сайт собирается из `docs/` с помощью [MkDocs](https://www.mkdocs.org) и темы [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/), а публикуется на GitHub Pages: <https://nikiquark.github.io/ai-plugins/>.

## Правило

**Изменили плагин — обновите docs.** Документация пишется вручную, поэтому при изменении скилла, агента, хука, шаблона или настройки обновите соответствующую страницу в том же коммите.

| Изменение | Страница |
|---|---|
| `skills/<name>/SKILL.md` (команда) | `docs/<plugin>/commands/<name>.md` |
| `skills/<name>/SKILL.md` (навык) | `docs/<plugin>/skills/<name>.md` |
| `agents/<name>.md` | `docs/<plugin>/agents/<name>.md`, сводки в `agents/index.md` и `reference/agents.md` |
| `bin/<name>` | `docs/<plugin>/<name>.md` |
| `hooks/hooks.json`, `scripts/*` | `docs/<plugin>/hooks.md` (или страница хука) |
| `templates/*` | `docs/<plugin>/templates.md`, `configuration.md` |
| Новый плагин | [Новый плагин](new-plugin.md), шаг 6 |

## Локальный просмотр

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements-docs.txt
.venv/bin/mkdocs serve          # http://127.0.0.1:8000, с автообновлением
```

## Проверки

CI (`.github/workflows/docs.yml`) запускает на каждом pull request и при push в `main`:

```bash
python3 scripts/check-docs.py   # у каждого скилла, агента и файла в bin/ есть страница
mkdocs build --strict           # битые ссылки и якоря, страницы вне nav — ошибка
```

`check-docs.py` ожидает такие страницы:

| Исходник | Страница |
|---|---|
| `plugins/<p>/skills/<s>/SKILL.md` | `docs/<p>/skills/<s>.md` или `docs/<p>/commands/<s>.md` |
| `plugins/<p>/agents/<a>.md` | `docs/<p>/agents/<a>.md` |
| `plugins/<p>/bin/<b>` | `docs/<p>/<b>.md` |

Он проверяет только наличие страниц, а не их содержимое.

## Публикация

При push в `main` workflow собирает сайт и публикует его через `actions/deploy-pages`. Отдельной ветки `gh-pages` нет.

Однократная настройка репозитория: **Settings → Pages → Build and deployment → Source: GitHub Actions**.

## Оформление

- Язык — русский, идентификаторы — как в исходниках.
- Страница команды: назначение · таблица свойств · этапы (Mermaid) · точки решения · кто задействован · файлы · типичные проблемы.
- Страница агента: роль · таблица (модель, effort, инструменты, навыки, кто вызывает) · вход и выход · ограничения.
- Страница скилла: когда срабатывает (цитата `description`) · что делает · как вызвать · с чем взаимодействует.
- Mermaid — только там, где показан поток, без декоративных схем.
- Заголовки на русском получают якоря на кириллице (`#строка-состояния`), используйте их в ссылках.
