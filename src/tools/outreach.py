#!/usr/bin/env python3
"""外联发信（backlink outreach）—— 只发「一对一、指名到页面」的信，不群发。

    python3 src/tools/outreach.py --status        # 只看今天谁会发、为什么
    python3 src/tools/outreach.py --send --limit 2  # 真发（Chrome→Gmail→验证进 Sent）

为什么独立于 ops/ 那套发信管线：那套的第五道闸要求「信里的实测数字有证据且未过期」，
是防止它退化成群发的关键。外联信里没有站点实测数字，硬塞进去只能拆那道闸。
这里用同一台机器的 Chrome（已登录 Gmail）真发，发完回写队列，判据自己写清楚：
  1. 每个目标必须已经人工核过「页面确实开着 dofollow 外链、且已在列竞品」
  2. 每天上限 cap_per_day，且同一域名只发一封
  3. 正文必须含 opt-out 句，且不允许群发模板（每个 target 各写各的）
  4. 发完必须换页搜 in:sent 找到那封才算成功，找不到就整轮中止
默认 dry run；要真发必须显式 --send。
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib
import subprocess
import sys
import urllib.parse

HERE = pathlib.Path(__file__).resolve().parent
QUEUE = HERE / "outreach-queue.json"
SENT_LOG = HERE / "outreach-sent.json"
EGO = "ego-browser"


def load() -> dict:
    return json.loads(QUEUE.read_text(encoding="utf-8"))


def save(q: dict) -> None:
    QUEUE.write_text(json.dumps(q, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def sent_log() -> dict:
    if SENT_LOG.exists():
        return json.loads(SENT_LOG.read_text(encoding="utf-8"))
    return {"sent": []}


def eligible(q: dict) -> tuple[list[dict], list[str]]:
    """返回今天可以发的目标，以及被挡掉的目标+原因。"""
    log = sent_log()
    today = dt.date.today().isoformat()
    sent_today = [s for s in log["sent"] if s.get("at", "").startswith(today)]
    domains_today = {urllib.parse.urlsplit(s["page"]).netloc for s in sent_today}
    already = {s["id"] for s in log["sent"]}
    room = max(0, q["cap_per_day"] - len(sent_today))

    ok, blocked = [], []
    for t in sorted(q["targets"], key=lambda x: x["id"]):
        if t["id"] in already:
            blocked.append(f"{t['id']}: 已发过 ({next(s['at'] for s in log['sent'] if s['id'] == t['id'])})")
            continue
        if t["status"] != "pending":
            blocked.append(f"{t['id']}: status={t['status']}（不是可发状态）")
            continue
        if t.get("approved") is not True:
            blocked.append(f"{t['id']}: 未人工批准（approved 不为 true），定时任务不会替你决定发什么")
            continue
        if not t.get("email"):
            blocked.append(f"{t['id']}: 没有邮箱，走表单，人工处理")
            continue
        if not (t.get("subject") and t.get("body")):
            blocked.append(f"{t['id']}: 主题或正文是空的")
            continue
        if q["optout"].split("?")[0].strip() not in t["body"]:
            blocked.append(f"{t['id']}: 正文缺 opt-out 句（会被当成群发）")
            continue
        if urllib.parse.urlsplit(t["page"]).netloc in domains_today:
            blocked.append(f"{t['id']}: 同域名今天已经发过一封")
            continue
        if len(ok) >= room:
            blocked.append(f"{t['id']}: 今天额度用完（cap={q['cap_per_day']}）")
            continue
        if t["dofollow"] != "yes":
            blocked.append(f"{t['id']}: dofollow 未实测确认，不发（发信成本高，先确认再发）")
            continue
        ok.append(t)
    return ok, blocked


def ego_script(q: dict, t: dict) -> str:
    to = t["email"]
    compose = ("https://mail.google.com/mail/?view=cm&fs=1&tf=1"
               f"&to={urllib.parse.quote(to)}"
               f"&su={urllib.parse.quote(t['subject'])}"
               f"&body={urllib.parse.quote(t['body'] + chr(10) + chr(10) + q['sign'])}")
    # 只有 aria-label 以「发送」开头的那个才是 compose 里的发送键；
    # 按文本找会撞上「发送反馈给 Google」并且点了不进 Sent（实测 2026-11-03）。
    needle = json.dumps(t["subject"][:25])
    to_q = json.dumps(f"in:sent to:{t['email']}")
    return f"""
const task = await taskSpace("typing.rerivo outreach");
const p = task.page("p1");
await p.goto({json.dumps(compose)});
let clicked = 'NO_SEND_BUTTON';
for (let i = 0; i < 20; i++) {{
  await new Promise(r => setTimeout(r, 1000));
  clicked = await p.evaluate(() => {{
    const btn = document.querySelector('div[role=button][aria-label^="发送"],div[role=button][aria-label^="Send"]');
    if (!btn) return 'NO_SEND_BUTTON';
    btn.click();
    return 'CLICKED';
  }});
  if (clicked === 'CLICKED') break;
}}
console.log('send:', clicked);
await new Promise(r => setTimeout(r, 5000));
await p.goto("https://mail.google.com/mail/u/0/#search/" + encodeURIComponent({to_q}));
await new Promise(r => setTimeout(r, 6000));
const rows = await p.evaluate((needle) =>
  [...document.querySelectorAll('tr.zA')].map(t => t.innerText.replace(/\\s+/g, ' ').slice(0, 120))
    .filter(t => t.includes(needle)).length, {needle});
console.log('in_sent_rows:', rows);
"""


def send_one(q: dict, t: dict) -> bool:
    script = ego_script(q, t)
    r = subprocess.run([EGO, "nodejs"], input=script, capture_output=True, text=True, timeout=180)
    out = (r.stdout or "") + (r.stderr or "")
    ok = "CLICKED" in out and "in_sent_rows: 0" not in out and "in_sent_rows:" in out
    print(out.strip()[-400:])
    if not ok:
        print(f"❌ {t['id']}: 发送或验证失败，整轮中止（不记账，避免重复发）")
        return False
    log = sent_log()
    log["sent"].append({"id": t["id"], "page": t["page"], "email": t["email"],
                        "subject": t["subject"], "at": dt.datetime.now().isoformat(timespec="seconds")})
    SENT_LOG.write_text(json.dumps(log, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    t["status"] = "sent"
    save(q)
    print(f"✅ {t['id']} → {t['email']}")
    return True


def main() -> int:
    ap = argparse.ArgumentParser(description="backlink outreach sender")
    ap.add_argument("--status", action="store_true", help="dry run: 打印今天会发什么")
    ap.add_argument("--send", action="store_true", help="真发")
    ap.add_argument("--limit", type=int, default=2)
    args = ap.parse_args()

    q = load()
    ok, blocked = eligible(q)
    print(f"队列 {len(q['targets'])} 个目标｜今天可用于发信 {len(ok)} 封")
    for t in ok:
        print(f"  → {t['id']:26s} {t['email']}  | {t['subject'][:60]}")
    for b in blocked:
        print(f"  · {b}")

    if not args.send:
        print("\ndry run：什么都没发。加 --send 才真发。")
        return 0
    if not ok:
        return 0
    for t in ok[: args.limit]:
        if not send_one(q, t):
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
