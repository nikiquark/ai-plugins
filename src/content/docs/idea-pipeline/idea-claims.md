---
title: "idea-claims"
---

Проверяет, что у каждой цифры в исследовании идеи есть метка: источник, расчёт, оценка, гипотеза или слова основателя, и что каждый процитированный источник есть в списке.

| | |
|---|---|
| Вызов | `idea-claims [папка или файл …]`, по умолчанию `docs/idea` |
| Где доступен | В PATH инструмента Bash, пока включён `idea-pipeline` |
| Кто использует | [`new-idea`](commands/new-idea.md) (фазы 4 и 8, команда проверки в [review-loop](../dev-core/skills/review-loop.md)) |
| Зависимости | `python3` |
| Исходник | `plugins/idea-pipeline/bin/idea-claims` |

## Что проверяет

Для папки проверяются файлы исследования: `preflight.md`, `market.md`, `competitors.md`, `customers.md`, `strategy.md`, `risks.md`, `memo.md`. Бриф, дерево гипотез, `readiness.md`, `experiments.md` и заметки-доказательства не проверяются: там утверждения основателя, гипотезы и пороги.

**Ошибки** (код возврата 1):

- строка с количеством без метки `[S#]`, `[calc]`, `[est]`, `[hyp]` или `[user]`. Количество — это проценты, деньги, порядки (`млн`, `bn`, `k`), множители (`3x`), числа от четырёх знаков и дробные;
- ссылка `[S#]`, которой нет в разделе `## Sources` этого файла.

**Предупреждения** (код возврата 0):

- веб-источник без URL или без даты `accessed YYYY-MM-DD`;
- источник старше `stale_years` из [`.claude/idea-pipeline.json`](configuration.md) (по умолчанию 3 года).

Не считаются количеством: годы и диапазоны лет, даты ISO, id (`H2.1`, `EXP-3`, `CRL 4`, `FC-2`), `B2B`, `2×2`, содержимое блоков кода и инлайн-кода, адреса ссылок. Разделы `## Sources` и `## Data requests` проверяются отдельно или пропускаются.

## Пример

```bash
$ idea-claims
docs/idea/market.md:10: number without a claim label: - There are 15000 shops in Moscow.
docs/idea/market.md:8: [S9] is not listed under '## Sources'
warning: docs/idea/market.md:31: source S2 is from 2019, older than 3 years
idea-claims: 7 file(s), 2 error(s), 1 warning(s)
```

## Ограничения

- Проверка построчная: одной метки на строке достаточно, даже если цифр несколько.
- Скрипт проверяет наличие меток, а не их правдивость. Правдивость проверяет [fact-checker](agents/fact-checker.md), который открывает источники.

## Почему в bin/

Исполняемые файлы из `bin/` плагина Claude Code добавляет в PATH инструмента Bash, а `${CLAUDE_PLUGIN_ROOT}` в Bash недоступен ([Соглашения](../development/conventions.md)).
