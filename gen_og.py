#!/usr/bin/env python3
"""生成 6 张成绩分享 OG 图（1200×630 PNG，<200KB）到 /og/。"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

OUT = Path(__file__).resolve().parent / "og"
OUT.mkdir(exist_ok=True)

BG = (11, 12, 16)
PANEL = (21, 23, 31)
ACCENT = (255, 201, 60)
TEXT = (237, 238, 242)
DIM = (139, 145, 166)

def font(size, bold=True):
    for p in ("/System/Library/Fonts/Helvetica.ttc",
              "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
              "/System/Library/Fonts/Supplemental/Arial.ttf"):
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            continue
    return ImageFont.load_default()

TIERS = [
    ("elite", "ELITE — TOP 1%", "I scored 100+ WPM on this typing test", "Can you beat me?"),
    ("fast", "FAST — TOP 10%", "I scored 80-99 WPM on this typing test", "Can you beat me?"),
    ("good", "GOOD — OFFICE STANDARD", "I scored 60-79 WPM on this typing test", "Can you beat me?"),
    ("average", "AVERAGE TYPIST", "I scored 40-59 WPM on this typing test", "Can you beat me?"),
    ("beginner", "BEGINNER TYPIST", "I scored under 40 WPM — just started", "Watch me improve!"),
    ("generic", "FREE TYPING SPEED TEST", "Check your WPM in 60 seconds", "No sign up, instant results"),
]

for name, badge, line1, line2 in TIERS:
    im = Image.new("RGB", (1200, 630), BG)
    d = ImageDraw.Draw(im)
    d.rectangle([40, 40, 1160, 590], outline=(38, 42, 55), width=2)
    d.rectangle([40, 40, 1160, 150], fill=PANEL)
    d.text((80, 72), "TYPING.RERIVO", font=font(44), fill=ACCENT)
    d.text((80, 200), badge, font=font(72), fill=ACCENT)
    d.text((80, 320), line1, font=font(46, False), fill=TEXT)
    d.text((80, 400), line2, font=font(46, False), fill=TEXT)
    d.text((80, 510), "typing.rerivo.com — free, no sign up", font=font(32, False), fill=DIM)
    im.save(OUT / f"{name}.png", optimize=True)
    print(f"og/{name}.png", (OUT / f"{name}.png").stat().st_size, "B")
