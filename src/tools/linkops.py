#!/usr/bin/env python3
"""外链/收录运维工具（link ops）—— 把独立站的外链维护从「手工记事」变成可复跑命令。

四个子命令：
  ledger [report|check]  外链台账：状态机汇总 / 数据一致性校验
  probe  [--update]      批量探测目录站：HTTP 状态 + 是否 Cloudflare 墙 / 需登录
  pr     [--update]      PR 合并状态同步：用 gh 查 state/mergedAt/closedAt 回写台账
  live   [--json]        收录核实：sitemap 全量 URL 逐个 HTTP 检查是否 200
  index  [--json]        收录就绪：线上 canonical / robots / AI 清单一致性核实

设计原则：探测只做公开 GET + 文本特征判定，**不绕任何人机验证**；
blocked_cf 的含义就是「自动化被挡，交回人工」，不是失败。
需登录的 gh 只用于 pr（人工命令），不进 CI。
"""
import argparse
import json
import re
import subprocess
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import date
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


# ───────────────────────── pr ─────────────────────────
# 外链 PR 的合并状态只有 GitHub 知道，「每隔几天手点一遍 6 个链接」正是本命令要
# 消灭的动作。用 gh CLI 查 state/mergedAt/closedAt，只回写**明确**信号：
#   MERGED         → live（date = 合并日）
#   CLOSED（未合并）→ dead（date = 关闭日）
#   OPEN           → 保持 submitted
# gh 属人工凭据，不进 CI（CI 只跑 ledger check 这类离线校验）。

GH_HINT = ("需要已登录的 gh CLI（https://cli.github.com）：\n"
           "  brew install gh && gh auth login")


def gh_ready() -> str | None:
    """None = 可用；否则返回带指引的错误文本。"""
    try:
        r = subprocess.run(["gh", "auth", "status"], capture_output=True, text=True, timeout=20)
    except FileNotFoundError:
        return GH_HINT
    except subprocess.TimeoutExpired:
        return "gh auth status 超时（网络或代理问题）"
    if r.returncode != 0:
        return GH_HINT + "\n  （gh auth status 未通过）"
    return None


def gh_pr_state(url: str) -> dict:
    """查单个 PR 的 state/mergedAt/closedAt。"""
    r = subprocess.run(["gh", "pr", "view", url, "--json", "state,mergedAt,closedAt"],
                       capture_output=True, text=True, timeout=30)
    if r.returncode != 0:
        raise RuntimeError((r.stderr or "").strip().splitlines()[-1][:160] if r.stderr else f"gh exit {r.returncode}")
    return json.loads(r.stdout)


def cmd_pr(args) -> int:
    bad = gh_ready()
    if bad:
        print(f"❌ {bad}", file=sys.stderr)
        return 1
    data = load()
    rows = [d for d in data["directories"] if "/pull/" in (d.get("url") or "")]
    if not rows:
        print("台账里没有 /pull/ 条目")
        return 0
    with ThreadPoolExecutor(max_workers=6) as ex:
        results = list(ex.map(lambda d: _safe_pr(d["url"]), rows))

    changed, errs, report = 0, [], []
    for d, res in zip(rows, results):
        if isinstance(res, Exception):
            errs.append(f"{d['name']}: {res}")
            print(f"{d['name'][:44]:<44} {d['status']:<10} → 查询失败：{res}")
            continue
        st = res.get("state")
        if st == "MERGED":
            want, day = "live", (res.get("mergedAt") or "")[:10]
        elif st == "CLOSED":
            want, day = "dead", (res.get("closedAt") or "")[:10]
        else:
            want, day = "submitted", None
        mark = "  ← 变化" if want != d["status"] else ""
        print(f"{d['name'][:44]:<44} {d['status']:<10} → {want:<10} (gh={st}, {day or '-'}){mark}")
        report.append({"name": d["name"], "url": d["url"], "gh": st,
                       "from": d["status"], "to": want, "date": day})
        to_write = want in ("live", "dead") and want != d["status"]
        if to_write:
            changed += 1
            if args.update:
                d["status"] = want
                if day:
                    d["date"] = day
    if args.update and changed:
        data["updated"] = date.today().isoformat()
        save(data)
    if args.json:
        print(json.dumps({"total": len(rows), "changed": changed,
                          "errors": errs, "prs": report}, ensure_ascii=False, indent=1))
    elif args.update:
        print(f"\n已回写台账（{changed} 条变化）" if changed else "\n无变化，未写盘")
    else:
        print(f"\n(dry-run；加 --update 回写台账)  PR {len(rows)} 个，{changed} 个与台账不符")
    return 1 if errs else 0


def _safe_pr(url: str):
    try:
        return gh_pr_state(url)
    except Exception as e:  # noqa: BLE001 - 汇总成错误行，不中断其余 PR
        return e


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


