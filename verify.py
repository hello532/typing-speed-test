#!/usr/bin/env python3
"""站点产物校验器 —— 任何一项失败即退出码 1。

    python3 verify.py

检查覆盖：产物完整性、模板占位符、共享资源一致性、引擎漂移、
JSON-LD 合法性、sitemap 一致性、llms.txt（AI 发现清单）一致性、
外链存在性、结构等价（委托 structure_gate：骨架归一 + 金标锁）、
页脚内链覆盖、构建幂等性、引擎与多语页默认语言的行为级 harness。
"""
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
SITE = "https://typing.rerivo.com"

# ── 结构等价守卫：委托 src/tools/structure_gate.py（骨架归一 + 金标锁）──
# 旧方案（EXEMPT 逐条豁免 + 逐功能 strip 正则 + 冻结基线字节 diff）已废弃：
# 它要求每新增一个功能块/页面就手工改验证器，豁免表会无限膨胀。
# 新方案见 src/tools/skeleton.py 的槽位定义与 structure_gate.py 的 S1/S1a/S2/S3。
STRUCTURE_GATE = SRC / "tools" / "structure_gate.py"

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
    VAR_NORM = r'var dur=\d+, mode="\w+", layout="\w+", VARIANT=.*?;/\*VAR_INIT\*/'
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
            marker = f'var dur={p["dur"]}, mode="{p["mode"]}", layout="{p.get("layout") or "qwerty"}", VARIANT="{v}", VPOOL={{'
        else:
            marker = f'var dur={p["dur"]}, mode="{p["mode"]}", layout="{p.get("layout") or "qwerty"}", VARIANT=null, VPOOL=null;/*VAR_INIT*/'
        if marker not in h:
            check(f"5b. {n} dur/mode/variant 初值", False, f"未找到 {marker[:60]}")
            break
    else:
        check("5b. 每页 dur/mode/variant 初值与配置一致", True)

    # 6. JSON-LD 可解析且类型正确（Round-6：首页 + Organization/WebSite）
    bad_ld = []
    for n, h in htmls.items():
        raws = re.findall(r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>', h, re.S)
        types = []
        for raw in raws:
            try:
                types.append(json.loads(raw)["@type"])
            except Exception as e:
                bad_ld.append((n, str(e)[:50]))
        want_types = (["WebApplication", "FAQPage", "BreadcrumbList", "Organization", "WebSite"]
                      if n == "index.html" else ["WebApplication", "FAQPage", "BreadcrumbList"])
        if types != want_types:
            bad_ld.append((n, f"types={types}"))
    check("6. 每页 JSON-LD 合法且类型顺序正确（首页 5 块含 Org/Site）", not bad_ld, str(bad_ld[:3]) if bad_ld else f"{len(htmls)*3+2} 块")

    # 7. sitemap 与实际页面一致
    sm = ROOT / "sitemap.xml"
    if sm.exists():
        urls = set(re.findall(r"<loc>(.*?)</loc>", sm.read_text(encoding="utf-8")))
        want = {SITE + "/" if n == "index.html" else SITE + "/" + n for n in names}
        check("7. sitemap.xml 覆盖且仅覆盖全部页面 URL",
              urls == want, f"缺 {sorted(want-urls)[:2]} 多 {sorted(urls-want)[:2]}" if urls != want else f"{len(urls)}/{len(want)} 个 URL 一致")
    else:
        check("7. sitemap.xml 存在", False)

    # 13. llms.txt 覆盖且仅覆盖全部页面 URL（AI 爬虫发现清单）
    # llms.txt 是手工维护的（build.py 不生成它），每加一页必须手写登记，
    # 否则 AI 收录会静默漏页——本 check 正为堵这个缺口而加。
    lt = ROOT / "llms.txt"
    if lt.exists():
        lurls = set(re.findall(r"\]\((https?://[^\)]+)\)", lt.read_text(encoding="utf-8")))
        lwant = {SITE + "/" if n == "index.html" else SITE + "/" + n for n in names}
        check("13. llms.txt 覆盖且仅覆盖全部页面 URL",
              lurls == lwant, f"缺 {sorted(lwant-lurls)[:2]} 多 {sorted(lurls-lwant)[:2]}" if lurls != lwant else f"{len(lurls)}/{len(lwant)} 个 URL 一致")
    else:
        check("13. llms.txt 存在", False)

    # 8. 外链资源存在
    refs = set()
    # 站内绝对路径（/favicon.svg 等，根部署）也纳入校验；仅排除外部 URL、
    # protocol-relative（//）、锚点（#）、mailto。
    for h in htmls.values():
        refs |= set(re.findall(r'(?:src|href)="(?!https?://|//|#|mailto:)([^"?]+)', h))
    refs = {r for r in refs if r.strip("/")}  # 剔除 logo href="/" 这类首页自引用
    miss = sorted(r for r in refs if not (ROOT / r.lstrip("/")).exists())
    check("8. 页面引用的本地资源全部存在", not miss, f"缺失: {miss}" if miss else f"{len(refs)} 个: {sorted(refs)}")

    # 9. 结构等价（委托 structure_gate.py：骨架唯一 + 金标锁）
    #    取代旧的「对冻结基线字节 diff + EXEMPT 手工豁免表 + 逐功能 strip 正则」——
    #    该方案每新增功能/页面都要改验证器，正是本轮升级要修的债。
    r9 = subprocess.run([sys.executable, str(STRUCTURE_GATE)],
                        cwd=ROOT, capture_output=True, text=True)
    lines9 = [l.strip() for l in r9.stdout.splitlines() if l.strip().startswith(("✅", "❌", "↻"))]
    check("9. 结构等价（骨架唯一 + 金标锁，零维护）", r9.returncode == 0,
          (lines9[-1][1:100] if lines9 else (r9.stderr.strip() or "无输出")[:120]))
    for l in lines9:
        print(f'      {l}')

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

    # 11. 行为级 harness（引擎内部行为 + 多语页“页面默认语言”链路）
    harnesses = ["engine_harness.mjs", "lang_default_harness.mjs"]
    node = shutil.which("node")
    if not node:
        check("11. 行为级 harness 全绿", False, "node 不在 PATH，无法验证行为")
    else:
        all_ok, oks, fails = True, [], []
        for hf in harnesses:
            hp = SRC / "tools" / hf
            if not hp.exists():
                all_ok = False; fails.append(f"缺失 {hf}"); continue
            r3 = subprocess.run([node, str(hp)], cwd=ROOT, capture_output=True, text=True)
            tail = (r3.stdout + r3.stderr).strip().splitlines()
            last = tail[-1] if tail else "(无输出)"
            if r3.returncode == 0:
                oks.append(f"{hf}: {last}")
            else:
                all_ok = False
                fails.append(f"{hf}: {last} | " + " ; ".join(l for l in tail if "❌" in l)[:120])
        check("11. 行为级 harness 全绿", all_ok,
              " ; ".join(oks) if all_ok else " ; ".join(fails)[:200])

    # 14. 外链台账数据合法（linkops ledger check）
    r14 = subprocess.run([sys.executable, str(SRC / "tools" / "linkops.py"), "ledger", "check"],
                         cwd=ROOT, capture_output=True, text=True)
    check("14. 外链台账数据合法（linkops ledger check）", r14.returncode == 0,
          (r14.stdout.strip() or r14.stderr.strip())[-90:])

    # 15. llms-full.txt 覆盖全部页面（GEO：AI 可直接引用的全文清单）
    lf = ROOT / "llms-full.txt"
    if lf.exists():
        body = lf.read_text(encoding="utf-8")
        miss_full = [n for n in names if (SITE + "/" if n == "index.html" else SITE + "/" + n)
                     not in body]
        check("15. llms-full.txt 覆盖全部页面", not miss_full,
              f"缺 {miss_full[:3]}" if miss_full else f"{len(names)} 页全文已收录")
    else:
        check("15. llms-full.txt 存在", False, "缺失（build.py 生成）")

    # 15b. GEO 镜像必须保留结构化内容（表格/清单）
    #      教训：build_seo 会把 <table>/<div class="tbl">/<ul>/<ol> 原样输出而不包 <p>，
    #      一旦抽取正则只认 <(h2|p)>，所有基准表与清单会**静默**从 AI 可引用文本里消失
    #      —— 而基准数据正是最值得被 AI 引用的部分。本 check 锁死该不变式。
    def _struct_rows(html: str) -> list[str]:
        """取 seo 区块内表格的每一行 / 清单的每一项（归一为与镜像一致的文本）。

        按「行/项」而不是按词验：按词会因关键字在别处也出现而**假阴性**
        （删掉 “Data entry...” 后 “Data” 仍可能在正文里）。
        与 build.py 的 _blocks clean() 同规则（td/th 用 “ | ” 连接、解实体）。
        """
        def norm(s: str) -> str:
            s = re.sub(r"</(?:td|th)>", " | ", s)
            s = re.sub(r"</(?:tr|li)>", "\n", s)
            s = re.sub(r"<[^>]+>", "", s)
            for ent, ch in (("&ndash;", "-"), ("&mdash;", "-"), ("&nbsp;", " "),
                            ("&amp;", "&"), ("&lt;", "<"), ("&gt;", ">"),
                            ("&quot;", '"'), ("&#39;", "'")):
                s = s.replace(ent, ch)
            lines = [re.sub(r"[ \t]+", " ", ln).strip(" |\t") for ln in s.split("\n")]
            return "\n".join(ln for ln in lines if ln)

        rows: list[str] = []
        for sec in re.findall(r'<section class="seo">(.*?)</section>', html, re.S):
            for blk in re.findall(r"<(?:table|ul|ol)>(.*?)</(?:table|ul|ol)>", sec, re.S):
                rows += [ln for ln in norm(blk).split("\n") if len(ln) > 12]
        return rows

    full_text = lf.read_text(encoding="utf-8", errors="replace") if lf.exists() else ""
    lost_mirror, lost_full = [], []
    for n in names:
        rows = _struct_rows((ROOT / n).read_text(encoding="utf-8", errors="replace"))
        if not rows:
            continue
        # 必须按「本页自己的镜像」逐页判：用全局合集会因别页也有同行而假阴性
        m = ROOT / n.replace(".html", ".md")
        mtxt = m.read_text(encoding="utf-8", errors="replace") if m.exists() else ""
        lost_mirror += [f"{n}:{r}" for r in rows if r not in mtxt]
        lost_full += [f"{n}:{r}" for r in rows if r not in full_text]
    check("15b. GEO 镜像保留表格/清单内容（防结构化内容静默丢失）",
          not lost_mirror and not lost_full,
          f".md 丢 {lost_mirror[:2]} / llms-full 丢 {lost_full[:2]}"
          if (lost_mirror or lost_full) else f"{sum(len(_struct_rows((ROOT / n).read_text(encoding='utf-8', errors='replace'))) for n in names)} 行表格/清单已进入镜像")

    # 16. 闭环快照可生成（retro.py 离线只读；只验字段齐全，不比对内容）
    #     快照内容随 commit/时间变化，比对内容会让 CI 频繁误红；此处只保证
    #     「复盘一步跑得通且六段字段在」，真实快照由 CI 信息步/人工查看。
    r16 = subprocess.run([sys.executable, str(SRC / "tools" / "retro.py"), "--json"],
                         cwd=ROOT, capture_output=True, text=True)
    if r16.returncode != 0:
        check("16. 闭环快照可生成（retro.py）", False, (r16.stderr.strip() or "")[-110:])
    else:
        try:
            snap = json.loads(r16.stdout)
            need = ["git", "pages", "sitemap", "ai_manifest", "robots", "backlinks"]
            miss = [k for k in need if k not in snap]
            pages_ok = snap.get("pages", {}).get("count") == len(pages)
            check("16. 闭环快照可生成（retro.py）", not miss and pages_ok,
                  f"缺字段 {miss}" if miss else ("页数不一致" if not pages_ok
                                                else f"六段齐备，{snap['pages']['count']} 页"))
        except Exception as e:  # noqa: BLE001 - 快照不可解析即失败
            check("16. 闭环快照可生成（retro.py）", False, f"输出非 JSON: {e}")

    # 17. GSC 快照可解析（离线；只验存在时字段合法，缺失不算失败）
    #     快照由人工跑 gsc.py snapshot 生成（需服务账号权限），CI 无凭据，
    #     因此缺失时不报错；存在则必须含必需字段且可解析。
    gs = SRC / "tools" / "gsc-snapshot.json"
    if not gs.exists():
        check("17. GSC 快照字段合法（缺失则跳过）", True, "无 gsc-snapshot.json（需手工 gsc.py snapshot）")
    else:
        try:
            g = json.loads(gs.read_text(encoding="utf-8"))
            need17 = ["captured", "range", "clicks", "impressions", "ctr", "position"]
            miss17 = [k for k in need17 if k not in g]
            check("17. GSC 快照字段合法（缺失则跳过）", not miss17,
                  f"缺字段 {miss17}" if miss17 else
                  f"clicks {g['clicks']:.0f} / impressions {g['impressions']:.0f}")
        except Exception as e:  # noqa: BLE001
            check("17. GSC 快照字段合法（缺失则跳过）", False, f"不可解析: {e}")

    print(f"\n通过 {len(ok)}/{len(ok)+len(fail)} 项")
    if fail:
        print("失败项: " + ", ".join(fail))
        return 1
    print("全部检查通过 ✅")
    return 0


if __name__ == "__main__":
    sys.exit(main())
