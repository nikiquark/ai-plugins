---
title: "Документация"
---

Этот сайт собирается из `src/content/docs/` с помощью [Astro Starlight](https://starlight.astro.build), а публикуется на GitHub Pages: <https://nikiquark.github.io/ai-plugins/>.

## Правило

**Изменили плагин — обновите docs.** Документация пишется вручную, поэтому при изменении скилла, агента, хука, шаблона или настройки обновите соответствующую страницу в том же коммите.

| Изменение | Страница |
|---|---|
| `skills/<name>/SKILL.md` (команда) | `src/content/docs/<plugin>/commands/<name>.md` |
| `skills/<name>/SKILL.md` (навык) | `src/content/docs/<plugin>/skills/<name>.md` |
| `agents/<name>.md` | `src/content/docs/<plugin>/agents/<name>.md`, сводки в `agents/index.md` и `reference/agents.md` |
| `bin/<name>` | `src/content/docs/<plugin>/<name>.md` |
| `hooks/hooks.json`, `scripts/*` | `src/content/docs/<plugin>/hooks.md` (или страница хука) |
| `templates/*` | `src/content/docs/<plugin>/templates.md`, `configuration.md` |
| Новый плагин | [Новый плагин](new-plugin.md), шаг 6 |

## Локальный просмотр

```bash
npm ci
npm run dev                     # http://localhost:4321/ai-plugins/, с автообновлением
```

## Проверки

CI (`.github/workflows/docs.yml`) запускает на каждом pull request и при push в `main`:

```bash
python3 scripts/check-docs.py   # у каждого скилла, агента и файла в bin/ есть страница
npm run build                   # битые ссылки и якоря между страницами — ошибка
```

`check-docs.py` ожидает такие страницы:

| Исходник | Страница |
|---|---|
| `plugins/<p>/skills/<s>/SKILL.md` | `src/content/docs/<p>/skills/<s>.md` или `src/content/docs/<p>/commands/<s>.md` |
| `plugins/<p>/agents/<a>.md` | `src/content/docs/<p>/agents/<a>.md` |
| `plugins/<p>/bin/<b>` | `src/content/docs/<p>/<b>.md` |

Он проверяет только наличие страниц, а не их содержимое.

## Публикация

При push в `main` workflow собирает сайт и публикует его через `actions/deploy-pages`. Отдельной ветки `gh-pages` нет.

Однократная настройка репозитория: **Settings → Pages → Build and deployment → Source: GitHub Actions**.

## Оформление

- Язык — русский, идентификаторы — как в исходниках.
- Страница команды: назначение · таблица свойств · этапы (Mermaid) · точки решения · кто задействован · файлы · типичные проблемы.
- Страница агента: роль · таблица (модель, effort, инструменты, навыки, кто вызывает) · вход и выход · ограничения.
- Страница скилла: когда срабатывает (цитата `description`) · что делает · как вызвать · с чем взаимодействует.
- Заголовок страницы задаётся в frontmatter (`title:`), а не через `# H1`. Новая страница добавляется в `sidebar` в `astro.config.mjs`.
- Врезки — синтаксис Starlight: `:::tip[Заголовок]` … `:::` (типы `note`, `tip`, `caution`, `danger`). Сворачиваемые блоки — `<details>`.
- Ссылки между страницами — относительные пути к `.md`, как в остальных страницах: они работают и на GitHub, и на сайте. MDX не используем: валидатор ссылок его не проверяет.
- Mermaid — только там, где показан поток, без декоративных схем.
- Заголовки на русском получают якоря на кириллице (`#строка-состояния`), используйте их в ссылках.
