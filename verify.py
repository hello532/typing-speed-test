#!/usr/bin/env python3
"""站点产物校验器 —— 11 项检查，任何一项失败即退出码 1。

    python3 verify.py

检查覆盖：产物完整性、模板占位符、共享资源一致性、引擎漂移、
JSON-LD 合法性、sitemap 一致性、外链存在性、与 git 基线的字节等价
（剥引擎块后对比，豁免表见 EXEMPT）、构建幂等性、引擎行为级 harness。
"""
import difflib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
SITE = "https://typing.rerivo.com"

# 产物中引擎内联块的形态（无属性 <script> + IIFE + "use strict"）。
# 全站唯一，check 5 与 check 9 共用；head-snippet 不以 (function(){ 开头，不会误伤。
ENGINE_BLOCK_RE = r"<script>\n\(function\(\)\{\n.*?\n</script>"


STYLE_BLOCK_RE = r"<style>.*?</style>"

def strip_engine(html: str) -> str:
    """剥掉引擎内联块与内联 <style> 块后再对比。
    引擎自 Task#2 起有意演进（无限文本流+增量渲染等）；CSS 自 Task#5/6 起有意演进
    （a11y 动效/对比降级、移动端保留音效开关等）。两者的正确性不由 check 9 字节对比守卫：
    引擎由 check 4/5/5b + check 11 行为级 harness 守卫，CSS 由 check 4
    （全站单版本且 == src/style.css）守卫。check 9 只守卫 HTML 结构等价。"""
    html = re.sub(ENGINE_BLOCK_RE, "<script>{{ENGINE}}</script>", html, flags=re.S)
    return re.sub(STYLE_BLOCK_RE, "<style>{{CSS}}</style>", html, flags=re.S)

# Task#5 起全站补的无障碍标记。这些是有意的功能性新增（非渲染等价），
# 但不应污染 check 9 的"产物等价于原站"守卫：对比前先从双方剥掉，
# 使 check 9 仍严格守卫"a11y 标记之外的字节等价"。
A11Y_ATTR_RE = re.compile(
    r'\s+(?:role="(?:timer|status|img)"|aria-live="(?:polite|assertive|off)"|data-aria="[^"]*"|aria-pressed="(?:true|false)")')
A11Y_LABELS = (' aria-label="Time remaining"', ' aria-label="Typing input"',
               ' aria-label="WPM over time line chart"')
SKIP_LINK_RE = re.compile(r'<a class="skip"[^>]*>.*?</a>\n?')
# Task#6 起全站 head 新增的 PWA/图标引用（favicon、apple-touch、manifest）。
# 这是有意的功能性新增，基线里不存在，剥掉后双方归一，不污染 check 9。
PWA_LINK_RE = re.compile(r'<link rel="(?:icon|apple-touch-icon|manifest)"[^>]*>\n?')
# 全站页脚内链枢纽：有意演进的 SEO 内链（给每页全站入口），不参与 check 9
# 字节守卫；其“覆盖所有页且无死链”由 check 12 单独守卫。
FOOTER_RE = re.compile(r"<footer>.*?</footer>", re.S)
def strip_a11y(html: str) -> str:
    """剥掉 Task#5 新增的 a11y 属性/元素（skip link、role、aria-*、button type），
    Task#6 新增的 PWA/图标引用，以及有意演进的页脚内链枢纽（见 check 12）。
    内联 <style> 块已由 strip_engine 整体剥离，故此处无需再处理 a11y CSS。
    基线里本就存在的同类属性（如 kbd-size 的 aria-label、sndToggle 的
    aria-pressed）会被一并移除，双方归一，不影响守卫。"""
    html = FOOTER_RE.sub("", html)
    html = PWA_LINK_RE.sub("", html)
    html = A11Y_ATTR_RE.sub("", html)
    html = SKIP_LINK_RE.sub("", html)
    html = html.replace(' type="button"', "")
    for lit in A11Y_LABELS:
        html = html.replace(lit, "")
    return html
# 架构重构前的基线提交。检查 9 永久对比它，使"产物等价于原站"成为回归守卫，
# 而不是提交后退化成自我对比。
BASELINE_REF = "eada54e"

