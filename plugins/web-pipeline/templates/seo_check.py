#!/usr/bin/env python3
"""SEO checker: verifies the indexing and share-preview basics of a running site.

Owned by the project (copied from the web-pipeline plugin), stdlib only, safe for CI.

    python3 scripts/seo_check.py BASE_URL [--site-url URL] [--expect index|noindex]
                                 [--path PATH ...] [--ignore RULE ...] [--strict] [--quiet]

It reads every page as served, without running JavaScript, the way search and
share-preview bots do. Pages come from the sitemap (found through robots.txt), plus
any --path. URLs on the public origin (--site-url, or the sitemap's own origin) are
fetched from BASE_URL, so a local or staging run checks the same pages.

--expect index (default): robots.txt, sitemap, 404 status, and per page the title,
description, canonical, headings, Open Graph, Twitter card, hreflang and JSON-LD.
--expect noindex: every page must be kept out of search (staging, private apps).

Errors fail the run (exit 1). Warnings are printed for the reviewer to judge;
--strict turns them into errors. Skip a rule for this project with --ignore <rule>.
"""
from __future__ import annotations

import argparse
import json
import re
import struct
import sys
import urllib.error
import urllib.request
import uuid
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from html.parser import HTMLParser
from urllib.parse import urlsplit, urlunsplit

USER_AGENT = "seo_check/1.0 (web-pipeline)"
TIMEOUT = 15
MAX_BODY = 5 * 1024 * 1024
TITLE_MAX = 60
DESCRIPTION_RANGE = (50, 160)
OG_REQUIRED = ("og:title", "og:description", "og:type", "og:url", "og:image")
OG_IMAGE_SIZE = (1200, 630)
OG_IMAGE_MAX_BYTES = 1024 * 1024
SITEMAP_NS = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
NOINDEX = re.compile(r"\b(?:noindex|none)\b", re.I)
W3C_DATE = re.compile(r"^\d{4}(-\d{2}(-\d{2}(T\d{2}:\d{2}(:\d{2}(\.\d+)?)?(Z|[+-]\d{2}:\d{2}))?)?)?$")


@dataclass
class Response:
    url: str  # final URL after redirects
    status: int
    content_type: str = ""
    robots_tags: list[str] = field(default_factory=list)
    body: bytes = b""
    error: str = ""

    @property
    def text(self) -> str:
        return self.body.decode("utf-8", errors="replace")


def fetch(url: str) -> Response:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as resp:
            return Response(resp.geturl(), resp.status, resp.headers.get("Content-Type", ""),
                            resp.headers.get_all("X-Robots-Tag") or [], resp.read(MAX_BODY))
    except urllib.error.HTTPError as e:
        tags = e.headers.get_all("X-Robots-Tag") if e.headers else None
        return Response(e.geturl() or url, e.code, robots_tags=tags or [])
    except (urllib.error.URLError, OSError, ValueError) as e:
        return Response(url, 0, error=str(getattr(e, "reason", e)))


def origin(url: str) -> str:
    parts = urlsplit(url)
    return f"{parts.scheme}://{parts.netloc}".lower()


def is_absolute(url: str) -> bool:
    parts = urlsplit(url)
    return parts.scheme in ("http", "https") and bool(parts.netloc)


class Site:
    """Maps public URLs onto the base URL where the site actually runs."""

    def __init__(self, base: str, public: str | None) -> None:
        self.base = origin(base)
        self.public = origin(public) if public else None

    def local(self, url: str) -> str:
        if self.public and origin(url) == self.public:
            parts = urlsplit(url)
            return self.base + urlunsplit(("", "", parts.path or "/", parts.query, ""))
        return url


