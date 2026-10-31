#!/usr/bin/env python3
"""R96：补厚 4 个「有曝光但正文偏短」的页面。

选点依据（GSC 28 天 × 正文长度）：
  keyboard-practice   341 曝光 / p77.2 / 1,790 字符
  typing-tutorial     176 曝光 / p47.6 / 1,890
  online-typing-test  159 曝光 / p53.9 / 1,997
  touch-typing-test   100 曝光 / p45.7 / 1,647

这是「曝光已经存在、内容却撑不住位置」的典型组合，比再开新页更值得动。
补的都是页面独有的一层：键盘硬件差异、教程卡住时怎么办、在线测试的可信度判据、
盲打进度怎么量——不是把已有段落换个说法。

用法：python3 src/batches/r96_deepen5.py [--check]
"""
import json
import sys
from pathlib import Path

CFG = Path(__file__).resolve().parents[1] / "pages.json"

PATCH = {
    "keyboard-practice.html": {
        "seo_add": [
            {"h2": "The keyboard itself changes the exercise", "p": [
                "A laptop chiclet keyboard has about 1.5 mm of travel and keys 19 mm apart; a mechanical board usually has 3-4 mm and the same spacing. The spacing matters for accuracy - your fingers reach the same distance - while the travel matters for speed and for how forgiving a mistyped key is.",
                "Three practical consequences for practice: on a laptop, your wrists sit lower and the temptation to rest them on the palm rest is stronger; on a full-size board the number pad pushes the mouse further away, which changes shoulder position; and on a compact board without a number pad, the digit row is the only way to type numbers, so the drill is different.",
                "If you practise on one keyboard and are tested on another, spend one session a week on the other one. Key travel and keycap shape change your error rate more than a week of extra drills.",
            ]},
            {"h2": "Reading your error report", "p": [
                "After a session, look at which keys appear most often in the miss list rather than at the score. A cluster on the right hand usually means the reaches to the bracket and apostrophe area; a cluster on the left hand usually means the pinky is not returning to A.",
                "Then drill the cluster, not the whole alphabet. Thirty seconds on five keys beats ten minutes on all of them, because the failure is local and so is the fix.",
            ]},
        ],
        "faq_add": [
            {"q": "Does a mechanical keyboard make you faster?", "a": "Slightly, for most people - shorter travel and clearer feedback are worth roughly 3-8 WPM at best. It will not fix the look-at-keyboard habit, which is the larger constraint."},
            {"q": "Can I practise on a laptop keyboard?", "a": "Yes, and you should if that is what you will be tested on. Laptops have less key travel and a lower wrist position, both of which change your error pattern."},
        ],
    },
    "typing-tutorial.html": {
        "seo_add": [
            {"h2": "When a stage will not click", "p": [
                "Every stage has a characteristic failure, and each has one fix that works better than repeating the same drill:",
                "<table><tr><th>Symptom</th><th>What it usually means</th><th>Fix</th></tr>"
                "<tr><td>Accuracy collapses when you cover your hands</td><td>The key map is visual, not spatial</td><td>Two weeks of covered rounds at 30 seconds, no target</td></tr>"
                "<tr><td>Speed rises but errors rise faster</td><td>You are typing ahead of the buffer</td><td>Drop to 85% pace for a week; one error per round allowed</td></tr>"
                "<tr><td>Fine on sentences, lost on digits</td><td>The number row was never drilled</td><td>Two minutes of Numbers mode daily, graded on errors</td></tr>"
                "<tr><td>Good in practice, worse in tests</td><td>The countdown itself is the problem</td><td>Practise with the timer visible every session, same length as the test</td></tr></table>",
            ]},
            {"h2": "How long each stage actually takes", "p": [
                "These are typical ranges for an adult practising fifteen minutes a day, not guarantees. The spread between people is wide, and the variable that predicts progress is how many days you show up, not how long each session is.",
                "<ul><li><strong>Home row secure:</strong> 1-2 weeks.</li>"
                "<li><strong>All rows without looking:</strong> 3-4 weeks.</li>"
                "<li><strong>Capitals and punctuation not breaking rhythm:</strong> 5-6 weeks.</li>"
                "<li><strong>45 WPM sustained on normal text:</strong> 2-3 months.</li>"
                "<li><strong>60 WPM:</strong> 4-6 months for most adults starting from two-finger typing.</li></ul>",
                "If you are outside those ranges by a lot, the cause is almost always one of the four symptoms above rather than talent.",
            ]},
        ],
        "faq_add": [
            {"q": "What if I get stuck at a stage?", "a": "Each stage has a characteristic failure: a visual key map (fix with covered rounds), typing ahead of the buffer (drop to 85% pace), undrilled digits (two minutes of Numbers mode), or test anxiety (practise with the timer visible)."},
        ],
    },
    "online-typing-test.html": {
        "seo_add": [
            {"h2": "What makes an online typing test trustworthy", "p": [
                "Four things decide whether a browser typing test gives you a number worth quoting:",
                "<ol><li><strong>It reports net WPM</strong>, not only gross. A test that counts every character and never subtracts errors will flatter you by 5-10 WPM.</li>"
                "<li><strong>It states the length</strong> and lets you change it. A 15-second burst and a five-minute run are different measurements.</li>"
                "<li><strong>It shows accuracy beside speed.</strong> Speed without accuracy is not what employers screen on.</li>"
                "<li><strong>It does not reward skipping punctuation.</strong> If capitals and full stops are absent from the passage, the score will not transfer to a document.</li></ol>",
                "None of that requires an account. A test that gates the score behind a sign-up is optimising for its own funnel, not for your measurement.",
            ]},
            {"h2": "Device and browser caveats", "p": [
                "Your keyboard changes the result more than your browser does. A laptop board, a mechanical board and a phone screen produce three different scores for the same skill - roughly 51 WPM, similar or slightly higher, and 36 WPM respectively in the published measurements.",
                "Two browser-level things are worth knowing: autocorrect and text-expansion tools can inflate a score without you noticing, and browser zoom changes how much text is visible, which changes how far ahead you can read. Test at 100% zoom, with autocorrect off, on the device you will be tested on.",
            ]},
        ],
        "faq_add": [
            {"q": "How do I know an online typing test is accurate?", "a": "It reports net WPM (errors subtracted), states the test length, shows accuracy beside speed, and includes capitals and punctuation in the passage. Sign-up walls and gross-only scoring are the usual red flags."},
            {"q": "Does my browser affect the score?", "a": "Less than the keyboard does, but autocorrect, text expansion and unusual zoom levels all change the result. Test at 100% zoom with those tools off."},
        ],
    },
    "touch-typing-test.html": {
        "seo_add": [
            {"h2": "Measuring progress without fooling yourself", "p": [
                "Three numbers, once a week, same test length and time of day: net WPM, accuracy, and consistency (how much your speed varies second to second). Progress in touch typing usually shows up in accuracy first, then consistency, then speed - in that order.",
                "If speed rises while accuracy falls, you are trading one for the other and the net result is flat. That is the most common false plateau, and the fix is a week of accuracy-only rounds rather than more speed work.",
            ]},
        ],
        "faq_add": [
            {"q": "How do I know my touch typing is improving?", "a": "Track net WPM, accuracy and consistency weekly at the same length. Accuracy improves first, then consistency, then speed; if speed rises while accuracy falls, the net result is flat."},
        ],
    },
}