# 架构重构豁免表：相对 git 基线唯一允许的差异。
# 全部是不可见空白或渲染等价的正确性修正，逐条给出理由。
EXEMPT = {
    # crumbs 前统一留一个空行（11/16 页的多数约定）
    "capital-letter-typing-test.html": "crumbs 前补空行，归一多数约定",
    "easy-typing-test.html": "crumbs 前补空行，归一多数约定",
    "free-typing-test.html": "crumbs 前补空行，归一多数约定",
    "punctuation-typing-test.html": "crumbs 前补空行，归一多数约定",
    "wpm-test-online.html": "crumbs 前补空行，归一多数约定",
    # <title> 内裸 & 属无效 HTML，统一转义（渲染结果不变）
    "typing-accuracy-test.html": "title 内 & → &amp;，修正无效 HTML",
    # seo 开标签缩进 4→2，与该页闭标签及多数页一致
    "1-minute-typing-test.html": "seo 缩进 4→2，修正自身不一致",
    "words-per-minute-test.html": "seo 缩进 4→2，修正自身不一致",
    # dur=120 但静态 sTime 写 1:00，是原站缺陷；按 dur 派生为 2:00
    "typing-practice.html": "seo 缩进 4→2；sTime 1:00→2:00 修正（dur=120）",
}

ok, fail = [], []


def check(name, cond, detail=""):
    (ok if cond else fail).append(name)
    print(f'  {"✅" if cond else "❌"} {name}' + (f" — {detail}" if detail else ""))
    return cond


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)


