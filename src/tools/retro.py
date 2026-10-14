#!/usr/bin/env python3
"""闭环快照生成器（retrospective snapshot）—— 把「复盘」从凭印象+手写 HTML 报告
变成一条可复跑、可版本化的离线命令。

    python3 src/tools/retro.py            # markdown 快照 → stdout
    python3 src/tools/retro.py --out x.md # 写文件
    python3 src/tools/retro.py --json     # 机器可读（CI / 二次加工）

对应哥飞闭环的第 6 步「复盘」：只读采集，**不联网、不调用 verify.py**
（避免递归与联网抖动）。所有数字都来自仓库内的确定性来源：
git 历史、src/pages.json、sitemap.xml、llms*.txt、robots.txt、
directories.json、构建产物（*.html / *.md）。
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
SITE = "https://typing.rerivo.com"


def git(*args: str) -> str:
    r = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else ""


def collect() -> dict:
    cfg = json.loads((SRC / "pages.json").read_text(encoding="utf-8"))
    pages = cfg["pages"]
    names = [p["file"] for p in pages]

    # ── sitemap：URL 数与 lastmod 分布 ──
    sm = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    sm_urls = re.findall(r"<loc>(.*?)</loc>", sm)
    lastmods = Counter(re.findall(r"<lastmod>([0-9-]+)</lastmod>", sm))

    # ── AI 清单覆盖（llms.txt 链接 / llms-full.txt 页数 / .md 镜像）──
    want = {SITE + "/" if n == "index.html" else SITE + "/" + n for n in names}
    llms_links = set()
    lp = ROOT / "llms.txt"
    if lp.exists():
        llms_links = set(re.findall(r"\]\((https?://[^\)]+)\)", lp.read_text(encoding="utf-8")))
    full_body = (ROOT / "llms-full.txt").read_text(encoding="utf-8") if (ROOT / "llms-full.txt").exists() else ""
    full_covered = sum(1 for u in want if u in full_body)
    md_names = {n.rsplit(".html", 1)[0] + ".md" for n in names}
    md_have = sum(1 for m in md_names if (ROOT / m).exists())

    # ── robots 分桶 ──
    rb = (ROOT / "robots.txt").read_text(encoding="utf-8")
    allow, disallow = [], []
    cur = None
    for raw in rb.splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line or ":" not in line:
            continue
        f, _, v = line.partition(":")
        f, v = f.strip().lower(), v.strip()
        if f == "user-agent":
            cur = v
        elif cur and f == "allow" and v == "/":
            allow.append(cur)
        elif cur and f == "disallow" and v == "/":
            disallow.append(cur)

    # ── 外链台账 ──
    led = json.loads((SRC / "tools" / "directories.json").read_text(encoding="utf-8"))
    rows = led["directories"]
    status = Counter(r["status"] for r in rows)
    dopen = [r["url"] for r in rows if "/pull/" in (r.get("url") or "")]
    dlive = [r["name"] for r in rows if r["status"] == "live"]

    return {
        "git": {
            "commit": git("rev-parse", "--short", "HEAD"),
            "date": git("log", "-1", "--format=%ad", "--date=short"),
            "subject": git("log", "-1", "--format=%s"),
            "commits": len(git("log", "--oneline").splitlines()),
            "dirty": bool(git("status", "--porcelain")),
        },
        "pages": {"count": len(names)},
        "sitemap": {"urls": len(sm_urls), "lastmod_kinds": len(lastmods),
                    "lastmod_latest": max(lastmods) if lastmods else None},
        "ai_manifest": {
            "llms_txt_links": len(llms_links),
            "llms_txt_matches_pages": llms_links == want,
            "llms_full_pages": full_covered,
            "llms_full_bytes": len(full_body),
            "md_mirrors": md_have,
        },
        "robots": {"allow": len(allow), "disallow": len(disallow),
                   "disallow_ua": disallow},
        "backlinks": {"total": len(rows), "by_status": dict(status),
                      "open_prs": len(dopen), "live": len(dlive)},
    }


def as_markdown(d: dict) -> str:
    g, bl = d["git"], d["backlinks"]
    st = bl["by_status"]
    order = ["live", "submitted", "candidate", "blocked_cf", "needs_login", "dead", "skipped"]
    status_line = " · ".join(f"{k}={st[k]}" for k in order if k in st)
    return "\n".join([
        "# 闭环快照（retro snapshot）",
        "",
        f"- 采集时间基点：commit `{g['commit']}`（{g['date']}）",
        f"- 最新提交：{g['subject']}",
        f"- 仓库提交数：{g['commits']}　工作区：{'有未提交改动' if g['dirty'] else '干净'}",
        "",
        "## 1. 建页",
        f"- 落地页：{d['pages']['count']} 页（src/pages.json → build.py 产物）",
        "",
        "## 2. 站内",
        f"- sitemap：{d['sitemap']['urls']} URL，lastmod 最新 {d['sitemap']['lastmod_latest']}"
        f"（{d['sitemap']['lastmod_kinds']} 个日期档）",
        f"- AI 清单：llms.txt {d['ai_manifest']['llms_txt_links']} 链接"
        f"（与页面集{'一致' if d['ai_manifest']['llms_txt_matches_pages'] else '不一致'}）"
        f"、llms-full.txt {d['ai_manifest']['llms_full_pages']} 页 / {d['ai_manifest']['llms_full_bytes']:,}B"
        f"、.md 镜像 {d['ai_manifest']['md_mirrors']} 个",
        f"- robots 分桶：放行 {d['robots']['allow']} UA，拦截 {d['robots']['disallow']} UA",
        "",
        "## 3. 收录",
        f"- sitemap 覆盖 {d['sitemap']['urls']}/{d['pages']['count']} 页"
        f"（线上 200 用 `linkops live`，canonical/robots 用 `linkops index`）",
        f"- 拦截训练爬虫：{', '.join(d['robots']['disallow_ua']) or '（无）'}",
        "",
        "## 4. 外链",
        f"- 台账：{bl['total']} 条（{status_line}）",
        f"- 待合并 PR：{bl['open_prs']} 个　已生效链接：{bl['live']} 条",
        f"- 状态同步：`python3 src/tools/linkops.py pr`（--update 回写）",
        "",
        "## 5. 复盘",
        "- 本文件由 `python3 src/tools/retro.py` 生成（离线、确定性、可版本化）",
        "- 建议每轮闭环收尾时重跑一次，diff 前后快照即为该轮实际增量",
        "",
    ])


def main() -> int:
    ap = argparse.ArgumentParser(description="闭环快照生成器（离线只读）")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    ap.add_argument("--out", help="写入文件（默认 stdout）")
    args = ap.parse_args()

    d = collect()
    text = json.dumps(d, ensure_ascii=False, indent=1) if args.json else as_markdown(d)
    if args.out:
        Path(args.out).write_text(text.rstrip("\n") + "\n", encoding="utf-8")
        print(f"written: {args.out}")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