class Report:
    def __init__(self, strict: bool, quiet: bool, ignore: set[str], silent: bool = False) -> None:
        self.strict, self.quiet, self.ignore, self.silent = strict, quiet, ignore, silent
        self.errors = self.warnings = 0

    def add(self, where: str, level: str, rule: str, message: str) -> None:
        if self.silent or rule in self.ignore:
            return
        if level == "warn" and self.strict:
            level = "error"
        if level == "error":
            self.errors += 1
        else:
            self.warnings += 1
            if self.quiet:
                return
        print(f"{where}: [{level}] {rule}: {message}")


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.lang: str | None = None
        self.titles: list[str] = []
        self.meta: dict[str, list[str]] = {}
        self.links: list[dict[str, str]] = []
        self.h1 = 0
        self.json_ld: list[str] = []
        self._svg_depth = 0
        self._capture: str | None = None
        self._buf: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = {k.lower(): (v or "") for k, v in attrs}
        if tag == "html" and self.lang is None:
            self.lang = a.get("lang", "").strip()
        elif tag == "svg":
            self._svg_depth += 1
        elif tag == "title" and self._svg_depth == 0:
            self._capture, self._buf = "title", []
        elif tag == "meta":
            key = (a.get("name") or a.get("property") or "").lower()
            if key:
                self.meta.setdefault(key, []).append(a.get("content", "").strip())
        elif tag == "link":
            self.links.append(a)
        elif tag == "h1":
            self.h1 += 1
        elif tag == "script" and a.get("type", "").lower() == "application/ld+json":
            self._capture, self._buf = "json-ld", []

    def handle_endtag(self, tag: str) -> None:
        if tag == "svg" and self._svg_depth:
            self._svg_depth -= 1
        elif tag == "title" and self._capture == "title":
            self.titles.append(" ".join("".join(self._buf).split()))
            self._capture = None
        elif tag == "script" and self._capture == "json-ld":
            self.json_ld.append("".join(self._buf))
            self._capture = None

    def handle_data(self, data: str) -> None:
        if self._capture:
            self._buf.append(data)

    def first(self, key: str) -> str:
        values = self.meta.get(key) or [""]
        return values[0]

    def link_hrefs(self, rel: str) -> list[dict[str, str]]:
        return [link for link in self.links if rel in link.get("rel", "").lower().split()]


def parse_robots(text: str) -> tuple[list[tuple[list[str], list[tuple[str, str]]]], list[str]]:
    groups: list[tuple[list[str], list[tuple[str, str]]]] = []
    sitemaps: list[str] = []
    after_agent = False
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].strip()
        if ":" not in line:
            continue
        key, value = (part.strip() for part in line.split(":", 1))
        key = key.lower()
        if key == "user-agent":
            if not after_agent:
                groups.append(([], []))
            groups[-1][0].append(value.lower())
            after_agent = True
            continue
        after_agent = False
        if key == "sitemap":
            sitemaps.append(value)
        elif key in ("allow", "disallow") and groups:
            groups[-1][1].append((key, value))
    return groups, sitemaps


def blocks_everything(groups: list[tuple[list[str], list[tuple[str, str]]]]) -> bool:
    for agents, rules in groups:
        if "*" in agents:
            disallow_root = any(k == "disallow" and v in ("/", "/*") for k, v in rules)
            allow_root = any(k == "allow" and v in ("/", "/*") for k, v in rules)
            return disallow_root and not allow_root
    return False


def read_sitemaps(urls: list[str], site: Site, report: Report, required: bool) -> list[str]:
    locs: list[str] = []
    queue, seen = list(urls), set()
    while queue and len(seen) < 50:
        url = queue.pop(0)
        if url in seen:
            continue
        seen.add(url)
        resp = fetch(site.local(url))
        if resp.status != 200:
            if required:
                report.add(url, "error", "sitemap-missing",
                           f"sitemap not reachable ({resp.error or f'HTTP {resp.status}'})")
            continue
        try:
            root = ET.fromstring(resp.body)
        except ET.ParseError as e:
            report.add(url, "error", "sitemap-invalid", f"not valid XML: {e}")
            continue
        if root.tag == f"{SITEMAP_NS}sitemapindex":
            queue += [(el.text or "").strip() for el in root.iter(f"{SITEMAP_NS}loc")]
            continue
        if root.tag != f"{SITEMAP_NS}urlset":
            report.add(url, "error", "sitemap-invalid", "root element is not <urlset> or <sitemapindex>")
            continue
        for entry in root.iter(f"{SITEMAP_NS}url"):
            loc = (entry.findtext(f"{SITEMAP_NS}loc") or "").strip()
            lastmod = (entry.findtext(f"{SITEMAP_NS}lastmod") or "").strip()
            if not is_absolute(loc):
                report.add(url, "error", "sitemap-loc", f"<loc> is not an absolute URL: {loc!r}")
                continue
            if lastmod and not W3C_DATE.match(lastmod):
                report.add(loc, "warn", "sitemap-lastmod", f"<lastmod> is not a W3C date: {lastmod!r}")
            if loc in locs:
                report.add(loc, "warn", "sitemap-duplicate", "listed more than once")
                continue
            locs.append(loc)
    return locs


