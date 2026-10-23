# Валидация и версии

## После любого изменения

```bash
claude plugin validate .
```

Команда проверяет `marketplace.json` и все плагины: манифесты, frontmatter скиллов и агентов, `hooks.json`, `.mcp.json`.

## Запуск без установки

```bash
claude --plugin-dir plugins/dev-core --plugin-dir plugins/web-pipeline
```

Плагины подключаются только на эту сессию, прямо из рабочей копии. Так проще всего проверить правку в деле. Внутри сессии `/reload-plugins` перечитывает изменения.

## Проверка хуков вручную

Скрипты хуков читают JSON из stdin, поэтому их можно вызывать напрямую:

```bash
echo '{"tool_input":{"command":"ansible-playbook site.yml"}}' \
  | plugins/web-pipeline/scripts/guard-bash.sh
# → {"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"ask",…}}

echo '{"session_id":"x","hook_event_name":"UserPromptSubmit","cwd":"'"$PWD"'"}' \
  | plugins/dev-core/scripts/context-guard.sh
```

## Версии

- При публикации изменений поднимайте `version` в `plugin.json` **изменённого** плагина. При установке с GitHub плагины закреплены на версии, и без повышения пользователи не получат обновление.
- Схема версий: semver. `0.x` — пока поведение пайплайнов меняется.
- Изменения только в `docs/`, `README.md`, `mkdocs.yml` и корневых файлах не требуют повышения версии плагинов.

## Коммиты

Semantic Commit Messages: `<type>(<scope>): <summary>`, например `feat(web-pipeline): add smoke playbook check`. В качестве scope используется имя плагина или `docs`.
