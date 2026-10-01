#!/usr/bin/env python3
"""生成内页(长尾词)+robots+sitemap, 并给首页加 schema 和真实内链。正则只匹配唯一处, 零风险。"""
import re

BASE = "https://hello532.github.io/typing-speed-test/"
html = open("index.html", encoding="utf-8").read()

def sub1(pat, new, txt, flags=0):
    out, n = re.subn(pat, new, txt, flags=flags)
    assert n == 1, f"替换非唯一({n}): {pat[:40]}"
    return out

def make_page(cfg):
    t = html
    t = sub1(r'<title>.*?</title>', f'<title>{cfg["title"]}</title>', t)
    t = sub1(r'<meta name="description" content=".*?">',
             f'<meta name="description" content="{cfg["desc"]}">', t)
    t = sub1(r'<meta name="keywords" content=".*?">',
             f'<meta name="keywords" content="{cfg["kw"]}">', t)
    t = sub1(r'<link rel="canonical" href=".*?">',
             f'<link rel="canonical" href="{BASE + cfg["file"]}">', t)
    t = sub1(r'<h1>.*?</h1>', f'<h1>{cfg["h1"]}</h1>', t)
    t = sub1(r'<p class="sub">.*?</p>', f'<p class="sub">{cfg["sub"]}</p>', t)
    t = sub1(r'<section class="doc">.*?</section>', cfg["doc"], t, flags=re.S)
    t = sub1(r'<footer>.*?</footer>', cfg["footer"], t)
    open(cfg["file"], "w", encoding="utf-8").write(t)
    print("wrote", cfg["file"], len(t), "bytes")

LINKS = """<ul>
      <li><a href="index.html">Typing Speed Test</a> — the full speed test with 1-5 minute options.</li>
      <li><a href="1-minute-typing-test.html">1 Minute Typing Test</a> — a focused 60-second speed check.</li>
      <li><a href="words-per-minute-test.html">Words Per Minute Test</a> — benchmark your WPM the standard way.</li>
    </ul>"""

FOOT = '<footer>&copy; 2026 · <a href="index.html">Typing Speed Test</a> · Free online WPM test</footer>'

pages = [
 dict(
  file="1-minute-typing-test.html",
  title="1 Minute Typing Test - Quick WPM Speed Test in 60 Seconds",
  desc="Take a 1 minute typing test and see your words per minute instantly. A fast 60-second WPM test with accuracy and error count. Free, no sign-up.",
  kw="1 minute typing test, 60 second typing test, one minute typing test, 1 min wpm test, quick typing test",
  h1="1 Minute Typing Test",
  sub="How many words can you type in 60 seconds? A fast one-minute typing test with instant WPM and accuracy.",
  doc="""  <section class="doc">
    <h2>What is a 1 minute typing test?</h2>
    <p>A 1 minute typing test is the fastest way to check your typing speed. You type for exactly 60 seconds, and at the end you see your words per minute (WPM), your accuracy and how many errors you made. Sixty seconds is long enough for a meaningful score and short enough to fit into any break.</p>
    <h2>How many words per minute is a good score?</h2>
    <p>Most people type between 35 and 45 WPM. Reaching 60 WPM puts you above average and makes everyday writing, email and coding feel noticeably faster. Professional typists often pass 80 WPM, but speed means little without accuracy, so aim for a high score with very few errors rather than a high score alone.</p>
    <h2>Tips for your 60 second test</h2>
    <p>Sit up straight, keep your eyes on the text instead of the keyboard, and type at a pace you can control. If you make a mistake, fix it before moving on, because uncorrected errors lower both your accuracy and your effective speed.</p>
    <h2>Other typing tests</h2>
""" + LINKS + """
  </section>""",
  footer=FOOT),
 dict(
  file="words-per-minute-test.html",
  title="Words Per Minute Test - Free WPM Test Online | Check Your Typing Speed",
  desc="Free words per minute test. Find out your WPM and typing accuracy in one minute. Learn what words per minute means and how to improve it. No sign-up.",
  kw="words per minute test, wpm test, words per minute, typing speed, how many words per minute, wpm benchmark",
  h1="Words Per Minute Test",
  sub="Measure your words per minute (WPM) the standard way. One minute, instant results, free and no sign-up.",
  doc="""  <section class="doc">
    <h2>What does words per minute (WPM) mean?</h2>
    <p>Words per minute, usually written as WPM, is the standard measure of typing speed. One word is counted as five characters of text, so longer words are not rewarded more than short ones. When you take a words per minute test you learn not just your raw speed, but how accurate you are while typing under a time limit.</p>
    <h2>How is WPM calculated?</h2>
    <p>WPM = correct characters divided by 5, divided by the number of minutes you typed. Accuracy = correct characters divided by everything you typed. This is why guessing words you are unsure about rarely helps your score: every wrong keystroke lowers both numbers.</p>
    <h2>How to increase your words per minute</h2>
    <p>Type a little every day, keep your eyes on the screen, and let your fingers find the keys without looking down. Slow down on the words that trip you up until they become automatic. Accuracy is what allows real speed to last, so practice cleanly first and let speed follow.</p>
    <h2>Other typing tests</h2>
""" + LINKS + """
  </section>""",
  footer=FOOT),
 dict(
  file="typing-practice.html",
  title="Typing Practice - Free Online Typing Drills to Improve Speed & Accuracy",
  desc="Free typing practice online. Longer typing drills to build accuracy and speed a few minutes at a time. Practice typing daily, no sign-up needed.",
  kw="typing practice, typing drills, practice typing, typing exercise, improve typing speed, typing training",
  h1="Typing Practice",
  sub="Build accuracy and speed with longer typing drills. Pick 3 or 5 minutes and practice a little every day.",
  doc="""  <section class="doc">
    <h2>Why typing practice works</h2>
    <p>Typing is a muscle-memory skill, and short regular practice beats long rare sessions. Ten focused minutes a day retrains your fingers far faster than one exhausted hour a week, because you are building steady habits rather than fighting fatigue.</p>
    <h2>How to practice typing effectively</h2>
    <p>Choose a longer test above, focus on pressing each key correctly rather than quickly, and only speed up once your accuracy stays above 95%. Watch the words a little ahead of the one you are typing, so your fingers always know where to go next.</p>
    <h2>Make practice a habit</h2>
    <p>Take one test with your morning coffee and one in the afternoon. Track your WPM and accuracy each time, and celebrate small wins: a steady upward trend over a few weeks matters far more than any single high score.</p>
    <h2>Other typing tests</h2>
""" + LINKS + """
  </section>""",
  footer=FOOT),
]

