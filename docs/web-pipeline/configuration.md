# Конфигурация web-pipeline.json

Файл `.claude/web-pipeline.json` в корне проекта решает две задачи: включает [хуки](hooks.md) плагина для этого проекта и хранит их настройки. Его создаёт [`init`](commands/init.md) из шаблона `templates/web-pipeline.json`.

## Шаблон

```json
{
  "stack": "TBD",
  "commands": {
    "format_file": "",
    "lint_file": "",
    "check": "make check"
  },
  "lint_extensions": [],
  "stop_gate": {
    "enabled": false,
    "max_blocks": 3,
    "timeout_seconds": 540
  }
}
```

## Поля

| Поле | Тип | По умолчанию | Кто читает | Значение |
|---|---|---|---|---|
| `stack` | string | `"TBD"` | Оркестраторы | Стек проекта. Заполняется после GATE 1 |
| `commands.format_file` | string | `""` | post-edit | Команда форматирования одного файла, `{file}` заменяется путём |
| `commands.lint_file` | string | `""` | post-edit | Команда линтера одного файла. Ненулевой код возврата — ошибка, которая уходит Claude |
| `commands.check` | string | `"make check"` | stop-gate | Полная проверка проекта |
| `lint_extensions` | string[] | `[]` | post-edit | Расширения с точкой, например `[".ts", ".tsx"]`. Остальные файлы post-edit пропускает |
| `stop_gate.enabled` | bool | `false` | stop-gate | `false` выключает stop-gate. Включается в D1 |
| `stop_gate.max_blocks` | int | `3` | stop-gate | Сколько раз подряд можно заблокировать остановку, прежде чем хук сдастся |
| `stop_gate.timeout_seconds` | int | `540` | stop-gate | Таймаут `check`. Таймаут самого хука — 600 с |

## Примеры

=== "TypeScript"

    ```json
    {
      "stack": "Next.js 15 + Postgres (Drizzle)",
      "commands": {
        "format_file": "npx prettier --write {file}",
        "lint_file": "npx eslint {file}",
        "check": "make check"
      },
      "lint_extensions": [".ts", ".tsx", ".js", ".jsx", ".mjs"],
      "stop_gate": { "enabled": true, "max_blocks": 3, "timeout_seconds": 540 }
    }
    ```

=== "Python"

    ```json
    {
      "stack": "Django 5 + Postgres",
      "commands": {
        "format_file": "ruff format {file}",
        "lint_file": "ruff check {file}",
        "check": "make check"
      },
      "lint_extensions": [".py"],
      "stop_gate": { "enabled": true, "max_blocks": 3, "timeout_seconds": 540 }
    }
    ```

=== "Biome"

    ```json
    {
      "stack": "Astro + Hono",
      "commands": {
        "format_file": "npx biome format --write {file}",
        "lint_file": "npx biome lint {file}",
        "check": "make check"
      },
      "lint_extensions": [".ts", ".tsx", ".astro"],
      "stop_gate": { "enabled": true, "max_blocks": 3, "timeout_seconds": 540 }
    }
    ```

## Советы

- Команда `lint_file` должна работать на одном файле быстро: каждая команда post-edit ограничена 60 с.
- Если `make check` медленный, увеличьте `timeout_seconds`, но не больше ~580: иначе Claude Code прервёт сам хук по таймауту 600 с.
- Не ставьте `stop_gate.enabled: true`, пока `make check` не проходит: каждая остановка будет блокироваться до `max_blocks`.
