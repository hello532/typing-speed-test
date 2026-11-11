#!/usr/bin/env python3
"""r108: 去规模化（scaled content）手术。

背景（2026-11-11 诊断）：
  GSC 显示全站曝光在 2026-10-28 从 ~400/天 断崖到 0–3/天；首页
  indexStatusResult.verdict = NEUTRAL / "Crawled - currently not indexed"；
  sitemap 报 submitted 184 / indexed 0。站点没有任何技术性阻断
  （robots ALLOWED、indexing ALLOWED、fetch SUCCESSFUL），因此这是
  站点级质量判定：184 个页面里大批是同一模板套出来的角色/考试/词表变体
  （typing-test-for-*、*-exam、top-*-words），命中 Google 的
  "scaled content abuse" 特征。

本脚本按类别一次到位地删掉这些变体页，并在四处同步：
  src/pages.json   页面定义
  src/clusters.json 枢纽页目录（否则 typing-tests.html 会留死链）
  llms.txt          AI 清单（gate 13 要求与页面集合精确一致）
  产物 *.html / *.md 直接删除（GH Pages 对缺失文件返回 404，比软 404 干净）

用法：
  python3 src/tools/prune_scaled.py --dry     # 只打印将删除的清单
  python3 src/tools/prune_scaled.py           # 真删
删完必须跑： python3 build.py && python3 verify.py
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"

# 保留名单（这些虽然也在族里，但有真实搜索量与独立意图，先留）
KEEP = {
    "typing-test-for-jobs.html",     # 入门口，role 页的枢纽
    "typing-test-for-students.html",  # 90 天 84 曝光，族内最高
    "typing-test-for-kids.html",
    "typing-speed-requirements.html",  # 全职业 WPM 要求的真实数据页
    "top-1000-english-words.html",     # 词表族里唯一有独立工具价值的
    "typing-practice-for-programmers.html",
    "programmer-typing-speed.html",
    "sql-typing-practice.html",
    "typing-tips.html",
    "how-to-get-better-at-typing.html",
}

# 按族删除：族 = 一批同模板、同意图、互 cannibalize 的页面
FAMILIES = {
    "job-role": [
        "typing-test-for-accountants", "typing-test-for-call-center",
        "typing-test-for-court-clerk", "typing-test-for-court-reporter",
        "typing-test-for-customer-service", "typing-test-for-dispatch",
        "typing-test-for-insurance-claims", "typing-test-for-interview",
        "typing-test-for-legal-secretary", "typing-test-for-medical-billing",
        "typing-test-for-medical-receptionist", "typing-test-for-nurse",
        "typing-test-for-paralegal", "typing-test-for-receptionist",
        "typing-test-for-seniors", "typing-test-for-virtual-assistant",
        "typing-test-for-warehouse-admin", "typing-test-for-teachers",
        "typing-test-for-adults",
    ],
    "exam": [
        "bank-typing-test", "civil-service-typing-test", "criticall-typing-test",
        "federal-typing-test", "government-typing-test", "ssc-typing-test",
        "usps-postal-exam-typing-test", "typing-test-government-jobs",
    ],
    "word-list": [
        "top-en-words", "top-es-words", "top-hi-words", "top-id-words",
        "top-ja-words", "top-ko-words", "top-th-words", "top-tr-words",
        "top-ur-words", "top-vi-words",
    ],
    "code-lang": [
        "go-typing-practice", "javascript-code-typing", "python-code-typing",
        "rust-typing-practice", "typescript-typing-practice",
    ],
    "speed-guide": [
        "easy-way-to-learn-touch-typing", "how-to-type-faster-and-more-accurately",
        "how-to-type-faster-for-beginners", "learn-to-type-faster",
        "learn-to-type-faster-free", "touch-typing-tips",
        "typing-speed-exercises", "typing-speed-improvement-tips",
        "typing-test-tips", "how-to-pass-a-typing-test",
    ],
}


def targets() -> list[str]:
    out = []
    for fam, stems in FAMILIES.items():
        for s in stems:
            f = s + ".html"
            if f in KEEP:
                print(f"  skip (keep list): {f}")
                continue
            out.append(f)
    return sorted(set(out))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", action="store_true")
    args = ap.parse_args()

    drop = targets()
    print(f"将删除 {len(drop)} 个页面：")
    for d in drop:
        print("  -", d)

    if args.dry:
        return 0

    # 1) pages.json
    pj = SRC / "pages.json"
    cfg = json.loads(pj.read_text(encoding="utf-8"))
    before = len(cfg["pages"])
    cfg["pages"] = [p for p in cfg["pages"] if p["file"] not in drop]
    pj.write_text(json.dumps(cfg, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"pages.json: {before} → {len(cfg['pages'])}")

    # 2) clusters.json（枢纽页目录）
    cj = SRC / "clusters.json"
    cl = json.loads(cj.read_text(encoding="utf-8"))
    removed_links = 0
    for k, items in cl.items():
        keep = [it for it in items if it.get("file") not in drop]
        removed_links += len(items) - len(keep)
        cl[k] = keep
    cj.write_text(json.dumps(cl, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"clusters.json: 去掉 {removed_links} 条目录链接")

    # 3) llms.txt
    lt = ROOT / "llms.txt"
    dropped_urls = {f"https://typing.rerivo.com/{d}" for d in drop}
    lines = lt.read_text(encoding="utf-8").splitlines(keepends=True)
    kept = [ln for ln in lines if not any(u in ln for u in dropped_urls)]
    lt.write_text("".join(kept), encoding="utf-8")
    print(f"llms.txt: 去掉 {len(lines)-len(kept)} 行")

    # 4) 产物
    n = 0
    for d in drop:
        for p in (ROOT / d, ROOT / d.replace(".html", ".md")):
            if p.exists():
                p.unlink()
                n += 1
    print(f"删除产物文件 {n} 个")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
