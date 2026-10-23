# <Project name>: Content

_Status: draft | approved · Date: YYYY-MM-DD_

## 1. Message
- **Core message**: one sentence a visitor could repeat to a friend.
- **For whom**: the persona from the spec, in a few words.
- **Primary action**: the one thing a visitor should do.
- **Proof**: facts that make the message believable, each with its source in the spec.
- **Voice**: three rules, each with a do and a don't.

## 2. Page map
| URL | Purpose | Query / intent | Index | Sitemap |
|---|---|---|---|---|

## 3. Pages

### `/`: <page name>
- **Key message**: one sentence.
- **Primary action**: … · **Secondary**: … (optional)
- **Emphasis**: the one element that gets visual weight, and why.

Sections, in priority order:
1. <section>: the question it answers.

**Cut**: what was considered and left out, and why.

Copy:
| Element | Text | Note |
|---|---|---|
| H1 | | |
| Subhead | | |
| Primary CTA | | |

Metadata:
| Field | Value |
|---|---|
| title | |
| description | |
| canonical | |
| og:type | |
| og:image | what it shows |
| JSON-LD | type and fields |

## 4. Interface copy
Navigation, footer, form errors, empty states, confirmations and the 404 page.

## 5. Site
- **Canonical host**: https://… · www or not · trailing-slash policy
- **Locales**: … · hreflang: …
- **robots.txt (production)**: all crawlers allowed, AI crawlers included, unless stated otherwise here. `Sitemap:` line.
- **Staging**: `X-Robots-Tag: noindex, nofollow` on every response.
- **Sitemap**: which pages, and where `lastmod` comes from.

Redirects (301):
| Old URL | New URL | Why |
|---|---|---|

## 6. Open questions
Anything left undecided, including claims that need proof before they can be used.
