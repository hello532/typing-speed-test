#!/usr/bin/env python3
"""外链/收录运维工具（link ops）—— 把独立站的外链维护从「手工记事」变成可复跑命令。

三个子命令：
  ledger [report|check]  外链台账：状态机汇总 / 数据一致性校验
  probe  [--update]      批量探测目录站：HTTP 状态 + 是否 Cloudflare 墙 / 需登录
  live   [--json]        收录核实：sitemap 全量 URL 逐个 HTTP 检查是否 200

设计原则：探测只做公开 GET + 文本特征判定，**不绕任何人机验证**；
blocked_cf 的含义就是「自动化被挡，交回人工」，不是失败。
"""
import argparse
import json
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
LEDGER = ROOT / "src" / "tools" / "directories.json"
SITEMAP = ROOT / "sitemap.xml"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

VALID = {"candidate", "submitted", "live", "blocked_cf", "needs_login", "dead", "skipped"}
CF_MARKERS = ("just a moment", "performing security verification", "cf-turnstile",
              "attention required", "checking your browser", "verify you are human")
LOGIN_MARKERS = ('type="password"', "name=\"password\"", "name='password'")
TERMINAL = {"submitted", "live", "skipped"}


# ───────────────────────── ledger ─────────────────────────

def load() -> dict:
    return json.loads(LEDGER.read_text(encoding="utf-8"))


def save(data: dict) -> None:
    LEDGER.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")


def cmd_ledger(args) -> int:
    data = load()
    rows = data["directories"]
    if args.action == "check":
        bad = []
        for d in rows:
            for f in ("name", "url", "status"):
                if not d.get(f):
                    bad.append(f"{d.get('name', '?')}: 缺 {f}")
            if d["status"] not in VALID:
                bad.append(f"{d['name']}: 非法 status={d['status']}")
            if d["status"] in ("submitted", "live") and not d.get("date"):
                bad.append(f"{d['name']}: {d['status']} 必须有 date")
        if bad:
            print("❌ 台账校验失败:")
            for b in bad:
                print("  -", b)
            return 1
        print(f"✅ 台账校验通过（{len(rows)} 条）")
        return 0

    order = ["live", "submitted", "candidate", "blocked_cf", "needs_login", "dead", "skipped"]
    print(f"{'STATUS':<12} {'LINK':<9} {'DR':<4} NAME")
    print("-" * 74)
    for st in order:
        for d in sorted([r for r in rows if r["status"] == st], key=lambda r: -(r.get("dr") or 0)):
            link = {"yes": "dofollow", "no": "nofollow"}.get(d.get("dofollow"), "?")
            print(f"{d['status']:<12} {link:<9} {str(d.get('dr') or '-'):<4} {d['name']}")
            print(f"{'':<12} {d['url']}")
    counts = {}
    for d in rows:
        counts[d["status"]] = counts.get(d["status"], 0) + 1
    print("-" * 74)
    print(" | ".join(f"{k}={v}" for k, v in sorted(counts.items())))
    print(f"total={len(rows)}  updated={data.get('updated')}")
    return 0


# ───────────────────────── probe ─────────────────────────

def probe(url: str) -> dict:
    """公开 GET 一次，按文本特征分类。不做任何验证绕过。"""
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            status = r.status
            body = r.read(200_000).decode("utf-8", "ignore").lower()
    except urllib.error.HTTPError as e:
        if e.code in (404, 410):
            return {"status": "dead", "http": e.code, "why": f"HTTP {e.code}"}
        try:
            body = e.read(200_000).decode("utf-8", "ignore").lower()
        except Exception:
            body = ""
        status, _ = e.code, None
        if any(m in body for m in CF_MARKERS):
            return {"status": "blocked_cf", "http": e.code, "why": "Cloudflare challenge"}
        return {"status": "candidate", "http": e.code, "why": f"HTTP {e.code}"}
    except Exception as e:
        return {"status": "dead", "http": None, "why": type(e).__name__}

    if any(m in body for m in CF_MARKERS):
        return {"status": "blocked_cf", "http": status, "why": "Cloudflare challenge"}
    has_pw = any(m in body for m in LOGIN_MARKERS)
    has_form = ("<form" in body) or ("<input" in body)
    if has_pw and not has_form:
        return {"status": "needs_login", "http": status, "why": "password-only login"}
    if has_pw and "sign up" not in body and "register" not in body:
        return {"status": "needs_login", "http": status, "why": "login form"}
    return {"status": "candidate", "http": status, "why": "reachable"}


# 「可达」是弱信号：很多需要登录的目录根页也返回 200。因此只有**明确**信号
# （Cloudflare 挑战 / 404-410 下架）才允许改写台账，其余仅作提示，交人工判断。
UNAMBIGUOUS = {"blocked_cf", "dead"}


def cmd_probe(args) -> int:
    data = load()
    rows = [d for d in data["directories"] if d.get("kind") != "indexing"]
    if not args.all:
        rows = [d for d in rows if d["status"] not in TERMINAL]
    with ThreadPoolExecutor(max_workers=8) as ex:
        results = list(ex.map(lambda d: probe(d["url"]), rows))
    changed = 0
    for d, res in zip(rows, results):
        mark = "" if res["status"] == d["status"] else "  ← 变化"
        if mark:
            changed += 1
        print(f"{d['name']:<34} {d['status']:<12} → {res['status']:<12} ({res['why']}, http={res['http']}){mark}")
        if args.update and d["status"] not in TERMINAL and res["status"] in UNAMBIGUOUS:
            d["status"] = res["status"]
    if args.update:
        if changed:
            data["updated"] = __import__("datetime").date.today().isoformat()
            save(data)
        print(f"\n已回写台账（{changed} 条变化）" if changed else "\n无变化，未写盘")
    else:
        print(f"\n(dry-run；加 --update 回写台账)  探测 {len(rows)} 个，{changed} 个与台账不符")
    return 0


# ───────────────────────── live ─────────────────────────

def cmd_live(args) -> int:
    import re
    urls = re.findall(r"<loc>(.*?)</loc>", SITEMAP.read_text(encoding="utf-8"))
    def head(u):
        req = urllib.request.Request(u, headers={"User-Agent": UA}, method="GET")
        try:
            with urllib.request.urlopen(req, timeout=15) as r:
                return u, r.status
        except urllib.error.HTTPError as e:
            return u, e.code
        except Exception:
            return u, 0
    with ThreadPoolExecutor(max_workers=10) as ex:
        out = list(ex.map(head, urls))
    bad = [(u, s) for u, s in out if s != 200]
    for u, s in out:
        if s != 200:
            print(f"  ❌ {s:>4} {u}")
    if args.json:
        print(json.dumps({"total": len(out), "ok": len(out) - len(bad), "bad": bad}, ensure_ascii=False))
    else:
        print(f"\nsitemap {len(out)} URL：{len(out)-len(bad)} × 200，{len(bad)} 异常")
    return 1 if bad else 0


def main() -> int:
    ap = argparse.ArgumentParser(description="外链/收录运维工具")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p1 = sub.add_parser("ledger"); p1.add_argument("action", nargs="?", default="report", choices=["report", "check"])
    p2 = sub.add_parser("probe"); p2.add_argument("--update", action="store_true"); p2.add_argument("--all", action="store_true")
    p3 = sub.add_parser("live"); p3.add_argument("--json", action="store_true")
    a = ap.parse_args()
    return {"ledger": cmd_ledger, "probe": cmd_probe, "live": cmd_live}[a.cmd](a)

if __name__ == "__main__":
    sys.exit(main())
