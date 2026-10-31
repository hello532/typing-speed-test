#!/usr/bin/env python3
"""正文内链图 —— 区分「页脚样板链接」与「正文上下文链接」。

    python3 src/tools/linkgraph.py            # 概览 + 正文入链为 0 的页面
    python3 src/tools/linkgraph.py --top 30   # 按正文入链数排序
    python3 src/tools/linkgraph.py --json

为什么要分：footer 每页都有 160 条链接，等于零信息量；真正传递主题相关性的是
正文里那句「这里有个讲 X 的页」。所以本工具把 <footer>…</footer> 和 related
区块剥掉，只统计正文（hero + seo + faq 里）出现的链接，再按目标页聚合。

深度口径：从 index.html 出发，按正文链接 BFS，报告每页的点击深度。
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict, deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SITE = "https://typing.rerivo.com"

FOOTER_RE = re.compile(r"<footer>.*?</footer>", re.S)
RELATED_RE = re.compile(r'<nav class="related".*?</nav>', re.S)
HEADER_RE = re.compile(r'<header class="top">.*?</header>', re.S)
CRUMB_RE = re.compile(r'<nav class="crumbs".*?</nav>', re.S)
FAQ_RE = re.compile(r'<section class="seo faq">.*?</section>', re.S)
LINK_RE = re.compile(r'<a\s[^>]*href="([^"#?]+)"[^>]*>(.*?)</a>', re.S)


def strip_tags(s: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s)).strip()


def body_links(html: str) -> list[tuple[str, str]]:
    body = FOOTER_RE.sub("", html)
    body = HEADER_RE.sub("", body)
    body = CRUMB_RE.sub("", body)
    body = RELATED_RE.sub("", body)
    out = []
    for href, text in LINK_RE.findall(body):
        if href.startswith(("http://", "https://", "mailto:", "/")):
            continue
        out.append((href, strip_tags(text)[:60]))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--top", type=int, default=0)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    files = sorted(p.name for p in ROOT.glob("*.html"))
    graph, anchors = {}, defaultdict(Counter)
    for f in files:
        links = body_links((ROOT / f).read_text(encoding="utf-8"))
        graph[f] = links
        for href, text in links:
            if href in files:
                anchors[href][text] += 1

    inbound = {f: sum(1 for src in files for h, _ in graph[src] if h == f) for f in files}

    # 从首页按正文链接 BFS
    depth = {"index.html": 0}
    q = deque(["index.html"])
    while q:
        cur = q.popleft()
        for href, _ in graph.get(cur, []):
            if href in files and href not in depth:
                depth[href] = depth[cur] + 1
                q.append(href)

    orphan = sorted([f for f in files if inbound[f] == 0])
    unreachable = sorted([f for f in files if f not in depth])
    deep = sorted([(depth.get(f, 99), f) for f in files if depth.get(f, 99) >= 3])

    if a.json:
        print(json.dumps({"pages": len(files), "orphans": orphan,
                          "unreachable": unreachable,
                          "inbound": inbound,
                          "depth": depth}, ensure_ascii=False, indent=1))
        return 0

    print(f"正文内链图：{len(files)} 页")
    print(f"  正文入链中位数 {sorted(inbound.values())[len(files)//2]}，合计 {sum(inbound.values())} 条")
    print(f"  从首页正文可达 {len(depth)}/{len(files)} 页；深度 1: "
          f"{sum(1 for d in depth.values() if d == 1)}，深度 2: "
          f"{sum(1 for d in depth.values() if d == 2)}，深度 ≥3: {len(deep)}")
    print(f"\n正文入链为 0 的页面（{len(orphan)}）：")
    for f in orphan[:40]:
        print("  ·", f)
    if len(orphan) > 40:
        print(f"  … 另有 {len(orphan)-40} 页")
    if unreachable:
        print(f"\n首页不可达（{len(unreachable)}）：{', '.join(unreachable[:15])}")
    if a.top:
        print(f"\n正文入链最多的 {a.top} 页：")
        for f, n in sorted(inbound.items(), key=lambda x: -x[1])[:a.top]:
            print(f"  {n:>4}  {f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