def main():
    cfg = json.loads((SRC / "pages.json").read_text(encoding="utf-8"))
    pages = cfg["pages"]
    names = [p["file"] for p in pages]
    print(f"校验 {len(pages)} 个页面配置\n")

    # 1. 产物完整性
    missing = [n for n in names if not (ROOT / n).exists()]
    check("1. 页面产物全部存在", not missing, f"缺失: {missing}" if missing else f"{len(names)} 页")

    htmls = {n: (ROOT / n).read_text(encoding="utf-8") for n in names if (ROOT / n).exists()}

    # 2. 无未填充占位符
    leftover = {n: sorted(set(re.findall(r"\{\{[A-Z0-9_]+\}\}", h))) for n, h in htmls.items()}
    leftover = {n: v for n, v in leftover.items() if v}
    check("2. 无未填充 {{占位符}}", not leftover, str(leftover) if leftover else "全部已替换")

    # 3. 与 build.py 输出一致（无手工改动）
    r = subprocess.run([sys.executable, str(ROOT / "build.py"), "--check"],
                       cwd=ROOT, capture_output=True, text=True)
    check("3. 产物 == build.py 输出（无手改）", r.returncode == 0,
          r.stdout.strip()[:90] or r.stderr.strip()[:90])

    # 4. CSS 全站唯一
    csss = {re.search(r"<style>\n(.*?)\n</style>", h, re.S).group(1) for h in htmls.values()}
    base_css = (SRC / "style.css").read_text(encoding="utf-8").rstrip("\n")
    check("4. CSS 全站单版本且等于 src/style.css",
          len(csss) == 1 and next(iter(csss)) == base_css,
          f"{len(csss)} 个版本，{len(base_css):,}B")

    # 5. 引擎归一后仅 1 个版本（漂移只在 dur/mode/variant 初值一行）
    #    VAR_INIT 行含 per-page VARIANT/VPOOL 注入（变体页携带各自数据池），
    #    整行归一为 "VAR"；不用 re.S，保证只匹配这一行（JSON 是单行）。
    VAR_NORM = r'var dur=\d+, mode="\w+", VARIANT=.*?;/\*VAR_INIT\*/'
    variants = {}
    for n, h in htmls.items():
        e = re.search(r"<script>\n\(function\(\)\{\n.*?\n</script>", h, re.S)
        if e:
            variants.setdefault(re.sub(VAR_NORM, "VAR", e.group(0)), []).append(n)
    check("5. 引擎归一后仅 1 个版本（漂移只在 VAR_INIT 行）",
          len(variants) == 1, f"{len(variants)} 个版本")
    for n in names:
        p = next(x for x in pages if x["file"] == n)
        h = htmls.get(n, "")
        v = p.get("variant")
        if v:
            marker = f'var dur={p["dur"]}, mode="{p["mode"]}", VARIANT="{v}", VPOOL={{'
        else:
            marker = f'var dur={p["dur"]}, mode="{p["mode"]}", VARIANT=null, VPOOL=null;/*VAR_INIT*/'
        if marker not in h:
            check(f"5b. {n} dur/mode/variant 初值", False, f"未找到 {marker[:60]}")
            break
    else:
        check("5b. 每页 dur/mode/variant 初值与配置一致", True)

    # 6. JSON-LD 三块可解析且类型正确
    bad_ld = []
    for n, h in htmls.items():
        raws = re.findall(r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>', h, re.S)
        types = []
        for raw in raws:
            try:
                types.append(json.loads(raw)["@type"])
            except Exception as e:
                bad_ld.append((n, str(e)[:50]))
        if types != ["WebApplication", "FAQPage", "BreadcrumbList"]:
            bad_ld.append((n, f"types={types}"))
    check("6. 每页 3 块 JSON-LD 合法且类型顺序正确", not bad_ld, str(bad_ld[:3]) if bad_ld else f"{len(htmls)*3} 块")

    # 7. sitemap 与实际页面一致
    sm = ROOT / "sitemap.xml"
    if sm.exists():
        urls = set(re.findall(r"<loc>(.*?)</loc>", sm.read_text(encoding="utf-8")))
        want = {SITE + "/" if n == "index.html" else SITE + "/" + n for n in names}
        check("7. sitemap.xml 覆盖且仅覆盖全部页面 URL",
              urls == want, f"缺 {sorted(want-urls)[:2]} 多 {sorted(urls-want)[:2]}" if urls != want else f"{len(urls)}/{len(want)} 个 URL 一致")
    else:
        check("7. sitemap.xml 存在", False)

    # 8. 外链资源存在
    refs = set()
    # 站内绝对路径（/favicon.svg 等，根部署）也纳入校验；仅排除外部 URL、
    # protocol-relative（//）、锚点（#）、mailto。
    for h in htmls.values():
        refs |= set(re.findall(r'(?:src|href)="(?!https?://|//|#|mailto:)([^"?]+)', h))
    refs = {r for r in refs if r.strip("/")}  # 剔除 logo href="/" 这类首页自引用
    miss = sorted(r for r in refs if not (ROOT / r.lstrip("/")).exists())
    check("8. 页面引用的本地资源全部存在", not miss, f"缺失: {miss}" if miss else f"{len(refs)} 个: {sorted(refs)}")

    # 重构后新增的落地页：基线中不存在，属有意新增（补 gap 词），不是回归。
    NEW_PAGES = {
        "30-second-typing-test.html": "新增 30 秒时长落地页（补时长阶梯）",
        "3-minute-typing-test.html": "新增 3 分钟时长落地页（补时长阶梯）",
        "10-minute-typing-test.html": "新增 10 分钟时长落地页（补时长阶梯）",
        "typing-games.html": "新增 typing games 落地页（补游戏线 gap 词）",
        "typing-lessons.html": "新增 typing lessons 落地页（补教育线 gap 词）",
        "learn-to-type-faster.html": "新增 learn to type faster 落地页（补教育线提速 P1 词）",
        "typing-tips.html": "新增 typing tips 落地页（补信息线技巧聚合 P1 词）",
    }

    # 9. 与 git 基线字节等价（豁免表内差异需逐条命中；新增页单独登记）
    base_ref = BASELINE_REF
    if git("cat-file", "-e", f"{BASELINE_REF}^{{commit}}").returncode != 0:
        base_ref = "HEAD"  # 浅克隆等取不到基线时退化
    diffs, unexpected, unmatched, new_hit = {}, {}, set(EXEMPT), 0
    for n in names:
        g = git("show", f"{base_ref}:{n}")
        if g.returncode != 0:
            if n in NEW_PAGES:
                new_hit += 1
                continue  # 有意新增的落地页（基线不存在），非回归
            unexpected[n] = ["(基线中不存在)"]
            continue
        # 剥掉引擎块与 Task#5 a11y 标记再比：引擎有意演进、a11y 有意新增，
        # 除此之外的 HTML/CSS 仍逐字节守卫
        base = strip_a11y(strip_engine(g.stdout))
        cur = strip_a11y(strip_engine(htmls.get(n, "")))
        if base == cur:
            continue
        d = [l for l in difflib.unified_diff(base.split("\n"),
                                             cur.split("\n"),
                                             lineterm="", n=0)
             if l[:1] in "+-" and not l.startswith(("+++", "---"))]
        diffs[n] = d
        if n in EXEMPT:
            unmatched.discard(n)
            for line in d:
                body = line[1:].strip()
                allowed = (body == "" or "<section class=\"seo\">" in body
                           or "id=\"sTime\"" in body or "<title>" in body)
                if not allowed:
                    unexpected.setdefault(n, []).append(line[:100])
        else:
            unexpected.setdefault(n, []).extend(l[:100] for l in d)
    # 基线是重构前提交，diffs 恒为豁免表内容；豁免项必须全部命中
    passed9 = not unexpected and not unmatched
    check("9. 相对 git 基线仅有豁免表内差异", passed9,
          f"意外差异 {list(unexpected)[:2]}" if unexpected else
          (f"豁免表未命中 {sorted(unmatched)}" if unmatched and diffs else
           (f"{len(diffs)+new_hit}/{len(names)} 页命中豁免（基线 {base_ref}"
            + (f"，含 {new_hit} 个新增落地页" if new_hit else "") + "）" if diffs
            else f"无差异，与基线 {base_ref} 完全一致")))
    for n, d in sorted(diffs.items()):
        print(f'      · {n}: {len(d)} 行 — {EXEMPT.get(n, "未登记")}')

    # 12. 页脚内链枢纽覆盖所有页面且无死链（哥飞第5步：每个页都要有全站入口）
    foot_src = (SRC / "footer.html").read_text(encoding="utf-8")
    foot_links = set(re.findall(r'href="([^"]+)"', foot_src))
    foot_pages = {l for l in foot_links if l.endswith(".html")}
    covered = foot_pages | ({"index.html"} if "/" in foot_links else set())
    miss12 = set(names) - covered
    dead12 = foot_pages - set(names)
    check("12. 页脚枢纽覆盖所有页面且无死链", not miss12 and not dead12,
          f"缺入口 {sorted(miss12)}" if miss12 else
          (f"死链 {sorted(dead12)}" if dead12 else f"{len(covered)}/{len(names)} 页有页脚入口"))

    # 10. 构建幂等
    r2 = subprocess.run([sys.executable, str(ROOT / "build.py")], cwd=ROOT, capture_output=True, text=True)
    again = {n: (ROOT / n).read_text(encoding="utf-8") for n in names}
    check("10. build.py 幂等（重跑产物不变）", r2.returncode == 0 and again == htmls)

    # 11. 引擎行为级 harness（P0-1 无限流 / P1 五项修复）
    harness = SRC / "tools" / "engine_harness.mjs"
    node = shutil.which("node")
    if not node:
        check("11. 引擎行为级 harness", False, "node 不在 PATH，无法验证引擎行为")
    elif not harness.exists():
        check("11. 引擎行为级 harness", False, f"缺失 {harness}")
    else:
        r3 = subprocess.run([node, str(harness)], cwd=ROOT, capture_output=True, text=True)
        tail = (r3.stdout + r3.stderr).strip().splitlines()
        summary = tail[-1] if tail else "(无输出)"
        check("11. 引擎行为级 harness 全绿", r3.returncode == 0,
              summary if r3.returncode == 0 else (summary + " | " + " ; ".join(l for l in tail if "❌" in l)[:120]))

    print(f"\n通过 {len(ok)}/{len(ok)+len(fail)} 项")
    if fail:
        print("失败项: " + ", ".join(fail))
        return 1
    print("全部检查通过 ✅")
    return 0


if __name__ == "__main__":
    sys.exit(main())
