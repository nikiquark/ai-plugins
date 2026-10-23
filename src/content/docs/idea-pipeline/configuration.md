---
title: "Конфигурация idea-pipeline.json"
---

Файл `.claude/idea-pipeline.json` хранит настройки идеи: целевой рынок, амбицию, обязательные оси готовности, глубину исследования и текущую стадию. Его пишет [`new-idea`](commands/new-idea.md) после интервью, из шаблона `templates/idea-pipeline.json`. Хуков у плагина нет, поэтому файл ничего не включает: это просто настройки.

## Шаблон

```json
{
  "idea": "",
  "slug": "",
  "market": {
    "geography": [],
    "languages": [],
    "currency": "",
    "model": "B2B | B2C | B2B2C | B2G"
  },
  "ambition": "lifestyle | venture",
  "minimum_outcome": "",
  "required_axes": ["CRL", "BRL", "TRL", "TMRL"],
  "depth": "standard",
  "stale_years": 3,
  "stage": "A"
}
```

## Поля

| Поле | Тип | По умолчанию | Кто читает | Значение |
|---|---|---|---|---|
| `idea` | string | — | все | Идея одним предложением |
| `slug` | string | — | оркестратор | Короткое имя для файлов |
| `market.geography` | string[] | — | исследователи | Страны или регионы рынка. Определяет каталог источников |
| `market.languages` | string[] | — | исследователи | Языки, на которых искать клиентов и конкурентов |
| `market.currency` | string | — | market-analyst, strategist | Валюта оценок рынка и юнит-экономики |
| `market.model` | string | — | все | B2B, B2C, B2B2C или B2G. Влияет на пороги по умолчанию |
| `ambition` | string | — | strategist, red-team | `lifestyle` или `venture` |
| `minimum_outcome` | string | — | market-analyst, strategist, red-team | Результат, ниже которого идея не стоит усилий. С ним сравнивается SOM |
| `required_axes` | string[] | `["CRL", "BRL", "TRL", "TMRL"]` | fact-checker | Обязательные оси [KTH](skills/readiness-levels.md). Можно добавить `IPRL`, `FRL` |
| `depth` | string | `"standard"` | исследователи | `light`, `standard` или `deep` ([уровни глубины](skills/research-standards.md#уровни-глубины)). Выбирается на GATE 1 |
| `stale_years` | int | `3` | [`idea-claims`](idea-claims.md), fact-checker | Возраст данных, после которого источник считается устаревшим |
| `stage` | string | `"A"` | evidence, readiness | Текущая стадия: `A`…`E`. Меняется только на гейте |

## Пример

```json
{
  "idea": "Учёт расходников для небольших стоматологий",
  "slug": "dental-supplies",
  "market": {
    "geography": ["RU"],
    "languages": ["ru"],
    "currency": "RUB",
    "model": "B2B"
  },
  "ambition": "lifestyle",
  "minimum_outcome": "1 млн ₽ выручки в месяц через 3 года",
  "required_axes": ["CRL", "BRL", "TRL", "TMRL"],
  "depth": "standard",
  "stale_years": 3,
  "stage": "B"
}
```

Пороги гейтов хранятся не здесь, а в `docs/idea/readiness.md`: рядом с журналом их изменений и решений.
