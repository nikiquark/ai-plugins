# seo-standards

Стандарты технического SEO и превью ссылок. Поисковики и превью в мессенджерах читают HTML, который отдаёт сервер. Что говорит каждая страница и какие у неё метаданные, решает `docs/content.md`. Этот навык решает, **как** это доставить.

| | |
|---|---|
| Вызов | `/web-pipeline:seo-standards` или автоматически для плана контента, архитектуры публичных страниц и фронтенда публичных страниц |
| Предзагружен в | [content-strategist](../agents/content-strategist.md), [architect](../agents/architect.md), [frontend-dev](../agents/frontend-dev.md), [design-critic](../agents/design-critic.md) |
| Контроль | [`scripts/seo_check.py`](../seo-check.md) через `make seo` |
| Исходник | `plugins/web-pipeline/skills/seo-standards/SKILL.md` |

## Когда срабатывает

> Technical SEO and share-preview standards for this user's web projects - server-rendered public pages, per-page title/description/canonical/Open Graph/Twitter/JSON-LD, robots.txt (all crawlers allowed by default), sitemap.xml, hreflang, redirects, staging noindex, Core Web Vitals - and the seo_check.py gate. Load for content planning, the architecture of public pages, and any frontend work on public pages.

## Отрисовка

- Публичные страницы рендерятся на сервере или при сборке (SSG, SSR, ISR). Title, meta-теги, canonical, Open Graph, JSON-LD и основной текст должны быть в первом HTML-ответе. Боты превью в мессенджерах и соцсетях не выполняют JavaScript, а поисковики выполняют его поздно и не всегда.
- SPA, которое рисуется только в браузере, допустимо за логином, но не для публичных страниц.
- Каждый маршрут отдаёт правильный статус: 200 для страницы, 301 для переехавшей, 404 для несуществующей (настоящий статус 404, а не страница с кодом 200 и надписью «не найдено»), 410 для удалённой навсегда.

## Каждая публичная страница

Значения берутся из `docs/content.md` и хранятся в одном типизированном месте на страницу, а не строками по компонентам.

| Элемент | Правило |
|---|---|
| `<html lang>`, `charset`, `viewport` | Обязательны |
| `<title>` | Уникальный и конкретный. Ключевое сообщение страницы словами, которые ищут люди. Около 60 символов до обрезки, бренд в конце (`Страница — Бренд`). Без перечня ключевых слов |
| `meta description` | Уникальный пересказ этой страницы. Жёсткого лимита нет, видно около 150 символов. Google может переписать его, но хороший description остаётся вариантом по умолчанию |
| `canonical` | Абсолютный, на каноническом хосте, на саму страницу. URL с метками и сортировкой указывают на чистый URL |
| `<h1>` | Ровно один, несёт ключевое сообщение. Заголовки идут по порядку без пропуска уровней |
| Open Graph | `og:title`, `og:description`, `og:type`, `og:url` (равен canonical), `og:image`, `og:image:alt`, `og:site_name`, `og:locale` |
| `og:image` | Абсолютный HTTPS, 1200×630, PNG или JPEG, до 1 МБ, текст не у краёв: некоторые приложения их обрезают |
| Twitter/X | `twitter:card` = `summary_large_image`, остальное берётся из Open Graph |
| JSON-LD | По `docs/content.md`: `Organization` и `WebSite` на главной, `BreadcrumbList` на вложенных, плюс тип страницы (`Article`, `Product`, `FAQPage`, `Event`, `LocalBusiness`…). Размечается только то, что видно на странице. Перед релизом — проверка в Google Rich Results Test |
| Изображения | Осмысленный `alt`, явные ширина и высота, картинка первого экрана без lazy-load |
| Ссылки | Настоящие `<a href>` с понятным текстом, навигация работает без JavaScript |

## OG-картинки

Шаблон в выбранном стиле делает [designer](../agents/designer.md): `docs/design/og-template.html`. Из него получается одна статичная картинка на тип страницы, или картинки генерируются для каждой страницы при сборке средствами фреймворка (`next/og`, satori, эндпоинт Astro). Скриншот hero — это не OG-картинка.

## Сайт целиком

- **Один канонический хост.** http → https и www → без www (или наоборот) через 301. Одна политика слэша в конце URL, закреплённая редиректом.
- **robots.txt** в production, его генерирует приложение или отдаёт прокси:
    ```text
    User-agent: *
    Allow: /

    Sitemap: https://example.com/sitemap.xml
    ```
    - По умолчанию пускаются **все** роботы, включая AI-ботов. `Disallow` добавляется только для закрытых разделов (`/admin`, `/api`), если так сказано в `docs/content.md`.
    - robots.txt управляет обходом, а не индексацией. Чтобы убрать страницу из поиска, нужен `noindex`. Блокировать такую страницу в robots.txt нельзя: тогда робот не увидит `noindex`.
    - `llms.txt` не делается, если вы не попросили.
- **sitemap.xml:**
    - только канонические индексируемые URL, которые отвечают 200, абсолютные и на каноническом хосте;
    - генерируется из маршрутов и контента, а не вручную;
    - `lastmod` только настоящий, то есть дата последнего изменения контента, а не «сейчас» при каждой сборке. `priority` и `changefreq` не пишутся: Google их игнорирует;
    - больше 50 000 URL или 50 МБ — разбить через sitemap index.
- **Многоязычные сайты:** отдельный URL на локаль (`/en/…`) и `hreflang` на все локали, включая саму страницу и `x-default`.
- **Страницы за логином** и служебные (поиск, корзина, «спасибо»): `noindex`, не в sitemap.
- **Staging и превью-окружения:** `X-Robots-Tag: noindex, nofollow` на каждом ответе. Его ставит роль прокси, переключатель задаётся в inventory ([`ansible-conventions`](ansible-conventions.md)). Другой вариант — HTTP basic auth. В production этого заголовка не бывает.
- **Переехавшие URL:** 301 на новый адрес, обновлённые внутренние ссылки и sitemap, строка в таблице редиректов `docs/content.md`.
- **Иконки:** `favicon.ico`, SVG-иконка, `apple-touch-icon` 180×180 и web manifest с названием сайта.

## Сначала готовое

Сначала используются средства самого фреймворка:

| Фреймворк | Средства |
|---|---|
| Next.js | `metadata` и `generateMetadata`, `app/robots.ts`, `app/sitemap.ts`, `opengraph-image` |
| Astro | `@astrojs/sitemap`, общий head в layout |
| Nuxt | `useSeoMeta`, `@nuxtjs/sitemap` |
| SvelteKit | `<svelte:head>`, эндпоинт `sitemap.xml` |
| Django | `django.contrib.sitemaps` |

## Производительность

Core Web Vitals для 75-го процентиля на мобильных: LCP ≤ 2,5 с, INP ≤ 200 мс, CLS ≤ 0,1. LCP-картинка и дисплейный шрифт загружаются заранее через preload, `font-display: swap` с подобранным по метрикам fallback, поздние баннеры не сдвигают раскладку.

## Проверка

[`seo_check.py`](../seo-check.md) читает запущенный сайт так же, как роботы, без JavaScript. Его ошибки нужно исправлять, предупреждения оценивает [design-critic](../agents/design-critic.md).
