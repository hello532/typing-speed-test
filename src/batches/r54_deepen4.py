#!/usr/bin/env python3
"""R54：补厚最后 4 个薄页（教程 / 打字教练 / 全字母句 / 银行考试）。

完成"全站正文 ≥1,500 字符"的收尾。这四页各自的内容层：
教程 = 学习路径与检查点；教练 = 人工 vs 软件的分工与选人标准；
全字母句 = 26 字母覆盖的原理与最佳句子；银行考试 = 印度银行文书岗的口径与练习。

用法：python3 src/batches/r54_deepen4.py [--check]
"""
import json
import sys
from pathlib import Path

CFG = Path(__file__).resolve().parents[1] / "pages.json"

PATCH = {
    "typing-tutorial.html": {
        "seo": [
            {"h2": "The path, and what each stage is for", "p": [
                "<table><tr><th>Stage</th><th>What you do</th><th>Move on when</th></tr>"
                "<tr><td>1. Home row</td><td>asdf jkl; until the fingers return without looking</td><td>95% accuracy, no glances</td></tr>"
                "<tr><td>2. All rows</td><td>Top row, then bottom row, one at a time</td><td>30 WPM on ordinary words</td></tr>"
                "<tr><td>3. Modifiers</td><td>Shift for capitals, punctuation in sentences</td><td>96% accuracy with punctuation intact</td></tr>"
                "<tr><td>4. Digits</td><td>Number row with correct fingers; keypad if relevant</td><td>97% accuracy on a numbers round</td></tr>"
                "<tr><td>5. Speed</td><td>30-second sprints plus slow accuracy rounds</td><td>Sprint peak 10-15 WPM above sustained</td></tr></table>",
            ]},
            {"h2": "What to skip, and in what order", "p": [
                "Skip alternative layouts (Dvorak, Colemak) until you are past 60 WPM on QWERTY. Switching early means paying the learning cost twice and measuring neither. Skip code typing until you can type sentences without looking, because brackets make a hard task harder.",
                "Do not skip the digits stage even if your job seems prose-only. Every real document contains a date or an amount, and the number row is where untrained typists lose the most accuracy.",
            ]},
            {"h2": "A four-week schedule that fits a working day", "p": [
                "Week 1: two minutes home row, three minutes normal text, one minute covered. Week 2: add the row you miss most, keep the covered round. Week 3: punctuation and capitals in sentences, plus a numbers round every other day. Week 4: five-minute rounds and one full test as a checkpoint.",
                "Fifteen minutes a day is enough. The variable that predicts progress is not session length but the number of days you show up.",
            ]},
            {"h2": "How to know the tutorial worked", "p": [
                "Two checks. First, you can type a sentence with your hands covered at 90% of your normal accuracy. Second, your five-minute net score improved by at least 5 WPM since the start.",
                "If neither happened, the cause is almost always that the covered round got dropped. It is the least pleasant part of the tutorial and the only part that removes the ceiling.",
            ]},
        ],
        "faq": [
            {"q": "How long does a typing tutorial take?", "a": "Four to six weeks at 15 minutes a day to go from two-finger typing to sentences without looking. Speed beyond that comes from months of regular practice rather than more lessons."},
            {"q": "Should I learn Dvorak or Colemak instead of QWERTY?", "a": "Not before 60 WPM on QWERTY. Switching early doubles the learning cost and prevents a clean comparison."},
            {"q": "Do I need to learn the number row?", "a": "Yes. Dates, amounts and reference codes appear in almost every real document, and the number row is where untrained typists lose accuracy first."},
            {"q": "What is the most important drill?", "a": "The covered round. It is the only one that removes the look-at-keyboard habit, which is what caps most people at 35-40 WPM."},
            {"q": "Is this tutorial free?", "a": "Yes, with no account. Each stage links to the test mode it needs, and results stay in your browser."},
        ],
    },
    "typing-tutor.html": {
        "seo": [
            {"h2": "What a tutor does that software cannot", "p": [
                "Software measures output: WPM, accuracy, which keys you miss. A tutor watches process: posture, whether the same hand presses Shift, whether you look down before or after an error, whether you tense your shoulders when the timer starts.",
                "That distinction matters because most adult blockers are process problems. A typist who types at 45 WPM with all ten fingers and no looking has a posture or tension problem, and no amount of drill volume fixes it.",
            ]},
            {"h2": "What a diagnosis should contain", "p": [
                "<ul><li><strong>Baseline:</strong> five-minute net WPM, accuracy, and the same on a numbers round.</li>"
                "<li><strong>Technique observations:</strong> finger assignment, Shift hand, looking frequency, wrist position.</li>"
                "<li><strong>Error pattern:</strong> which characters cluster in the error report, not just how many.</li>"
                "<li><strong>Prescription:</strong> two or three drills, not a course. Anything more will not be done.</li></ul>",
                "If an assessment gives you a number and a course to buy, it is a sales funnel rather than a diagnosis.",
            ]},
            {"h2": "Choosing a tutor, or self-tutoring", "p": [
                "A good tutor will ask what you type and why before testing you, and will spend most of the first session watching rather than timing. Ask whether they teach touch typing from scratch or fix existing habits - the second is harder and rarer.",
                "Self-tutoring works if you follow three rules: measure the same way every week, change one variable at a time, and keep a covered round in every session. The data does the diagnosing; you just have to write it down.",
            ]},
            {"h2": "Using this site as the measurement layer", "p": [
                "Run a five-minute test at the start of each week and record net WPM, accuracy and the two slowest keys from the results panel. That is enough data to see whether a drill is working after three weeks.",
                "For the drills themselves, the <a href=\"touch-typing-course.html\">touch typing course</a> is structured, and the <a href=\"typing-speed-exercises.html\">typing speed exercises</a> page covers the ones that target specific weaknesses.",
            ]},
        ],
        "faq": [
            {"q": "Do I need a typing tutor?", "a": "Not if you are progressing: weekly measurements and a covered round are enough. A tutor helps when you are stuck at the same speed for months with correct technique, or when posture and tension are the problem."},
            {"q": "What should a first session cover?", "a": "Mostly observation: a baseline five-minute score, finger assignment, Shift hand, how often you look down, and where your errors cluster. A number alone is not a diagnosis."},
            {"q": "Can software replace a tutor?", "a": "For measurement, yes - it is more consistent than a person. For technique and posture, no: software cannot see your hands or your shoulders."},
            {"q": "How often should I be re-tested?", "a": "Weekly, always the same length and time of day. Every six weeks, add a numbers round and one unfamiliar-keyboard round."},
            {"q": "Is this page a tutor service?", "a": "No. It is the test and measurement layer. There is no account, no coaching product and no data leaving your browser."},
        ],
    },
    "pangram-typing-test.html": {
        "seo": [
            {"h2": "Why pangrams are the best warm-up", "p": [
                "A pangram contains every letter of the alphabet at least once. That makes it the shortest text that touches every key you own, which is exactly what a warm-up should do: no letter gets skipped because the passage happened not to contain it.",
                "It also exposes weak keys honestly. On ordinary prose you can drift for a minute without pressing Q, X or Z; on a pangram you press all of them, and the error report has something to say.",
            ]},
            {"h2": "The pangrams worth using", "p": [
                "<table><tr><th>Pangram</th><th>Why use it</th></tr>"
                "<tr><td>The quick brown fox jumps over the lazy dog</td><td>The classic - short, all 26 letters, quick to finish</td></tr>"
                "<tr><td>Sphinx of black quartz, judge my vow</td><td>Shorter, punctuation included, good for a 15-second round</td></tr>"
                "<tr><td>Pack my box with five dozen liquor jugs</td><td>Letter-dense with unusual letters in the home-row reach</td></tr>"
                "<tr><td>How vexingly quick daft zebras jump</td><td>Modern, all 26 letters, tests the Z and X reaches</td></tr>"
                "<tr><td>Waltz, bad nymph, for quick jigs vex</td><td>Short and punctuation-heavy</td></tr></table>",
                "Use two or three rather than all sixteen. Repetition of the same pangram is what builds the reflex; variety only prevents boredom.",
            ]},
            {"h2": "How to use them without fooling yourself", "p": [
                "A pangram round is short, so it reads high - typically 5-10 WPM above your five-minute score. Use it as a warm-up and a key check, never as the number you quote.",
                "Best routine: one pangram at maximum speed to wake up, one at 80% pace with zero errors, then normal text for the actual measurement.",
            ]},
            {"h2": "Where pangrams come from", "p": [
                "The quick brown fox dates from the late nineteenth century and was used to test typewriters and telegraphs; the shorter ones are modern inventions written to be typed. All of them are public domain and safe to reproduce.",
            ]},
        ],
        "faq": [
            {"q": "What is a pangram typing test?", "a": "A test using sentences that contain every letter of the alphabet, so one short round touches every key and exposes weak ones."},
            {"q": "What is the shortest pangram?", "a": "The shortest commonly used ones are around 30 letters, such as \"Waltz, bad nymph, for quick jigs vex\". The classic quick brown fox is 35 letters plus spaces."},
            {"q": "Why is my pangram score higher than my normal score?", "a": "Short rounds avoid fatigue and drift, and a memorised sentence is easier to type than unfamiliar prose. Expect 5-10 WPM above a five-minute score."},
            {"q": "How many pangrams should I practise?", "a": "Two or three. Repeating the same one builds the reflex; cycling through many mainly prevents boredom."},
            {"q": "Is this pangram test free?", "a": "Yes, no account needed, and the pool includes sixteen pangrams from the classic quick brown fox to modern short ones."},
        ],
    },
    "bank-typing-test.html": {
        "seo": [
            {"h2": "What bank clerical tests actually require", "p": [
                "Indian bank clerical recruitment commonly quotes 30 words per minute in English or 25 words per minute in Hindi, tested on a standard keyboard for a fixed period, with a small error allowance. Probationary officer and specialist officer posts generally do not include a typing test; clerical and some office-assistant posts do.",
                "These figures appear in recruitment notifications rather than in a single national standard, so the notice for your cycle is the authority. Read it before you practise: the language, layout and error allowance all change between years.",
            ]},
            {"h2": "What the test looks like on the day", "p": [
                "<table><tr><th>Element</th><th>Typical form</th></tr>"
                "<tr><td>Mode</td><td>Copy typing from a printed or on-screen passage</td></tr>"
                "<tr><td>Language</td><td>English or Hindi, chosen at application</td></tr>"
                "<tr><td>Duration</td><td>A fixed period, often around ten minutes</td></tr>"
                "<tr><td>Scoring</td><td>Words per minute with an error allowance</td></tr>"
                "<tr><td>Outcome</td><td>Qualifying - it does not add marks to the merit list</td></tr></table>",
                "Because it is qualifying, the strategy is accuracy at a comfortable pace, not maximum speed. A clean 32 WPM passes; a 45 WPM run with 10% errors does not.",
            ]},
            {"h2": "Practising for the format", "p": [
                "Use full-length rounds, not one-minute bursts. The error rate at minute eight is what decides the result, and it is invisible in a short round. Type passages with punctuation and capitals, since the actual passage includes them.",
                "Add a Hindi round if you are taking the Hindi option, on the layout named in your notice - Krutidev, Remington or InScript are not interchangeable, and learning the wrong one creates conflicting reflexes.",
            ]},
            {"h2": "Cross-checking with other exams", "p": [
                "Bank clerical requirements are close to SSC CHSL: both ask around 30-35 WPM and both are qualifying. The <a href=\"ssc-chsl-typing-test.html\">SSC CHSL page</a> covers the 35/30 WPM and 8000 key-depression split in detail, and the <a href=\"government-typing-test.html\">government typing test</a> page covers the general civil-service format.",
            ]},
        ],
        "faq": [
            {"q": "What typing speed do bank exams require?", "a": "Commonly 30 words per minute in English or 25 in Hindi for clerical posts, with a small error allowance. The recruitment notice for your cycle states the exact figure."},
            {"q": "Do bank PO exams include a typing test?", "a": "Generally no. Clerical and some office-assistant posts include a qualifying typing test; probationary officer and specialist officer posts usually do not."},
            {"q": "Is the bank typing test qualifying or merit?", "a": "Qualifying. It does not add marks to your total, which is why accuracy at a comfortable pace beats a fast, error-heavy run."},
            {"q": "Which language should I choose?", "a": "Whichever you type faster and more accurately. Hindi requires 25 WPM against 30 for English, but only if you are fluent in the layout your notice specifies."},
            {"q": "How long should I practise per session?", "a": "Full-length rounds of about ten minutes, three times a week, plus five minutes of accuracy work daily. Short bursts do not reveal the errors that appear late in a real test."},
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
        body = sum(len(x) for s in patch["seo"] for x in s["p"])
        if body < 1600:
            errs.append(f"{f}: 新正文 {body} < 1600")
        if len(patch["faq"]) < 5:
            errs.append(f"{f}: FAQ 不足 5")
    if errs:
        for e in errs:
            print("  ·", e)
        print("❌ 未写入")
        return 1
    if "--check" in sys.argv:
        print("✅ 校验通过")
        return 0
    for f, patch in PATCH.items():
        pages[f].update(patch)
    CFG.write_text(json.dumps(cfg, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"已补厚 {len(PATCH)} 页")
    return 0


if __name__ == "__main__":
    sys.exit(main())