def image_size(data: bytes) -> tuple[int, int] | None:
    if data[:8] == b"\x89PNG\r\n\x1a\n" and len(data) >= 24:
        width, height = struct.unpack(">II", data[16:24])
        return width, height
    if data[:2] == b"\xff\xd8":
        i = 2
        while i + 9 < len(data):
            if data[i] != 0xFF:
                i += 1
                continue
            marker = data[i + 1]
            if marker in (0xD8, 0x01, 0xFF) or 0xD0 <= marker <= 0xD7:
                i += 1 if marker == 0xFF else 2
                continue
            (length,) = struct.unpack(">H", data[i + 2:i + 4])
            if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
                height, width = struct.unpack(">HH", data[i + 5:i + 9])
                return width, height
            i += 2 + length
    return None


def check_og_image(url: str, where: str, site: Site, report: Report, cache: dict[str, bool]) -> None:
    if url in cache:
        return
    cache[url] = True
    if not is_absolute(url):
        report.add(where, "error", "og-image", f"og:image must be an absolute URL: {url!r}")
        return
    resp = fetch(site.local(url))
    if resp.status != 200 or not resp.content_type.startswith("image/"):
        report.add(where, "error", "og-image",
                   f"og:image {url} is not an image ({resp.error or f'HTTP {resp.status}, {resp.content_type}'})")
        return
    if len(resp.body) > OG_IMAGE_MAX_BYTES:
        report.add(where, "warn", "og-image-weight",
                   f"og:image is {len(resp.body) // 1024} KB; some messengers skip previews over ~1 MB")
    size = image_size(resp.body)
    if size:
        width, height = size
        target_w, target_h = OG_IMAGE_SIZE
        if width < target_w or height < target_h or abs(width / height - target_w / target_h) > 0.1:
            report.add(where, "warn", "og-image-size",
                       f"og:image is {width}x{height}; use {target_w}x{target_h} for large previews")


def has_noindex(resp: Response, page: PageParser | None) -> bool:
    values = list(resp.robots_tags)
    if page:
        values += page.meta.get("robots", []) + page.meta.get("googlebot", [])
    return any(NOINDEX.search(v) for v in values)


