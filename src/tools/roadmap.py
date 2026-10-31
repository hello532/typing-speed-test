#!/usr/bin/env python3
"""目标路线图 —— 把「2000 点击/28 天」拆成可验收的中间台阶。

    python3 src/tools/roadmap.py             # 现状 + 台阶表 + 缺口归因
    python3 src/tools/roadmap.py --json

和 gauges.py 的分工：gauges 回答「今天先改哪一页」，roadmap 回答「2000 点击
到底需要什么条件，现在卡在哪一层」。三层口径仍然分开：

  observed   GSC 实测（点击/曝光/CTR/平均排名）
  arithmetic 曝光 × CTR = 点击；反推需要的曝光与 CTR
  assumption CTR 曲线与「排名提升来自哪里」的行业经验，全部显式标注

不做的事：不预测日期，不承诺排名。模型只给出「达到 X 门槛需要哪些条件同时成立」。
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gsc  # noqa: E402
import gauges  # noqa: E402

TARGET = 2000
MILESTONES = [100, 250, 500, 1000, 2000]


def observed(days: int = 28) -> dict:
    cred = json.loads(gsc.cred_path().read_text(encoding="utf-8"))
    return gauges.totals(gsc.get_token(cred), days)


def ladder(cur: dict) -> list[dict]:
    """每个里程碑：在三种 CTR 假设下需要的曝光，以及相对当前曝光的倍数。"""
    rows = []
    for m in MILESTONES:
        row = {"clicks": m, "needs": []}
        for ctr in (0.02, 0.03, 0.05):
            imp = m / ctr
            row["needs"].append({"ctr": ctr, "impressions": round(imp),
                                  "multiple_of_now": round(imp / max(cur["impressions"], 1), 1)})
        rows.append(row)
    return rows


def attribution(cur: dict) -> list[dict]:
    """缺口归因：把「还差多少」拆成曝光缺口与位置缺口，各自给出判断依据。"""
    imp, clk, pos, ctr = cur["impressions"], cur["clicks"], cur["position"], cur["ctr"]
    need_imp_at_now_ctr = TARGET / max(ctr, 1e-9)
    need_ctr_at_now_imp = TARGET / max(imp, 1)
    return [
        {"lever": "曝光量（覆盖的查询数 × 每个查询的可见概率）",
         "now": f"{imp:,.0f} 次/28 天",
         "required": f"{need_imp_at_now_ctr:,.0f} 次（保持当前 CTR）",
         "gap_multiple": round(need_imp_at_now_ctr / max(imp, 1), 1),
         "how": "新增页覆盖更多查询 + 现有页排名进入前 20（排名越靠前，进入结果页的机会越多）"},
        {"lever": "CTR（同样曝光被点到的概率）",
         "now": f"{ctr*100:.2f}%",
         "required": f"{need_ctr_at_now_imp*100:.1f}%（保持当前曝光）",
         "gap_multiple": round(need_ctr_at_now_imp / max(ctr, 1e-9), 1),
         "how": "只能靠标题/描述与排名位置，位置 >30 时 CTR 基本由位置决定，文案改善空间有限"},
        {"lever": "平均排名",
         "now": f"{pos:.1f}",
         "required": "≤15 才有稳定的点击面（行业 CTR 曲线：11-20 位约 1.2%）",
         "gap_multiple": round(pos / 15, 1),
         "how": "排名由相关性（页面是否真的回答问题）+ 权威度（引用域名）共同决定；本站相关性工作已做，权威度是当前瓶颈"},
    ]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=28)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    cur = observed(a.days)
    out = {"target": TARGET, "current": cur, "ladder": ladder(cur),
           "attribution": attribution(cur),
           "ctr_curve": gauges.POS_CTR}
    if a.json:
        print(json.dumps(out, ensure_ascii=False, indent=1))
        return 0
    print(f"目标 {TARGET} 点击 / {a.days} 天 ｜ 实测 {cur['clicks']:.0f} 点击 / "
          f"{cur['impressions']:,.0f} 曝光 / CTR {cur['ctr']*100:.2f}% / 平均排名 {cur['position']:.1f}")
    print("\n台阶表（算术，不是预测）：")
    print(f"{'点击目标':>8} {'CTR 2%':>22} {'CTR 3%':>22} {'CTR 5%':>22}")
    for r in out["ladder"]:
        cells = "".join(f"{n['impressions']:>12,}(×{n['multiple_of_now']})" for n in r["needs"])
        print(f"{r['clicks']:>8}{cells}")
    print("\n缺口归因：")
    for x in out["attribution"]:
        print(f"  · {x['lever']}\n      现在 {x['now']} → 需要 {x['required']}（×{x['gap_multiple']}）\n      手段：{x['how']}")
    print("\n注：CTR 曲线是行业观察值，非本站实测；换曲线只需改 gauges.POS_CTR，结论可复算。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