def fetch(u: str, timeout: int = 20) -> tuple[int, str]:
    """GET 一个 URL，返回 (status, body)。失败返回 (0, "")。"""
    req = urllib.request.Request(u, headers={"User-Agent": UA}, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read(500_000).decode("utf-8", "ignore")
    except urllib.error.HTTPError as e:
        return e.code, ""
    except Exception:
        return 0, ""


# ───────────────────────── index ─────────────────────────
# live 只回答「200 不 200」；index 回答「200 但收得对不对」：canonical 是否自指、
# robots 是否声明 Sitemap 且搜索类 UA 未被误拦、AI 清单（llms*.txt）是否可达。
# 这些错都能“返回 200 但丢收录”，只能靠比对线上真实内容发现。

CANON_RE = re.compile(r'<link\s+rel="canonical"\s+href="([^"]*)"', re.I)

# 必须放行的搜索/引用类 UA（与 robots.txt 策略一致；拦了=丢引用）
SEARCH_UAS = ["OAI-SearchBot", "ChatGPT-User", "PerplexityBot", "Claude-SearchBot",
              "Amzn-SearchBot", "Bingbot"]
# 必须拦截的训练类 UA
TRAIN_UAS = ["GPTBot", "CCBot", "Google-Extended", "ClaudeBot"]


def parse_robots(text: str) -> dict[str, list[str]]:
    """按 User-agent 分组解析 Allow/Disallow 值（大小写不敏感）。"""
    groups: dict[str, list[str]] = {}
    cur: list[str] = []
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line or ":" not in line:
            continue
        field, _, val = line.partition(":")
        field, val = field.strip().lower(), val.strip()
        if field == "user-agent":
            cur = [val]
            groups.setdefault(val, [])
        elif field in ("allow", "disallow") and cur:
            for ua in cur:
                groups.setdefault(ua, []).append(f"{field}:{val}")
    return groups


def cmd_index(args) -> int:
    import re as _re
    urls = _re.findall(r"<loc>(.*?)</loc>", SITEMAP.read_text(encoding="utf-8"))
    issues: list[dict] = []

    # 1) 每页 canonical 必须自指（错配 = 权重指到别处或首页）
    def check_canon(u):
        st, body = fetch(u)
        if st != 200:
            return {"url": u, "kind": "status", "detail": f"HTTP {st}"}
        m = CANON_RE.search(body)
        if not m:
            return {"url": u, "kind": "canonical", "detail": "缺 canonical"}
        found = m.group(1).strip()
        if found != u:
            return {"url": u, "kind": "canonical", "detail": f"canonical={found}"}
        return None

    with ThreadPoolExecutor(max_workers=10) as ex:
        for res in ex.map(check_canon, urls):
            if res:
                issues.append(res)
    ok_canon = len(urls) - sum(1 for i in issues if i["kind"] in ("canonical", "status"))

    # 2) robots.txt：必须声明 Sitemap，且搜索类 UA 未被 Disallow、训练类已拦
    rb = "https://typing.rerivo.com/robots.txt"
    st, body = fetch(rb)
    if st != 200:
        issues.append({"url": rb, "kind": "robots", "detail": f"HTTP {st}"})
    else:
        low = body.lower()
        if not any(l.strip().lower().startswith("sitemap:") for l in body.splitlines()):
            issues.append({"url": rb, "kind": "robots-sitemap", "detail": "缺 Sitemap 行"})
        groups = parse_robots(body)
        for ua in SEARCH_UAS:
            if ua not in groups:
                issues.append({"url": rb, "kind": "robots-search-ua", "detail": f"缺 {ua} 声明"})
            elif any(g.lower().startswith("disallow:/") for g in groups[ua]):
                issues.append({"url": rb, "kind": "robots-search-ua", "detail": f"{ua} 被 Disallow（丢引用）"})
        for ua in TRAIN_UAS:
            if ua in groups and not any(g.lower().startswith("disallow:/") for g in groups[ua]):
                issues.append({"url": rb, "kind": "robots-train-ua", "detail": f"{ua} 未拦（允许训练）"})

    # 3) AI 清单与 sitemap 本身可达
    for path in ("llms.txt", "llms-full.txt", "sitemap.xml"):
        u = f"https://typing.rerivo.com/{path}"
        st, _ = fetch(u)
        if st != 200:
            issues.append({"url": u, "kind": "asset", "detail": f"HTTP {st}"})

    for i in issues:
        print(f"  ❌ {i['kind']:<18} {i['detail']:<34} {i['url']}")
    if args.json:
        print(json.dumps({"urls": len(urls), "canonical_ok": ok_canon,
                          "issues": issues}, ensure_ascii=False, indent=1))
    else:
        print(f"\n收录就绪：canonical {ok_canon}/{len(urls)} 自指；"
              f"robots/清单 异常 {sum(1 for i in issues if i['kind'] not in ('canonical','status'))} 项；"
              f"总异常 {len(issues)}")
    return 1 if issues else 0


def main() -> int:
    ap = argparse.ArgumentParser(description="外链/收录运维工具")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p1 = sub.add_parser("ledger"); p1.add_argument("action", nargs="?", default="report", choices=["report", "check"])
    p2 = sub.add_parser("probe"); p2.add_argument("--update", action="store_true"); p2.add_argument("--all", action="store_true")
    p3 = sub.add_parser("live"); p3.add_argument("--json", action="store_true")
    p4 = sub.add_parser("pr"); p4.add_argument("--update", action="store_true"); p4.add_argument("--json", action="store_true")
    p5 = sub.add_parser("index"); p5.add_argument("--json", action="store_true")
    a = ap.parse_args()
    return {"ledger": cmd_ledger, "probe": cmd_probe, "live": cmd_live, "pr": cmd_pr,
            "index": cmd_index}[a.cmd](a)

if __name__ == "__main__":
    sys.exit(main())
