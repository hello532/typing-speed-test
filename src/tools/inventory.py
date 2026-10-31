#!/usr/bin/env python3
"""内容清单 —— 把 184 页按聚类排开，附真实曝光/位置/正文长度，生成 INVENTORY.md。

    python3 src/tools/inventory.py            # 写 INVENTORY.md
    python3 src/tools/inventory.py --stdout

有什么用：决定「该删、该扩、该合并」时看的是这张表，而不是印象。
没有 GSC 凭据时照常生成，只是曝光列显示为 —（页面清单与厚度仍然有用）。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def gsc_pages() -> dict:
    try:
        sys.path.insert(0, str(ROOT / "src" / "tools"))
        import gsc  # noqa: E402
        cred = json.loads(gsc.cred_path().read_text(encoding="utf-8"))
        rows = gsc.query_rows(gsc.get_token(cred), "page", 28, limit=1000)
        return {r["keys"][0].replace("https://typing.rerivo.com/", "").replace("https://typing.rerivo.com", "index.html"):
                {"impressions": r["impressions"], "clicks": r["clicks"], "position": r["position"]}
                for r in rows}
    except Exception:
        return {}


def body_len(p: dict) -> int:
    return sum(len(x) for s in p["seo"] for x in s["p"])


def main() -> int:
    cfg = json.loads((ROOT / "src" / "pages.json").read_text(encoding="utf-8"))
    clusters = json.loads((ROOT / "src" / "clusters.json").read_text(encoding="utf-8"))
    labels = {  # 与 build.py 的 CLUSTER_LABELS 保持一致
        "duration": "Test lengths", "metric": "WPM, CPM and scoring", "language": "Languages",
        "layout": "Layouts and hand position", "exam": "Certificates, jobs and exams",
        "audience": "By age and skill level", "practice": "Practice and lessons",
        "game": "Games and races", "jobs": "Typing jobs and transcription",
        "core": "Popular tests", "meta": "Site pages",
    }
    pages = {p["file"]: p for p in cfg["pages"]}
    gsc_rows = gsc_pages()
    lines = ["# Content inventory", "",
             f"{len(pages)} pages. Figures are GSC, last 28 days, as of this run. "
             "A dash means the page had no impressions in the window.", ""]
    total_impr = 0
    for name, items in clusters.items():
        lines.append(f"## {labels.get(name, name.title())} ({len(items)})")
        lines.append("")
        lines.append("| page | body chars | FAQ | impressions | position |")
        lines.append("|---|---|---|---|---|")
        rows = []
        for it in items:
            p = pages.get(it["file"])
            if not p:
                continue
            g = gsc_rows.get(it["file"], {})
            impr = g.get("impressions", 0)
            total_impr += impr
            rows.append((impr, it["file"], body_len(p), len(p["faq"]),
                         f"{g.get('position', 0):.1f}" if g else "—"))
        rows.sort(key=lambda r: -r[0])
        for impr, f, bl, faq, pos in rows:
            lines.append(f"| [{f}](https://typing.rerivo.com/{f}) | {bl:,} | {faq} | "
                         f"{int(impr) if impr else '—'} | {pos} |")
        lines.append("")
    lines.append("\\* body chars = characters of prose in the SEO section (excludes FAQ, nav, footer). "
                 "Impressions are per page from GSC's page dimension; their sum does not equal the "
                 "property-level total, so no total is published here.")
    text = "\n".join(lines) + "\n"
    if "--stdout" in sys.argv:
        print(text)
    else:
        (ROOT / "INVENTORY.md").write_text(text, encoding="utf-8")
        print(f"wrote INVENTORY.md ({len(pages)} pages, {len(text)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