def main() -> int:
    cfg = json.loads(CFG.read_text(encoding="utf-8"))
    pages = {p["file"]: p for p in cfg["pages"]}
    errs = []
    for f, patch in PATCH.items():
        if f not in pages:
            errs.append(f"{f}: 不存在")
            continue
        add = [s for s in patch.get("seo_add", []) if s.get("p")]
        if not add:
            errs.append(f"{f}: 没有有效新增小节")
        if len(patch.get("faq_add", [])) < 1:
            errs.append(f"{f}: 没有新增 FAQ")
    if errs:
        for e in errs:
            print("  ·", e)
        print("❌ 未写入")
        return 1
    if "--check" in sys.argv:
        print("✅ 校验通过")
        return 0
    for f, patch in PATCH.items():
        pg = pages[f]
        have = {s["h2"] for s in pg["seo"]}
        for s in patch.get("seo_add", []):
            if s.get("h2") and s["h2"] not in have and s.get("p"):
                pg["seo"].append(s)
        haveq = {q["q"] for q in pg["faq"]}
        for q in patch.get("faq_add", []):
            if q["q"] not in haveq:
                pg["faq"].append(q)
    CFG.write_text(json.dumps(cfg, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    for f in PATCH:
        pg = pages[f]
        print(f, sum(len(x) for s in pg["seo"] for x in s["p"]), "chars |", len(pg["faq"]), "faq")
    return 0


if __name__ == "__main__":
    sys.exit(main())
