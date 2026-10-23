# Новый плагин

Пошаговое добавление доменного плагина (условное имя `foo-pipeline`).

## 1. Каркас

```text
plugins/foo-pipeline/
  .claude-plugin/plugin.json
  skills/
  agents/
  hooks/hooks.json        # если нужны хуки
  scripts/
```

`plugin.json`:

```json
{
  "name": "foo-pipeline",
  "displayName": "Foo Pipeline",
  "version": "0.1.0",
  "description": "One line in English",
  "author": { "name": "nikiquark", "email": "nikiquark@gmail.com" },
  "license": "MIT",
  "keywords": ["foo"],
  "dependencies": ["dev-core"]
}
```

## 2. Регистрация в marketplace

Добавьте запись в `.claude-plugin/marketplace.json`:

```json
{
  "name": "foo-pipeline",
  "source": "./plugins/foo-pipeline",
  "description": "One line in English"
}
```

## 3. Оркестратор

- Скилл-команда с `disable-model-invocation: true` и `argument-hint`.
- Раздел «Resume first»: прочитать `.claude/state/pipeline.json` и продолжить.
- Сразу после старта записывать `pipeline.json` с `flow` и `phase`, чтобы работал context-guard.
- Общие механизмы вызывать из `dev-core`: `dev-core:grill-me` для интервью, `dev-core:review-loop` для ревью, `git-snapshot` для снимков.
- Явные GATE там, где решение принимает пользователь.

## 4. Хуки

- Файл-маркер `.claude/foo-pipeline.json` в проекте; без него хук сразу выходит с кодом 0.
- Скилл `init`, который создаёт маркер.
- Скрипты вызываются как `"${CLAUDE_PLUGIN_ROOT}/scripts/<name>.sh"`.

## 5. Агенты

- Модель и effort под задачу; ревьюеры — с `disallowedTools`.
- Самодостаточные инструкции: агент не видит диалог.
- Формат отчёта, который удобно разбирать оркестратору (для ревьюеров — вердикт `review-loop`).

## 6. Документация

- Раздел `docs/foo-pipeline/` по образцу `docs/web-pipeline/`: `index.md`, `commands/`, `agents/`, `skills/`.
- Страница на каждый скилл, агента и файл в `bin/`. Иначе упадёт `scripts/check-docs.py`.
- Пункты в `nav` в `mkdocs.yml`. Иначе упадёт `mkdocs build --strict`.
- Строка в таблице плагинов в `README.md` и `docs/index.md`.

## 7. Проверка

```bash
claude plugin validate .
claude --plugin-dir plugins/dev-core --plugin-dir plugins/foo-pipeline
python3 scripts/check-docs.py && mkdocs build --strict
```

Подробнее на странице [Валидация и версии](validation.md).
