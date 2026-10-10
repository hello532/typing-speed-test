# Typing.Rerivo

**A free online typing test — 41 landing pages, no signup, no ads.**

🔗 Live: **<https://typing.rerivo.com>**

![cover](og-cover.png)

Instant WPM and accuracy, runs entirely in your browser, and your results are
saved locally. Built as a multilingual typing-practice playground.

## Why

Most typing tests force you to sign up, shove ads into the practice area, or
only offer a single 1-minute round. Typing.Rerivo is the opposite: open the
page, pick a duration, start typing.

## Features

- **41 landing pages** covering the full duration ladder, practice variants, an
  education line, a games line, and five languages
  ([30 second](https://typing.rerivo.com/30-second-typing-test.html) ·
  [1 minute](https://typing.rerivo.com/1-minute-typing-test.html) ·
  [3 minute](https://typing.rerivo.com/3-minute-typing-test.html) ·
  [5 minute](https://typing.rerivo.com/5-minute-typing-test.html) ·
  [10 minute](https://typing.rerivo.com/10-minute-typing-test.html) ·
  [numbers](https://typing.rerivo.com/number-typing-test.html) ·
  [punctuation](https://typing.rerivo.com/punctuation-typing-test.html) ·
  [typing games](https://typing.rerivo.com/typing-games.html) ·
  [typing lessons](https://typing.rerivo.com/typing-lessons.html) ·
  [typing tutorial](https://typing.rerivo.com/typing-tutorial.html) ·
  [typing tutor](https://typing.rerivo.com/typing-tutor.html) ·
  [learn to type](https://typing.rerivo.com/learn-to-type.html) ·
  [typing trainer](https://typing.rerivo.com/typing-trainer.html) ·
  [touch typing](https://typing.rerivo.com/touch-typing-test.html) ·
  [typing race](https://typing.rerivo.com/typing-race.html) ·
  [spanish](https://typing.rerivo.com/spanish-typing-test.html) ·
  [chinese](https://typing.rerivo.com/chinese-typing-test.html) ·
  [hindi](https://typing.rerivo.com/hindi-typing-test.html) ·
  [arabic](https://typing.rerivo.com/arabic-typing-test.html) …)
- **Differentiated features**: a [printable typing certificate](https://typing.rerivo.com/typing-certificate.html),
  a [Dvorak typing test](https://typing.rerivo.com/dvorak-typing.html) with an on-screen Dvorak keyboard,
  and [one hand typing](https://typing.rerivo.com/one-hand-typing.html) practice
- **Timed rounds from 15s to 10min** with 4 text modes: sentences, quotes, numbers, words
- **Instant WPM + accuracy**, results stored in `localStorage`, unlimited retakes
- **Multilingual practice pools** — English, Chinese, Spanish, Hindi, Arabic
- **Installable PWA** (works offline once loaded)
- **Zero backend** — 100% static, no account, no tracking, no ads

## How it's built

One template + one config table generate the whole site — every page is a
build artifact, never hand-edited.

- **Vanilla JS + HTML/CSS**, no framework, no build toolchain beyond Python
- `src/template.html` + `src/pages.json` → `build.py` renders all 34 pages
- **SEO built-in**: JSON-LD (`WebApplication` / `FAQPage` / `BreadcrumbList`)
  on every page, plus `sitemap.xml`, `robots.txt`, `llms.txt`
- **Regression guard**: `verify.py` (14/14 structural checks) + an engine
  behavior harness keep the generated pages honest

## Local development

```bash
python3 build.py      # render all pages from src/
python3 verify.py     # run the 14/14 regression checks
python3 -m http.server 8000   # then open http://localhost:8000
```

Requires only Python 3 (the static generator). No `npm install`.

## Deploy

```bash
git push origin main   # → GitHub Pages (CNAME: typing.rerivo.com)
```

Pushing to `main` auto-deploys. Don't hand-edit files in the repo root —
change `src/`, re-run `build.py`, then commit the regenerated pages.

## Repo layout

```
src/            template, pages.json, engine.js, ui.js, footer.html, style.css
src/pools/      practice content (en / zh / es / hi / ar)
src/tools/      generator & extraction helpers
*.html          generated pages (build artifacts)
og-cover.png    social preview image
```

## Links

- Live site — <https://typing.rerivo.com>
- 30-second quick test — <https://typing.rerivo.com/30-second-typing-test.html>
- Typing lessons — <https://typing.rerivo.com/typing-lessons.html>
- Typing games — <https://typing.rerivo.com/typing-games.html>
- Learn to type — <https://typing.rerivo.com/learn-to-type.html>
- Practice — <https://typing.rerivo.com/typing-practice.html>

---

Feedback and PRs welcome.
