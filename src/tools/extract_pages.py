#!/usr/bin/env python3
"""一次性提取器：从现有 18 个 HTML 反推 src/pages.json。

只在架构重构时运行一次。所有字段从真实文件读出，不手写猜测，
以保证 build.py 能语义等价重建每一页。产物提交后本脚本保留作审计证据。
"""
import glob
import html as htmllib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SITE = "https://typing.rerivo.com"


def jsonld_blocks(h):
    """按出现顺序返回 JSON-LD 解析后的 dict 列表。"""
    out = []
    for raw in re.findall(
        r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>', h, re.S
    ):
        out.append(json.loads(raw))
    return out


def extract(fp):
    f = Path(fp).name
    h = open(fp, encoding="utf-8").read()

    def one(pat, s=h, flags=re.S):
        m = re.search(pat, s, flags)
        if not m:
            sys.exit(f"{f}: missing {pat[:40]}")
        return m.group(1) if m.groups() else m.group(0)

    p = {"file": f}
    p["title"] = htmllib.unescape(one(r"<title>(.*?)</title>"))
    p["metaDesc"] = htmllib.unescape(one(r'<meta name="description" content="(.*?)"'))
    p["canonical"] = one(r'rel="canonical" href="(.*?)"', flags=0)

    # og / twitter：等于 title / metaDesc（已验证 17 页如此），
    # 但属性位置会转义 & → &amp;，比较前先解码。
    for key, pat in [
        ("ogTitle", r'property="og:title" content="(.*?)"'),
        ("ogDesc", r'property="og:description" content="(.*?)"'),
        ("ogUrl", r'property="og:url" content="(.*?)"'),
        ("twTitle", r'name="twitter:title" content="(.*?)"'),
        ("twDesc", r'name="twitter:description" content="(.*?)"'),
    ]:
        p[key] = htmllib.unescape(one(pat))
    assert p["ogTitle"] == p["twTitle"] == p["title"], f"{f}: title mismatch"
    assert p["ogDesc"] == p["twDesc"] == p["metaDesc"], f"{f}: desc mismatch"
    assert p["ogUrl"] == p["canonical"], f"{f}: ogUrl != canonical"
    for k in ("ogTitle", "ogDesc", "ogUrl", "twTitle", "twDesc"):
        del p[k]  # 由 title/metaDesc/file 派生，不重复存

    # 引擎初值
    m = re.search(r'var dur=(\d+), mode="(\w+)"', h)
    p["dur"], p["mode"] = int(m.group(1)), m.group(2)

    # nav：header 内除 logo 外的链接（保留原始顺序与 Home 变体 href）
    header = one(r'<header class="top">.*?</header>')
    p["nav"] = [
        {"href": a, "text": t}
        for a, t in re.findall(r'<a href="([^"]*)">(.*?)</a>', header)
        if t != "Typing.Rerivo"
    ]

    # 面包屑（index 无）
    m = re.search(r'<nav class="crumbs".*?</nav>', h, re.S)
    p["crumbs"] = None
    if m:
        parts = re.findall(r"<(?:a|span)[^>]*>(.*?)</(?:a|span)>", m.group(0))
        p["crumbs"] = [x.strip() for x in parts if x.strip() and "&rsaquo;" not in x]

    # hero
    hero = one(r'<section class="hero">.*?</section>')
    p["h1"] = one(r"<h1>(.*?)</h1>", hero)
    p["heroP"] = one(r"<h1>.*?</h1>\s*<p>(.*?)</p>", hero)

    # SEO 正文：h2 + 其后所有 p
    seo_blk = one(r'<section class="seo">\s*.*?</section>')
    p["seo"] = []
    for h2, body in re.findall(r"<h2>(.*?)</h2>(.*?)(?=<h2>|</section>)", seo_blk, re.S):
        ps = re.findall(r"<p>(.*?)</p>", body, re.S)
        if ps:
            p["seo"].append({"h2": h2, "p": ps})

    # FAQ 可见区块
    faq_blk = one(r'<section class="seo faq">.*?</section>')
    p["faqFirstOpen"] = "<details open>" in faq_blk
    p["faqH2"] = one(r"<h2>(.*?)</h2>", faq_blk)
    p["faq"] = [
        {"q": q, "a": a}
        for q, a in re.findall(r"<summary>(.*?)</summary>\s*<p>(.*?)</p>", faq_blk, re.S)
    ]

    # JSON-LD
    ld = jsonld_blocks(h)
    by_type = {d["@type"]: d for d in ld}
    wa = by_type["WebApplication"]
    p["webAppName"] = wa["name"]
    p["webAppUrl"] = wa["url"]
    p["_webAppDesc"] = wa["description"]  # 仅用于校验恒定，输出时提到顶层

    bc = by_type.get("BreadcrumbList")
    p["bcItems"] = (
        [{"name": i["name"], "item": i["item"]} for i in bc["itemListElement"]] if bc else []
    )

    # JSON-LD 原文格式标记：压缩(41块) / 默认分隔符(10块)，用于字节等价重建
    p["ldPretty"] = []
    for d, raw in zip(ld, re.findall(
        r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>', h, re.S
    )):
        if json.dumps(d, ensure_ascii=False) == raw.strip():
            p["ldPretty"].append(d["@type"])

    # FAQPage JSON-LD 应与可见 faq 完全一致（已验证 0/17 不一致）→ 不存，build 时派生
    fa = by_type["FAQPage"]
    ld_pairs = [
        (e["name"].strip(), e["acceptedAnswer"]["text"].strip()) for e in fa["mainEntity"]
    ]
    vis_pairs = [
        (re.sub(r"<[^>]+>", "", x["q"]).strip(), re.sub(r"<[^>]+>", "", x["a"]).strip())
        for x in p["faq"]
    ]
    assert ld_pairs == vis_pairs, f"{f}: FAQPage JSON-LD != visible FAQ"
    return p


