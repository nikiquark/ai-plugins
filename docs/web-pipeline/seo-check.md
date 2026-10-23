# seo_check.py

Проверка запущенного сайта на основы индексации и превью ссылок. Скрипт читает каждую страницу так же, как поисковые роботы и боты превью в мессенджерах: в том виде, в каком её отдаёт сервер, **без выполнения JavaScript**. Метаданные, которые появляются только после загрузки скриптов в браузере, для него не существуют, как и для этих ботов.

| | |
|---|---|
| В плагине | `plugins/web-pipeline/templates/seo_check.py` |
| В проекте | `scripts/seo_check.py` (копию ставит [`init`](commands/init.md)) |
| Зависимости | Только стандартная библиотека Python 3 |
| Запускается | `make seo`; frontend-dev на задачах с публичными страницами; оркестратор и [design-critic](agents/design-critic.md) в [D4](delivery.md#d4-ограниченное-ревью); [`deploy`](commands/deploy.md) в smoke-тестах |
| Стандарт | [`seo-standards`](skills/seo-standards.md) |

Скрипту нужен запущенный сайт, поэтому в `make check` он не входит. Копия принадлежит проекту: её можно настраивать, и она работает в CI без Claude.

## Использование

```bash
python3 scripts/seo_check.py BASE_URL [--site-url URL] [--expect index|noindex] \
    [--path PATH ...] [--ignore RULE ...] [--max-pages N] [--strict] [--quiet]
```

| Флаг | Эффект |
|---|---|
| `BASE_URL` | Где сейчас работает сайт: `http://localhost:3000`, staging или production |
| `--site-url` | Публичный канонический адрес, например `https://example.com`. Если не задан, берётся из sitemap |
| `--expect index` | По умолчанию. Сайт должен индексироваться: production и локальная проверка публичного сайта |
| `--expect noindex` | Сайт не должен попадать в поиск: staging и закрытые приложения |
| `--path` | Дополнительная страница для проверки, можно повторять |
| `--ignore` | Пропустить правило, можно повторять |
| `--max-pages` | Сколько страниц проверять, по умолчанию 500 |
| `--strict` | Предупреждения считаются ошибками |
| `--quiet` | Печатать только ошибки |

Ошибки дают exit 1, предупреждения только печатаются. Формат строки: `url: [error|warn] rule: message`.

### Как сопоставляются адреса

Страницы берутся из sitemap, а sitemap находится через строку `Sitemap:` в robots.txt. В sitemap адреса публичные (`https://example.com/about/`), а сайт может работать локально. Поэтому каждый URL на публичном хосте запрашивается с `BASE_URL` по тому же пути. Так локальный прогон и прогон на staging проверяют те же страницы, что увидит поисковик в production.

### make seo

[`init`](commands/init.md) добавляет в `Makefile` цель:

```make
BASE_URL ?= http://localhost:3000
SITE_URL ?=
SEO_EXPECT ?= index
seo:
	python3 scripts/seo_check.py $(BASE_URL) --expect $(SEO_EXPECT) $(if $(SITE_URL),--site-url $(SITE_URL))
```

`BASE_URL` — адрес dev-сервера. `SITE_URL` и `SEO_EXPECT` (`noindex` для закрытого приложения) берутся из `docs/content.md`, когда он появится.

## Правила в режиме index

### Сайт

| Правило | Уровень | Что ловит |
|---|---|---|
| `robots-txt` | error | robots.txt не отдаётся |
| `robots-blocks-all` | error | `Disallow: /` для всех роботов |
| `robots-sitemap` | error | В robots.txt нет строки `Sitemap:` или адрес в ней не абсолютный |
| `sitemap-missing`, `sitemap-invalid` | error | Sitemap недоступен, не XML или корень не `<urlset>` и не `<sitemapindex>` |
| `sitemap-loc`, `sitemap-origin` | error | Адрес в sitemap не абсолютный или не на каноническом хосте |
| `sitemap-empty` | error | В sitemap нет страниц |
| `sitemap-lastmod` | warn | `lastmod` не в формате W3C |
| `sitemap-duplicate` | warn | Адрес указан дважды |
| `status-404` | error | Несуществующий адрес отвечает не 404 и не 410 («мягкий» 404) |
| `max-pages` | warn | Страниц больше `--max-pages`, проверены первые |

Sitemap index поддерживается: вложенные sitemap читаются, всего до 50 файлов.

### Каждая страница из sitemap

| Правило | Уровень | Что ловит |
|---|---|---|
| `page-unreachable`, `page-status`, `page-type` | error | Страница недоступна, отвечает не 200 или отдаёт не HTML |
| `page-redirect` | error | Страница редиректит: в sitemap должен быть конечный адрес |
| `noindex` | error | Страница в sitemap, но закрыта `noindex` (meta robots или `X-Robots-Tag`) |
| `html-lang`, `viewport` | error | Нет `lang` у `<html>` или `meta viewport` |
| `title` | error | Нет `<title>`, он пустой или их несколько. `<title>` внутри SVG не считается |
| `title-length` | warn | Title длиннее 60 символов |
| `description` | error | Нет meta description, или он пустой |
| `description-length` | warn | Description короче 50 или длиннее 160 символов |
| `canonical` | error | Нет canonical, их несколько, он не абсолютный, не на каноническом хосте или указывает не на эту страницу |
| `og-url` | warn | `og:url` не совпадает с canonical |
| `h1` | error / warn | Нет `<h1>` (error) или их несколько (warn) |
| `open-graph` | error | Нет одного из `og:title`, `og:description`, `og:type`, `og:url`, `og:image` |
| `og-image` | error | `og:image` не абсолютный, недоступен или не картинка |
| `og-image-size` | warn | Картинка не 1200×630 или с другим соотношением сторон (размер определяется для PNG и JPEG) |
| `og-image-weight` | warn | Картинка тяжелее 1 МБ |
| `twitter-card` | warn | Нет `twitter:card` |
| `hreflang` | error | Адрес в `hreflang` не абсолютный |
| `json-ld` | error / warn | JSON-LD не разбирается (error) или у элемента нет `@type` (warn) |
| `duplicate-title` | error | Одинаковый title на нескольких страницах |
| `duplicate-description` | warn | Одинаковый description на нескольких страницах |

## Правила в режиме noindex

Страницы берутся из sitemap, если он есть, иначе проверяются главная и `--path`.

| Правило | Уровень | Что ловит |
|---|---|---|
| `indexable` | error | Страница отвечает 200 без `noindex`: её может проиндексировать поисковик |
| `robots-hides-noindex` | warn | `noindex` есть, но robots.txt запрещает обход, поэтому робот его не увидит. Уберите `Disallow` |
| `page-unreachable` | error | Сайт недоступен |

Ответы 401 и 403 (сайт закрыт паролем), 404 и ошибки сервера считаются неиндексируемыми.

## Пропуск правил

Если правило не подходит проекту, его пропускают в цели `seo` с комментарием, почему:

```make
# Сайт без соцсетей: превью в X не нужно
seo:
	python3 scripts/seo_check.py $(BASE_URL) --ignore twitter-card
```

Константы `TITLE_MAX`, `DESCRIPTION_RANGE`, `OG_REQUIRED` и `OG_IMAGE_SIZE` в начале файла можно править. Изменения касаются только копии в проекте.
