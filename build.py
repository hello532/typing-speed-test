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

# Round-6 GEO：全站共享的 OG 图片 alt（单张通用封面，各页一致 → 不破坏骨架唯一）
OG_IMAGE_ALT = "Rerivo free online typing speed test — measure WPM and accuracy"

# Round-6 GEO：组织 / 站点实体（仅首页输出 Organization + WebSite，其余页空串）
ORG_OBJ = {"@context": "https://schema.org", "@type": "Organization",
           "name": "Rerivo", "url": SITE, "logo": SITE + "/icon-512.png"}
SITE_OBJ = {"@context": "https://schema.org", "@type": "WebSite",
            "name": "Rerivo Typing Speed Test", "url": SITE + "/"}


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
        on = sec == page["dur"]
        cls = "chip dur on" if on else "chip dur"
        out["{{CHIP_DUR_%d}}" % sec] = f'<button type="button" class="{cls}" data-d="{sec}" aria-pressed="{str(on).lower()}">{lab}</button>'
    for mode, lab, i18n in MODES:
        on = mode == page["mode"]
        cls = "chip mode on" if on else "chip mode"
        out["{{CHIP_MODE_%s}}" % mode.upper()] = (
            f'<button type="button" class="{cls}" data-m="{mode}" data-i18n="{i18n}" aria-pressed="{str(on).lower()}">{lab}</button>')
    return out


def build_seo(page):
    parts = ['<section class="seo">']
    for sec in page["seo"]:
        parts.append(f'    <h2>{sec["h2"]}</h2>')
        for p in sec["p"]:
            if p.lstrip().startswith(("<table", "<ul", "<ol", "<div", "<figure")):
                parts.append(f"    {p}")
            else:
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


def build_tldr(page):
    """Round-6 GEO：TL;DR 前置摘要（仅配置了 tldr 的页输出，其余空串）。

    落在 hero 区内，骨架归一整块剥除，不影响金标。内容须每页唯一。
    """
    t = (page.get("tldr") or "").strip()
    if not t:
        return ""
    return f'    <p class="tldr"><strong>TL;DR:</strong> {t}</p>'


def build_jsonld(page, cfg):
    pretty = set(page["ldPretty"])
    wa = {"@context": "https://schema.org", "@type": "WebApplication",
          "name": page["webAppName"], "url": page["webAppUrl"],
          **WEBAPP_CONST}
    # 字段顺序须与原文一致：name,url,applicationCategory,operatingSystem,description,offers,featureList
    wa = {"@context": wa["@context"], "@type": wa["@type"], "name": wa["name"], "url": wa["url"],
          "applicationCategory": wa["applicationCategory"], "operatingSystem": wa["operatingSystem"],
          "description": cfg["webAppDesc"], "offers": wa["offers"], "featureList": wa["featureList"],
          "datePublished": "2026-10-01", "dateModified": "2026-10-14"}
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
            ld_block(bc, "BreadcrumbList" in pretty),
            ld_block(ORG_OBJ, False) if page["file"] == "index.html" else "",
            ld_block(SITE_OBJ, False) if page["file"] == "index.html" else "")


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

    pat = r'var dur=\d+, mode="\w+", layout="\w+", VARIANT=null, VPOOL=null;/\*VAR_INIT\*/'
    lay = page.get("layout") or "qwerty"
    repl = (f'var dur={page["dur"]}, mode="{page["mode"]}", layout="{lay}", '
            f'VARIANT={vjson}, VPOOL={pjson};/*VAR_INIT*/')
    out, n = re.subn(pat, lambda m: repl, engine, count=1)
    if n == 0:
        sys.exit(f'{page["file"]}: VAR_INIT marker line not found in engine.js')
    return out


