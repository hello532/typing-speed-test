#!/usr/bin/env python3
"""R98：补厚位置最好的三个薄页（custom / keyboard-typing / beginner）。

选点依据（GSC 28 天，按位置排序的薄页）：
  custom-typing-test     p14.1 / 47 曝光 / 1,903 字符
  keyboard-typing-test   p22.9 / 18 曝光 / 1,513 字符
  beginner-typing-test   p29.7 / 37 曝光 / 1,959 字符

其中 keyboard-typing-test 存在真实的**意图错配**：标题里的 "keyboard test" 同时指向
「检查键盘按键是否正常」和「测打字速度」两种需求。补一节「怎么逐键检查键盘」，
把两种意图都接住——这是本轮最有价值的一处。

用法：python3 src/batches/r98_deepen7.py [--check]
"""
import json
import sys
from pathlib import Path

CFG = Path(__file__).resolve().parents[1] / "pages.json"

PATCH = {
    "custom-typing-test.html": {
        "seo_add": [
            {"h2": "When a custom test is the right measurement", "p": [
                "A custom test is valid for <em>practising a specific text</em>. It is not valid for <em>comparing yourself to a benchmark</em>, because the passage you chose is not a neutral sample.",
                "Use it for: rehearsing the exact format of an employer's test, drilling your own domain vocabulary, and reproducing a text you keep mistyping. Do not use it to decide whether you are fast enough for a job - use a standard sentence test at the same length as the employer's, because that is what their test will be.",
            ]},
            {"h2": "How pasted text behaves in the engine", "p": [
                "The text is split on whitespace and typed word by word. Punctuation inside a word (hyphens, apostrophes, brackets) is counted as part of that word, so a passage full of citations will score lower than the same character count of plain prose - correctly, because it is harder to type.",
                "Two things to watch when pasting: smart quotes and non-breaking spaces from a word processor can produce characters your keyboard does not have a key for, and a very long single line will wrap in a way that makes the cursor jump. Paste plain text, and keep paragraphs under about 400 words.",
            ]},
        ],
        "faq_add": [
            {"q": "Can I use a custom test to measure my speed for a job?", "a": "Not as a benchmark - the passage you chose is not a neutral sample. Use a standard test at the employer's length for the number, and a custom test to rehearse their format."},
        ],
    },
    "keyboard-typing-test.html": {
        "seo_add": [
            {"h2": "Is my keyboard working? A key-by-key check", "p": [
                "If you arrived looking for a way to test whether keys are broken rather than how fast you type, this is the same exercise from the other direction: the test above records which characters you produce, so a key that never registers will show up as a missing character rather than a slow one.",
                "<ol><li><strong>Type every character deliberately</strong>, including Shift, in a one-minute round: a-z, 0-9, and the punctuation you use.</li>"
                "<li><strong>Read the error report</strong>, not the score. A key that produces nothing shows up as an omission on every attempt; a key that double-registers shows as extra characters.</li>"
                "<li><strong>Repeat on a second device if possible</strong> - if the same key fails on both, it is the key; if only one, it is that keyboard or its connection.</li>"
                "<li><strong>For a laptop, note whether it fails only on battery</strong> - some keyboards behave differently under power management.</li></ol>",
                "This will not diagnose a hardware fault with certainty, and it cannot test keys your operating system intercepts (media keys, function-row shortcuts). For those, use the operating system's own input viewer.",
            ]},
            {"h2": "Keyboard types and what they change for typing tests", "p": [
                "<table><tr><th>Type</th><th>Key travel</th><th>What it changes in a test</th></tr>"
                "<tr><td>Laptop chiclet</td><td>~1.5 mm</td><td>Faster to actuate, less feedback; lower wrist position</td></tr>"
                "<tr><td>Standard membrane</td><td>~3 mm</td><td>Slower return, mushier bottom-out; what testing centres usually provide</td></tr>"
                "<tr><td>Mechanical (linear)</td><td>3-4 mm</td><td>Consistent actuation, no tactile bump; slightly faster for most typists</td></tr>"
                "<tr><td>Mechanical (tactile/clicky)</td><td>3-4 mm</td><td>Clear feedback, slightly slower but fewer accidental presses</td></tr></table>",
                "Expect 3-8 WPM difference between a laptop board and a mechanical one for the same typist. If a test result matters, use the keyboard you will be tested on.",
            ]},
        ],
        "faq_add": [
            {"q": "How can I check if a key on my keyboard is broken?", "a": "Type every character deliberately in a one-minute round and read the error report: a dead key appears as a repeated omission, a double-registering key as extra characters. Repeat on another device to tell a key fault from a keyboard or connection fault."},
            {"q": "Does the keyboard type affect a typing test score?", "a": "By roughly 3-8 WPM between a laptop chiclet board and a mechanical one. Key travel and feedback affect error rate more than raw speed."},
        ],
    },
    "beginner-typing-test.html": {
        "seo_add": [
            {"h2": "Your first week, day by day", "p": [
                "<table><tr><th>Day</th><th>10 minutes</th><th>What to notice</th></tr>"
                "<tr><td>1</td><td>Find F and J by touch; type the home row slowly</td><td>Whether you can return to the home row without looking</td></tr>"
                "<tr><td>2</td><td>Home row words; one 30-second covered round</td><td>How much accuracy drops when you cannot see</td></tr>"
                "<tr><td>3</td><td>Top row added; short real words</td><td>Which finger reaches wrong first</td></tr>"
                "<tr><td>4</td><td>Bottom row added; one minute of normal text</td><td>Whether you are backspacing more than typing</td></tr>"
                "<tr><td>5</td><td>No-backspace round, then a slow accuracy round</td><td>How much the corrections were costing you</td></tr>"
                "<tr><td>6-7</td><td>One timed round per day, same length</td><td>The size of the gap between your two scores</td></tr></table>",
            ]},
            {"h2": "Three beginner mistakes worth avoiding", "p": [
                "<ul><li><strong>Practising at the edge of frustration.</strong> If accuracy drops below 90%, the session is teaching you to make mistakes. Slow down until it is above 95%.</li>"
                "<li><strong>Chasing WPM in week one.</strong> The first two weeks are about the map, not the speed. Speed arrives as a side effect and then keeps arriving.</li>"
                "<li><strong>Switching keyboards or layouts mid-month.</strong> Each switch resets the motor learning you just built. Pick one and stay for a month.</li></ul>",
                "The fourth mistake is invisible: practising only when motivated. Ten minutes, four days a week, beats a two-hour session every other Sunday by a wide margin.",
            ]},
        ],
        "faq_add": [
            {"q": "What should I do in my first week of typing practice?", "a": "Find F and J by touch, drill the home row, then add the top and bottom rows one at a time, keeping accuracy above 95%. One covered round a day from day two."},
        ],
    },
}


def main() -> int:
    cfg = json.loads(CFG.read_text(encoding="utf-8"))
    pages = {p["file"]: p for p in cfg["pages"]}
    errs = [f"{f}: 不存在" for f in PATCH if f not in pages]
    if errs:
        print("\n".join(errs))
        return 1
    if "--check" in sys.argv:
        print("✅ 校验通过")
        return 0
    for f, patch in PATCH.items():
        pg = pages[f]
        have = {s["h2"] for s in pg["seo"]}
        for s in patch["seo_add"]:
            if s["h2"] not in have:
                pg["seo"].append(s)
        haveq = {q["q"] for q in pg["faq"]}
        for q in patch["faq_add"]:
            if q["q"] not in haveq:
                pg["faq"].append(q)
    CFG.write_text(json.dumps(cfg, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    for f in PATCH:
        pg = pages[f]
        print(f, sum(len(x) for s in pg["seo"] for x in s["p"]), "chars |", len(pg["faq"]), "faq")
    return 0


if __name__ == "__main__":
    sys.exit(main())
