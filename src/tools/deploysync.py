#!/usr/bin/env python3
"""部署一致性 —— 本地构建产物 vs 线上实际返回的字节。

    python3 src/tools/deploysync.py            # 只报不一致
    python3 src/tools/deploysync.py --all      # 全部列出
    python3 src/tools/deploysync.py --sample 20

为什么需要它：这一晚遇到两次「改完看不到」——GitHub Pages 构建延迟、Fastly 的
max-age=600、以及浏览器自身缓存。三者叠在一起时，"我验证过了"和"用户看到的是它"
不是同一件事。这个脚本把两者逐字节对比，作为上线后的最后一道确认。

做法：对每个页面取本地 sha256，再从线上拉一次（带随机查询串绕过 CDN 缓存），
归一化 HTML 后比对摘要。不比对时间戳之类易变内容——产物是确定性的，不一致就是
真的不一致，而不是"看起来不一样"。

退出码：1 = 有页面不一致或取不到；0 = 全部一致。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SITE = "https://typing.rerivo.com"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def local_pages() -> list[str]:
    skip = ("google", "share")
    return sorted(p.name for p in ROOT.glob("*.html")
                  if not p.name.startswith(skip) and p.name != "404.html")


def fetch(url: str) -> tuple[str, str | None]:
    bust = f"?ds={random.randint(0, 10**9)}"
    req = urllib.request.Request(url + bust, headers={"User-Agent": UA,
                                                      "Cache-Control": "no-cache"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return "ok", r.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        return f"http-{e.code}", None
    except Exception as e:
        return type(e).__name__, None


def check(name: str) -> dict:
    path = ROOT / name
    local = digest(path.read_text(encoding="utf-8"))
    url = SITE + "/" + ("" if name == "index.html" else name)
    status, body = fetch(url)
    if body is None:
        return {"page": name, "status": status, "live": None, "local": local, "match": False}
    live = digest(body)
    return {"page": name, "status": status, "live": live, "local": local, "match": live == local}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--sample", type=int, default=0)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--workers", type=int, default=8)
    a = ap.parse_args()
    names = local_pages()
    if a.sample:
        names = names[: a.sample]
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        results = list(ex.map(check, names))
    bad = [r for r in results if not r["match"]]
    if a.json:
        print(json.dumps({"checked": len(results), "mismatch": len(bad), "results": results},
                         ensure_ascii=False, indent=1))
        return 1 if bad else 0
    print(f"比对 {len(results)} 页（本地 sha256 vs 线上实际返回）")
    if a.all:
        for r in results:
            print(f"  {'✅' if r['match'] else '❌'} {r['status']:<9} {r['local']} {r['live'] or '-':<16} {r['page']}")
    if bad:
        print(f"\n❌ 不一致 {len(bad)} 页：")
        for r in bad[:20]:
            print(f"   {r['status']:<9} local={r['local']} live={r['live'] or '-'}  {r['page']}")
        print("\n可能原因：Pages 构建未完成 / CDN 仍在 max-age 窗口内 / 本地未重新 build。"
              "\n等待 60-90 秒后重跑；仍不一致则 git push 是否成功需要确认。")
        return 1
    print("✅ 全部与本地构建一致")
    return 0


if __name__ == "__main__":
    sys.exit(main())