for cfg in pages:
    make_page(cfg)

# robots.txt
open("robots.txt", "w").write(
    "User-agent: *\nAllow: /\n\n"
    f"Sitemap: {BASE}sitemap.xml\n")
print("wrote robots.txt")

# sitemap.xml
urls = [BASE] + [BASE + c["file"] for c in pages]
sm = ['<?xml version="1.0" encoding="UTF-8"?>',
      '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for i, u in enumerate(urls):
    sm.append(f'  <url><loc>{u}</loc><changefreq>weekly</changefreq>'
              f'<priority>{"1.0" if i == 0 else "0.8"}</priority></url>')
sm.append('</urlset>')
open("sitemap.xml", "w").write("\n".join(sm) + "\n")
print("wrote sitemap.xml", len(urls), "urls")

# 首页: 加 WebApplication schema + 真实内链
schema = """<script type="application/ld+json">
{"@context":"https://schema.org","@type":"WebApplication","name":"Typing Speed Test","url":"https://hello532.github.io/typing-speed-test/","applicationCategory":"UtilityApplication","operatingSystem":"Any device with a web browser","description":"Free online typing speed test. Measure words per minute (WPM) and typing accuracy in 1 to 5 minutes.","offers":{"@type":"Offer","price":"0","priceCurrency":"USD"},"featureList":["WPM test","typing accuracy","1/2/3/5 minute tests","typing practice"],"isAccessibleForFree":true}
</script>
</head>"""
html2 = sub1(r'</head>', schema, html)
html2 = sub1(r'<h2>Other typing tests</h2>\s*<p>.*?</p>',
             """<h2>Other typing tests</h2>
    <ul>
      <li><a href="1-minute-typing-test.html">1 Minute Typing Test</a> — a focused 60-second speed check.</li>
      <li><a href="words-per-minute-test.html">Words Per Minute Test</a> — benchmark your WPM the standard way.</li>
      <li><a href="typing-practice.html">Typing Practice</a> — longer drills to build accuracy and speed.</li>
    </ul>""", html2, flags=re.S)
open("index.html", "w", encoding="utf-8").write(html2)
print("updated index.html", len(html2), "bytes")
