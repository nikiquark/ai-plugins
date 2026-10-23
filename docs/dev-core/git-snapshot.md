# git-snapshot

Печатает хэш git-дерева текущей рабочей копии: отслеживаемые и неотслеживаемые файлы с учётом `.gitignore`. Индекс, stash и история при этом не меняются.

| | |
|---|---|
| Вызов | `git-snapshot` или `git snapshot` |
| Где доступен | В PATH инструмента Bash, пока включён `dev-core` |
| Кто использует | [`review-loop`](skills/review-loop.md), [`new-project`](../web-pipeline/commands/new-project.md), [`change`](../web-pipeline/commands/change.md) |
| Исходник | `plugins/dev-core/bin/git-snapshot` |

## Зачем

Пайплайну нужно точно знать, что изменилось с определённого момента, даже если ничего не закоммичено. Обычный `git stash create` или `git add` меняет состояние, которое принадлежит вам. `git-snapshot` записывает дерево через временный индекс и возвращает только хэш.

## Использование

```bash
base=$(git-snapshot)
# … работа …
now=$(git-snapshot)
git diff "$base" "$now"            # всё, что изменилось
git diff --stat "$base" "$now"
```

Так считаются объёмы ревью в `review-loop` (`base..round_start`, `round_start..новый снимок`) и `implementation_base` в `pipeline.json`.

## Как работает

1. Создаёт временный индекс `$GIT_DIR/snapshot-index.<pid>` и удаляет его при выходе.
2. Если есть `HEAD`, загружает его дерево в этот индекс (`git read-tree HEAD`).
3. Добавляет все файлы рабочей копии (`git add -A`) во временный индекс.
4. Записывает дерево (`git write-tree`) и печатает его хэш.

Объекты попадают в базу объектов git, но на них не ссылается ни одна ветка, поэтому со временем их уберёт `git gc`.

## Почему в bin/

`${CLAUDE_PLUGIN_ROOT}` подставляется в текст скиллов и в окружение хуков, но не попадает в окружение инструмента Bash. Исполняемые файлы из `bin/` плагина Claude Code сам добавляет в PATH. Поскольку имя начинается с `git-`, git также понимает его как подкоманду `git snapshot`.
