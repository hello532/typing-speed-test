#!/usr/bin/env python3
"""一次性派生器：从 index.html 机械生成 src/template.html。

不手写模板 —— 把可变区替换成 {{占位符}}，其余逐字节保留。
这样 build.py 重建时天然与原始产物字节等价，避免手抄引入偏差。
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SC = "<" + "script"
ESC = "<" + "/script" + ">"


def sub1(text, pat, repl, label):
    new, n = re.subn(pat, lambda m: repl, text, count=1, flags=re.S)
    if n != 1:
        sys.exit(f"FAILED {label}: {n} matches for {pat[:60]}")
    return new


def main():
    t = (ROOT / "index.html").read_text(encoding="utf-8")

    # 恒定资源
    t = sub1(t, r"<style>\n.*?\n</style>", "<style>\n{{CSS}}\n</style>", "css")
    t = sub1(t, SC + r">try\{var _t=localStorage.*?" + ESC,
             SC + ">{{HEAD_SNIPPET}}" + ESC, "head-snippet")
    t = sub1(t, SC + r">\n\(function\(\)\{\n[^\n]*use strict[^\n]*\nvar SENTENCES=\[.*?" + ESC,
             SC + ">\n{{ENGINE}}\n" + ESC, "engine")
    t = sub1(t, r"<footer>.*?</footer>", "{{FOOTER}}", "footer")

    # head 可变字段
    t = sub1(t, r"<title>.*?</title>", "<title>{{TITLE}}</title>", "title")
    t = sub1(t, r'<meta name="description" content=".*?">',
             '<meta name="description" content="{{META_DESC}}">', "metaDesc")
    t = sub1(t, r'<meta name="keywords" content=".*?">',
             '<meta name="keywords" content="{{KEYWORDS}}">', "keywords")
    t = sub1(t, r'<link rel="canonical" href=".*?">',
             '<link rel="canonical" href="{{CANONICAL}}">', "canonical")
    t = sub1(t, r'<meta property="og:title" content=".*?">',
             '<meta property="og:title" content="{{OG_TITLE}}">', "ogTitle")
    t = sub1(t, r'<meta property="og:description" content=".*?">',
             '<meta property="og:description" content="{{OG_DESC}}">', "ogDesc")
    t = sub1(t, r'<meta property="og:url" content=".*?">',
             '<meta property="og:url" content="{{OG_URL}}">', "ogUrl")
    t = sub1(t, r'<meta name="twitter:title" content=".*?">',
             '<meta name="twitter:title" content="{{TW_TITLE}}">', "twTitle")
    t = sub1(t, r'<meta name="twitter:description" content=".*?">',
             '<meta name="twitter:description" content="{{TW_DESC}}">', "twDesc")

    # JSON-LD 三块
    ld = re.findall(SC + r' type="application/ld\+json">\s*\{.*?\}\s*' + ESC, t, re.S)
    if len(ld) != 3:
        sys.exit(f"expected 3 JSON-LD blocks, got {len(ld)}")
    for i, block in enumerate(ld):
        ph = ["{{LD_WEBAPP}}", "{{LD_FAQ}}", "{{LD_BREADCRUMB}}"][i]
        t = t.replace(block, ph, 1)

    # body 可变区
    t = sub1(t, r'<header class="top">.*?</header>', "{{HEADER}}", "header")
    m = re.search(r"\n\n  <nav class=\"crumbs\".*?</nav>", t, re.S)
    if m:
        sys.exit("index.html unexpectedly has crumbs")
    t = sub1(t, r'\{\{HEADER\}\}\n\n  <section class="hero">',
             "{{HEADER}}\n{{CRUMBS}}\n  <section class=\"hero\">", "crumbs-slot")
    t = sub1(t, r"<h1>.*?</h1>", "<h1>{{H1}}</h1>", "h1")
    t = sub1(t, r"<h1>\{\{H1\}\}</h1>\n    <p>.*?</p>", "<h1>{{H1}}</h1>\n    <p>{{HERO_P}}</p>", "heroP")
    t = sub1(t, r'<section class="seo">\s*.*?</section>', "{{SEO}}", "seo")
    t = sub1(t, r'<section class="seo faq">.*?</section>', "{{FAQ}}", "faq")
    t = sub1(t, r'<div class="panel result".*?\n  </div>', "{{RESULT}}", "result")

    # 面板 dur/mode 派生位
    for dur, lab in [("15", "15s"), ("30", "30s"), ("60", "1 min"), ("120", "2 min"),
                     ("180", "3 min"), ("300", "5 min"), ("600", "10 min")]:
        t = sub1(t, r'<button class="chip dur[^"]*" data-d="%s">%s</button>' % (dur, lab),
                 "{{CHIP_DUR_%s}}" % dur, "chip" + dur)
    for mode, lab in [("sentences", "Sentences"), ("quotes", "Quotes"),
                      ("numbers", "Numbers"), ("words", "Words")]:
        t = sub1(t, r'<button class="chip mode[^"]*" data-m="%s"[^>]*>%s</button>' % (mode, lab),
                 "{{CHIP_MODE_%s}}" % mode.upper(), "chip" + mode)
    t = sub1(t, r'<div class="num accent" id="sTime">.*?</div>',
             '<div class="num accent" id="sTime">{{STIME}}</div>', "sTime")

    # 引擎 dur/mode 初值由 build.py 在注入 engine.js 时替换（基线保留 dur=60/mode=sentences）

    out = ROOT / "src" / "template.html"
    out.write_text(t, encoding="utf-8")
    ph = sorted(set(re.findall(r"\{\{[A-Z0-9_]+\}\}", t)))
    print(f"wrote {out.relative_to(ROOT)} — {len(t):,} bytes, {len(ph)} placeholders")
    for x in ph:
        print("  ", x)


if __name__ == "__main__":
    main()