def render(page, cfg, tpl, css, engine, head_snippet, footer, result, variants, cluster):
    wa, faq, bc, org, site = build_jsonld(page, cfg)
    engine_page = inject_variant(page, engine, variants)
    hs = head_snippet
    pl = page.get("lang")
    if pl:
        hs = hs + "\nwindow.__trPageLang=" + json.dumps(pl) + ";"

    title = page["title"]
    desc = page["metaDesc"]
    # hreflang 聚类：只有 alts:true 的语种落地页互相声明 alternate（含 x-default），
    # 其余页渲染空串，与未加占位符时逐字节一致。
    if page.get("alts"):
        alt_lines = [f'<link rel="alternate" hreflang="{c}" href="{u}">' for c, u in cluster]
        default_url = next((u for c, u in cluster if c == "en"), None)
        if default_url:
            alt_lines.append(f'<link rel="alternate" hreflang="x-default" href="{default_url}">')
        hreflang = "\n" + "\n".join(alt_lines)
    else:
        hreflang = ""
    subs = {
        "{{TITLE}}": esc_attr(title),
        "{{META_DESC}}": esc_attr(desc),
        "{{KEYWORDS}}": esc_attr(cfg["keywords"]),
        "{{CANONICAL}}": page["canonical"],
        "{{HREFLANG}}": hreflang,
        "{{OG_TITLE}}": esc_attr(title),
        "{{OG_DESC}}": esc_attr(desc),
        "{{OG_URL}}": page["canonical"],
        "{{TW_TITLE}}": esc_attr(title),
        "{{TW_DESC}}": esc_attr(desc),
        "{{OG_ALT}}": esc_attr(OG_IMAGE_ALT),
        "{{TW_ALT}}": esc_attr(OG_IMAGE_ALT),
        "{{MD_URL}}": page["canonical"].replace(".html", ".md") if page["file"] != "index.html" else SITE + "/index.md",
        "{{TLDR}}": build_tldr(page),
        "{{LD_WEBAPP}}": wa, "{{LD_FAQ}}": faq, "{{LD_BREADCRUMB}}": bc,
        "{{LD_ORG}}": org, "{{LD_SITE}}": site,
        "{{CSS}}": css, "{{ENGINE}}": engine_page, "{{HEAD_SNIPPET}}": hs,
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


def build_ui_js():
    """生成 ui.js：src/ui.js 模板 + src/pools/*.json 五语练习池。

    ui.js 是外链脚本（不在 HTML 内联），17 页共享同一份。词池是真源，
    必须由 build 派生，否则根目录 ui.js 会与 src/ 漂移。
    """
    ui_tpl = (SRC / "ui.js").read_text(encoding="utf-8")
    pool = {}
    for lang in ("en", "zh", "es", "hi", "ar"):
        p = json.loads((SRC / "pools" / f"{lang}.json").read_text(encoding="utf-8"))
        for key in ("sentences", "quotes", "words"):
            if key not in p or not isinstance(p[key], list):
                sys.exit(f"src/pools/{lang}.json: 缺少 {key} 数组")
            if not p[key]:
                sys.exit(f"src/pools/{lang}.json: {key} 为空")
        pool[lang] = {k: p[k] for k in ("sentences", "quotes", "words")}
    pool_json = json.dumps(pool, ensure_ascii=False, separators=(",", ":"))
    out = ui_tpl.replace("var POOL=/*{{POOL}}*/;", "var POOL=" + pool_json + ";")
    if "/*{{POOL}}*/" in out:
        sys.exit("src/ui.js: POOL 占位符未被替换")
    return out


def _blocks(html_section: str) -> list[str]:
    """把 seo/faq 区块里的可引用内容抽成纯文本块。

    关键：`build_seo` 会把 <table>/<div class="tbl">/<ul>/<ol> 原样输出（不包 <p>），
    所以只匹配 <(h2|p)> 会**静默丢掉所有基准表与清单**——而这些恰恰是基准数据
    （WPM 分档、按年龄、按职业），是 AI 引擎最值得引用的部分。
    这里按 <h2> / <p> / 列表块 / 表格块 四类分别抽取，表格按行降级为可读文本。
    """
    def clean(s: str) -> str:
        s = re.sub(r"(?i)<br\s*/?>", " ", s)
        s = re.sub(r"</(?:td|th)>", " | ", s)
        s = re.sub(r"</(?:tr|li)>", "\n", s)
        s = re.sub(r"<[^>]+>", "", s)
        s = s.replace("&ndash;", "-").replace("&mdash;", "-")
        s = s.replace("&amp;", "&").replace("&nbsp;", " ")
        s = s.replace("&lt;", "<").replace("&gt;", ">")
        s = s.replace("&quot;", '"').replace("&#39;", "'")
        lines = [re.sub(r"[ \t]+", " ", ln).strip(" |\t") for ln in s.split("\n")]
        return "\n".join(ln for ln in lines if ln)

    out = []
    for tag, txt in re.findall(r"<(h2|p|ul|ol|table)>(.*?)</\1>", html_section, re.S):
        t = clean(txt)
        if not t:
            continue
        out.append(f"## {t}" if tag == "h2" else t)
    return out


def build_llms_full(cfg, htmls):
    """生成 llms-full.txt —— AI 抓取清单的「全文版」（GEO）。

    llms.txt = 只给链接与一句话摘要；llms-full.txt = 把每页的 H1 + 正文段落
    直接内联，AI 引擎无需二次抓取即可引用，提升被 AI Overview / Perplexity
    检索并引用的概率。与 llms.txt 一样是派生文件，由 build 生成，避免漂移。
    """
    parts = ["# Rerivo Typing Speed Test — Full Content",
             "",
             "> Free, no-signup online typing speed test. Below is the full readable text of every page,",
             "> for AI answer engines and retrieval systems. Source: https://typing.rerivo.com/",
             ""]
    for page in cfg["pages"]:
        url = page["canonical"]
        h = htmls.get(page["file"], "")
        seo = re.search(r'<section class="seo">(.*?)</section>', h, re.S)
        faq = re.search(r'<section class="seo faq">(.*?)</section>', h, re.S)
        body = []
        for blk in (seo, faq):
            if blk:
                body.extend(_blocks(blk.group(1)))
        parts.append(f"## {page['h1']}")
        parts.append(f"Source: {url}")
        parts.append("")
        parts.append(page["heroP"].replace("<strong>", "").replace("</strong>", ""))
        parts.append("")
        parts.extend(body)
        parts.append("")
    return "\n".join(parts).rstrip("\n") + "\n"


def build_md_mirrors(cfg, htmls):
    """生成各页的 Markdown 镜像 —— GEO（alternate text/markdown 目标）。

    内容 = H1 + heroP（去标签）+ SEO h2/p + FAQ Q/A，派生自产物 HTML
    （与 build_llms_full 同源：正则提取 → 去标签 → 空白归一），由 build 生成，
    main() 里与 llms-full.txt 同模式做 --check 漂移检测，避免手改漂移。
    文件名：<basename>.md（index.html → index.md），写到仓库根目录。
    """
    def clean(s):
        return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s)).strip()

    mirrors = {}
    for page in cfg["pages"]:
        h = htmls.get(page["file"], "")
        lines = ["# " + page["h1"], "", "Source: " + page["canonical"], ""]
        hero = clean(page["heroP"])
        if hero:
            lines += [hero, ""]
        seo = re.search(r'<section class="seo">(.*?)</section>', h, re.S)
        if seo:
            for blk in _blocks(seo.group(1)):
                if blk.startswith("## "):
                    lines += [blk, ""]
                else:
                    lines += [blk, ""]
        faq = re.search(r'<section class="seo faq">(.*?)</section>', h, re.S)
        fh2 = page.get("faqH2", "FAQ")
        pairs = []
        if faq:
            m2 = re.search(r"<h2>(.*?)</h2>", faq.group(1), re.S)
            if m2 and clean(m2.group(1)):
                fh2 = clean(m2.group(1))
            raw = re.findall(r"<summary>(.*?)</summary>\s*<p>(.*?)</p>", faq.group(1), re.S)
            pairs = [(clean(q), clean(a)) for q, a in raw]
            pairs = [(q, a) for q, a in pairs if q or a]
        if not pairs:  # 兜底：产物正则未命中时回落配置原文（渲染系逐字替换，正常应一致）
            pairs = [(clean(f["q"]), clean(f["a"])) for f in page.get("faq", [])]
        if pairs:
            lines += [f"## {fh2}", ""]
            for q, a in pairs:
                lines += [f"### {q}", "", a, ""]
        name = Path(page["file"]).with_suffix(".md").name
        mirrors[name] = "\n".join(lines).rstrip("\n") + "\n"
    return mirrors


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
    cluster = [(p["lang"], p["canonical"]) for p in cfg["pages"]
               if p.get("alts") and p.get("lang")]
    ui_js = build_ui_js()
    bad = []
    ui_target = ROOT / "ui.js"
    if check:
        cur_ui = ui_target.read_text(encoding="utf-8") if ui_target.exists() else None
        if cur_ui != ui_js:
            bad.append("ui.js")
    else:
        ui_target.write_text(ui_js, encoding="utf-8")

    htmls = {}
    for page in cfg["pages"]:
        html = render(page, cfg, tpl, css, engine, head_snippet, footer, result, variants, cluster)
        htmls[page["file"]] = html
        target = ROOT / page["file"]
        if check:
            cur = target.read_text(encoding="utf-8") if target.exists() else None
            if cur != html:
                bad.append(page["file"])
        else:
            target.write_text(html, encoding="utf-8")

    # llms-full.txt（GEO 全文版）：派生自产物，AI 引擎可直接引用，无需二次抓取
    full = build_llms_full(cfg, htmls)
    ftarget = ROOT / "llms-full.txt"
    if check:
        cur = ftarget.read_text(encoding="utf-8") if ftarget.exists() else None
        if cur != full:
            bad.append("llms-full.txt")
    else:
        ftarget.write_text(full, encoding="utf-8")

    # .md 镜像（GEO alternate text/markdown 目标）：派生自产物 HTML，与 llms-full.txt 同模式漂移检测
    mirrors = build_md_mirrors(cfg, htmls)
    for name, body in mirrors.items():
        mtarget = ROOT / name
        if check:
            cur = mtarget.read_text(encoding="utf-8") if mtarget.exists() else None
            if cur != body:
                bad.append(name)
        else:
            mtarget.write_text(body, encoding="utf-8")

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
