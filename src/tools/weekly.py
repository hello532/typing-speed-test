#!/usr/bin/env python3
"""周报 —— 上周 vs 前一周的真实变化，只看能行动的信号。

    python3 src/tools/weekly.py             # 默认 7 天窗口对比
    python3 src/tools/weekly.py --days 28
    python3 src/tools/weekly.py --json

输出四段：
  1. 总量对比（点击/曝光/CTR/平均排名）
  2. 新进榜查询（上周没有曝光、这周有）—— 说明新页面或新内容开始被看见
  3. 排名跃升 / 跌落最大的页面（≥5 个名次才报）
  4. 结论：这周该改什么（只根据数据，不根据心情）

GSC 有 ~2 天延迟，所以窗口取 [today-2-days, today-2-days] 之前，避免把不完整的一天算进来。
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.parse
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gsc  # noqa: E402


def window(days: int, offset: int) -> tuple[str, str]:
    # 3 天回退：GSC 最后 2-3 天常未定型，早读会把「数据没到」当成「排名掉了」
    end = date.today() - timedelta(days=3 + offset)
    return (end - timedelta(days=days - 1)).isoformat(), end.isoformat()


def rows(tok: str, dim: str, start: str, end: str) -> list[dict]:
    body = {"startDate": start, "endDate": end, "dimensions": [dim], "rowLimit": 1000}
    r = gsc.api(f"sites/{urllib.parse.quote(gsc.SITE, safe='')}/searchAnalytics/query", tok, body)
    return r.get("rows", [])


def totals(tok: str, start: str, end: str) -> dict:
    body = {"startDate": start, "endDate": end, "dimensions": [], "rowLimit": 1}
    r = gsc.api(f"sites/{urllib.parse.quote(gsc.SITE, safe='')}/searchAnalytics/query", tok, body)
    row = (r.get("rows") or [{}])[0]
    return {"clicks": row.get("clicks", 0), "impressions": row.get("impressions", 0),
            "ctr": row.get("ctr", 0), "position": row.get("position", 0)}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=7)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    cred = json.loads(gsc.cred_path().read_text(encoding="utf-8"))
    tok = gsc.get_token(cred)

    cur_s, cur_e = window(a.days, 0)
    prev_s, prev_e = window(a.days, a.days)
    cur, prev = totals(tok, cur_s, cur_e), totals(tok, prev_s, prev_e)

    cq = {r["keys"][0]: r for r in rows(tok, "query", cur_s, cur_e)}
    pq = {r["keys"][0]: r for r in rows(tok, "query", prev_s, prev_e)}
    cp = {r["keys"][0]: r for r in rows(tok, "page", cur_s, cur_e)}
    pp = {r["keys"][0]: r for r in rows(tok, "page", prev_s, prev_e)}

    new_q = sorted([q for q in cq if q not in pq], key=lambda q: -cq[q]["impressions"])[:15]
    movers = []
    for u, r in cp.items():
        if u in pp:
            delta = pp[u]["position"] - r["position"]
            if abs(delta) >= 5:
                movers.append({"page": u.replace("https://typing.rerivo.com/", ""),
                               "delta": round(delta, 1), "now": round(r["position"], 1),
                               "impressions": r["impressions"], "clicks": r["clicks"]})
    movers.sort(key=lambda x: -abs(x["delta"]))

    out = {"range": {"current": [cur_s, cur_e], "previous": [prev_s, prev_e]},
           "current": cur, "previous": prev,
           "new_queries": [{"query": q, "impressions": cq[q]["impressions"],
                            "position": round(cq[q]["position"], 1)} for q in new_q],
           "movers": movers[:12]}

    if a.json:
        print(json.dumps(out, ensure_ascii=False, indent=1))
        return 0

    print(f"周报 {cur_s} ~ {cur_e}（对比 {prev_s} ~ {prev_e}）")
    for k, label in (("clicks", "点击"), ("impressions", "曝光")):
        d = cur[k] - prev[k]
        print(f"  {label}: {cur[k]:.0f}（前一窗口 {prev[k]:.0f}，{'+' if d>=0 else ''}{d:.0f}）")
    print(f"  CTR: {cur['ctr']*100:.2f}%（前 {prev['ctr']*100:.2f}%）")
    print(f"  平均排名: {cur['position']:.1f}（前 {prev['position']:.1f}）")
    print(f"\n新进榜查询（{len(out['new_queries'])} 个，按曝光）：")
    for q in out["new_queries"]:
        print(f"  {q['impressions']:>4.0f} 次  p{q['position']:>5.1f}  {q['query']}")
    print(f"\n名次变动 ≥5 的页面：")
    for m in out["movers"]:
        arrow = "↑" if m["delta"] > 0 else "↓"
        print(f"  {arrow}{abs(m['delta']):>5.1f}  p{m['now']:>5.1f}  {m['impressions']:>5.0f} 次  {m['page']}")
    if min(cur["impressions"], prev["impressions"]) < 500:
        print("\n⚠️  窗口曝光 <500，名次变动与 CTR 波动基本是噪声，只把「新进榜查询」当信号看。")
    print("\n结论口径："
          "曝光涨而排名不动 → 覆盖变宽，继续加页/加内链；"
          "排名涨而点击不动 → 改标题描述；"
          "两者都不动 → 缺外链，内容不是瓶颈。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
