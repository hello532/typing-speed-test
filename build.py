#!/usr/bin/env python3
"""Typing.Rerivo 站点生成器 —— 单一模板 + 配置表 → 17 个页面。

    python3 build.py          # 生成全部页面到仓库根目录
    python3 build.py --check  # 只校验，不写入（CI 用）

设计约束：
  * 仅用 Python 标准库（无 npm/pip 依赖）。
  * CSS/JS 仍内联进 HTML（保持零请求首屏）。
  * src/ 是唯一真源；根目录 *.html 全部是产物，不要手改。
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
SITE = "https://typing.rerivo.com"
LD = '<script type="application/ld+json">'

# 面板时长/文本模式按钮的显示文案与顺序（与 ui.js 的 data-d/data-m 契约一致）
DURATIONS = [(15, "15s"), (30, "30s"), (60, "1 min"), (120, "2 min"),
             (180, "3 min"), (300, "5 min"), (600, "10 min")]
MODES = [("sentences", "Sentences", "m_sentences"), ("quotes", "Quotes", "m_quotes"),
         ("numbers", "Numbers", "m_numbers"), ("words", "Words", "m_words")]

# WebApplication 结构化数据的恒定部分（17 页一致）
WEBAPP_CONST = {
    "applicationCategory": "UtilitiesGame",
    "operatingSystem": "All",
    "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
    "featureList": ["WPM speed test", "Accuracy tracking", "15s to 10 minute tests",
                    "Sentences, quotes, numbers and words practice", "Local typing history"],
}


def esc_attr(s):
    """属性值转义：& → &amp;（原文 <title> 保留裸 &，故 title 不走这里）。"""
    return s.replace("&", "&amp;")


def fmt_dur(sec):
    """面板 sTime 初值，与 ui.js 的 fmtDur 同规则。"""
    return f"{sec // 60}:{sec % 60:02d}"


def ld_block(obj, pretty):
    """按原文格式输出一个 JSON-LD 块（pretty=False → 压缩，True → 默认分隔符）。"""
    sep = (", ", ": ") if pretty else (",", ":")
    body = json.dumps(obj, separators=sep, ensure_ascii=False)
    return f"{LD}\n{body}\n</script>"


def build_header(page):
    """导航 = 用户配置里的链接原样输出（保留各页 Home 变体）。"""
    links = "\n".join(f'      <a href="{n["href"]}">{n["text"]}</a>' for n in page["nav"])
    return (f'<header class="top">\n'
            f'    <a class="logo" href="/">Typing.Rerivo</a>\n'
            f'    <nav class="toplinks">\n{links}\n    </nav>\n'
            f'  </header>')


def build_crumbs(page):
    """面包屑；index 无（返回空串正好还原原文空行）。\n\n    前后各一个空行是 17 页里的多数约定（11 页），生成时统一归一。\n    """
    if not page["crumbs"]:
        return ""
    home, name = page["crumbs"][0], page["crumbs"][1]
    return (f'\n  <nav class="crumbs" aria-label="Breadcrumb">'
            f'<a href="/">{home}</a> <span>&rsaquo;</span> <span>{name}</span></nav>\n')


def build_chips(page):
    """时长/模式按钮：高亮态由 dur/mode 派生。"""
    out = {}
    for sec, lab in DURATIONS:
        cls = "chip dur on" if sec == page["dur"] else "chip dur"
        out["{{CHIP_DUR_%d}}" % sec] = f'<button class="{cls}" data-d="{sec}">{lab}</button>'
    for mode, lab, i18n in MODES:
        cls = "chip mode on" if mode == page["mode"] else "chip mode"
        out["{{CHIP_MODE_%s}}" % mode.upper()] = (
            f'<button class="{cls}" data-m="{mode}" data-i18n="{i18n}">{lab}</button>')
    return out


def build_seo(page):
    parts = ['<section class="seo">']
    for sec in page["seo"]:
        parts.append(f'    <h2>{sec["h2"]}</h2>')
        for p in sec["p"]:
            parts.append(f"    <p>{p}</p>")
    parts.append("  </section>")
    return "\n".join(parts)


def build_faq(page):
    parts = ['<section class="seo faq">', f'    <h2>{page["faqH2"]}</h2>']
    for i, fa in enumerate(page["faq"]):
        op = " open" if (i == 0 and page["faqFirstOpen"]) else ""
        parts.append(f'    <details{op}><summary>{fa["q"]}</summary><p>{fa["a"]}</p></details>')
    parts.append("  </section>")
    return "\n".join(parts)


def build_jsonld(page, cfg):
    pretty = set(page["ldPretty"])
    wa = {"@context": "https://schema.org", "@type": "WebApplication",
          "name": page["webAppName"], "url": page["webAppUrl"],
          **WEBAPP_CONST}
    # 字段顺序须与原文一致：name,url,applicationCategory,operatingSystem,description,offers,featureList
    wa = {"@context": wa["@context"], "@type": wa["@type"], "name": wa["name"], "url": wa["url"],
          "applicationCategory": wa["applicationCategory"], "operatingSystem": wa["operatingSystem"],
          "description": cfg["webAppDesc"], "offers": wa["offers"], "featureList": wa["featureList"]}
    faq = {"@context": "https://schema.org", "@type": "FAQPage",
           "mainEntity": [{"@type": "Question", "name": f["q"],
                           "acceptedAnswer": {"@type": "Answer", "text": f["a"]}}
                          for f in page["faq"]]}
    bc = {"@context": "https://schema.org", "@type": "BreadcrumbList",
          "itemListElement": [{"@type": "ListItem", "position": i + 1,
                               "name": it["name"], "item": it["item"]}
                              for i, it in enumerate(page["bcItems"])]}
    return (ld_block(wa, "WebApplication" in pretty),
            ld_block(faq, "FAQPage" in pretty),
            ld_block(bc, "BreadcrumbList" in pretty))


def inject_variant(page, engine, variants):
    r"""把 engine.js 源码里的 VAR_INIT 标记行替换成本页的 dur/mode/VARIANT/VPOOL。

    普通页 VARIANT=null, VPOOL=null；变体页注入变体名与该变体的数据池（含 css）。
    数据只落在需要它的那一页，零冗余。用 lambda 作 repl，避免 JSON 里的反斜杠
    被 re.sub 当成反向引用（\g / \1）解释。
    """
    vname = page.get("variant")
    if vname:
        if vname not in variants:
            sys.exit(f'{page["file"]}: unknown variant "{vname}" (not in src/variants.json)')
        pool = {k: v for k, v in variants[vname].items() if not k.startswith("_")}
        vjson = json.dumps(vname)
        pjson = json.dumps(pool, separators=(",", ":"), ensure_ascii=False)
    else:
        vjson, pjson = "null", "null"

    pat = r'var dur=\d+, mode="\w+", VARIANT=null, VPOOL=null;/\*VAR_INIT\*/'
    repl = (f'var dur={page["dur"]}, mode="{page["mode"]}", '
            f'VARIANT={vjson}, VPOOL={pjson};/*VAR_INIT*/')
    out, n = re.subn(pat, lambda m: repl, engine, count=1)
    if n == 0:
        sys.exit(f'{page["file"]}: VAR_INIT marker line not found in engine.js')
    return out


def render(page, cfg, tpl, css, engine, head_snippet, footer, result, variants):
    wa, faq, bc = build_jsonld(page, cfg)
    engine_page = inject_variant(page, engine, variants)

    title = page["title"]
    desc = page["metaDesc"]
    subs = {
        "{{TITLE}}": esc_attr(title),
        "{{META_DESC}}": esc_attr(desc),
        "{{KEYWORDS}}": esc_attr(cfg["keywords"]),
        "{{CANONICAL}}": page["canonical"],
        "{{OG_TITLE}}": esc_attr(title),
        "{{OG_DESC}}": esc_attr(desc),
        "{{OG_URL}}": page["canonical"],
        "{{TW_TITLE}}": esc_attr(title),
        "{{TW_DESC}}": esc_attr(desc),
        "{{LD_WEBAPP}}": wa, "{{LD_FAQ}}": faq, "{{LD_BREADCRUMB}}": bc,
        "{{CSS}}": css, "{{ENGINE}}": engine_page, "{{HEAD_SNIPPET}}": head_snippet,
        "{{FOOTER}}": footer, "{{RESULT}}": result,
        "{{HEADER}}": build_header(page), "{{CRUMBS}}": build_crumbs(page),
        "{{H1}}": page["h1"], "{{HERO_P}}": page["heroP"],
        "{{SEO}}": build_seo(page), "{{FAQ}}": build_faq(page),
        "{{STIME}}": fmt_dur(page["dur"]),
        **build_chips(page),
    }
    out = tpl
    for k, v in subs.items():
        out = out.replace(k, v)
    left = sorted(set(re.findall(r"\{\{[A-Z0-9_]+\}\}", out)))
    if left:
        sys.exit(f'{page["file"]}: unfilled placeholders {left}')
    return out


def main():
    check = "--check" in sys.argv
    cfg = json.loads((SRC / "pages.json").read_text(encoding="utf-8"))
    tpl = (SRC / "template.html").read_text(encoding="utf-8")
    css = (SRC / "style.css").read_text(encoding="utf-8").rstrip("\n")
    engine = (SRC / "engine.js").read_text(encoding="utf-8").rstrip("\n")
    head_snippet = (SRC / "head-snippet.js").read_text(encoding="utf-8").rstrip("\n")
    footer = (SRC / "footer.html").read_text(encoding="utf-8").rstrip("\n")
    result = (SRC / "result.html").read_text(encoding="utf-8").rstrip("\n")
    variants = json.loads((SRC / "variants.json").read_text(encoding="utf-8"))

    bad = []
    for page in cfg["pages"]:
        html = render(page, cfg, tpl, css, engine, head_snippet, footer, result, variants)
        target = ROOT / page["file"]
        if check:
            cur = target.read_text(encoding="utf-8") if target.exists() else None
            if cur != html:
                bad.append(page["file"])
        else:
            target.write_text(html, encoding="utf-8")
    if check:
        if bad:
            print(f"DRIFT: {len(bad)} page(s) differ from src/ → run build.py")
            for f in bad:
                print("  ", f)
            sys.exit(1)
        print(f"OK: all {len(cfg['pages'])} pages match src/")
    else:
        print(f"built {len(cfg['pages'])} pages from src/")


if __name__ == "__main__":
    main()
