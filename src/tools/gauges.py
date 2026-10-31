#!/usr/bin/env python3
"""目标仪表盘 —— 把「点击做到 2000」翻译成可复算的漏斗，并给出该先改哪一页。

    python3 src/tools/gauges.py              # 现状 + 差距 + 机会队列
    python3 src/tools/gauges.py --json       # 机器可读
    python3 src/tools/gauges.py --days 90    # 换窗口

三个口径必须分开（混在一起就会自己骗自己）：

  1. observed  —— GSC 实测：点击、曝光、CTR、平均排名。这是唯一的事实层。
  2. required  —— 反推：要在 28 天内拿到 2000 点击，需要多少曝光 × 多少 CTR。
                  这是算术，不是预测。
  3. assumption—— CTR 曲线（位置 → 点击率）。业界观察值，不是本站实测，
                  所以单列出来，改曲线只改一个 dict，结论可复算。

机会队列的算法：对每个已有曝光的页面，用「若排名进到 1–10 的 CTR」算该页
可得的点击上限，减去它现在实际得到的点击，得到 uplift。uplift 最大的先改。
这只回答「先动哪页」，不承诺「动了就涨」——排名由外链与内容共同决定。
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gsc  # noqa: E402  复用取数/鉴权，不重复实现 JWT

TARGET_CLICKS = 2000          # 目标：每 28 天 2000 次点击
WINDOW = 28

# 位置 → CTR（业界观察区间中位，非本站实测；改这里结论跟着变）
POS_CTR = [(1, 0.274), (2, 0.155), (3, 0.110), (4, 0.080), (5, 0.060),
           (6, 0.045), (7, 0.035), (8, 0.030), (9, 0.025), (10, 0.022),
           (20, 0.012), (30, 0.008), (50, 0.005), (100, 0.002)]


def ctr_at(pos: float) -> float:
    for edge, ctr in POS_CTR:
        if pos <= edge:
            return ctr
    return 0.001


def totals(tok: str, days: int) -> dict:
    start, end = gsc.date_range(days)
    body = {"startDate": start, "endDate": end, "dimensions": [], "rowLimit": 1}
    rows = gsc.api(f"sites/{urllib.parse.quote(gsc.SITE, safe='')}/searchAnalytics/query",
                   tok, body).get("rows") or [{}]
    r = rows[0]
    return {"start": start, "end": end, "days": days,
            "clicks": r.get("clicks", 0), "impressions": r.get("impressions", 0),
            "ctr": r.get("ctr", 0), "position": r.get("position", 0)}


def page_rows(tok: str, days: int) -> list[dict]:
    rows = gsc.query_rows(tok, "page", days, limit=1000)
    for r in rows:
        r["url"] = r["keys"][0]
    return rows


def build(days: int) -> dict:
    cred = json.loads(gsc.cred_path().read_text(encoding="utf-8"))
    tok = gsc.get_token(cred)
    cur = totals(tok, days)
    prev = totals(tok, days * 2)          # 同一接口取双窗口，再相减近似「上一窗口」
    pages = page_rows(tok, days)

    # 反推：2000 点击需要什么
    need = []
    for ctr_assumed in (0.02, 0.03, 0.05):
        need.append({"assumed_ctr": ctr_assumed,
                     "required_impressions": round(TARGET_CLICKS / ctr_assumed)})

    # 机会队列：uplift = 曝光 × (CTR@top10 − 实际 CTR)
    queue = []
    for r in pages:
        imp, clk, pos = r["impressions"], r["clicks"], r["position"]
        if imp < 5:
            continue
        upside = imp * ctr_at(10) - clk
        queue.append({"url": r["url"], "impressions": imp, "clicks": clk,
                      "position": round(pos, 1), "ctr": round(clk / imp, 4) if imp else 0,
                      "uplift_if_top10": round(upside, 1)})
    queue.sort(key=lambda x: -x["uplift_if_top10"])

    # 已进前 30 的页面：最容易真正吃到点击的一批
    near = sorted([q for q in queue if q["position"] <= 30], key=lambda x: x["position"])

    return {"target_clicks": TARGET_CLICKS, "window_days": days,
            "current": cur, "prev_window_approx": prev,
            "required": need, "pages_with_impressions": len(pages),
            "opportunity_queue": queue[:40], "near_top30": near[:20],
            "total_available_uplift": round(sum(q["uplift_if_top10"] for q in queue), 1)}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=WINDOW)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    d = build(a.days)
    if a.json:
        print(json.dumps(d, ensure_ascii=False, indent=1))
        return 0
    c = d["current"]
    print(f"目标：{d['target_clicks']} 点击 / {d['window_days']} 天")
    print(f"实测 {c['start']} ~ {c['end']}：点击 {c['clicks']:.0f} | 曝光 {c['impressions']:.0f} "
          f"| CTR {c['ctr']*100:.2f}% | 平均排名 {c['position']:.1f}")
    gap = d["target_clicks"] - c["clicks"]
    print(f"缺口：{gap:.0f} 点击（当前完成度 {c['clicks']/d['target_clicks']*100:.1f}%）")
    print("\n反推（算术，不是预测）：")
    for n in d["required"]:
        print(f"  若 CTR {n['assumed_ctr']*100:.0f}% → 需要曝光 {n['required_impressions']:,}"
              f"（现值 {c['impressions']:,.0f}，倍数 ×{n['required_impressions']/max(c['impressions'],1):.1f}）")
    print(f"\n有曝光的页面：{d['pages_with_impressions']} 个")
    print(f"若全部进前 10 的可回收点击上限：{d['total_available_uplift']:.0f}")
    print("\n机会队列（uplift 高者先改）：")
    print(f"{'impr':>7} {'clicks':>6} {'pos':>6} {'uplift':>7}  page")
    for q in d["opportunity_queue"][:20]:
        print(f"{q['impressions']:>7.0f} {q['clicks']:>6.0f} {q['position']:>6.1f} "
              f"{q['uplift_if_top10']:>7.1f}  {q['url'].replace('https://typing.rerivo.com/', '')}")
    print("\n已进前 30（先保住再往上推）：")
    for q in d["near_top30"]:
        print(f"  pos {q['position']:>5.1f}  {q['clicks']:>3.0f}/{q['impressions']:<5.0f} "
              f"{q['url'].replace('https://typing.rerivo.com/', '')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
