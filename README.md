# Corporate insurance agency — design demo

A four-page information site for an insurance agency: Home, About Us, Our Team, Contact.

**Everything on this site is placeholder content.** The company name, people, figures,
address and telephone number are invented for layout purposes and do not describe a
real business.

Live preview: https://anirudhatalmale6-alt.github.io/corporate-insurance-demo/

## What it demonstrates

- Corporate/financial-services visual language: restrained navy + brass, serif display
  headings, generous whitespace, no decorative noise.
- Fully responsive — desktop, tablet and phone, with a real mobile nav.
- Accessibility: skip link, visible focus rings, labelled form fields with inline
  errors, correct heading order, AA contrast.
- On-page SEO: unique title and meta description per page, canonical, Open Graph.
- Performance: no web fonts, no frameworks, no images to download — the hero and the
  team portraits are inline SVG. One 13 KB stylesheet, one 2 KB script.

## Lighthouse (lighthouse 12, headless Chromium)

| Page     | Performance | Accessibility | Best practices | SEO |
|----------|-------------|---------------|----------------|-----|
| Home     | 100 | 100 | 100 | 100 |
| About Us | 100 | 100 | 100 | 100 |
| Our Team | 100 | 100 | 100 | 100 |
| Contact  | 100 | 100 | 100 | 100 |

Measured on the indexable build. The published demo carries `noindex` and a
`Disallow: /` robots.txt on purpose, so Lighthouse's SEO category reports 66 against
this URL — that single `is-crawlable` audit is deliberate and is removed on the real
site.

## Build

```
python3 tools/build_site.py     # renders dist/ from the content dict in that file
python3 tools/shots.py          # viewport screenshots, requires a local server on :8741
```

Content lives in the dicts at the top of `tools/build_site.py`; `src/site.css` and
`src/site.js` are copied into `dist/assets/`. On the real project this layer is
replaced by a CMS so the client edits text and images in a browser.
