#!/usr/bin/env python3
"""IndexNow submitter (Round-6): submit all sitemap.xml URLs to api.indexnow.org.

Stdlib only. Reads key from 39f4fcd69975670c8a24a9ab78838ba9.txt,
reads URLs from sitemap.xml, POSTs JSON {host, key, keyLocation, urlList}
in batches of up to 10000. Prints success/failure counts; exits 1 on failure.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HOST = "typing.rerivo.com"
KEY_FILE = ROOT / "39f4fcd69975670c8a24a9ab78838ba9.txt"
KEY_LOCATION = f"https://{HOST}/39f4fcd69975670c8a24a9ab78838ba9.txt"
SITEMAP = ROOT / "sitemap.xml"
ENDPOINT = "https://api.indexnow.org/indexnow"
BATCH_SIZE = 10000


def load_key(key_file: Path) -> str:
    return key_file.read_text(encoding="utf-8").strip()


def load_urls(sitemap: Path) -> list[str]:
    tree = ET.parse(sitemap)
    root = tree.getroot()
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    locs = root.findall("sm:url/sm:loc", ns) or root.findall("url/loc")
    urls = [ (el.text or "").strip() for el in locs ]
    urls = [u for u in urls if u]
    # de-dup preserving order
    return list(dict.fromkeys(urls))


def submit_batch(key: str, batch: list[str]) -> bool:
    payload = {
        "host": HOST,
        "key": key,
        "keyLocation": KEY_LOCATION,
        "urlList": batch,
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        ENDPOINT,
        data=data,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            code = resp.getcode()
            return 200 <= code < 300
    except Exception as e:  # noqa: BLE001 - report and count as failure
        print(f"batch failed ({len(batch)} urls): {e}", file=sys.stderr)
        return False


def main() -> int:
    ap = argparse.ArgumentParser(description="Submit sitemap URLs to IndexNow.")
    ap.add_argument("--dry-run", action="store_true",
                    help="Only print URL count, do not submit.")
    ap.add_argument("--sitemap", default=str(SITEMAP), help="Path to sitemap.xml")
    ap.add_argument("--key-file", default=str(KEY_FILE), help="Path to IndexNow key file")
    args = ap.parse_args()

    key = load_key(Path(args.key_file))
    urls = load_urls(Path(args.sitemap))
    print(f"urls: {len(urls)}")

    if args.dry_run:
        print("dry-run: 0 submitted, no requests sent")
        return 0

    batches = [urls[i:i + BATCH_SIZE] for i in range(0, len(urls), BATCH_SIZE)] or [[]]
    ok = sum(1 for b in batches if submit_batch(key, b))
    fail = len(batches) - ok
    print(f"batches: {len(batches)}, success: {ok}, failed: {fail}")
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
