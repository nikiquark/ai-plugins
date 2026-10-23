# anti_slop.py

Статическая проверка на визуальные признаки шаблонного фронтенда, сгенерированного ИИ. Она ловит то из запретов [`frontend-style`](skills/frontend-style.md), что можно поймать без браузера. Остальное оценивает [design-critic](agents/design-critic.md) по скриншотам.

| | |
|---|---|
| В плагине | `plugins/web-pipeline/templates/anti_slop.py` |
| В проекте | `scripts/anti_slop.py` (копию ставит [`init`](commands/init.md)) |
| Зависимости | Только стандартная библиотека Python 3 |
| Запускается | Из `make check`, вручную, дизайнером на концептах, критиком с `--strict` |

Копия принадлежит проекту: её можно настраивать, и она работает в CI без Claude.

## Использование

```bash
python3 scripts/anti_slop.py [paths...] [--since REF] [--strict] [--quiet]
```

| Флаг | Эффект |
|---|---|
| `paths` | Что проверять (по умолчанию `.`). Внутри git берутся отслеживаемые и неигнорируемые файлы |
| `--since REF` | Только файлы, изменённые с `REF` (включая незакоммиченные и новые). Для унаследованного кода: `--since origin/main` |
| `--strict` | Предупреждения считаются ошибками |
| `--quiet` | Печатать только ошибки |

Ошибки дают exit 1, предупреждения только печатаются. Формат строки: `path:line: [error|warn] rule: message`.

## Правила

| Правило | Уровень | Что ловит |
|---|---|---|
| `icon-library` | error | Импорт или CDN lucide, heroicons, tabler, feather, react-icons |
| `banned-font` | error | Inter, Roboto, Open Sans, Lato, Arial, Montserrat, Poppins, Geist, Geist Mono, Space Grotesk, system-ui, -apple-system, BlinkMacSystemFont как основной шрифт: в `font-family`, `fontFamily`, теме Tailwind, URL Google Fonts, `next/font`, `@fontsource` |
| `background-orb` | error | `rounded-full` вместе с `blur-2xl`/`blur-3xl`/`blur-[NNpx]`, или CSS `filter: blur(≥40px)` |
| `purple-gradient` | error | Tailwind-градиент с `from-`, `via-` или `to-` цвета purple, violet, indigo, fuchsia, или CSS-градиент с фиолетовыми цветами (по имени или по оттенку 250–300°) |
| `emoji` | error | Эмодзи и пиктографические символы в исходниках UI |
| `gradient-text` | warn | `bg-clip-text` + `text-transparent`, или `background-clip: text` |
| `badge` | warn | `rounded-full` + маленькие `px`/`py` + `text-xs` |
| `card` | warn | `rounded-lg…3xl` + `shadow*` |
| `glassmorphism` | warn | `backdrop-blur` или `backdrop-filter: blur` |
| `eyebrow` | warn | `uppercase` + `tracking-wide…` + `text-xs`/`text-sm` |

Проверяются файлы `.html`, `.css`, `.scss`, `.js`, `.ts`, `.tsx`, `.vue`, `.svelte`, `.astro`, `.mdx`, шаблоны Jinja, Twig, ERB, Handlebars, Liquid, PHP и другие, а также `package.json`. Пропускаются `node_modules`, `dist`, `build`, `.next`, `vendor`, `.venv`, отчёты тестов и минифицированные файлы.

## Исключения

Намеренное исключение помечается на той же строке комментарием:

```css
font-family: "Inter", sans-serif; /* anti-slop: allow брендбук клиента требует Inter */
```

Причина обязательна: ревьюеры её проверяют. frontend-dev упоминает каждое использование в отчёте.

## Настройка под проект

Списки `BANNED_FONTS`, `ICON_PACKAGES`, `UI_EXTENSIONS`, `SKIP_DIRS` и `RULES` в начале файла можно править. Изменения касаются только копии в проекте, шаблон в плагине не меняется.
