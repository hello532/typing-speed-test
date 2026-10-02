#!/usr/bin/env python3
"""站点产物校验器 —— 10 项检查，任何一项失败即退出码 1。

    python3 verify.py

检查覆盖：产物完整性、模板占位符、共享资源一致性、引擎漂移、
JSON-LD 合法性、sitemap 一致性、外链存在性、与 git 基线的字节等价
（豁免表见 EXEMPT）、构建幂等性、无重复内联块。
"""
import difflib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
SITE = "https://typing.rerivo.com"

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
    check("1. 17 个页面产物全部存在", not missing, f"缺失: {missing}" if missing else f"{len(names)} 页")

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

    # 5. 引擎仅 dur/mode 初值一行漂移
    variants = {}
    for n, h in htmls.items():
        e = re.search(r"<script>\n\(function\(\)\{\n.*?\n</script>", h, re.S)
        if e:
            variants.setdefault(re.sub(r'var dur=\d+, mode="\w+"', "VAR", e.group(0)), []).append(n)
    check("5. 引擎归一后仅 1 个版本（漂移只在 dur/mode）",
          len(variants) == 1, f"{len(variants)} 个版本")
    for n in names:
        p = next(x for x in pages if x["file"] == n)
        h = htmls.get(n, "")
        want = f'var dur={p["dur"]}, mode="{p["mode"]}"'
        if want not in h:
            check(f"5b. {n} dur/mode 初值", False, f"未找到 {want}")
            break
    else:
        check("5b. 每页 dur/mode 初值与配置一致", True)

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
        check("7. sitemap.xml 覆盖且仅覆盖这 17 个 URL",
              urls == want, f"缺 {sorted(want-urls)[:2]} 多 {sorted(urls-want)[:2]}" if urls != want else "17/17")
    else:
        check("7. sitemap.xml 存在", False)

    # 8. 外链资源存在
    refs = set()
    for h in htmls.values():
        refs |= set(re.findall(r'(?:src|href)="((?!https?://|/|#|mailto:)[^"?]+)', h))
    miss = sorted(r for r in refs if not (ROOT / r).exists())
    check("8. 页面引用的本地资源全部存在", not miss, f"缺失: {miss}" if miss else f"{len(refs)} 个: {sorted(refs)}")

    # 9. 与 git 基线字节等价（豁免表内差异需逐条命中）
    base_ref = git("rev-parse", "HEAD").stdout.strip()[:7]
    diffs, unexpected, unmatched = {}, {}, set(EXEMPT)
    for n in names:
        g = git("show", f"HEAD:{n}")
        if g.returncode != 0:
            unexpected[n] = ["(基线中不存在)"]
            continue
        if g.stdout == htmls.get(n):
            continue
        d = [l for l in difflib.unified_diff(g.stdout.split("\n"), htmls[n].split("\n"),
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
    # 提交后 HEAD == 产物，diffs 为空，豁免表自然满足（它是本次重构的一次性审计记录）
    passed9 = not unexpected and (not diffs or not unmatched)
    check("9. 相对 git 基线仅有豁免表内差异", passed9,
          f"意外差异 {list(unexpected)[:2]}" if unexpected else
          (f"豁免表未命中 {sorted(unmatched)}" if unmatched and diffs else
           (f"{len(diffs)}/{len(names)} 页命中豁免（基线 {base_ref}）" if diffs
            else f"无差异，与基线 {base_ref} 完全一致")))
    for n, d in sorted(diffs.items()):
        print(f'      · {n}: {len(d)} 行 — {EXEMPT.get(n, "未登记")}')

    # 10. 构建幂等
    r2 = subprocess.run([sys.executable, str(ROOT / "build.py")], cwd=ROOT, capture_output=True, text=True)
    again = {n: (ROOT / n).read_text(encoding="utf-8") for n in names}
    check("10. build.py 幂等（重跑产物不变）", r2.returncode == 0 and again == htmls)

    print(f"\n通过 {len(ok)}/{len(ok)+len(fail)} 项")
    if fail:
        print("失败项: " + ", ".join(fail))
        return 1
    print("全部检查通过 ✅")
    return 0


if __name__ == "__main__":
    sys.exit(main())
