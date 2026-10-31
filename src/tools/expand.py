#!/usr/bin/env python3
"""批量加页 —— 一次把「新页定义」写进四个真源，避免手改大 JSON 时漏项。

    python3 src/tools/expand.py src/batches/r23-jobs.json          # 应用
    python3 src/tools/expand.py src/batches/r23-jobs.json --check   # 只校验

为什么要这个工具：加一页要同时改 4 处（pages.json 页面表 / footer.html 页脚枢纽 /
llms.txt 清单 / clusters.json 相关聚类），漏一处就撞 verify 门禁（12 页脚覆盖、
13 llms 覆盖）或让新页成为孤儿页。手工改四处必然出错，所以把这四处写成一个动作。

批次文件格式：
{
  "footer_group": "Guides & articles",     # 页脚 <p class="foot-cap"> 的原文
  "llms_section": "Guides & Articles",     # llms.txt 里 "## " 后的标题
  "cluster": "jobs",                        # src/clusters.json 的键
  "pages": [ { ...页面配置... } ]
}

页面配置最少写：file/title/metaDesc/h1/heroP/seo/faq/dur/mode/crumbs。
其余（canonical/webAppUrl/webAppName/bcItems/nav/faqH2/faqFirstOpen/ldPretty）自动补全。
"""
from __future__ import annotations

import difflib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
SITE = "https://typing.rerivo.com"
NAV = [{"href": "1-minute-typing-test.html", "text": "1 Minute Test"},
       {"href": "words-per-minute-test.html", "text": "WPM Test"},
       {"href": "typing-practice.html", "text": "Typing Practice"}]
REQUIRED = ("file", "title", "metaDesc", "h1", "heroP", "seo", "faq", "dur", "mode", "crumbs")
TITLE_MAX, DESC_MAX = 62, 158


def fail(msg: str) -> int:
    print(f"❌ {msg}")
    return 1


def normalise(p: dict) -> dict:
    canonical = f"{SITE}/{p['file']}"
    out = {
        "file": p["file"],
        "title": p["title"],
        "metaDesc": p["metaDesc"],
        "canonical": canonical,
        "dur": p["dur"],
        "mode": p["mode"],
        "variant": p.get("variant"),
        "nav": NAV,
        "crumbs": p["crumbs"],
        "h1": p["h1"],
        "heroP": p["heroP"],
        "seo": p["seo"],
        "faqFirstOpen": True,
        "faqH2": p.get("faqH2", "Frequently asked questions"),
        "faq": p["faq"],
        "webAppName": p.get("webAppName", p["h1"]),
        "webAppUrl": canonical,
        "bcItems": [{"name": "Home", "item": SITE + "/"},
                    {"name": p["crumbs"][1], "item": canonical}],
        "ldPretty": ["FAQPage", "BreadcrumbList"],
    }
    for k in ("tldr", "layout", "lang", "alts"):
        if p.get(k) is not None:
            out[k] = p[k]
    return out


def validate(new_pages: list[dict], existing: list[dict]) -> list[str]:
    errs = []
    known = {p["file"] for p in existing}
    for p in new_pages:
        miss = [k for k in REQUIRED if k not in p]
        if miss:
            errs.append(f"{p.get('file')}: 缺字段 {miss}")
            continue
        if p["file"] in known:
            errs.append(f"{p['file']}: 已存在")
        if len(p["title"]) > TITLE_MAX:
            errs.append(f"{p['file']}: title {len(p['title'])} > {TITLE_MAX}")
        if len(p["metaDesc"]) > DESC_MAX:
            errs.append(f"{p['file']}: metaDesc {len(p['metaDesc'])} > {DESC_MAX}")
        if not p["file"].endswith(".html"):
            errs.append(f"{p['file']}: 文件名须以 .html 结尾")
        body = sum(len(x) for s in p["seo"] for x in s["p"])
        if body < 1200:
            errs.append(f"{p['file']}: 正文 {body} 字符 < 1200（薄页，不许进）")
        if len(p["faq"]) < 5:
            errs.append(f"{p['file']}: FAQ {len(p['faq'])} 条 < 5")
        if not p["heroP"].strip():
            errs.append(f"{p['file']}: heroP 空")
        others = [(q["file"], q["metaDesc"]) for q in existing] + \
                 [(q["file"], q["metaDesc"]) for q in new_pages if q is not p]
        for f, d in others:
            r = difflib.SequenceMatcher(None, p["metaDesc"], d).ratio()
            if r > 0.70:
                errs.append(f"{p['file']}: 描述与 {f} 相似度 {r:.2f} > 0.70")
    return errs


def insert_footer(group: str, lines: list[tuple[str, str]]) -> None:
    f = SRC / "footer.html"
    html = f.read_text(encoding="utf-8")
    cap = f'<p class="foot-cap">{group}</p>'
    if cap not in html:
        raise SystemExit(f"footer.html: 未找到分组 {group!r}")
    i = html.index(cap)
    j = html.index("</p>", i + len(cap)) + 4
    chunk = "".join(f' · <a href="{href}">{text}</a>' for href, text in lines)
    html = html[:j - 4] + chunk + html[j - 4:]
    f.write_text(html, encoding="utf-8")


def insert_llms(section: str, lines: list[tuple[str, str, str]]) -> None:
    f = ROOT / "llms.txt"
    txt = f.read_text(encoding="utf-8")
    head = f"## {section}"
    if head not in txt:
        raise SystemExit(f"llms.txt: 未找到小节 {head!r}")
    i = txt.index(head)
    nxt = txt.find("\n## ", i + len(head))
    insert_at = len(txt) if nxt == -1 else nxt
    block = "".join(f"- [{title}]({SITE}/{href}): {desc}\n" for href, title, desc in lines)
    txt = txt[:insert_at].rstrip("\n") + "\n" + block + ("\n" + txt[insert_at:] if nxt != -1 else "")
    f.write_text(txt, encoding="utf-8")


def insert_cluster(cluster: str, items: list[dict]) -> None:
    f = SRC / "clusters.json"
    data = json.loads(f.read_text(encoding="utf-8"))
    if cluster not in data:
        raise SystemExit(f"clusters.json: 未找到聚类 {cluster!r}")
    files = {i["file"] for i in data[cluster]}
    for it in items:
        if it["file"] not in files:
            data[cluster].append({"file": it["file"], "title": it["title_h1"]})
    f.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    if len(sys.argv) < 2:
        return fail("用法: expand.py <batch.json> [--check]")
    batch = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    check = "--check" in sys.argv
    cfg_path = SRC / "pages.json"
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    raw = batch["pages"]
    errs = validate(raw, cfg["pages"])
    if errs:
        for e in errs:
            print("  ·", e)
        return fail(f"{len(errs)} 处不合规，未写入")
    pages = [normalise(p) for p in raw]
    print(f"校验通过：{len(pages)} 页，正文均 ≥1200 字符，描述互不雷同")
    if check:
        return 0
    cfg["pages"].extend(pages)
    cfg_path.write_text(json.dumps(cfg, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    insert_footer(batch["footer_group"],
                  [(p["file"], p.get("footerText") or p["h1"]) for p in pages])
    insert_llms(batch["llms_section"],
                [(p["file"], p["title"].split(" - ")[0].split(" — ")[0],
                  (p.get("tldr") or p["metaDesc"]).strip()[:160]) for p in pages])
    insert_cluster(batch["cluster"],
                   [{"file": p["file"], "title_h1": p["h1"]} for p in pages])
    print(f"已写入 pages.json / footer.html / llms.txt / clusters.json：{len(pages)} 页")
    return 0


if __name__ == "__main__":
    sys.exit(main())
