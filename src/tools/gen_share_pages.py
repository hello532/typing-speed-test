#!/usr/bin/env python3
"""生成 6 个静态成绩分享页（OG meta 逐页硬编码，爬虫零 JS 依赖）。
设计：静态 OG 给爬虫；正文用 ?s=&a= 参数 JS 渲染精确分数给人类。
产物不进 sitemap（noindex,follow），canonical 自指。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITE = "https://typing.rerivo.com"

TIERS = {
 "elite":   {"badge": "ELITE · TOP 1%", "title": "I scored in the top 1% (Elite) on this typing speed test — can you beat me?",
             "desc": "100+ WPM with elite accuracy on a free 60-second typing speed test. Can you beat my score?"},
 "fast":    {"badge": "FAST · TOP 10%", "title": "I scored in the top 10% on this typing speed test — can you beat me?",
             "desc": "80-99 WPM on a free 60-second typing speed test. Can you beat my score?"},
 "good":    {"badge": "GOOD · OFFICE STANDARD", "title": "I beat the office standard on this typing speed test — can you beat me?",
             "desc": "60-79 WPM on a free 60-second typing speed test. Can you beat my score?"},
 "average": {"badge": "AVERAGE TYPIST", "title": "I scored above the adult average on this typing speed test — can you beat me?",
             "desc": "40-59 WPM on a free 60-second typing speed test. Can you beat my score?"},
 "beginner": {"badge": "JUST STARTED", "title": "I just measured my typing speed — watch me improve",
             "desc": "Under 40 WPM and improving on a free typing speed test. Follow my progress!"},
}
GENERIC = {"badge": "FREE TYPING SPEED TEST", "title": "Check your typing speed in 60 seconds — free, no sign up",
           "desc": "Free online typing speed test. Measure WPM and accuracy with instant results. No sign up."}

CSS = """body{background:#0b0c10;color:#edeef2;font-family:'Inter','Segoe UI',system-ui,sans-serif;margin:0;display:flex;min-height:100vh;align-items:center;justify-content:center}
.card{max-width:640px;margin:24px;padding:40px 44px;background:#15171f;border:1px solid #262a37;border-radius:16px;text-align:center;box-shadow:0 10px 40px -12px rgba(0,0,0,.55)}
.badge{display:inline-block;background:rgba(255,201,60,.14);color:#ffc93c;font-weight:800;letter-spacing:.08em;padding:8px 18px;border-radius:999px;font-size:.85rem}
.score{font-size:4.2rem;font-weight:800;margin:18px 0 4px;color:#ffc93c;font-variant-numeric:tabular-nums}
.unit{color:#8b91a6;font-size:1.1rem}
.acc{font-size:1.3rem;margin:10px 0 26px;color:#b4b8c7}
a.btn{display:inline-block;background:linear-gradient(180deg,#ffd96b,#ffc93c);color:#241c00;font-weight:700;text-decoration:none;padding:14px 28px;border-radius:999px;margin:6px 8px 0}
a.ghost{background:transparent;color:#b4b8c7;border:1px solid #3c4252}
p.sub{color:#8b91a6;font-size:.95rem;margin:22px 0 0}"""

JS = """var p=new URLSearchParams(location.search),s=p.get('s'),a=p.get('a');
if(s){document.getElementById('score').textContent=s;document.getElementById('sunit').textContent='WPM';}
if(a){document.getElementById('acc').textContent=a+'% accuracy';}
var og=document.querySelector('meta[property="og:title"]');document.title=og?og.content:document.title;"""

def page(tier, info, slug=None):
    slug = slug or tier
    og_img = f"{SITE}/og/{tier}.png"
    url = f"{SITE}/{slug}.html"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{info['title']}</title>
<meta name="description" content="{info['desc']}">
<meta name="robots" content="noindex, follow">
<link rel="canonical" href="{url}">
<meta property="og:title" content="{info['title']}">
<meta property="og:description" content="{info['desc']}">
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og_img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:site_name" content="Typing.Rerivo">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{info['title']}">
<meta name="twitter:description" content="{info['desc']}">
<meta name="twitter:image" content="{og_img}">
<style>{CSS}</style>
</head>
<body>
<div class="card">
  <span class="badge">{info['badge']}</span>
  <div class="score" id="score">—</div>
  <div class="unit" id="sunit"></div>
  <div class="acc" id="acc"></div>
  <a class="btn" href="/">Take the test — beat my score</a>
  <a class="btn ghost" href="/average-typing-speed.html">See speed benchmarks</a>
  <p class="sub">Free typing speed test at typing.rerivo.com — 60 seconds, instant results, no sign up.</p>
</div>
<script>{JS}</script>
</body>
</html>
"""

for tier, info in TIERS.items():
    (ROOT / f"share-{tier}.html").write_text(page(tier, info), encoding="utf-8")
    print(f"share-{tier}.html 写出")
(ROOT / "share.html").write_text(page("generic", GENERIC, slug="share"), encoding="utf-8")
print("share.html 写出（generic 兜底）")
