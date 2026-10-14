#!/usr/bin/env python3
"""GSC 取数工具（Google Search Console）—— 把「收录/排名」从人工看板变成可复跑命令。

    python3 src/tools/gsc.py report                 # 28d 概览 + sitemap 状态
    python3 src/tools/gsc.py pages                  # 按页聚合（点击数/曝光/排名）
    python3 src/tools/gsc.py queries                # 按查询聚合
    python3 src/tools/gsc.py unindexed              # 未编入索引的 URL 清单
    python3 src/tools/gsc.py growth                 # 与基线对比算增幅
    python3 src/tools/gsc.py --json report          # 机器可读

凭据：服务账号 JSON（默认读 GSC_CREDENTIALS 环境变量；未设则尝试
~/.config/google-seo-mcp/kinx-seo-credentials.json）。该账号须在 GSC 里
被授予该资源的权限，否则 API 返回 403 —— 这是「完整」权限用户，不是拥有者。

仅用标准库。Python 3.14 默认开启 VERIFY_X509_STRICT，会拒绝本地代理（Surge）
的 MITM 根证书（缺 Authority Key Identifier）；本模块在发现 CA 文件时
关闭该标志，仅用于让系统代理链通过验证，不跳过证书校验本身。
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import ssl
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
SITE = "https://typing.rerivo.com/"
SITEMAP = "https://typing.rerivo.com/sitemap.xml"
DEFAULT_CRED = Path.home() / ".config" / "google-seo-mcp" / "kinx-seo-credentials.json"
DEFAULT_CA = Path.home() / ".config" / "google-seo-mcp" / "ca" / "surge-all.pem"
SCOPES = "https://www.googleapis.com/auth/webmasters.readonly"
API = "https://www.googleapis.com/webmasters/v3"
BASELINE = Path(__file__).resolve().parent / "gsc-baseline.json"

# 基线（2026-10-14 建立，用于 growth 对比）
FALLBACK_BASELINE = {"captured": "2026-10-14", "days": 28,
                     "clicks": 4, "impressions": 1290, "ctr": 0.0031, "position": 57.2,
                     "indexed": 23, "not_indexed": 13}


def cred_path() -> Path:
    return Path(os.environ.get("GSC_CREDENTIALS") or DEFAULT_CRED)


def build_ctx() -> ssl.SSLContext:
    ca = Path(os.environ.get("GSC_CA") or DEFAULT_CA)
    ctx = ssl.create_default_context(cafile=str(ca) if ca.exists() else None)
    # 本地代理的 MITM 根证书缺 AKI，被 3.13+ 的严格模式拒收
    if hasattr(ssl, "VERIFY_X509_STRICT"):
        ctx.verify_flags &= ~ssl.VERIFY_X509_STRICT
    return ctx


def _b64(o: dict) -> str:
    return base64.urlsafe_b64encode(json.dumps(o, separators=(",", ":")).encode()).decode().rstrip("=")


def sign_jwt(cred: dict) -> str:
    """用 openssl 签 RS256（避免依赖 cryptography 库）。"""
    now = int(time.time())
    claim = {"iss": cred["client_email"], "scope": SCOPES, "aud": cred["token_uri"],
             "exp": now + 3600, "iat": now}
    signing_input = f"{_b64({'alg': 'RS256', 'typ': 'JWT'})}.{_b64(claim)}"
    with tempfile.NamedTemporaryFile("w", suffix=".pem", delete=False) as f:
        f.write(cred["private_key"])
        keyfile = f.name
    try:
        p = subprocess.run(["openssl", "dgst", "-sha256", "-sign", keyfile],
                           input=signing_input.encode(), capture_output=True)
        if p.returncode != 0:
            sys.exit(f"openssl 签名失败：{p.stderr.decode()[:200]}")
        sig = base64.urlsafe_b64encode(p.stdout).decode().rstrip("=")
    finally:
        os.unlink(keyfile)
    return f"{signing_input}.{sig}"


def get_token(cred: dict) -> str:
    data = urllib.parse.urlencode({
        "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
        "assertion": sign_jwt(cred)}).encode()
    req = urllib.request.Request(cred["token_uri"], data=data,
                                 headers={"Content-Type": "application/x-www-form-urlencoded"})
    with urllib.request.urlopen(req, timeout=30, context=build_ctx()) as r:
        return json.load(r)["access_token"]


def api(path: str, token: str, body: dict | None = None, method: str | None = None) -> dict:
    """GET 读接口；带 body 时默认 POST（Search Console 的 query 接口必须 POST）。"""
    method = method or ("POST" if body is not None else "GET")
    url = f"{API}/{path}"
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method,
                                 headers={"Authorization": f"Bearer {token}",
                                          "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=45, context=build_ctx()) as r:
            raw = r.read().decode()
            return json.loads(raw) if raw.strip() else {}
    except urllib.error.HTTPError as e:
        detail = e.read().decode()[:300]
        if e.code == 403:
            sys.exit(f"❌ 403 无权限。确认服务账号已在 GSC 里被授予「完整」权限。\n{detail}")
        sys.exit(f"❌ HTTP {e.code}: {detail}")


def date_range(days: int) -> tuple[str, str]:
    end = date.today() - timedelta(days=1)      # GSC 数据有 ~1 天延迟
    return (end - timedelta(days=days - 1)).isoformat(), end.isoformat()


def cmd_report(args) -> int:
    cred = json.loads(cred_path().read_text(encoding="utf-8"))
    tok = get_token(cred)
    start, end = date_range(args.days)
    body = {"startDate": start, "endDate": end, "dimensions": [], "rowLimit": 1}
    tot = api(f"sites/{urllib.parse.quote(SITE, safe='')}/searchAnalytics/query", tok, body)
    rows = tot.get("rows") or [{}]
    cur = {"clicks": rows[0].get("clicks", 0), "impressions": rows[0].get("impressions", 0),
           "ctr": rows[0].get("ctr", 0), "position": rows[0].get("position", 0)}
    sms = api(f"sites/{urllib.parse.quote(SITE, safe='')}/sitemaps", tok)
    out = {"site": SITE, "range": {"start": start, "end": end, "days": args.days}, "totals": cur,
           "sitemaps": [{"path": s.get("path"), "lastSubmitted": s.get("lastSubmitted"),
                         "lastDownloaded": s.get("lastDownloaded"), "errors": s.get("errors"),
                         "warnings": s.get("warnings"), "isPending": s.get("isPending")}
                        for s in sms.get("sitemap", [])]}
    if args.json:
        print(json.dumps(out, ensure_ascii=False, indent=1))
        return 0
    print(f"GSC 概览 {SITE}（{start} ~ {end}，{args.days} 天）")
    print(f"  点击 {cur['clicks']:.0f} | 曝光 {cur['impressions']:.0f} | "
          f"CTR {cur['ctr']*100:.2f}% | 平均排名 {cur['position']:.1f}")
    for s in out["sitemaps"]:
        print(f"  sitemap {s['path']}: 错误 {s['errors']} 警告 {s['warnings']} "
              f"下载于 {s['lastDownloaded']}")
    return 0


def query_rows(token: str, dimension: str, days: int, limit: int = 500) -> list[dict]:
    start, end = date_range(days)
    body = {"startDate": start, "endDate": end, "dimensions": [dimension],
            "rowLimit": limit}
    return api(f"sites/{urllib.parse.quote(SITE, safe='')}/searchAnalytics/query",
               token, body).get("rows", [])


def cmd_pages(args) -> int:
    cred = json.loads(cred_path().read_text(encoding="utf-8"))
    rows = query_rows(get_token(cred), "page", args.days)
    rows.sort(key=lambda r: -r["impressions"])
    if args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=1))
        return 0
    print(f"{'impressions':>11} {'clicks':>7} {'pos':>6}  page")
    for r in rows:
        print(f"{r['impressions']:>11.0f} {r['clicks']:>7.0f} {r['position']:>6.1f}  {r['keys'][0]}")
    print(f"\n{len(rows)} 个有曝光的页面")
    return 0


def cmd_queries(args) -> int:
    cred = json.loads(cred_path().read_text(encoding="utf-8"))
    rows = query_rows(get_token(cred), "query", args.days)
    rows.sort(key=lambda r: -r["impressions"])
    if args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=1))
        return 0
    print(f"{'impressions':>11} {'clicks':>7} {'pos':>6}  query")
    for r in rows:
        print(f"{r['impressions']:>11.0f} {r['clicks']:>7.0f} {r['position']:>6.1f}  {r['keys'][0]}")
    print(f"\n{len(rows)} 个查询")
    return 0


def cmd_unindexed(args) -> int:
    """列出 sitemap 里有、但 GSC「已编入索引」列表里没有的 URL。"""
    sm = ROOT / "sitemap.xml"
    import re as _re
    want = _re.findall(r"<loc>(.*?)</loc>", sm.read_text(encoding="utf-8"))
    cred = json.loads(cred_path().read_text(encoding="utf-8"))
    tok = get_token(cred)
    rows = query_rows(tok, "page", 180)          # 180 天，接近全量历史
    seen = {r["keys"][0] for r in rows}
    missing = [u for u in want if u not in seen]
    if args.json:
        print(json.dumps({"sitemap": len(want), "with_impressions": len(seen),
                          "never_seen": missing}, ensure_ascii=False, indent=1))
        return 0
    print(f"sitemap {len(want)} 页，其中 {len(seen)} 页有曝光记录，{len(missing)} 页从未出现：")
    for u in missing:
        print(f"  · {u}")
    print("\n注意：GSC API 不暴露「索引状态」计数，准确未编入清单请在浏览器看"
          "\n      编制索引 → 未编入索引（本命令用曝光缺失近似）。")
    return 0


def load_baseline() -> dict:
    if BASELINE.exists():
        return json.loads(BASELINE.read_text(encoding="utf-8"))
    return dict(FALLBACK_BASELINE)


def cmd_growth(args) -> int:
    """与基线对比，算增幅（这就是「GSC 增长 200%」的度量口径）。"""
    cred = json.loads(cred_path().read_text(encoding="utf-8"))
    tok = get_token(cred)
    start, end = date_range(args.days)
    rows = api(f"sites/{urllib.parse.quote(SITE, safe='')}/searchAnalytics/query", tok,
               {"startDate": start, "endDate": end, "dimensions": [], "rowLimit": 1}).get("rows") or [{}]
    cur = {"clicks": rows[0].get("clicks", 0), "impressions": rows[0].get("impressions", 0),
           "ctr": rows[0].get("ctr", 0), "position": rows[0].get("position", 0)}
    base = load_baseline()

    def pct(now, was):
        if not was:
            return None
        return (now - was) / was * 100

    out = {"baseline_captured": base["captured"], "range": {"start": start, "end": end},
           "baseline": {k: base[k] for k in ("clicks", "impressions", "ctr", "position")},
           "current": cur,
           "growth_pct": {k: pct(cur[k], base[k]) for k in ("clicks", "impressions")}}
    if args.json:
        print(json.dumps(out, ensure_ascii=False, indent=1))
        return 0
    print(f"GSC 增长对比（基线 {base['captured']} → {start}~{end}）")
    for k, label in (("clicks", "点击"), ("impressions", "曝光")):
        g = out["growth_pct"][k]
        flag = "✅ 达标(+200%)" if (g or 0) >= 200 else ("— 未达标" if g is not None else "无基线")
        print(f"  {label}: {base[k]:.0f} → {cur[k]:.0f}  ({g:+.1f}%)  {flag}" if g is not None
              else f"  {label}: {base[k]:.0f} → {cur[k]:.0f}  无基线")
    print(f"  CTR: {base['ctr']*100:.2f}% → {cur['ctr']*100:.2f}% | "
          f"平均排名: {base['position']:.1f} → {cur['position']:.1f}")
    return 0


def cmd_snapshot(args) -> int:
    """取一次搜索表现快照并落盘 gsc-snapshot.json，供离线 retro.py 读取。"""
    cred = json.loads(cred_path().read_text(encoding="utf-8"))
    tok = get_token(cred)
    start, end = date_range(args.days)
    rows = api(f"sites/{urllib.parse.quote(SITE, safe='')}/searchAnalytics/query", tok,
               {"startDate": start, "endDate": end, "dimensions": [], "rowLimit": 1}).get("rows") or [{}]
    out = {"captured": date.today().isoformat(),
           "range": {"start": start, "end": end, "days": args.days},
           "clicks": rows[0].get("clicks", 0), "impressions": rows[0].get("impressions", 0),
           "ctr": rows[0].get("ctr", 0), "position": rows[0].get("position", 0)}
    p = SRC / "tools" / "gsc-snapshot.json"
    p.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"written: {p.relative_to(ROOT)}")
    print(f"  clicks {out['clicks']:.0f} | impressions {out['impressions']:.0f} | "
          f"CTR {out['ctr']*100:.2f}% | pos {out['position']:.1f}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="GSC 取数工具（需服务账号已被授予 GSC 权限）")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--days", type=int, default=28)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("report", "pages", "queries", "unindexed", "growth", "snapshot"):
        sub.add_parser(name)
    # 顶层 --json/--days 也允许写在子命令后
    a = ap.parse_args()
    if not cred_path().exists():
        print(f"❌ 找不到凭据 {cred_path()}\n   设置 GSC_CREDENTIALS 指向服务账号 JSON。", file=sys.stderr)
        return 1
    return {"report": cmd_report, "pages": cmd_pages, "queries": cmd_queries,
            "unindexed": cmd_unindexed, "growth": cmd_growth,
            "snapshot": cmd_snapshot}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
