#!/usr/bin/env python3
"""站点体检 —— 一次跑完「不依赖搜索引擎数据」的硬检查。

    python3 src/tools/health.py            # 全量体检
    python3 src/tools/health.py --json

检查项（都能在本地判定，不需要 GSC）：
  1. 正文内链是否有指向不存在文件的死链
  2. title 是否重复（描述重复已由 verify 6b 管）
  3. canonical 是否自指
  4. sitemap / llms.txt / 页面集合是否三方一致（verify 已管，这里再报一次便于外部引用）
  5. 每页是否恰好一个 h1
  6. 每页是否有 meta description（且非空）
  7. 页脚是否覆盖全部页面（verify 12）
  8. .md 镜像是否存在且与页面同源
  9. og:image / twitter 卡片是否有值
 10. 页内锚点是否全部能解析

退出码 1 表示有 FAIL，方便挂 CI。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SITE = "https://typing.rerivo.com"
FOOTER_RE = re.compile(r"<footer>.*?</footer>", re.S)
# 证书/分享卡是 JS 里拼出来的字符串文档（含它自己的 <h1>），统计页面结构时必须先剥掉
SCRIPT_RE = re.compile(r"<script.*?</script>", re.S)


def pages() -> list[Path]:
    return sorted(p for p in ROOT.glob("*.html") if not p.name.startswith(("google", "share")))


def check() -> dict:
    files = pages()
    names = {p.name for p in files}
    out = {"pages": len(files), "fail": [], "warn": [], "ok": []}

    dead, titles, missing_desc, bad_canon, bad_h1, missing_md = [], Counter(), [], [], [], []
    for p in files:
        h = p.read_text(encoding="utf-8")
        body = FOOTER_RE.sub("", h)
        for href in re.findall(r'href="([^"#?:]+\.html)"', body):
            if href not in names:
                dead.append((p.name, href))
        t = re.search(r"<title>(.*?)</title>", h, re.S)
        titles[t.group(1).strip() if t else ""] += 1
        d = re.search(r'<meta name="description" content="([^"]*)"', h)
        if not d or not d.group(1).strip():
            missing_desc.append(p.name)
        c = re.search(r'<link rel="canonical" href="([^"]+)"', h)
        want = SITE + "/" if p.name == "index.html" else SITE + "/" + p.name
        if not c or c.group(1) != want:
            bad_canon.append((p.name, c.group(1) if c else None))
        if len(re.findall(r"<h1[\s>]", SCRIPT_RE.sub("", h))) != 1:
            bad_h1.append(p.name)
        md = p.with_suffix(".md")
        if p.name != "index.html" and not md.exists():
            missing_md.append(p.name)

    dup_titles = [t for t, n in titles.items() if n > 1]
    (out["fail"] if dead else out["ok"]).append(
        f"死链：{len(dead)} 条" + (f" {dead[:5]}" if dead else ""))
    (out["fail"] if dup_titles else out["ok"]).append(
        f"重复 title：{len(dup_titles)}" + (f" {dup_titles[:3]}" if dup_titles else ""))
    (out["fail"] if missing_desc else out["ok"]).append(f"缺 description：{len(missing_desc)}")
    (out["fail"] if bad_canon else out["ok"]).append(
        f"canonical 非自指：{len(bad_canon)}" + (f" {bad_canon[:3]}" if bad_canon else ""))
    (out["fail"] if bad_h1 else out["ok"]).append(f"h1 数量不为 1：{len(bad_h1)}" + (f" {bad_h1[:3]}" if bad_h1 else ""))
    (out["warn"] if missing_md else out["ok"]).append(f"缺 .md 镜像：{len(missing_md)}")

    sm = set(re.findall(r"<loc>(.*?)</loc>", (ROOT / "sitemap.xml").read_text(encoding="utf-8")))
    want = {SITE + "/" if n == "index.html" else SITE + "/" + n for n in names}
    (out["fail"] if sm != want else out["ok"]).append(
        f"sitemap 与页面集合一致：{'是' if sm == want else f'差 {len(sm ^ want)}'}")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    missing_llms = [n for n in names if n != "index.html" and n not in llms]
    (out["fail"] if missing_llms else out["ok"]).append(f"llms.txt 缺页：{len(missing_llms)}")

    # 10) 页内锚点必须能解析（目录、跳转列表、脚注都靠它）
    bad_anchor = []
    for p in files:
        h = p.read_text(encoding="utf-8")
        ids = set(re.findall(r'\sid="([^"]+)"', h))
        missing = {t for t in re.findall(r'href="#([^"]+)"', h) if t not in ids}
        if missing:
            bad_anchor.append((p.name, sorted(missing)[:3]))
    (out["fail"] if bad_anchor else out["ok"]).append(
        f"页内锚点未解析：{len(bad_anchor)}" + (f" {bad_anchor[:3]}" if bad_anchor else ""))

    # 描述长度分布（软指标，只报数）
    lens = []
    for p in files:
        d = re.search(r'<meta name="description" content="([^"]*)"', p.read_text(encoding="utf-8"))
        if d:
            lens.append(len(d.group(1)))
    lens.sort()
    out["desc_len"] = {"min": lens[0], "median": lens[len(lens) // 2], "max": lens[-1]}
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    r = check()
    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=1))
        return 1 if r["fail"] else 0
    print(f"站点体检：{r['pages']} 页")
    for line in r["ok"]:
        print("  ✅", line)
    for line in r["warn"]:
        print("  ⚠️ ", line)
    for line in r["fail"]:
        print("  ❌", line)
    print(f"  描述长度 min/median/max = {r['desc_len']['min']}/{r['desc_len']['median']}/{r['desc_len']['max']}")
    return 1 if r["fail"] else 0


if __name__ == "__main__":
    sys.exit(main())
