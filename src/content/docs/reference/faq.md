---
title: "FAQ и проблемы"
---

## Установка

<details>
<summary><code>web-pipeline</code> не видит <code>dev-core:*</code> скиллы</summary>

При установке из marketplace зависимость ставится автоматически. При запуске через `--plugin-dir` её нужно подключить явно: `claude --plugin-dir plugins/dev-core --plugin-dir plugins/web-pipeline`.

</details>

<details>
<summary>Правки в локальном клоне не подхватываются</summary>

Выполните `/reload-plugins`. Если marketplace подключён с GitHub, а не из папки, правки в клоне вообще не используются: подключите его из папки ([Установка](../getting-started/installation.md#из-локального-клона)).

</details>

<details>
<summary>После обновления с GitHub ничего не поменялось</summary>

Плагины закреплены на `version` из `plugin.json`. Нужны и `claude plugin marketplace update nikiquark-ai-plugins`, и `claude plugin update <plugin>@nikiquark-ai-plugins`. Если версия в репозитории не поднята, обновления не будет.

</details>

## Хуки

<details>
<summary>Хуки не срабатывают в проекте</summary>

Проверьте, что есть `.claude/web-pipeline.json` (его создаёт [`init`](../web-pipeline/commands/init.md)) и установлен `jq`. Для stop-gate нужен `"stop_gate": { "enabled": true }` и git-репозиторий.

</details>

<details>
<summary>Хуки мешают в проекте, где пайплайн не нужен</summary>

Их там не должно быть: все хуки, кроме guard для Bash, требуют `.claude/web-pipeline.json`. Guard только спрашивает подтверждение на `ansible-playbook` без `--check` и `git push --force`.

</details>

<details>
<summary>Stop-хук блокирует завершение снова и снова</summary>

После `max_blocks` (по умолчанию 3) неудач подряд он сам перестаёт блокировать и сообщает об этом. Если `make check` ещё не может пройти, поставьте `stop_gate.enabled: false` до исправления каркаса.

</details>

<details>
<summary>Линтер после правки падает по таймауту</summary>

Каждая команда post-edit ограничена 60 секундами. Используйте линтер для одного файла (`eslint {file}`, `ruff check {file}`), а не для всего проекта.

</details>

## Контекст

<details>
<summary>Оркестратор не предлагает /clear</summary>

context-guard работает, только если ваша строка состояния пишет процент в `~/.cache/claude-context/<session_id>`. Пример скрипта есть на странице [Контекст и /clear](../concepts/context.md#строка-состояния). Без него оркестратор всё равно предлагает перезапуск в чистых точках, если диалог длинный.

</details>

<details>
<summary>После /clear пайплайн начал заново</summary>

Значит, нет `.claude/state/pipeline.json`. Проверьте, что запускаете команду из корня того же проекта. Для `change` нужен `"flow": "change"` в файле.

</details>

## Пайплайн

<details>
<summary>Можно ли пропустить точку решения?</summary>

Нет. Но вы можете отвечать коротко («утверждаю», «A») и заранее дать указания в аргументах команды.

</details>

<details>
<summary>Как сделать дешевле?</summary>

`CLAUDE_CODE_SUBAGENT_MODEL=sonnet CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1` переводит всех субагентов на Sonnet. Качество архитектуры, дизайна и ревью при этом снизится.

</details>

<details>
<summary>anti_slop.py ругается на старый код</summary>

Для существующих проектов `make check` должен вызывать `python3 scripts/anti_slop.py --since origin/main`. Тогда проверяются только изменённые файлы.

</details>

<details>
<summary>Мне нужен Inter по брендбуку</summary>

Пометьте строку `anti-slop: allow <причина>` и зафиксируйте это в `docs/design.md`. Ревьюер проверит, что причина реальная.

</details>

<details>
<summary>У меня закрытое приложение, SEO не нужно</summary>

Скажите это на интервью. [content-strategist](../web-pipeline/agents/content-strategist.md) запишет в `docs/content.md`, что сайт закрыт, и напишет только тексты интерфейса. В `Makefile` поставьте `SEO_EXPECT ?= noindex`: тогда [`make seo`](../web-pipeline/seo-check.md) проверяет, что страницы не попадут в поиск.

</details>

<details>
<summary>Хочу запретить AI-ботов</summary>

По умолчанию robots.txt пускает всех роботов. Скажите на интервью или на GATE 1, каких ботов закрыть. Учтите, что боты для обучения моделей (GPTBot, ClaudeBot, Google-Extended) и боты для поиска в AI-ассистентах (OAI-SearchBot, Claude-SearchBot, PerplexityBot) — разные. Если закрыть вторых, сайт пропадёт из ответов AI.

</details>

<details>
<summary>Почему нет llms.txt?</summary>

Крупные поисковые системы и AI-сервисы не подтвердили, что читают его, поэтому по умолчанию он не делается. Если нужен, попросите на интервью.

</details>

<details>
<summary>Пайплайн задеплоил без меня?</summary>

Не может. Deploy запускается только вручную (`disable-model-invocation`), применение требует вашего «go», а guard-хук дополнительно спрашивает разрешение на `ansible-playbook` без `--check`.

</details>
