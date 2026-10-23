# Переменные окружения

## Настраиваете вы

| Переменная | По умолчанию | Кто читает | Значение |
|---|---|---|---|
| `CONTEXT_WARN_PCT` | `50` | [context-guard](../dev-core/context-guard.md) | Порог заполнения контекста, после которого оркестратор получает предупреждения (раз на каждые 10%) |
| `CLAUDE_CODE_SUBAGENT_MODEL` | — | Claude Code | Модель для всех субагентов |
| `CLAUDE_CODE_SUBAGENT_MODEL_FORCE` | — | Claude Code | `1`: применять `CLAUDE_CODE_SUBAGENT_MODEL` даже к агентам с моделью во frontmatter |
| `XDG_CACHE_HOME` | `~/.cache` | context-guard, строка состояния | Корень кэша `claude-context/` |
| `BASE_URL` | — | Playwright-тесты проекта | Адрес приложения для e2e и `@smoke`-прогона при деплое |

```bash
CONTEXT_WARN_PCT=40 claude
CLAUDE_CODE_SUBAGENT_MODEL=sonnet CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1 claude
```

## Задаёт Claude Code

| Переменная | Где доступна | Значение |
|---|---|---|
| `${CLAUDE_PLUGIN_ROOT}` | Текст скиллов и агентов, окружение хуков. **Не** в инструменте Bash | Корень установленного плагина (каталог в кэше версий) |
| `${CLAUDE_PLUGIN_DATA}` | Текст скиллов и агентов, хуки | Постоянная папка данных плагина; там живёт `font-registry.md` |
| `CLAUDE_PROJECT_DIR` | Окружение хуков | Корень проекта. Если её нет, хуки берут `cwd` из входного JSON |
| `$ARGUMENTS` | Текст скилла | Аргументы, переданные команде |
