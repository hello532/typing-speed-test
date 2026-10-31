#!/usr/bin/env python3
"""基线快照 —— 每次收工前跑一次，把「当时站点的状态」写进 state/，下次可以 diff。

    python3 src/tools/baseline.py            # 写 state/<今天>.json，并与上一份对比
    python3 src/tools/baseline.py --json

记录的内容都是**本地可判定**的：
  · 页面数、正文长度分布、FAQ 总数、TL;DR 覆盖
  · build --check / verify.py / health.py 的退出码与关键计数
  · 若有 src/tools/gsc-snapshot.json，附上当时的点击/曝光/CTR/位置

不做的：不去抓线上（那是 deploysync.py 的事）、不调用浏览器（那是 cwv/browsercheck 的事）。
这样它能在任何环境里跑，包括没有网络和没有浏览器的 CI。
"""
from __future__ import annotations

import json
import re
import statistics
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STATE = ROOT / "state"


def run(cmd: list[str]) -> tuple[int, str]:
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr)


def main() -> int:
    cfg = json.loads((ROOT / "src" / "pages.json").read_text(encoding="utf-8"))
    pages = cfg["pages"]
    bodies = [sum(len(x) for s in p["seo"] for x in s["p"]) for p in pages]
    snap = {
        "date": date.today().isoformat(),
        "pages": len(pages),
        "body_chars": {"min": min(bodies), "median": int(statistics.median(bodies)),
                       "max": max(bodies)},
        "faq_total": sum(len(p["faq"]) for p in pages),
        "tldr_pages": sum(1 for p in pages if p.get("tldr")),
        "sitemap_urls": len(re.findall(r"<loc>", (ROOT / "sitemap.xml").read_text(encoding="utf-8"))),
        "llms_bytes": (ROOT / "llms.txt").stat().st_size,
    }
    code, out = run([sys.executable, "build.py", "--check"])
    snap["build_check"] = {"exit": code, "ok": code == 0}
    code, out = run([sys.executable, "verify.py"])
    m = re.search(r"通过 (\d+)/(\d+) 项", out)
    snap["verify"] = {"exit": code, "passed": int(m.group(1)) if m else None,
                      "total": int(m.group(2)) if m else None}
    code, out = run([sys.executable, "src/tools/health.py"])
    m = re.search(r"检查 (\d+) 项", out)
    ok = len(re.findall(r"✅", out))
    snap["health"] = {"exit": code, "checks_ok": ok}
    gs = ROOT / "src" / "tools" / "gsc-snapshot.json"
    if gs.exists():
        g = json.loads(gs.read_text(encoding="utf-8"))
        snap["gsc"] = {k: g.get(k) for k in ("captured", "clicks", "impressions", "ctr", "position")}

    STATE.mkdir(exist_ok=True)
    target = STATE / f"{snap['date']}.json"
    prev = sorted(p for p in STATE.glob("*.json") if p.stem < snap["date"])
    diff = {}
    if prev:
        old = json.loads(prev[-1].read_text(encoding="utf-8"))
        for k in ("pages", "faq_total", "tldr_pages", "sitemap_urls", "llms_bytes"):
            if k in old and old[k] != snap[k]:
                diff[k] = [old[k], snap[k]]
        if old.get("gsc") and snap.get("gsc"):
            for k in ("clicks", "impressions", "position"):
                if old["gsc"].get(k) != snap["gsc"].get(k):
                    diff[f"gsc.{k}"] = [old["gsc"].get(k), snap["gsc"].get(k)]
        snap["compared_to"] = prev[-1].name
    target.write_text(json.dumps(snap, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    if "--json" in sys.argv:
        print(json.dumps(snap, ensure_ascii=False, indent=1))
    else:
        print(f"baseline → {target.relative_to(ROOT)}")
        print(f"  pages {snap['pages']} ｜ body {snap['body_chars']['median']} median ｜ "
              f"FAQ {snap['faq_total']} ｜ TL;DR {snap['tldr_pages']} ｜ "
              f"sitemap {snap['sitemap_urls']} ｜ llms {snap['llms_bytes']}B")
        print(f"  build {snap['build_check']['ok']} ｜ verify {snap['verify']['passed']}/{snap['verify']['total']} "
              f"｜ health {snap['health']['checks_ok']} checks")
        if snap.get("gsc"):
            print(f"  gsc {snap['gsc']['captured']}: {snap['gsc']['clicks']:.0f} clicks / "
                  f"{snap['gsc']['impressions']:.0f} impressions / pos {snap['gsc']['position']:.1f}")
        print("  diff vs previous: " + (json.dumps(diff, ensure_ascii=False) if diff else "no change"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
