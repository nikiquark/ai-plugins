# FAQ и проблемы

## Установка

??? question "`web-pipeline` не видит `dev-core:*` скиллы"
    При установке из marketplace зависимость ставится автоматически. При запуске через `--plugin-dir` её нужно подключить явно: `claude --plugin-dir plugins/dev-core --plugin-dir plugins/web-pipeline`.

??? question "Правки в локальном клоне не подхватываются"
    Выполните `/reload-plugins`. Если marketplace подключён с GitHub, а не из папки, правки в клоне вообще не используются: подключите его из папки ([Установка](../getting-started/installation.md#из-локального-клона)).

??? question "После обновления с GitHub ничего не поменялось"
    Плагины закреплены на `version` из `plugin.json`. Нужны и `claude plugin marketplace update nikiquark-ai-plugins`, и `claude plugin update <plugin>@nikiquark-ai-plugins`. Если версия в репозитории не поднята, обновления не будет.

## Хуки

??? question "Хуки не срабатывают в проекте"
    Проверьте, что есть `.claude/web-pipeline.json` (его создаёт [`init`](../web-pipeline/commands/init.md)) и установлен `jq`. Для stop-gate нужен `"stop_gate": { "enabled": true }` и git-репозиторий.

??? question "Хуки мешают в проекте, где пайплайн не нужен"
    Их там не должно быть: все хуки, кроме guard для Bash, требуют `.claude/web-pipeline.json`. Guard только спрашивает подтверждение на `ansible-playbook` без `--check` и `git push --force`.

??? question "Stop-хук блокирует завершение снова и снова"
    После `max_blocks` (по умолчанию 3) неудач подряд он сам перестаёт блокировать и сообщает об этом. Если `make check` ещё не может пройти, поставьте `stop_gate.enabled: false` до исправления каркаса.

??? question "Линтер после правки падает по таймауту"
    Каждая команда post-edit ограничена 60 секундами. Используйте линтер для одного файла (`eslint {file}`, `ruff check {file}`), а не для всего проекта.

## Контекст

??? question "Оркестратор не предлагает /clear"
    context-guard работает, только если ваша строка состояния пишет процент в `~/.cache/claude-context/<session_id>`. Пример скрипта есть на странице [Контекст и /clear](../concepts/context.md#строка-состояния). Без него оркестратор всё равно предлагает перезапуск в чистых точках, если диалог длинный.

??? question "После /clear пайплайн начал заново"
    Значит, нет `.claude/state/pipeline.json`. Проверьте, что запускаете команду из корня того же проекта. Для `change` нужен `"flow": "change"` в файле.

## Пайплайн

??? question "Можно ли пропустить точку решения?"
    Нет. Но вы можете отвечать коротко («утверждаю», «A») и заранее дать указания в аргументах команды.

??? question "Как сделать дешевле?"
    `CLAUDE_CODE_SUBAGENT_MODEL=sonnet CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1` переводит всех субагентов на Sonnet. Качество архитектуры, дизайна и ревью при этом снизится.

??? question "anti_slop.py ругается на старый код"
    Для существующих проектов `make check` должен вызывать `python3 scripts/anti_slop.py --since origin/main`. Тогда проверяются только изменённые файлы.

??? question "Мне нужен Inter по брендбуку"
    Пометьте строку `anti-slop: allow <причина>` и зафиксируйте это в `docs/design.md`. Ревьюер проверит, что причина реальная.

??? question "Пайплайн задеплоил без меня?"
    Не может. Deploy запускается только вручную (`disable-model-invocation`), применение требует вашего «go», а guard-хук дополнительно спрашивает разрешение на `ansible-playbook` без `--check`.
