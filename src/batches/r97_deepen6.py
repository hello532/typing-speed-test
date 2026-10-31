#!/usr/bin/env python3
"""R97：补厚 3 个「有曝光、正文 ~1,900 字符」的受众/技能页。

选点依据（GSC 28 天 × 正文长度）：
  typing-test-for-students   84 曝光 / p31.5 / 1,881
  typing-test-for-adults     56 曝光 / p54.7 / 1,930
  number-typing-test         54 曝光 / p57.4 / 1,880

其中 students 页已经站在 p31.5 —— 站内位置最好的一批之一，正文却只有 1,881 字符，
是最值得先补的一页。补的是页面独有的那一层，不是把已有段落扩写。

用法：python3 src/batches/r97_deepen6.py [--check]
"""
import json
import sys
from pathlib import Path

CFG = Path(__file__).resolve().parents[1] / "pages.json"

PATCH = {
    "typing-test-for-students.html": {
        "seo_add": [
            {"h2": "Where students actually lose time", "p": [
                "Not in essays. Students lose time in the small, repeated typing tasks: searching a database for a citation, writing lab notes, replying to a seminar email, formatting a bibliography by hand. Each is two minutes of typing, five times a day.",
                "The measurable consequence is that typing speed correlates with how much written work gets finished, not with how good it is. A student at 35 WPM spends roughly twice as long on the same written output as one at 70 WPM, and that gap comes out of reading time.",
            ]},
            {"h2": "Exam and coursework contexts worth rehearsing", "p": [
                "<table><tr><th>Context</th><th>What is timed</th><th>What to rehearse</th></tr>"
                "<tr><td>Timed online exam with typed answers</td><td>The whole paper, including thinking</td><td>Typing while composing, not copying - practise answering a question in 200 words at pace</td></tr>"
                "<tr><td>In-class laptop notes</td><td>Nothing, but you fall behind the lecture</td><td>Speed with abbreviations and no backspace; lectures run 130-150 words a minute</td></tr>"
                "<tr><td>Referencing and formatting</td><td>Your own patience</td><td>Repeat the same citation ten times rather than ten citations once</td></tr>"
                "<tr><td>Language or typing exam (e.g. SSC, school boards)</td><td>A fixed passage at a fixed speed</td><td>The exact format: length, punctuation, error allowance</td></tr></table>",
            ]},
            {"h2": "A term-long plan that fits around coursework", "p": [
                "Ten minutes, four days a week, for twelve weeks. Weeks 1-4: home row and covered rounds - this is the only part that feels like a step backwards. Weeks 5-8: accuracy at speed, 30-second sprints plus one slow round. Weeks 9-12: real material - lecture notes, your own essay paragraphs, a citation style you actually use.",
                "Do not practise on random word lists in week 9. By then the constraint is your vocabulary and your punctuation habits, and those only appear in your own subject's text.",
            ]},
        ],
        "faq_add": [
            {"q": "Does typing speed matter for grades?", "a": "Indirectly. Timed exams, coursework volume and note-taking all convert typing speed into time. A student at 70 WPM writes the same essay in roughly half the keystrokes' worth of time as one at 35 WPM."},
            {"q": "What typing speed should a university student have?", "a": "45-60 WPM with 97% accuracy covers essay writing, notes and referencing comfortably. Below 35 WPM, the keyboard becomes the bottleneck for written coursework."},
        ],
    },
    "typing-test-for-adults.html": {
        "seo_add": [
            {"h2": "Why adults usually start below where they could be", "p": [
                "Almost every adult who types slowly learned by using a computer, not by being taught. That means the habits formed were whatever got the work done: two fingers, looking at the keyboard, backspacing through errors. None of those are permanent, but all of them are invisible until you try to type without looking.",
                "The encouraging part is that adults learn the key map faster than children do - you already read and write fluently, so the bottleneck is motor habit rather than language. Two weeks of covered rounds typically produces the first real jump.",
            ]},
            {"h2": "Reasons adults actually have for improving", "p": [
                "<ul><li><strong>A job requirement</strong> - clerical, reception, dispatch, legal and medical support postings quote 40-60 WPM and often test it.</li>"
                "<li><strong>A return to work</strong> - the test is usually a five-minute sample with an accuracy floor, not a race.</li>"
                "<li><strong>Career change into admin or support</strong> - the typing bar is modest but the accuracy expectation is not.</li>"
                "<li><strong>Writing volume</strong> - reports, emails and documentation that used to be someone else's job.</li>"
                "<li><strong>Comfort</strong> - less hunting means less wrist and shoulder tension by the end of a day.</li></ul>",
            ]},
            {"h2": "What to expect in the first month", "p": [
                "Week 1 is slower and frustrating: you are replacing a working habit. Weeks 2-3 bring accuracy up and speed back to where it started. Week 4 usually produces the first measurable gain, often 5-8 WPM, mostly from no longer looking down.",
                "If you are over 50, add one thing: a five-minute break every half hour during practice, and stop at the first sign of hand or wrist discomfort. The skill builds fine at that pace; strain does not.",
            ]},
        ],
        "faq_add": [
            {"q": "Can adults learn to touch type?", "a": "Yes, and often faster than children on the key map, because reading and writing are already fluent. The slower part is replacing the two-finger habit, which takes about two weeks of short daily covered practice."},
            {"q": "What typing speed do adult job seekers need?", "a": "40-50 WPM with 97% accuracy covers most clerical, reception and admin postings. Legal, medical and transcription roles ask 60-75, and public-sector tests often require a proctored certificate."},
        ],
    },
    "number-typing-test.html": {
        "seo_add": [
            {"h2": "Digits fail differently from letters", "p": [
                "A letter error is usually visible: the word looks wrong. A digit error looks exactly like a correct number, which is why numeric work is judged on verification rather than on speed. The typical numeric mistakes are transposition (1234 typed as 1324), doubling (11 instead of 1), and a wrong-row slip that turns 4 into 5 or 7 into 8.",
                "Transposition is the most common and the hardest to catch, because both digits are individually valid. It is also the reason numeric drills should be scored on complete fields rather than on character accuracy.",
            ]},
            {"h2": "Drills by digit group", "p": [
                "<table><tr><th>Group</th><th>Where it fails</th><th>Drill</th></tr>"
                "<tr><td>Top row 1-5</td><td>Left hand reaching up, index finger confusion</td><td>Alternate 3-4-3-4 and 4-5-4-5 for 30 seconds</td></tr>"
                "<tr><td>Top row 6-0</td><td>Right hand, weakest fingers</td><td>7-8 and 9-0 pairs; then 6-7-8-9-0 sequences</td></tr>"
                "<tr><td>Amounts with decimals</td><td>The dot key position, and trailing zeros</td><td>Type 10 amounts with two decimals, verify each</td></tr>"
                "<tr><td>Keypad</td><td>Home row 4-5-6 and the thumb on 0</td><td>Enter ten figures, press Enter after each</td></tr></table>",
                "Two minutes a day on one row beats ten minutes cycling through all of them, because the failure is local.",
            ]},
        ],
        "faq_add": [
            {"q": "Why do I transpose digits?", "a": "Both digits are individually correct, so there is no visual signal that anything is wrong. It is the most common numeric error and the reason numeric work is scored on complete fields rather than on characters."},
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
        elif len(patch.get("seo_add", [])) < 1 or len(patch.get("faq_add", [])) < 1:
            errs.append(f"{f}: 新增内容不足")
    if errs:
        for e in errs:
            print("  ·", e)
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