def check_page(url: str, site: Site, report: Report, seen: dict[str, dict[str, list[str]]],
               images: dict[str, bool]) -> None:
    target = site.local(url)
    resp = fetch(target)
    if resp.status == 0:
        report.add(url, "error", "page-unreachable", resp.error)
        return
    if resp.status != 200:
        report.add(url, "error", "page-status", f"HTTP {resp.status}; the sitemap must list only 200 pages")
        return
    if resp.url != target:
        report.add(url, "error", "page-redirect", f"redirects to {resp.url}; list the final URL instead")
    if "html" not in resp.content_type:
        report.add(url, "error", "page-type", f"content type is {resp.content_type!r}, not HTML")
        return

    page = PageParser()
    page.feed(resp.text)

    if has_noindex(resp, page):
        report.add(url, "error", "noindex", "page is noindex but listed for indexing")
    if not page.lang:
        report.add(url, "error", "html-lang", "<html> has no lang attribute")
    if "viewport" not in page.meta:
        report.add(url, "error", "viewport", "no <meta name=\"viewport\">")

    title = page.titles[0] if page.titles else ""
    if not title:
        report.add(url, "error", "title", "no <title>, or it is empty")
    else:
        if len(page.titles) > 1:
            report.add(url, "error", "title", f"{len(page.titles)} <title> elements; keep one")
        if len(title) > TITLE_MAX:
            report.add(url, "warn", "title-length", f"title is {len(title)} characters; about {TITLE_MAX} show")
        seen["title"].setdefault(title, []).append(url)

    description = page.first("description")
    if not description:
        report.add(url, "error", "description", "no meta description, or it is empty")
    else:
        low, high = DESCRIPTION_RANGE
        if not low <= len(description) <= high:
            report.add(url, "warn", "description-length",
                       f"description is {len(description)} characters; aim for {low}-{high}")
        seen["description"].setdefault(description, []).append(url)

    canonicals = page.link_hrefs("canonical")
    if not canonicals:
        report.add(url, "error", "canonical", "no <link rel=\"canonical\">")
    else:
        canonical = canonicals[0].get("href", "").strip()
        if len(canonicals) > 1:
            report.add(url, "error", "canonical", f"{len(canonicals)} canonical links; keep one")
        if not is_absolute(canonical):
            report.add(url, "error", "canonical", f"canonical must be absolute: {canonical!r}")
        elif site.public and origin(canonical) != site.public:
            report.add(url, "error", "canonical", f"canonical {canonical} is not on {site.public}")
        elif canonical != url:
            report.add(url, "error", "canonical",
                       f"canonical is {canonical}; the sitemap must list canonical URLs only")
        og_url = page.first("og:url")
        if og_url and canonical and og_url != canonical:
            report.add(url, "warn", "og-url", f"og:url {og_url} differs from the canonical {canonical}")

    if page.h1 == 0:
        report.add(url, "error", "h1", "no <h1>")
    elif page.h1 > 1:
        report.add(url, "warn", "h1", f"{page.h1} <h1> elements; one states the key message")

    missing = [key for key in OG_REQUIRED if not page.first(key)]
    if missing:
        report.add(url, "error", "open-graph", f"missing {', '.join(missing)}")
    if page.first("og:image"):
        check_og_image(page.first("og:image"), url, site, report, images)
    if not page.first("twitter:card"):
        report.add(url, "warn", "twitter-card", "no twitter:card; use summary_large_image")

    for link in page.link_hrefs("alternate"):
        if link.get("hreflang") and not is_absolute(link.get("href", "")):
            report.add(url, "error", "hreflang", f"hreflang {link['hreflang']} href must be absolute")

    for block in page.json_ld:
        try:
            data = json.loads(block)
        except json.JSONDecodeError as e:
            report.add(url, "error", "json-ld", f"invalid JSON-LD: {e}")
            continue
        items = data if isinstance(data, list) else [data]
        if not all(isinstance(i, dict) and ("@type" in i or "@graph" in i) for i in items):
            report.add(url, "warn", "json-ld", "JSON-LD item without @type")


def page_list(locs: list[str], site: Site, paths: list[str], limit: int, report: Report) -> list[str]:
    public = site.public or site.base
    pages = locs + [public + "/" + p.lstrip("/") for p in paths]
    pages = list(dict.fromkeys(pages))
    if len(pages) > limit:
        report.add(public, "warn", "max-pages", f"{len(pages)} pages; checked the first {limit}")
    return pages[:limit]


def check_index(site: Site, args: argparse.Namespace, report: Report) -> int:
    robots = fetch(site.base + "/robots.txt")
    sitemap_urls: list[str] = []
    if robots.status != 200:
        report.add(site.base + "/robots.txt", "error", "robots-txt",
                   f"robots.txt not served ({robots.error or f'HTTP {robots.status}'})")
    else:
        groups, sitemap_urls = parse_robots(robots.text)
        if blocks_everything(groups):
            report.add(site.base + "/robots.txt", "error", "robots-blocks-all",
                       "Disallow: / for every crawler; this environment is expected to be indexed")
        if not sitemap_urls:
            report.add(site.base + "/robots.txt", "error", "robots-sitemap", "no Sitemap: line")
        for url in sitemap_urls:
            if not is_absolute(url):
                report.add(site.base + "/robots.txt", "error", "robots-sitemap",
                           f"Sitemap: must be an absolute URL: {url!r}")
        sitemap_urls = [u for u in sitemap_urls if is_absolute(u)]
    if site.public is None:
        site.public = origin(sitemap_urls[0]) if sitemap_urls else site.base
    if not sitemap_urls:
        sitemap_urls = [site.public + "/sitemap.xml"]

    locs = read_sitemaps(sitemap_urls, site, report, required=True)
    for loc in locs:
        if origin(loc) != site.public:
            report.add(loc, "error", "sitemap-origin", f"sitemap URL is not on {site.public}")
    locs = [loc for loc in locs if origin(loc) == site.public]
    if not locs and not args.path:
        report.add(sitemap_urls[0], "error", "sitemap-empty", "the sitemap lists no pages")

    missing = fetch(f"{site.base}/seo-check-{uuid.uuid4().hex[:12]}")
    if missing.status not in (404, 410):
        report.add(site.base, "error", "status-404",
                   f"a missing URL returns {missing.error or f'HTTP {missing.status}'}; serve a real 404")

    pages = page_list(locs, site, args.path, args.max_pages, report)
    seen: dict[str, dict[str, list[str]]] = {"title": {}, "description": {}}
    images: dict[str, bool] = {}
    for url in pages:
        check_page(url, site, report, seen, images)
    for key, level in (("title", "error"), ("description", "warn")):
        for value, urls in seen[key].items():
            if len(urls) > 1:
                report.add(urls[0], level, f"duplicate-{key}",
                           f"same {key} on {len(urls)} pages: {', '.join(urls[1:4])}")
    return len(pages)


