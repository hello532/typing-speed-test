#!/usr/bin/env python3
"""站外链接审计 —— 检查所有出站链接是否还能打开。

    python3 src/tools/linkout.py            # 只报非 200
    python3 src/tools/linkout.py --all      # 全部列出
    python3 src/tools/linkout.py --json

为什么要单独一个工具：
  1. health.py 是**离线**门禁，不能依赖网络；出站链接天然会腐坏，必须单独跑。
  2. 学术出版商（ACM / Elsevier / Wiley）对非浏览器 UA 返回 403。这是反爬，不是死链。
     所以 403 会被标成 `publisher-blocked`，并提示用真浏览器复核，而不是直接判失败。
     真正的死链是 404 / 410 / 域名不存在。
  3. schema.org、adsbygoogle 这类机器可读 URL 不算可点击链接，单独跳过。

退出码：1 = 存在疑似死链；0 = 只有正常与「被出版商拦截」两类。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
SKIP_HOSTS = ("schema.org", "pagead2.googlesyndication.com", "googletagmanager.com")
PUBLISHER_HOSTS = ("dl.acm.org", "doi.org", "link.springer.com", "sciencedirect.com",
                   "onlinelibrary.wiley.com", "ieeexplore.ieee.org", "tandfonline.com")
URL_RE = re.compile(r'https?://[^\s"\'<>)\\]+')


def collect() -> Counter:
    seen: Counter = Counter()
    for p in list(ROOT.glob("*.html")) + [ROOT / "llms.txt", ROOT / "404.html"]:
        if not p.exists():
            continue
        for u in URL_RE.findall(p.read_text(encoding="utf-8", errors="ignore")):
            u = u.rstrip(".,;:'\"")
            if "typing.rerivo.com" in u:
                continue
            if any(h in u for h in SKIP_HOSTS):
                continue
            seen[u] += 1
    return seen


def probe(url: str) -> tuple[str, str]:
    req = urllib.request.Request(url, headers={"User-Agent": UA,
                                               "Accept": "text/html,application/xhtml+xml"})
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            return "ok", str(r.status)
    except urllib.error.HTTPError as e:
        if e.code in (403, 429) and any(h in url for h in PUBLISHER_HOSTS):
            return "publisher-blocked", str(e.code)
        if e.code in (403, 429):
            return "blocked", str(e.code)
        return "dead", str(e.code)
    except Exception as e:                                   # 超时 / DNS / TLS
        return "dead", type(e).__name__


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    urls = collect()
    results = []
    for u in sorted(urls):
        verdict, detail = probe(u)
        results.append({"url": u, "verdict": verdict, "detail": detail, "refs": urls[u]})
    dead = [r for r in results if r["verdict"] == "dead"]
    if a.json:
        print(json.dumps({"results": results, "dead": len(dead)}, ensure_ascii=False, indent=1))
        return 1 if dead else 0
    print(f"站外链接 {len(results)} 条（去重后）：")
    for r in results:
        if r["verdict"] == "ok" and not a.all:
            continue
        mark = {"ok": "✅", "publisher-blocked": "🔒", "blocked": "🚧", "dead": "❌"}[r["verdict"]]
        print(f"  {mark} {r['verdict']:<18} {r['detail']:<12} {r['url'][:88]}")
    print(f"\n死链 {len(dead)} 条；🔒 = 出版商反爬（用真浏览器复核，非死链）")
    return 1 if dead else 0


if __name__ == "__main__":
    sys.exit(main())
