#!/usr/bin/env python3
"""结构闸门（structural gate）—— 零维护的全站骨架不变量。

替代旧的 check 9（对 2024 冻结基线做字节 diff + 手工维护 EXEMPT 豁免表 /
逐功能 strip 正则）。旧方案的病：**每加一个功能块或页面，都要手工改验证器**，
否则闸门变红；且豁免表会无限膨胀，最终没人敢动。

新方案把「结构等价」变成一个**不变量 + 显式意图**：

  S1  全站 49 页骨架归一后必须收敛到同一结构（面包屑为可选槽位，单独守卫）。
      —— 任何页面多出/缺失结构块，立刻失败并打印差异行。
  S2  每页骨架必须含全部必需槽位（TDK/canonical/hero/seo/faq/LD/nav/footer）。
  S3  **金标锁（golden lock）**：骨架必须等于 src/tools/structure_gate.golden。
      有意改结构时跑 `python3 src/tools/structure_gate.py --update` 重新登记金标 ——
      这一步取代了过去的「手工往 EXEMPT 里加一行」，但由**机器生成**差异，
      且把「有意变更」记录在版本化的金标文件里，可 review、可回滚。

用法：
  python3 src/tools/structure_gate.py            # 校验
  python3 src/tools/structure_gate.py --update   # 重签金标（结构有意变更后）
"""
import difflib
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SRC = ROOT / "src"
GOLDEN = SRC / "tools" / "structure_gate.golden"
sys.path.insert(0, str(SRC / "tools"))
from skeleton import skeleton  # noqa: E402

REQUIRED_SLOTS = ["{{TITLE}}", "{{DESC}}", "{{CANONICAL}}", "{{OG}}", "{{TW}}",
                  "{{HERO}}", "{{SEO}}", "{{FAQ}}", "{{LD}}", "{{NAV}}", "{{FOOT}}"]


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def main() -> int:
    update = "--update" in sys.argv
    cfg = json.loads((SRC / "pages.json").read_text(encoding="utf-8"))
    names = [p["file"] for p in cfg["pages"]]
    ok, fail = [], []

    def check(name, cond, detail=""):
        (ok if cond else fail).append(name)
        print(f'  {"✅" if cond else "❌"} {name}' + (f" — {detail}" if detail else ""))
        return cond

    skels = {}
    for n in names:
        p = ROOT / n
        skels[n] = skeleton(p.read_text(encoding="utf-8")) if p.exists() else ""

    # —— S1a 面包屑：除首页外每页都应有
    no_crumbs = [n for n, s in skels.items() if n != "index.html" and "{{CRUMBS}}" not in s]
    check("S1a. 除首页外每页都有面包屑",
          not no_crumbs, f"缺面包屑: {no_crumbs[:5]}" if no_crumbs else f"{len(names)-1} 页均有")

    # —— S1 骨架唯一（面包屑剥掉后比）
    variants = {}
    for n, s in skels.items():
        variants.setdefault(s.replace("{{CRUMBS}}\n", "").replace("{{CRUMBS}}", ""), []).append(n)
    base_key, base_pages = max(variants.items(), key=lambda kv: len(kv[1]))
    if not check("S1. 全站骨架唯一（归一后收敛到同一结构）",
                 len(variants) == 1,
                 f"{len(variants)} 种骨架：" + "; ".join(f"{len(v)}页" for v in variants.values())):
        for k, v in variants.items():
            if k == base_key:
                continue
            d = [l for l in difflib.unified_diff(base_key.split("\n"), k.split("\n"),
                                                 lineterm="", n=0)
                 if l[:1] in "+-" and not l.startswith(("+++", "---"))]
            print(f'      · 异常簇 {v[:3]}（{len(v)} 页）差异 {len(d)} 行：')
            for l in d[:8]:
                print(f"          {l[:120]}")

    # —— S2 必需槽位齐全
    miss_slots = {n: [s for s in REQUIRED_SLOTS if s not in sk] for n, sk in skels.items()}
    miss_slots = {n: v for n, v in miss_slots.items() if v}
    check("S2. 每页骨架含全部必需槽位（TDK/hero/seo/faq/LD/nav/footer）",
          not miss_slots, str(list(miss_slots.items())[:3]) if miss_slots else f"{len(names)} 页齐全")

    # —— S3 金标锁
    cur = base_key
    if update:
        GOLDEN.write_text(cur + "\n", encoding="utf-8")
        print(f"  ↻ 金标重签 → {GOLDEN.relative_to(ROOT)}（{digest(cur)}）")
        return 0
    if not GOLDEN.exists():
        check("S3. 骨架 == 金标（golden lock）", False, "金标缺失，跑 --update 生成")
    else:
        gold = GOLDEN.read_text(encoding="utf-8").rstrip("\n")
        same = (gold == cur)
        check("S3. 骨架 == 金标（golden lock）", same,
              f"金标 {digest(gold)} / 现产 {digest(cur)}"
              + ("" if same else " —— 结构有意变更则跑 --update 重签"))
        if not same:
            d = [l for l in difflib.unified_diff(gold.split("\n"), cur.split("\n"),
                                                 lineterm="", n=1,
                                                 fromfile="golden", tofile="product")
                 if l[:1] in "+-" and not l.startswith(("+++", "---"))]
            for l in d[:14]:
                print(f"          {l[:130]}")

    print(f"\n通过 {len(ok)}/{len(ok)+len(fail)} 项")
    if fail:
        print("失败项: " + ", ".join(fail))
        return 1
    print("结构闸门全绿 ✅")
    return 0


if __name__ == "__main__":
    sys.exit(main())