def main():
    files = sorted(f for f in glob.glob(str(ROOT / "*.html")) if "google" not in f)
    pages = [extract(fp) for fp in files]

    # 校验恒定字段
    kw = {
        htmllib.unescape(
            re.search(r'<meta name="keywords" content="(.*?)"', open(fp, encoding="utf-8").read()).group(1)
        )
        for fp in files
    }
    assert len(kw) == 1, f"keywords not constant: {len(kw)} variants"
    footers = {
        re.search(r"<footer>.*?</footer>", open(fp, encoding="utf-8").read(), re.S).group(0)
        for fp in files
    }
    assert len(footers) == 1, f"footer not constant: {len(footers)} variants"
    wadesc = {p["_webAppDesc"] for p in pages}
    assert len(wadesc) == 1, f"webApp description not constant: {len(wadesc)}"

    webapp_desc = pages[0]["_webAppDesc"]
    for pg in pages:
        pg.pop("_webAppDesc", None)

    out = ROOT / "src" / "pages.json"
    out.write_text(
        json.dumps(
            {
                "site": SITE,
                "keywords": kw.pop(),
                "webAppDesc": webapp_desc,
                "pages": pages,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"wrote {out.relative_to(ROOT)} — {len(pages)} pages")
    print(f'{"page":<34} {"dur":>4} {"mode":<10} {"nav":>3} {"crumbs":>6} {"h2":>3} {"faq":>3} {"webApp"}')
    for p in pages:
        tag = "定制" if p["webAppUrl"] != SITE + "/" else "通用"
        print(
            f'{p["file"]:<34} {p["dur"]:>4} {p["mode"]:<10} {len(p["nav"]):>3} '
            f'{len(p["crumbs"] or []):>6} {len(p["seo"]):>3} {len(p["faq"]):>3} {tag}'
        )


if __name__ == "__main__":
    main()
