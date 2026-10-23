# init

Подключает проект к веб-пайплайну: создаёт `.claude/web-pipeline.json` (он включает хуки плагина), ставит проверки anti-slop и SEO, подключает `make check` и `make seo`, создаёт `.claude/state/` и раздел в `CLAUDE.md`.

| | |
|---|---|
| Вызов | `/web-pipeline:init [--legacy]` |
| Автовызов | Да, когда веб-пайплайн впервые запускается в проекте |
| Кто вызывает | Фаза 0 в [`new-project`](new-project.md) и [`change`](change.md) |
| Исходник | `plugins/web-pipeline/skills/init/SKILL.md` |

## Зачем

Хуки плагина (линтер после правок, `make check` перед остановкой) ничего не делают, пока нет `.claude/web-pipeline.json`. Благодаря этому другие проекты, например научные, остаются нетронутыми.

!!! warning "Ничего не перезаписывается без вопроса"
    Если файл уже есть, init объединяет содержимое и показывает diff.

## Шаги

1. **Определить стек** по lock-файлам и манифестам: `package.json`, `pnpm-lock.yaml`, `pyproject.toml`, `uv.lock`, `requirements*.txt`, `manage.py`, `Dockerfile`, `deploy/ansible/`. Для нового пустого проекта стек записывается как `TBD`.
2. **Записать `.claude/web-pipeline.json`** из [шаблона](../configuration.md) и заполнить команды для стека:
    - `format_file` и `lint_file`: команды для одного файла с подстановкой `{file}`, их запускает post-edit-хук. Например, `npx prettier --write {file}` / `npx eslint {file}` или `ruff format {file}` / `ruff check {file}`. Пока стек `TBD`, команды пустые;
    - `check`: обычно `make check`;
    - `lint_extensions`: расширения, которые понимает `lint_file`;
    - `stop_gate.enabled`: `false`, пока `make check` не существует и не проходит. В новом проекте его включает фаза D1. В существующем init один раз запускает `make check`: если проверка проходит, ставит `true`, иначе оставляет `false` и перечисляет ошибки.
3. **Поставить проверки.** `templates/anti_slop.py` копируется в `scripts/anti_slop.py`. Копия принадлежит проекту, поэтому работает и в CI, и без Claude. Для существующего кода (`--legacy`, или если аудит нашёл существующий UI) `make check` запускает её как `python3 scripts/anti_slop.py --since origin/main`: проверяются только изменённые файлы, и старый код не блокирует каждое изменение. Подробнее на странице [anti_slop.py](../anti-slop.md).

    Так же копируется `templates/seo_check.py` в `scripts/seo_check.py`. Он проверяет запущенный сайт, поэтому в `make check` не входит ([seo_check.py](../seo-check.md)).
4. **Подключить `make check` и `make seo`.** Если `Makefile` есть, добавить или расширить цель `check` и показать diff. Если нет, создать его с целями `check`, `dev`, `test`, `lint`, `fmt`, `seo`. Для невыбранных инструментов ставятся заглушки, которые **падают** с понятным сообщением (`@echo "configure lint for <stack>" && exit 1`), а не проходят молча. Цель `seo` запускает `seo_check.py` против dev-сервера ([make seo](../seo-check.md#make-seo)): `BASE_URL` — адрес dev-сервера, а `SITE_URL` и `SEO_EXPECT` берутся из `docs/content.md`, когда он появится.
5. **Папка состояния.** Создать `.claude/state/` и добавить её в `.gitignore`.
6. **Раздел в CLAUDE.md.** Дописать [шаблон раздела](../templates.md#claude-md-sectionmd) в `CLAUDE.md` проекта (создать файл при необходимости) и заполнить стек и команды. Если раздел уже есть, обновить его на месте.
7. **Отчёт:** что создано или изменено, каких инструментов, нужных `make check`, не хватает (с командами установки), и что хуки теперь активны в проекте.

## Аргументы

| Аргумент | Эффект |
|---|---|
| `--legacy` | Существующий код: anti-slop проверяет только изменения относительно `origin/main` |

## Отключить пайплайн в проекте

Удалите или переименуйте `.claude/web-pipeline.json`, и хуки форматирования и stop-gate перестанут работать. Guard для Bash продолжит работать, потому что он не зависит от этого файла ([Хуки](../hooks.md)).