def check_noindex(site: Site, args: argparse.Namespace, report: Report) -> int:
    robots = fetch(site.base + "/robots.txt")
    blocked = False
    sitemap_urls: list[str] = []
    if robots.status == 200:
        groups, sitemap_urls = parse_robots(robots.text)
        blocked = blocks_everything(groups)
    sitemap_urls = [u for u in sitemap_urls if is_absolute(u)]
    if site.public is None:
        site.public = origin(sitemap_urls[0]) if sitemap_urls else site.base
    silent = Report(False, True, set(), silent=True)  # sitemap quality is the index run's job
    locs = read_sitemaps(sitemap_urls or [site.public + "/sitemap.xml"], site, silent, required=False)
    locs = [loc for loc in locs if origin(loc) == site.public]
    pages = page_list(locs or [site.public + "/"], site, args.path, args.max_pages, report)

    for url in pages:
        resp = fetch(site.local(url))
        if resp.status == 0:
            report.add(url, "error", "page-unreachable", resp.error)
            continue
        if resp.status != 200:
            continue  # auth walls, 404s and errors are not indexed
        page = None
        if "html" in resp.content_type:
            page = PageParser()
            page.feed(resp.text)
        if not has_noindex(resp, page):
            report.add(url, "error", "indexable",
                       "no noindex; send X-Robots-Tag: noindex from the proxy, or protect it with auth")
        elif blocked:
            report.add(url, "warn", "robots-hides-noindex",
                       "robots.txt blocks crawling, so crawlers never see the noindex; drop the Disallow")
    return len(pages)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("base_url", help="where the site runs, e.g. http://localhost:3000")
    parser.add_argument("--site-url", help="the public canonical origin, e.g. https://example.com")
    parser.add_argument("--expect", choices=("index", "noindex"), default="index")
    parser.add_argument("--path", action="append", default=[], help="extra page to check (repeatable)")
    parser.add_argument("--ignore", action="append", default=[], help="rule to skip (repeatable)")
    parser.add_argument("--max-pages", type=int, default=500)
    parser.add_argument("--strict", action="store_true", help="treat warnings as errors")
    parser.add_argument("--quiet", action="store_true", help="print errors only")
    args = parser.parse_args()

    if not is_absolute(args.base_url):
        parser.error("BASE_URL must be an absolute http(s) URL")
    report = Report(args.strict, args.quiet, set(args.ignore))
    site = Site(args.base_url, args.site_url)
    check = check_index if args.expect == "index" else check_noindex
    pages = check(site, args, report)

    sys.stdout.flush()
    print(f"seo-check ({args.expect}): {report.errors} error(s), {report.warnings} warning(s) "
          f"on {pages} page(s)", file=sys.stderr)
    if report.errors:
        print("The checker reads HTML as served, without JavaScript, like share-preview bots. "
              "Metadata added only on the client does not count.", file=sys.stderr)
    return 1 if report.errors else 0


if __name__ == "__main__":
    sys.exit(main())
